from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import run_tests
from case_catalog import phase_for


def attempt(identifier: str, phase: str, status: str, iteration: int = 1) -> dict:
    return {"id": identifier, "phase": phase, "status": status, "iteration": iteration,
            "seed": 23 + iteration, "clock": run_tests.DEFAULT_CLOCK,
            "seconds": 0.001, "diagnostics": ["Synthetic injected failure"] if status != "pass" else [],
            "stdout": "", "stderr": "", "warnings": []}


class RunnerCase(unittest.TestCase):
    def campaign(self, outcome=None, incomplete: bool = False, discovery_error: bool = False,
                 acceptance: bool = False, portal_status: str | None = None):
        phases = {"negative": [Mock(id=Mock(return_value="synthetic.negative"))],
                  "positive": [Mock(id=Mock(return_value="synthetic.positive"))]}
        calls = []

        def fake_process(command, **_kwargs):
            phase = command[command.index("--_worker") + 1]
            iteration = int(command[command.index("--_iteration") + 1])
            journal = Path(command[command.index("--_journal") + 1])
            calls.append(phase)
            status = outcome(phase, iteration) if outcome else "pass"
            rows = [] if incomplete and phase == "negative" else [
                attempt("synthetic." + phase, phase, status, iteration)]
            journal.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            return Mock(returncode=0, stderr="")

        with tempfile.TemporaryDirectory(prefix="finops-runner-test-") as directory:
            root = Path(directory)
            arguments = ["--repeat", "2", "--out-dir", str(root)]
            if not acceptance:
                arguments += ["--offline-only"]
            if portal_status is not None:
                arguments += ["--portal-config", str(root / "operator-config.json"),
                              "--portal-mode", "live" if portal_status == "LIVE_PORTAL_PARITY_PASS" else "evidence"]
            with patch.object(run_tests, "discover", side_effect=ValueError("Synthetic discovery failure")
                              if discovery_error else None, return_value=phases), \
                    patch.object(run_tests, "fingerprint", return_value={"sha256": "synthetic", "files": {}}), \
                    patch.object(run_tests.subprocess, "run", side_effect=fake_process), \
                    patch.object(run_tests, "run_portal_stage", return_value={"status": portal_status}) as portal, \
                    patch("sys.stdout", new_callable=io.StringIO):
                status = run_tests.main(arguments)
            run = next(root.iterdir())
            report = json.loads((run / "report.json").read_text(encoding="utf-8"))
            files = sorted(path.name for path in run.iterdir())
            text = (run / "report.md").read_text(encoding="utf-8")
            report["testPortalStageCalls"] = portal.call_count
        return status, report, files, text, calls


class NegativeRunnerTests(RunnerCase):
    phase = "negative"

    def test_unclassified_test_cannot_silently_run_in_the_wrong_phase(self):
        with self.assertRaisesRegex(ValueError, "Unclassified"):
            phase_for("future_suite.TestThing.test_negative_in_name_only", None)
        with self.assertRaisesRegex(ValueError, "Unclassified"):
            phase_for("test_finops.NewTests.test_unknown", "negative")

    def test_negative_failure_does_not_skip_other_negatives_or_turn_green(self):
        status, report, files, _, calls = self.campaign(
            lambda phase, _iteration: "failure" if phase == "negative" else "pass")
        self.assertEqual(status, 1)
        self.assertEqual(report["verdict"], "FAIL")
        self.assertTrue(report["negativeComplete"])
        self.assertEqual(calls, ["negative", "negative", "positive", "positive"])
        self.assertIn("negative-01.md", files)
        self.assertIn("negative-02.md", files)

    def test_incomplete_negative_journal_blocks_every_positive_sweep(self):
        status, report, _, _, calls = self.campaign(incomplete=True)
        self.assertEqual(status, 1)
        self.assertFalse(report["negativeComplete"])
        self.assertEqual(calls, ["negative", "negative"])
        self.assertIn("BLOCKED", report["positiveStatus"])

    def test_skipped_negative_is_incomplete_not_a_pass(self):
        status, report, _, _, calls = self.campaign(
            lambda phase, _iteration: "skip" if phase == "negative" else "pass")
        self.assertEqual(status, 1)
        self.assertFalse(report["negativeComplete"])
        self.assertEqual(calls, ["negative", "negative"])

    def test_flaky_pass_fail_is_never_retried_to_a_green_verdict(self):
        status, report, _, text, _ = self.campaign(
            lambda phase, iteration: "failure" if phase == "negative" and iteration == 1 else "pass")
        self.assertEqual(status, 1)
        flaky = [case for case in report["caseSummary"] if case["stability"] == "observed-flaky"]
        self.assertEqual([case["id"] for case in flaky], ["synthetic.negative"])
        self.assertIn("observed-flaky", text)

    def test_discovery_error_still_persists_a_test_report(self):
        status, report, files, text, calls = self.campaign(discovery_error=True)
        self.assertEqual(status, 2)
        self.assertEqual(report["verdict"], "RUNNER ERROR")
        self.assertEqual(calls, [])
        self.assertIn("report.json", files)
        self.assertIn("Synthetic discovery failure", text)

    def test_expected_failure_is_not_counted_as_exhausted_negative_coverage(self):
        status, report, _, _, calls = self.campaign(
            lambda phase, _iteration: "expected-failure" if phase == "negative" else "pass")
        self.assertEqual(status, 1)
        self.assertFalse(report["negativeComplete"])
        self.assertEqual(calls, ["negative", "negative"])

    def test_no_positive_only_bypass_is_in_the_schedule(self):
        self.assertEqual(run_tests.schedule(3, True), [("negative", 1), ("negative", 2), ("negative", 3)])
        with self.assertRaises(ValueError):
            run_tests.schedule(0, False)

    def test_changed_source_context_is_not_mislabeled_as_flakiness(self):
        first = attempt("same", "negative", "failure")
        second = {**attempt("same", "negative", "pass", 2), "contextComparable": False}
        self.assertEqual(run_tests.summarize([first, second])[0]["stability"], "not-comparable-context-changed")

    def test_missing_portal_inputs_cannot_pass_acceptance(self):
        status, report, _, _, _ = self.campaign(acceptance=True)
        self.assertEqual(status, 2)
        self.assertIn("BLOCKED", report["verdict"])
        self.assertFalse(report["acceptanceValidated"])
        self.assertEqual(report["testPortalStageCalls"], 0)

    def test_portal_mismatch_is_not_hidden_by_green_offline_tests(self):
        status, report, _, _, _ = self.campaign(acceptance=True, portal_status="MISMATCH")
        self.assertEqual(status, 1)
        self.assertFalse(report["acceptanceValidated"])
        self.assertEqual(report["verdict"], "FAIL (PORTAL MISMATCH)")

    def test_offline_failures_block_live_queries(self):
        status, report, _, _, _ = self.campaign(
            lambda phase, _iteration: "failure" if phase == "negative" else "pass",
            acceptance=True, portal_status="LIVE_PORTAL_PARITY_PASS")
        self.assertEqual(status, 1)
        self.assertEqual(report["testPortalStageCalls"], 0)


