"""Run every negative sweep before positive sweeps, retaining a report after each."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import platform
import random
import subprocess
import sys
import time
import traceback
import unittest
import uuid
import warnings
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator
from unittest.mock import patch

from case_catalog import phase_for
from line_coverage import LineCoverage, merge as merge_coverage


TESTS = Path(__file__).resolve().parent
WORKSPACE = TESTS.parents[3]
DEFAULT_CLOCK = "2026-10-30T00:00:00Z"
Json = dict[str, Any]
BAD = {"failure", "error", "unexpected-success"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def flatten(suite: unittest.TestSuite) -> Iterator[unittest.TestCase]:
    for entry in suite:
        if isinstance(entry, unittest.TestSuite):
            yield from flatten(entry)
        else:
            yield entry


def discover() -> dict[str, list[unittest.TestCase]]:
    loader = unittest.TestLoader()
    suite = loader.discover(str(TESTS), pattern="test_*.py")
    if loader.errors:
        raise ValueError("Test discovery failed:\n" + "\n".join(loader.errors))
    phases: dict[str, list[unittest.TestCase]] = {"negative": [], "positive": []}
    seen = set()
    for test in flatten(suite):
        if test.id() in seen:
            raise ValueError(f"Duplicate test ID: {test.id()}.")
        seen.add(test.id())
        phase = phase_for(test.id(), getattr(test, "phase", None))
        phases[phase].append(test)
    if not all(phases.values()):
        raise ValueError("Both negative and positive test catalogs must be nonempty.")
    return phases


def schedule(repeat: int, negative_only: bool) -> list[tuple[str, int]]:
    if repeat < 1:
        raise ValueError("Repetitions must be positive.")
    phases = ("negative",) if negative_only else ("negative", "positive")
    return [(phase, iteration) for phase in phases for iteration in range(1, repeat + 1)]


def summarize(results: list[Json]) -> list[Json]:
    grouped: dict[str, list[Json]] = {}
    for result in results:
        grouped.setdefault(result["id"], []).append(result)
    summary = []
    for identifier, attempts in sorted(grouped.items()):
        statuses = Counter(a["status"] for a in attempts)
        if any(not a.get("contextComparable", True) for a in attempts):
            stability = "not-comparable-context-changed"
        elif statuses["pass"] and any(statuses[s] for s in BAD):
            stability = "observed-flaky"
        elif any(statuses[s] for s in BAD):
            stability = "consistent-failure"
        elif set(statuses) != {"pass"}:
            stability = "incomplete"
        else:
            stability = "stable-in-sample" if len(attempts) >= 2 else "insufficient-repetitions"
        summary.append({"id": identifier, "phase": attempts[0]["phase"], "attempts": len(attempts),
                        "outcomes": dict(statuses), "stability": stability})
    return summary


def classify(result: unittest.TestResult) -> str:
    if result.errors:
        return "error"
    if result.failures:
        return "failure"
    if result.unexpectedSuccesses:
        return "unexpected-success"
    if result.skipped:
        return "skip"
    if result.expectedFailures:
        return "expected-failure"
    return "pass"


def fingerprint() -> Json:
    paths = [WORKSPACE / "README.md", WORKSPACE / "TEST-STRATEGY.md",
             WORKSPACE / ".github" / "agents" / "FinOpsAgent.agent.md"]
    skills = WORKSPACE / ".github" / "skills"
    paths.extend(skills.glob("*\\SKILL.md"))
    paths.extend((TESTS.parent / "scripts").glob("*.py"))
    paths.extend(TESTS.glob("*.py"))
    paths.extend(TESTS.glob("*.json"))
    paths.extend((TESTS.parent / "assets").glob("*.json"))
    paths.extend((TESTS.parent / "references").glob("*.md"))
    setup = WORKSPACE / "tools" / "verification_setup"
    paths.extend(setup.glob("*.py"))
    paths.extend((setup / "static").glob("*"))
    hashes = {str(path.relative_to(WORKSPACE)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(set(paths)) if path.is_file()}
    return {"sha256": hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest(), "files": hashes}


def save_reports(directory: Path, stem: str, report: Json) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    text = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
    target = directory / (stem + ".json")
    temporary = directory / (stem + ".json.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(target)
    temporary = directory / (stem + ".md.tmp")
    temporary.write_text(markdown(report), encoding="utf-8")
    temporary.replace(directory / (stem + ".md"))


def markdown(report: Json) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("|", "&#124;").replace("\r", " ").replace("\n", " ")

    results = report.get("results", [])
    counts = Counter(r["status"] for r in results)
    summaries = summarize(results)
    flaky = [s for s in summaries if s["stability"] == "observed-flaky"]
    lines = ["# FinOpsAgent test report", "", f"**Verdict: {report['verdict']}**", "",
             f"- Run: `{report['runId']}`",
             f"- Started: {report['startedAt']}; updated: {report['updatedAt']}",
             f"- Source fingerprint: `{report['source']['sha256']}`",
             f"- Source remained unchanged during execution: {report.get('sourceStable', True)}",
             f"- Python: {cell(report['environment']['python'])}",
             f"- OS: {cell(report['environment']['platform'])}",
             f"- Frozen offline-test clock (not used by the real Portal stage): {report['clock']}",
             f"- Base order/hash seed: {report['seed']}; requested repetitions: {report['repeat']}",
             "- Offline sweeps: synthetic; real subprocess/network calls blocked only in those workers.",
             f"- Catalog: {report.get('catalogCounts', {})}",
             f"- Attempt outcomes: {dict(counts)}",
             f"- Negative phase exhausted: {report.get('negativeComplete', False)}",
             f"- Positives: {report.get('positiveStatus', 'not started')}",
             f"- Portal parity required: {report.get('portalParityRequired', False)}",
             f"- Portal parity status: {report.get('portalParity', {}).get('status', 'NOT RUN')}",
             f"- Portal stage mode: {report.get('portalParity', {}).get('mode', 'not selected')}",
             f"- Acceptance validated: {report.get('acceptanceValidated', False)}",
             f"- Fresh live Portal parity validated: {report.get('livePortalValidated', False)}",
             f"- Observed flaky tests (same code/environment/clock, varying order/hash seeds): {len(flaky)}", "",
             "## Coverage boundaries", "",
             "- These tests execute deterministic helpers, CLI entry points, fixtures, and test-runner controls.",
             "- Offline sweeps do not authenticate Azure or query billing. Only an explicitly approved live Portal stage does so.",
             "- Supplied-evidence parity compares saved captures; it does not freshly authenticate or query Azure.",
             "- This runner alone does not execute model conversations; consult the separate harness report when available.",
             "- Browser PDF behavior is mocked in this campaign, not validated against an installed browser.",
             "- Exhausted means every defined executable negative case was attempted in every requested sweep, not all possible inputs.",
             "- Repeated green outcomes are evidence of stability in this sample, not proof of no flakiness.", "",
             "## Sweep order", "", "| Phase | Sweep | Attempted / planned | Worker exit |",
             "|---|---:|---:|---:|"]
    portal = report.get("portalParity", {})
    if portal.get("reportRelativePath"):
        lines.insert(lines.index("## Coverage boundaries"),
                     f"[Portal evidence report]({portal['reportRelativePath']})\n")
    if portal.get("error"):
        lines.insert(lines.index("## Coverage boundaries"), f"Portal gate: {cell(portal['error'])}\n")
    for sweep in report.get("sweeps", []):
        lines.append(f"| {sweep['phase']} | {sweep['iteration']} | {sweep['attempted']} / {sweep['planned']} | "
                     f"{sweep.get('exitCode', 'not started')} |")
    lines += ["", "## Failures and observed flakes", ""]
    failures = [s for s in summaries if s["stability"] in (
        "consistent-failure", "observed-flaky", "incomplete", "not-comparable-context-changed")]
    if not failures:
        lines.append("None observed in executed cases. Consult NOT RUN boundaries above.")
    else:
        lines += ["| Test | Phase | Classification | Outcomes |", "|---|---|---|---|"]
        for case in failures:
            lines.append("| " + " | ".join(cell(v) for v in (
                case["id"], case["phase"], case["stability"], case["outcomes"])) + " |")
    lines += ["", "## First failure evidence per test", ""]
    seen = set()
    for result in results:
        if result["status"] not in BAD or result["id"] in seen:
            continue
        seen.add(result["id"])
        lines += [f"### {cell(result['id'])}", "",
                  f"Sweep {result['iteration']}, seed {result['seed']}; {result['status']}.",
                  "", "```text", "\n".join(result["diagnostics"]).replace("```", "'''"), "```", ""]
    if report.get("errors"):
        lines += ["## Runner errors", "", "```text", "\n".join(report["errors"]).replace("```", "'''"), "```"]
    lines += ["", "## All executed test outcomes", "",
              "| Test | Phase | Attempts | Outcomes | Stability |", "|---|---|---:|---|---|"]
    for case in summaries:
        lines.append("| " + " | ".join(cell(v) for v in (
            case["id"], case["phase"], case["attempts"], case["outcomes"], case["stability"])) + " |")
    if report.get("coverage"):
        lines += ["", "## Executable-line coverage", "",
                  "Not branch coverage. Imports and entry points outside test execution may remain uncovered.",
                  "", "| Module | Covered / executable lines | Percent |", "|---|---:|---:|"]
        for name, values in report["coverage"]["files"].items():
            lines.append(f"| {cell(name)} | {values['coveredLines']} / {values['executableLines']} | "
                         f"{values['percent']}% |")
        lines += ["", "Exact uncovered line numbers are retained in the JSON report."]
    return "\n".join(lines) + "\n"


def worker(phase: str, iteration: int, seed: int, clock: str, journal: Path,
           coverage: bool = False) -> int:
    cases = discover()[phase]
    random.Random(seed).shuffle(cases)
    from test_finops import finops

    instant = finops.timestamp(clock).timestamp()
    journal.parent.mkdir(parents=True, exist_ok=True)
    tracker = LineCoverage() if coverage else None
    with contextlib.ExitStack() as stack:
        if tracker is not None:
            stack.enter_context(tracker)
        stack.enter_context(patch.object(finops, "utc_now", return_value=clock))
        stack.enter_context(patch.object(finops.time, "time", return_value=instant))
        for target in ("socket.create_connection", "socket.socket.connect", "subprocess.Popen"):
            stack.enter_context(patch(target, side_effect=AssertionError("Real network/process call in offline test.")))
        with journal.open("x", encoding="utf-8") as output:
            for test in cases:
                started = time.monotonic()
                stdout, stderr = io.StringIO(), io.StringIO()
                result = unittest.TestResult()
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    with warnings.catch_warnings(record=True) as caught:
                        warnings.simplefilter("always")
                        test.run(result)
                diagnostics = [text for _, text in result.failures + result.errors + result.expectedFailures]
                diagnostics.extend(reason for _, reason in result.skipped)
                record = {"id": test.id(), "phase": phase, "iteration": iteration, "seed": seed,
                          "clock": clock, "status": classify(result),
                          "seconds": round(time.monotonic() - started, 6), "diagnostics": diagnostics,
                          "stdout": stdout.getvalue(), "stderr": stderr.getvalue(),
                          "warnings": [str(w.message) for w in caught]}
                output.write(json.dumps(record, ensure_ascii=True) + "\n")
                output.flush()
    if tracker is not None:
        tracker.save(journal.with_suffix(".coverage.json"))
    return 0


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("Use a positive integer.")
    return number


def run_portal_stage(config: Path, mode: str, confirmation: str | None, directory: Path) -> Json:
    portal_root = directory / "portal-parity"
    command = [sys.executable, "-B", str(TESTS.parent / "scripts" / "portal_validation.py"),
               "--config", str(config.resolve()), "--mode", mode, "--out-dir", str(portal_root)]
    if confirmation is not None:
        command += ["--confirm-live-plan", confirmation]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                                   timeout=600, check=False)
    except subprocess.TimeoutExpired:
        return {"status": "BLOCKED", "mode": mode, "error": "Portal validation exceeded 600s."}
    reports = list(portal_root.glob("*\\report.json"))
    if len(reports) != 1:
        return {"status": "BLOCKED", "mode": mode, "error": "Portal validation did not produce exactly one report."}
    result = json.loads(reports[0].read_text(encoding="utf-8"))
    result["reportPath"] = str(reports[0].with_suffix(".md"))
    result["reportRelativePath"] = str(reports[0].with_suffix(".md").relative_to(directory)).replace("\\", "/")
    expected = "LIVE_PORTAL_PARITY_PASS" if mode == "live" else "CAPTURED_PORTAL_PARITY_PASS"
    if result.get("status") == expected:
        live = mode == "live"
        if completed.returncode != 0 or result.get("mode") != mode or \
                result.get("liveQueryExecuted") is not live or result.get("identityVerifiedThisRun") is not live:
            return {"status": "BLOCKED", "mode": mode, "error": "Portal report/exit/identity proof is inconsistent."}
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeat", type=positive_int, default=5)
    parser.add_argument("--seed", type=int, default=1729)
    parser.add_argument("--clock", default=DEFAULT_CLOCK)
    parser.add_argument("--negative-only", action="store_true")
    parser.add_argument("--offline-only", action="store_true",
                        help="Developer checks only; explicitly not Portal/live acceptance.")
    parser.add_argument("--portal-config", type=Path)
    parser.add_argument("--portal-mode", choices=("evidence", "live"), default="evidence")
    parser.add_argument("--confirm-live-plan")
    parser.add_argument("--out-dir", type=Path, default=WORKSPACE / ".finops-runs" / "tests")
    parser.add_argument("--sweep-timeout", type=positive_int, default=120)
    parser.add_argument("--coverage", action="store_true", help="Record standard-library executable-line coverage.")
    parser.add_argument("--_worker", choices=("negative", "positive"), help=argparse.SUPPRESS)
    parser.add_argument("--_iteration", type=int, default=1, help=argparse.SUPPRESS)
    parser.add_argument("--_journal", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args._worker:
        if args._journal is None:
            parser.error("Worker journal is required.")
        return worker(args._worker, args._iteration, args.seed, args.clock, args._journal, args.coverage)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    directory = args.out_dir.resolve() / run_id
    report: Json = {
        "schemaVersion": 1, "runId": run_id, "startedAt": now(), "updatedAt": now(),
        "source": fingerprint(), "environment": {"python": sys.version, "executable": sys.executable,
                                                 "platform": platform.platform()},
        "clock": args.clock, "seed": args.seed, "repeat": args.repeat, "verdict": "RUNNING",
        "negativeComplete": False, "positiveStatus": "not started", "sourceStable": True,
        "portalParity": {"status": "NOT RUN", "mode": args.portal_mode},
        "portalParityRequired": not args.offline_only and not args.negative_only,
        "acceptanceValidated": False, "livePortalValidated": False,
        "results": [], "sweeps": [], "errors": [],
    }
    print(f"Test reports: {directory}", flush=True)
    save_reports(directory, "report", report)
    exit_code = 2
    try:
        if args.offline_only and args.portal_config is not None:
            raise ValueError("--offline-only cannot be combined with --portal-config.")
        datetime.strptime(args.clock, "%Y-%m-%dT%H:%M:%SZ")
        phases = discover()
        report["catalogCounts"] = {p: len(t) for p, t in phases.items()}
        negative_attempts = len(phases["negative"]) * args.repeat
        for phase, iteration in schedule(args.repeat, args.negative_only):
            if phase == "positive":
                negatives = [r for r in report["results"] if r["phase"] == "negative"]
                complete = len(negatives) == negative_attempts and all(
                    r["status"] not in ("skip", "expected-failure") for r in negatives)
                if not complete:
                    report["positiveStatus"] = "BLOCKED: negative execution incomplete"
                    break
                report["negativeComplete"] = True
                report["positiveStatus"] = "running"
            seed = (args.seed + iteration + (100000 if phase == "positive" else 0)) % (2 ** 32)
            stem = f"{phase}-{iteration:02d}"
            journal = directory / (stem + ".jsonl")
            command = [sys.executable, "-B", str(Path(__file__).resolve()), "--_worker", phase,
                       "--_iteration", str(iteration), "--seed", str(seed),
                       "--clock", args.clock, "--_journal", str(journal)]
            if args.coverage:
                command.append("--coverage")
            environment = {**os.environ, "PYTHONHASHSEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1"}
            errors = []
            try:
                completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                                           timeout=args.sweep_timeout, env=environment, check=False)
                code = completed.returncode
                if code:
                    errors.append(f"{stem} worker exited {code}:\n{completed.stderr}")
            except subprocess.TimeoutExpired:
                code = "timeout"
                errors.append(f"{stem} exceeded {args.sweep_timeout}s; positives cannot bypass incomplete negatives.")
            records = [json.loads(line) for line in journal.read_text(encoding="utf-8").splitlines()] if journal.exists() else []
            expected = {test.id() for test in phases[phase]}
            if len(records) != len(expected) or {r["id"] for r in records} != expected:
                errors.append(f"{stem} attempted {len(records)} of {len(expected)} catalog cases.")
            stable = fingerprint()["sha256"] == report["source"]["sha256"]
            if not stable:
                errors.append(f"{stem}: source changed during the campaign; outcomes are not comparable for flakiness.")
                report["sourceStable"] = False
            for record in records:
                record["contextComparable"] = stable
            report["errors"].extend(errors)
            report["results"].extend(records)
            negatives = [r for r in report["results"] if r["phase"] == "negative"]
            report["negativeComplete"] = len(negatives) == negative_attempts and all(
                r["status"] not in ("skip", "expected-failure") for r in negatives)
            report["sweeps"].append({"phase": phase, "iteration": iteration, "seed": seed,
                                     "attempted": len(records), "planned": len(expected), "exitCode": code})
            if args.coverage:
                coverage_path = journal.with_suffix(".coverage.json")
                if not coverage_path.is_file():
                    report["errors"].append(f"{stem}: coverage evidence is missing.")
                report["coverage"] = merge_coverage(list(directory.glob("*.coverage.json")))
            sweep_report = {**report, "results": records, "sweeps": [report["sweeps"][-1]],
                            "verdict": "FAIL" if errors or any(r["status"] != "pass" for r in records) else "PASS",
                            "updatedAt": now()}
            save_reports(directory, stem, sweep_report)
            report["updatedAt"] = now()
            save_reports(directory, "report", report)
            print(f"{stem}: {dict(Counter(r['status'] for r in records))}", flush=True)
            if not stable:
                break
        negatives = [r for r in report["results"] if r["phase"] == "negative"]
        report["negativeComplete"] = len(negatives) == negative_attempts and all(
            r["status"] not in ("skip", "expected-failure") for r in negatives)
        if args.negative_only:
            report["positiveStatus"] = "NOT REQUESTED (negative-only run)"
        elif report["positiveStatus"] == "running":
            report["positiveStatus"] = "completed"
        failed = report["errors"] or any(r["status"] != "pass" for r in report["results"])
        if failed:
            report["verdict"] = "FAIL"
            report["portalParity"] = {"status": "BLOCKED", "mode": args.portal_mode,
                                      "error": "Offline failures/incomplete execution must be resolved first."}
            exit_code = 1
        elif args.negative_only or args.offline_only:
            label = "NEGATIVE ONLY" if args.negative_only else "OFFLINE ONLY"
            report["verdict"] = f"PASS ({label}; PORTAL PARITY NOT VALIDATED)"
            exit_code = 0
        elif args.portal_config is None:
            report["portalParity"] = {"status": "BLOCKED", "mode": args.portal_mode,
                                      "error": "Portal parity is required. Supply --portal-config, or use "
                                               "--offline-only for non-acceptance developer checks."}
            report["verdict"], exit_code = "BLOCKED (PORTAL PARITY REQUIRED)", 2
        else:
            report["portalParity"] = run_portal_stage(args.portal_config, args.portal_mode,
                                                      args.confirm_live_plan, directory)
            if fingerprint()["sha256"] != report["source"]["sha256"]:
                report["sourceStable"] = False
                report["portalParity"] = {"status": "BLOCKED", "mode": args.portal_mode,
                                          "error": "Source changed during Portal validation; acceptance is invalid."}
            status = report["portalParity"]["status"]
            report["livePortalValidated"] = status == "LIVE_PORTAL_PARITY_PASS"
            report["acceptanceValidated"] = status in ("LIVE_PORTAL_PARITY_PASS", "CAPTURED_PORTAL_PARITY_PASS")
            if report["acceptanceValidated"]:
                label = "LIVE PORTAL PARITY" if report["livePortalValidated"] else \
                    "CAPTURED PORTAL EVIDENCE; LIVE REQUERY NOT RUN"
                report["verdict"], exit_code = f"PASS ({label})", 0
            else:
                report["verdict"] = "FAIL (PORTAL MISMATCH)" if status == "MISMATCH" else "BLOCKED (PORTAL PARITY)"
                exit_code = 1 if status == "MISMATCH" else 2
    except KeyboardInterrupt:
        report["verdict"] = "INTERRUPTED"
        report["errors"].append("Interrupted; unattempted cases are not passes.")
        exit_code = 130
    except Exception:
        report["verdict"] = "RUNNER ERROR"
        report["errors"].append(traceback.format_exc())
    finally:
        report["updatedAt"] = now()
        report["caseSummary"] = summarize(report["results"])
        save_reports(directory, "report", report)
        print(f"{report['verdict']}: {directory / 'report.md'}", flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
