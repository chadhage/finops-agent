# BL-073 - Prove scoped completeness and data freshness

Define the requested population and distinguish complete observed coverage from stale, permission-trimmed or unavailable evidence.

**Force rank:** 18 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Evidence and collection integrity  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-GROUNDING; CAP-RESOURCE; CAP-COST  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 3 = **3.333**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** guardrail scenario validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to define the requested population and distinguish complete observed coverage from stale, permission-trimmed or unavailable evidence so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Confirm population, as-of/date basis, required sources, permitted exclusions, finality and freshness criteria before the business query; do not redefine them after seeing gaps.
2. A complete label requires the approved source-contract proofs and terminal coverage for that defined population, not just HTTP success, Reader access, a row count or model confidence.
3. Report complete/partial/blocked and collection/display truncation separately; explicit unavailable labels do not fill missing factual completeness.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-073-01 | core | All required sources finish within approved scope and satisfy declared freshness/finality checks | Evaluate source-population, terminal-page and freshness proofs | Report complete for that precise observed population | coverage proofs and exclusions are visible |
| FSC-073-02 | edge | ARG returns indexed resources while the request assumes an atomic live estate | Evaluate source-population, terminal-page and freshness proofs | Clarify or block the stronger completeness claim | no atomic/full-estate assertion |
| FSC-073-03 | failure | A required source is denied or unavailable | Evaluate source-population, terminal-page and freshness proofs | Report partial/blocked affected coverage, not zero or clean findings | missing facts remain missing |
| FSC-073-04 | boundary | A response is truncated with no usable continuation | Evaluate source-population, terminal-page and freshness proofs | Do not claim complete results | unresolved truncation recorded |
| FSC-073-05 | edge | A cost watermark lags the requested closed period | Evaluate source-population, terminal-page and freshness proofs | Block final-period completeness or explicitly obtain provisional intent | lag not hidden by retrieval timestamp |
| FSC-073-06 | edge | Presentation is shortened after complete collection | Evaluate source-population, terminal-page and freshness proofs | Preserve complete collection status and separately flag omitted display detail | collection and display coverage not conflated |
| FSC-073-07 | adversarial | The user asks to call missing data complete to avoid a warning | Evaluate source-population, terminal-page and freshness proofs | Retain the evidence-based status | no user waiver manufactures source proof |
| FSC-073-08 | metamorphic | The same complete population is partitioned into different page sizes | Evaluate source-population, terminal-page and freshness proofs | Produce equal observed membership and coverage conclusions | page-size changes do not change totals |

## Priority and Kano rationale

- **Cost of delay:** False completeness is a major financial-reporting error even when returned rows are accurate.
- **Duration estimate:** A multi-source coverage ledger and watermark/permission-trimming fixtures. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-066 - Clarify reporting periods time zones and cutoff boundaries](./bl-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md); [BL-070 - Validate typed read-only query plans and tool destinations](./bl-070-validate-typed-read-only-query-plans-and-tool-destinations.md); [BL-071 - Validate source schemas field capabilities and identifiers](./bl-071-validate-source-schemas-field-capabilities-and-identifiers.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-038 - Confirm Zava subscription coverage using explicit IDs](./bl-038-confirm-zava-subscription-coverage-using-explicit-ids.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-040 - Verify MCA cost visibility and permitted aggregation paths](./bl-040-verify-mca-cost-visibility-and-permitted-aggregation-paths.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-073 - Prove scoped completeness and data freshness](../voc/voc-073-prove-scoped-completeness-and-data-freshness.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-073-prove-scoped-completeness-and-data-freshness.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
