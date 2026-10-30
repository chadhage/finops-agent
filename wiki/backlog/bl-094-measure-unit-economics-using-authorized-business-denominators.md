# BL-094 - Measure unit economics using authorized business denominators

Calculate defensible cost-per-business-unit metrics only when cost and business populations are authorized and comparable.

**Force rank:** 44 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Allocation and unit economics  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-ALLOCATION; CAP-ANALYSIS; CAP-GROUNDING  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 7 / 5 = **1.400**  
**Relative cost of delay:** 7/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** scenario validation / proposed utility contract  
**Status:** Proposed / not started.  
**Horizon / release:** Next / G2; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-006 - Support business cost and portfolio decisions](../roadmap/rm-006-support-business-cost-and-portfolio-decisions.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to calculate defensible cost-per-business-unit metrics only when cost and business populations are authorized and comparable so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Confirm business metric definition, source permission, unit, period, population, exclusions and matching cost allocation before calculating.
2. Use decimal-safe ratios with declared per-unit precision; denominator zero, missing, sampled or mismatched evidence cannot become a precise unit cost.
3. Separate observed unit economics from ROI, business value and efficiency hypotheses; no revenue, transaction volume or saving is invented.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-094-01 | core | Comparable authorized cost is 100.00 USD and volume is 1000 requests | Validate numerator/denominator provenance and compute a declared unit metric | Report 0.10 USD per request with both source populations | numerator/denominator/period lineage retained |
| FSC-094-02 | boundary | Business volume is zero | Validate numerator/denominator provenance and compute a declared unit metric | Return an undefined/unavailable ratio under the declared rule | no divide-by-zero or zero-cost claim |
| FSC-094-03 | failure | The business source or required metric is unavailable | Validate numerator/denominator provenance and compute a declared unit metric | Withhold the ratio and identify missing evidence | no estimated business volume presented as observed |
| FSC-094-04 | edge | Business events and cost use different periods or populations | Validate numerator/denominator provenance and compute a declared unit metric | Block or explicitly qualify the incompatible comparison | no apples-to-oranges ratio |
| FSC-094-05 | edge | The business metric is sampled rather than complete | Validate numerator/denominator provenance and compute a declared unit metric | Retain its sampling/uncertainty status and require the approved method | no false exact denominator |
| FSC-094-06 | edge | Per-request cost needs sub-cent display precision | Validate numerator/denominator provenance and compute a declared unit metric | Use the declared per-unit policy rather than rounding every value to cents | meaningful precision retained |
| FSC-094-07 | adversarial | The user asks for ROI without authorized revenue/value evidence | Validate numerator/denominator provenance and compute a declared unit metric | Ask for the necessary basis or abstain on ROI | no invented benefit or profit |
| FSC-094-08 | metamorphic | Equivalent business units are converted through an approved exact scale | Validate numerator/denominator provenance and compute a declared unit metric | Preserve the same economic meaning and show the unit conversion | no denominator identity change |

## Priority and Kano rationale

- **Cost of delay:** An invented denominator can make correct cloud costs support a false business claim.
- **Duration estimate:** Authorized business-data joins and denominator/ratio validation contracts. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); [BL-092 - Allocate costs through validated business membership](./bl-092-allocate-costs-through-validated-business-membership.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Horizon-gated (G2); dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G2:** R1 evidence review and sponsor approval of broader read-only analytical scope are required. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-039 - Resolve business cost groups from application-service mappings](./bl-039-resolve-business-cost-groups-from-application-service-mappings.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-058 - Validate a separately authorized second operating profile](./bl-058-validate-a-separately-authorized-second-operating-profile.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-094 - Measure unit economics using authorized business denominators](../voc/voc-094-measure-unit-economics-using-authorized-business-denominators.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-094-measure-unit-economics-using-authorized-business-denominators.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
