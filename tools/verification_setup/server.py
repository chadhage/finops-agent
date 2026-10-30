"""Loopback-only setup and execution UI for the existing FinOps verification runner."""

from __future__ import annotations

import argparse
import hmac
import importlib
import json
import logging
import os
import re
import secrets
import subprocess
import sys
import tempfile
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit


WORKSPACE = Path(__file__).resolve().parents[2]
PACK = WORKSPACE / ".github" / "skills" / "finops-cost-evidence"
RUNNER = PACK / "tests" / "run_tests.py"
STATIC = Path(__file__).resolve().parent / "static"
sys.path.insert(0, str(PACK / "scripts"))
finops = importlib.import_module("finops")
portal_validation = importlib.import_module("portal_validation")


Json = dict[str, Any]
DEFAULTS = {"mode": "evidence", "repeat": 5, "seed": 1729,
            "clock": "2026-10-30T00:00:00Z", "sweepTimeout": 120,
            "maxEvidenceAgeSeconds": 3600}
ATTESTATIONS = {"exportedFromAzurePortal", "sameViewScopeAndFilters",
                "noSecretsIncluded", "actualCaptureIsAuthentic"}
LOGGER = logging.getLogger("verification_setup")


class SetupError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def require(condition: bool, message: str, status: int = 400) -> None:
    if not condition:
        raise SetupError(message, status)


def object_fields(value: Any, allowed: set[str], label: str) -> Json:
    require(isinstance(value, dict), f"{label} must be a JSON object.")
    require(not set(value) - allowed, f"Unknown {label} fields: {sorted(set(value) - allowed)}.")
    return value


def positive(value: Any, label: str) -> int:
    require(type(value) is int and value > 0, f"{label} must be a positive integer.")
    return value


def runner_options(value: Any) -> Json:
    data = object_fields(value, {"repeat", "seed", "clock", "sweepTimeout"}, "runner options")
    positive(data.get("repeat"), "Repetitions")
    positive(data.get("sweepTimeout"), "Sweep timeout")
    require(type(data.get("seed")) is int, "Seed must be an integer.")
    finops.timestamp(data.get("clock"))
    return data


def safe_path(base: Path, value: Any, roots: list[Path], *, file: bool = True) -> Path:
    require(isinstance(value, str) and bool(value.strip()), "Enter a local evidence file path.")
    require(not value.startswith(("\\\\", "//")) and not any(c in value for c in "<>\x00\r\n"),
            "UNC paths, placeholders, and control characters are not allowed.")
    path = Path(value)
    require(".." not in path.parts, "Parent-directory traversal is not allowed.")
    require(not any(":" in part for part in path.parts[1:]) and
            (not path.parts or ":" not in path.parts[0] or bool(path.drive)),
            "Alternate data-stream paths are not allowed.")
    resolved = (base / path).resolve()
    require(any(resolved.is_relative_to(root) for root in roots),
            "The path is outside the approved evidence roots.")
    require(not file or resolved.is_file(), f"Local evidence file not found: {resolved}.")
    return resolved


def write_record(directory: Path, value: Json) -> None:
    temporary = directory / "setup.json.tmp"
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n",
                         encoding="utf-8")
    temporary.replace(directory / "setup.json")


