# BL-089 - Detect anomalies only against comparable sufficient baselines

Identify source-supported unusual spend while separating anomaly scores, billing artifacts and confirmed incidents.

**Force rank:** 34 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Variance budgets and forecasting  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-COST; CAP-ANALYSIS  
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

As a FinOps analyst, I want to identify source-supported unusual spend while separating anomaly scores, billing artifacts and confirmed incidents so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Record baseline length, seasonality, granularity, scope/basis/currency, missing data and approved model/threshold provenance; do not fabricate production defaults.
2. Label an anomaly as a method-relative signal, not waste, fraud, an outage or a causal incident; expose contributing evidence and validation questions.
3. Data lag, refunds, new resources, billing corrections and regime changes must be considered before stronger conclusions or an all-clear statement.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-089-01 | core | A complete comparable series exceeds the approved anomaly threshold | Evaluate an approved anomaly method against its declared historical population | Report the signal, method, baseline and supported contributors | not labeled confirmed waste or incident |
| FSC-089-02 | failure | History is shorter than the approved requirement | Evaluate an approved anomaly method against its declared historical population | Return insufficient-history evidence rather than a score | no fabricated baseline |
| FSC-089-03 | edge | A weekly seasonal peak is expected under the approved method | Evaluate an approved anomaly method against its declared historical population | Apply the declared seasonal treatment | no naive daily comparison masquerading as calibrated detection |
| FSC-089-04 | edge | A refund or rebill creates a large signed change | Evaluate an approved anomaly method against its declared historical population | Expose the financial artifact before inferring operational cause | charge semantics retained |
| FSC-089-05 | boundary | A new resource has no historical baseline | Evaluate an approved anomaly method against its declared historical population | Report a new-population limitation | no invented zero-cost history |
| FSC-089-06 | failure | Missing days or ingestion lag distort the series | Evaluate an approved anomaly method against its declared historical population | Block a definitive signal/all-clear claim | missing values not filled with zero silently |
| FSC-089-07 | edge | A legitimate workload regime change invalidates prior calibration | Evaluate an approved anomaly method against its declared historical population | Request revalidation or label the method limitation | no stale anomaly certification |
| FSC-089-08 | metamorphic | The same baseline is presented in an equivalent approved partition | Evaluate an approved anomaly method against its declared historical population | Preserve the declared signal and evidence semantics | no unexplained score change from row order |

## Priority and Kano rationale

- **Cost of delay:** False anomaly and all-clear claims undermine human analyst trust.
- **Duration estimate:** An anomaly/baseline eligibility contract over validated cost series. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); [BL-088 - Explain cost variance without inventing causal explanations](./bl-088-explain-cost-variance-without-inventing-causal-explanations.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Horizon-gated (G2); dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G2:** R1 evidence review and sponsor approval of broader read-only analytical scope are required. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-030 - Design bounded repeat follow-up for obvious waste](./bl-030-design-bounded-repeat-follow-up-for-obvious-waste.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-031 - Create a human review path for ambiguous optimization](./bl-031-create-a-human-review-path-for-ambiguous-optimization.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-089 - Detect anomalies only against comparable sufficient baselines](../voc/voc-089-detect-anomalies-only-against-comparable-sufficient-baselines.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-089-detect-anomalies-only-against-comparable-sufficient-baselines.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
