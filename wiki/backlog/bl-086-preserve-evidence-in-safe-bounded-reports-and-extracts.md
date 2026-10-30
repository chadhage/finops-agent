# BL-086 - Preserve evidence in safe bounded reports and extracts

Render and export faithful, private, parseable evidence without losing coverage or executing untrusted source content.

**Force rank:** 32 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Grouping and presentation  
**Parent backlog:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-REPORT; CAP-GROUNDING  
**Scenario cases:** 8  
**Evidence status:** Unexecuted planning scenarios  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 3 = **3.000**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; analyst planning hypotheses, not validated engineering effort or a financial delay rate.  
**Work type:** guardrail scenario validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / G1; explicit data/candidate approval remains required.  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to render and export faithful, private, parseable evidence without losing coverage or executing untrusted source content so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Preserve schema, identity, exact monetary meaning, currency, provenance and separate collection/display coverage across Markdown, CSV and JSON.
2. Escape untrusted names, formula-like text, delimiters, HTML and mentions according to the declared format; legitimate signed numeric values are not corrupted into text guesses.
3. Respect approved output limits and private delivery; no new attachment service, public link, mailbox or durable store is introduced by a format request.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-086-01 | core | A complete typed ledger is rendered as Markdown and copy-ready JSON | Render an approved report or copy-ready structured extract | Preserve the same factual values, IDs, currencies and coverage metadata | schema/value parity verified |
| FSC-086-02 | adversarial | A resource name contains HTML, table delimiters, mentions or formula-like text | Render an approved report or copy-ready structured extract | Display inert source text with the required escaping | no execution, mention or extra table cell |
| FSC-086-03 | edge | A legitimate numeric refund is -2.50 USD | Render an approved report or copy-ready structured extract | Retain the signed numeric meaning in each declared format | no formula-defense corruption of monetary value |
| FSC-086-04 | boundary | Output exceeds the approved display budget | Render an approved report or copy-ready structured extract | Flag presentation truncation and omitted detail separately | complete collection not silently relabeled or dropped |
| FSC-086-05 | failure | The requested export would require an unapproved public file link | Render an approved report or copy-ready structured extract | Reject the delivery mode or offer authorized copy-ready text | no new storage/share API |
| FSC-086-06 | edge | A numeric-looking resource identifier could be spreadsheet-coerced | Render an approved report or copy-ready structured extract | Use the declared safe representation and preserve the original identifier | no identity loss |
| FSC-086-07 | edge | A no-match view is built from partial evidence | Render an approved report or copy-ready structured extract | Keep partial coverage rather than asserting no such estate resources | no false negative estate claim |
| FSC-086-08 | metamorphic | The same evidence is rendered in a different supported format | Render an approved report or copy-ready structured extract | Return equivalent facts and explicit representation limits | no new collection or authority |

## Priority and Kano rationale

- **Cost of delay:** Presentation can corrupt correct evidence or leak/exploit financial output.
- **Duration estimate:** Format fidelity, injection-safe rendering and bounded truncation fixtures. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-073 - Prove scoped completeness and data freshness](./bl-073-prove-scoped-completeness-and-data-freshness.md); [BL-078 - Preserve signed monetary precision and currency minor units](./bl-078-preserve-signed-monetary-precision-and-currency-minor-units.md); [BL-080 - Group resources without loss or double membership](./bl-080-group-resources-without-loss-or-double-membership.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-009 - Improve report readability using existing content](./bl-009-improve-report-readability-using-existing-content.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-014 - Package reusable report evidence for workshop handoff](./bl-014-package-reusable-report-evidence-for-workshop-handoff.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-024 - Support deployment-neutral remediation guidance](./bl-024-support-deployment-neutral-remediation-guidance.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-086 - Preserve evidence in safe bounded reports and extracts](../voc/voc-086-preserve-evidence-in-safe-bounded-reports-and-extracts.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-086-preserve-evidence-in-safe-bounded-reports-and-extracts.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
