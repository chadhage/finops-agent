# BL-071 - Validate source schemas field capabilities and identifiers

Reject missing, incompatible or changed source fields instead of guessing schema meaning.

**Force rank:** 11 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Evidence and collection integrity  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-RESOURCE; CAP-COST; CAP-BILLING  
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

As a FinOps analyst, I want to reject missing, incompatible or changed source fields instead of guessing schema meaning so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Use explicit source/version mappings for resource IDs, charge IDs, amounts, currencies, timestamps, status, invoice linkage and units.
2. Distinguish optional absent fields from required evidence gaps; nulls, numeric strings, unsupported enums or changed units cannot silently become valid zero-valued records.
3. A source/schema change invalidates affected qualification until the mapping and fixtures are reviewed; unknown fields do not extend authority or claimed coverage.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-071-01 | core | Required fields match the approved schema and units | Validate a source response against its versioned field contract | Accept typed records with their source/version provenance | typed values equal validated source fields |
| FSC-071-02 | edge | The amount field is missing or null | Validate a source response against its versioned field contract | Mark financial evidence unavailable with a schema reason | no zero coercion |
| FSC-071-03 | edge | The provider renames an amount or currency field | Validate a source response against its versioned field contract | Require the reviewed version mapping rather than nearest-name inference | unknown mapping blocked |
| FSC-071-04 | boundary | An amount arrives as a locale-formatted string | Validate a source response against its versioned field contract | Use an approved unambiguous parse contract or reject it | no comma/decimal guess |
| FSC-071-05 | failure | Resource or invoice identifiers have an invalid type | Validate a source response against its versioned field contract | Reject the affected record or collection explicitly | no stringified object used as identity |
| FSC-071-06 | edge | An optional location is absent but identity and scope are valid | Validate a source response against its versioned field contract | Retain the resource with explicit unknown location | no resource loss or invented region |
| FSC-071-07 | adversarial | An unknown status value is success-shaped text | Validate a source response against its versioned field contract | Reject or surface the unsupported enum | no implicit Available/complete status |
| FSC-071-08 | metamorphic | Column ordering changes without a schema change | Validate a source response against its versioned field contract | Resolve fields by the approved schema mapping | records and arithmetic unchanged |

## Priority and Kano rationale

- **Cost of delay:** Silent schema drift can contaminate every later join and subtotal.
- **Duration estimate:** Versioned mappings and table-driven malformed/optional-field checks. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-065 - Resolve billing agreement and minimum invoice scope](./bl-065-resolve-billing-agreement-and-minimum-invoice-scope.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-070 - Validate typed read-only query plans and tool destinations](./bl-070-validate-typed-read-only-query-plans-and-tool-destinations.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-040 - Verify MCA cost visibility and permitted aggregation paths](./bl-040-verify-mca-cost-visibility-and-permitted-aggregation-paths.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-071 - Validate source schemas field capabilities and identifiers](../voc/voc-071-validate-source-schemas-field-capabilities-and-identifiers.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-071-validate-source-schemas-field-capabilities-and-identifiers.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
