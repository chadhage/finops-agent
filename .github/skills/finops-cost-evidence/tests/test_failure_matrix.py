from __future__ import annotations

import base64
import copy
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import Mock, patch

import test_finops as fixture


finops = fixture.finops
MISSING = object()


def change(document: dict, path: tuple[str, ...], value: object) -> None:
    target = document
    for key in path[:-1]:
        target = target[key]
    if value is MISSING:
        del target[path[-1]]
    else:
        target[path[-1]] = copy.deepcopy(value)


class CliCase(unittest.TestCase):
    def assert_blocked(self, command: str, documents: dict, extra: list[str] | None = None) -> None:
        with tempfile.TemporaryDirectory(prefix="finops-negative-") as directory:
            root = Path(directory)
            arguments = [command]
            for flag, value in documents.items():
                source = root / (flag + ".json")
                finops.write_json(source, value)
                arguments += ["--" + flag, str(source)]
            output = root / "must-not-exist.json"
            arguments += [*(extra or []), "--out", str(output)]
            with patch("sys.stderr", new_callable=io.StringIO) as errors:
                status = finops.main(arguments)
            self.assertEqual(status, 2, "Invalid input was accepted by the CLI.")
            self.assertIn("FinOps blocked:", errors.getvalue(), "Failure was not explicitly surfaced.")
            self.assertFalse(output.exists(), "A blocked request produced a success-shaped artifact.")


class NegativeScenarioTests(CliCase):
    phase = "negative"


SCENARIO_MUTATIONS = [
    ("boolean_schema_version", ("schemaVersion",), True),
    ("decimal_schema_version", ("schemaVersion",), 1.0),
    ("unknown_schema_version", ("schemaVersion",), 2),
    ("malformed_tenant_uuid", ("tenantId",), "not-a-uuid"),
    ("null_principal", ("principalId",), None),
    ("empty_subscription_allowlist", ("approvedSubscriptionIds",), []),
    ("null_subscription_allowlist", ("approvedSubscriptionIds",), None),
    ("string_subscription_allowlist", ("approvedSubscriptionIds",), fixture.SUB),
    ("duplicate_subscription_allowlist", ("approvedSubscriptionIds",), [fixture.SUB, fixture.SUB]),
    ("mixed_subscription_allowlist", ("approvedSubscriptionIds",), [fixture.SUB, 7]),
    ("unsupported_cost_basis", ("costBasis",), "Usage"),
    ("combined_cost_bases", ("costBasis",), ["ActualCost", "AmortizedCost"]),
    ("null_period", ("period",), None),
    ("array_period", ("period",), []),
    ("missing_period_end", ("period", "to"), MISSING),
    ("non_utc_period", ("period", "from"), "2026-09-01T00:00:00-04:00"),
    ("invalid_calendar_day", ("period", "from"), "2026-09-31T00:00:00Z"),
    ("reversed_period", ("period", "from"), "2026-10-01T00:00:00Z"),
    ("partial_reporting_day", ("period", "to"), "2026-09-30T12:00:00Z"),
    ("null_selection", ("selection",), None),
    ("array_selection", ("selection",), []),
    ("unknown_selector", ("selection",), {"region": ["eastus"]}),
    ("empty_region_selector", ("selection",), {"regions": []}),
    ("null_region_value", ("selection",), {"regions": [None]}),
    ("blank_region_value", ("selection",), {"regions": [" "]}),
    ("unknown_region", ("selection",), {"regions": ["a nonexistent region"]}),
    ("empty_tags_selector", ("selection",), {"tags": []}),
    ("empty_tag_key", ("selection",), {"tags": [{"key": "", "values": ["checkout"]}]}),
    ("duplicate_casefolded_tag_keys", ("selection",), {"tags": [
        {"key": "Application", "values": ["checkout"]}, {"key": "APPLICATION", "values": ["data"]}]}),
    ("empty_tag_values", ("selection",), {"tags": [{"key": "Application", "values": []}]}),
    ("extra_tag_field", ("selection",), {"tags": [{"key": "Application", "values": ["checkout"], "or": True}]}),
    ("missing_owner_semantics", ("selection",), {"owners": {"users": [fixture.OWNER]}}),
    ("invented_owner_kind", ("selection",), {"owners": {"kind": "contributor", "users": [fixture.OWNER]}}),
    ("empty_owner_array", ("selection",), {"owners": {"kind": "rbac", "users": []}}),
    ("unresolved_owner_email", ("selection",), {"owners": {"kind": "rbac", "users": ["missing@example.test"]}}),
    ("unapproved_subscription", ("selection",), {"subscriptionIds": [fixture.OTHER_SUB]}),
    ("unresolved_subscription_name", ("selection",), {"subscriptionNames": ["missing"]}),
    ("unresolved_management_group", ("selection",), {"managementGroupNames": ["missing"]}),
    ("unresolved_resource_group", ("selection",), {"resourceGroupNames": ["missing"]}),
    ("missing_current_resource", ("selection",), {"resourceIds": [fixture.RESOURCE + "-deleted"]}),
]
for field in fixture.scenario():
    SCENARIO_MUTATIONS.append(("missing_" + field, (field,), MISSING))


