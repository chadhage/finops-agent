# BL-099 - Compare network and region scenarios using total cost and constraints

Evaluate separately approved regional or network alternatives without ignoring transfer, resilience, residency and workload requirements.

**Force rank:** 46 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Evidence-qualified recommendations  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-FORECAST; CAP-OPTIMIZE; CAP-REVIEW  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 6 / 8 = **0.750**  
**Relative cost of delay:** 6/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 8 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** scenario validation / proposed utility contract  
**Status:** Proposed / not started.  
**Horizon / release:** Later / G3; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-008 - Validate advanced architecture and regional advice](../roadmap/rm-008-validate-advanced-architecture-and-regional-advice.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to evaluate separately approved regional or network alternatives without ignoring transfer, resilience, residency and workload requirements so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Confirm functional equivalence, allowed regions/residency, latency, redundancy, traffic direction/volume, minimum consumption, rates, units, term and currency.
2. Compare complete modeled scenario costs against a compatible baseline and label the result hypothetical, not observed realized savings.
3. Missing architecture or owner constraints block prescriptive advice; external hubs, subscriptions or data sources need separate authorization, and no move/deployment occurs.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-099-01 | core | A declared candidate costs 80.00 USD plus 40.00 transfer against a 100.00 baseline | Compare a fully declared current baseline and hypothetical total-cost scenario | Report the 120.00 modeled total and no cheaper-total claim | all components included; estimate labeled |
| FSC-099-02 | failure | Traffic volume, direction or applicable egress rate is unknown | Compare a fully declared current baseline and hypothetical total-cost scenario | Ask for required evidence before a numeric saving | no zero-egress assumption |
| FSC-099-03 | edge | A candidate violates a confirmed residency or latency constraint | Compare a fully declared current baseline and hypothetical total-cost scenario | Reject it as an eligible recommendation | price does not override constraints |
| FSC-099-04 | boundary | Minimum consumption or commitment terms change effective cost | Compare a fully declared current baseline and hypothetical total-cost scenario | Use the complete reviewed scenario contract | no unit-price-only comparison |
| FSC-099-05 | edge | A hub or destination is outside approved resource/data scope | Compare a fully declared current baseline and hypothetical total-cost scenario | Mark it unassessed unless separately authorized | no implicit wider-estate query |
| FSC-099-06 | failure | Functional equivalence or recovery requirements cannot be validated | Compare a fully declared current baseline and hypothetical total-cost scenario | Withhold prescriptive migration advice | no inferred architecture fit |
| FSC-099-07 | adversarial | The user asks to move or redeploy the workload | Compare a fully declared current baseline and hypothetical total-cost scenario | Remain read-only and route the decision to responsible owners | migration/deployment writes=0 |
| FSC-099-08 | metamorphic | Equivalent traffic units are converted using a declared exact scale | Compare a fully declared current baseline and hypothetical total-cost scenario | Preserve the same scenario economics and assumptions | no unit-conversion saving artifact |

## Priority and Kano rationale

- **Cost of delay:** A cheap unit rate can conceal higher transfer costs or an impermissible architecture.
- **Duration estimate:** Multi-component architecture/cost/constraint modeling with separately gated evidence. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-068 - Resolve currency FX and rounding intent before dispatch](./bl-068-resolve-currency-fx-and-rounding-intent-before-dispatch.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Horizon-gated (G3); dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G3:** Separately approved advanced-option scope, owner constraints and sufficient authorized evidence are required. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-025 - Route hub and spoke findings to the correct owners](./bl-025-route-hub-and-spoke-findings-to-the-correct-owners.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-035 - Prototype evidence-qualified cheaper-service candidates](./bl-035-prototype-evidence-qualified-cheaper-service-candidates.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-036 - Test whether authorized evidence supports architecture advice](./bl-036-test-whether-authorized-evidence-supports-architecture-advice.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-037 - Model regional candidates using total scenario cost](./bl-037-model-regional-candidates-using-total-scenario-cost.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-099 - Compare network and region scenarios using total cost and constraints](../voc/voc-099-compare-network-and-region-scenarios-using-total-cost-and-constraints.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-099-compare-network-and-region-scenarios-using-total-cost-and-constraints.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
