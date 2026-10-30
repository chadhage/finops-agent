# BL-067 - Confirm cost basis units and aggregation grain

Agree on the cost definition, units, charge population and output grain before any financial result is calculated.

**Force rank:** 9 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Clarification and query planning  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-QUERY; CAP-COST  
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

As a FinOps analyst, I want to agree on the cost definition, units, charge population and output grain before any financial result is calculated so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Resolve actual versus amortized cost, billing versus pricing currency, tax/credit treatment, charge types, time grain and resource/group aggregation.
2. Use the source's supported metric and units rather than inferring a monetary amount from quantity, a retail rate or a similarly named field.
3. Reject or clarify incompatible requests such as mixing invoice amount due with resource ActualCost or summing incompatible units.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-067-01 | core | ActualCost, billing currency, signed resource charges and resource/currency grain are confirmed | Validate semantic parameters against the approved cost schema | Use exactly those source and output semantics | metric, units, filters and grain match the plan |
| FSC-067-02 | edge | The user requests effective cost without defining the metric | Validate semantic parameters against the approved cost schema | Ask which supported cost basis is intended | unresolved includes metric meaning |
| FSC-067-03 | edge | Only consumption quantity is available | Validate semantic parameters against the approved cost schema | Do not label the quantity as money | monetary output unavailable with reason |
| FSC-067-04 | edge | A retail price is available but actual charges are not | Validate semantic parameters against the approved cost schema | Label a separately authorized estimate or block actual-spend output | no retail-as-actual substitution |
| FSC-067-05 | boundary | The requested group grain would discard required resource rows | Validate semantic parameters against the approved cost schema | Clarify or preserve resource detail plus a separate group subtotal | detail cardinality not silently collapsed |
| FSC-067-06 | edge | The user asks to include tax in resource costs without an allocation contract | Validate semantic parameters against the approved cost schema | Ask for a supported basis or keep invoice tax separate | no fabricated tax allocation |
| FSC-067-07 | failure | The selected metric is unsupported by the current agreement/schema | Validate semantic parameters against the approved cost schema | Return a capability error rather than a nearest-name metric | unsupported metric dispatches=0 |
| FSC-067-08 | metamorphic | The same approved metric is expressed with an approved synonym | Validate semantic parameters against the approved cost schema | Use the same canonical metric and query fingerprint | semantic mapping unchanged |

## Priority and Kano rationale

- **Cost of delay:** Correct arithmetic over the wrong metric still produces a false financial answer.
- **Duration estimate:** A finite semantic parameter/metric mapping with incompatible-combination fixtures. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-043 - Add authorized shared-commitment coverage evidence](./bl-043-add-authorized-shared-commitment-coverage-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-067 - Confirm cost basis units and aggregation grain](../voc/voc-067-confirm-cost-basis-units-and-aggregation-grain.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-067-confirm-cost-basis-units-and-aggregation-grain.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
