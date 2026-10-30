# BL-065 - Resolve billing agreement and minimum invoice scope

Choose a supported agreement-specific financial source contract without assuming that subscription access grants billing or invoice access.

**Force rank:** 7 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Identity and scope  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-IDENTITY; CAP-BILLING; CAP-QUERY  
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

As a FinOps analyst, I want to choose a supported agreement-specific financial source contract without assuming that subscription access grants billing or invoice access so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Record the observed billing agreement, supported API/schema contract and authoritative subscription-to-billing mapping; do not infer them from names or a prior user's context.
2. Request confirmation and separate permission verification for the minimum linked billing profile, invoice section or other agreement-specific scope actually needed.
3. An unknown or unsupported agreement is an explicit capability gap; do not silently reuse the MCA contract for EA, MOSP or partner billing.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-065-01 | core | An MCA mapping authoritatively links S1 to separately approved BP1 | Resolve the billing agreement and separately approved financial scopes | Use the reviewed MCA source contract within S1 and BP1 | agreement=MCA; approved billing mapping recorded |
| FSC-065-02 | edge | Inventory and Cost Management are readable but invoice access is absent | Resolve the billing agreement and separately approved financial scopes | Ask for an authorized scope decision or report invoice verification blocked | no inferred invoice permission |
| FSC-065-03 | edge | The billing agreement is unknown | Resolve the billing agreement and separately approved financial scopes | Ask or use authorized metadata discovery permitted by the picker contract | no invoice query with an assumed agreement |
| FSC-065-04 | edge | An EA or partner agreement lacks an approved adapter contract | Resolve the billing agreement and separately approved financial scopes | Return an unsupported-contract gap rather than an MCA-shaped result | state=blocked for unsupported source |
| FSC-065-05 | adversarial | A document mentions a billing account outside the approved mapping | Resolve the billing agreement and separately approved financial scopes | Treat the mention as untrusted context, not permission | unapproved billing_dispatches=0 |
| FSC-065-06 | boundary | The minimum invoice scope contains multiple subscriptions | Resolve the billing agreement and separately approved financial scopes | Keep selected-subscription disclosure separate from approved invoice context | no other-subscription charge details disclosed |
| FSC-065-07 | failure | The mapping changes while a report is in progress | Resolve the billing agreement and separately approved financial scopes | Invalidate the financial plan and request reviewed rebinding | old billing handle cannot continue |
| FSC-065-08 | metamorphic | Billing profile display labels change but immutable IDs do not | Resolve the billing agreement and separately approved financial scopes | Preserve the same approved mapping and contract | billing scope key unchanged |

## Priority and Kano rationale

- **Cost of delay:** An incorrect agreement or billing scope makes invoice attribution unsafe.
- **Duration estimate:** An agreement/scope decision contract over existing read-capability and billing-evidence controls. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); [BL-064 - Bind immutable user tenant and subscription selection](./bl-064-bind-immutable-user-tenant-and-subscription-selection.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-040 - Verify MCA cost visibility and permitted aggregation paths](./bl-040-verify-mca-cost-visibility-and-permitted-aggregation-paths.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-065 - Resolve billing agreement and minimum invoice scope](../voc/voc-065-resolve-billing-agreement-and-minimum-invoice-scope.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-065-resolve-billing-agreement-and-minimum-invoice-scope.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
