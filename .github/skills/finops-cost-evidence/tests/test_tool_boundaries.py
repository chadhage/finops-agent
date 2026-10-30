from __future__ import annotations

import base64
import copy
import io
import json
import subprocess
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import Mock, patch

import test_failure_matrix as matrix
import test_finops as fixture
import test_portal_validation as portal_fixture


finops = fixture.finops
portal = portal_fixture.portal_validation


class NegativeTokenBoundaryTests(matrix.CliCase):
    phase = "negative"

    def blocked_token(self, claims):
        payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
        with patch.object(finops, "cli_json", side_effect=[matrix.profile(),
                                                         {"accessToken": "synthetic." + payload + ".signature"}]):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])

    def test_null_token_audience_is_an_explicit_failure(self):
        claims = {"oid": fixture.INVOKER, "tid": fixture.TENANT, "exp": int(finops.time.time()) + 3600, "aud": None}
        self.blocked_token(claims)

    def test_numeric_token_audience_is_an_explicit_failure(self):
        claims = {"oid": fixture.INVOKER, "tid": fixture.TENANT, "exp": int(finops.time.time()) + 3600, "aud": 7}
        self.blocked_token(claims)

    def test_missing_token_identity_is_not_inferred_from_email(self):
        self.blocked_token({"tid": fixture.TENANT, "aud": finops.ARM,
                            "exp": int(finops.time.time()) + 3600, "upn": "owner@example.test"})

    def test_non_numeric_token_expiry_is_blocked(self):
        self.blocked_token({"oid": fixture.INVOKER, "tid": fixture.TENANT, "aud": finops.ARM, "exp": "later"})

    def test_array_jwt_claims_are_blocked(self):
        self.blocked_token([])

    def test_expired_cli_command_does_not_fall_back_to_another_account(self):
        with patch.object(finops.shutil, "which", return_value="synthetic-az"), \
                patch.object(finops.subprocess, "run", side_effect=subprocess.TimeoutExpired("synthetic-az", 90)) as run:
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])
        self.assertEqual(run.call_count, 1)

    def test_cli_malformed_json_is_explicit(self):
        with patch.object(finops.shutil, "which", return_value="synthetic-az"), \
                patch.object(finops.subprocess, "run", return_value=Mock(returncode=0, stdout="{broken")):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])


class NegativeScopeShapeTests(matrix.CliCase):
    phase = "negative"


CATALOG_SHAPES = [
    ("null_resources", ("resources",), None),
    ("object_resources", ("resources",), {}),
    ("null_subscriptions", ("subscriptions",), None),
    ("invalid_subscription_entry", ("subscriptions",), [None]),
    ("invalid_resource_entry", ("resources",), [None]),
    ("resource_group_is_null", ("resourceGroups",), None),
    ("location_is_null", ("locations",), [None]),
    ("owner_user_is_null", ("users",), [None]),
    ("owner_bindings_is_null", ("ownerBindings",), None),
    ("resource_tag_value_is_not_a_string", ("resources",), [
        {"id": fixture.RESOURCE, "location": "eastus", "tags": {"Application": True}}]),
]


def catalog_shape_case(path, value):
    def test(self):
        scenario, catalog = fixture.scenario(), fixture.catalog()
        matrix.change(catalog, path, value)
        if path[0] == "locations":
            scenario["selection"] = {"regions": ["East US"]}
        elif path[0] in ("users", "ownerBindings"):
            scenario["selection"] = {"owners": {"kind": "rbac", "users": [fixture.OWNER]}}
        elif path[0] == "resourceGroups":
            scenario["selection"] = {"resourceGroupNames": ["app"]}
        self.assert_blocked("resolve", {"scenario": scenario, "catalog": catalog})
    return test


for case_name, case_path, case_value in CATALOG_SHAPES:
    setattr(NegativeScopeShapeTests, "test_" + case_name, catalog_shape_case(case_path, case_value))