class SetupApp:
    def __init__(self, workspace: Path = WORKSPACE, evidence_roots: list[Path] | None = None):
        self.workspace = workspace.resolve()
        self.output = self.workspace / ".finops-runs" / "verification-setup"
        self.output.mkdir(parents=True, exist_ok=True)
        self.roots = [self.workspace / ".finops-runs"]
        for root in evidence_roots or []:
            require(not str(root).startswith(("\\\\", "//")), "Evidence roots must be local.")
            resolved = root.resolve()
            require(resolved.is_dir(), f"Evidence root is not a directory: {resolved}.")
            self.roots.append(resolved)
        self.roots = list(dict.fromkeys(root.resolve() for root in self.roots))
        self.token = secrets.token_urlsafe(32)
        self.lock = threading.RLock()
        self.active_id: str | None = None
        self.monitor: threading.Thread | None = None

    def bootstrap(self) -> Json:
        return {"token": self.token, "workspace": str(self.workspace), "outputRoot": str(self.output),
                "evidenceRoots": [str(root) for root in self.roots], "defaults": DEFAULTS}

    def evidence_file(self, value: Any, base: Path | None = None) -> Path:
        return safe_path(base or self.workspace, value, self.roots)

    def plan(self, value: Any) -> tuple[Path, Json]:
        path = self.evidence_file(value)
        plan = finops.read_json(path)
        portal_validation.no_secrets(plan)
        finops.verify_plan(plan)
        return path, plan

    @staticmethod
    def plan_summary(plan: Json) -> Json:
        manifest = plan["manifest"]
        return {"sha256": plan["sha256"], "tenantId": manifest["tenantId"],
                "principalId": manifest["principalId"], "subscriptionIds": manifest["subscriptionIds"],
                "period": manifest["period"], "costBasis": manifest["costBasis"],
                "scopeMode": manifest["scopeMode"], "resourceCount": len(manifest["resourceIds"]),
                "scopeReference": manifest["scopeReference"]["status"],
                "requests": [{"id": r["id"], "kind": r["kind"], "url": r["url"],
                              "expectedBody": json.dumps(r["body"], indent=2)} for r in plan["requests"]]}

    def copy_input(self, value: Any, destination: Path, base: Path | None = None) -> Path:
        source = self.evidence_file(value, base)
        raw = source.read_bytes()
        text = raw.decode("utf-8-sig")
        if text.strip():
            finops.no_secrets(finops.parse_json(text))
        with destination.open("xb") as stream:
            stream.write(raw)
        return source

    def reference_index(self, payload: Json, plan: Json, directory: Path) -> Json:
        flags = object_fields(payload.get("attestations"), ATTESTATIONS, "attestations")
        require(set(flags) == ATTESTATIONS and all(flag is True for flag in flags.values()),
                "Explicitly confirm all four evidence attestations; none are pre-approved.")
        confirmed = payload.get("confirmedAt")
        finops.timestamp(confirmed)
        principal = plan["manifest"]["principalId"]
        attestation: Json = {key: True for key in ATTESTATIONS - {"actualCaptureIsAuthentic"}}
        attestation.update({"confirmedByPrincipalId": principal, "confirmedAt": confirmed})
        mode = payload.get("referenceMode")
        require(mode in ("create", "existing"), "Choose a new or existing Portal reference index.")
        base = self.workspace
        if mode == "existing":
            source = self.evidence_file(payload.get("portalIndexPath"))
            index = finops.read_json(source)
            portal_validation.real_document(index, "Portal reference index")
            base = source.parent
        else:
            reference = object_fields(payload.get("reference"),
                                      {"capturedAt", "portalViewUrl", "displayedTotals", "captures"},
                                      "Portal reference")
            index = {"schemaVersion": 1, "isExample": False, "source": "portal-query-export",
                     "tenantId": plan["manifest"]["tenantId"], "principalId": principal, **reference}
        portal_validation.no_secrets(index)
        index["attestation"] = attestation
        require(isinstance(index.get("captures"), list) and bool(index["captures"]),
                "Load a plan and supply every Portal detail/control request and response page.")
        captures = []
        requests = {request["id"]: request for request in plan["requests"]}
        for number, item in enumerate(index["captures"]):
            fields = {"requestId", "pages", "requestBodyPath"} if mode == "create" else {
                "requestId", "pages", "requestBody"}
            item = object_fields(item, fields, "Portal request")
            request_id = item.get("requestId")
            require(isinstance(request_id, str) and request_id in requests, "Unexpected Portal request ID.")
            if mode == "create":
                body_path = directory / f"portal-request-{number}.json"
                self.copy_input(item.get("requestBodyPath"), body_path, base)
                body = finops.read_json(body_path)
            else:
                body = item.get("requestBody")
            require(body == requests[request_id]["body"],
                    f"Portal request {request_id} differs from the approved plan.")
            portal_validation.no_secrets(body)
            pages = item.get("pages")
            if not isinstance(pages, list) or not pages:
                raise SetupError(f"Response pages are missing for {request_id}.")
            copied_pages = []
            for page_number, entry in enumerate(pages):
                entry = object_fields(entry, {"path", "url", "status"}, "Portal page")
                require(type(entry.get("status")) is int and entry["status"] in (200, 204),
                        "Portal page status must be 200 or 204.")
                require(isinstance(entry.get("url"), str), "Enter the exact Portal response URL.")
                name = f"portal-page-{number}-{page_number}.json"
                self.copy_input(entry.get("path"), directory / name, base)
                copied_pages.append({**entry, "path": name})
            captures.append({"requestId": request_id, "requestBody": body, "pages": copied_pages})
        index["captures"] = captures
        return index

    def prepare(self, payload: Json) -> Json:
        payload = object_fields(payload, {"mode", "runner", "planPath", "actualPath", "approvedPlanSha256",
                                         "maxEvidenceAgeSeconds", "referenceMode", "portalIndexPath",
                                         "reference", "attestations", "confirmedAt"}, "setup")
        mode = payload.get("mode")
        require(mode in ("offline", "evidence"), "Only offline and captured-evidence modes are available.")
        options = runner_options(payload.get("runner"))
        identifier = uuid.uuid4().hex
        record: Json = {"id": identifier, "mode": mode, "runner": options, "state": "prepared",
                        "createdAt": finops.utc_now(), "exitCode": None, "error": None,
                        "source": finops.source_fingerprint()}
        with tempfile.TemporaryDirectory(prefix=".preparing-", dir=self.output) as temporary:
            directory = Path(temporary)
            if mode == "evidence":
                plan_path, plan = self.plan(payload.get("planPath"))
                require(payload.get("approvedPlanSha256") == plan["sha256"],
                        "Paste the exact approved plan hash after reviewing the plan.")
                age = positive(payload.get("maxEvidenceAgeSeconds"), "Evidence-age limit")
                require(plan["manifest"]["scopeReference"]["status"] == "exact-match",
                        "The plan needs an independent exact resource-set reference before Portal verification.")
                self.copy_input(str(plan_path), directory / "approved-plan.json")
                self.copy_input(payload.get("actualPath"), directory / "actual.json")
                actual = finops.read_json(directory / "actual.json")
                portal_validation.no_secrets(actual)
                require(actual.get("source") == "invoker-azure-cli-arm",
                        "The actual capture must be genuine saved invoker-bound Azure query evidence.")
                finops.validate_bundle(actual)
                require(actual["plan"]["sha256"] == plan["sha256"],
                        "The saved actual capture uses a different approved plan.")
                for capture in actual["captures"]:
                    for page in capture["pages"]:
                        if page["raw"].strip():
                            portal_validation.no_secrets(finops.parse_json(page["raw"]))
                index = self.reference_index(payload, plan, directory)
                finops.write_json(directory / "portal-reference.json", index)
                config = {"schemaVersion": 1, "isExample": False, "planPath": "approved-plan.json",
                          "portalIndexPath": "portal-reference.json", "actualPath": "actual.json",
                          "approvedPlanSha256": plan["sha256"], "maxEvidenceAgeSeconds": age}
                finops.write_json(directory / "portal-validation.json", config)
                portal_validation.load_inputs(directory / "portal-validation.json", "evidence", None)
                record["plan"] = self.plan_summary(plan)
            write_record(directory, record)
            directory.rename(self.output / identifier)
        return self.status(identifier)

    def run_directory(self, identifier: str) -> Path:
        require(re.fullmatch(r"[a-f0-9]{32}", identifier) is not None, "Unknown setup ID.", 404)
        directory = self.output / identifier
        require((directory / "setup.json").is_file(), "Setup not found.", 404)
        require(directory.resolve().is_relative_to(self.output.resolve()), "Invalid setup directory.", 403)
        return directory

    def read_record(self, identifier: str) -> Json:
        return finops.read_json(self.run_directory(identifier) / "setup.json")

    @staticmethod
    def saved_report(directory: Path) -> Json | None:
        root = directory / "reports"
        paths = [path for folder in root.iterdir() for path in folder.glob("report.json")] if root.is_dir() else []
        require(len(paths) <= 1, "Runner produced more than one campaign report.", 500)
        if not paths:
            return None
        try:
            report = json.loads(paths[0].read_text(encoding="utf-8"), object_pairs_hook=finops._object)
            finops.object_fields(report, {"verdict"}, "Campaign report")
            finops.no_secrets(report)
        except (finops.EvidenceError, ValueError) as exc:
            raise SetupError("The saved campaign report has an invalid shape.", 500) from exc
        require(isinstance(report, dict) and isinstance(report.get("verdict"), str),
                "The saved campaign report has an invalid shape.", 500)
        return report

    def command(self, record: Json) -> list[str]:
        directory = self.run_directory(record["id"])
        options = runner_options(record["runner"])
        command = [sys.executable, "-B", str(RUNNER), "--repeat", str(options["repeat"]),
                   "--seed", str(options["seed"]), "--clock", options["clock"],
                   "--sweep-timeout", str(options["sweepTimeout"]), "--out-dir", str(directory / "reports")]
        require(record["mode"] in ("offline", "evidence"), "Unsupported execution mode.")
        if record["mode"] == "offline":
            command.append("--offline-only")
        else:
            command += ["--portal-config", str(directory / "portal-validation.json"), "--portal-mode", "evidence"]
        return command

    def start(self, identifier: str) -> Json:
        with self.lock:
            require(self.active_id is None, "Another test campaign is running. Wait for it to finish.", 409)
            record = self.read_record(identifier)
            require(record["state"] == "prepared", "This setup was already invoked; generate a new setup to rerun.", 409)
            require(isinstance(record.get("source"), dict) and
                    record["source"].get("sha256") == finops.source_fingerprint()["sha256"],
                    "Source changed since preparation; generate and review a new setup.", 409)
            directory = self.run_directory(identifier)
            command = self.command(record)
            record.update({"state": "running", "startedAt": finops.utc_now(), "command": command})
            self.active_id = identifier
            try:
                write_record(directory, record)
                with (directory / "runner.log").open("xb") as log:
                    process = subprocess.Popen(command, cwd=self.workspace, stdout=log, stderr=subprocess.STDOUT,
                                               env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, shell=False)
            except OSError as exc:
                record.update({"state": "error", "error": f"Could not start test runner: {exc}"})
                self.active_id = None
                write_record(directory, record)
                LOGGER.exception("Test runner could not start")
                raise SetupError(record["error"], 500) from exc
            record["pid"] = process.pid
            write_record(directory, record)
            self.monitor = threading.Thread(target=self.finish, args=(identifier, process), daemon=True)
            self.monitor.start()
        return self.status(identifier)

    def finish(self, identifier: str, process: subprocess.Popen) -> None:
        code = process.wait()
        with self.lock:
            directory = self.run_directory(identifier)
            record = self.read_record(identifier)
            try:
                report = self.saved_report(directory)
                if report is None or report.get("verdict") == "RUNNING":
                    raise SetupError("Runner exited without a completed campaign report; "
                                     "no passing outcome can be claimed.", 500)
                require(not report.get("livePortalValidated"),
                        "Unexpected live-validation claim in a non-live setup run.", 500)
                require(record["mode"] != "offline" or not report.get("acceptanceValidated"),
                        "Offline checks cannot establish Portal acceptance.", 500)
                require((code == 0) == report["verdict"].startswith("PASS") and
                        (code != 0 or report.get("negativeComplete") is True),
                        "Runner exit code and saved report disagree.", 500)
                require(code != 0 or record["mode"] != "evidence" or
                        (report.get("acceptanceValidated") is True and
                         report.get("portalParity", {}).get("status") == "CAPTURED_PORTAL_PARITY_PASS"),
                        "A passing evidence run needs the captured-Portal acceptance gate.", 500)
                require(isinstance(report.get("source"), dict) and
                        report["source"].get("sha256") == record["source"]["sha256"],
                        "Runner source differs from the reviewed setup; no acceptance can be claimed.", 500)
                record.update({"state": "completed", "verdict": report["verdict"]})
            except (OSError, ValueError, SetupError, finops.EvidenceError) as exc:
                record.update({"state": "error", "error": str(exc)})
                LOGGER.exception("Test runner outcome could not be verified")
            record.update({"exitCode": code, "completedAt": finops.utc_now()})
            try:
                write_record(directory, record)
            finally:
                self.active_id = None

    def status(self, identifier: str) -> Json:
        with self.lock:
            directory = self.run_directory(identifier)
            record = self.read_record(identifier)
            if record["state"] == "running" and self.active_id != identifier:
                record.update({"state": "interrupted", "error": "Server restarted before completion was recorded. "
                               "Inspect the saved reports and runner PID; this is not a completed verification."})
                record["completedAt"] = finops.utc_now()
                write_record(directory, record)
            report = self.saved_report(directory)
            log = ""
            log_path = directory / "runner.log"
            if log_path.is_file():
                with log_path.open("rb") as stream:
                    stream.seek(max(0, log_path.stat().st_size - 24000))
                    log = stream.read().decode("utf-8", errors="replace")
            previews = {}
            for name in ("portal-validation.json", "portal-reference.json"):
                if (directory / name).is_file():
                    previews[name] = (directory / name).read_text(encoding="utf-8")
            artifacts = [str(path.relative_to(directory)).replace("\\", "/")
                         for path in sorted(directory.rglob("*")) if path.is_file() and
                         path.suffix in (".json", ".jsonl", ".md", ".log") and
                         path.resolve().is_relative_to(directory.resolve())]
            return {**record, "report": report, "log": log, "previews": previews, "artifacts": artifacts,
                    "commandPreview": subprocess.list2cmdline(self.command(record))}

    def history(self) -> list[Json]:
        with self.lock:
            records = [self.read_record(path.name) for path in self.output.iterdir()
                       if re.fullmatch(r"[a-f0-9]{32}", path.name) and (path / "setup.json").is_file()]
            return sorted(records, key=lambda record: record["createdAt"], reverse=True)

    def artifact(self, identifier: str, value: str) -> Path:
        directory = self.run_directory(identifier)
        path = safe_path(directory, value, [directory.resolve()])
        require(path.suffix in (".json", ".jsonl", ".md", ".log"), "Artifact type is not downloadable.", 403)
        return path

    def wait(self) -> None:
        if self.monitor is not None:
            self.monitor.join()


