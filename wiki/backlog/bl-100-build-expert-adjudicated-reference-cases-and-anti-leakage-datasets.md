# BL-100 - Build expert-adjudicated reference cases and anti-leakage datasets

Create a versioned, independently reviewable reference population before claiming human-analyst parity or a measured accuracy/completeness rate.

**Force rank:** 38 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Qualification and human review  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-EVALUATION; CAP-GROUNDING; CAP-REVIEW  
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

As a FinOps analyst, I want to create a versioned, independently reviewable reference population before claiming human-analyst parity or a measured accuracy/completeness rate so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Reference cases require authoritative source fixtures, declared populations and parameter/action oracles, reproducible exact financial expectations, and qualified human review with disagreements adjudicated against evidence.
2. Include answerable, ambiguous, denied, unavailable, adversarial and temporal cohorts; preserve held-out cases and detect training/prompt/reference leakage.
3. Synthetic planning cases, an LLM grader alone, correlated repeated runs or an unresolved oracle cannot establish representative independent qualification evidence.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-100-01 | core | Independent reviewers approve source-backed expected plans, facts, amounts and coverage for a held-out case | Approve and partition the qualification reference corpus | Admit the case with versioned lineage and reviewer disposition | oracle is evidence-backed and reproducible |
| FSC-100-02 | failure | Reviewers disagree and authoritative evidence does not resolve the dispute | Approve and partition the qualification reference corpus | Mark the oracle unresolved and block its use as a passing qualification case | no majority-vote financial fact invented |
| FSC-100-03 | edge | Expected answers were generated only by the evaluated model | Approve and partition the qualification reference corpus | Reject them as the sole ground truth | independent oracle required |
| FSC-100-04 | adversarial | A held-out answer appears in the prompt or training/reference path | Approve and partition the qualification reference corpus | Quarantine the contaminated qualification evidence | no leakage-shaped passing score |
| FSC-100-05 | boundary | Many rows are duplicated from one source event | Approve and partition the qualification reference corpus | Do not count them as independent qualification cases | effective independence/design reviewed |
| FSC-100-06 | edge | The corpus contains only easy successful requests | Approve and partition the qualification reference corpus | Require the declared ambiguity, failure and high-risk cohorts | no broad human-parity claim from easy cases |
| FSC-100-07 | failure | Real financial samples lack permission or privacy clearance | Approve and partition the qualification reference corpus | Use approved synthetic/redacted fixtures or block collection | no unauthorized dataset capture |
| FSC-100-08 | metamorphic | A source/schema or oracle definition changes | Approve and partition the qualification reference corpus | Create a new corpus version and invalidate incompatible results | old scores not transferred silently |

## Priority and Kano rationale

- **Cost of delay:** A weak or contaminated oracle makes every confidence number misleading.
- **Duration estimate:** Reference-corpus design, expert adjudication, cohort and version/leakage controls. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); [BL-070 - Validate typed read-only query plans and tool destinations](./bl-070-validate-typed-read-only-query-plans-and-tool-destinations.md); [BL-071 - Validate source schemas field capabilities and identifiers](./bl-071-validate-source-schemas-field-capabilities-and-identifiers.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-051 - Define the Zava pilot go-no-go contract](./bl-051-define-the-zava-pilot-go-no-go-contract.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-100 - Build expert-adjudicated reference cases and anti-leakage datasets](../voc/voc-100-build-expert-adjudicated-reference-cases-and-anti-leakage-datasets.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-100-build-expert-adjudicated-reference-cases-and-anti-leakage-datasets.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
