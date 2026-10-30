# BL-081 - Keep multi-currency and approved conversions auditable

Retain original monetary evidence and verify any explicitly approved FX-derived presentation independently.

**Force rank:** 23 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Monetary correctness  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-MONEY; CAP-COST  
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

As a FinOps analyst, I want to retain original monetary evidence and verify any explicitly approved FX-derived presentation independently so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Partition original costs by authoritative billing currency and retain original values even when a converted presentation is separately authorized.
2. Validate rate source, time, direction, precision, coverage and rounding against the confirmed plan; currencies cannot be inferred from resource region or profile context.
3. Converted amounts are labeled derived estimates/presentation values as appropriate, never observed billing charges or proof of invoice reconciliation.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-081-01 | core | A group has 10.00 USD and 5.00 EUR costs with no conversion approval | Partition monetary results and validate an optional conversion derivation | Return separate USD and EUR subtotals | no 15.00 unlabeled total |
| FSC-081-02 | core | 100.00 EUR is converted with an approved rate of 1.10 USD per EUR | Partition monetary results and validate an optional conversion derivation | Show original 100.00 EUR and derived 110.00 USD with rate lineage | direction and decimal calculation verified |
| FSC-081-03 | edge | The supplied rate is EUR per USD rather than USD per EUR | Partition monetary results and validate an optional conversion derivation | Reject the incompatible direction or ask for confirmation | no inverted-rate arithmetic |
| FSC-081-04 | failure | A required rate date or source proof is missing | Partition monetary results and validate an optional conversion derivation | Block converted output while retaining original currencies | no rate guess |
| FSC-081-05 | edge | The invoice is USD but a linked record claims a conflicting billing currency | Partition monetary results and validate an optional conversion derivation | Flag the mismatch and do not manufacture reconciliation | currency disagreement remains visible |
| FSC-081-06 | boundary | A rate changes within the reporting period | Partition monetary results and validate an optional conversion derivation | Use only the approved temporal conversion policy | no silent average or spot selection |
| FSC-081-07 | edge | A profile currency is known but a charge currency is absent | Partition monetary results and validate an optional conversion derivation | Keep that charge's currency unavailable | profile currency does not fill missing charge evidence |
| FSC-081-08 | metamorphic | The display currency or locale is changed | Partition monetary results and validate an optional conversion derivation | Require a new conversion plan where needed and preserve original source totals | original-currency evidence remains unchanged |

## Priority and Kano rationale

- **Cost of delay:** Currency mixing and hidden conversion can make otherwise accurate cost data misleading.
- **Duration estimate:** Currency partitioning and traceable FX derivation/exception contracts. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-068 - Resolve currency FX and rounding intent before dispatch](./bl-068-resolve-currency-fx-and-rounding-intent-before-dispatch.md); [BL-071 - Validate source schemas field capabilities and identifiers](./bl-071-validate-source-schemas-field-capabilities-and-identifiers.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-081 - Keep multi-currency and approved conversions auditable](../voc/voc-081-keep-multi-currency-and-approved-conversions-auditable.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-081-keep-multi-currency-and-approved-conversions-auditable.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