def scenario_case(path: tuple[str, ...], value: object):
    def test(self: NegativeScenarioTests) -> None:
        scenario = fixture.scenario()
        change(scenario, path, value)
        self.assert_blocked("resolve", {"scenario": scenario, "catalog": fixture.catalog()})
    return test


for name, path, value in SCENARIO_MUTATIONS:
    setattr(NegativeScenarioTests, "test_" + name, scenario_case(path, value))


class NegativeCatalogTests(CliCase):
    phase = "negative"

    def test_null_catalog_root(self):
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": None})

    def test_null_coverage_object(self):
        source = fixture.catalog()
        source["coverage"] = None
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_array_coverage_object(self):
        source = fixture.catalog()
        source["coverage"] = []
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_boolean_catalog_schema_version(self):
        source = fixture.catalog()
        source["schemaVersion"] = True
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_future_catalog_timestamp(self):
        source = fixture.catalog()
        source["collectedAt"] = "9999-12-31T23:59:59Z"
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_false_inventory_coverage(self):
        source = fixture.catalog()
        source["coverage"]["resources"] = False
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_numeric_inventory_coverage(self):
        source = fixture.catalog()
        source["coverage"]["resources"] = 1
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_case_insensitive_duplicate_resource(self):
        source = fixture.catalog()
        source["resources"].append({**source["resources"][0], "id": fixture.RESOURCE.upper()})
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_resource_subscription_metadata_disagrees(self):
        source = fixture.catalog()
        source["resources"][0]["subscriptionId"] = fixture.OTHER_SUB
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_null_resource_tags(self):
        source = fixture.catalog()
        source["resources"][0]["tags"] = None
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_null_resource_location(self):
        source = fixture.catalog()
        source["resources"][0]["location"] = None
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_subscription_id_is_not_a_resource_id(self):
        source = fixture.catalog()
        source["resources"][0]["id"] = f"/subscriptions/{fixture.SUB}"
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_incomplete_provider_resource_id(self):
        source = fixture.catalog()
        source["resources"][0]["id"] = fixture.RG + "/providers/Microsoft.Compute/virtualMachines"
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_dot_segment_resource_id(self):
        source = fixture.catalog()
        source["resources"][0]["id"] += "/.."
        self.assert_blocked("resolve", {"scenario": fixture.scenario(), "catalog": source})

    def test_resource_reference_has_no_source(self):
        scenario = fixture.scenario()
        reference = {"scenarioSha256": finops.digest(scenario), "source": "",
                     "capturedAt": fixture.AS_OF, "resourceIds": [fixture.RESOURCE, fixture.SECOND]}
        self.assert_blocked("resolve", {"scenario": scenario, "catalog": fixture.catalog(),
                                        "resource-reference": reference})

    def test_duplicate_reference_resource_ids(self):
        scenario = fixture.scenario()
        reference = {"scenarioSha256": finops.digest(scenario), "source": "synthetic independent set",
                     "capturedAt": fixture.AS_OF, "resourceIds": [fixture.RESOURCE, fixture.RESOURCE.upper()]}
        self.assert_blocked("resolve", {"scenario": scenario, "catalog": fixture.catalog(),
                                        "resource-reference": reference})

    def test_business_owner_with_blank_freshness_rule(self):
        scenario, source = fixture.scenario(), fixture.catalog()
        scenario["selection"] = {"owners": {"kind": "business", "users": [fixture.OWNER]}}
        source["ownerBindings"][1]["freshnessRule"] = "   "
        self.assert_blocked("resolve", {"scenario": scenario, "catalog": source})

    def test_rbac_owner_with_blank_source(self):
        scenario, source = fixture.scenario(), fixture.catalog()
        scenario["selection"] = {"owners": {"kind": "rbac", "users": [fixture.OWNER]}}
        source["ownerBindings"][0]["source"] = "   "
        self.assert_blocked("resolve", {"scenario": scenario, "catalog": source})

    def test_inactive_owner_is_not_used(self):
        scenario, source = fixture.scenario(), fixture.catalog()
        scenario["selection"] = {"owners": {"kind": "rbac", "users": [fixture.OWNER]}}
        source["ownerBindings"][0]["effective"] = False
        self.assert_blocked("resolve", {"scenario": scenario, "catalog": source})


