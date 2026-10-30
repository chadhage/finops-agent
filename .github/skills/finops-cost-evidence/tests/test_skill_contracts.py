from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[4]
SKILLS = ROOT / ".github" / "skills"
EXPECTED = {"finops-invoker-access", "finops-scope-resolution", "finops-cost-evidence",
            "finops-reporting", "azure-cost-management"}


class PositiveSkillContractTests(unittest.TestCase):
    """Static discovery/contracts only; no model compliance is inferred."""

    phase = "positive"

    def test_exact_five_skills_are_discoverable_with_portable_metadata(self):
        found = {path.parent.name for path in SKILLS.rglob("SKILL.md")}
        self.assertEqual(found, EXPECTED)
        for name in sorted(EXPECTED):
            with self.subTest(skill=name):
                text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
                header = text.split("---", 2)[1]
                self.assertRegex(header, rf"(?m)^name: {name}$")
                description = re.search(r'(?m)^description: (".*")$', header)
                self.assertIsNotNone(description)
                self.assertGreater(len(json.loads(description.group(1))), 40)
                self.assertLessEqual(len(json.loads(description.group(1))), 1024)
                self.assertLess(len(text.splitlines()), 500)

    def test_all_skill_and_agent_relative_links_resolve(self):
        paths = list(SKILLS.rglob("*.md")) + [ROOT / ".github" / "agents" / "FinOpsAgent.agent.md"]
        for path in paths:
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" not in target and not target.startswith("#"):
                    with self.subTest(path=path, target=target):
                        self.assertTrue((path.parent / target.split("#", 1)[0]).is_file())

    def test_agent_has_native_tool_map_and_no_model_lock_or_subagent_dependency(self):
        text = (ROOT / ".github" / "agents" / "FinOpsAgent.agent.md").read_text(encoding="utf-8")
        header = text.split("---", 2)[1]
        self.assertIn("tools: [read, search, execute, edit, web, vscode/askQuestions]", header)
        self.assertIn("agents: []", header)
        self.assertNotRegex(header, r"(?m)^model:")
        for name in EXPECTED:
            self.assertIn(f"../skills/{name}/SKILL.md", text)

    def test_documentation_skill_links_only_official_public_sources(self):
        text = (SKILLS / "azure-cost-management" / "SKILL.md").read_text(encoding="utf-8")
        urls = re.findall(r"\[[^\]]+\]\((https://[^)]+)\)", text)
        categories = ["Troubleshooting", "Best practices", "Decision making", "Limits and quotas",
                      "Security and access", "Configuration", "Integrations and coding patterns", "Deployment"]
        for category in categories:
            self.assertIn("| " + category + " |", text)
        learn = [url for url in urls if urlsplit(url).netloc == "learn.microsoft.com"]
        self.assertGreaterEqual(len(learn), 16)
        self.assertTrue(all(urlsplit(url).netloc in ("learn.microsoft.com", "github.com", "creativecommons.org")
                            for url in urls))
        for boundary in ("no Azure login", "Never send tokens", "web-fetch", "Preserve existing query parameters",
                         "does not implement a new adapter", "Do not install"):
            self.assertIn(boundary, text)

    def test_every_registered_conversation_has_a_unique_oracle(self):
        path = SKILLS / "finops-cost-evidence" / "tests" / "agent_conversations.json"
        matrix = json.loads(path.read_text(encoding="utf-8"))
        identifiers = []
        for phase in ("negative", "positive"):
            self.assertGreater(len(matrix[phase]), 0)
            for case in matrix[phase]:
                identifiers.append(case["id"])
                self.assertGreater(len(case["prompt"]), 30)
                self.assertGreater(len(case["oracle"]), 30)
        self.assertEqual(len(identifiers), len(set(identifiers)))


class NegativeSkillBoundaryTests(unittest.TestCase):
    phase = "negative"

    def test_documentation_does_not_replace_cost_or_auth_adapters(self):
        text = (SKILLS / "azure-cost-management" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("not to", text)
        self.assertIn("No billing/invoice", text)
        self.assertIn("Never execute upstream examples", text)
        self.assertIn("Do not upgrade BLOCKED", text)

    def test_cross_period_comparison_cannot_be_a_same_plan_reconciliation(self):
        text = (SKILLS / "finops-cost-evidence" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("never two different reporting periods", text)
        self.assertIn("does not calculate cross-period deltas", text)
        self.assertIn("not proof of cause", text)

    def test_aks_ai_allocation_is_not_invented_from_resource_totals(self):
        text = (SKILLS / "finops-cost-evidence" / "SKILL.md").read_text(encoding="utf-8")
        for limitation in ("nodes, disks", "per-token", "additional sources", "Do not enable AKS cost analysis"):
            self.assertIn(limitation, text)

    def test_reporting_does_not_treat_missing_references_as_validated(self):
        text = (SKILLS / "finops-reporting" / "SKILL.md").read_text(encoding="utf-8")
        for limitation in ("UNVERIFIED", "no implicit FX", "not a successful acceptance", "Do not rewrite monetary"):
            self.assertIn(limitation, text)
