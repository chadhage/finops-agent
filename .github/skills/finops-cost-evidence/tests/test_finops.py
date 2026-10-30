from __future__ import annotations

import base64
import copy
import io
import json
import sys
import tempfile
import time
import unittest
import urllib.error
from decimal import Decimal
from pathlib import Path
from unittest.mock import Mock, patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import finops


TENANT = "10000000-0000-0000-0000-000000000001"
INVOKER = "20000000-0000-0000-0000-000000000001"
OWNER = "20000000-0000-0000-0000-000000000002"
OTHER_OWNER = "20000000-0000-0000-0000-000000000003"
SUB = "30000000-0000-0000-0000-000000000001"
OTHER_SUB = "30000000-0000-0000-0000-000000000002"
RG = f"/subscriptions/{SUB}/resourceGroups/app"
RESOURCE = RG + "/providers/Microsoft.Compute/virtualMachines/vm1"
SECOND = RG + "/providers/Microsoft.Storage/storageAccounts/store1"
MG = "/providers/Microsoft.Management/managementGroups/engineering"
AS_OF = "2026-09-30T12:00:00Z"


def scenario() -> dict:
    return {"schemaVersion": 1, "tenantId": TENANT, "principalId": INVOKER,
            "approvedSubscriptionIds": [SUB], "costBasis": "ActualCost",
            "period": {"from": "2026-09-01T00:00:00Z", "to": "2026-09-30T23:59:59Z"},
            "selection": {}}


def catalog() -> dict:
    return {
        "schemaVersion": 1, "tenantId": TENANT, "principalId": INVOKER, "collectedAt": AS_OF,
        "coverage": dict.fromkeys(("subscriptions", "resources", "resourceGroups", "managementGroups",
                                   "locations", "users", "rbacOwners", "businessOwners"), True),
        "subscriptions": [{"id": SUB, "name": "Production",
                           "managementGroups": [{"id": MG, "name": "Engineering"}]}],
        "resourceGroups": [{"id": RG, "name": "app"}],
        "resources": [
            {"id": RESOURCE, "subscriptionId": SUB, "location": "eastus", "tags": {"Application": "checkout"}},
            {"id": SECOND, "subscriptionId": SUB, "location": "westus", "tags": {"Application": "data"}},
        ],
        "locations": [{"name": "eastus", "displayName": "East US"}, {"name": "westus", "displayName": "West US"}],
        "users": [{"id": OWNER, "displayName": "App Owner", "mail": "owner@example.test",
                   "userPrincipalName": "owner@tenant.example.test"},
                  {"id": OTHER_OWNER, "displayName": "Data Owner", "mail": "data@example.test",
                   "userPrincipalName": "data@tenant.example.test"}],
        "ownerBindings": [
            {"kind": "rbac", "userId": OWNER, "scopeId": RG, "source": "synthetic ARM assignment/group evidence",
             "roleDefinitionId": finops.OWNER_ROLE, "effective": True, "exclusionsChecked": True,
             "validatedAt": AS_OF},
            {"kind": "business", "userId": OWNER, "scopeId": RESOURCE, "source": "synthetic approved CMDB record",
             "effective": True, "validatedAt": AS_OF, "freshUntil": "2026-12-31T23:59:59Z",
             "freshnessRule": "Synthetic customer-approved validity interval"},
        ],
    }


def plan_for(selection: dict | None = None) -> dict:
    request = scenario()
    request["selection"] = selection or {}
    return finops.make_plan(finops.resolve_scope(request, catalog()))


def raw_response(kind: str, rows: list[list], next_link: str | None = None) -> str:
    columns = [{"name": "PreTaxCost", "type": "Number"}, {"name": "Currency", "type": "String"}]
    if kind == "detail":
        columns += [{"name": "ResourceId", "type": "String"}, {"name": "ResourceLocation", "type": "String"},
                    {"name": "UsageDate", "type": "Number"}]
    encoded = []
    for row in rows:
        encoded.append("[" + str(row[0]) + "," + ",".join(json.dumps(v) for v in row[1:]) + "]")
    return ('{"properties":{"columns":' + json.dumps(columns) + ',"rows":[' + ",".join(encoded)
            + '],"nextLink":' + json.dumps(next_link) + "}}")


def page(url: str, raw: str, status: int = 200) -> dict:
    return {"url": url, "raw": raw, "status": status, "sha256": finops.raw_digest(raw),
            "retrievedAt": AS_OF, "azureRequestId": "synthetic-request-id"}


def records() -> list[list]:
    return [["0.004", "USD", RESOURCE.lower(), "eastus", 20260901],
            ["0.004", "USD", SECOND.lower(), "westus", 20260901]]


