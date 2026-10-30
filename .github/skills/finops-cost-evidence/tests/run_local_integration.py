"""Real CLI and installed-browser checks using synthetic evidence; never query Azure."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import test_finops as fixture
from run_tests import fingerprint


ROOT = Path(__file__).resolve().parents[4]
HELPER = fixture.SCRIPTS / "finops.py"
PORTAL = fixture.SCRIPTS / "portal_validation.py"


def save(directory: Path, report: dict) -> None:
    lines = ["# FinOps real local-tool integration", "", f"**Status: {report['status']}**", "",
             "- All inputs are synthetic. No Azure CLI login, Azure API, directory, or ServiceNow connection is used.",
             "- Subprocess CLI invocations and, when selected, browser/PDF generation are real, not mocked.",
             f"- Source: {report['source']['sha256']}", "", "| Case | Phase | Expected exit | Actual exit | Result |",
             "|---|---|---:|---:|---|"]
    for case in report["results"]:
        lines.append(f"| {case['id']} | {case['phase']} | {case['expectedExit']} | {case['actualExit']} | {case['status']} |")
    if report.get("pdf"):
        lines += ["", "## Actual PDF", "", json.dumps(report["pdf"], ensure_ascii=True)]
    if report.get("error"):
        lines += ["", "## Error", "", report["error"]]
    for name, value in (("report.json", json.dumps(report, indent=2, ensure_ascii=True) + "\n"),
                        ("report.md", "\n".join(lines) + "\n")):
        temporary = directory / (name + ".tmp")
        temporary.write_text(value, encoding="utf-8")
        temporary.replace(directory / name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", type=Path)
    parser.add_argument("--negative-only", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=ROOT / ".finops-runs" / "local-integration")
    args = parser.parse_args(argv)
    directory = args.out_dir.resolve() / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    directory.mkdir(parents=True)
    report = {"schemaVersion": 1, "status": "RUNNING", "source": fingerprint(), "results": [],
              "liveAzure": "NOT RUN", "portalParity": "NOT VALIDATED"}
    save(directory, report)
    print(f"Local-tool integration report: {directory}", flush=True)

    def run(identifier, phase, script, arguments, expected):
        completed = subprocess.run([sys.executable, "-B", str(script), *map(str, arguments)],
                                   capture_output=True, text=True, encoding="utf-8", timeout=150, check=False)
        (directory / (identifier + ".stdout.txt")).write_text(completed.stdout, encoding="utf-8")
        (directory / (identifier + ".stderr.txt")).write_text(completed.stderr, encoding="utf-8")
        result = {"id": identifier, "phase": phase, "expectedExit": expected, "actualExit": completed.returncode,
                  "status": "PASS" if completed.returncode == expected else "FAIL"}
        report["results"].append(result)
        save(directory, report)
        if result["status"] != "PASS" and phase == "positive":
            raise AssertionError(f"{identifier} exited {completed.returncode}; expected {expected}.")

    try:
        scenario, catalog = fixture.scenario(), fixture.catalog()
        for name, value in (("scenario.json", scenario), ("catalog.json", catalog)):
            fixture.finops.write_json(directory / name, value)
        fixture.finops.write_json(directory / "actual.json", fixture.bundle_for())
        (directory / "malformed.json").write_text("{broken", encoding="utf-8")
        existing = directory / "existing.md"
        existing.write_text("DO NOT CHANGE", encoding="utf-8")
        stub = HELPER.parent.parent / "assets" / "portal-validation.example.json"
        negatives = [
            ("missing-file", HELPER, ["report", "--actual", directory / "absent.json", "--out", directory / "missing.md"], 2),
            ("invalid-json", HELPER, ["report", "--actual", directory / "malformed.json", "--out", directory / "invalid.md"], 2),
            ("overwrite", HELPER, ["report", "--actual", directory / "actual.json", "--out", existing], 2),
            ("unsupported-format", HELPER, ["report", "--actual", directory / "actual.json", "--format", "docx",
                                          "--out", directory / "unsupported.docx"], 2),
            ("invalid-identity-input", HELPER, ["identity", "--tenant", "invalid", "--subscription", fixture.SUB,
                                              "--out", directory / "identity.json"], 2),
            ("missing-pdf-browser", HELPER, ["report", "--actual", directory / "actual.json", "--format", "pdf",
                                           "--out", directory / "missing.pdf"], 2),
            ("nonexistent-pdf-browser", HELPER, ["report", "--actual", directory / "actual.json", "--format", "pdf",
                                               "--browser", directory / "not-installed.exe", "--out", directory / "absent.pdf"], 2),
            ("sample-evidence-rejected", PORTAL, ["--config", stub, "--mode", "evidence",
                                                "--out-dir", directory / "sample-evidence"], 2),
            ("sample-live-rejected", PORTAL, ["--config", stub, "--mode", "live", "--confirm-live-plan", "not-approved",
                                            "--out-dir", directory / "sample-live"], 2),
        ]
        for identifier, script, arguments, expected in negatives:
            run(identifier, "negative", script, arguments, expected)
        assert existing.read_text(encoding="utf-8") == "DO NOT CHANGE"
        for root in ("sample-evidence", "sample-live"):
            result = json.loads(next((directory / root).glob("*\\report.json")).read_text(encoding="utf-8"))
            assert result["status"] == "BLOCKED" and not result["liveQueryAttempted"]
        report["negativeComplete"] = True
        save(directory, report)
        if any(result["status"] != "PASS" for result in report["results"]):
            report["status"] = "FAIL (NEGATIVE TOOL CHECKS)"
            save(directory, report)
            return 1
        if args.negative_only:
            report["status"] = "PASS (NEGATIVE ONLY)"
            save(directory, report)
            return 0
        run("resolve", "positive", HELPER, ["resolve", "--scenario", directory / "scenario.json",
                                          "--catalog", directory / "catalog.json", "--out", directory / "manifest.json"], 0)
        run("plan", "positive", HELPER, ["plan", "--manifest", directory / "manifest.json",
                                       "--out", directory / "plan.json"], 0)
        plan = fixture.finops.read_json(directory / "plan.json")
        actual = fixture.bundle_for(plan)
        fixture.finops.write_json(directory / "planned-actual.json", actual)
        index = {"source": "manual-azure-cli", "tenantId": fixture.TENANT, "principalId": fixture.INVOKER,
                 "capturedAt": fixture.AS_OF, "captures": []}
        for number, capture in enumerate(actual["captures"]):
            page = capture["pages"][0]
            name = f"synthetic-reference-{number}.json"
            (directory / name).write_text(page["raw"], encoding="utf-8")
            index["captures"].append({"requestId": capture["requestId"], "pages": [
                {"path": name, "url": page["url"], "status": 200}]})
        fixture.finops.write_json(directory / "index.json", index)
        run("import-reference", "positive", HELPER, ["import-reference", "--plan", directory / "plan.json",
                                                   "--index", directory / "index.json", "--out", directory / "reference.json"], 0)
        run("reconcile", "positive", HELPER, ["reconcile", "--actual", directory / "planned-actual.json",
                                            "--reference", directory / "reference.json", "--out", directory / "comparison.json"], 0)
        for format_, name in (("markdown", "workload.md"), ("html", "workload.html")):
            run("report-" + format_, "positive", HELPER, ["report", "--actual", directory / "planned-actual.json",
                "--format", format_, "--out", directory / name], 0)
            text = (directory / name).read_text(encoding="utf-8")
            assert "0.008" in text and "$0.01" in text and "UNVERIFIED" in text
        if args.browser is None:
            report["pdf"] = {"status": "NOT RUN", "reason": "No installed browser explicitly selected."}
        else:
            run("report-pdf", "positive", HELPER, ["report", "--actual", directory / "planned-actual.json",
                "--format", "pdf", "--browser", args.browser, "--out", directory / "workload.pdf"], 0)
            data = (directory / "workload.pdf").read_bytes()
            assert data.startswith(b"%PDF-") and len(data) > 1000
            report["pdf"] = {"status": "REAL PDF CREATED", "bytes": len(data), "browser": str(args.browser)}
            try:
                from pypdf import PdfReader
            except ImportError:
                report["pdf"]["textVerification"] = "NOT RUN: pypdf not installed; no automatic installation."
            else:
                reader = PdfReader(directory / "workload.pdf")
                text = "\n".join(page.extract_text() for page in reader.pages)
                assert "0.008" in text and "$0.01" in text and "UNVERIFIED" in text
                assert fixture.SUB in text
                report["pdf"].update(textVerification="PASS", pages=len(reader.pages))
        report["status"] = "PASS (SYNTHETIC LOCAL TOOLS; LIVE PARITY NOT VALIDATED)"
        if fingerprint()["sha256"] != report["source"]["sha256"]:
            report.update(status="NOT COMPARABLE", error="Source changed during local integration.")
        save(directory, report)
        return 0
    except (AssertionError, OSError, ValueError, subprocess.SubprocessError) as exc:
        report.update(status="FAIL", error=str(exc))
        save(directory, report)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