class SetupServer(ThreadingHTTPServer):
    daemon_threads = False

    def __init__(self, address: tuple[str, int], app: SetupApp):
        self.app = app
        super().__init__(address, SetupHandler)


class SetupHandler(BaseHTTPRequestHandler):
    @property
    def setup_server(self) -> SetupServer:
        if not isinstance(self.server, SetupServer):
            raise SetupError("Invalid local setup server.", 500)
        return self.server

    def guard(self, mutating: bool = False) -> None:
        origin = f"http://127.0.0.1:{self.setup_server.server_port}"
        require(self.headers.get("Host") == origin.removeprefix("http://"),
                "Only the loopback host is accepted.", 403)
        require(self.headers.get("Sec-Fetch-Site") != "cross-site", "Cross-site requests are not allowed.", 403)
        if mutating:
            require(self.headers.get("Origin") == origin, "A same-origin browser request is required.", 403)
            require(hmac.compare_digest(self.headers.get("X-Setup-Token", ""), self.setup_server.app.token),
                    "Missing or invalid setup request token. Reload the page.", 403)

    def respond(self, status: int, data: bytes, content_type: str, filename: str | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; connect-src 'self'; "
                         "script-src 'self'; style-src 'self'; img-src 'none'; object-src 'none'; "
                         "base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        if filename is not None:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(data)

    def json_response(self, value: Any, status: int = 200) -> None:
        self.respond(status, json.dumps(value, ensure_ascii=True, allow_nan=False).encode("utf-8"),
                     "application/json; charset=utf-8")

    def dispatch(self, mutating: bool) -> None:
        try:
            self.guard(mutating)
            path = unquote(urlsplit(self.path).path)
            app = self.setup_server.app
            if mutating:
                require(self.headers.get("Content-Type", "").split(";")[0] == "application/json",
                        "Send application/json.", 415)
                require(self.headers.get("Transfer-Encoding") is None, "Chunked requests are not supported.", 400)
                length = int(self.headers.get("Content-Length", "0"))
                require(0 < length <= 2_000_000, "Request body must be between 1 byte and 2 MB.", 413)
                payload = finops.parse_json(self.rfile.read(length).decode("utf-8"))
                if path == "/api/plan":
                    object_fields(payload, {"planPath"}, "plan lookup")
                    self.json_response(app.plan_summary(app.plan(payload.get("planPath"))[1]))
                elif path == "/api/prepare":
                    self.json_response(app.prepare(payload), 201)
                elif re.fullmatch(r"/api/runs/[a-f0-9]{32}/start", path):
                    object_fields(payload, set(), "run request")
                    self.json_response(app.start(path.split("/")[3]), 202)
                else:
                    raise SetupError("Endpoint not found.", 404)
            elif path == "/api/bootstrap":
                self.json_response(app.bootstrap())
            elif path == "/api/runs":
                self.json_response(app.history())
            elif re.fullmatch(r"/api/runs/[a-f0-9]{32}", path):
                self.json_response(app.status(path.split("/")[3]))
            elif re.fullmatch(r"/api/runs/[a-f0-9]{32}/artifacts/.+", path):
                parts = path.split("/", 5)
                artifact = app.artifact(parts[3], parts[5])
                self.respond(200, artifact.read_bytes(), "application/octet-stream", artifact.name)
            elif path in ("/", "/app.js", "/style.css"):
                name, mime = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"),
                              "/style.css": ("style.css", "text/css")}[path]
                self.respond(200, (STATIC / name).read_bytes(), mime + "; charset=utf-8")
            else:
                raise SetupError("Page not found.", 404)
        except SetupError as exc:
            LOGGER.warning("Request rejected: %s", exc)
            self.json_response({"error": str(exc)}, exc.status)
        except (finops.EvidenceError, KeyError, TypeError, ValueError) as exc:
            LOGGER.warning("Invalid setup input: %s", exc)
            self.json_response({"error": f"Invalid setup input: {exc}"}, 400)
        except OSError as exc:
            LOGGER.exception("Local setup I/O failed")
            self.json_response({"error": f"Local file/process error: {exc}"}, 500)

    def do_GET(self) -> None:
        self.dispatch(False)

    def do_POST(self) -> None:
        self.dispatch(True)

    def log_message(self, format: str, *args: Any) -> None:
        LOGGER.info("%s", format % args)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765, help="Loopback port; use 0 for an available port.")
    parser.add_argument("--evidence-root", type=Path, action="append", default=[],
                        help="Additional explicitly approved local evidence directory (repeatable).")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        require(0 <= args.port <= 65535, "Port must be 0..65535.")
        app = SetupApp(evidence_roots=args.evidence_root)
        server = SetupServer(("127.0.0.1", args.port), app)
    except (OSError, SetupError) as exc:
        LOGGER.error("Cannot start verification setup: %s", exc)
        return 2
    print(f"Verification setup: http://127.0.0.1:{server.server_port}", flush=True)
    print(f"Private local outputs: {app.output}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping. Waiting for any active test campaign to finish.", flush=True)
    finally:
        server.server_close()
        app.wait()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
