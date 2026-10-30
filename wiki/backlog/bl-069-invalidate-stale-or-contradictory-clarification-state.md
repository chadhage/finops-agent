# BL-069 - Invalidate stale or contradictory clarification state

Keep the confirmed query ledger consistent across multi-turn clarification, cancellation and scope changes.

**Force rank:** 14 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Clarification and query planning  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-QUERY; CAP-IDENTITY  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 2 = **4.500**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** guardrail scenario validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to keep the confirmed query ledger consistent across multi-turn clarification, cancellation and scope changes so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Store parameter values, origin, confirmation state, actor/scope binding and plan revision; a changed material parameter invalidates the prior prepared plan.
2. Contradictory answers trigger a focused clarification rather than silently choosing the latest convenient interpretation or merging incompatible requests.
3. Expired, cancelled or cross-user clarification state cannot be restored from conversational text or used as authority.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-069-01 | core | U1 confirms a previously missing cost basis for plan revision 1 | Apply a new user answer to the bound clarification ledger | Create revision 2 with that field resolved and other verified fields retained | revision advances; provenance retained |
| FSC-069-02 | edge | The user changes S1 to S2 after confirming the period | Apply a new user answer to the bound clarification ledger | Invalidate scope-dependent permissions, sources and query fingerprint | old prepared query cannot dispatch |
| FSC-069-03 | edge | The user gives mutually inconsistent period answers | Apply a new user answer to the bound clarification ledger | Ask which period to retain | no silent precedence or union |
| FSC-069-04 | boundary | A stale answer arrives after a newer revision | Apply a new user answer to the bound clarification ledger | Reject or explicitly reconcile the stale update | no rollback of confirmed parameters |
| FSC-069-05 | failure | The session expires during clarification | Apply a new user answer to the bound clarification ledger | Require fresh authorization and re-entry as needed | expired ledger not executable |
| FSC-069-06 | adversarial | U2 supplies a handle copied from U1's conversation | Apply a new user answer to the bound clarification ledger | Reject cross-user state use | no U1 data or plan disclosed |
| FSC-069-07 | edge | The user cancels and then asks continue without rebinding | Apply a new user answer to the bound clarification ledger | Explain the lost/cancelled state and request required confirmations | no resurrection from message history |
| FSC-069-08 | metamorphic | The same confirmed answer is delivered twice | Apply a new user answer to the bound clarification ledger | Apply it idempotently without extra dispatch | one logical revision; no duplicate query |

## Priority and Kano rationale

- **Cost of delay:** A stale answer can send a technically valid query for the wrong financial job.
- **Duration estimate:** State-transition and revision checks over the typed clarification contract. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); [BL-064 - Bind immutable user tenant and subscription selection](./bl-064-bind-immutable-user-tenant-and-subscription-selection.md); [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-068 - Resolve currency FX and rounding intent before dispatch](./bl-068-resolve-currency-fx-and-rounding-intent-before-dispatch.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-069 - Invalidate stale or contradictory clarification state](../voc/voc-069-invalidate-stale-or-contradictory-clarification-state.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-069-invalidate-stale-or-contradictory-clarification-state.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
