# Agent references and skill usage

## Verification setup page

Use the [local setup page](verification-setup.md) to enter verification inputs,
generate the config/Portal reference index, run the existing negative-first
suite, and inspect saved reports. Start it with the
[standard-library Python server](../tools/verification_setup/server.py).
The UI supports offline and captured-evidence modes only; it does not authorize
or execute live Azure access.

## Azure Cost Management documentation skill

**Integrated:** 2026-10-30  
**Local name:** `azure-cost-management`  
**Purpose:** Current Microsoft Learn guidance for Cost Management concepts,
troubleshooting, source-specific access, API selection, and configuration
explanations. This is a documentation skill, not a new billing connector.

### Where it is wired

- [Workspace skill](../.github/skills/azure-cost-management/SKILL.md): discoverable
  instructions, eight-category documentation index, source attribution, and
  read-only safeguards.
- [FinOpsAgent](../.github/agents/FinOpsAgent.agent.md): loads the skill on demand
  for Cost Management documentation and troubleshooting questions.
- [Cost-evidence skill](../.github/skills/finops-cost-evidence/SKILL.md): retains
  the executable workflow and uses the documentation skill for API/error/data
  semantics, without changing its evidence contract.
- [Capability boundaries](../.github/skills/finops-cost-evidence/references/analyst-capabilities.md):
  distinguishes explanatory guidance from supported data collection.

### How to use it

1. Open this workspace in VS Code and select **FinOpsAgent** in Chat.
2. Ask a Cost Management documentation question; the agent loads the skill when
   relevant. You can also explicitly invoke `/azure-cost-management` when the
   chat client exposes skill slash commands.
3. If the skill is missing, reload the VS Code window or start a new chat.
4. The agent fetches the relevant official documentation and cites it, explains
   scope/agreement caveats, and separates guidance from customer-specific facts.

Documentation-only examples:

> Use azure-cost-management to explain Cost Management access-denied errors and
> how subscription cost-read access differs from MCA invoice access. Cite current
> Microsoft Learn sources. Do not sign in or query customer data.

> Explain ActualCost versus AmortizedCost, data latency, and which Cost Management
> API fits resource/day cost analysis. Documentation only; do not change the
> helper's API version or query plan.

> Explain how budgets, alerts, and recurring cost exports work and their
> prerequisites. Do not create, change, or inspect a live configuration.

For an actual analysis, explicitly approve the identity/scope/dates/basis:

> For my confirmed tenant and approved subscription IDs, analyze the approved
> complete UTC period as ActualCost. Resolve the workload and show the manifest
> for approval before querying. Use azure-cost-management for documented error
> and data-semantics explanations, and the existing helper for exact cost evidence.

The last request still follows
[invoker access](../.github/skills/finops-invoker-access/SKILL.md),
[scope resolution](../.github/skills/finops-scope-resolution/SKILL.md),
[cost evidence](../.github/skills/finops-cost-evidence/SKILL.md), and
[reporting](../.github/skills/finops-reporting/SKILL.md). Documentation does not
replace approvals, full pagination, decimal-safe currency-separated amounts,
independent references, or validation-status checks.

### Tools, privacy, and limits

- Documentation retrieval requires network access, not an Azure login.
  Prefer an available Microsoft Learn MCP documentation-fetch tool; the existing
  web-fetch tool is the fallback. No MCP server, package, plugin, or extension
  was installed for this integration.
- Documentation URLs use `from=learn-agent-skill`; the web fallback also uses
  `accept=text/markdown`. Tool names are discovered rather than assumed.
- Only public URLs and generic product/error-code terms go to documentation
  services. Never send customer identifiers, owner emails, costs, invoices,
  evidence, or credentials.
- Budget/reservation/export/configuration documentation is explanatory.
  It adds no live adapter, forecast engine, permission grant, purchase ability,
  write operation, or deployed/hosted application feature.
- If documentation retrieval fails, report the missing source. If actual
  evidence is unavailable, preserve the existing blocked/unverified outcome;
  documentation cannot establish a customer's spend or configuration.
- Recheck source applicability and dates. If the upstream generation date is
  more than three months old, review an upstream update deliberately; do not
  automatically overwrite the local safeguards.

### Source and license

- [Requested upstream skill on main](https://github.com/MicrosoftDocs/Agent-Skills/blob/main/skills/azure-cost-management/SKILL.md).
- [Reviewed source revision](https://github.com/MicrosoftDocs/Agent-Skills/blob/95544200a6621ee7481b253beb115ac0be701689/skills/azure-cost-management/SKILL.md):
  `95544200a6621ee7481b253beb115ac0be701689`, committed 2026-10-26; upstream
  generation date 2026-10-25. Microsoft Learn pages are fetched live and are
  not pinned to that repository revision.
- Attribution: **Cost Management Skill**, MicrosoftDocs/Agent-Skills contributors,
  under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) and the
  [upstream license](https://github.com/MicrosoftDocs/Agent-Skills/blob/95544200a6621ee7481b253beb115ac0be701689/LICENSE).
- Local changes: curated the eight-category index, added tool discovery/web
  fallback and data-minimization rules, connected the evidence skills, and made
  write/configuration/deployment material explanation-only. No upstream
  endorsement or full catalog implementation is implied.

See also the [analyst capability register](tooling/finops-analyst-capabilities.md)
and [cost-analysis integration guide](tooling/cost-analysis-skill.md).
