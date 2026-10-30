from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import line_coverage
import run_tests
import test_finops as fixture


class PortalStageCase(unittest.TestCase):
    def stage(self, status, mode="evidence", exit_code=0, **changes):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            portal_root = root / "portal-parity" / "test-run"
            portal_root.mkdir(parents=True)
            report = {"status": status, "mode": mode, "liveQueryExecuted": mode == "live",
                      "identityVerifiedThisRun": mode == "live", **changes}
            (portal_root / "report.json").write_text(json.dumps(report), encoding="utf-8")
            with patch.object(run_tests.subprocess, "run", return_value=Mock(returncode=exit_code)):
                return run_tests.run_portal_stage(root / "config.json", mode, None, root)


class NegativePortalStageTests(PortalStageCase):
    phase = "negative"

    def test_evidence_mode_cannot_accept_a_live_pass_from_another_mode(self):
        result = self.stage("LIVE_PORTAL_PARITY_PASS", mode="evidence")
        self.assertEqual(result["status"], "BLOCKED")

    def test_live_mode_cannot_accept_captured_only_pass(self):
        result = self.stage("CAPTURED_PORTAL_PARITY_PASS", mode="live")
        self.assertEqual(result["status"], "BLOCKED")

    def test_live_pass_requires_actual_current_identity_proof(self):
        result = self.stage("LIVE_PORTAL_PARITY_PASS", mode="live", identityVerifiedThisRun=False)
        self.assertEqual(result["status"], "BLOCKED")

    def test_nonzero_process_cannot_produce_a_valid_pass(self):
        self.assertEqual(self.stage("CAPTURED_PORTAL_PARITY_PASS", exit_code=2)["status"], "BLOCKED")

    def test_missing_portal_report_remains_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(run_tests.subprocess, "run", return_value=Mock(returncode=0)):
                result = run_tests.run_portal_stage(Path("absent.json"), "evidence", None, Path(directory))
        self.assertEqual(result["status"], "BLOCKED")

    def test_stage_timeout_is_not_parity(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(run_tests.subprocess, "run",
                              side_effect=run_tests.subprocess.TimeoutExpired("synthetic", 600)):
                result = run_tests.run_portal_stage(Path("absent.json"), "evidence", None, Path(directory))
        self.assertEqual(result["status"], "BLOCKED")


class NegativeCoverageTests(unittest.TestCase):
    phase = "negative"

    def test_coverage_never_counts_unexecuted_lines_as_covered(self):
        source = compile("x = 1\nif x:\n    y = 2\nelse:\n    y = 3\n", "synthetic.py", "exec")
        executable = line_coverage.executable_lines(source)
        self.assertIn(5, executable)
        self.assertNotIn(0, executable)

    def test_coverage_does_not_replace_an_existing_trace_hook(self):
        tracer = lambda *_args: None
        previous = line_coverage.sys.gettrace()
        try:
            line_coverage.sys.settrace(tracer)
            with line_coverage.LineCoverage():
                pass
            self.assertIs(line_coverage.sys.gettrace(), tracer)
        finally:
            line_coverage.sys.settrace(previous)


class PositiveRunnerEdgeTests(PortalStageCase):
    phase = "positive"

    def test_matched_portal_stage_preserves_the_evidence_report_link(self):
        result = self.stage("CAPTURED_PORTAL_PARITY_PASS")
        self.assertEqual(result["status"], "CAPTURED_PORTAL_PARITY_PASS")
        self.assertEqual(result["reportRelativePath"], "portal-parity/test-run/report.md")

    def test_actual_live_stage_requires_both_flags_and_matching_mode(self):
        result = self.stage("LIVE_PORTAL_PARITY_PASS", mode="live")
        self.assertEqual(result["status"], "LIVE_PORTAL_PARITY_PASS")
        self.assertTrue(result["identityVerifiedThisRun"])

    def test_unknown_result_status_is_not_classified_as_a_pass(self):
        result = unittest.TestResult()
        result.addSkip(self, "synthetic")
        self.assertEqual(run_tests.classify(result), "skip")
        result = unittest.TestResult()
        result.addUnexpectedSuccess(self)
        self.assertEqual(run_tests.classify(result), "unexpected-success")

    def test_line_coverage_persists_missing_lines_and_merges_sweeps(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tracker = line_coverage.LineCoverage()
            with tracker:
                fixture.finops.guid(fixture.TENANT)
            tracker.save(root / "first.json")
            data = line_coverage.merge([root / "first.json", root / "first.json"])
            values = data["files"][str(fixture.SCRIPTS.relative_to(line_coverage.ROOT) / "finops.py")]
            self.assertGreater(values["coveredLines"], 0)
            self.assertGreater(len(values["missingLines"]), 0)
            self.assertLess(values["percent"], 100)

    def test_negative_only_and_offline_modes_remain_explicit_in_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch("sys.stdout", new_callable=io.StringIO), patch.object(run_tests, "discover",
                       side_effect=ValueError("synthetic-discovery-error")):
                result = run_tests.main(["--repeat", "1", "--out-dir", str(root), "--offline-only"])
            self.assertEqual(result, 2)
            report = json.loads(next(root.glob("*\\report.json")).read_text(encoding="utf-8"))
            self.assertFalse(report["acceptanceValidated"])
            self.assertEqual(report["verdict"], "RUNNER ERROR")
