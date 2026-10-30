from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_finops as fixture

sys.path.insert(0, str(fixture.SCRIPTS))
import portal_validation


finops = fixture.finops
CLOCK = "2026-10-30T00:00:00Z"


class PortalCase(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="finops-portal-test-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.clock = patch.object(finops, "utc_now", return_value=CLOCK)
        self.clock.start()
        self.addCleanup(self.clock.stop)
        scenario = fixture.scenario()
        resource_reference = {"scenarioSha256": finops.digest(scenario), "source": "Synthetic independent inventory",
                              "capturedAt": CLOCK, "resourceIds": [fixture.RESOURCE, fixture.SECOND]}
        self.plan = finops.make_plan(finops.resolve_scope(scenario, fixture.catalog(), resource_reference))
        self.config = {
            "schemaVersion": 1, "isExample": False, "planPath": "plan.json", "portalIndexPath": "portal.json",
            "actualPath": "actual.json", "approvedPlanSha256": self.plan["sha256"],
            "maxEvidenceAgeSeconds": 600,
            "liveApproval": {"confirmed": True, "tenantId": fixture.TENANT, "principalId": fixture.INVOKER,
                             "subscriptionIds": [fixture.SUB], "planSha256": self.plan["sha256"],
                             "confirmedAt": CLOCK, "expiresAt": "2026-10-30T00:10:00Z"},
        }
        self.index = {
            "schemaVersion": 1, "isExample": False, "source": "portal-query-export",
            "tenantId": fixture.TENANT, "principalId": fixture.INVOKER, "capturedAt": CLOCK,
            "portalViewUrl": "https://portal.azure.com/#synthetic-cost-analysis-view",
            "attestation": {"exportedFromAzurePortal": True, "sameViewScopeAndFilters": True,
                            "noSecretsIncluded": True, "confirmedByPrincipalId": fixture.INVOKER,
                            "confirmedAt": CLOCK},
            "displayedTotals": [{"currency": "USD", "amount": "0.01", "decimalPlaces": 2}],
            "captures": [],
        }
        self.replace_records(fixture.records())

    def capture(self, entries: list[list]) -> dict:
        result = fixture.bundle_for(self.plan, entries)
        result["source"], result["capturedAt"] = "invoker-azure-cli-arm", CLOCK
        for capture in result["captures"]:
            for page in capture["pages"]:
                page["retrievedAt"] = CLOCK
        return fixture.reseal(result)

    def replace_records(self, entries: list[list]) -> None:
        self.actual = self.capture(entries)
        self.index["captures"] = []
        requests = {r["id"]: r for r in self.plan["requests"]}
        for number, capture in enumerate(self.actual["captures"]):
            page = capture["pages"][0]
            name = f"portal-page-{number}.json"
            (self.root / name).write_text(page["raw"], encoding="utf-8")
            self.index["captures"].append({
                "requestId": capture["requestId"], "requestBody": requests[capture["requestId"]]["body"],
                "pages": [{"path": name, "url": page["url"], "status": 200}],
            })

    def write_inputs(self) -> None:
        for name, value in (("config.json", self.config), ("plan.json", self.plan),
                            ("portal.json", self.index), ("actual.json", self.actual)):
            (self.root / name).write_text(json.dumps(value), encoding="utf-8")

    def check(self, mode: str = "evidence", confirmation: str | None = None) -> dict:
        self.write_inputs()
        report = portal_validation.run_validation(self.root / "config.json", mode, self.root / "result", confirmation)
        self.assertTrue((self.root / "result" / "report.md").is_file())
        self.assertEqual(finops.read_json(self.root / "result" / "report.json")["status"], report["status"])
        return report

    def assert_blocked(self, text: str = "", mode: str = "evidence", confirmation: str | None = None):
        with patch.object(finops, "AzureClient") as azure:
            report = self.check(mode, confirmation)
        self.assertEqual(report["status"], "BLOCKED")
        self.assertFalse(report["liveQueryExecuted"])
        self.assertIn(text, report["error"])
        azure.assert_not_called()


class NegativePortalTests(PortalCase):
    phase = "negative"

    def test_example_config_cannot_be_authoritative(self):
        self.config["isExample"] = True
        self.assert_blocked("sample")

    def test_example_portal_index_is_rejected(self):
        self.index["isExample"] = True
        self.assert_blocked("sample")

    def test_sample_response_cannot_be_used_as_real_data(self):
        path = self.root / self.index["captures"][0]["pages"][0]["path"]
        response = finops.read_json(path)
        response["isExample"] = True
        path.write_text(json.dumps(response, default=str), encoding="utf-8")
        self.assert_blocked("sample response")

    def test_cli_reference_is_not_a_proxy_for_portal(self):
        self.index["source"] = "manual-azure-cli"
        self.assert_blocked("not Azure Portal evidence")

    def test_missing_portal_attestation_is_blocked(self):
        self.index["attestation"]["exportedFromAzurePortal"] = False
        self.assert_blocked("attest Portal origin")

    def test_different_portal_identity_is_blocked(self):
        self.index["principalId"] = fixture.OWNER
        self.assert_blocked("tenant/invoker")

    def test_different_approved_plan_hash_is_blocked(self):
        self.config["approvedPlanSha256"] = "0" * 64
        self.assert_blocked("plan hash")

    def test_boolean_plan_schema_is_blocked(self):
        self.plan["schemaVersion"] = True
        self.plan = fixture.reseal(self.plan)
        self.config["approvedPlanSha256"] = self.plan["sha256"]
        self.assert_blocked("plan schema")

    def test_null_plan_manifest_is_reported_as_blocked_not_an_uncaught_crash(self):
        self.plan["manifest"] = None
        self.plan = fixture.reseal(self.plan)
        self.config["approvedPlanSha256"] = self.plan["sha256"]
        self.assert_blocked("manifest must be an object")

    def test_non_string_portal_url_is_blocked(self):
        self.index["portalViewUrl"] = {}
        self.assert_blocked("URL must be a string")

    def test_different_portal_request_basis_is_blocked(self):
        self.index["captures"][0]["requestBody"] = copy.deepcopy(self.index["captures"][0]["requestBody"])
        self.index["captures"][0]["requestBody"]["type"] = "AmortizedCost"
        self.assert_blocked("Portal request differs")

    def test_different_portal_filter_is_blocked(self):
        self.index["captures"][0]["requestBody"] = copy.deepcopy(self.index["captures"][0]["requestBody"])
        self.index["captures"][0]["requestBody"]["dataset"]["filter"] = {
            "dimensions": {"name": "ResourceId", "operator": "In", "values": [fixture.RESOURCE.lower()]}}
        self.assert_blocked("Portal request differs")

    def test_missing_page_file_is_blocked(self):
        self.index["captures"][0]["pages"][0]["path"] = "absent.json"
        self.assert_blocked("file missing")

    def test_missing_captured_pages_are_blocked(self):
        self.index["captures"][0]["pages"] = []
        self.assert_blocked("pages are missing")

    def test_credentials_in_portal_evidence_are_rejected(self):
        self.index["Authorization"] = "synthetic-token-do-not-persist"
        self.assert_blocked("Credential/header")

    def test_stale_portal_capture_is_blocked(self):
        self.index["capturedAt"] = fixture.AS_OF
        self.assert_blocked("age limit")

    def test_future_portal_capture_is_blocked(self):
        self.index["capturedAt"] = "2026-10-30T01:00:00Z"
        self.assert_blocked("future-dated")

    def test_boolean_evidence_age_is_not_an_integer(self):
        self.config["maxEvidenceAgeSeconds"] = True
        self.assert_blocked("positive approved evidence age")

    def test_missing_displayed_portal_total_is_blocked(self):
        self.index["displayedTotals"] = []
        self.assert_blocked("displayed totals")

    def test_unknown_display_currency_is_not_mixed_with_usd(self):
        self.index["displayedTotals"][0]["currency"] = "EUR"
        self.assert_blocked("currency sets")

    def test_duplicate_display_currency_is_blocked(self):
        self.index["displayedTotals"] *= 2
        self.assert_blocked("Duplicate")

    def test_float_display_amount_is_rejected(self):
        self.index["displayedTotals"][0]["amount"] = 0.01
        self.assert_blocked("decimal string")

    def test_default_currency_precision_is_not_assumed(self):
        del self.index["displayedTotals"][0]["decimalPlaces"]
        self.assert_blocked("decimalPlaces")

    def test_same_grand_total_but_different_resource_allocation_fails(self):
        changed = fixture.records()
        changed[0][0], changed[1][0] = "0.003", "0.005"
        self.actual = self.capture(changed)
        report = self.check()
        self.assertEqual(report["status"], "MISMATCH")
        self.assertEqual(len(report["comparison"]["rawRowComparison"]["differences"]), 2)

    def test_subcent_difference_cannot_hide_behind_same_portal_display(self):
        changed = fixture.records()
        changed[0][0] = "0.00400000000001"
        self.actual = self.capture(changed)
        report = self.check()
        self.assertEqual(report["status"], "MISMATCH")
        self.assertTrue(report["comparison"]["displayComparisons"][0]["match"])

    def test_rounding_each_row_cannot_manufacture_display_parity(self):
        self.index["displayedTotals"][0]["amount"] = "0.00"
        report = self.check()
        self.assertEqual(report["status"], "MISMATCH")
        self.assertEqual(report["comparison"]["displayComparisons"][0]["queryDisplay"], "0.01")

    def test_stale_saved_query_is_blocked(self):
        self.actual["capturedAt"] = fixture.AS_OF
        for capture in self.actual["captures"]:
            capture["pages"][0]["retrievedAt"] = fixture.AS_OF
        self.actual = fixture.reseal(self.actual)
        self.assert_blocked("Actual query")

    def test_synthetic_actual_capture_is_not_query_proof(self):
        self.actual["source"] = "synthetic-unit-test"
        self.actual = fixture.reseal(self.actual)
        self.assert_blocked("invoker-bound Azure query")

    def test_unverified_resource_set_blocks_portal_acceptance(self):
        manifest = self.plan["manifest"]
        manifest["scopeReference"] = {"status": "not-verified"}
        self.plan = finops.make_plan(fixture.reseal(manifest))
        self.config["approvedPlanSha256"] = self.plan["sha256"]
        self.assert_blocked("resource-set verification")

    def test_live_requires_explicit_approval(self):
        self.config["liveApproval"]["confirmed"] = False
        self.assert_blocked("explicit invoker approval", "live", self.plan["sha256"])

    def test_live_requires_runtime_plan_confirmation(self):
        self.assert_blocked("confirm-live-plan", "live")

    def test_live_rejects_another_plan_confirmation(self):
        self.assert_blocked("confirm-live-plan", "live", "0" * 64)

    def test_live_rejects_another_invoker(self):
        self.config["liveApproval"]["principalId"] = fixture.OWNER
        self.assert_blocked("identity/scope approval", "live", self.plan["sha256"])

    def test_live_cannot_expand_approved_subscriptions(self):
        self.config["liveApproval"]["subscriptionIds"].append(fixture.OTHER_SUB)
        self.assert_blocked("identity/scope approval", "live", self.plan["sha256"])

    def test_live_rejects_expired_approval(self):
        self.config["liveApproval"]["expiresAt"] = fixture.AS_OF
        self.assert_blocked("expired", "live", self.plan["sha256"])

    def test_live_identity_denial_has_no_fallback(self):
        with patch.object(finops, "AzureClient", side_effect=finops.EvidenceError("synthetic identity mismatch")) as azure:
            report = self.check("live", self.plan["sha256"])
        self.assertEqual(report["status"], "BLOCKED")
        self.assertFalse(report["identityVerifiedThisRun"])
        self.assertFalse(report["liveQueryExecuted"])
        azure.assert_called_once()

    def test_live_query_failure_is_not_a_successful_validation(self):
        with patch.object(finops, "AzureClient"), \
                patch.object(finops, "execute_plan", side_effect=finops.EvidenceError("synthetic HTTP 403")):
            report = self.check("live", self.plan["sha256"])
        self.assertEqual(report["status"], "BLOCKED")
        self.assertTrue(report["liveQueryAttempted"])
        self.assertFalse(report["liveQueryExecuted"])
        self.assertIn("403", report["error"])

    def test_shipped_stub_blocks_before_any_azure_access(self):
        config = fixture.SCRIPTS.parent / "assets" / "portal-validation.example.json"
        with patch.object(finops, "AzureClient") as azure:
            report = portal_validation.run_validation(config, "live", self.root / "sample-result", "not-a-plan")
        self.assertEqual(report["status"], "BLOCKED")
        azure.assert_not_called()


class PositivePortalTests(PortalCase):
    phase = "positive"

    def test_supplied_authoritative_evidence_matches_exact_rows_and_portal_display(self):
        with patch.object(finops, "AzureClient") as azure:
            report = self.check()
        self.assertEqual(report["status"], "CAPTURED_PORTAL_PARITY_PASS")
        self.assertFalse(report["liveQueryExecuted"])
        self.assertFalse(report["identityVerifiedThisRun"])
        self.assertEqual(report["comparison"]["displayComparisons"][0]["queryExact"], "0.008")
        self.assertEqual(report["comparison"]["displayComparisons"][0]["queryDisplay"], "0.01")
        azure.assert_not_called()

    def test_live_mode_binds_current_invoker_and_runs_the_exact_approved_plan(self):
        with patch.object(finops, "AzureClient") as azure, \
                patch.object(finops, "execute_plan", return_value=self.actual) as query:
            report = self.check("live", self.plan["sha256"])
        self.assertEqual(report["status"], "LIVE_PORTAL_PARITY_PASS")
        self.assertTrue(report["identityVerifiedThisRun"])
        self.assertTrue(report["liveQueryExecuted"])
        azure.assert_called_once_with(fixture.TENANT, fixture.INVOKER, [fixture.SUB])
        query.assert_called_once_with(self.plan, azure.return_value)

    def test_currencies_credits_and_declared_zero_and_three_decimal_displays(self):
        self.replace_records([
            ["-2.5", "USD", fixture.RESOURCE.lower(), "eastus", 20260901],
            ["100.5", "JPY", fixture.RESOURCE.lower(), "eastus", 20260901],
            ["1.2345", "KWD", fixture.RESOURCE.lower(), "eastus", 20260901],
        ])
        self.index["displayedTotals"] = [
            {"currency": "USD", "amount": "-2.50", "decimalPlaces": 2},
            {"currency": "JPY", "amount": "101", "decimalPlaces": 0},
            {"currency": "KWD", "amount": "1.235", "decimalPlaces": 3},
        ]
        report = self.check()
        self.assertEqual(report["status"], "CAPTURED_PORTAL_PARITY_PASS")
        self.assertTrue(all(r["match"] for r in report["comparison"]["displayComparisons"]))

    def test_real_zero_cost_records_can_match_without_treating_no_data_as_zero(self):
        self.replace_records([["0.00", "USD", fixture.RESOURCE.lower(), "eastus", 20260901]])
        self.index["displayedTotals"][0]["amount"] = "0.00"
        self.assertEqual(self.check()["status"], "CAPTURED_PORTAL_PARITY_PASS")

    def test_portal_reports_keep_raw_reference_and_query_provenance(self):
        report = self.check()
        root = self.root / "result"
        actual = finops.read_json(root / "actual.json")
        reference = finops.read_json(root / "portal-reference.json")
        self.assertEqual(report["comparison"]["actualSha256"], actual["sha256"])
        self.assertEqual(report["comparison"]["portalReferenceSha256"], reference["sha256"])
        self.assertEqual(report["portalIndexSha256"], finops.digest(self.index))
        self.assertIn("operator-attested", (root / "report.md").read_text(encoding="utf-8"))

    def test_resource_guard_preserves_nested_extension_and_subscription_resources(self):
        resources = [
            f"/subscriptions/{fixture.SUB}/providers/Microsoft.Authorization/roleAssignments/{fixture.OWNER}",
            fixture.RG + "/providers/Microsoft.Sql/servers/sql1/databases/db1",
            fixture.RESOURCE + "/providers/Microsoft.Insights/diagnosticSettings/default",
        ]
        for resource in resources:
            with self.subTest(resource=resource):
                self.assertEqual(finops.resource_id(resource), resource.lower())
