"""Compare authoritative Azure Portal evidence with saved or freshly queried costs."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal, localcontext
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import finops


Json = dict[str, Any]
def no_secrets(value: Any) -> None:
    finops.no_secrets(value)


def real_document(value: Json, label: str) -> None:
    finops.require(type(value.get("schemaVersion")) is int and value["schemaVersion"] == 1,
                   f"Unsupported {label} schema.")
    finops.require(value.get("isExample") is False,
                   f"{label} is a sample or is not explicitly marked authoritative; replace the stub.")
    no_secrets(value)


def local_file(directory: Path, value: str) -> Path:
    finops.require(isinstance(value, str) and bool(value.strip()) and "<" not in value and ">" not in value,
                   "Replace all evidence path placeholders.")
    path = (directory / value).resolve()
    finops.require(not str(path).startswith("\\\\") and path.is_file(), f"Local evidence file missing: {path}.")
    return path


def bounded_time(value: str, now: datetime, maximum_age: int, label: str) -> None:
    age = (now - finops.timestamp(value)).total_seconds()
    finops.require(0 <= age <= maximum_age, f"{label} is future-dated or older than the approved age limit.")


def load_inputs(config_path: Path, mode: str, confirm_live_plan: str | None) -> Json:
    finops.require(mode in ("evidence", "live"), "Choose evidence or live Portal validation.")
    config = finops.read_json(config_path)
    real_document(config, "Portal validation config")
    allowed = {"schemaVersion", "isExample", "planPath", "portalIndexPath", "actualPath",
               "approvedPlanSha256", "maxEvidenceAgeSeconds", "liveApproval"}
    finops.require(not set(config) - allowed, "Unknown Portal validation config fields.")
    age = config["maxEvidenceAgeSeconds"]
    finops.require(type(age) is int and age > 0, "Specify a positive approved evidence age in seconds.")
    root = config_path.resolve().parent
    plan_path = local_file(root, config["planPath"])
    plan = finops.read_json(plan_path)
    finops.require(isinstance(plan.get("manifest"), dict), "The plan manifest must be an object.")
    finops.verify_plan(plan)
    finops.require(config["approvedPlanSha256"] == plan["sha256"], "The approved plan hash does not match.")
    manifest = plan["manifest"]
    finops.require(manifest["scopeReference"]["status"] == "exact-match",
                   "Independent exact resource-set verification is required before Portal acceptance.")
    index_path = local_file(root, config["portalIndexPath"])
    index = finops.read_json(index_path)
    real_document(index, "Portal reference index")
    finops.require(index["source"] == "portal-query-export",
                   "A CLI capture is not Azure Portal evidence; use a genuine Portal query export.")
    finops.require(index["tenantId"] == manifest["tenantId"] and index["principalId"] == manifest["principalId"],
                   "Portal reference tenant/invoker differs from the approved plan.")
    attestation = index["attestation"]
    finops.require(isinstance(attestation, dict) and
                   all(attestation.get(k) is True for k in
                       ("exportedFromAzurePortal", "sameViewScopeAndFilters", "noSecretsIncluded")) and
                   attestation.get("confirmedByPrincipalId") == manifest["principalId"],
                   "The invoker must attest Portal origin, matching view/scope, and credential-free evidence.")
    finops.require(isinstance(index["portalViewUrl"], str), "Portal view URL must be a string.")
    portal_url = urlsplit(index["portalViewUrl"])
    finops.require(portal_url.scheme == "https" and portal_url.netloc == "portal.azure.com" and not portal_url.query,
                   "Use a public Azure Portal view URL without credentials or query parameters.")
    now = finops.timestamp(finops.utc_now())
    bounded_time(index["capturedAt"], now, age, "Portal capture")
    bounded_time(attestation["confirmedAt"], now, age, "Portal attestation")
    requests = {r["id"]: r for r in plan["requests"]}
    finops.require(isinstance(index["captures"], list) and bool(index["captures"]), "Portal pages are missing.")
    for capture in index["captures"]:
        finops.require(capture["requestId"] in requests, "Unexpected Portal request.")
        finops.require(capture["requestBody"] == requests[capture["requestId"]]["body"],
                       "Portal request differs from the plan's scope, period, basis, grouping, or filter.")
        finops.require(isinstance(capture["pages"], list) and bool(capture["pages"]), "Portal response pages are missing.")
        for entry in capture["pages"]:
            raw_path = local_file(index_path.parent, entry["path"])
            raw = raw_path.read_text(encoding="utf-8-sig")
            if raw.strip():
                document = finops.parse_json(raw)
                finops.require(document.get("isExample") is not True, "Synthetic sample response is not authoritative.")
                no_secrets(document)
    reference = finops.import_reference(plan, index, index_path.parent)
    reference_data = finops.validate_bundle(reference)
    finops.require(bool(reference_data["ledger"]) and not reference_data["emptyRequests"],
                   "Empty Portal evidence cannot prove live amounts or zero spend.")
    displayed = index["displayedTotals"]
    finops.require(isinstance(displayed, list) and bool(displayed), "Portal displayed totals are required.")
    currencies = []
    for total in displayed:
        finops.require(isinstance(total, dict) and set(total) == {"currency", "amount", "decimalPlaces"},
                       "Each displayed total needs currency, normalized decimal amount, and decimalPlaces.")
        finops.require(isinstance(total["currency"], str) and
                       re.fullmatch(r"[A-Z]{3}", total["currency"]) is not None, "Invalid display currency.")
        places = total["decimalPlaces"]
        finops.require(type(places) is int and 0 <= places <= 8, "Portal display precision must be 0..8 decimal places.")
        finops.require(isinstance(total["amount"], str) and
                       re.fullmatch(r"-?\d+" + (rf"\.\d{{{places}}}" if places else ""), total["amount"]) is not None,
                       "Portal displayed amount must be a decimal string at the declared precision, without symbols/FX.")
        currencies.append(total["currency"])
    finops.unique(currencies, "Portal display currencies")
    finops.require(set(currencies) == set(reference_data["totals"]), "Portal display/raw currency sets differ.")
    actual_path = None
    if mode == "live":
        approval = config["liveApproval"]
        finops.require(isinstance(approval, dict) and approval.get("confirmed") is True,
                       "Live queries require explicit invoker approval, not a sample or agent-inferred consent.")
        finops.require(confirm_live_plan == plan["sha256"], "Supply --confirm-live-plan with the exact approved plan hash.")
        finops.require(approval.get("tenantId") == manifest["tenantId"] and
                       approval.get("principalId") == manifest["principalId"] and
                       approval.get("subscriptionIds") == manifest["subscriptionIds"] and
                       approval.get("planSha256") == plan["sha256"], "Live identity/scope approval does not match.")
        finops.require(finops.timestamp(approval["confirmedAt"]) <= now <= finops.timestamp(approval["expiresAt"]),
                       "Live approval is not yet valid or has expired.")
    else:
        actual_path = local_file(root, config["actualPath"])
    return {"config": config, "plan": plan, "reference": reference, "portalIndex": index,
            "portalIndexSha256": finops.digest(index), "configSha256": finops.digest(config), "actualPath": actual_path}


def compare_amounts(actual: Json, inputs: Json) -> Json:
    finops.require(actual["source"] == "invoker-azure-cli-arm",
                   "The actual capture must be recorded as an invoker-bound Azure query, not synthetic/Portal data.")
    result = finops.validate_bundle(actual)
    finops.require(bool(result["ledger"]) and not result["emptyRequests"],
                   "Empty actual evidence is not proof of zero spend.")
    now = finops.timestamp(finops.utc_now())
    maximum_age = inputs["config"]["maxEvidenceAgeSeconds"]
    bounded_time(result["retrievedFrom"], now, maximum_age, "Actual query")
    bounded_time(inputs["portalIndex"]["capturedAt"], now, maximum_age, "Portal capture")
    comparison = finops.reconcile(actual, inputs["reference"])
    displays = []
    for observed in inputs["portalIndex"]["displayedTotals"]:
        currency, places = observed["currency"], observed["decimalPlaces"]
        amount = result["totals"].get(currency)
        expected = None
        if amount is not None:
            with localcontext() as context:
                context.prec = max(28, len(amount.as_tuple().digits) + max(0, amount.adjusted()) + places + 4)
                expected = amount.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
        displays.append({"currency": currency, "portalDisplayed": observed["amount"],
                         "queryExact": format(amount, "f") if amount is not None else None,
                         "queryDisplay": format(expected, f".{places}f") if expected is not None else None,
                         "decimalPlaces": places,
                         "match": expected is not None and expected == Decimal(observed["amount"])})
    matched = comparison["status"] == "exact-match" and all(row["match"] for row in displays)
    return {"status": "match" if matched else "mismatch", "tolerance": "0",
            "rawRowComparison": comparison, "displayComparisons": displays,
            "rounding": "ROUND_HALF_UP after aggregation; no rounding of source rows",
            "actualSha256": actual["sha256"], "portalReferenceSha256": inputs["reference"]["sha256"]}


def save_report(directory: Path, report: Json) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    lines = ["# Azure Portal parity validation", "", f"**Status: {report['status']}**", "",
             f"- Mode: {report['mode']}", f"- Started: {report['startedAt']}",
             f"- Live Azure query executed this run: {report['liveQueryExecuted']}",
             f"- Identity verified this run: {report['identityVerifiedThisRun']}",
             f"- Portal index hash: {report.get('portalIndexSha256', 'not validated')}",
             f"- Approved plan hash: {report.get('planSha256', 'not validated')}",
             "- Portal origin/display amounts are operator-attested; this does not authenticate a browser export.",
             "- Parity is bounded to captured evidence and freshness limits, not future costs or final invoices.", ""]
    comparison = report.get("comparison")
    if comparison:
        lines += ["| Currency | Exact query amount | Portal displayed | Query display | Match |",
                  "|---|---:|---:|---:|---|"]
        for row in comparison["displayComparisons"]:
            lines.append(f"| {row['currency']} | {row['queryExact']} | {row['portalDisplayed']} | "
                         f"{row['queryDisplay']} | {row['match']} |")
        lines += ["", f"Exact resource/day/region/currency row comparison: {comparison['rawRowComparison']['status']}.",
                  f"Different monetary rows: {len(comparison['rawRowComparison']['differences'])}. Tolerance: 0."]
    if report.get("error"):
        lines += ["", "## Blocking error", "", "```text", report["error"].replace("```", "'''"), "```"]
    for name, text in (("report.json", json.dumps(report, indent=2, ensure_ascii=True) + "\n"),
                       ("report.md", "\n".join(lines) + "\n")):
        temporary = directory / (name + ".tmp")
        temporary.write_text(text, encoding="utf-8")
        temporary.replace(directory / name)


def run_validation(config_path: Path, mode: str, output_dir: Path,
                   confirm_live_plan: str | None = None) -> Json:
    finops.require(not output_dir.exists(), "Use a new Portal validation output directory.")
    report: Json = {"schemaVersion": 1, "status": "RUNNING", "mode": mode, "startedAt": finops.utc_now(),
                    "liveQueryAttempted": False, "liveQueryExecuted": False, "identityVerifiedThisRun": False,
                    "source": finops.source_fingerprint()}
    save_report(output_dir, report)
    try:
        inputs = load_inputs(config_path, mode, confirm_live_plan)
        plan = inputs["plan"]
        report.update({"planSha256": plan["sha256"], "portalIndexSha256": inputs["portalIndexSha256"],
                       "configSha256": inputs["configSha256"],
                       "tenantId": plan["manifest"]["tenantId"], "principalId": plan["manifest"]["principalId"],
                       "subscriptionIds": plan["manifest"]["subscriptionIds"], "period": plan["manifest"]["period"],
                       "costBasis": plan["manifest"]["costBasis"]})
        finops.write_json(output_dir / "portal-reference.json", inputs["reference"])
        if mode == "live":
            manifest = plan["manifest"]
            client = finops.AzureClient(manifest["tenantId"], manifest["principalId"], manifest["subscriptionIds"])
            report["identityVerifiedThisRun"] = True
            report["liveQueryAttempted"] = True
            save_report(output_dir, report)
            actual = finops.execute_plan(plan, client)
            report["liveQueryExecuted"] = True
        else:
            actual = finops.read_json(inputs["actualPath"])
        no_secrets(actual)
        finops.write_json(output_dir / "actual.json", actual)
        report["comparison"] = compare_amounts(actual, inputs)
        finops.require(finops.source_fingerprint()["sha256"] == report["source"]["sha256"],
                       "Source changed during Portal validation; acceptance is invalid.")
        if report["comparison"]["status"] != "match":
            report["status"] = "MISMATCH"
        else:
            report["status"] = "LIVE_PORTAL_PARITY_PASS" if mode == "live" else "CAPTURED_PORTAL_PARITY_PASS"
    except (finops.EvidenceError, OSError, KeyError, TypeError, ValueError) as exc:
        report["status"], report["error"] = "BLOCKED", str(exc)
    except KeyboardInterrupt:
        report["status"], report["error"] = "INTERRUPTED", "Portal validation interrupted; acceptance is incomplete."
        raise
    finally:
        if report["status"] == "RUNNING":
            report["status"], report["error"] = "ERROR", "Portal validation ended without a completed outcome."
        report["completedAt"] = finops.utc_now()
        save_report(output_dir, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--mode", choices=("evidence", "live"), required=True)
    parser.add_argument("--confirm-live-plan")
    parser.add_argument("--out-dir", type=Path, default=Path(".finops-runs") / "portal")
    args = parser.parse_args(argv)
    directory = args.out_dir / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    try:
        report = run_validation(args.config, args.mode, directory, args.confirm_live_plan)
    except KeyboardInterrupt:
        print("Portal validation interrupted; no acceptance claimed.", file=sys.stderr)
        return 130
    except (finops.EvidenceError, OSError) as exc:
        print(f"Portal validation blocked: {exc}", file=sys.stderr)
        return 2
    print(f"{report['status']}: {directory / 'report.md'}")
    return 0 if report["status"].endswith("_PARITY_PASS") else 1 if report["status"] == "MISMATCH" else 2


if __name__ == "__main__":
    raise SystemExit(main())
