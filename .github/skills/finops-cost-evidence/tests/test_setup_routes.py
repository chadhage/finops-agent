from __future__ import annotations

import io
import json
import unittest
from email.message import Message
from unittest.mock import patch

import test_verification_setup as fixture


setup = fixture.setup


class RouteCase(fixture.SetupCase):
    def dispatch(self, path, *, payload=None, headers=None, raw=None):
        handler = object.__new__(setup.SetupHandler)
        server = object.__new__(setup.SetupServer)
        server.app, server.server_port = self.app, 8765
        handler.server, handler.path = server, path
        handler.headers = Message()
        body = raw if raw is not None else json.dumps(payload).encode() if payload is not None else b""
        request_headers = {"Host": "127.0.0.1:8765", "Origin": "http://127.0.0.1:8765",
                           "X-Setup-Token": self.app.token, "Content-Type": "application/json",
                           "Content-Length": str(len(body)), **(headers or {})}
        for key, value in request_headers.items():
            if value is not None:
                handler.headers[key] = value
        handler.rfile, handler.wfile = io.BytesIO(body), io.BytesIO()
        status, response_headers = [], {}
        handler.send_response = status.append
        handler.send_header = lambda key, value: response_headers.__setitem__(key, value)
        handler.end_headers = lambda: None
        with patch.object(setup.LOGGER, "warning"), patch.object(setup.LOGGER, "exception"):
            handler.dispatch(payload is not None or raw is not None)
        return status[0], response_headers, handler.wfile.getvalue()


class NegativeSetupRouteTests(RouteCase):
    phase = "negative"

    def test_missing_host_is_rejected(self):
        self.assertEqual(self.dispatch("/api/bootstrap", headers={"Host": None})[0], 403)

    def test_cross_site_bootstrap_is_rejected(self):
        self.assertEqual(self.dispatch("/api/bootstrap", headers={"Sec-Fetch-Site": "cross-site"})[0], 403)

    def test_mutation_without_origin_is_rejected(self):
        self.assertEqual(self.dispatch("/api/prepare", payload={}, headers={"Origin": None})[0], 403)

    def test_mutation_with_wrong_token_is_rejected(self):
        self.assertEqual(self.dispatch("/api/prepare", payload={},
                                       headers={"X-Setup-Token": "synthetic-wrong"})[0], 403)

    def test_mutation_with_wrong_content_type_is_rejected(self):
        self.assertEqual(self.dispatch("/api/prepare", payload={},
                                       headers={"Content-Type": "text/plain"})[0], 415)

    def test_mutation_with_transfer_encoding_is_rejected(self):
        self.assertEqual(self.dispatch("/api/prepare", payload={},
                                       headers={"Transfer-Encoding": "chunked"})[0], 400)

    def test_oversized_body_is_rejected_before_parsing(self):
        self.assertEqual(self.dispatch("/api/prepare", payload={},
                                       headers={"Content-Length": "2000001"})[0], 413)

    def test_invalid_length_is_explicit(self):
        self.assertEqual(self.dispatch("/api/prepare", payload={},
                                       headers={"Content-Length": "not-an-int"})[0], 400)

    def test_json_duplicate_keys_are_rejected(self):
        self.assertEqual(self.dispatch("/api/prepare", raw=b'{"mode":"offline","mode":"live"}')[0], 400)

    def test_invalid_utf8_is_rejected(self):
        self.assertEqual(self.dispatch("/api/prepare", raw=b"\xff")[0], 400)

    def test_live_request_is_rejected_without_spawn(self):
        with patch.object(setup.subprocess, "Popen") as process:
            status, _, _ = self.dispatch("/api/prepare", payload={"mode": "live", "runner": self.payload["runner"]})
        self.assertEqual(status, 400)
        process.assert_not_called()

    def test_unknown_routes_are_404(self):
        self.assertEqual(self.dispatch("/not-a-page")[0], 404)
        self.assertEqual(self.dispatch("/api/delete", payload={})[0], 404)

    def test_unknown_plan_lookup_fields_are_not_ignored(self):
        self.assertEqual(self.dispatch("/api/plan", payload={"planPath": "none", "command": "ignored"})[0], 400)

    def test_unknown_setup_is_404(self):
        self.assertEqual(self.dispatch("/api/runs/" + "a" * 32)[0], 404)

    def test_artifact_traversal_is_rejected(self):
        record = self.offline()
        status, _, _ = self.dispatch(f"/api/runs/{record['id']}/artifacts/%2e%2e/actual.json")
        self.assertIn(status, (400, 403))

    def test_program_files_cannot_be_downloaded(self):
        record = self.offline()
        (self.app.run_directory(record["id"]) / "synthetic.exe").write_bytes(b"synthetic")
        status, _, _ = self.dispatch(f"/api/runs/{record['id']}/artifacts/synthetic.exe")
        self.assertEqual(status, 403)

    def test_missing_static_asset_is_explicit_io_error(self):
        with patch.object(setup, "STATIC", self.root / "missing-static"):
            self.assertEqual(self.dispatch("/app.js")[0], 500)

    def test_multiple_campaign_reports_cannot_be_claimed_as_one(self):
        record = self.offline()
        self.write_report(record["id"])
        extra = self.app.run_directory(record["id"]) / "reports" / "second"
        extra.mkdir()
        (extra / "report.json").write_text('{"verdict":"PASS"}', encoding="utf-8")
        with self.assertRaisesRegex(setup.SetupError, "more than one"):
            self.app.status(record["id"])

    def test_malformed_campaign_report_is_not_a_passing_outcome(self):
        record = self.offline()
        self.write_report(record["id"])
        target = next((self.app.run_directory(record["id"]) / "reports").glob("*\\report.json"))
        target.write_text("[]", encoding="utf-8")
        with self.assertRaisesRegex(setup.SetupError, "invalid shape"):
            self.app.status(record["id"])


