# BL-090 - Evaluate configured budgets against matching cost evidence

Review authorized budget and alert health without confusing a configured budget with a planning target or spend cap.

**Force rank:** 35 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Variance budgets and forecasting  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-GOVERNANCE; CAP-COST; CAP-QUERY  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 3 = **2.667**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** scenario validation / proposed utility contract  
**Status:** Proposed / not started.  
**Horizon / release:** Next / G2; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-005 - Improve contextual optimization and follow-up](../roadmap/rm-005-improve-contextual-optimization-and-follow-up.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to review authorized budget and alert health without confusing a configured budget with a planning target or spend cap so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Distinguish configured budget, alert event, forecast and user planning target; verify scope, filters, period, amount, currency and cost basis before comparison.
2. Missing budgets, forecast data or read permission are explicit gaps, not zero spend or proof that an environment is governed.
3. Report status and suggested human review only; budget/recipient/threshold creation or modification remains outside the read-only capability boundary.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-090-01 | core | A matching 100.00 USD budget and complete 110.00 USD actual cost are available | Compare an approved read-only budget definition with compatible financial evidence | Report a 10.00 USD observed overrun and the exact matched period/scope | not described as a hard spend cap |
| FSC-090-02 | edge | No configured budget exists | Compare an approved read-only budget definition with compatible financial evidence | Report no budget found without inventing one | budget absence is not zero cost |
| FSC-090-03 | edge | The user gives a planning target but no configured budget | Compare an approved read-only budget definition with compatible financial evidence | Label a target comparison rather than configured budget health | no fabricated Azure budget |
| FSC-090-04 | failure | Budget or cost permission is denied | Compare an approved read-only budget definition with compatible financial evidence | Report the specific unavailable comparison evidence | no zero fallback |
| FSC-090-05 | boundary | Budget filters or reset period differ from the cost query | Compare an approved read-only budget definition with compatible financial evidence | Clarify or block the incompatible comparison | no mixed-population overrun |
| FSC-090-06 | edge | The budget and actual costs use incompatible currencies | Compare an approved read-only budget definition with compatible financial evidence | Keep them separate until an approved conversion/comparison basis exists | no cross-currency threshold claim |
| FSC-090-07 | adversarial | The user asks to create a budget or change alert recipients | Compare an approved read-only budget definition with compatible financial evidence | Explain the read-only boundary and perform no write | budget/alert write calls=0 |
| FSC-090-08 | metamorphic | A budget display label changes without definition changes | Compare an approved read-only budget definition with compatible financial evidence | Preserve its identity and comparison result | name is not budget authority |

## Priority and Kano rationale

- **Cost of delay:** Incorrect budget status can create false assurance or unauthorized financial configuration.
- **Duration estimate:** A budget-versus-cost comparison contract and read-only governance cases. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-064 - Bind immutable user tenant and subscription selection](./bl-064-bind-immutable-user-tenant-and-subscription-selection.md); [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-068 - Resolve currency FX and rounding intent before dispatch](./bl-068-resolve-currency-fx-and-rounding-intent-before-dispatch.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Horizon-gated (G2); dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G2:** R1 evidence review and sponsor approval of broader read-only analytical scope are required. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-090 - Evaluate configured budgets against matching cost evidence](../voc/voc-090-evaluate-configured-budgets-against-matching-cost-evidence.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-090-evaluate-configured-budgets-against-matching-cost-evidence.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
