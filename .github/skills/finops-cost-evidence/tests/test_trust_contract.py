from __future__ import annotations

import copy
import inspect
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_failure_matrix as matrix
import test_finops as fixture
import test_portal_validation as portal_fixture
import test_runner_edges as runner_fixture
import test_tool_boundaries as boundary
import test_verification_setup as setup_fixture


finops = fixture.finops
portal = portal_fixture.portal_validation


class NegativeArtifactSchemaTests(matrix.CliCase):
    phase = "negative"

    def test_numeric_date_guard_detects_a_removed_type_check(self):
        original = finops.require

        def mutant(condition, message):
            if message != "Usage date must be an exact JSON integer.":
                original(condition, message)

        result = unittest.TestResult()
        with patch.object(finops, "require", side_effect=mutant):
            boundary.NegativeLedgerShapeTests(
                "test_string_usage_date_cannot_impersonate_numeric_column").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])

    def test_resource_comparison_guard_detects_a_removed_set_check(self):
        original = finops.require

        def mutant(condition, message):
            if message != "Resource reference mismatch: exact resource sets differ.":
                original(condition, message)

        result = unittest.TestResult()
        with patch.object(finops, "require", side_effect=mutant):
            fixture.ScopeTests("test_exact_resource_reference_required_for_scope_validation").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])

    def test_audience_guard_detects_a_removed_identity_check(self):
        original = finops.require

        def mutant(condition, message):
            if message != "Unexpected ARM token audience.":
                original(condition, message)

        result = unittest.TestResult()
        with patch.object(finops, "require", side_effect=mutant):
            boundary.NegativeTokenBoundaryTests("test_null_token_audience_is_an_explicit_failure").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])

    def test_object_shape_guard_detects_a_removed_validation_check(self):
        result = unittest.TestResult()
        with patch.object(finops, "object_fields", side_effect=lambda value, required, label: value):
            boundary.NegativeLedgerShapeTests("test_null_plan_root_is_explicitly_blocked").run(result)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.failures, [])

    def test_portal_mode_guard_detects_a_removed_mode_check(self):
        runner = runner_fixture.run_tests
        source = inspect.getsource(runner.run_portal_stage)
        mutant = source.replace('result["status"] != expected or ', "", 1)
        self.assertNotEqual(mutant, source)
        namespace = dict(vars(runner))
        exec(compile(mutant, runner.__file__, "exec"), namespace)
        result = unittest.TestResult()
        with patch.object(runner, "run_portal_stage", namespace["run_portal_stage"]):
            runner_fixture.NegativePortalStageTests("test_live_mode_cannot_accept_captured_only_pass").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])


def missing_manifest_field(field):
    def test(self):
        manifest = fixture.plan_for()["manifest"]
        del manifest[field]
        self.assert_blocked("plan", {"manifest": fixture.reseal(manifest)})
    return test


for field in ("schemaVersion", "scenario", "scenarioSha256", "tenantId", "principalId", "period",
              "costBasis", "approvedSubscriptionIds", "subscriptionIds", "excludedSubscriptionIds",
              "resourceIds", "scopeMode", "scopeReference", "inventoryAsOf", "catalogSha256", "ownerEvidence"):
    setattr(NegativeArtifactSchemaTests, "test_missing_manifest_" + field, missing_manifest_field(field))


def capture_shape_case(path, value):
    def test(self):
        capture = fixture.bundle_for()
        matrix.change(capture, path, value)
        self.assert_blocked("report", {"actual": fixture.reseal(capture)})
    return test


for name, path, value in (
    ("source_null", ("source",), None),
    ("source_empty", ("source",), ""),
    ("source_object", ("source",), {}),
    ("captures_object", ("captures",), {}),
    ("capture_id_null", ("captureId",), None),
    ("plan_array", ("plan",), []),
    ("plan_requests_object", ("plan", "requests"), {}),
):
    setattr(NegativeArtifactSchemaTests, "test_" + name, capture_shape_case(path, value))


