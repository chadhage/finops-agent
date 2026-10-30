# BL-076 - Separate current historical and changing resource inventory

Avoid presenting current resource metadata as historical billing-period truth or losing charges for moved/deleted resources.

**Force rank:** 30 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Inventory and financial attribution  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-RESOURCE; CAP-COST  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 3 = **3.000**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** guardrail scenario validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to avoid presenting current resource metadata as historical billing-period truth or losing charges for moved/deleted resources so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Identify current-inventory versus billed-resource population and their separate observation times; require a supported historical source for historical inventory claims.
2. Match immutable source identities and explicit lineage rather than names; moved, renamed, deleted, child or subscription-level resources retain truthful attribution gaps.
3. Keep unmatched historical/unallocated charges separate and do not claim inventory group totals reconcile every invoice charge.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-076-01 | core | Current R1 and its period cost record share an authoritative normalized identity | Join a declared inventory observation to period-specific cost evidence | Join them and retain both observation times | resource fields and billing period remain distinct |
| FSC-076-02 | edge | A deleted resource has period charges but no current inventory row | Join a declared inventory observation to period-specific cost evidence | Report it outside current-inventory group totals | historical charge retained; no invented live resource |
| FSC-076-03 | edge | A resource move changes its ARM ID between the billing period and collection | Join a declared inventory observation to period-specific cost evidence | Require supported identity lineage or leave the charge unmatched | no name-only reassignment |
| FSC-076-04 | edge | Two resource groups contain resources with the same name | Join a declared inventory observation to period-specific cost evidence | Keep their distinct IDs and charges separate | no name collision merge |
| FSC-076-05 | boundary | A resource legitimately has no resource-group field | Join a declared inventory observation to period-specific cost evidence | Retain it under an explicit display-only unreported-group label | no fabricated Azure group |
| FSC-076-06 | edge | Child-resource charges use a different supported attribution grain | Join a declared inventory observation to period-specific cost evidence | Use only the reviewed mapping or retain the mismatch | no speculative parent aggregation |
| FSC-076-07 | failure | Historical inventory is requested but only current ARG evidence exists | Join a declared inventory observation to period-specific cost evidence | Ask for changed scope or report the unsupported historical population | no historical snapshot fabricated |
| FSC-076-08 | metamorphic | Resource display casing or naming changes without identity change | Join a declared inventory observation to period-specific cost evidence | Preserve identity-based attribution and label the observed metadata change | no false deletion, recreation or savings claim |

## Priority and Kano rationale

- **Cost of delay:** Lifecycle changes routinely make a current-inventory join financially incomplete.
- **Duration estimate:** Temporal identity/attribution fixtures over the existing inventory and cost contracts. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-071 - Validate source schemas field capabilities and identifiers](./bl-071-validate-source-schemas-field-capabilities-and-identifiers.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-038 - Confirm Zava subscription coverage using explicit IDs](./bl-038-confirm-zava-subscription-coverage-using-explicit-ids.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-076 - Separate current historical and changing resource inventory](../voc/voc-076-separate-current-historical-and-changing-resource-inventory.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-076-separate-current-historical-and-changing-resource-inventory.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
