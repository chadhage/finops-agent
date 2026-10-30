# BL-101 - Qualify precision completeness and query accuracy with confidence bounds

Make the 99% goal a measured, scoped qualification target rather than an LLM self-confidence score or a claim that source completeness is known before collection.

**Force rank:** 39 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Qualification and human review  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-EVALUATION; CAP-GROUNDING  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 5 = **2.000**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** guardrail scenario validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to make the 99% goal a measured, scoped qualification target rather than an LLM self-confidence score or a claim that source completeness is known before collection so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Before business dispatch, require all mandatory parameters resolved, deterministic scope/operation/permission/budget gates passed, and a current qualification artifact for the exact query/model/prompt/tool/source-contract class.
2. Qualify declared independent-case indicators for semantic query accuracy, factual precision and scoped completeness using approved one-sided simultaneous 99% confidence bounds with lower bounds at least 99%; record cohorts, denominators, abstention/clarification rates and answerable-case yield.
3. Unsupported factual claims, exact financial invariant failures, privacy/scope violations and false-complete outcomes have zero observed tolerance; any such failure blocks qualification regardless of aggregate score. No benchmark or clarification can guarantee all future provider facts or forecast outcomes.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-101-01 | core | A current, independently reviewed qualification and all deterministic readiness checks pass | Evaluate a query-class qualification artifact against the approved statistical and hard-error gates | Permit only the exact qualified query class; validate returned evidence afterward | pre-dispatch readiness is not a pre-proved complete result |
| FSC-101-02 | boundary | Three declared metrics have 567 independent all-pass cases each under the illustrative Bonferroni design | Evaluate a query-class qualification artifact against the approved statistical and hard-error gates | Do not claim the simultaneous 99% lower-bound target is met | illustrative lower bound below 0.99 |
| FSC-101-03 | boundary | Three declared metrics have 568 independent all-pass cases each under the same approved assumptions | Evaluate a query-class qualification artifact against the approved statistical and hard-error gates | The statistical example can meet the target only if all hard gates and design assumptions also pass | illustrative lower bound at least 0.99; not current product certification |
| FSC-101-04 | failure | One unsupported financial claim or scope breach is observed among many passing cases | Evaluate a query-class qualification artifact against the approved statistical and hard-error gates | Reject qualification despite a high average | zero-tolerance invariant failure blocks |
| FSC-101-05 | adversarial | The model prints confidence=0.999 without a trusted artifact | Evaluate a query-class qualification artifact against the approved statistical and hard-error gates | Ignore it for dispatch/qualification authority | self-score cannot satisfy the gate |
| FSC-101-06 | edge | Extra metric/cohort comparisons are added after selecting a favorable result | Evaluate a query-class qualification artifact against the approved statistical and hard-error gates | Require the declared multiplicity adjustment and a reviewed design | no cherry-picked confidence claim |
| FSC-101-07 | edge | The agent abstains on every answerable case to inflate precision | Evaluate a query-class qualification artifact against the approved statistical and hard-error gates | Fail required answerable-case checks and report yield/abstention honestly | no denominator gaming |
| FSC-101-08 | failure | Source pagination/freshness fails after a qualified query is executed | Evaluate a query-class qualification artifact against the approved statistical and hard-error gates | Return partial/blocked output rather than a complete 99% result | post-collection evidence gates remain mandatory |

## Priority and Kano rationale

- **Cost of delay:** An uncalibrated 99% claim would directly violate the requested precision and trust objective.
- **Duration estimate:** A ground-truth-backed qualification method, multiple-comparison handling and release/dispatch evidence contract. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); [BL-070 - Validate typed read-only query plans and tool destinations](./bl-070-validate-typed-read-only-query-plans-and-tool-destinations.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); [BL-100 - Build expert-adjudicated reference cases and anti-leakage datasets](./bl-100-build-expert-adjudicated-reference-cases-and-anti-leakage-datasets.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-051 - Define the Zava pilot go-no-go contract](./bl-051-define-the-zava-pilot-go-no-go-contract.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-101 - Qualify precision completeness and query accuracy with confidence bounds](../voc/voc-101-qualify-precision-completeness-and-query-accuracy-with-confidence-bounds.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-101-qualify-precision-completeness-and-query-accuracy-with-confidence-bounds.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
