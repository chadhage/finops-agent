# BL-070 - Validate typed read-only query plans and tool destinations

Dispatch only a typed, approved, read-only plan whose destinations and parameters match confirmed intent and authority.

**Force rank:** 16 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Query and tool integrity  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-QUERY; CAP-IDENTITY; CAP-SKILLS  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 3 = **3.333**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** guardrail scenario validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to dispatch only a typed, approved, read-only plan whose destinations and parameters match confirmed intent and authority so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Validate operation, endpoint, API/schema version, required fields, scoped parameters, query-template fingerprint, output contract and approved execution bounds before dispatch.
2. Treat user/retrieved query text as untrusted input; bind values through approved templates and reject unsupported operators, destinations or write operations.
3. Qualification and permission evidence must match the exact query class and versions; syntactic validity alone does not establish semantic accuracy or completeness.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-070-01 | core | A fully confirmed plan matches an approved read-only template and current qualification | Compile and validate a prepared query against its source/tool contract | Dispatch the exact plan within its approved bounds | operation, scope and fingerprint equal approved values |
| FSC-070-02 | adversarial | The prompt supplies a different executable KQL or shell command | Compile and validate a prepared query against its source/tool contract | Reject replacement of the template contract | unapproved command dispatches=0 |
| FSC-070-03 | edge | A syntactically valid query projects an unsupported financial field from inventory | Compile and validate a prepared query against its source/tool contract | Reject semantic/source-schema mismatch | no invented billed-cost field |
| FSC-070-04 | adversarial | A continuation redirects credentials to a different host | Compile and validate a prepared query against its source/tool contract | Reject it before token transmission | foreign-host token sends=0 |
| FSC-070-05 | boundary | A plan exceeds the approved row, byte, page or time budget | Compile and validate a prepared query against its source/tool contract | Block or use an explicitly reviewed bounded plan | no unlimited execution fallback |
| FSC-070-06 | failure | The query class has no current qualification artifact | Compile and validate a prepared query against its source/tool contract | Do not label or dispatch it as 99%-qualified | state=blocked; qualification gap identified |
| FSC-070-07 | adversarial | A budget or optimization tool exposes a write operation | Compile and validate a prepared query against its source/tool contract | Reject the write in the read-only capability boundary | create/update/delete/purchase calls=0 |
| FSC-070-08 | metamorphic | Irrelevant natural-language whitespace changes | Compile and validate a prepared query against its source/tool contract | Retain the same canonical typed plan and fingerprint | no unreviewed template mutation |

## Priority and Kano rationale

- **Cost of delay:** An unconstrained query can leak scope or produce plausible but semantically wrong results.
- **Duration estimate:** Cross-source typed-plan, allowlist and negative template-contract checks. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); [BL-064 - Bind immutable user tenant and subscription selection](./bl-064-bind-immutable-user-tenant-and-subscription-selection.md); [BL-065 - Resolve billing agreement and minimum invoice scope](./bl-065-resolve-billing-agreement-and-minimum-invoice-scope.md); [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-068 - Resolve currency FX and rounding intent before dispatch](./bl-068-resolve-currency-fx-and-rounding-intent-before-dispatch.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-050 - Preserve the local user-authenticated execution contract](./bl-050-preserve-the-local-user-authenticated-execution-contract.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-070 - Validate typed read-only query plans and tool destinations](../voc/voc-070-validate-typed-read-only-query-plans-and-tool-destinations.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-070-validate-typed-read-only-query-plans-and-tool-destinations.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
