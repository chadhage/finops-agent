# Azure cost-analysis skill

Optional development-assistant guidance from Microsoft's `azure-cost` plugin for analyzing actual Azure spend, bill changes, and AKS or AI service costs.

**Documentation date:** 2026-10-29  
**Execution status:** The upstream installer was not run for the workspace integration; upstream installation remains unverified. Useful guidance is now ported into the local agent as described below.

## Workspace-native integration

The existing [cost-evidence skill](../../.github/skills/finops-cost-evidence/SKILL.md)
now includes historical-spend, bill-change, and bounded AKS/AI resource-cost
workflows. [FinOpsAgent](../../.github/agents/FinOpsAgent.agent.md) routes those
requests through the skill and its
[analyst capability boundaries](../../.github/skills/finops-cost-evidence/references/analyst-capabilities.md).
Select FinOpsAgent in this workspace; reload VS Code or start a new chat if
updated skill discovery is not visible.

This is a port into the existing four-skill pack, not a copy of the upstream
MCP tool contract. It preserves raw evidence, exact decimal arithmetic, complete
pagination, explicit scope approval, and read-only access. It does not supply
namespace/model allocation, forecasts, invoice linkage, or other gated adapters.
The original guide stays here so existing planning/backlog links remain valid.

## Optional upstream installation command

The requested command is:

```powershell
npx skills add https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-cost/skills/cost-analysis
```

Run it only when you intend to install the skill and have Node.js/npm with `npx` available. For a project-scoped installation, start from the repository root and review the installer's agent, scope, and destination choices before accepting. This guide does not select or authorize a global/user-profile installation.

The URL follows `main`, so the upstream content may change. Review the [upstream skill](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-cost/skills/cost-analysis) before installing or accepting updates.

## Intended use and verification

- Use the skill for historical spend breakdowns, bill-change investigation, and authorized AKS or AI cost analysis.
- Forecasting, pricing estimates, rightsizing, commitments, and budgets are outside this skill's stated scope; use the appropriate separately reviewed workflow.
- After installation, verify that the intended assistant can discover `cost-analysis` and that the configured Azure data tools referenced by the skill are available.
- The command does not by itself configure Azure data tools or guarantee MCP availability. Follow the selected assistant's tool configuration and authentication requirements separately.
- Before querying, confirm the approved subscription/billing scope, reporting period, cost basis, currency, and requested breakdown. Preserve incomplete-data warnings and keep currencies separate.
- Follow the installed skill's source/tool-side grouping, totals, sorting, row-limit, and safety guidance. Do not treat unavailable data as zero or inferred causes as measured facts.

## Authorization and invoice boundaries

Installing guidance does not grant Azure permissions, authenticate the prompting user, grant consent, activate PIM, or authorize broader billing access.

Resource inventory, Cost Management details, and billing/invoice records can require different permissions and scopes. For MCA invoices, validate the minimum linked billing-profile/invoice access separately; a subscription resource role alone does not establish invoice access. Do not substitute another identity or silently broaden scope.

Resource-level `ActualCost` in billing currency is not the invoice amount due. Invoice-level taxes, credits, and fees must not be added again to resource costs or allocated to resources without authoritative evidence. Shared-invoice data must remain within the explicitly approved disclosure boundary.

## Project and MVP boundary

This is development-assistant tooling, not a deployment or application feature. Installing it does not change the approved MVP, enable cost/billing/invoice APIs in the hosted agent, deploy resources, modify permissions, or establish that a backlog item has passed acceptance.

The [approved M1 implementation scope](../iterations/iteration-0002.md#committed-scope) remains private, user-authorized inventory plus its five utility outcomes. New [product priorities](../backlog/index.md) retain their separate source-contract, permission, estimate, candidate-scope, and release gates. Skill installation is not an extra accepted delivery outcome or a substitute for those gates.

For the broader read-only analyst requirements, see the [capability register](./finops-analyst-capabilities.md) and [scenario/qualification programme](../bdd/finops-scenario-coverage.md). These remain planning requirements, not proof that all capabilities are implemented or analytically qualified; the local port's supported subset and gates are documented above.

## References

- [Microsoft cost-analysis skill and workflow](https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-cost/skills/cost-analysis/SKILL.md)
- [Azure cost plugin metadata](https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-cost/.plugin/plugin.json)
- [MCA billing-profile roles](https://learn.microsoft.com/azure/cost-management-billing/manage/understand-mca-roles#billing-profile-roles-and-tasks)
- [Review an MCA invoice and its usage charges](https://learn.microsoft.com/azure/cost-management-billing/understand/review-customer-agreement-bill)
- [Cost details fields and invoice identifiers](https://learn.microsoft.com/azure/cost-management-billing/automate/understand-usage-details-fields#list-of-fields-and-descriptions)

---

[Product backlog](../backlog/index.md) | [Product roadmap](../roadmap/index.md) | [Approved M1 scope](../iterations/iteration-0002.md#committed-scope)