class PositiveRunnerTests(RunnerCase):
    phase = "positive"

    def test_fingerprint_includes_every_discoverable_skill(self):
        snapshot = run_tests.fingerprint()
        skills = run_tests.WORKSPACE / ".github" / "skills"
        for path in skills.glob("*\\SKILL.md"):
            with self.subTest(path=path):
                self.assertIn(str(path.relative_to(run_tests.WORKSPACE)), snapshot["files"])

    def test_fingerprint_includes_setup_server_and_browser_assets(self):
        snapshot = run_tests.fingerprint()
        directory = run_tests.WORKSPACE / "tools" / "verification_setup"
        for path in [directory / "server.py", *(directory / "static").glob("*")]:
            with self.subTest(path=path):
                self.assertIn(str(path.relative_to(run_tests.WORKSPACE)), snapshot["files"])

    def test_every_sweep_and_the_campaign_have_markdown_and_json_reports(self):
        status, report, files, _, calls = self.campaign()
        self.assertEqual(status, 0)
        self.assertEqual(calls, ["negative", "negative", "positive", "positive"])
        for stem in ("negative-01", "negative-02", "positive-01", "positive-02", "report"):
            self.assertIn(stem + ".md", files)
            self.assertIn(stem + ".json", files)
        self.assertTrue(report["negativeComplete"])

    def test_consistently_passing_test_is_only_stable_in_the_sample(self):
        results = [attempt("same", "negative", "pass", n) for n in range(1, 4)]
        summary = run_tests.summarize(results)
        self.assertEqual(summary[0]["stability"], "stable-in-sample")
        self.assertEqual(run_tests.summarize(results[:1])[0]["stability"], "insufficient-repetitions")

    def test_repeated_deterministic_failure_is_not_called_flaky(self):
        results = [attempt("same", "negative", "failure", n) for n in range(1, 4)]
        self.assertEqual(run_tests.summarize(results)[0]["stability"], "consistent-failure")

    def test_supplied_evidence_pass_is_not_labeled_live(self):
        status, report, _, _, _ = self.campaign(acceptance=True, portal_status="CAPTURED_PORTAL_PARITY_PASS")
        self.assertEqual(status, 0)
        self.assertTrue(report["acceptanceValidated"])
        self.assertFalse(report["livePortalValidated"])
        self.assertIn("LIVE REQUERY NOT RUN", report["verdict"])

    def test_explicit_live_stage_pass_is_reported_separately(self):
        status, report, _, _, _ = self.campaign(acceptance=True, portal_status="LIVE_PORTAL_PARITY_PASS")
        self.assertEqual(status, 0)
        self.assertTrue(report["acceptanceValidated"])
        self.assertTrue(report["livePortalValidated"])
        self.assertEqual(report["verdict"], "PASS (LIVE PORTAL PARITY)")

    def test_offline_only_pass_is_explicitly_not_acceptance(self):
        status, report, _, _, _ = self.campaign()
        self.assertEqual(status, 0)
        self.assertFalse(report["acceptanceValidated"])
        self.assertIn("PORTAL PARITY NOT VALIDATED", report["verdict"])
