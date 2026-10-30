# BL-093 - Allocate shared costs without hiding residual or duplicate charges

Perform explicitly approved shared-cost allocation while preserving total cost, residuals, currency and accountability uncertainty.

**Force rank:** 41 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Allocation and unit economics  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-ALLOCATION; CAP-MONEY  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 5 = **1.600**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** scenario validation / proposed utility contract  
**Status:** Proposed / not started.  
**Horizon / release:** Next / G2; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-006 - Support business cost and portfolio decisions](../roadmap/rm-006-support-business-cost-and-portfolio-decisions.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to perform explicitly approved shared-cost allocation while preserving total cost, residuals, currency and accountability uncertainty so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Require the approved allocation basis, effective period, eligible population, weights/denominators and currency treatment; equal split is not an implicit default.
2. Preserve raw source cost and separately labeled allocated values, including negative charges and explicit unallocated residuals.
3. Do not double count shared charges, hide rounding residuals, invent weights or treat a mapping proposal as customer-approved allocation.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-093-01 | core | 100.00 USD is allocated using approved 60/40 weights | Validate and apply a declared shared-cost allocation rule | Show source 100.00 and allocations 60.00 plus 40.00 USD | allocation conservation verified |
| FSC-093-02 | edge | Weights or the allocation basis are missing | Validate and apply a declared shared-cost allocation rule | Ask for the approved rule or keep cost unallocated | no default equal split |
| FSC-093-03 | failure | Weights total more than the permitted full allocation | Validate and apply a declared shared-cost allocation rule | Reject over-allocation | no duplicated financial ownership |
| FSC-093-04 | boundary | Rounded allocations leave a small residual | Validate and apply a declared shared-cost allocation rule | Show or resolve it only under the approved residual policy | no hidden balancing adjustment |
| FSC-093-05 | edge | A shared negative adjustment is included | Validate and apply a declared shared-cost allocation rule | Preserve the sign under the reviewed allocation contract | no clamped refund |
| FSC-093-06 | edge | The eligible beneficiary population changes mid-period | Validate and apply a declared shared-cost allocation rule | Use effective-dated rules or report the unsupported segment | no retrospective guessed weights |
| FSC-093-07 | failure | One beneficiary's authorized denominator is unavailable | Validate and apply a declared shared-cost allocation rule | Expose incomplete allocation rather than inventing its share | residual and evidence gap retained |
| FSC-093-08 | metamorphic | Beneficiary order changes with identical approved weights | Validate and apply a declared shared-cost allocation rule | Return identical allocation values and residual | order-independent conservation |

## Priority and Kano rationale

- **Cost of delay:** Shared-cost allocation can create believable but financially invalid chargeback totals.
- **Duration estimate:** Conservation, weight eligibility and effective-period allocation contracts. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-077 - Deduplicate charge identities without discarding legitimate charges](./bl-077-deduplicate-charge-identities-without-discarding-legitimate-charges.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); [BL-092 - Allocate costs through validated business membership](./bl-092-allocate-costs-through-validated-business-membership.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Horizon-gated (G2); dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G2:** R1 evidence review and sponsor approval of broader read-only analytical scope are required. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-039 - Resolve business cost groups from application-service mappings](./bl-039-resolve-business-cost-groups-from-application-service-mappings.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-093 - Allocate shared costs without hiding residual or duplicate charges](../voc/voc-093-allocate-shared-costs-without-hiding-residual-or-duplicate-charges.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-093-allocate-shared-costs-without-hiding-residual-or-duplicate-charges.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
