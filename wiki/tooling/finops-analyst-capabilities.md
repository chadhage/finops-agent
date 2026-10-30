# Read-only FinOps analyst capability register

**Review date:** 2026-10-29  
**Capability entries:** 16  
**Verification status:** Catalog descriptions reviewed; installation, hosted-tool availability and analytical qualification are not established by this document.

The product owner approved broad read-only scenario planning, not tool installation, data access, MVP expansion or production certification. The four catalog cost skills below are complementary; none promises zero hallucinations or independently certifies 99% accuracy/completeness. Required custom controls must be implemented and qualified separately.

## Local agent integration

The useful routing, parameter, evidence, and read-only controls are now ported
into the workspace [FinOpsAgent](../../.github/agents/FinOpsAgent.agent.md),
[cost-evidence skill](../../.github/skills/finops-cost-evidence/SKILL.md), and
its [local capability boundaries](../../.github/skills/finops-cost-evidence/references/analyst-capabilities.md).
The local reference maps all 16 capability IDs to bounded support or explicit
missing-source/calculation gates. It is included with the reusable skill pack
and does not require the wiki at runtime.

This register remains the broader planning source. Its catalog availability
statements are not claims about the local implementation or hosted .NET
application. No external plugin, new data adapter, permission, or qualification
is established by the port; unsupported intents remain blocked rather than
being guessed from historical cost evidence.

The workspace also includes a read-only
[Azure Cost Management documentation skill](../../.github/skills/azure-cost-management/SKILL.md)
adapted from MicrosoftDocs. It supplies official-documentation guidance, not a
new data adapter or evidence qualification. See [references and usage](../references.md)
for invocation examples, attribution, and its explanatory-only configuration scope.

## Capability register

| Capability ID | Required capability | Guidance / availability status | Read-only and evidence boundary | Scenario variants |
| --- | --- | --- | --- | --- |
| CAP-QUERY | Clarification and typed query planning | Required custom capability; implementation/availability unverified | Resolve intent and required parameters; approved templates only; no self-confidence authorization. | BL-063; BL-064; BL-065; BL-066; BL-067; BL-068; BL-103; BL-069; BL-070; BL-087; BL-090; BL-091 |
| CAP-IDENTITY | User authority and source-scope verification | Existing identity controls plus reviewed extensions; financial availability unverified | Current prompting-user delegation; independent resource/cost/invoice reads; no role or credential fallback. | BL-064; BL-065; BL-103; BL-069; BL-070; BL-075; BL-082; BL-102 |
| CAP-RESOURCE | Resource inventory and lifecycle evidence | [azure-resource-lookup](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-resource-lookup) guidance plus approved ARM/ARG adapters; availability unverified | Only selected authorized resource scope; indexed/current evidence is not an atomic historical estate. | BL-071; BL-080; BL-073; BL-074; BL-076; BL-096 |
| CAP-COST | Historical costs and billing-currency evidence | [cost-analysis](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-cost/skills/cost-analysis) guidance verified; tools/hosted support unverified | Actual/amortized semantics, source-side bounded queries and explicit missing/partial evidence. | BL-066; BL-067; BL-071; BL-078; BL-073; BL-074; BL-077; BL-079; BL-081; BL-076; BL-084; BL-088; BL-089; BL-090; BL-092; BL-091; BL-095 |
| CAP-BILLING | Agreement-specific billing and invoice linkage | Required reviewed adapter capability; not supplied merely by a cost skill | Minimum separately approved agreement-specific scope; no payment, invoice edit or invoice-wide disclosure by inference. | BL-065; BL-071; BL-074; BL-082; BL-083; BL-084 |
| CAP-MONEY | Deterministic monetary and FX ledger | Required custom capability; no implementation/qualification claim | Decimal-safe signed arithmetic, currency partitioning, explicit precision and approved FX provenance; no model arithmetic. | BL-068; BL-078; BL-080; BL-077; BL-079; BL-081; BL-083; BL-093 |
| CAP-GROUNDING | Evidence lineage and factual-claim validation | Required custom capability; no zero-error certification claimed | Every factual claim/cell has validated support or a reproducible derivation; conflicts cause abstention or explicit partial coverage. | BL-063; BL-072; BL-073; BL-075; BL-082; BL-083; BL-085; BL-087; BL-098; BL-102; BL-084; BL-086; BL-088; BL-092; BL-104; BL-100; BL-101; BL-094 |
| CAP-REPORT | Private safe reports and structured extracts | Existing private-formatting work plus separately reviewed extensions; acceptance unverified | Declared schemas, escaping, output bounds and provenance; no implicit public link, mailbox or durable store. | BL-080; BL-072; BL-086 |
| CAP-FORECAST | Forecasts and hypothetical pricing | [cost-estimation](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-cost/skills/cost-estimation) guidance verified; tools/hosted support unverified | Confirm assumptions/rates/history; label predictions and intervals; never guarantee future cost or substitute retail for negotiated actuals. | BL-091; BL-097; BL-099 |
| CAP-GOVERNANCE | Configured budget and guardrail reads | [cost-governance](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-cost/skills/cost-governance) guidance verified; tools/hosted support unverified | Read-only budgets, alerts, tags and policies; create/update/recipient/threshold actions remain forbidden. | BL-090 |
| CAP-OPTIMIZE | Evidence-qualified optimization and commitments | [cost-optimization](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-cost/skills/cost-optimization) guidance verified; tools/hosted support unverified | Separate measured facts, source recommendations and hypotheses; no resize, delete, purchase, exchange or deployment. | BL-079; BL-098; BL-095; BL-096; BL-097; BL-099 |
| CAP-ALLOCATION | Business membership and denominator evidence | Required custom approved business-data capability; availability unverified | Effective-dated mappings and authorized business metrics; no inferred ownership, invented weights or hidden residuals. | BL-092; BL-093; BL-094 |
| CAP-EVALUATION | Reference corpus and quantitative qualification | Required custom evaluation capability; qualification not measured | Independent expert-adjudicated oracles, held-out cases, declared denominators/multiplicity and hard zero-error gates. | BL-102; BL-104; BL-100; BL-101 |
| CAP-REVIEW | Private human validation and escalation | Required reviewed human workflow; no new sharing integration approved | Bounded clarification, evidence-preserving private questions, human decision authority and no opinion-as-source-fact promotion. | BL-085; BL-098; BL-104; BL-100; BL-095; BL-096; BL-097; BL-099 |
| CAP-SKILLS | Skill/tool capability registry and operation allowlists | Required custom registry; catalog discovery is not installation or runtime proof | Verify supported tools/versions/permissions; no tool-name guessing, unapproved installation, financial write or scope expansion. | BL-103; BL-070; BL-087 |
| CAP-ANALYSIS | Comparable variance anomaly and economic analysis | [cost-analysis](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-cost/skills/cost-analysis) plus reviewed statistical/business contracts; availability unverified | Validate populations/baselines/denominators; an anomaly is not a cause, incident, waste finding or measured saving. | BL-088; BL-089; BL-094 |

