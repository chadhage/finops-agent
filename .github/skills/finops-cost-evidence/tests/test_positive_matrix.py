from __future__ import annotations

import random
import tempfile
import unittest
from decimal import Decimal, localcontext
from html.parser import HTMLParser
from pathlib import Path

import test_finops as fixture


finops = fixture.finops


class PositiveScopeTests(unittest.TestCase):
    phase = "positive"

    def test_management_group_never_adds_unapproved_descendants(self):
        request, source = fixture.scenario(), fixture.catalog()
        request["selection"] = {"managementGroupIds": [fixture.MG]}
        manifest = finops.resolve_scope(request, source)
        self.assertEqual(manifest["subscriptionIds"], [fixture.SUB])
        self.assertEqual(manifest["approvedSubscriptionIds"], [fixture.SUB])

    def test_multiple_users_union_their_distinct_resources(self):
        request, source = fixture.scenario(), fixture.catalog()
        request["selection"] = {"owners": {"kind": "business",
                                           "users": ["owner@example.test", "data@example.test"]}}
        source["ownerBindings"].append({**source["ownerBindings"][1], "userId": fixture.OTHER_OWNER,
                                         "scopeId": fixture.SECOND})
        manifest = finops.resolve_scope(request, source)
        self.assertEqual(manifest["resourceIds"], sorted([fixture.RESOURCE.lower(), fixture.SECOND.lower()]))

    def test_two_tag_keys_intersect_while_values_union(self):
        request, source = fixture.scenario(), fixture.catalog()
        source["resources"][0]["tags"]["Environment"] = "prod"
        source["resources"][1]["tags"]["Environment"] = "dev"
        request["selection"] = {"tags": [
            {"key": "Application", "values": ["checkout", "data"]},
            {"key": "Environment", "values": ["prod"]}]}
        self.assertEqual(finops.resolve_scope(request, source)["resourceIds"], [fixture.RESOURCE.lower()])

    def test_resource_order_does_not_change_selected_ids(self):
        request, source = fixture.scenario(), fixture.catalog()
        request["selection"] = {"regions": ["East US", "West US"]}
        expected = finops.resolve_scope(request, source)["resourceIds"]
        random.Random(510).shuffle(source["resources"])
        self.assertEqual(finops.resolve_scope(request, source)["resourceIds"], expected)

    def test_multiple_subscriptions_remain_disjoint_in_the_plan(self):
        request, source = fixture.scenario(), fixture.catalog()
        request["approvedSubscriptionIds"].append(fixture.OTHER_SUB)
        source["subscriptions"].append({"id": fixture.OTHER_SUB, "name": "Second subscription",
                                         "managementGroups": [{"id": fixture.MG, "name": "Engineering"}]})
        source["resources"].append({**source["resources"][0],
                                     "id": fixture.RESOURCE.replace(fixture.SUB, fixture.OTHER_SUB),
                                     "subscriptionId": fixture.OTHER_SUB})
        plan = finops.make_plan(finops.resolve_scope(request, source))
        self.assertEqual(len(plan["requests"]), 4)
        self.assertEqual({finops.subscription_of(r["scope"]) for r in plan["requests"]},
                         {fixture.SUB, fixture.OTHER_SUB})

    def test_nested_group_owner_binding_preserves_source_provenance(self):
        request, source = fixture.scenario(), fixture.catalog()
        request["selection"] = {"owners": {"kind": "rbac", "users": [fixture.OWNER]}}
        source["ownerBindings"][0]["scopeId"] = fixture.MG
        source["ownerBindings"][0]["source"] = "Synthetic active assignment / group A > group B > user; denies checked"
        manifest = finops.resolve_scope(request, source)
        self.assertEqual(len(manifest["resourceIds"]), 2)
        self.assertEqual(manifest["ownerEvidence"][0]["source"], source["ownerBindings"][0]["source"])


