# Read-only analyst capability boundaries

Use this reference before routing a FinOps request. It ports the useful
capability-register controls into the local skill pack without claiming
that every planned capability is implemented. Instructions guide behavior;
they are not an authorization boundary or a machine-enforced tool registry.

The [cost workflow](../SKILL.md) and [evidence contract](./evidence-contract.md)
define the executable boundary. Catalog guidance, a discoverable local skill,
an available tool, source permissions, hosted-application support, and measured
analytical qualification are separate facts.

## Capability routing

| ID | Local availability and required boundary |
|---|---|
| CAP-QUERY | Supported for the documented scenario schema and generated, sealed query plans only. Clarify missing intent; do not execute model-written arbitrary queries or silently change dimensions. |
| CAP-IDENTITY | Supported for confirmed interactive invoker/tenant and approved subscription IDs. Resource, cost, directory, ownership, and invoice permissions are independent; denial never authorizes identity substitution. |
| CAP-RESOURCE | Supported for paginated current ARG inventory and exact resource sets. Caller-visible current evidence is not an atomic historical estate; historical membership needs another approved source. |
| CAP-COST | Supported for ActualCost/AmortizedCost daily PreTaxCost by resource/location and original billing currency. Missing, denied, partial, or unsupported evidence is not zero. |
| CAP-BILLING | No billing/invoice adapter is bundled. Require authoritative agreement-specific invoice linkage, separately approved minimum scope and entitlement; subscription access is insufficient. |
| CAP-MONEY | Supported for the helper's exact signed decimal aggregation and reconciliation, with currency isolation. FX, cross-period calculations, rates, and arbitrary derived metrics need reviewed deterministic adapters and source provenance; never model arithmetic. |
| CAP-GROUNDING | Capture hashes, raw pages, plans, controls, and reference parity provide lineage. Attach each factual finding to source rows or helper-emitted values; this is not an automatic universal factual-claim validator. |
| CAP-REPORT | Supported for private local Markdown, standalone HTML, and explicitly selected installed-browser PDF. Other extract schemas, delivery integrations, and public sharing are not supplied. |
| CAP-FORECAST | No forecast or hypothetical-pricing adapter is bundled. A future reviewed workflow must declare horizon, history, assumptions, rates, region/tier/term, currency, and uncertainty; retail estimates never replace negotiated actuals. |
| CAP-GOVERNANCE | No budget/alert/policy read adapter is bundled. Any future source must be independently approved and read-only; a budget is not a spending cap, and a planning target is not an Azure budget. |
| CAP-OPTIMIZE | Conditional advice only; no bundled utilization, pricing, Advisor, or commitment adapter. Measured savings/rightsizing need those sources plus existing benefits, ownership and commercial constraints. Never resize, delete, purchase, exchange, or deploy. |
| CAP-ALLOCATION | No shared-cost/business-denominator adapter is bundled. Require authorized effective-dated membership, metrics, allocation rules, and visible residuals; do not invent owners, weights, unit costs, or historical attribution. |
| CAP-EVALUATION | Offline helper tests and conversation scenarios exist, not analytical certification. Model compliance/live parity require independently executed traces and references; no zero-hallucination or 99% qualification claim. |
| CAP-REVIEW | Supported through private invoker clarification and local evidence handoff. No new mailbox, ticket, external reviewer, or sharing integration is authorized; human opinion is not promoted into a source fact. |
| CAP-SKILLS | Verify actual skill/tool discovery, supported operation, source contract, permissions, and scope before use. This document supplies routing guidance, not a dynamic registry or permission grant; never guess tool names or install tools automatically. |
| CAP-ANALYSIS | Supported for evidence-backed observations and side-by-side native amounts under comparable scopes. No bundled variance/percentage/anomaly-statistics or unit-economics engine; a spike alone establishes neither cause nor waste. |

## Preflight for any additional source

Before using a separately approved adapter, establish its actual availability,
documented operation and response schema, read-only behavior, invoker identity,
authorized source scope, complete pagination, precision, and evidence-retention
contract. Discovery is not approval. Do not inherit write operations from an
upstream optimization/governance skill or broaden subscription/billing scope.
If those facts cannot be established, explain the missing capability and abstain
from that part of the request. Offer supported work only with the invoker's
approval; do not imply that a future adapter is already usable.

Required intent includes immutable scope, current versus historical membership,
complete UTC dates, cost basis, requested dimensions, original currencies,
comparison population/windows when relevant, and private output format.
Resolve facts through approved authoritative metadata; ask targeted questions
for user decisions. Do not request secrets or manufacture missing evidence.

## Invoice, money, and claim boundaries

- Resource-level ActualCost is not an invoice amount due. For MCA, linked
  billing-profile/invoice access must be proven separately. Do not expose a
  shared invoice beyond the approved disclosure boundary.
- Invoice taxes, fees, credits, and benefits must not be added again to resource
  costs or allocated without authoritative linkage. Preserve signed source
  charges; do not deduplicate legitimate equal-value rows by guesswork.
- Keep original currencies separate. No FX ledger or conversion is bundled;
  never introduce an assumed exchange rate or a cross-currency grand total.
- Distinguish measured costs, independently sourced recommendations, hypotheses,
  and predictions. Cite the applicable scope, period, basis, currency, capture,
  and exact source rows/emitted totals. A hash or confidence score is not proof.
- Retain BLOCKED, UNVERIFIED, or VALIDATED AGAINST CAPTURED REFERENCES exactly as
  defined by the agent. A capability's presence never upgrades validation.

## Upstream guidance

The local [Azure Cost Management documentation skill](../../azure-cost-management/SKILL.md)
adapts MicrosoftDocs guidance for official-documentation retrieval, API/error
explanations, limits, and source-specific access. It adds conceptual coverage,
not any of the missing data/calculation adapters listed above.

The [Microsoft cost-analysis skill](https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-cost/skills/cost-analysis/SKILL.md)
informs the historical-spend, bill-change, AKS, and AI routing above. Its MCP
tools are not dependencies of this pack. Adjacent
[estimation](https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-cost/skills/cost-estimation/SKILL.md),
[governance](https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-cost/skills/cost-governance/SKILL.md),
and [optimization](https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-cost/skills/cost-optimization/SKILL.md)
guidance describes separate workflows, not installed capabilities or approved
writes. Upstream `main` can change; review any later integration independently.