class NegativeProvenanceTests(matrix.CliCase):
    phase = "negative"

    def test_resealed_reference_with_different_membership_is_recompared(self):
        scenario = fixture.scenario()
        reference = {"scenarioSha256": finops.digest(scenario), "source": "synthetic independent set",
                     "capturedAt": fixture.AS_OF, "resourceIds": [fixture.RESOURCE, fixture.SECOND]}
        manifest = finops.resolve_scope(scenario, fixture.catalog(), reference)
        metadata = manifest["scopeReference"]
        metadata["reference"]["resourceIds"].pop()
        metadata["sha256"] = finops.digest(metadata["reference"])
        self.assert_blocked("plan", {"manifest": fixture.reseal(manifest)})

    def test_resealed_reference_metadata_cannot_contradict_embedded_evidence(self):
        scenario = fixture.scenario()
        reference = {"scenarioSha256": finops.digest(scenario), "source": "synthetic independent set",
                     "capturedAt": fixture.AS_OF, "resourceIds": [fixture.RESOURCE, fixture.SECOND]}
        manifest = finops.resolve_scope(scenario, fixture.catalog(), reference)
        manifest["scopeReference"]["source"] = "different source"
        self.assert_blocked("plan", {"manifest": fixture.reseal(manifest)})


class NegativeCredentialTests(portal_fixture.PortalCase):
    phase = "negative"

    def test_shared_writer_rejects_embedded_credentials_before_creating_output(self):
        value = {"url": "https://management.azure.com/", "status": 200,
                 "raw": '{"nested":[{"client_secret":"SYNTHETIC-PRIVATE-MARKER"}]}'}
        target = self.root / "must-not-exist.json"
        with self.assertRaises(finops.EvidenceError) as error:
            finops.write_json(target, value)
        self.assertFalse(target.exists())
        self.assertNotIn("SYNTHETIC-PRIVATE-MARKER", str(error.exception))

    def test_import_never_persists_credential_bearing_raw_response(self):
        capture = self.index["captures"][0]
        raw_path = self.root / capture["pages"][0]["path"]
        raw_path.write_text('{"Authorization":"SYNTHETIC-PRIVATE-MARKER"}', encoding="utf-8")
        self.write_inputs()
        output = self.root / "imported.json"
        with patch("sys.stderr", new_callable=io.StringIO) as errors:
            code = finops.main(["import-reference", "--plan", str(self.root / "plan.json"),
                               "--index", str(self.root / "portal.json"), "--out", str(output)])
        self.assertEqual(code, 2)
        self.assertFalse(output.exists())
        self.assertNotIn("SYNTHETIC-PRIVATE-MARKER", errors.getvalue())

    def test_credential_guard_removal_is_detected_by_original_regression(self):
        result = unittest.TestResult()
        with patch.object(finops, "no_secrets"):
            boundary.NegativePortalToolTests(
                "test_credentials_in_raw_actual_response_are_never_persisted").run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.errors, [])

    def test_interruption_persists_terminal_non_acceptance(self):
        self.write_inputs()
        with patch.object(portal, "load_inputs", side_effect=KeyboardInterrupt), \
                self.assertRaises(KeyboardInterrupt):
            portal.run_validation(self.root / "config.json", "evidence", self.root / "interrupted")
        report = finops.read_json(self.root / "interrupted" / "report.json")
        self.assertEqual(report["status"], "INTERRUPTED")
        self.assertIn("completedAt", report)
        self.assertFalse(report["liveQueryExecuted"])

    def test_unexpected_error_is_reraised_but_not_left_running(self):
        self.write_inputs()
        with patch.object(portal, "load_inputs", side_effect=RuntimeError("synthetic bug")), \
                self.assertRaises(RuntimeError):
            portal.run_validation(self.root / "config.json", "evidence", self.root / "unexpected")
        report = finops.read_json(self.root / "unexpected" / "report.json")
        self.assertEqual(report["status"], "ERROR")
        self.assertIn("completedAt", report)

    def test_error_after_comparison_cannot_leave_a_passing_report(self):
        self.write_inputs()
        source = finops.source_fingerprint()
        with patch.object(finops, "source_fingerprint", side_effect=[source, RuntimeError("synthetic bug")]), \
                self.assertRaises(RuntimeError):
            portal.run_validation(self.root / "config.json", "evidence", self.root / "late-error")
        report = finops.read_json(self.root / "late-error" / "report.json")
        self.assertEqual(report["status"], "ERROR")


