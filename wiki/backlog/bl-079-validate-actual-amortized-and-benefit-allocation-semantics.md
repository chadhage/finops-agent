# BL-079 - Validate actual amortized and benefit-allocation semantics

Keep purchase, usage, benefit allocation and amortized evidence distinct instead of manufacturing a cost basis.

**Force rank:** 22 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Monetary correctness  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-COST; CAP-MONEY; CAP-OPTIMIZE  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 3 = **3.333**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** guardrail scenario validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-004 - Make commercial recommendations safe](../roadmap/rm-004-make-commercial-recommendations-safe.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to keep purchase, usage, benefit allocation and amortized evidence distinct instead of manufacturing a cost basis so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Use only the source-supported actual or amortized metric selected in the confirmed plan, retaining purchase/refund/usage/allocation charge semantics.
2. Do not add an upfront purchase to its amortized allocations, treat covered usage as universally free, or infer amortization by dividing a purchase without a reviewed source contract.
3. Unavailable shared-benefit or allocation evidence blocks a definitive allocation or incremental-purchase conclusion, not an assumed zero.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-079-01 | core | ActualCost is selected and the source reports an upfront purchase separately from resource usage | Validate the selected cost basis and charge population before aggregation | Report source actual charges with their distinct attribution grain | no amortized allocation added to actual purchase |
| FSC-079-02 | core | AmortizedCost is selected and an approved source supplies a 100.00 USD allocation | Validate the selected cost basis and charge population before aggregation | Use that allocation with its basis and lineage | allocation is source-supported, not guessed |
| FSC-079-03 | edge | A 1200.00 USD purchase exists without an approved amortization record | Validate the selected cost basis and charge population before aggregation | Do not invent a 100.00 monthly allocation | unsupported derived amortization blocked |
| FSC-079-04 | edge | Both purchase and corresponding amortized rows enter one proposed total | Validate the selected cost basis and charge population before aggregation | Reject the incompatible population | no actual-plus-amortized double count |
| FSC-079-05 | edge | Covered usage has zero actual cost but nonzero amortized cost | Validate the selected cost basis and charge population before aggregation | Preserve the selected metric distinction | not labeled universally free |
| FSC-079-06 | failure | Shared commitment data is inaccessible | Validate the selected cost basis and charge population before aggregation | Keep coverage/allocation unknown and block definitive advice | no zero shared-coverage fallback |
| FSC-079-07 | boundary | A refund or exchange changes a commitment charge | Validate the selected cost basis and charge population before aggregation | Use reviewed signed adjustment and period rules | no clamping or unsupported historical rewrite |
| FSC-079-08 | metamorphic | The user changes from actual to amortized basis | Validate the selected cost basis and charge population before aggregation | Create a distinct plan, query and qualification binding | old-basis totals cannot be reused as new-basis facts |

## Priority and Kano rationale

- **Cost of delay:** Mixing actual and amortized populations can double count major commitment charges.
- **Duration estimate:** Metric/grain validation over benefit, purchase and adjustment source fixtures. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-071 - Validate source schemas field capabilities and identifiers](./bl-071-validate-source-schemas-field-capabilities-and-identifiers.md); [BL-077 - Deduplicate charge identities without discarding legitimate charges](./bl-077-deduplicate-charge-identities-without-discarding-legitimate-charges.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-043 - Add authorized shared-commitment coverage evidence](./bl-043-add-authorized-shared-commitment-coverage-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-044 - Encode customer-specific commitment preference rules](./bl-044-encode-customer-specific-commitment-preference-rules.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-045 - Surface resource-change risk in commitment candidates](./bl-045-surface-resource-change-risk-in-commitment-candidates.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-079 - Validate actual amortized and benefit-allocation semantics](../voc/voc-079-validate-actual-amortized-and-benefit-allocation-semantics.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-079-validate-actual-amortized-and-benefit-allocation-semantics.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
