# BL-077 - Deduplicate charge identities without discarding legitimate charges

Count each legitimate source charge once without using amount equality or resource ID alone as a deduplication key.

**Force rank:** 21 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Inventory and financial attribution  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-COST; CAP-MONEY  
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

As a FinOps analyst, I want to count each legitimate source charge once without using amount equality or resource ID alone as a deduplication key so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Use the reviewed source charge/grain identity, billing period, scope and version semantics to distinguish duplicates from independent equal-valued charges.
2. Detect repeated pages, replayed exports, overlapping source windows and corrections explicitly; do not combine duplicate source populations or deduplicate by amount alone.
3. Preserve source sign, quantity/unit context, commitment/purchase charge grain and unallocated records without forcing them onto a live resource.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-077-01 | core | Distinct charge IDs C1 and C2 for R1 have amounts 10.00 and 2.50 USD | Validate charge identity and aggregate the accepted charge population | Aggregate 12.50 USD once | accepted charge IDs={C1,C2} |
| FSC-077-02 | edge | Distinct C1 and C2 both have amount 5.00 USD | Validate charge identity and aggregate the accepted charge population | Retain both and total 10.00 USD | equal amounts do not imply duplication |
| FSC-077-03 | failure | The same charge identity is replayed by a retried page | Validate charge identity and aggregate the accepted charge population | Do not add it again; retain the duplicate trace | one accepted source identity |
| FSC-077-04 | edge | Two approved exports overlap in dates and source population | Validate charge identity and aggregate the accepted charge population | Reconcile the overlap or block a combined total | no blind union of repeated charges |
| FSC-077-05 | boundary | A correction/version changes the treatment of an earlier charge | Validate charge identity and aggregate the accepted charge population | Apply only the reviewed source correction contract | original and correction not blindly duplicated |
| FSC-077-06 | edge | A purchase charge lacks a current resource ID | Validate charge identity and aggregate the accepted charge population | Keep it as supported unallocated/benefit evidence | no speculative resource attachment |
| FSC-077-07 | failure | Required charge-grain identity is unavailable | Validate charge identity and aggregate the accepted charge population | Report the deduplication uncertainty and block a complete total | no invented stable charge ID |
| FSC-077-08 | metamorphic | Charge input order or page partition changes | Validate charge identity and aggregate the accepted charge population | Produce the same accepted identity set and signed total | order/page-size invariant |

## Priority and Kano rationale

- **Cost of delay:** Silent charge multiplication or removal directly corrupts spend.
- **Duration estimate:** Charge-grain/idempotency and overlapping-source reconciliation fixtures. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-071 - Validate source schemas field capabilities and identifiers](./bl-071-validate-source-schemas-field-capabilities-and-identifiers.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-074 - Bound pagination throttling retries and cancellation](./bl-074-bound-pagination-throttling-retries-and-cancellation.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-077 - Deduplicate charge identities without discarding legitimate charges](../voc/voc-077-deduplicate-charge-identities-without-discarding-legitimate-charges.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-077-deduplicate-charge-identities-without-discarding-legitimate-charges.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