## Routing and required parameter coverage

- Historical bill/spend investigation uses verified cost-analysis tools; a spike is not proof of cause, waste, fraud or a security incident.
- Forecasts and hypothetical pricing use separately verified cost-estimation tools. Confirm horizon, history, assumptions, rates, region/OS/tier/term, currency and the declared output type. Predictions remain uncertain.
- Configured budget/alert/tag/policy review uses the read-only subset of cost-governance. A budget is not a spending cap, and a planning target is not an Azure budget. Upstream write operations are not approved here.
- Rightsizing/idle-resource/commitment review uses cost-optimization only with utilization, pricing, existing benefit, owner and commercial constraints. Advice is conditional; no resource or commitment change is executed.
- Billing/invoice access requires reviewed agreement-specific adapters and independent minimum-scope permission proof; a subscription role or a cost skill cannot grant it.
- Monetary math, allocation/denominators, typed clarification/plans, grounding, safe presentation and statistical qualification are required capabilities, not claims that a currently installed skill implements them.

The [shared readiness contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract) defines required intent parameters, supported states and fail-closed behavior. Use verified authoritative metadata to resolve facts within an approved preflight contract, and ask targeted clarification for intent choices; never ask for secrets or manufacture unavailable source evidence.

## Installation and application boundaries

The [cost-analysis command guide](./cost-analysis-skill.md) retains the optional upstream installation command; it was not run for the local port and upstream installation remains unverified. This register itself installs no skill. The existing local pack carries the bounded guidance linked above. Catalog guidance, a local assistant skill, MCP availability, Azure permission and the hosted .NET application's implemented capability are separate facts.

Any later setup needs explicit scope/agent/tool decisions and approval. Do not copy upstream write permissions into this read-only agent, guess tool names, use another identity after denial, enable new storage/sharing APIs or replace the approved M1 source contract.

## Verified catalog references

- [cost-analysis](https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-cost/skills/cost-analysis/SKILL.md): actual spend, bill changes and AKS/AI costs, not forecasts, budgets or commitments.
- [cost-estimation](https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-cost/skills/cost-estimation/SKILL.md): forecasts and planned pricing, not configured budget health or rightsizing.
- [cost-governance](https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-cost/skills/cost-governance/SKILL.md): budgets, alerts, tags and guardrails; only approved reads are in this programme.
- [cost-optimization](https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-cost/skills/cost-optimization/SKILL.md): evidence-qualified waste/rightsizing and reservation/savings-plan analysis; recommendations only.

These are reviewed upstream descriptions from main, not pinned deployments or proof of actual tool availability. Reverify versions, source/permission contracts and qualification before use.

---

[Scenario programme](../bdd/finops-scenario-coverage.md) | [Ranked backlog](../backlog/index.md#scenario-coverage) | [Derived VoCs](../voc/index.md#scenario-coverage) | [Approved MVP scope](../iterations/iteration-0002.md#committed-scope)
