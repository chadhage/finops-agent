# BL-088 - Explain cost variance without inventing causal explanations

Explain comparable cost changes and supported contributors without turning correlation into a claimed root cause.

**Force rank:** 33 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Variance budgets and forecasting  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-COST; CAP-ANALYSIS; CAP-GROUNDING  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 9 / 3 = **3.000**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** scenario validation / proposed utility contract  
**Status:** Proposed / not started.  
**Horizon / release:** Next / G2; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-005 - Improve contextual optimization and follow-up](../roadmap/rm-005-improve-contextual-optimization-and-follow-up.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to explain comparable cost changes and supported contributors without turning correlation into a claimed root cause so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Require comparable scope, basis, currency, charge populations, date semantics and source freshness, with explicit normalization for unequal periods where approved.
2. Show signed absolute and supported percentage changes with a valid denominator and reproducible contributor decomposition.
3. Separate observed changes from hypotheses about causes; missing activity, workload or pricing evidence must produce a question, not a confident causal narrative.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-088-01 | core | Comparable complete costs change from 100.00 to 150.00 USD | Compare approved financial populations and describe the observed variance | Report +50.00 USD and +50% with the comparable basis | difference and denominator reproduce |
| FSC-088-02 | edge | The baseline cost is zero | Compare approved financial populations and describe the observed variance | Show the absolute change and percentage unavailable under the declared definition | no divide-by-zero or invented percent |
| FSC-088-03 | edge | The baseline is negative because of a credit | Compare approved financial populations and describe the observed variance | Use an explicitly reviewed comparison definition or avoid a misleading percentage | signed context retained |
| FSC-088-04 | boundary | One period has more days than the other | Compare approved financial populations and describe the observed variance | Require declared normalization or report the comparability limit | no unqualified like-for-like growth claim |
| FSC-088-05 | failure | The current period is partial or stale | Compare approved financial populations and describe the observed variance | Do not present the difference as a complete period variance | coverage gap visible |
| FSC-088-06 | edge | A resource's charges increased but no causal workload evidence exists | Compare approved financial populations and describe the observed variance | Report the observed contributor and ask about cause | no invented deployment or demand event |
| FSC-088-07 | edge | Multiple contributors overlap in scope | Compare approved financial populations and describe the observed variance | Reconcile the decomposition without double counting | contribution totals match the defined delta |
| FSC-088-08 | metamorphic | Equivalent contributor rows are reordered | Compare approved financial populations and describe the observed variance | Preserve variance values and distinguish identical evidence from new causes | order-independent explanation |

## Priority and Kano rationale

- **Cost of delay:** Unsupported causal explanations can drive costly incorrect owner decisions.
- **Duration estimate:** A bounded variance/decomposition contract with comparability and denominator cases. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Horizon-gated (G2); dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G2:** R1 evidence review and sponsor approval of broader read-only analytical scope are required. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-011 - Expose the largest defensible report opportunities](./bl-011-expose-the-largest-defensible-report-opportunities.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-031 - Create a human review path for ambiguous optimization](./bl-031-create-a-human-review-path-for-ambiguous-optimization.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-088 - Explain cost variance without inventing causal explanations](../voc/voc-088-explain-cost-variance-without-inventing-causal-explanations.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-088-explain-cost-variance-without-inventing-causal-explanations.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