def bundle_for(plan: dict | None = None, entries: list[list] | None = None) -> dict:
    plan = plan or plan_for()
    entries = records() if entries is None else entries
    captures = []
    for request in plan["requests"]:
        chunk = request["body"]["dataset"].get("filter", {}).get("dimensions", {}).get("values")
        selected = [r for r in entries if chunk is None or r[2] in chunk]
        if request["kind"] == "detail":
            rows = selected
        else:
            currencies = sorted({r[1] for r in selected})
            rows = [[format(finops.exact_sum([Decimal(r[0]) for r in selected if r[1] == c]), "f"), c]
                    for c in currencies]
        captures.append({"requestId": request["id"],
                         "pages": [page(request["url"], raw_response(request["kind"], rows))]})
    return finops.sealed({"schemaVersion": 1, "captureId": str(finops.uuid.uuid4()),
                         "capturedAt": AS_OF, "source": "synthetic-unit-test",
                         "plan": plan, "captures": captures})


def reseal(value: dict) -> dict:
    return finops.sealed({k: v for k, v in value.items() if k != "sha256"})


def replace_raw(bundle: dict, capture: int, raw: str) -> dict:
    result = copy.deepcopy(bundle)
    old_page = result["captures"][capture]["pages"][0]
    result["captures"][capture]["pages"][0] = page(old_page["url"], raw)
    return reseal(result)


