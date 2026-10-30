from __future__ import annotations

import copy
import json
import sys
import unittest
from email.message import Message
from pathlib import Path
from unittest.mock import Mock, patch

import test_portal_validation as portal_fixture


sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from tools.verification_setup import server as setup


class SetupCase(portal_fixture.PortalCase):
    def setUp(self):
        super().setUp()
        self.write_inputs()
        self.app = setup.SetupApp(self.root, [self.root])
        self.payload = {
            "mode": "evidence",
            "runner": {"repeat": 1, "seed": 1729, "clock": portal_fixture.CLOCK, "sweepTimeout": 120},
            "planPath": str(self.root / "plan.json"), "actualPath": str(self.root / "actual.json"),
            "approvedPlanSha256": self.plan["sha256"], "maxEvidenceAgeSeconds": 600,
            "referenceMode": "create", "confirmedAt": portal_fixture.CLOCK,
            "attestations": dict.fromkeys(setup.ATTESTATIONS, True),
            "reference": {key: copy.deepcopy(self.index[key]) for key in
                          ("capturedAt", "portalViewUrl", "displayedTotals", "captures")},
        }
        for number, capture in enumerate(self.payload["reference"]["captures"]):
            body = capture.pop("requestBody")
            path = self.root / f"request-body-{number}.json"
            path.write_text(json.dumps(body), encoding="utf-8")
            capture["requestBodyPath"] = str(path)
            for page in capture["pages"]:
                page["path"] = str(self.root / page["path"])

    def offline(self):
        return self.app.prepare({"mode": "offline", "runner": self.payload["runner"]})

    def handler(self, **headers):
        handler = object.__new__(setup.SetupHandler)
        handler.server = Mock(spec=setup.SetupServer, app=self.app, server_port=8765)
        handler.headers = Message()
        for name, value in {"Host": "127.0.0.1:8765", "Origin": "http://127.0.0.1:8765",
                            "X-Setup-Token": self.app.token, **headers}.items():
            handler.headers[name] = value
        return handler

    def write_report(self, identifier, verdict="PASS (OFFLINE ONLY; PORTAL PARITY NOT VALIDATED)",
                     negative_complete=True):
        directory = self.app.run_directory(identifier) / "reports" / "synthetic-campaign"
        directory.mkdir(parents=True)
        report = {"verdict": verdict, "negativeComplete": negative_complete,
                  "acceptanceValidated": False, "livePortalValidated": False, "results": [],
                  "portalParity": {"status": "NOT RUN"}}
        (directory / "report.json").write_text(json.dumps(report), encoding="utf-8")
        return report

    def start_mocked(self, identifier, code=0):
        process = Mock(pid=12345)
        process.wait.return_value = code
        with patch.object(setup.subprocess, "Popen", return_value=process) as launch, \
                patch.object(setup.threading, "Thread"):
            self.app.start(identifier)
        return process, launch


