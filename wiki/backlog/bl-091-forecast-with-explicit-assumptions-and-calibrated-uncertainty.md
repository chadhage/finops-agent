# BL-091 - Forecast with explicit assumptions and calibrated uncertainty

Offer source-supported forecasts and what-if estimates without presenting future costs as observed or guaranteed facts.

**Force rank:** 40 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Variance budgets and forecasting  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-FORECAST; CAP-COST; CAP-QUERY  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 5 = **1.600**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** scenario validation / proposed utility contract  
**Status:** Proposed / not started.  
**Horizon / release:** Next / G2; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-005 - Improve contextual optimization and follow-up](../roadmap/rm-005-improve-contextual-optimization-and-follow-up.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to offer source-supported forecasts and what-if estimates without presenting future costs as observed or guaranteed facts so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Clarify forecast versus hypothetical pricing, horizon, history, scope, units, currency, assumptions and approved model/rate sources.
2. Label point predictions, source-supported prediction intervals, confidence level and limitations accurately; a query-quality 99% target is not a guarantee of future spend.
3. Insufficient history, missing inputs, regime changes or unsupported intervals produce a visible limitation or abstention, never model-invented forecasts, rates or certainty.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-091-01 | core | A supported forecast returns a point estimate and declared prediction interval | Validate and present an approved forecast or hypothetical pricing scenario | Display the forecast type, level, currency, horizon and source assumptions | prediction is not an observed invoice or guarantee |
| FSC-091-02 | failure | History is insufficient for the approved forecasting contract | Validate and present an approved forecast or hypothetical pricing scenario | Explain the missing history and withhold unsupported numbers | no invented trend |
| FSC-091-03 | edge | The user asks how much a proposed workload will cost | Validate and present an approved forecast or hypothetical pricing scenario | Clarify hypothetical usage, region, OS/tier/term and rate basis | not mislabeled as an existing-spend forecast |
| FSC-091-04 | edge | The source supplies a 95% interval but the user asks for 99% | Validate and present an approved forecast or hypothetical pricing scenario | Do not relabel or extrapolate the interval without a supported method | interval level remains source-supported |
| FSC-091-05 | boundary | A material workload or pricing change breaks historical comparability | Validate and present an approved forecast or hypothetical pricing scenario | Record the scenario or require revalidation | no stale model certainty |
| FSC-091-06 | edge | A negotiated pricesheet is unavailable but retail prices exist | Validate and present an approved forecast or hypothetical pricing scenario | Label a separately approved retail estimate or abstain on negotiated cost | no retail-as-contract-rate claim |
| FSC-091-07 | adversarial | The user demands 99% certainty about future demand | Validate and present an approved forecast or hypothetical pricing scenario | Explain irreducible uncertainty and refuse a guarantee | query readiness is not future-outcome certainty |
| FSC-091-08 | metamorphic | Only display locale changes for the same forecast inputs | Validate and present an approved forecast or hypothetical pricing scenario | Preserve forecast values, source interval and assumptions | no financial/model change from formatting |

## Priority and Kano rationale

- **Cost of delay:** An unlabeled or fabricated forecast can be mistaken for an actionable financial commitment.
- **Duration estimate:** Forecast eligibility, uncertainty/backtesting and what-if assumption contracts. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-068 - Resolve currency FX and rounding intent before dispatch](./bl-068-resolve-currency-fx-and-rounding-intent-before-dispatch.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Horizon-gated (G2); dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G2:** R1 evidence review and sponsor approval of broader read-only analytical scope are required. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-037 - Model regional candidates using total scenario cost](./bl-037-model-regional-candidates-using-total-scenario-cost.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-056 - Clarify future per-policy exception handoff](./bl-056-clarify-future-per-policy-exception-handoff.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-091 - Forecast with explicit assumptions and calibrated uncertainty](../voc/voc-091-forecast-with-explicit-assumptions-and-calibrated-uncertainty.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-091-forecast-with-explicit-assumptions-and-calibrated-uncertainty.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
