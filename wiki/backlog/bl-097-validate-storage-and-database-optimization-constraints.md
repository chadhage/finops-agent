# BL-097 - Validate storage and database optimization constraints

Compare storage or database alternatives using complete functional, resilience, performance and total-cost assumptions.

**Force rank:** 45 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Evidence-qualified recommendations  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-OPTIMIZE; CAP-FORECAST; CAP-REVIEW  
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
**Roadmap initiative:** [RM-005 - Improve contextual optimization and follow-up](../roadmap/rm-005-improve-contextual-optimization-and-follow-up.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to compare storage or database alternatives using complete functional, resilience, performance and total-cost assumptions so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Confirm workload access pattern, retention, recovery/replication needs, performance, compatibility, pricing/rate source and all relevant operation/egress/restore costs.
2. Distinguish a modeled alternative from observed current spend; a cheaper unit price or isolated configuration field does not prove equivalence or net saving.
3. Unknown requirements or entitlements trigger targeted owner questions or abstention; no service, tier, replication or data change is executed.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-097-01 | core | All approved functional and cost inputs support a compatible lower-cost candidate | Evaluate an approved tier/service candidate without prescribing an unsupported downgrade | Present a bounded modeled comparison with assumptions | not a measured saving or executed migration |
| FSC-097-02 | edge | Access latency or restore requirements are unknown | Evaluate an approved tier/service candidate without prescribing an unsupported downgrade | Ask before prescribing an archival or lower-performance tier | candidate blocked pending requirements |
| FSC-097-03 | edge | Replication is required for an approved recovery objective | Evaluate an approved tier/service candidate without prescribing an unsupported downgrade | Do not recommend reducing it based only on price | resilience constraint preserved |
| FSC-097-04 | boundary | Operation, restore or egress charges outweigh a unit-price reduction | Evaluate an approved tier/service candidate without prescribing an unsupported downgrade | Report the full scenario cost rather than a false saving | cost components reconcile |
| FSC-097-05 | failure | Negotiated rates or necessary usage measurements are missing | Evaluate an approved tier/service candidate without prescribing an unsupported downgrade | Label the estimate basis or abstain on a numeric comparison | no fabricated rate/usage |
| FSC-097-06 | edge | A database alternative has incompatible features or licensing assumptions | Evaluate an approved tier/service candidate without prescribing an unsupported downgrade | Expose the incompatibility and required validation | no unsupported equivalence claim |
| FSC-097-07 | adversarial | The user asks to apply the tier or schema change | Evaluate an approved tier/service candidate without prescribing an unsupported downgrade | Stay read-only and preserve the owner/deployment boundary | service/data writes=0 |
| FSC-097-08 | metamorphic | The same approved inputs are expressed in equivalent units | Evaluate an approved tier/service candidate without prescribing an unsupported downgrade | Return equivalent total-scenario economics after declared unit conversion | no unit-conversion saving artifact |

## Priority and Kano rationale

- **Cost of delay:** A superficially cheaper tier can be functionally wrong or more expensive overall.
- **Duration estimate:** Service-specific constraint and total-scenario-cost validation cases. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); [BL-096 - Ground rightsizing and idle-resource advice in workload evidence](./bl-096-ground-rightsizing-and-idle-resource-advice-in-workload-evidence.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Horizon-gated (G2); dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G2:** R1 evidence review and sponsor approval of broader read-only analytical scope are required. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-032 - Assess storage tier and replication fit before savings advice](./bl-032-assess-storage-tier-and-replication-fit-before-savings-advice.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-033 - Prototype configuration-defect versus unused-resource diagnosis](./bl-033-prototype-configuration-defect-versus-unused-resource-diagnosis.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-034 - Require owner validation for fix-versus-delete decisions](./bl-034-require-owner-validation-for-fix-versus-delete-decisions.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-035 - Prototype evidence-qualified cheaper-service candidates](./bl-035-prototype-evidence-qualified-cheaper-service-candidates.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-097 - Validate storage and database optimization constraints](../voc/voc-097-validate-storage-and-database-optimization-constraints.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-097-validate-storage-and-database-optimization-constraints.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