def profile() -> dict:
    return {"id": fixture.SUB, "tenantId": fixture.TENANT, "environmentName": "AzureCloud",
            "state": "Enabled", "name": "Synthetic subscription", "user": {"type": "user"}}


def token(changes: dict | None = None) -> str:
    claims = {"oid": fixture.INVOKER, "tid": fixture.TENANT, "aud": finops.ARM,
              "exp": int(finops.time.time()) + 3600}
    claims.update(changes or {})
    payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    return "synthetic." + payload + ".not-a-real-signature"


class NegativeIdentityTests(CliCase):
    phase = "negative"

    def test_null_cli_user_profile(self):
        context = profile()
        context["user"] = None
        with patch.object(finops, "cli_json", return_value=context):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])

    def test_unsupported_azure_cloud(self):
        context = profile()
        context["environmentName"] = "AzureUSGovernment"
        with patch.object(finops, "cli_json", return_value=context):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])

    def test_disabled_subscription(self):
        context = profile()
        context["state"] = "Disabled"
        with patch.object(finops, "cli_json", return_value=context):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])

    def test_expired_token(self):
        with patch.object(finops, "cli_json", side_effect=[profile(), {"accessToken": token({"exp": 1})}]):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])

    def test_token_expiring_at_the_safety_boundary(self):
        boundary = int(finops.time.time()) + 60
        with patch.object(finops, "cli_json", side_effect=[profile(), {"accessToken": token({"exp": boundary})}]):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])

    def test_wrong_token_audience(self):
        with patch.object(finops, "cli_json", side_effect=[profile(), {"accessToken": token({"aud": "https://graph.microsoft.com"})}]):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])

    def test_app_only_token_with_user_shaped_profile(self):
        with patch.object(finops, "cli_json", side_effect=[profile(), {"accessToken": token({"idtyp": "app"})}]):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])

    def test_cli_missing_is_not_auto_installed(self):
        with patch.object(finops.shutil, "which", return_value=None):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])

    def test_cli_failure_has_no_identity_fallback(self):
        with patch.object(finops.shutil, "which", return_value="synthetic-az"), \
                patch.object(finops.subprocess, "run", return_value=Mock(returncode=1)) as process:
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])
        self.assertEqual(process.call_count, 1)


