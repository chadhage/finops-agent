# BL-068 - Resolve currency FX and rounding intent before dispatch

Clarify currency and conversion intent without using locale, resource location or invoice context as a guessed currency.

**Force rank:** 10 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Clarification and query planning  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-QUERY; CAP-MONEY  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 2 = **5.000**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** guardrail scenario validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to clarify currency and conversion intent without using locale, resource location or invoice context as a guessed currency so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Default to neither USD nor a user's locale; obtain billing currency from authoritative records and ask whether original-currency partitions or an explicit conversion are intended.
2. A conversion requires approved rate source, base/quote direction, rate date, rate type, precision and rounding policy; absence blocks converted totals.
3. Preserve original amounts/currencies alongside any separately approved derived presentation, and never describe conversion as an observed source charge.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-068-01 | core | The user confirms original billing currencies with no conversion | Validate currency provenance and any proposed conversion contract | Keep separate currency partitions | conversion_calls=0; original amounts retained |
| FSC-068-02 | edge | A cost amount has no currency while the user's locale is USD | Validate currency provenance and any proposed conversion contract | Report missing currency, not USD | currency=Unavailable; no invented code |
| FSC-068-03 | edge | A single common-currency total is requested without an FX basis | Validate currency provenance and any proposed conversion contract | Ask for source, date and direction before conversion | converted total blocked |
| FSC-068-04 | boundary | USD/EUR and EUR/USD rates could both be selected | Validate currency provenance and any proposed conversion contract | Require the approved direction explicitly | rate direction recorded in the plan |
| FSC-068-05 | edge | A monthly average and a spot rate would yield different totals | Validate currency provenance and any proposed conversion contract | Ask which approved rate type applies | no silent rate-type choice |
| FSC-068-06 | failure | The approved rate source is unavailable | Validate currency provenance and any proposed conversion contract | Keep original-currency output or block conversion visibly | no cached/guessed fallback rate |
| FSC-068-07 | boundary | The currency uses zero or three minor units | Validate currency provenance and any proposed conversion contract | Apply only the agreed presentation policy after full-precision calculation | no universal two-decimal assumption |
| FSC-068-08 | metamorphic | The display locale changes but the financial intent does not | Validate currency provenance and any proposed conversion contract | Change formatting only, not amount or currency identity | financial values and source codes unchanged |

## Priority and Kano rationale

- **Cost of delay:** A guessed currency or inverted exchange rate creates materially false totals.
- **Duration estimate:** A finite conversion-parameter schema and no-default monetary-intent checks. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-068 - Resolve currency FX and rounding intent before dispatch](../voc/voc-068-resolve-currency-fx-and-rounding-intent-before-dispatch.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-068-resolve-currency-fx-and-rounding-intent-before-dispatch.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