class NegativeSetupTests(SetupCase):
    phase = "negative"

    def test_live_execution_and_unknown_fields_are_rejected(self):
        for changes in ({"mode": "live"}, {"command": "az login"}, {"runner": {"repeat": True}}):
            with self.subTest(changes=changes), self.assertRaises((setup.SetupError, setup.finops.EvidenceError)):
                self.app.prepare({**self.payload, **changes})

    def test_missing_operator_attestation_cannot_generate_authoritative_json(self):
        self.payload["attestations"]["exportedFromAzurePortal"] = False
        with self.assertRaisesRegex(setup.SetupError, "four evidence attestations"):
            self.app.prepare(self.payload)
        self.assertEqual(list(self.app.output.iterdir()), [])

    def test_wrong_approved_plan_hash_is_blocked(self):
        self.payload["approvedPlanSha256"] = "0" * 64
        with self.assertRaisesRegex(setup.SetupError, "approved plan hash"):
            self.app.prepare(self.payload)

    def test_currency_amount_must_remain_a_decimal_string(self):
        self.payload["reference"]["displayedTotals"][0]["amount"] = 0.01
        with self.assertRaisesRegex(setup.finops.EvidenceError, "decimal string"):
            self.app.prepare(self.payload)

    def test_stale_evidence_is_blocked_before_test_invocation(self):
        self.payload["reference"]["capturedAt"] = "2026-09-01T00:00:00Z"
        with patch.object(setup.subprocess, "Popen") as launch:
            with self.assertRaisesRegex(setup.finops.EvidenceError, "age limit"):
                self.app.prepare(self.payload)
        launch.assert_not_called()

    def test_missing_control_request_is_not_a_complete_reference(self):
        self.payload["reference"]["captures"].pop()
        with self.assertRaises(setup.finops.EvidenceError):
            self.app.prepare(self.payload)

    def test_actual_portal_request_body_cannot_be_substituted_by_another_basis(self):
        path = Path(self.payload["reference"]["captures"][0]["requestBodyPath"])
        body = json.loads(path.read_text(encoding="utf-8"))
        body["type"] = "AmortizedCost"
        path.write_text(json.dumps(body), encoding="utf-8")
        with self.assertRaisesRegex(setup.SetupError, "differs from the approved plan"):
            self.app.prepare(self.payload)

    def test_credentials_in_raw_response_are_blocked_without_persistent_setup(self):
        path = Path(self.payload["reference"]["captures"][0]["pages"][0]["path"])
        raw = path.read_text(encoding="utf-8")
        path.write_text('{"Authorization":"synthetic-not-a-credential",' + raw[1:], encoding="utf-8")
        with self.assertRaisesRegex(setup.finops.EvidenceError, "Credential"):
            self.app.prepare(self.payload)
        self.assertEqual(list(self.app.output.iterdir()), [])

    def test_original_example_index_cannot_be_promoted_by_editor(self):
        self.index["isExample"] = True
        self.write_inputs()
        self.payload.update({"referenceMode": "existing", "portalIndexPath": str(self.root / "portal.json")})
        with self.assertRaisesRegex(setup.finops.EvidenceError, "sample"):
            self.app.prepare(self.payload)

    def test_unapproved_paths_unc_streams_and_traversal_are_rejected(self):
        for value in (str(self.root.parent / "outside.json"), r"\\server\share\file.json",
                      r"..\outside.json", str(self.root / "actual.json") + ":stream"):
            with self.subTest(value=value), self.assertRaises(setup.SetupError):
                self.app.evidence_file(value)

    def test_cross_origin_host_and_missing_token_are_rejected(self):
        for headers in ({"Host": "attacker.example.test:8765"},
                        {"Origin": "https://attacker.example.test"},
                        {"X-Setup-Token": ""}, {"Sec-Fetch-Site": "cross-site"}):
            with self.subTest(headers=headers), self.assertRaises(setup.SetupError) as error:
                self.handler(**headers).guard(True)
            self.assertEqual(error.exception.status, 403)

    def test_second_campaign_cannot_start_while_first_is_active(self):
        first, second = self.offline(), self.offline()
        self.start_mocked(first["id"])
        with self.assertRaisesRegex(setup.SetupError, "Another test campaign"):
            self.app.start(second["id"])

    def test_run_cannot_be_invoked_twice(self):
        record = self.offline()
        process, _ = self.start_mocked(record["id"])
        self.write_report(record["id"])
        self.app.finish(record["id"], process)
        with self.assertRaisesRegex(setup.SetupError, "already invoked"):
            self.app.start(record["id"])

    def test_exit_zero_without_report_is_an_explicit_failure(self):
        record = self.offline()
        process, _ = self.start_mocked(record["id"])
        with self.assertLogs(setup.LOGGER, level="ERROR"):
            self.app.finish(record["id"], process)
        result = self.app.status(record["id"])
        self.assertEqual(result["state"], "error")
        self.assertIn("without a completed campaign report", result["error"])

    def test_incomplete_negative_execution_cannot_be_success(self):
        record = self.offline()
        process, _ = self.start_mocked(record["id"])
        self.write_report(record["id"], negative_complete=False)
        with self.assertLogs(setup.LOGGER, level="ERROR"):
            self.app.finish(record["id"], process)
        self.assertEqual(self.app.status(record["id"])["state"], "error")

    def test_nonzero_exit_with_a_passing_report_is_inconsistent(self):
        record = self.offline()
        process, _ = self.start_mocked(record["id"], code=2)
        self.write_report(record["id"])
        with self.assertLogs(setup.LOGGER, level="ERROR"):
            self.app.finish(record["id"], process)
        self.assertEqual(self.app.status(record["id"])["state"], "error")

    def test_process_start_failure_is_persisted_and_does_not_leave_busy_state(self):
        record = self.offline()
        with patch.object(setup.subprocess, "Popen", side_effect=OSError("Synthetic spawn failure")), \
                self.assertLogs(setup.LOGGER, level="ERROR"), self.assertRaises(setup.SetupError):
            self.app.start(record["id"])
        self.assertIsNone(self.app.active_id)
        result = self.app.status(record["id"])
        self.assertEqual(result["state"], "error")
        self.assertIn("Synthetic spawn failure", result["error"])

    def test_artifacts_cannot_escape_the_run_or_download_programs(self):
        record = self.offline()
        (self.app.run_directory(record["id"]) / "program.exe").write_bytes(b"synthetic")
        for path in ("..\\actual.json", "program.exe"):
            with self.subTest(path=path), self.assertRaises(setup.SetupError):
                self.app.artifact(record["id"], path)

    def test_reopened_unfinished_campaign_is_not_reported_as_completed(self):
        record = self.offline()
        self.start_mocked(record["id"])
        reopened = setup.SetupApp(self.root, [self.root])
        status = reopened.status(record["id"])
        self.assertEqual(status["state"], "interrupted")
        self.assertIn("not a completed verification", status["error"])