class NegativeContinuationTests(unittest.TestCase):
    phase = "negative"

    def test_fragment_cannot_be_a_cost_continuation(self):
        initial = fixture.plan_for()["requests"][0]["url"]
        with self.assertRaises(finops.EvidenceError):
            finops.validate_next_url(initial + "#fragment", initial)

    def test_continuation_with_empty_api_version_is_invalid(self):
        initial = fixture.plan_for()["requests"][0]["url"]
        with self.assertRaises(finops.EvidenceError):
            finops.validate_next_url(initial.replace(finops.API_VERSION, ""), initial)

    def test_repeated_continuation_token_parameters_are_invalid(self):
        initial = fixture.plan_for()["requests"][0]["url"]
        with self.assertRaises(finops.EvidenceError):
            finops.validate_next_url(initial + "&$skiptoken=a&$skiptoken=b", initial)

    def test_userinfo_host_cannot_receive_an_invoker_token(self):
        initial = fixture.plan_for()["requests"][0]["url"]
        with self.assertRaises(finops.EvidenceError):
            finops.validate_next_url(initial.replace("management.azure.com", "user@management.azure.com"), initial)

    def test_resource_graph_cannot_use_unapproved_query_text(self):
        client = object.__new__(finops.AzureClient)
        client.subscriptions = [fixture.SUB]
        with self.assertRaisesRegex(finops.EvidenceError, "Non-allowlisted inventory"):
            client.request("POST", finops.ARM + "/providers/Microsoft.ResourceGraph/resources",
                           fixture.SUB, {"subscriptions": [fixture.SUB], "query": "Resources | take 1"})

    def test_resource_graph_cannot_expand_subscription_body(self):
        client = object.__new__(finops.AzureClient)
        client.subscriptions = [fixture.SUB]
        with self.assertRaisesRegex(finops.EvidenceError, "Non-allowlisted inventory"):
            client.request("POST", finops.ARM + "/providers/Microsoft.ResourceGraph/resources",
                           fixture.SUB, {"subscriptions": [fixture.SUB, fixture.OTHER_SUB],
                                         "query": finops.RESOURCE_QUERY})

    def test_cost_execution_loop_stops_without_partial_bundle(self):
        plan = fixture.plan_for()
        request = plan["requests"][0]
        client = Mock(tenant=fixture.TENANT, principal=fixture.INVOKER, subscriptions=[fixture.SUB])
        client.request.return_value = fixture.page(request["url"],
            fixture.raw_response("detail", fixture.records(), request["url"]))
        with self.assertRaisesRegex(finops.EvidenceError, "Repeated continuation"):
            finops.execute_plan(plan, client)
        self.assertEqual(client.request.call_count, 1)

    def test_wrong_client_tenant_never_starts_query(self):
        client = Mock(tenant=fixture.OWNER, principal=fixture.INVOKER, subscriptions=[fixture.SUB])
        with self.assertRaisesRegex(finops.EvidenceError, "identity/scope"):
            finops.execute_plan(fixture.plan_for(), client)
        client.request.assert_not_called()


class NegativeLedgerShapeTests(matrix.CliCase):
    phase = "negative"

    def test_string_usage_date_cannot_impersonate_numeric_column(self):
        capture = fixture.bundle_for(entries=[
            ["0.008", "USD", fixture.RESOURCE.lower(), "eastus", "20260901"]])
        self.assert_blocked("report", {"actual": capture})

    def test_null_capture_entry_is_blocked(self):
        capture = fixture.bundle_for()
        capture["captures"][0] = None
        self.assert_blocked("report", {"actual": fixture.reseal(capture)})

    def test_null_response_schema_entry_is_blocked(self):
        raw = json.loads(fixture.raw_response("detail", fixture.records()))
        raw["properties"]["columns"][0] = None
        capture = fixture.replace_raw(fixture.bundle_for(), 0, json.dumps(raw))
        self.assert_blocked("report", {"actual": capture})

    def test_null_plan_root_is_explicitly_blocked(self):
        capture = fixture.bundle_for()
        capture["plan"] = None
        self.assert_blocked("report", {"actual": fixture.reseal(capture)})

    def test_capture_without_source_cannot_claim_provenance(self):
        capture = fixture.bundle_for()
        del capture["source"]
        self.assert_blocked("report", {"actual": fixture.reseal(capture)})

    def test_scope_validation_flag_without_provenance_cannot_validate_report(self):
        plan = fixture.plan_for()
        manifest = plan["manifest"]
        manifest["scopeReference"] = {"status": "exact-match"}
        manifest = fixture.reseal(manifest)
        with self.assertRaises(finops.EvidenceError):
            finops.make_plan(manifest)
        plan = fixture.reseal({**plan, "manifest": manifest})
        actual, reference = fixture.bundle_for(plan), fixture.bundle_for(plan)
        self.assert_blocked("report", {"actual": actual, "reference": reference})

    def test_money_float_cannot_be_imported_from_formatter(self):
        capture = fixture.bundle_for()
        raw = fixture.raw_response("detail", fixture.records()).replace("0.004", '"0.004"')
        self.assert_blocked("report", {"actual": fixture.replace_raw(capture, 0, raw)})

    def test_invalid_unicode_source_is_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / "bad.json", root / "no-output.md"
            source.write_bytes(b"\xff\xfe\x00\xff")
            with patch("sys.stderr", new_callable=io.StringIO) as errors:
                status = finops.main(["report", "--actual", str(source), "--out", str(output)])
            self.assertEqual(status, 2)
            self.assertIn("FinOps blocked:", errors.getvalue())
            self.assertFalse(output.exists())