class PositiveSetupRouteTests(RouteCase):
    phase = "positive"

    def test_static_files_have_required_content_and_no_cache_headers(self):
        for path, mime in (("/", "text/html"), ("/app.js", "text/javascript"), ("/style.css", "text/css")):
            with self.subTest(path=path):
                status, headers, body = self.dispatch(path)
                self.assertEqual(status, 200)
                self.assertTrue(headers["Content-Type"].startswith(mime))
                self.assertEqual(headers["Cache-Control"], "no-store")
                self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
                self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
                self.assertTrue(body)

    def test_bootstrap_exposes_only_local_roots_and_unapproved_defaults(self):
        status, _, raw = self.dispatch("/api/bootstrap")
        body = json.loads(raw)
        self.assertEqual(status, 200)
        self.assertEqual(body["token"], self.app.token)
        self.assertNotIn("live", body["defaults"])

    def test_plan_inspection_binds_exact_identity_scope_and_requests(self):
        status, _, raw = self.dispatch("/api/plan", payload={"planPath": str(self.root / "plan.json")})
        plan = json.loads(raw)
        self.assertEqual(status, 200)
        self.assertEqual(plan["sha256"], self.plan["sha256"])
        self.assertEqual(plan["principalId"], self.plan["manifest"]["principalId"])
        self.assertEqual(len(plan["requests"]), 2)

    def test_prepare_history_status_and_download_round_trip(self):
        status, _, raw = self.dispatch("/api/prepare", payload={"mode": "offline", "runner": self.payload["runner"]})
        record = json.loads(raw)
        self.assertEqual(status, 201)
        identifier = record["id"]
        status, _, raw = self.dispatch("/api/runs")
        self.assertEqual(json.loads(raw)[0]["id"], identifier)
        self.assertEqual(status, 200)
        status, _, raw = self.dispatch("/api/runs/" + identifier)
        self.assertEqual(json.loads(raw)["state"], "prepared")
        self.assertEqual(status, 200)
        status, headers, raw = self.dispatch(f"/api/runs/{identifier}/artifacts/setup.json")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(raw)["id"], identifier)
        self.assertIn("attachment;", headers["Content-Disposition"])

    def test_start_route_invokes_only_existing_runner(self):
        record = self.offline()
        with patch.object(setup.SetupApp, "start", return_value={"id": record["id"], "state": "running"}) as start:
            status, _, raw = self.dispatch(f"/api/runs/{record['id']}/start", payload={})
        self.assertEqual(status, 202)
        self.assertEqual(json.loads(raw)["state"], "running")
        start.assert_called_once_with(record["id"])