class PositiveSetupTests(SetupCase):
    phase = "positive"

    def test_editor_generates_valid_portable_config_and_preserves_raw_evidence(self):
        source = Path(self.payload["reference"]["captures"][0]["pages"][0]["path"])
        original = source.read_bytes()
        with patch.object(setup.finops, "AzureClient") as azure:
            record = self.app.prepare(self.payload)
            root = self.app.run_directory(record["id"])
            inputs = setup.portal_validation.load_inputs(root / "portal-validation.json", "evidence", None)
        self.assertEqual(record["state"], "prepared")
        self.assertEqual(inputs["config"]["approvedPlanSha256"], self.plan["sha256"])
        self.assertNotIn("liveApproval", inputs["config"])
        self.assertEqual((root / "portal-page-0-0.json").read_bytes(), original)
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(inputs["portalIndex"]["attestation"]["confirmedAt"], portal_fixture.CLOCK)
        azure.assert_not_called()

    def test_existing_index_is_snapshotted_without_modifying_original(self):
        source = self.root / "portal.json"
        original = source.read_bytes()
        self.payload.update({"referenceMode": "existing", "portalIndexPath": str(source)})
        record = self.app.prepare(self.payload)
        self.assertEqual(record["state"], "prepared")
        self.assertEqual(source.read_bytes(), original)
        index = json.loads(record["previews"]["portal-reference.json"])
        self.assertEqual(index["captures"][0]["pages"][0]["path"], "portal-page-0-0.json")

    def test_display_totals_above_javascript_safe_integer_range_remain_exact_strings(self):
        self.payload["reference"]["displayedTotals"][0]["amount"] = "9007199254740993.01"
        record = self.app.prepare(self.payload)
        index = json.loads(record["previews"]["portal-reference.json"])
        self.assertEqual(index["displayedTotals"][0]["amount"], "9007199254740993.01")

    def test_offline_launch_uses_current_interpreter_argument_array_and_reports_actual_outcome(self):
        record = self.offline()
        process, launch = self.start_mocked(record["id"])
        command = launch.call_args.args[0]
        self.assertEqual(command[0], sys.executable)
        self.assertIn("--offline-only", command)
        self.assertNotIn("--portal-config", command)
        self.assertNotIn("--_worker", command)
        self.assertIs(launch.call_args.kwargs["shell"], False)
        self.write_report(record["id"])
        self.app.finish(record["id"], process)
        result = self.app.status(record["id"])
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["exitCode"], 0)
        self.assertFalse(result["report"]["acceptanceValidated"])
        self.assertIn("PORTAL PARITY NOT VALIDATED", result["verdict"])

    def test_evidence_command_never_enables_live_approval(self):
        record = self.app.prepare(self.payload)
        command = self.app.command(record)
        self.assertIn("--portal-config", command)
        self.assertEqual(command[command.index("--portal-mode") + 1], "evidence")
        self.assertNotIn("--offline-only", command)
        self.assertNotIn("--confirm-live-plan", command)

    def test_failed_runner_report_and_diagnostics_are_retained(self):
        record = self.offline()
        process, _ = self.start_mocked(record["id"], code=1)
        report = self.write_report(record["id"], verdict="FAIL")
        self.app.finish(record["id"], process)
        result = self.app.status(record["id"])
        self.assertEqual(result["state"], "completed")
        self.assertEqual(result["report"], report)
        self.assertEqual(result["exitCode"], 1)

    def test_saved_setup_can_be_reopened_and_config_downloaded(self):
        record = self.app.prepare(self.payload)
        reopened = setup.SetupApp(self.root, [self.root])
        self.assertEqual(reopened.history()[0]["id"], record["id"])
        artifact = reopened.artifact(record["id"], "portal-validation.json")
        self.assertEqual(json.loads(artifact.read_text(encoding="utf-8"))["schemaVersion"], 1)

    def test_same_origin_and_session_token_are_accepted(self):
        self.handler().guard(True)
        self.handler().guard(False)


if __name__ == "__main__":
    unittest.main()
