# BL-064 - Bind immutable user tenant and subscription selection

Bind every plan and response to the prompting user, selected tenant and immutable authorized subscription ID.

**Force rank:** 6 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Identity and scope  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-IDENTITY; CAP-QUERY  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 2 = **5.000**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** guardrail scenario validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to bind every plan and response to the prompting user, selected tenant and immutable authorized subscription ID so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Keep user, resource tenant and subscription identifiers separate from display names, hosting context and bot credentials.
2. Resolve an ambiguous authorized selection through the user; reject an invalid or unauthorized immutable ID before resource or financial collection.
3. Changing user, tenant or selected subscription invalidates reusable query plans, source handles and private results rather than rebinding them silently.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-064-01 | core | User U1 confirms authorized tenant T1 and subscription S1 | Validate identity and selected-scope bindings before dispatch | Dispatch only S1 under U1 and T1 | all source and response bindings=(U1,T1,S1) |
| FSC-064-02 | edge | Two accessible subscriptions have the same display name | Validate identity and selected-scope bindings before dispatch | Ask for immutable-ID selection without scanning their resources | resource_dispatches=0 until explicit selection |
| FSC-064-03 | edge | A subscription is renamed after selection | Validate identity and selected-scope bindings before dispatch | Retain the same immutable S1 binding | scope unchanged; name is descriptive metadata |
| FSC-064-04 | adversarial | A valid S2 ID is supplied but S2 is not approved | Validate identity and selected-scope bindings before dispatch | Reject it without reading S2 or using an administrator identity | state=blocked; S2_dispatches=0 |
| FSC-064-05 | edge | A subscription ID is malformed or an all-zero placeholder | Validate identity and selected-scope bindings before dispatch | Return a specific invalid-scope error | business_dispatches=0 |
| FSC-064-06 | failure | A guest/resource-tenant relationship cannot be verified | Validate identity and selected-scope bindings before dispatch | Block and name the missing tenant-binding proof | no assumed cross-tenant capability |
| FSC-064-07 | boundary | The signed-in user changes from U1 to U2 during clarification | Validate identity and selected-scope bindings before dispatch | Invalidate U1's selection and request U2's own authorization | no U1 handle or result reusable by U2 |
| FSC-064-08 | metamorphic | Resource and subscription ID letter casing changes without changing identity | Validate identity and selected-scope bindings before dispatch | Resolve the same authorized identity while preserving display evidence | normalized keys equal; permissions rechecked |

## Priority and Kano rationale

- **Cost of delay:** A scope or actor mismatch can disclose another party's financial data.
- **Duration estimate:** Extend existing approved-scope contracts with explicit ambiguity and rebinding scenarios. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-038 - Confirm Zava subscription coverage using explicit IDs](./bl-038-confirm-zava-subscription-coverage-using-explicit-ids.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-050 - Preserve the local user-authenticated execution contract](./bl-050-preserve-the-local-user-authenticated-execution-contract.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-064 - Bind immutable user tenant and subscription selection](../voc/voc-064-bind-immutable-user-tenant-and-subscription-selection.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-064-bind-immutable-user-tenant-and-subscription-selection.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
