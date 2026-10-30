"""Standard-library executable-line coverage; this is not branch coverage."""

from __future__ import annotations

import json
import sys
import types
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TARGETS = [
    ROOT / ".github" / "skills" / "finops-cost-evidence" / "scripts" / "finops.py",
    ROOT / ".github" / "skills" / "finops-cost-evidence" / "scripts" / "portal_validation.py",
    ROOT / ".github" / "skills" / "finops-cost-evidence" / "tests" / "run_tests.py",
    ROOT / "tools" / "verification_setup" / "server.py",
]


def executable_lines(code: types.CodeType) -> set[int]:
    result = {line for _, _, line in code.co_lines() if line is not None and line > 0}
    for item in code.co_consts:
        if isinstance(item, types.CodeType):
            result.update(executable_lines(item))
    return result


class LineCoverage:
    def __init__(self) -> None:
        self.files = {str(path.resolve()).casefold(): path for path in TARGETS}
        self.hits: dict[str, set[int]] = {name: set() for name in self.files}
        self.previous: Any = None

    def trace(self, frame: types.FrameType, event: str, _argument: Any):
        name = frame.f_code.co_filename.casefold()
        if name not in self.files:
            return None
        if event == "line":
            self.hits[name].add(frame.f_lineno)
        return self.trace

    def __enter__(self):
        self.previous = sys.gettrace()
        sys.settrace(self.trace)
        return self

    def __exit__(self, _kind, _value, _traceback):
        sys.settrace(self.previous)

    def save(self, path: Path) -> None:
        files = {}
        for name, source in self.files.items():
            lines = executable_lines(compile(source.read_text(encoding="utf-8-sig"), str(source), "exec"))
            files[str(source.relative_to(ROOT))] = {
                "executable": sorted(lines), "covered": sorted(self.hits[name] & lines)}
        path.write_text(json.dumps({"metric": "Python bytecode executable lines; not branch coverage",
                                    "files": files}, indent=2), encoding="utf-8")


def merge(paths: list[Path]) -> dict:
    combined: dict[str, dict[str, set[int]]] = {}
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for name, values in data["files"].items():
            entry = combined.setdefault(name, {"executable": set(), "covered": set()})
            for kind in entry:
                entry[kind].update(values[kind])
    files = {}
    for name, values in sorted(combined.items()):
        total, covered = values["executable"], values["covered"]
        files[name] = {"executableLines": len(total), "coveredLines": len(covered),
                       "percent": round(100 * len(covered) / len(total), 2) if total else 0,
                       "missingLines": sorted(total - covered)}
    return {"metric": "Python bytecode executable lines; not branch coverage",
            "includesImportsAndEntrypoints": False, "files": files}
