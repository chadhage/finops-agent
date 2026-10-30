# BL-104 - Escalate unknown scenarios to human review and coverage maintenance

Handle irreducible or novel analytical uncertainty through a private, evidence-preserving human review path rather than unbounded questions or fabricated certainty.

**Force rank:** 37 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Qualification and human review  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-REVIEW; CAP-EVALUATION; CAP-GROUNDING  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 3 = **2.667**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** scenario validation / proposed utility contract  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to handle irreducible or novel analytical uncertainty through a private, evidence-preserving human review path rather than unbounded questions or fabricated certainty so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Explain the exact unresolved parameter, source conflict, missing permission/capability or out-of-distribution condition and the smallest safe next action; no number of questions can manufacture missing source truth.
2. Offer an authorized private worksheet of evidence, assumptions, alternatives and questions, labeling human assertions separately from observed Azure facts and retaining owner decision authority.
3. New cases require deduplication, expert-adjudicated expected outcomes, versioned negative regression coverage and affected requalification before closure; the catalogue is finite and extensible, not proof of all possible FinOps situations.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-104-01 | core | A source-backed conflict cannot be resolved within the approved clarification policy | Escalate an unresolved case and maintain the finite scenario inventory | Return a private evidence summary and precise human review question | state=abstained/blocked; no fabricated resolution |
| FSC-104-02 | edge | The user cannot obtain a required fact or permission | Escalate an unresolved case and maintain the finite scenario inventory | Name the gap and safe owner/configuration action without repeated impossible questions | bounded clarification; no credential request |
| FSC-104-03 | boundary | A novel request lies outside all qualified query classes | Escalate an unresolved case and maintain the finite scenario inventory | Stop and propose reviewed discovery rather than improvise | no unqualified business dispatch |
| FSC-104-04 | edge | A human supplies an unsupported opinion about a financial fact | Escalate an unresolved case and maintain the finite scenario inventory | Keep it labeled as a human assertion until evidence supports it | opinion does not overwrite the source ledger |
| FSC-104-05 | failure | An escalation target or evidence recipient is not authorized | Escalate an unresolved case and maintain the finite scenario inventory | Do not share private financial evidence | cross-user disclosure=0 |
| FSC-104-06 | edge | A newly discovered case duplicates an existing scenario | Escalate an unresolved case and maintain the finite scenario inventory | Link or refine existing coverage rather than inflate unique-case claims | deduplicated coverage disposition |
| FSC-104-07 | failure | A new negative regression fails after a proposed fix | Escalate an unresolved case and maintain the finite scenario inventory | Keep the affected qualification/release blocked | no closure from a written plan or retries |
| FSC-104-08 | metamorphic | The same approved evidence and unresolved question are summarized differently | Escalate an unresolved case and maintain the finite scenario inventory | Preserve facts, limitations and decision authority | no new unsupported claim or promised outcome |

## Priority and Kano rationale

- **Cost of delay:** Unknown cases need a useful, honest path forward rather than a confident wrong answer or endless questioning.
- **Duration estimate:** A bounded private escalation/feedback and coverage-change acceptance contract. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a proposed analytical utility; independent customer value and non-overlapping acceptance must still be validated.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); [BL-100 - Build expert-adjudicated reference cases and anti-leakage datasets](./bl-100-build-expert-adjudicated-reference-cases-and-anti-leakage-datasets.md); [BL-101 - Qualify precision completeness and query accuracy with confidence bounds](./bl-101-qualify-precision-completeness-and-query-accuracy-with-confidence-bounds.md); [BL-102 - Invalidate stale qualifications and audit production-quality evidence](./bl-102-invalidate-stale-qualifications-and-audit-production-quality-evidence.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-001 - Define the report-to-owner decision path](./bl-001-define-the-report-to-owner-decision-path.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-017 - Capture owner progress before workshop assistance](./bl-017-capture-owner-progress-before-workshop-assistance.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-031 - Create a human review path for ambiguous optimization](./bl-031-create-a-human-review-path-for-ambiguous-optimization.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-034 - Require owner validation for fix-versus-delete decisions](./bl-034-require-owner-validation-for-fix-versus-delete-decisions.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-051 - Define the Zava pilot go-no-go contract](./bl-051-define-the-zava-pilot-go-no-go-contract.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-104 - Escalate unknown scenarios to human review and coverage maintenance](../voc/voc-104-escalate-unknown-scenarios-to-human-review-and-coverage-maintenance.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-104-escalate-unknown-scenarios-to-human-review-and-coverage-maintenance.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
