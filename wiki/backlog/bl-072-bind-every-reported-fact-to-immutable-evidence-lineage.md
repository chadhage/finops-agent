# BL-072 - Bind every reported fact to immutable evidence lineage

Make each factual cell, subtotal and narrative assertion traceable to authorized source records or a reproducible deterministic calculation.

**Force rank:** 17 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Evidence and collection integrity  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-GROUNDING; CAP-REPORT  
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

As a FinOps analyst, I want to make each factual cell, subtotal and narrative assertion traceable to authorized source records or a reproducible deterministic calculation so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Retain non-secret source references, actor/scope binding, canonical plan/query fingerprint, source/API versions, period/basis/currency, retrieval time and supported data watermark.
2. Bind derived values to included inputs and declared decimal/rounding rules; a citation or document title alone does not prove that the claimed value is present.
3. Refuse unsupported factual assertions and protect private lineage from cross-user access, tampering and credential leakage.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-072-01 | core | A resource row and subtotal have validated source records and a declared calculation | Construct and validate the report evidence ledger | Attach references and reproducible input lineage | every factual output has supporting evidence IDs |
| FSC-072-02 | edge | A narrative states a saving absent from all source records and calculations | Construct and validate the report evidence ledger | Reject that claim instead of adding a plausible citation | unsupported claims=0 |
| FSC-072-03 | adversarial | A valid citation is attached to the wrong resource amount | Construct and validate the report evidence ledger | Reject the value/reference mismatch | claim not accepted by citation existence alone |
| FSC-072-04 | boundary | Collection time is known but data-through time is not | Construct and validate the report evidence ledger | Keep retrieval time separate and freshness unknown | no invented watermark |
| FSC-072-05 | failure | An evidence handle is expired or belongs to U2 | Construct and validate the report evidence ledger | Block reuse and explain the missing current evidence | no cross-user lineage disclosure |
| FSC-072-06 | adversarial | The query fingerprint or source scope is altered after collection | Construct and validate the report evidence ledger | Invalidate the affected ledger and output | tampered binding rejected |
| FSC-072-07 | edge | A total omits one included charge from its derivation | Construct and validate the report evidence ledger | Fail reconciliation rather than silently adjusting the value | input set and derivation mismatch exposed |
| FSC-072-08 | metamorphic | Source rows are reordered without changing their identities or values | Construct and validate the report evidence ledger | Preserve the same factual totals and evidence membership | order-independent derivation verified |

## Priority and Kano rationale

- **Cost of delay:** Untraceable statements are indistinguishable from hallucinated financial facts.
- **Duration estimate:** A source-to-cell/claim ledger with reproducible derivations and binding checks. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-064 - Bind immutable user tenant and subscription selection](./bl-064-bind-immutable-user-tenant-and-subscription-selection.md); [BL-070 - Validate typed read-only query plans and tool destinations](./bl-070-validate-typed-read-only-query-plans-and-tool-destinations.md); [BL-071 - Validate source schemas field capabilities and identifiers](./bl-071-validate-source-schemas-field-capabilities-and-identifiers.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-014 - Package reusable report evidence for workshop handoff](./bl-014-package-reusable-report-evidence-for-workshop-handoff.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-072 - Bind every reported fact to immutable evidence lineage](../voc/voc-072-bind-every-reported-fact-to-immutable-evidence-lineage.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-072-bind-every-reported-fact-to-immutable-evidence-lineage.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
