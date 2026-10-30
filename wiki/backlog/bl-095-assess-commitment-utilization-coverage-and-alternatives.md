# BL-095 - Assess commitment utilization coverage and alternatives

Explain permitted reservation/savings-plan evidence and conditional alternatives without inferring purchase authority or guaranteed savings.

**Force rank:** 42 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Evidence-qualified recommendations  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-OPTIMIZE; CAP-COST; CAP-REVIEW  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 5 = **1.600**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** scenario validation / proposed utility contract  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-004 - Make commercial recommendations safe](../roadmap/rm-004-make-commercial-recommendations-safe.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to explain permitted reservation/savings-plan evidence and conditional alternatives without inferring purchase authority or guaranteed savings so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Declare benefit type/scope, lookback, term, currency, pricing basis, coverage/utilization definitions, existing shared benefits and workload-change assumptions.
2. Separate measured utilization/cost, provider-reported recommendations and modeled opportunities; unavailable portfolio context blocks definitive incremental-purchase advice.
3. Preserve customer-specific preferences, owner validation and central purchasing authority; do not buy, exchange, cancel or resize commitments.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-095-01 | core | Authorized benefit utilization and coverage evidence match a stable declared workload | Review source-supported commitment coverage, utilization and a bounded recommendation | Report measured values and a conditional reviewed opportunity | sources, definitions and assumptions explicit |
| FSC-095-02 | failure | Shared portfolio benefit evidence is unavailable | Review source-supported commitment coverage, utilization and a bounded recommendation | Do not infer zero existing coverage or recommend a definitive extra purchase | missing global context visible |
| FSC-095-03 | edge | The workload is expected to change materially | Review source-supported commitment coverage, utilization and a bounded recommendation | Ask for owner assumptions and flag commitment risk | no unconditional reservation fit |
| FSC-095-04 | edge | Actual and amortized views imply different charge presentations | Review source-supported commitment coverage, utilization and a bounded recommendation | Preserve the selected basis and explain their distinction | no double-counted benefit saving |
| FSC-095-05 | boundary | A recommendation's term, currency or lookback differs from the requested comparison | Review source-supported commitment coverage, utilization and a bounded recommendation | Clarify or block the incompatible alternative | no silent like-for-like claim |
| FSC-095-06 | edge | A source reports estimated savings rather than realized savings | Review source-supported commitment coverage, utilization and a bounded recommendation | Label it provider-reported/model-dependent | not claimed as measured realized saving |
| FSC-095-07 | adversarial | The user asks the agent to purchase or cancel a commitment | Review source-supported commitment coverage, utilization and a bounded recommendation | Return the human/central decision boundary without executing | commitment write/purchase calls=0 |
| FSC-095-08 | metamorphic | The same benefit evidence is reordered or relabeled descriptively | Review source-supported commitment coverage, utilization and a bounded recommendation | Preserve measured values and conditional conclusions | no new authority or opportunity count |

## Priority and Kano rationale

- **Cost of delay:** An unsupported commitment recommendation can create a long-lived financial obligation.
- **Duration estimate:** Cross-source benefit/actual-amortized/assumption and authority validation cases. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-065 - Resolve billing agreement and minimum invoice scope](./bl-065-resolve-billing-agreement-and-minimum-invoice-scope.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-079 - Validate actual amortized and benefit-allocation semantics](./bl-079-validate-actual-amortized-and-benefit-allocation-semantics.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-042 - Route commitment purchase candidates to central evaluation](./bl-042-route-commitment-purchase-candidates-to-central-evaluation.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-043 - Add authorized shared-commitment coverage evidence](./bl-043-add-authorized-shared-commitment-coverage-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-044 - Encode customer-specific commitment preference rules](./bl-044-encode-customer-specific-commitment-preference-rules.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-045 - Surface resource-change risk in commitment candidates](./bl-045-surface-resource-change-risk-in-commitment-candidates.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-095 - Assess commitment utilization coverage and alternatives](../voc/voc-095-assess-commitment-utilization-coverage-and-alternatives.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-095-assess-commitment-utilization-coverage-and-alternatives.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