class NegativeSnapshotTests(setup_fixture.SetupCase):
    phase = "negative"

    def test_snapshot_rejects_raw_credentials_before_copying_bytes(self):
        source = self.root / "private-input.json"
        source.write_text(json.dumps({"url": "https://management.azure.com/", "status": 200,
                                      "raw": '{"Cookie":"SYNTHETIC-PRIVATE-MARKER"}'}), encoding="utf-8")
        destination = self.root / "snapshot.json"
        with self.assertRaises(finops.EvidenceError):
            self.app.copy_input(str(source), destination)
        self.assertFalse(destination.exists())

    def test_server_restart_persists_interruption(self):
        record = self.offline()
        directory = self.app.run_directory(record["id"])
        record["state"] = "running"
        setup_fixture.setup.write_record(directory, record)
        self.assertEqual(self.app.status(record["id"])["state"], "interrupted")
        self.assertEqual(self.app.read_record(record["id"])["state"], "interrupted")

    def test_source_change_after_review_blocks_execution(self):
        record = self.offline()
        with patch.object(finops, "source_fingerprint", return_value={"sha256": "0" * 64}), \
                patch.object(setup_fixture.setup.subprocess, "Popen") as launch:
            with self.assertRaisesRegex(setup_fixture.setup.SetupError, "Source changed"):
                self.app.start(record["id"])
        launch.assert_not_called()

    def test_source_mismatch_at_completion_is_a_terminal_error(self):
        record = self.offline()
        process, _ = self.start_mocked(record["id"])
        report = self.write_report(record["id"])
        report["source"] = {"sha256": "0" * 64}
        target = self.app.run_directory(record["id"]) / "reports" / "synthetic-campaign" / "report.json"
        target.write_text(json.dumps(report), encoding="utf-8")
        self.app.finish(record["id"], process)
        self.assertEqual(self.app.read_record(record["id"])["state"], "error")
        self.assertIsNone(self.app.active_id)


class PositiveSetupSerializationTests(setup_fixture.SetupCase):
    phase = "positive"

    def test_fractional_runner_timings_are_serializable_without_changing_cost_evidence(self):
        record = self.offline()
        report = self.write_report(record["id"])
        report["results"] = [{"seconds": 0.125, "id": "synthetic-case", "status": "pass"}]
        target = self.app.run_directory(record["id"]) / "reports" / "synthetic-campaign" / "report.json"
        target.write_text(json.dumps(report), encoding="utf-8")
        status = self.app.status(record["id"])
        self.assertEqual(json.loads(json.dumps(status, allow_nan=False))["report"]["results"][0]["seconds"], 0.125)


class NegativePortalResultTests(runner_fixture.PortalStageCase):
    phase = "negative"

    def test_missing_source_fingerprint_cannot_pass(self):
        self.assertEqual(self.stage("CAPTURED_PORTAL_PARITY_PASS", source=None)["status"], "BLOCKED")

    def test_different_source_fingerprint_cannot_pass(self):
        self.assertEqual(self.stage("CAPTURED_PORTAL_PARITY_PASS",
                                    source={"sha256": "0" * 64})["status"], "BLOCKED")


class PositiveTrustContractTests(unittest.TestCase):
    phase = "positive"

    def test_credential_inspection_does_not_reserialize_raw_money(self):
        raw = '{"properties":{"rows":[[0.000000000000000000004]],"nextLink":null}}'
        value = {"url": "https://management.azure.com/", "status": 200, "raw": raw}
        original = copy.deepcopy(value)
        finops.no_secrets(value)
        self.assertEqual(value, original)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "safe.json"
            finops.write_json(target, value)
            self.assertEqual(json.loads(target.read_text(encoding="utf-8"))["raw"], raw)

    def test_benign_raw_tag_is_not_treated_as_an_encoded_response(self):
        scenario, catalog = fixture.scenario(), fixture.catalog()
        catalog["resources"][0]["tags"]["raw"] = "{not JSON: ordinary tag text}"
        finops.resolve_scope(scenario, catalog)


class NegativePublicationTests(unittest.TestCase):
    phase = "negative"

    def test_failed_publication_leaves_no_partial_file_or_temporary_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.md"
            with patch.object(Path, "hardlink_to", side_effect=OSError("synthetic filesystem failure")), \
                    self.assertRaises(OSError):
                finops.write_text(output, "complete report")
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_publication_never_replaces_existing_user_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "existing.md"
            output.write_text("original", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                finops.write_text(output, "replacement")
            self.assertEqual(output.read_text(encoding="utf-8"), "original")