class NegativeTransportTests(unittest.TestCase):
    phase = "negative"

    def client(self) -> finops.AzureClient:
        client = object.__new__(finops.AzureClient)
        client.subscriptions = [fixture.SUB]
        client.tokens = {fixture.SUB: "synthetic-token-must-not-leak"}
        client.opener = Mock()
        return client

    def test_excessive_retry_delay_does_not_sleep_or_retry(self):
        client = self.client()
        url = fixture.plan_for()["requests"][0]["url"]
        client.opener.open.side_effect = urllib.error.HTTPError(url, 429, "synthetic", {"Retry-After": "61"}, None)
        with patch.object(finops.time, "sleep") as sleep, self.assertRaisesRegex(finops.EvidenceError, "HTTP 429"):
            client.request("POST", url, fixture.SUB, {})
        self.assertEqual(client.opener.open.call_count, 1)
        sleep.assert_not_called()

    def test_retry_exhaustion_remains_failure(self):
        client = self.client()
        url = fixture.plan_for()["requests"][0]["url"]
        client.opener.open.side_effect = [
            urllib.error.HTTPError(url, 503, "synthetic", {"Retry-After": "0"}, None),
            urllib.error.HTTPError(url, 503, "synthetic", {"Retry-After": "0"}, None)]
        with patch.object(finops.time, "sleep") as sleep, self.assertRaisesRegex(finops.EvidenceError, "HTTP 503"):
            client.request("POST", url, fixture.SUB, {})
        self.assertEqual(client.opener.open.call_count, 2)
        sleep.assert_called_once_with(0)

    def test_network_failure_is_not_empty_success(self):
        client = self.client()
        client.opener.open.side_effect = urllib.error.URLError("synthetic transport timeout")
        with self.assertRaisesRegex(finops.EvidenceError, "transport failed"):
            client.request("POST", fixture.plan_for()["requests"][0]["url"], fixture.SUB, {})

    def test_graph_repeated_skip_token(self):
        client = Mock(subscriptions=[fixture.SUB])
        rows = {"count": 1, "totalRecords": 2, "resultTruncated": True, "$skipToken": "same",
                "data": [{"id": fixture.RESOURCE}]}
        client.request.side_effect = [fixture.page("synthetic", json.dumps(rows))] * 2
        with self.assertRaisesRegex(finops.EvidenceError, "Repeated/invalid"):
            finops.collect_graph(client, finops.RESOURCE_QUERY)

    def test_graph_numeric_truncation_flag_is_not_boolean(self):
        client = Mock(subscriptions=[fixture.SUB])
        rows = {"count": 1, "totalRecords": 1, "resultTruncated": 0, "data": [{"id": fixture.RESOURCE}]}
        client.request.return_value = fixture.page("synthetic", json.dumps(rows))
        with self.assertRaises(finops.EvidenceError, msg="Malformed completeness metadata was accepted."):
            finops.collect_graph(client, finops.RESOURCE_QUERY)

    def test_graph_boolean_count_is_not_an_integer(self):
        client = Mock(subscriptions=[fixture.SUB])
        rows = {"count": True, "totalRecords": 1, "resultTruncated": False, "data": [{"id": fixture.RESOURCE}]}
        client.request.return_value = fixture.page("synthetic", json.dumps(rows))
        with self.assertRaises(finops.EvidenceError, msg="Boolean row count was accepted."):
            finops.collect_graph(client, finops.RESOURCE_QUERY)


def http_error_case(code: int):
    def test(self: NegativeTransportTests) -> None:
        client = self.client()
        url = fixture.plan_for()["requests"][0]["url"]
        client.opener.open.side_effect = urllib.error.HTTPError(
            url, code, "synthetic", {"x-ms-request-id": "synthetic-trace"}, None)
        with self.assertRaisesRegex(finops.EvidenceError, f"HTTP {code}.*synthetic-trace") as failure:
            client.request("POST", url, fixture.SUB, {})
        self.assertEqual(client.opener.open.call_count, 1)
        self.assertNotIn("synthetic-token-must-not-leak", str(failure.exception))
    return test


for status_code in (400, 401, 403, 404, 500, 504):
    setattr(NegativeTransportTests, f"test_http_{status_code}_is_explicit", http_error_case(status_code))


