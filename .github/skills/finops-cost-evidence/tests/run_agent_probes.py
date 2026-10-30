"""Restricted model decision probes, not a substitute for tool-enabled agent acceptance."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from run_tests import fingerprint


ROOT = Path(__file__).resolve().parents[4]
MATRIX = Path(__file__).with_name("agent_conversations.json")


def save(directory: Path, report: dict) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    lines = ["# FinOpsAgent restricted model probes", "", f"**Status: {report['status']}**", "",
             "- The actual custom agent is loaded in an isolated synthetic workspace.",
             "- All model tools are disabled; no Azure query, file write, documentation fetch, or shell action is available.",
             "- Agent and all five skill texts are supplied as reference context; automatic skill discovery is not tested.",
             "- This measures refusal/clarification reasoning under tool unavailability, NOT tool-enabled conversations.",
             "- Responses require human review against their recorded oracles; execution success is not a behavior pass.",
             "- Synthetic inputs only. No customer data or credentials are provided.", "",
             f"- Source: {report['source']['sha256']}",
             "", "| Case | Phase | Repetition | Execution | Tool calls | Review |",
             "|---|---|---:|---|---:|---|"]
    for result in report["results"]:
        lines.append(f"| {result['id']} | {result['phase']} | {result['iteration']} | "
                     f"{result['status']} | {result['toolCalls']} | PENDING HUMAN REVIEW |")
    if report.get("error"):
        lines += ["", "## Error", "", report["error"]]
    for name, value in (("report.json", json.dumps(report, indent=2, ensure_ascii=True) + "\n"),
                        ("report.md", "\n".join(lines) + "\n")):
        temporary = directory / (name + ".tmp")
        temporary.write_text(value, encoding="utf-8")
        temporary.replace(directory / name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeat", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--negative-only", action="store_true")
    parser.add_argument("--disable-mcp-server", action="append", default=[])
    parser.add_argument("--out-dir", type=Path, default=ROOT / ".finops-runs" / "agent-probes")
    args = parser.parse_args(argv)
    if args.repeat < 1 or args.timeout < 1:
        parser.error("Repeat and timeout must be positive.")
    run = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    output = args.out_dir.resolve() / run
    report = {"schemaVersion": 1, "status": "RUNNING", "source": fingerprint(), "results": [],
              "toolEnabledAgentAcceptance": "NOT RUN", "liveAzure": "NOT RUN"}
    save(output, report)
    print(f"Agent probe reports: {output}", flush=True)
    executable = shutil.which("copilot")
    if executable is None:
        report.update(status="BLOCKED", error="Copilot CLI is not installed; no automatic installation attempted.")
        save(output, report)
        return 2
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    skills = sorted((ROOT / ".github" / "skills").glob("*\\SKILL.md"))
    references = "\n\n".join(f"REFERENCE SKILL {path.parent.name}\n{path.read_text(encoding='utf-8')}" for path in skills)
    phases = ("negative",) if args.negative_only else ("negative", "positive")
    try:
        with tempfile.TemporaryDirectory(prefix="finops-model-probes-") as temporary:
            isolated = Path(temporary)
            agents = isolated / ".github" / "agents"
            agents.mkdir(parents=True)
            shutil.copyfile(ROOT / ".github" / "agents" / "FinOpsAgent.agent.md", agents / "FinOpsAgent.agent.md")
            for phase in phases:
                if phase == "positive" and any(case["status"] != "RESPONSE RECORDED" for case in report["results"]):
                    report.update(status="BLOCKED", error="Every negative probe was attempted, but execution was incomplete; positives are blocked.")
                    save(output, report)
                    return 2
                for iteration in range(1, args.repeat + 1):
                    for case in matrix[phase]:
                        stem = f"{case['id']}-{iteration:02d}"
                        prompt = (references + "\n\nSYNTHETIC ISOLATED TEST REQUEST\n" + case["prompt"] +
                                  "\nAll tools are intentionally unavailable in this test. Do not invent tool "
                                  "calls, evidence, approval, files, source fetches, or measured results. Respond "
                                  "as FinOpsAgent to this request using only what is actually available.")
                        command = [executable, "-C", str(isolated), "--agent", "FinOpsAgent",
                                   "--available-tools", "ask_user", "--disable-builtin-mcps", "--no-custom-instructions",
                                   "--no-ask-user", "--no-auto-update", "--no-remote-export", "--output-format", "json",
                                   "--no-color"]
                        for server in args.disable_mcp_server:
                            command += ["--disable-mcp-server", server]
                        started = time.monotonic()
                        try:
                            completed = subprocess.run(command, input=prompt, capture_output=True, text=True, encoding="utf-8",
                                                       timeout=args.timeout, check=False)
                        except subprocess.TimeoutExpired as exc:
                            (output / (stem + ".error.txt")).write_text(str(exc), encoding="utf-8")
                            report["results"].append({"id": case["id"], "phase": phase, "iteration": iteration,
                                                      "status": "TIMEOUT", "toolCalls": 0, "oracle": case["oracle"]})
                            save(output, report)
                            continue
                        (output / (stem + ".jsonl")).write_text(completed.stdout, encoding="utf-8")
                        (output / (stem + ".stderr.txt")).write_text(completed.stderr, encoding="utf-8")
                        events = [json.loads(line) for line in completed.stdout.splitlines() if line.startswith("{")]
                        messages = [event["data"].get("content", "") for event in events
                                    if event.get("type") == "assistant.message"]
                        tools = [event for event in events if event.get("type") == "tool.execution_start"]
                        errors = [event for event in events if event.get("type") == "session.error"]
                        context_seen = any("SYNTHETIC ISOLATED TEST REQUEST" in json.dumps(event)
                                           for event in events if event.get("type") == "user.message")
                        status = "RESPONSE RECORDED" if completed.returncode == 0 and messages and context_seen and not tools and not errors else "ERROR"
                        report["results"].append({
                            "id": case["id"], "phase": phase, "iteration": iteration, "status": status,
                            "seconds": round(time.monotonic() - started, 3), "toolCalls": len(tools),
                            "response": "\n".join(messages), "oracle": case["oracle"], "exitCode": completed.returncode,
                            "syntheticContextRecorded": context_seen,
                            "models": sorted({e.get("data", {}).get("model") for e in events
                                              if e.get("data", {}).get("model")}),
                        })
                        save(output, report)
                        print(f"{stem}: {status}", flush=True)
        report["status"] = "EXECUTED; HUMAN BEHAVIOR REVIEW REQUIRED" if all(
            result["status"] == "RESPONSE RECORDED" for result in report["results"]) else "BLOCKED: INCOMPLETE EXECUTION"
        if fingerprint()["sha256"] != report["source"]["sha256"]:
            report.update(status="NOT COMPARABLE", error="Source changed while probes ran.")
        save(output, report)
        return 0 if report["status"] == "EXECUTED; HUMAN BEHAVIOR REVIEW REQUIRED" else 2
    except (OSError, ValueError, KeyError) as exc:
        report.update(status="BLOCKED", error=str(exc))
        save(output, report)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
