# BL-092 - Allocate costs through validated business membership

Build accountable application or cost-center views from approved membership rules without inventing ownership or rewriting historical attribution.

**Force rank:** 36 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Allocation and unit economics  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-ALLOCATION; CAP-COST; CAP-GROUNDING  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 3 = **2.667**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** scenario validation / proposed utility contract  
**Status:** Proposed / not started.  
**Horizon / release:** Next / G2; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-006 - Support business cost and portfolio decisions](../roadmap/rm-006-support-business-cost-and-portfolio-decisions.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to build accountable application or cost-center views from approved membership rules without inventing ownership or rewriting historical attribution so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Record mapping authority/version/effective dates, business key, scope, allocation rules and permitted metadata sources.
2. Missing/conflicting tags or memberships remain unallocated or unresolved; resource names, RBAC roles and inferred application names do not establish accountable ownership.
3. Reconcile every included charge and retain historical-versus-current mapping distinctions; multi-subscription membership still needs separately approved resource/data scope.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-092-01 | core | Approved effective-dated membership assigns R1's charge to application A | Apply an approved business membership mapping to authorized cost evidence | Attribute the charge with mapping and source lineage | business total reconciles to included charge |
| FSC-092-02 | edge | A required CostCenter tag or membership is missing | Apply an approved business membership mapping to authorized cost evidence | Keep the amount explicitly unallocated | no resource-name inference |
| FSC-092-03 | failure | Two authoritative mappings conflict for the same charge period | Apply an approved business membership mapping to authorized cost evidence | Expose the conflict and block definitive attribution | no convenient mapping selection |
| FSC-092-04 | boundary | Current tags differ from billing-period membership | Apply an approved business membership mapping to authorized cost evidence | Use only the declared historical/current basis | no silent historical rewrite |
| FSC-092-05 | edge | One workload spans S1 and an unapproved S2 | Apply an approved business membership mapping to authorized cost evidence | Assess only approved S1 evidence and mark the gap | S2 queries=0 |
| FSC-092-06 | edge | A generic RBAC owner exists without accountable business-owner proof | Apply an approved business membership mapping to authorized cost evidence | Do not substitute it as financial accountability | owner remains unknown or separately asserted |
| FSC-092-07 | failure | The business-mapping source is unavailable | Apply an approved business membership mapping to authorized cost evidence | Report incomplete allocation while retaining source costs | no fabricated memberships |
| FSC-092-08 | metamorphic | Application display names change without mapping-key changes | Apply an approved business membership mapping to authorized cost evidence | Preserve business identity and financial membership | no duplicate or lost allocation |

## Priority and Kano rationale

- **Cost of delay:** Wrong business attribution can misdirect financial accountability even when totals match.
- **Duration estimate:** Effective-dated membership and ambiguity reconciliation fixtures. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-064 - Bind immutable user tenant and subscription selection](./bl-064-bind-immutable-user-tenant-and-subscription-selection.md); [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-071 - Validate source schemas field capabilities and identifiers](./bl-071-validate-source-schemas-field-capabilities-and-identifiers.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-077 - Deduplicate charge identities without discarding legitimate charges](./bl-077-deduplicate-charge-identities-without-discarding-legitimate-charges.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Horizon-gated (G2); dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G2:** R1 evidence review and sponsor approval of broader read-only analytical scope are required. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-039 - Resolve business cost groups from application-service mappings](./bl-039-resolve-business-cost-groups-from-application-service-mappings.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-042 - Route commitment purchase candidates to central evaluation](./bl-042-route-commitment-purchase-candidates-to-central-evaluation.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-092 - Allocate costs through validated business membership](../voc/voc-092-allocate-costs-through-validated-business-membership.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-092-allocate-costs-through-validated-business-membership.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
