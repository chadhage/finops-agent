# BL-083 - Reconcile invoice components without forcing equality

Explain reconcilable resource charges, tax, credits, fees and residuals without double counting or fabricated allocation.

**Force rank:** 25 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Billing and invoice evidence  
**Parent backlog:** [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-BILLING; CAP-MONEY; CAP-GROUNDING  
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
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to explain reconcilable resource charges, tax, credits, fees and residuals without double counting or fabricated allocation so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Declare the exact comparable population, cost basis, currency, dates and source rounding rules before calculating a reconciliation difference.
2. Keep resource cost, invoice pre-tax components, tax, credits, fees, amount due and payment state distinct; an invoice total is not an extra resource charge.
3. Unmatched components and rounding/timing differences remain explicit with source-supported explanations; never insert a balancing resource, invented rate or forced-zero adjustment.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-083-01 | core | Resource charges are 20.75 USD, tax is 2.08 USD and invoice total is 22.83 USD | Compare like-for-like charge evidence with permitted invoice components | Keep the component summary separate from resource costs | resource subtotal=20.75; invoice total not added again |
| FSC-083-02 | edge | A credit exists only at invoice level without resource allocation evidence | Compare like-for-like charge evidence with permitted invoice components | Keep it separate and label the unallocated component | no proportional resource allocation guess |
| FSC-083-03 | edge | Support or marketplace fees do not map to current resources | Compare like-for-like charge evidence with permitted invoice components | Report them separately with provenance | no invented resource/group |
| FSC-083-04 | boundary | Source rounding creates a declared 0.01 USD difference | Compare like-for-like charge evidence with permitted invoice components | Show the residual and approved comparison rule | no silent balancing entry |
| FSC-083-05 | failure | Cost and invoice periods or currencies are incompatible | Compare like-for-like charge evidence with permitted invoice components | Do not calculate a misleading reconciled total | comparison blocked with reason |
| FSC-083-06 | edge | Invoice amount due differs because of payment or carried balance | Compare like-for-like charge evidence with permitted invoice components | Do not relabel amount due as period resource spend | payment/balance semantics remain separate |
| FSC-083-07 | adversarial | A user asks to make the difference zero for presentation | Compare like-for-like charge evidence with permitted invoice components | Reject the unsupported adjustment | unsupported financial adjustments=0 |
| FSC-083-08 | metamorphic | Equivalent charge partitions have the same exact total | Compare like-for-like charge evidence with permitted invoice components | Preserve the same comparable total and residual | partition-independent reconciliation |

## Priority and Kano rationale

- **Cost of delay:** Forced reconciliation hides material financial errors behind plausible totals.
- **Duration estimate:** A component ledger and exact difference/rounding/attribution fixtures. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-077 - Deduplicate charge identities without discarding legitimate charges](./bl-077-deduplicate-charge-identities-without-discarding-legitimate-charges.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); [BL-081 - Keep multi-currency and approved conversions auditable](./bl-081-keep-multi-currency-and-approved-conversions-auditable.md); [BL-082 - Verify invoice linkage and shared-invoice disclosure](./bl-082-verify-invoice-linkage-and-shared-invoice-disclosure.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-040 - Verify MCA cost visibility and permitted aggregation paths](./bl-040-verify-mca-cost-visibility-and-permitted-aggregation-paths.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-083 - Reconcile invoice components without forcing equality](../voc/voc-083-reconcile-invoice-components-without-forcing-equality.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-083-reconcile-invoice-components-without-forcing-equality.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
