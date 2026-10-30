# BL-075 - Preserve authority and privacy across source and session changes

Keep resource, cost and invoice evidence private and currently authorized throughout clarification, collection and reuse.

**Force rank:** 20 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Identity and scope  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-IDENTITY; CAP-GROUNDING  
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

As a FinOps analyst, I want to keep resource, cost and invoice evidence private and currently authorized throughout clarification, collection and reuse so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Validate each source's current approved capability and the same prompting-user/tenant/session/scope binding; one source's permission does not authorize another.
2. Known sign-out, expiry, revocation or denial invalidates affected reusable plans/evidence; no bot, developer CLI, app-only or administrator fallback repairs access.
3. Shared-channel requests require an authorized same-user private continuation; redact credentials and raw sensitive provider payloads from user errors and audit logs.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-075-01 | core | U1 has independently valid inventory, cost and invoice reads for the approved scopes | Validate current authority and private delivery at a source/session transition | Use those capabilities and deliver only to U1's private context | actor and source scopes remain bound |
| FSC-075-02 | edge | A shared channel requests U1's invoice details | Validate current authority and private delivery at a source/session transition | Offer a bound private continuation without publishing financial rows | shared disclosure count=0 |
| FSC-075-03 | failure | Invoice permission is denied while cost access remains valid | Validate current authority and private delivery at a source/session transition | Preserve only still-authorized cost evidence and show the invoice gap | no inferred invoice authority |
| FSC-075-04 | boundary | Sign-out occurs after collection but before reuse | Validate current authority and private delivery at a source/session transition | Invalidate reusable context and require fresh authorization | old handles cannot authorize output |
| FSC-075-05 | adversarial | A bot or developer credential is available after user OBO fails | Validate current authority and private delivery at a source/session transition | Do not fall back to it | business fallback credentials used=0 |
| FSC-075-06 | failure | A known revocation invalidates one required source | Validate current authority and private delivery at a source/session transition | Block or explicitly mark affected coverage without pretending instantaneous detection elsewhere | known invalidation honored |
| FSC-075-07 | edge | A provider error contains a token or sensitive raw billing payload | Validate current authority and private delivery at a source/session transition | Return a safe code/correlation and redact sensitive content | no credential/raw-payload disclosure |
| FSC-075-08 | metamorphic | U2 requests the same textual query as U1 | Validate current authority and private delivery at a source/session transition | Create U2's separate authorized plan rather than reusing U1 state | no cross-user result or scope reuse |

## Priority and Kano rationale

- **Cost of delay:** Correct cost figures still constitute a serious failure if disclosed to an unauthorized actor.
- **Duration estimate:** Cross-source authority/lifetime and private-delivery regression contracts. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-064 - Bind immutable user tenant and subscription selection](./bl-064-bind-immutable-user-tenant-and-subscription-selection.md); [BL-065 - Resolve billing agreement and minimum invoice scope](./bl-065-resolve-billing-agreement-and-minimum-invoice-scope.md); [BL-069 - Invalidate stale or contradictory clarification state](./bl-069-invalidate-stale-or-contradictory-clarification-state.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-050 - Preserve the local user-authenticated execution contract](./bl-050-preserve-the-local-user-authenticated-execution-contract.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-075 - Preserve authority and privacy across source and session changes](../voc/voc-075-preserve-authority-and-privacy-across-source-and-session-changes.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-075-preserve-authority-and-privacy-across-source-and-session-changes.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