class NegativePortalToolTests(portal_fixture.PortalCase):
    phase = "negative"

    def test_credentials_in_raw_actual_response_are_never_persisted(self):
        first = self.actual["captures"][0]["pages"][0]
        first["raw"] = '{"Authorization":"SYNTHETIC-NOT-A-CREDENTIAL",' + first["raw"][1:]
        first["sha256"] = finops.raw_digest(first["raw"])
        self.actual = fixture.reseal(self.actual)
        report = self.check()
        self.assertEqual(report["status"], "BLOCKED")
        for path in (self.root / "result").glob("*"):
            self.assertNotIn("SYNTHETIC-NOT-A-CREDENTIAL", path.read_text(encoding="utf-8"))

    def test_raw_portal_error_body_cannot_be_accepted(self):
        path = self.root / self.index["captures"][0]["pages"][0]["path"]
        path.write_text('{"error":{"code":"Forbidden"}}', encoding="utf-8")
        self.assert_blocked("Invalid Cost Management response")

    def test_boolean_portal_attestation_is_not_assumed_from_one(self):
        self.index["attestation"]["exportedFromAzurePortal"] = 1
        self.assert_blocked("attest Portal origin")

    def test_missing_required_control_is_not_a_match(self):
        self.index["captures"].pop()
        self.assert_blocked("missing or unexpected")

    def test_evidence_mode_does_not_need_or_honor_live_consent(self):
        self.config["liveApproval"] = {"confirmed": True, "principalId": fixture.OWNER}
        with patch.object(finops, "AzureClient") as azure:
            report = self.check()
        self.assertFalse(report["liveQueryExecuted"])
        azure.assert_not_called()

    def test_null_actual_plan_is_explicitly_reported_not_left_running(self):
        self.actual["plan"] = None
        self.actual = fixture.reseal(self.actual)
        report = self.check()
        self.assertEqual(report["status"], "BLOCKED")

    def test_future_live_consent_is_blocked_before_authentication(self):
        self.config["liveApproval"]["confirmedAt"] = "2026-10-30T00:05:00Z"
        self.assert_blocked("not yet valid", "live", self.plan["sha256"])

    def test_actual_scope_mismatch_cannot_validate_against_portal(self):
        scenario = fixture.scenario()
        scenario["costBasis"] = "AmortizedCost"
        manifest = finops.resolve_scope(scenario, fixture.catalog())
        self.actual = fixture.bundle_for(finops.make_plan(manifest))
        self.actual["source"] = "invoker-azure-cli-arm"
        self.actual["capturedAt"] = portal_fixture.CLOCK
        for capture in self.actual["captures"]:
            capture["pages"][0]["retrievedAt"] = portal_fixture.CLOCK
        self.actual = fixture.reseal(self.actual)
        self.assert_blocked("Reference plan differs")


class PositiveCommandTests(unittest.TestCase):
    phase = "positive"

    def test_every_helper_subcommand_has_parseable_help_without_azure(self):
        commands = ("identity", "inventory", "resolve", "plan", "query", "import-reference", "reconcile", "report")
        for command in commands:
            with self.subTest(command=command), patch("sys.stdout", new_callable=io.StringIO) as output, \
                    self.assertRaises(SystemExit) as result:
                finops.main([command, "--help"])
            self.assertEqual(result.exception.code, 0)
            self.assertIn("--out", output.getvalue())

    def test_cli_identity_returns_bound_metadata_without_token(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "identity.json"
            with patch.object(finops, "cli_json", side_effect=[matrix.profile(), {"accessToken": matrix.token()}]):
                status = finops.main(["identity", "--tenant", fixture.TENANT,
                                     "--subscription", fixture.SUB, "--out", str(output)])
            result = finops.read_json(output)
            self.assertEqual(status, 0)
            self.assertEqual(result["principalId"], fixture.INVOKER)
            self.assertNotIn("accessToken", result)

    def test_successful_query_command_calls_only_the_generated_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = fixture.plan_for()
            finops.write_json(root / "plan.json", plan)
            with patch.object(finops, "AzureClient") as client, \
                    patch.object(finops, "execute_plan", return_value=fixture.bundle_for(plan)) as execute:
                status = finops.main(["query", "--plan", str(root / "plan.json"), "--out", str(root / "actual.json")])
            self.assertEqual(status, 0)
            execute.assert_called_once_with(plan, client.return_value)
            client.assert_called_once_with(fixture.TENANT, fixture.INVOKER, [fixture.SUB])

    def test_bom_json_and_whitespace_keep_numeric_precision(self):
        result = finops.parse_json('\ufeff  {"cost":1.2345678901234567890123456789} ')
        self.assertEqual(str(result["cost"]), "1.2345678901234567890123456789")

    def test_valid_json_no_data_is_not_a_zero_cost_row(self):
        result = finops.validate_bundle(fixture.bundle_for(entries=[]))
        self.assertEqual(result["totals"], {})
        self.assertEqual(len(result["emptyRequests"]), 2)
