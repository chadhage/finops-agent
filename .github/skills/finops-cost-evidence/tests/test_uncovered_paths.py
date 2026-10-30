from __future__ import annotations

import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import run_tests
import test_failure_matrix as matrix
import test_finops as fixture
import test_portal_validation as portal_fixture


finops = fixture.finops
portal = portal_fixture.portal_validation


class NegativeUncoveredPaths(matrix.CliCase):
    phase = "negative"

    def test_jwt_payload_with_invalid_utf8_is_explicit(self):
        with patch.object(finops, "cli_json", side_effect=[matrix.profile(),
                                                         {"accessToken": "synthetic._w.signature"}]):
            self.assert_blocked("identity", {}, ["--tenant", fixture.TENANT, "--subscription", fixture.SUB])

    def test_raw_json_must_be_an_object_not_an_array(self):
        with self.assertRaisesRegex(finops.EvidenceError, "JSON object"):
            finops.parse_json("[]")

    def test_url_retry_date_header_is_not_a_sleep_forever_instruction(self):
        client = object.__new__(finops.AzureClient)
        client.subscriptions, client.tokens, client.opener = [fixture.SUB], {fixture.SUB: "synthetic"}, Mock()
        url = fixture.plan_for()["requests"][0]["url"]
        client.opener.open.side_effect = finops.urllib.error.HTTPError(
            url, 429, "synthetic", {"Retry-After": "Thu, 01 Jan 2099 00:00:00 GMT"}, None)
        with patch.object(finops.time, "sleep") as sleep, self.assertRaises(finops.EvidenceError):
            client.request("POST", url, fixture.SUB, {})
        sleep.assert_not_called()

    def test_import_reference_rejects_a_network_share(self):
        plan = fixture.plan_for()
        index = {"source": "manual-azure-cli", "tenantId": fixture.TENANT, "principalId": fixture.INVOKER,
                 "capturedAt": fixture.AS_OF, "captures": [{"requestId": plan["requests"][0]["id"], "pages": [
                     {"path": r"\\synthetic-server\share\page.json", "url": plan["requests"][0]["url"], "status": 200}]}]}
        with self.assertRaisesRegex(finops.EvidenceError, "Network-share"):
            finops.import_reference(plan, index, Path.cwd())

    def test_portal_command_sample_is_blocked_and_reports_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            config = fixture.SCRIPTS.parent / "assets" / "portal-validation.example.json"
            with patch("sys.stdout", new_callable=io.StringIO), patch.object(finops, "AzureClient") as azure:
                status = portal.main(["--config", str(config), "--mode", "live", "--out-dir", directory])
            self.assertEqual(status, 2)
            report = finops.read_json(next(Path(directory).rglob("report.json")))
            self.assertEqual(report["status"], "BLOCKED")
            azure.assert_not_called()

    def test_worker_blocks_external_processes_and_journals_the_error(self):
        def attempts_spawn():
            subprocess.Popen(["SYNTHETIC-NEVER-EXECUTED"])

        case = unittest.FunctionTestCase(attempts_spawn)
        with tempfile.TemporaryDirectory() as directory:
            journal = Path(directory) / "attempt.jsonl"
            with patch.object(run_tests, "discover", return_value={"negative": [case]}):
                run_tests.worker("negative", 1, 4701, run_tests.DEFAULT_CLOCK, journal)
            result = json.loads(journal.read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "failure")
            self.assertIn("Real network/process call", "\n".join(result["diagnostics"]))

    def test_runner_cannot_report_success_when_offline_and_portal_modes_are_combined(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("sys.stdout", new_callable=io.StringIO):
                status = run_tests.main(["--offline-only", "--portal-config", "not-read.json",
                                         "--out-dir", directory, "--repeat", "1"])
            self.assertEqual(status, 2)
            report = json.loads(next(Path(directory).rglob("report.json")).read_text(encoding="utf-8"))
            self.assertFalse(report["acceptanceValidated"])
            self.assertIn("cannot be combined", "\n".join(report["errors"]))


class PositiveUncoveredPaths(unittest.TestCase):
    phase = "positive"

    def test_azure_client_constructor_binds_every_subscription_separately(self):
        contexts = [({"subscriptionId": sid, "principalId": fixture.INVOKER}, "synthetic-token-" + str(number))
                    for number, sid in enumerate((fixture.SUB, fixture.OTHER_SUB))]
        with patch.object(finops, "azure_identity", side_effect=contexts) as identity:
            client = finops.AzureClient(fixture.TENANT, fixture.INVOKER, [fixture.SUB, fixture.OTHER_SUB])
        self.assertEqual(identity.call_count, 2)
        self.assertEqual(set(client.contexts), {fixture.SUB, fixture.OTHER_SUB})
        self.assertNotEqual(client.tokens[fixture.SUB], client.tokens[fixture.OTHER_SUB])

    def test_inventory_cli_preserves_approved_inputs_and_optional_owner_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request = fixture.scenario()
            owners = {"schemaVersion": 1, "source": "synthetic approved ownership"}
            finops.write_json(root / "scenario.json", request)
            finops.write_json(root / "owners.json", owners)
            with patch.object(finops, "AzureClient") as client, \
                    patch.object(finops, "collect_inventory", return_value=fixture.catalog()) as collect:
                status = finops.main(["inventory", "--scenario", str(root / "scenario.json"),
                                      "--owners", str(root / "owners.json"), "--out", str(root / "catalog.json")])
            self.assertEqual(status, 0)
            collect.assert_called_once_with(request, client.return_value, owners)

    def test_collect_inventory_follows_all_location_metadata_pages(self):
        client = fixture.AzureBoundaryTests().inventory_client()
        pages = list(client.request.side_effect)
        url = finops.ARM + f"/subscriptions/{fixture.SUB}/locations?api-version=2022-12-01"
        following = url + "&$skiptoken=second"
        pages[2] = fixture.page(url, json.dumps({"value": [{"name": "eastus", "displayName": "East US"}],
                                               "nextLink": following}))
        pages.append(fixture.page(following, json.dumps({"value": [{"name": "westus", "displayName": "West US"}]})))
        client.request.side_effect = pages
        result = finops.collect_inventory(fixture.scenario(), client)
        self.assertEqual([r["name"] for r in result["locations"]], ["eastus", "westus"])
        self.assertEqual(client.request.call_args.args[1], following)

    def test_global_location_is_retained_when_absent_from_region_alias_api(self):
        client = fixture.AzureBoundaryTests().inventory_client()
        pages = list(client.request.side_effect)
        resources = json.loads(pages[0]["raw"])
        resources["data"][0]["location"] = "global"
        pages[0] = fixture.page(pages[0]["url"], json.dumps(resources))
        client.request.side_effect = pages
        result = finops.collect_inventory(fixture.scenario(), client)
        self.assertIn({"name": "global", "displayName": "global"}, result["locations"])

    def test_pdf_success_path_verifies_file_and_keeps_browser_sandbox_enabled(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            browser, output = root / "synthetic-browser.exe", root / "report.pdf"
            browser.write_text("mocked installed executable", encoding="utf-8")

            def print_pdf(arguments, **_kwargs):
                target = Path(next(arg.split("=", 1)[1] for arg in arguments if arg.startswith("--print-to-pdf=")))
                target.write_bytes(b"%PDF-1.7\n" + b"SYNTHETIC-MOCK-PDF " * 20)
                return Mock(returncode=0)

            with patch.object(finops.subprocess, "run", side_effect=print_pdf) as process:
                finops.export_pdf("<html>synthetic</html>", output, browser)
            self.assertTrue(output.read_bytes().startswith(b"%PDF-"))
            self.assertNotIn("--no-sandbox", process.call_args.args[0])

    def test_portal_main_returns_mismatch_exit_without_claiming_live_success(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(portal, "run_validation", return_value={"status": "MISMATCH"}), \
                    patch("sys.stdout", new_callable=io.StringIO):
                status = portal.main(["--config", "not-read.json", "--mode", "evidence", "--out-dir", directory])
            self.assertEqual(status, 1)

    def test_worker_repetitions_save_coverage_and_real_per_case_output(self):
        case = unittest.FunctionTestCase(lambda: finops.guid(fixture.TENANT))
        with tempfile.TemporaryDirectory() as directory:
            journal = Path(directory) / "attempt.jsonl"
            with patch.object(run_tests, "discover", return_value={"positive": [case]}):
                status = run_tests.worker("positive", 1, 4701, run_tests.DEFAULT_CLOCK, journal, coverage=True)
            self.assertEqual(status, 0)
            self.assertEqual(json.loads(journal.read_text(encoding="utf-8"))["status"], "pass")
            self.assertTrue(journal.with_suffix(".coverage.json").is_file())