def chunk_case(size: int):
    def test(self: unittest.TestCase) -> None:
        request, source = fixture.scenario(), fixture.catalog()
        request["selection"] = {"regions": ["eastus"]}
        source["resources"] = [{"id": fixture.RG + f"/providers/Microsoft.Compute/virtualMachines/vm{n}",
                                "location": "eastus", "tags": {}} for n in range(size)]
        manifest = finops.resolve_scope(request, source)
        plan = finops.make_plan(manifest)
        chunks = [r["body"]["dataset"]["filter"]["dimensions"]["values"]
                  for r in plan["requests"] if r["kind"] == "detail"]
        self.assertEqual(sum(map(len, chunks)), size)
        self.assertEqual(len({r for chunk in chunks for r in chunk}), size)
        self.assertEqual(len(chunks), (size + 99) // 100)
        self.assertTrue(all(1 <= len(chunk) <= 100 for chunk in chunks))
    return test


class PositiveChunkBoundaryTests(unittest.TestCase):
    phase = "positive"


for count in (1, 99, 100, 101, 199, 200, 201):
    setattr(PositiveChunkBoundaryTests, f"test_exactly_{count}_resources", chunk_case(count))


class PositiveMoneyTests(unittest.TestCase):
    phase = "positive"

    def test_zero_charges_are_records_not_missing_data(self):
        entries = [["0.00000000", "USD", fixture.RESOURCE.lower(), "eastus", 20260901]]
        result = finops.validate_bundle(fixture.bundle_for(entries=entries))
        self.assertEqual(result["totals"], {"USD": Decimal("0.00000000")})
        self.assertEqual(result["emptyRequests"], [])

    def test_credits_cancel_without_disappearing_from_the_ledger(self):
        entries = [["10.000000001", "USD", fixture.RESOURCE.lower(), "eastus", 20260901],
                   ["-10.000000001", "USD", fixture.RESOURCE.lower(), "eastus", 20260902]]
        result = finops.validate_bundle(fixture.bundle_for(entries=entries))
        self.assertEqual(result["totals"]["USD"], Decimal(0))
        self.assertEqual(len(result["ledger"]), 2)

    def test_exact_sum_is_independent_of_global_decimal_precision(self):
        with localcontext() as context:
            context.prec = 3
            result = finops.exact_sum([Decimal("123456789012345678901234567890.000000001"),
                                      Decimal("-123456789012345678901234567890")])
        self.assertEqual(result, Decimal("0.000000001"))

    def test_cost_rows_and_reference_may_be_in_different_order(self):
        actual = fixture.bundle_for()
        reference = fixture.bundle_for(actual["plan"], list(reversed(fixture.records())))
        self.assertEqual(finops.reconcile(actual, reference)["status"], "exact-match")

    def test_aggregation_is_permutation_invariant(self):
        amounts = [Decimal("1000000000000000000000000000.1"), Decimal("-1000000000000000000000000000"),
                   Decimal("0.000000001"), Decimal("-0.000000002")]
        expected = Decimal("0.099999999")
        generator = random.Random(620)
        for _ in range(25):
            generator.shuffle(amounts)
            self.assertEqual(finops.exact_sum(amounts), expected)


class TableReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_cell = False
        self.cells: list[str] = []

    def handle_starttag(self, tag: str, _attrs: list[tuple[str, str | None]]) -> None:
        self.in_cell = tag == "td"

    def handle_endtag(self, tag: str) -> None:
        if tag == "td":
            self.in_cell = False

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cells.append(data)


class PositiveWorkflowTests(unittest.TestCase):
    phase = "positive"

    def test_complete_cli_flow_preserves_scope_amounts_and_report_lineage(self):
        with tempfile.TemporaryDirectory(prefix="finops-positive-flow-") as directory:
            root = Path(directory)
            scenario = fixture.scenario()
            scenario["selection"] = {"regions": ["East US"]}
            resource_reference = {
                "scenarioSha256": finops.digest(scenario), "capturedAt": fixture.AS_OF,
                "source": "Synthetic independent inventory", "resourceIds": [fixture.RESOURCE]}
            for name, value in (("scenario.json", scenario), ("catalog.json", fixture.catalog()),
                                ("resource-reference.json", resource_reference)):
                finops.write_json(root / name, value)

            def invoke(*args: str) -> None:
                self.assertEqual(finops.main(list(args)), 0)

            invoke("resolve", "--scenario", str(root / "scenario.json"), "--catalog", str(root / "catalog.json"),
                   "--resource-reference", str(root / "resource-reference.json"), "--out", str(root / "manifest.json"))
            invoke("plan", "--manifest", str(root / "manifest.json"), "--out", str(root / "plan.json"))
            plan = finops.read_json(root / "plan.json")
            entries = [["0.004", "USD", fixture.RESOURCE.lower(), "eastus", 20260901],
                       ["0.004", "USD", fixture.RESOURCE.lower(), "eastus", 20260902],
                       ["-2.125", "EUR", fixture.RESOURCE.lower(), "eastus", 20260903]]
            actual = fixture.bundle_for(plan, entries)
            finops.write_json(root / "actual.json", actual)
            index = {"source": "manual-azure-cli", "tenantId": fixture.TENANT, "principalId": fixture.INVOKER,
                     "capturedAt": fixture.AS_OF, "captures": []}
            for number, capture in enumerate(actual["captures"]):
                filename = f"manual-{number}.json"
                raw_page = capture["pages"][0]
                finops.write_text(root / filename, raw_page["raw"])
                index["captures"].append({"requestId": capture["requestId"], "pages": [
                    {"path": filename, "url": raw_page["url"], "status": 200}]})
            finops.write_json(root / "index.json", index)
            invoke("import-reference", "--plan", str(root / "plan.json"), "--index", str(root / "index.json"),
                   "--out", str(root / "reference.json"))
            invoke("reconcile", "--actual", str(root / "actual.json"), "--reference", str(root / "reference.json"),
                   "--out", str(root / "comparison.json"))
            for format_, filename in (("markdown", "report.md"), ("html", "report.html")):
                invoke("report", "--actual", str(root / "actual.json"), "--reference", str(root / "reference.json"),
                       "--format", format_, "--out", str(root / filename))
            markdown = (root / "report.md").read_text(encoding="utf-8")
            document = (root / "report.html").read_text(encoding="utf-8")
            for text in (markdown, document):
                self.assertIn("VALIDATED AGAINST CAPTURED REFERENCES", text)
                self.assertIn(actual["sha256"], text)
                self.assertIn(plan["sha256"], text)
            self.assertIn("| USD | 0.008 | $0.01 |", markdown)
            self.assertIn("| EUR | -2.125 | Not assumed |", markdown)
            reader = TableReader()
            reader.feed(document)
            self.assertIn("0.008", reader.cells)
            self.assertIn("-2.125", reader.cells)
            self.assertIn("$0.01", reader.cells)
            self.assertEqual(finops.read_json(root / "comparison.json")["differences"], [])

    def test_billing_history_can_include_a_deleted_current_inventory_resource(self):
        source = fixture.catalog()
        source["resources"] = []
        manifest = finops.resolve_scope(fixture.scenario(), source)
        capture = fixture.bundle_for(finops.make_plan(manifest))
        model = finops.report_model(capture)
        self.assertEqual(model["manifest"]["resourceIds"], [])
        self.assertEqual(model["evidence"]["totals"]["USD"], Decimal("0.008"))
        self.assertIn("historical/non-resource billing can still exist", finops.markdown_report(model))

    def test_markdown_and_html_use_the_same_unrounded_credit(self):
        model = finops.report_model(fixture.bundle_for(entries=[
            ["-123.4567890123456789", "USD", fixture.RESOURCE.lower(), "eastus", 20260901]]))
        self.assertIn("-123.4567890123456789", finops.markdown_report(model))
        self.assertIn("-123.4567890123456789", finops.html_report(model))
