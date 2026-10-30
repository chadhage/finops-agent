# BL-096 - Ground rightsizing and idle-resource advice in workload evidence

Distinguish observed utilization, source recommendations, owner assertions and unknown workload requirements before suggesting a change.

**Force rank:** 43 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Evidence-qualified recommendations  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-OPTIMIZE; CAP-RESOURCE; CAP-REVIEW  
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
**Roadmap initiative:** [RM-005 - Improve contextual optimization and follow-up](../roadmap/rm-005-improve-contextual-optimization-and-follow-up.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to distinguish observed utilization, source recommendations, owner assertions and unknown workload requirements before suggesting a change so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Require the approved utilization window/aggregation, peaks, SLO/availability/capacity constraints, cost/rate basis and owner workload context.
2. No telemetry, low average use, a zero-cost row or an advisor recommendation alone proves that a resource is unused or safe to delete/resize.
3. Present evidence-qualified alternatives and questions only; avoid double-counted estimated savings and retain explicit owner change authority.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-096-01 | core | Validated utilization, peak and owner constraints support a bounded candidate | Assess a bounded rightsizing or idle-resource candidate using permitted evidence | Present the conditional candidate with all evidence and assumptions | no executed change or guaranteed saving |
| FSC-096-02 | failure | Utilization telemetry is missing or inaccessible | Assess a bounded rightsizing or idle-resource candidate using permitted evidence | Report insufficient evidence, not zero utilization | no idle/deletion conclusion |
| FSC-096-03 | edge | Average CPU is low but recorded peaks are significant | Assess a bounded rightsizing or idle-resource candidate using permitted evidence | Retain peak and SLO constraints in the assessment | no average-only recommendation |
| FSC-096-04 | edge | A resource is a required standby or disaster-recovery asset | Assess a bounded rightsizing or idle-resource candidate using permitted evidence | Preserve its stated purpose and validate constraints | low use not treated as waste |
| FSC-096-05 | boundary | Only a short or nonrepresentative window is available | Assess a bounded rightsizing or idle-resource candidate using permitted evidence | Withhold a definitive recommendation under the approved window rule | no invented representative history |
| FSC-096-06 | edge | Two recommendations apply to the same underlying cost | Assess a bounded rightsizing or idle-resource candidate using permitted evidence | Explain overlap and avoid summing incompatible savings | no additive saving inflation |
| FSC-096-07 | adversarial | The user asks to delete or resize immediately | Assess a bounded rightsizing or idle-resource candidate using permitted evidence | Require the existing owner/change process and perform no write | resource mutations=0 |
| FSC-096-08 | metamorphic | A descriptive resource name changes but evidence and constraints do not | Assess a bounded rightsizing or idle-resource candidate using permitted evidence | Keep the same conditional assessment | name does not establish workload function |

## Priority and Kano rationale

- **Cost of delay:** Premature rightsizing or deletion advice can damage a legitimate workload.
- **Duration estimate:** Cost/utilization/context joins and conditional recommendation validation. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); [BL-088 - Explain cost variance without inventing causal explanations](./bl-088-explain-cost-variance-without-inventing-causal-explanations.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Horizon-gated (G2); dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G2:** R1 evidence review and sponsor approval of broader read-only analytical scope are required. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-031 - Create a human review path for ambiguous optimization](./bl-031-create-a-human-review-path-for-ambiguous-optimization.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-033 - Prototype configuration-defect versus unused-resource diagnosis](./bl-033-prototype-configuration-defect-versus-unused-resource-diagnosis.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-034 - Require owner validation for fix-versus-delete decisions](./bl-034-require-owner-validation-for-fix-versus-delete-decisions.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-096 - Ground rightsizing and idle-resource advice in workload evidence](../voc/voc-096-ground-rightsizing-and-idle-resource-advice-in-workload-evidence.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-096-ground-rightsizing-and-idle-resource-advice-in-workload-evidence.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
