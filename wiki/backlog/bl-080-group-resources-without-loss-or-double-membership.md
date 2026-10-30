# BL-080 - Group resources without loss or double membership

Preserve resource/currency detail and reconciled group membership across casing, missing groups and source changes.

**Force rank:** 15 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Grouping and presentation  
**Parent backlog:** [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-RESOURCE; CAP-MONEY; CAP-REPORT  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 2 = **4.500**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** guardrail scenario validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to preserve resource/currency detail and reconciled group membership across casing, missing groups and source changes so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Use the declared inventory or approved historical group basis, never an invoice section or a cost-record display label as an automatic replacement.
2. Every accepted resource/currency row belongs to exactly one relevant section, including an explicit display-only unreported-group bucket; grouping cannot discard detail.
3. Group/currency subtotals reconcile to included signed source costs and remain incomplete when any required group evidence is missing.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-080-01 | core | Two rg-app rows cost 12.50 and 5.00 USD | Build resource-group sections and their currency-specific known-spend subtotals | Show both rows and a 17.50 USD known-spend subtotal | detail count=2; subtotal=17.50 USD |
| FSC-080-02 | edge | The same group appears as rg-app and RG-App | Build resource-group sections and their currency-specific known-spend subtotals | Use one case-insensitive group identity | no duplicate group or charge membership |
| FSC-080-03 | boundary | A resource's group field is empty | Build resource-group sections and their currency-specific known-spend subtotals | Retain it under '(No resource group reported)' as a display label | no invented Azure group |
| FSC-080-04 | edge | An invoice section happens to share a resource-group name | Build resource-group sections and their currency-specific known-spend subtotals | Keep invoice section and resource-group semantics distinct | no invoice-section substitution |
| FSC-080-05 | failure | One resource has no matching cost record | Build resource-group sections and their currency-specific known-spend subtotals | Keep its unavailable status and mark group cost coverage incomplete | missing spend not zero |
| FSC-080-06 | edge | One resource has costs in two currencies | Build resource-group sections and their currency-specific known-spend subtotals | Keep both currency rows in its group with separate subtotals | no mixed-currency total |
| FSC-080-07 | boundary | A group spans multiple pages and source ordering changes | Build resource-group sections and their currency-specific known-spend subtotals | Finish required collection and keep a single section | each resource/currency appears once |
| FSC-080-08 | metamorphic | A filter selects a strict subset of the collected group | Build resource-group sections and their currency-specific known-spend subtotals | Recompute only the subset's declared subtotal and coverage | subset not mislabeled as full-group cost |

## Priority and Kano rationale

- **Cost of delay:** A correct resource amount can still be lost or multiplied by incorrect grouping.
- **Duration estimate:** Deterministic membership and subtotal contracts over existing joined evidence. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-064 - Bind immutable user tenant and subscription selection](./bl-064-bind-immutable-user-tenant-and-subscription-selection.md); [BL-071 - Validate source schemas field capabilities and identifiers](./bl-071-validate-source-schemas-field-capabilities-and-identifiers.md); [BL-076 - Separate current historical and changing resource inventory](./bl-076-separate-current-historical-and-changing-resource-inventory.md); [BL-077 - Deduplicate charge identities without discarding legitimate charges](./bl-077-deduplicate-charge-identities-without-discarding-legitimate-charges.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-039 - Resolve business cost groups from application-service mappings](./bl-039-resolve-business-cost-groups-from-application-service-mappings.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-080 - Group resources without loss or double membership](../voc/voc-080-group-resources-without-loss-or-double-membership.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-080-group-resources-without-loss-or-double-membership.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