class NegativeCostCaptureTests(CliCase):
    phase = "negative"

    def test_boolean_capture_schema_version(self):
        capture = fixture.bundle_for()
        capture["schemaVersion"] = True
        self.assert_blocked("report", {"actual": fixture.reseal(capture)})

    def test_duplicate_ungrouped_control_currency_rows(self):
        capture = fixture.replace_raw(fixture.bundle_for(), 1,
                                      fixture.raw_response("control", [["0.004", "USD"], ["0.004", "USD"]]))
        self.assert_blocked("report", {"actual": capture})

    def test_offline_capture_reuses_the_same_continuation_url(self):
        capture = fixture.bundle_for()
        url = capture["captures"][0]["pages"][0]["url"]
        capture["captures"][0]["pages"] = [
            fixture.page(url, fixture.raw_response("detail", fixture.records()[:1], url)),
            fixture.page(url, fixture.raw_response("detail", fixture.records()[1:]))]
        self.assert_blocked("report", {"actual": fixture.reseal(capture)})

    def test_empty_204_response_cannot_contain_a_body(self):
        capture = fixture.bundle_for()
        first = capture["captures"][0]["pages"][0]
        capture["captures"][0]["pages"] = [fixture.page(first["url"], "not empty", 204)]
        self.assert_blocked("report", {"actual": fixture.reseal(capture)})

    def test_boolean_cost_is_not_a_number(self):
        capture = fixture.replace_raw(fixture.bundle_for(), 0, fixture.raw_response(
            "detail", [["true", "USD", fixture.RESOURCE.lower(), "eastus", 20260901]]))
        self.assert_blocked("report", {"actual": capture})

    def test_null_cost_is_not_zero(self):
        capture = fixture.replace_raw(fixture.bundle_for(), 0, fixture.raw_response(
            "detail", [["null", "USD", fixture.RESOURCE.lower(), "eastus", 20260901]]))
        self.assert_blocked("report", {"actual": capture})

    def test_missing_currency_is_not_assumed_usd(self):
        capture = fixture.replace_raw(fixture.bundle_for(), 0, fixture.raw_response(
            "detail", [["0.008", "", fixture.RESOURCE.lower(), "eastus", 20260901]]))
        self.assert_blocked("report", {"actual": capture})

    def test_lowercase_currency_is_not_silently_normalized(self):
        capture = fixture.replace_raw(fixture.bundle_for(), 0, fixture.raw_response(
            "detail", [["0.008", "usd", fixture.RESOURCE.lower(), "eastus", 20260901]]))
        self.assert_blocked("report", {"actual": capture})

    def test_cost_schema_drift_between_pages(self):
        capture = fixture.bundle_for()
        url = capture["captures"][0]["pages"][0]["url"]
        following = url + "&$skiptoken=second"
        raw = json.loads(fixture.raw_response("detail", fixture.records()[1:]))
        raw["properties"]["columns"].reverse()
        raw["properties"]["rows"][0].reverse()
        capture["captures"][0]["pages"] = [
            fixture.page(url, fixture.raw_response("detail", fixture.records()[:1], following)),
            fixture.page(following, json.dumps(raw))]
        self.assert_blocked("report", {"actual": fixture.reseal(capture)})

    def test_non_success_status_is_not_a_report(self):
        capture = fixture.bundle_for()
        capture["captures"][0]["pages"][0]["status"] = 403
        self.assert_blocked("report", {"actual": fixture.reseal(capture)})

    def test_reference_cannot_silently_change_the_region(self):
        actual = fixture.bundle_for()
        changed = fixture.records()
        changed[0][3] = "westus"
        reference = fixture.bundle_for(actual["plan"], changed)
        self.assert_blocked("report", {"actual": actual, "reference": reference})

    def test_reference_cannot_silently_change_the_usage_day(self):
        actual = fixture.bundle_for()
        changed = fixture.records()
        changed[0][4] = 20260902
        reference = fixture.bundle_for(actual["plan"], changed)
        self.assert_blocked("report", {"actual": actual, "reference": reference})

    def test_same_total_in_another_currency_is_not_parity(self):
        actual = fixture.bundle_for()
        changed = fixture.records()
        for row in changed:
            row[1] = "EUR"
        reference = fixture.bundle_for(actual["plan"], changed)
        self.assert_blocked("report", {"actual": actual, "reference": reference})


class NegativeReportOutputTests(CliCase):
    phase = "negative"

    def test_pdf_exit_zero_without_pdf_is_a_failure(self):
        with tempfile.TemporaryDirectory(prefix="finops-pdf-negative-") as directory:
            browser = Path(directory) / "synthetic-browser.exe"
            browser.write_text("not executable; mocked", encoding="utf-8")
            with patch.object(finops.subprocess, "run", return_value=Mock(returncode=0)):
                self.assert_blocked("report", {"actual": fixture.bundle_for()},
                                    ["--format", "pdf", "--browser", str(browser)])

    def test_pdf_timeout_does_not_leave_success_output(self):
        with tempfile.TemporaryDirectory(prefix="finops-pdf-negative-") as directory:
            browser = Path(directory) / "synthetic-browser.exe"
            browser.write_text("not executable; mocked", encoding="utf-8")
            error = finops.subprocess.TimeoutExpired("synthetic-browser", 120)
            with patch.object(finops.subprocess, "run", side_effect=error):
                self.assert_blocked("report", {"actual": fixture.bundle_for()},
                                    ["--format", "pdf", "--browser", str(browser)])

    def test_pdf_browser_missing_is_a_failure(self):
        self.assert_blocked("report", {"actual": fixture.bundle_for()}, ["--format", "pdf"])

    def test_read_only_output_parent_is_explicit(self):
        with tempfile.TemporaryDirectory(prefix="finops-write-negative-") as directory:
            root = Path(directory)
            actual, output = root / "actual.json", root / "must-not-exist.md"
            finops.write_json(actual, fixture.bundle_for())
            with patch.object(finops, "write_text", side_effect=PermissionError("synthetic write permission denied")), \
                    patch("sys.stderr", new_callable=io.StringIO) as errors:
                status = finops.main(["report", "--actual", str(actual), "--out", str(output)])
            self.assertEqual(status, 2)
            self.assertIn("synthetic write permission denied", errors.getvalue())
            self.assertFalse(output.exists())
