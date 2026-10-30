# BL-102 - Invalidate stale qualifications and audit production-quality evidence

Prevent a previous benchmark or cached readiness result from certifying a changed model, prompt, source contract or permission context.

**Force rank:** 29 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Qualification and human review  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-EVALUATION; CAP-GROUNDING; CAP-IDENTITY  
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

As a FinOps analyst, I want to prevent a previous benchmark or cached readiness result from certifying a changed model, prompt, source contract or permission context so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Bind qualification to the approved dataset/method, model/prompt/tool/query/schema versions, source class and declared applicability/expiry rules; no caller-held score grants business authority.
2. Drift, changed financial definitions, failed hard invariants or known invalidation suspend affected claims until revalidation and explicit release decisions.
3. Audit unresolved parameters, gate decisions, source/coverage/derivation references and safe correlations without credentials, unauthorized raw billing payloads or unapproved durable production state.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-102-01 | core | The deployed plan/model/tool/source versions match a current qualified artifact | Validate qualification freshness and emit a privacy-safe decision/evidence audit record | Record the applicable artifact and readiness decision | artifact binding visible without secrets |
| FSC-102-02 | edge | A model or prompt changes after qualification | Validate qualification freshness and emit a privacy-safe decision/evidence audit record | Require affected class requalification before a 99% claim | old score not inherited |
| FSC-102-03 | failure | A source schema or monetary definition drifts | Validate qualification freshness and emit a privacy-safe decision/evidence audit record | Suspend affected qualification and surface the exact gap | no silent adapter repair with old certification |
| FSC-102-04 | boundary | Qualification expires or the applicability condition no longer holds | Validate qualification freshness and emit a privacy-safe decision/evidence audit record | Block the qualification claim and dispatch where required | no unlimited validity default |
| FSC-102-05 | adversarial | A user-supplied artifact or confidence number imitates trusted metadata | Validate qualification freshness and emit a privacy-safe decision/evidence audit record | Reject untrusted qualification authority | no caller score authorizes data access |
| FSC-102-06 | failure | A monitored hard-invariant failure occurs | Validate qualification freshness and emit a privacy-safe decision/evidence audit record | Fail closed for the affected class and open reviewed regression work | no averaging away the failure |
| FSC-102-07 | edge | Audit payload includes tokens or raw unrelated invoice details | Validate qualification freshness and emit a privacy-safe decision/evidence audit record | Redact/reject the unsafe audit event while preserving safe correlation | no sensitive logging |
| FSC-102-08 | metamorphic | A restart loses permitted ephemeral session state | Validate qualification freshness and emit a privacy-safe decision/evidence audit record | Require rebinding/re-entry; do not reconstruct authority from audit text | no audit-as-authentication fallback |

## Priority and Kano rationale

- **Cost of delay:** Stale certification can make an apparently safe agent silently regress.
- **Duration estimate:** Qualification-version/lifecycle, audit-redaction and fail-closed regression contracts. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-070 - Validate typed read-only query plans and tool destinations](./bl-070-validate-typed-read-only-query-plans-and-tool-destinations.md); [BL-071 - Validate source schemas field capabilities and identifiers](./bl-071-validate-source-schemas-field-capabilities-and-identifiers.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-075 - Preserve authority and privacy across source and session changes](./bl-075-preserve-authority-and-privacy-across-source-and-session-changes.md); [BL-100 - Build expert-adjudicated reference cases and anti-leakage datasets](./bl-100-build-expert-adjudicated-reference-cases-and-anti-leakage-datasets.md); [BL-101 - Qualify precision completeness and query accuracy with confidence bounds](./bl-101-qualify-precision-completeness-and-query-accuracy-with-confidence-bounds.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-051 - Define the Zava pilot go-no-go contract](./bl-051-define-the-zava-pilot-go-no-go-contract.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-102 - Invalidate stale qualifications and audit production-quality evidence](../voc/voc-102-invalidate-stale-qualifications-and-audit-production-quality-evidence.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-102-invalidate-stale-qualifications-and-audit-production-quality-evidence.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