class ScopeTests(unittest.TestCase):
    def test_intersects_categories_and_unions_values(self):
        request = scenario()
        request["selection"] = {
            "subscriptionNames": ["production"], "managementGroupNames": ["Engineering"],
            "resourceGroupIds": [RG], "owners": {"kind": "either", "users": ["owner@example.test", "Data Owner"]},
            "tags": [{"key": "application", "values": ["checkout", "another"]}], "regions": ["East US"],
        }
        manifest = finops.resolve_scope(request, catalog())
        self.assertEqual(manifest["resourceIds"], [RESOURCE.lower()])
        self.assertEqual(manifest["scopeMode"], "current-resource-set")
        self.assertEqual({b["kind"] for b in manifest["ownerEvidence"]}, {"rbac", "business"})

    def test_exact_arm_scope_boundary(self):
        self.assertFalse(finops.scope_contains(RG, RG + "lication/providers/Microsoft.Compute/virtualMachines/vm", []))
        self.assertTrue(finops.scope_contains(MG, RESOURCE, [{"id": MG}]))

    def test_ambiguous_subscription_name_is_blocked(self):
        request, source = scenario(), catalog()
        request["approvedSubscriptionIds"].append(OTHER_SUB)
        request["selection"] = {"subscriptionNames": ["Production"]}
        source["subscriptions"].append({"id": OTHER_SUB, "name": "Production", "managementGroups": []})
        with self.assertRaisesRegex(finops.EvidenceError, "resolved to 2"):
            finops.resolve_scope(request, source)

    def test_ambiguous_resource_group_name_is_blocked(self):
        request, source = scenario(), catalog()
        request["approvedSubscriptionIds"].append(OTHER_SUB)
        request["selection"] = {"resourceGroupNames": ["app"]}
        source["subscriptions"].append({"id": OTHER_SUB, "name": "Other", "managementGroups": []})
        source["resourceGroups"].append({"id": f"/subscriptions/{OTHER_SUB}/resourceGroups/app", "name": "app"})
        with self.assertRaisesRegex(finops.EvidenceError, "resolved to 2"):
            finops.resolve_scope(request, source)

    def test_ambiguous_directory_identity_is_blocked(self):
        request, source = scenario(), catalog()
        request["selection"] = {"owners": {"kind": "rbac", "users": ["App Owner"]}}
        source["users"][1]["displayName"] = "App Owner"
        with self.assertRaisesRegex(finops.EvidenceError, "resolved to 2"):
            finops.resolve_scope(request, source)

    def test_business_owner_is_not_rbac_owner(self):
        request = scenario()
        request["selection"] = {"owners": {"kind": "business", "users": [OWNER]}}
        self.assertEqual(finops.resolve_scope(request, catalog())["resourceIds"], [RESOURCE.lower()])
        request["selection"]["owners"]["kind"] = "rbac"
        self.assertEqual(len(finops.resolve_scope(request, catalog())["resourceIds"]), 2)

    def test_ownership_uncertainty_is_not_an_empty_match(self):
        for field, value, message in (
            ("effective", None, "unresolved"), ("exclusionsChecked", False, "unresolved"),
            ("roleDefinitionId", OTHER_OWNER, "built-in Owner"),
        ):
            request, source = scenario(), catalog()
            request["selection"] = {"owners": {"kind": "rbac", "users": [OWNER]}}
            source["ownerBindings"][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(finops.EvidenceError, message):
                finops.resolve_scope(request, source)

    def test_stale_business_ownership_is_blocked(self):
        request, source = scenario(), catalog()
        request["selection"] = {"owners": {"kind": "business", "users": ["owner@example.test"]}}
        source["ownerBindings"][1]["freshUntil"] = "2026-09-01T00:00:00Z"
        with self.assertRaisesRegex(finops.EvidenceError, "stale"):
            finops.resolve_scope(request, source)

    def test_management_group_owner_needs_complete_ancestry(self):
        request, source = scenario(), catalog()
        request["selection"] = {"owners": {"kind": "rbac", "users": [OWNER]}}
        source["coverage"]["managementGroups"] = False
        source["ownerBindings"][0]["scopeId"] = MG
        with self.assertRaisesRegex(finops.EvidenceError, "complete ancestry"):
            finops.resolve_scope(request, source)

    def test_unknown_or_empty_filter_is_blocked(self):
        for selection in ({"regons": ["eastus"]}, {"regions": []},
                          {"owners": {"users": [OWNER]}}, {"tags": []}):
            request = scenario()
            request["selection"] = selection
            with self.subTest(selection=selection), self.assertRaises(finops.EvidenceError):
                finops.resolve_scope(request, catalog())

    def test_tags_are_exact_values_not_fuzzy_or_case_folded(self):
        request = scenario()
        request["selection"] = {"tags": [{"key": "APPLICATION", "values": ["Checkout"]}]}
        with self.assertRaisesRegex(finops.EvidenceError, "No resources matched"):
            finops.resolve_scope(request, catalog())

    def test_unselected_subscription_and_inventory_are_blocked(self):
        request = scenario()
        request["selection"] = {"subscriptionIds": [OTHER_SUB]}
        with self.assertRaisesRegex(finops.EvidenceError, "boundary"):
            finops.resolve_scope(request, catalog())
        source = catalog()
        source["resources"][0]["id"] = RESOURCE.replace(SUB, OTHER_SUB)
        with self.assertRaisesRegex(finops.EvidenceError, "boundary"):
            finops.resolve_scope(scenario(), source)

    def test_missing_inventory_or_mismatched_identity_is_blocked(self):
        source = catalog()
        source["coverage"]["resources"] = False
        with self.assertRaisesRegex(finops.EvidenceError, "Incomplete"):
            finops.resolve_scope(scenario(), source)
        source = catalog()
        source["principalId"] = OWNER
        with self.assertRaisesRegex(finops.EvidenceError, "identity"):
            finops.resolve_scope(scenario(), source)

    def test_exact_resource_reference_required_for_scope_validation(self):
        request, source = scenario(), catalog()
        reference = {"scenarioSha256": finops.digest(request), "source": "Synthetic independent inventory",
                     "capturedAt": AS_OF, "resourceIds": [RESOURCE, SECOND]}
        manifest = finops.resolve_scope(request, source, reference)
        self.assertEqual(manifest["scopeReference"]["status"], "exact-match")
        reference["resourceIds"].pop()
        with self.assertRaisesRegex(finops.EvidenceError, "exact resource sets"):
            finops.resolve_scope(request, source, reference)

    def test_partial_day_and_misspelled_basis_are_blocked(self):
        for change in ("period", "costBasis"):
            request = scenario()
            if change == "period":
                request["period"]["from"] = "2026-09-01T01:00:00Z"
            else:
                request["costBasis"] = "Actual"
            with self.subTest(change=change), self.assertRaises(finops.EvidenceError):
                finops.validate_scenario(request)


class PlanTests(unittest.TestCase):
    def test_resource_query_and_control_have_identical_filter_and_basis(self):
        request = scenario()
        request["costBasis"] = "AmortizedCost"
        request["selection"] = {"resourceIds": [RESOURCE]}
        plan = finops.make_plan(finops.resolve_scope(request, catalog()))
        detail, control = plan["requests"]
        self.assertEqual(detail["body"]["type"], "AmortizedCost")
        self.assertEqual(detail["body"]["timePeriod"], request["period"])
        self.assertEqual(detail["body"]["dataset"]["filter"], control["body"]["dataset"]["filter"])
        self.assertEqual(detail["body"]["dataset"]["filter"]["dimensions"]["values"], [RESOURCE.lower()])
        self.assertNotIn("grouping", control["body"]["dataset"])
        self.assertEqual(len(detail["body"]["dataset"]["grouping"]), 2)

    def test_resource_chunks_are_disjoint_and_complete(self):
        request, source = scenario(), catalog()
        request["selection"] = {"regions": ["eastus"]}
        source["resources"] = [{"id": RG + f"/providers/Microsoft.Compute/virtualMachines/vm{n}",
                                "location": "eastus", "tags": {}} for n in range(205)]
        plan = finops.make_plan(finops.resolve_scope(request, source))
        chunks = [r["body"]["dataset"]["filter"]["dimensions"]["values"]
                  for r in plan["requests"] if r["kind"] == "detail"]
        self.assertEqual([len(c) for c in chunks], [100, 100, 5])
        self.assertEqual(len(set().union(*(set(c) for c in chunks))), 205)

    def test_subscription_scope_preserves_unallocated_costs(self):
        plan = plan_for()
        self.assertTrue(all("filter" not in r["body"]["dataset"] for r in plan["requests"]))
        bundle = bundle_for(plan, [["1.25", "USD", "", "", 20260901]])
        self.assertEqual(finops.validate_bundle(bundle)["totals"], {"USD": Decimal("1.25")})

    def test_filter_cannot_be_removed_by_resealing_manifest(self):
        manifest = finops.resolve_scope(
            {**scenario(), "selection": {"resourceIds": [RESOURCE]}}, catalog())
        manifest["scopeMode"] = "subscription-charges"
        with self.assertRaisesRegex(finops.EvidenceError, "subscription-wide"):
            finops.make_plan(reseal(manifest))

    def test_plan_cannot_contain_non_generated_operations(self):
        plan = plan_for()
        plan["requests"][0]["url"] = finops.ARM + "/subscriptions/" + SUB + "/delete"
        with self.assertRaisesRegex(finops.EvidenceError, "modified operations"):
            finops.verify_plan(reseal(plan))

    def test_hash_tampering_is_blocked(self):
        plan = plan_for()
        plan["manifest"]["costBasis"] = "AmortizedCost"
        with self.assertRaisesRegex(finops.EvidenceError, "hash mismatch"):
            finops.verify_plan(plan)


class MoneyAndEvidenceTests(unittest.TestCase):
    def test_raw_numeric_parsing_and_large_sum_are_exact(self):
        value = finops.parse_json('{"cost":0.123456789012345678901234567890123456789}')["cost"]
        self.assertEqual(str(value), "0.123456789012345678901234567890123456789")
        total = finops.exact_sum([Decimal("99999999999999999999999999999.999"), Decimal("0.001")])
        self.assertEqual(format(total, "f"), "100000000000000000000000000000.000")

    def test_duplicate_json_keys_and_nonfinite_numbers_are_blocked(self):
        for raw in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(finops.EvidenceError):
                finops.parse_json(raw)

    def test_sum_is_not_sum_of_rounded_rows(self):
        self.assertEqual(finops.validate_bundle(bundle_for())["totals"]["USD"], Decimal("0.008"))
        self.assertEqual(finops.usd_display(Decimal("0.008")), "$0.01")
        self.assertEqual(finops.usd_display(Decimal("99999999999999999999999999999.995")),
                         "$100000000000000000000000000000.00")

    def test_credits_and_currencies_are_preserved(self):
        entries = records() + [["-2.50", "USD", RESOURCE.lower(), "eastus", 20260902],
                               ["100", "EUR", RESOURCE.lower(), "eastus", 20260902]]
        totals = finops.validate_bundle(bundle_for(entries=entries))["totals"]
        self.assertEqual(totals, {"USD": Decimal("-2.492"), "EUR": Decimal(100)})

    def test_internal_control_mismatch_is_blocked(self):
        bundle = replace_raw(bundle_for(), 1, raw_response("control", [["0.009", "USD"]]))
        with self.assertRaisesRegex(finops.EvidenceError, "Detail/control"):
            finops.validate_bundle(bundle)

    def test_empty_204_is_no_data_not_zero(self):
        bundle = bundle_for(entries=[])
        for capture in bundle["captures"]:
            capture["pages"] = [page(capture["pages"][0]["url"], "", 204)]
        bundle = reseal(bundle)
        self.assertEqual(finops.validate_bundle(bundle)["totals"], {})
        self.assertIn("not proof of zero", finops.markdown_report(finops.report_model(bundle)))

    def test_missing_query_schema_and_malformed_rows_are_blocked(self):
        bundle = bundle_for()
        broken = copy.deepcopy(bundle)
        broken["captures"].pop()
        with self.assertRaisesRegex(finops.EvidenceError, "missing or unexpected"):
            finops.validate_bundle(reseal(broken))
        for raw in (
            '{"properties":{"columns":[],"rows":[]}}',
            raw_response("detail", [["0.004", "USD"]]),
            raw_response("detail", [['"1.25"', "USD", RESOURCE.lower(), "eastus", 20260901]]),
        ):
            with self.subTest(raw=raw), self.assertRaises(finops.EvidenceError):
                finops.validate_bundle(replace_raw(bundle, 0, raw))

    def test_cross_scope_and_out_of_period_rows_are_blocked(self):
        for row in (
            ["0.008", "USD", RESOURCE.lower().replace(SUB, OTHER_SUB), "eastus", 20260901],
            ["0.008", "USD", RESOURCE.lower(), "eastus", 20261001],
            ["0.008", "USD", RESOURCE.lower(), "eastus", 20260931],
        ):
            with self.subTest(row=row), self.assertRaises(finops.EvidenceError):
                finops.validate_bundle(bundle_for(entries=[row]))

    def test_unexpected_resource_in_filtered_query_is_blocked(self):
        bundle = bundle_for(plan_for({"resourceIds": [RESOURCE]}))
        bundle = replace_raw(bundle, 0, raw_response("detail", [records()[1]]))
        with self.assertRaisesRegex(finops.EvidenceError, "exact resource filter"):
            finops.validate_bundle(bundle)

    def test_all_cost_pages_are_required_and_schema_is_stable(self):
        bundle = bundle_for()
        first = bundle["captures"][0]["pages"][0]
        following = first["url"].replace(finops.API_VERSION, "2021-10-01") + "&$skiptoken=second"
        first_page = page(first["url"], raw_response("detail", records()[:1], following))
        next_page = page(following, raw_response("detail", records()[1:]))
        bundle["captures"][0]["pages"] = [first_page, next_page]
        self.assertEqual(finops.validate_bundle(reseal(bundle))["totals"]["USD"], Decimal("0.008"))
        bundle["captures"][0]["pages"].pop()
        with self.assertRaisesRegex(finops.EvidenceError, "incomplete"):
            finops.validate_bundle(reseal(bundle))

    def test_duplicate_paged_rows_and_response_hash_tampering_are_blocked(self):
        bundle = replace_raw(bundle_for(), 0, raw_response("detail", [records()[0], records()[0]]))
        with self.assertRaisesRegex(finops.EvidenceError, "Duplicate aggregated"):
            finops.validate_bundle(bundle)
        bundle = bundle_for()
        bundle["captures"][0]["pages"][0]["raw"] += " "
        with self.assertRaisesRegex(finops.EvidenceError, "Raw response hash"):
            finops.validate_bundle(reseal(bundle))

    def test_reference_compares_per_resource_not_just_total(self):
        actual = bundle_for()
        changed = records()
        changed[0][0], changed[1][0] = "0.003", "0.005"
        comparison = finops.reconcile(actual, bundle_for(actual["plan"], changed))
        self.assertEqual(comparison["status"], "mismatch")
        self.assertEqual(len(comparison["differences"]), 2)
        self.assertEqual(comparison["tolerance"], "0")

    def test_exact_reference_match_and_self_reference_rejection(self):
        actual = bundle_for()
        reference = bundle_for(actual["plan"])
        self.assertEqual(finops.reconcile(actual, reference)["status"], "exact-match")
        with self.assertRaisesRegex(finops.EvidenceError, "itself"):
            finops.reconcile(actual, actual)

    def test_reference_with_different_cost_basis_is_blocked(self):
        other_scenario = scenario()
        other_scenario["costBasis"] = "AmortizedCost"
        other_plan = finops.make_plan(finops.resolve_scope(other_scenario, catalog()))
        with self.assertRaisesRegex(finops.EvidenceError, "Reference plan differs"):
            finops.reconcile(bundle_for(), bundle_for(other_plan))

    def test_future_or_inconsistent_cost_capture_times_are_blocked(self):
        bundle = bundle_for()
        bundle["capturedAt"] = "9999-12-31T23:59:59Z"
        with self.assertRaisesRegex(finops.EvidenceError, "capture time is in the future"):
            finops.validate_bundle(reseal(bundle))
        bundle = bundle_for()
        bundle["captures"][0]["pages"][0]["retrievedAt"] = "2026-10-01T00:00:00Z"
        with self.assertRaisesRegex(finops.EvidenceError, "later than the completed capture"):
            finops.validate_bundle(reseal(bundle))

    def test_import_reference_preserves_raw_precision_and_every_page(self):
        actual = bundle_for()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            index = {"source": "manual-azure-cli", "tenantId": TENANT, "principalId": INVOKER,
                     "capturedAt": AS_OF, "captures": []}
            for n, capture in enumerate(actual["captures"]):
                filename = f"page-{n}.json"
                raw_page = capture["pages"][0]
                (root / filename).write_text(raw_page["raw"], encoding="utf-8")
                index["captures"].append({"requestId": capture["requestId"], "pages": [
                    {"path": filename, "url": raw_page["url"], "status": 200}]})
            imported = finops.import_reference(actual["plan"], index, root)
            self.assertEqual(finops.reconcile(actual, imported)["status"], "exact-match")
            index["captures"].pop()
            with self.assertRaisesRegex(finops.EvidenceError, "missing or unexpected"):
                finops.import_reference(actual["plan"], index, root)


class AzureBoundaryTests(unittest.TestCase):
    def jwt(self, principal: str = INVOKER, tenant: str = TENANT) -> str:
        claims = {"oid": principal, "tid": tenant, "aud": finops.ARM + "/", "exp": int(time.time()) + 3600}
        encoded = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
        return "synthetic." + encoded + ".signature"

    def profile(self) -> dict:
        return {"id": SUB, "tenantId": TENANT, "environmentName": "AzureCloud", "state": "Enabled",
                "name": "Production", "user": {"type": "user"}}

    def test_identity_is_invoker_bound_without_account_switching(self):
        with patch.object(finops, "cli_json", side_effect=[self.profile(), {"accessToken": self.jwt()}]) as cli:
            context, _ = finops.azure_identity(TENANT, SUB, INVOKER)
        self.assertEqual(context["principalId"], INVOKER)
        self.assertNotIn("accessToken", context)
        self.assertTrue(all(call.args[0][:2] != ["account", "set"] for call in cli.call_args_list))

    def test_app_identity_wrong_tenant_or_wrong_invoker_is_blocked(self):
        profile = self.profile()
        profile["user"]["type"] = "servicePrincipal"
        with patch.object(finops, "cli_json", return_value=profile):
            with self.assertRaisesRegex(finops.EvidenceError, "interactive"):
                finops.azure_identity(TENANT, SUB, INVOKER)
        for token in (self.jwt(OWNER), self.jwt(tenant=OWNER)):
            with patch.object(finops, "cli_json", side_effect=[self.profile(), {"accessToken": token}]):
                with self.assertRaisesRegex(finops.EvidenceError, "Token identity"):
                    finops.azure_identity(TENANT, SUB, INVOKER)

    def test_continuation_cannot_exfiltrate_token_or_change_scope(self):
        initial = plan_for()["requests"][0]["url"]
        for url in (
            initial.replace("management.azure.com", "example.test"),
            initial.replace(SUB, OTHER_SUB), initial.replace("https:", "http:"),
            initial + "&redirect=https://example.test", initial + "&api-version=2025-03-01",
        ):
            with self.subTest(url=url), self.assertRaises(finops.EvidenceError):
                finops.validate_next_url(url, initial)
        with self.assertRaisesRegex(finops.EvidenceError, "redirect refused"):
            finops.NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.test")

    def test_only_read_operations_and_approved_scopes_are_allowed(self):
        client = object.__new__(finops.AzureClient)
        client.subscriptions = [SUB]
        for method, url, sid in (
            ("DELETE", finops.ARM + f"/subscriptions/{SUB}/locations", SUB),
            ("POST", finops.ARM + f"/subscriptions/{SUB}/providers/Microsoft.Resources/deployments/x", SUB),
            ("GET", finops.ARM + f"/subscriptions/{OTHER_SUB}/locations", OTHER_SUB),
        ):
            with self.subTest(method=method), self.assertRaises(finops.EvidenceError):
                client.request(method, url, sid)

    def test_403_is_explicit_and_never_zero_cost(self):
        client = object.__new__(finops.AzureClient)
        client.subscriptions, client.tokens = [SUB], {SUB: "synthetic-token"}
        client.opener = Mock()
        url = plan_for()["requests"][0]["url"]
        client.opener.open.side_effect = urllib.error.HTTPError(
            url, 403, "Forbidden", {"x-ms-request-id": "trace-403"}, None)
        with self.assertRaisesRegex(finops.EvidenceError, "HTTP 403.*trace-403"):
            client.request("POST", url, SUB, {})

    def test_rate_limit_retry_is_bounded_and_closes_error_response(self):
        client = object.__new__(finops.AzureClient)
        client.subscriptions, client.tokens = [SUB], {SUB: "synthetic-token"}
        client.opener = Mock()
        url = plan_for()["requests"][0]["url"]
        response = Mock()
        response.status, response.headers = 200, {}
        response.read.return_value = raw_response("control", [["0.008", "USD"]]).encode()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        error = urllib.error.HTTPError(url, 429, "Too Many Requests", {"Retry-After": "1"}, None)
        with patch.object(error, "close") as close:
            client.opener.open.side_effect = [error, response]
            with patch.object(finops.time, "sleep") as sleep:
                result = client.request("POST", url, SUB, {})
                sleep.assert_called_once_with(1)
            close.assert_called_once()
        error.close()
        self.assertEqual(result["status"], 200)
        self.assertEqual(client.opener.open.call_count, 2)

    def test_graph_pagination_is_complete_and_stable(self):
        client = Mock()
        client.subscriptions = [SUB]
        first = {"count": 1, "totalRecords": 2, "resultTruncated": "true", "$skipToken": "next",
                 "data": [{"id": RESOURCE}]}
        last = {"count": 1, "totalRecords": 2, "resultTruncated": "false", "data": [{"id": SECOND}]}
        client.request.side_effect = [page("synthetic", json.dumps(first)), page("synthetic", json.dumps(last))]
        data, _ = finops.collect_graph(client, finops.RESOURCE_QUERY)
        self.assertEqual(len(data), 2)
        self.assertEqual(client.request.call_args_list[1].args[3]["options"]["$skipToken"], "next")

    def test_graph_truncation_count_drift_and_duplicate_ids_are_blocked(self):
        examples = [
            [{"count": 1, "totalRecords": 2, "resultTruncated": "true", "data": [{"id": RESOURCE}]}],
            [{"count": 1, "totalRecords": 2, "resultTruncated": True, "$skipToken": "next", "data": [{"id": RESOURCE}]},
             {"count": 1, "totalRecords": 3, "resultTruncated": False, "data": [{"id": SECOND}]}],
            [{"count": 2, "totalRecords": 2, "resultTruncated": False,
              "data": [{"id": RESOURCE}, {"id": RESOURCE}]}],
        ]
        for responses in examples:
            client = Mock()
            client.subscriptions = [SUB]
            client.request.side_effect = [page("synthetic", json.dumps(r)) for r in responses]
            with self.subTest(responses=responses), self.assertRaises(finops.EvidenceError):
                finops.collect_graph(client, finops.RESOURCE_QUERY)

    def test_execute_preserves_tokens_only_in_client_not_evidence(self):
        plan = plan_for()
        expected = bundle_for(plan)
        client = Mock()
        client.tenant, client.principal, client.subscriptions = TENANT, INVOKER, [SUB]
        client.tokens = {SUB: "synthetic-token-never-persist"}
        client.request.side_effect = [c["pages"][0] for c in expected["captures"]]
        actual = finops.execute_plan(plan, client)
        self.assertNotIn("synthetic-token-never-persist", json.dumps(actual))
        self.assertEqual(finops.validate_bundle(actual)["totals"]["USD"], Decimal("0.008"))

    def inventory_client(self, tags: object = None, ancestry: bool = True) -> Mock:
        source = catalog()
        client = Mock()
        client.tenant, client.principal, client.subscriptions = TENANT, INVOKER, [SUB]
        client.contexts = {SUB: {"subscriptionName": "Production"}}
        resources = copy.deepcopy(source["resources"])
        resources[0]["tags"] = tags
        properties = {"managementGroupAncestorsChain": [{"name": "engineering", "displayName": "Engineering"}]}
        containers = [
            {"id": f"/subscriptions/{SUB}", "name": SUB, "subscriptionId": SUB,
             "type": "microsoft.resources/subscriptions", "properties": properties if ancestry else {}},
            {"id": RG, "name": "app", "subscriptionId": SUB,
             "type": "microsoft.resources/subscriptions/resourcegroups", "properties": {}},
        ]
        client.request.side_effect = [
            page("synthetic", json.dumps({"count": len(resources), "totalRecords": len(resources),
                                         "resultTruncated": False, "data": resources})),
            page("synthetic", json.dumps({"count": 2, "totalRecords": 2, "resultTruncated": False,
                                         "data": containers})),
            page("synthetic", json.dumps({"value": source["locations"]})),
        ]
        return client

    def test_inventory_collects_lineage_and_requires_supplied_owner_evidence(self):
        source = finops.collect_inventory(scenario(), self.inventory_client())
        self.assertEqual(len(source["sourcePages"]), 3)
        self.assertEqual(source["resources"][0]["tags"], {})
        self.assertEqual(source["subscriptions"][0]["managementGroups"][0]["id"], MG)
        self.assertFalse(source["coverage"]["businessOwners"])
        self.assertEqual(finops.resolve_scope(scenario(), source)["subscriptionIds"], [SUB])
        request = {**scenario(), "selection": {"owners": {"kind": "business", "users": [OWNER]}}}
        with self.assertRaisesRegex(finops.EvidenceError, "Directory"):
            finops.resolve_scope(request, source)

    def test_inventory_merges_only_identity_and_scope_bound_ownership(self):
        fixture = catalog()
        owners = {"tenantId": TENANT, "principalId": INVOKER, "subscriptionIds": [SUB], "collectedAt": AS_OF,
                  "coverage": {"users": True, "rbacOwners": True, "businessOwners": True},
                  "users": fixture["users"], "ownerBindings": fixture["ownerBindings"]}
        with patch.object(finops, "utc_now", return_value=AS_OF):
            source = finops.collect_inventory(scenario(), self.inventory_client(), owners)
            request = {**scenario(), "selection": {"owners": {"kind": "business", "users": ["owner@example.test"]}}}
            self.assertEqual(finops.resolve_scope(request, source)["resourceIds"], [RESOURCE.lower()])
        owners["principalId"] = OWNER
        with self.assertRaisesRegex(finops.EvidenceError, "another invoker"):
            finops.collect_inventory(scenario(), self.inventory_client(), owners)

    def test_inventory_does_not_hide_malformed_tags_or_missing_ancestry(self):
        with self.assertRaisesRegex(finops.EvidenceError, "tags are missing or malformed"):
            finops.collect_inventory(scenario(), self.inventory_client(tags=""))
        source = finops.collect_inventory(scenario(), self.inventory_client(ancestry=False))
        request = {**scenario(), "selection": {"managementGroupNames": ["Engineering"]}}
        with self.assertRaisesRegex(finops.EvidenceError, "ancestry is incomplete"):
            finops.resolve_scope(request, source)


class ReportingTests(unittest.TestCase):
    def test_no_reference_means_unverified_even_with_correct_internal_totals(self):
        model = finops.report_model(bundle_for())
        self.assertEqual(model["status"], "UNVERIFIED")
        self.assertIn("0.008", finops.markdown_report(model))
        self.assertIn("$0.01", finops.markdown_report(model))
        self.assertEqual(model["costParity"], "not-verified")

    def test_both_independent_references_gate_validated_status(self):
        request, source = scenario(), catalog()
        resource_reference = {"scenarioSha256": finops.digest(request), "source": "Synthetic portal inventory",
                              "capturedAt": AS_OF, "resourceIds": [RESOURCE, SECOND]}
        plan = finops.make_plan(finops.resolve_scope(request, source, resource_reference))
        actual, reference = bundle_for(plan), bundle_for(plan)
        self.assertEqual(finops.report_model(actual, reference)["status"], "VALIDATED AGAINST CAPTURED REFERENCES")
        changed = bundle_for(plan, [["0.008", "USD", RESOURCE.lower(), "eastus", 20260901]])
        with self.assertRaisesRegex(finops.EvidenceError, "Cost reference mismatch"):
            finops.report_model(actual, changed)

    def test_html_is_standalone_escaped_and_contains_same_exact_values(self):
        entries = [["0.008", "USD", RESOURCE.lower(), '<script>alert("x")</script>', 20260901]]
        model = finops.report_model(bundle_for(entries=entries))
        document = finops.html_report(model)
        self.assertIn("0.008", document)
        self.assertIn("&lt;script&gt;", document)
        self.assertNotIn("<script>", document)
        self.assertNotIn("<script src=", document)
        self.assertIn("default-src 'none'", document)
        self.assertIn("UNVERIFIED", document)
        self.assertIn("<h2>Exact billing-currency totals</h2>", document)
        self.assertIn("<td>0.008</td><td>$0.01</td>", document)

    def test_markdown_data_cannot_inject_external_images(self):
        plan = plan_for()
        manifest = plan["manifest"]
        manifest["scenario"]["selection"] = {"subscriptionNames": ["![image](https://example.test)"]}
        manifest["scenarioSha256"] = finops.digest(manifest["scenario"])
        plan = finops.make_plan(reseal(manifest))
        text = finops.markdown_report(finops.report_model(bundle_for(plan)))
        self.assertIn(r"\!\[image\]\(https://example.test\)", text)
        self.assertNotIn("![image](", text)

    def test_pdf_failure_is_not_a_success_or_html_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            browser = root / "browser.exe"
            browser.write_text("synthetic", encoding="utf-8")
            target = root / "report.pdf"
            with patch.object(finops.subprocess, "run", return_value=Mock(returncode=1)):
                with self.assertRaisesRegex(finops.EvidenceError, "PDF export failed"):
                    finops.export_pdf("<html>test</html>", target, browser)
            self.assertFalse(target.exists())

    def test_cli_writes_markdown_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            actual, report = root / "actual.json", root / "report.md"
            finops.write_json(actual, bundle_for())
            self.assertEqual(finops.main(["report", "--actual", str(actual), "--out", str(report)]), 0)
            original = report.read_text(encoding="utf-8")
            with patch("sys.stderr", new_callable=io.StringIO) as errors:
                result = finops.main(["report", "--actual", str(actual), "--out", str(report)])
                self.assertIn("already exists", errors.getvalue())
            self.assertEqual(result, 2)
            self.assertEqual(report.read_text(encoding="utf-8"), original)

    def test_cli_reconciliation_failure_is_nonzero_and_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            actual = bundle_for()
            reference = bundle_for(actual["plan"], [["0.008", "USD", RESOURCE.lower(), "eastus", 20260901]])
            for name, value in (("actual.json", actual), ("reference.json", reference)):
                finops.write_json(root / name, value)
            with patch("sys.stderr", new_callable=io.StringIO) as errors:
                result = finops.main(["reconcile", "--actual", str(root / "actual.json"),
                                      "--reference", str(root / "reference.json"), "--out", str(root / "result.json")])
                self.assertIn("monetary rows differ", errors.getvalue())
            self.assertEqual(result, 2)
            self.assertEqual(finops.read_json(root / "result.json")["status"], "mismatch")


class CustomizationTests(unittest.TestCase):
    def test_discoverable_metadata_and_relative_links(self):
        workspace = Path(__file__).resolve().parents[4]
        agent = workspace / ".github" / "agents" / "FinOpsAgent.agent.md"
        skills = workspace / ".github" / "skills"
        skill_paths = sorted(skills.rglob("SKILL.md"))
        self.assertEqual({path.parent.name for path in skill_paths}, {
            "azure-cost-management", "finops-invoker-access", "finops-scope-resolution",
            "finops-cost-evidence", "finops-reporting",
        })
        paths = [agent, *skill_paths]
        for path in paths:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                header = text.split("---\n", 2)[1]
                fields = dict(line.split(": ", 1) for line in header.splitlines() if ": " in line)
                description = json.loads(fields["description"])
                self.assertGreater(len(description), 30)
                self.assertLessEqual(len(description), 1024)
                if path.name == "SKILL.md":
                    self.assertEqual(fields["name"], path.parent.name)
                    if path.parent.name == "azure-cost-management":
                        self.assertEqual(fields["license"], "CC-BY-4.0")
                else:
                    self.assertEqual(fields["name"], "FinOpsAgent")
                    self.assertEqual(fields["agents"], "[]")
                    self.assertIn("vscode/askQuestions", fields["tools"])
                    self.assertIn("../skills/azure-cost-management/SKILL.md", text)
                for target in finops.re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                    if "://" not in target and not target.startswith("#"):
                        self.assertTrue((path.parent / target).exists(), f"Broken relative link: {target}")

    def test_scenario_example_uses_supported_schema(self):
        example = SCRIPTS.parent / "assets" / "scenario.example.json"
        finops.validate_scenario(finops.read_json(example))


if __name__ == "__main__":
    unittest.main()
