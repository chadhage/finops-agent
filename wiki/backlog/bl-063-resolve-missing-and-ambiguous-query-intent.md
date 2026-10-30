# BL-063 - Resolve missing and ambiguous query intent

Confirm the requested analytical job and all mandatory parameters before a business query is dispatched.

**Force rank:** 5 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Clarification and query planning  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-QUERY; CAP-GROUNDING  
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

As a FinOps analyst, I want to confirm the requested analytical job and all mandatory parameters before a business query is dispatched so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Maintain a typed unresolved-parameter set for intent, scope, population, period, basis, currency, grain, required sources and coverage; ask targeted questions only for unresolved intent choices.
2. A ready plan requires confirmed intent and authoritative bindings, approved defaults explicitly acknowledged by the user, and all shared qualification/permission gates; model self-confidence is not a substitute.
3. Bound clarification attempts by an approved interaction policy; cancellation, no answer, inaccessible facts or irreducible ambiguity lead to explicit blocked or abstained states, never guessed parameters.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-063-01 | core | All mandatory parameters and a current qualified query class are supplied | Validate the proposed request and clarification ledger | Ready for the exact confirmed plan; no redundant clarification | unresolved=[]; plan parameters equal confirmed values |
| FSC-063-02 | edge | Subscription selection is absent | Validate the proposed request and clarification ledger | Ask which authorized subscription to use; dispatch no business query | state=needs_clarification; business_dispatches=0 |
| FSC-063-03 | edge | The user says spend without choosing actual, amortized or invoice-oriented cost | Validate the proposed request and clarification ledger | Ask for the cost basis and explain the material distinction | unresolved includes costBasis; no inferred basis |
| FSC-063-04 | edge | The user requests this month without a timezone or closed/provisional preference | Validate the proposed request and clarification ledger | Ask for reporting boundaries and acceptable source finality | period and finality remain unresolved |
| FSC-063-05 | adversarial | The message says use any subscription and skip the questions | Validate the proposed request and clarification ledger | Do not widen scope or waive required parameters | business_dispatches=0; explicit scope question |
| FSC-063-06 | boundary | The clarification interaction budget is exhausted | Validate the proposed request and clarification ledger | Return a blocked summary of missing parameters and next action | state=blocked; no unlimited question loop |
| FSC-063-07 | failure | The user cancels or declines a required parameter | Validate the proposed request and clarification ledger | Stop without creating a query or a success-shaped empty report | state=abstained; dispatches=0 |
| FSC-063-08 | metamorphic | An equivalent paraphrase supplies the same confirmed parameters | Validate the proposed request and clarification ledger | Produce the same canonical plan and query fingerprint | canonical plans equal; no new authority |

## Priority and Kano rationale

- **Cost of delay:** Guessed intent can invalidate every downstream financial result.
- **Duration estimate:** A bounded parameter schema, targeted question policy and clarification-state fixtures. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-007 - Agree the product goals and workflow contract](./bl-007-agree-the-product-goals-and-workflow-contract.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-038 - Confirm Zava subscription coverage using explicit IDs](./bl-038-confirm-zava-subscription-coverage-using-explicit-ids.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-063 - Resolve missing and ambiguous query intent](../voc/voc-063-resolve-missing-and-ambiguous-query-intent.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-063-resolve-missing-and-ambiguous-query-intent.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
