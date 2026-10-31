"""Validate the public-only static Pages artifact without extra dependencies."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ALLOWED = {"index.html", "licenses/Apache-2.0.txt"}
REQUIRED_SECTIONS = {"main", "why", "zava", "workflow", "audience", "readiness", "verification", "start"}


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.controls: list[str] = []
        self.h1_count = 0
        self.scripts: list[str] = []
        self.text: list[str] = []
        self.in_script = False

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "a":
            assert attrs.get("href"), "Every link needs a destination."
            self.links.append(attrs["href"])
        if attrs.get("aria-controls"):
            self.controls.extend(attrs["aria-controls"].split())
        self.h1_count += tag == "h1"
        assert tag not in ("form", "iframe", "object", "embed"), "The public site must not accept customer data."
        assert "src" not in attrs, "No remote scripts, images, trackers, or other source assets are allowed."
        assert not any(key.startswith("on") for key in attrs), "Use registered event handlers, not inline handlers."
        if tag == "script":
            self.in_script = True
            self.scripts.append("")
        if tag == "html":
            assert attrs.get("lang") == "en", "Declare the document language."
        if tag == "main":
            assert attrs.get("id") == "main" and attrs.get("tabindex") == "-1", "The skip-link target must receive focus."

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self.in_script = False

    def handle_data(self, data: str) -> None:
        if self.in_script:
            self.scripts[-1] += data
        else:
            self.text.append(data)


def main() -> None:
    files = set()
    for path in SITE.rglob("*"):
        assert not path.is_symlink(), "Pages artifacts must not contain links to private files."
        if path.is_file():
            files.add(path.relative_to(SITE).as_posix())
    assert files == ALLOWED, f"Unexpected or missing public artifact files: {files ^ ALLOWED}."
    source = (SITE / "index.html").read_text(encoding="utf-8")
    page = Page()
    page.feed(source)
    assert len(page.ids) == len(set(page.ids)), "Duplicate document IDs."
    assert REQUIRED_SECTIONS <= set(page.ids), "A required explanatory section is missing."
    assert page.h1_count == 1, "Use a single page heading."
    for target in page.controls:
        assert target in page.ids, f"Missing interactive control destination: {target}."
    for href in page.links:
        parsed = urlsplit(href)
        if parsed.scheme:
            assert parsed.scheme == "https", f"Unsupported external link: {href}."
        elif href.startswith("#"):
            assert href[1:] in page.ids, f"Broken section link: {href}."
        else:
            destination = (SITE / unquote(parsed.path)).resolve()
            assert destination.is_relative_to(SITE.resolve()) and destination.is_file(), f"Broken local link: {href}."
    assert len(page.scripts) == 2, "Keep the site self-contained and the script surface small."
    assert "clawpilotTheme" in page.scripts[0] and "prefers-color-scheme" in page.scripts[0]
    for script in page.scripts:
        assert not re.search(r"\b(fetch|XMLHttpRequest|WebSocket|eval)\s*\(", script), "No public data/API connection."
        assert not re.search(r"\b(localStorage|sessionStorage|document\.cookie)\b", script), "No tracking storage."
    text = " ".join(page.text)
    for required in ("Zava", "read-only", "Decimal", "UNVERIFIED", "BLOCKED", "NOT RUN", "CC BY 4.0",
                     "not production-certified", "not Portal evidence", "current source fingerprint",
                     "complete independent resource reference", "not a universal secret detector",
                     "atomic create-only publication", "hard links",
                     "Restricted tools-disabled model probes"):
        assert required in text, f"Missing purpose or limitation: {required}."
    assert "DTNA" not in source, "The microsite must use only the approved illustrative Zava context."
    assert not re.search(r"\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b", source, re.I), "No tenant/resource UUIDs."
    assert "Synthetic example" in text, "The cost illustration must be labeled synthetic."
    workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    assert re.findall(r"(?m)^\s+path: (.+)$", workflow) == ["site"], "Only the site directory may be uploaded."
    actions = re.findall(r"uses: actions/([^@\s]+)@([^\s]+)", workflow)
    assert {name for name, _ in actions} == {"checkout", "configure-pages", "upload-pages-artifact", "deploy-pages"}
    assert all(re.fullmatch(r"[a-f0-9]{40}", sha) for _, sha in actions), "Pin all deployment actions."
    print(f"PASS: {len(files)} public files; section/local links, privacy boundary, notices and pinned Pages workflow validated.")


if __name__ == "__main__":
    main()
