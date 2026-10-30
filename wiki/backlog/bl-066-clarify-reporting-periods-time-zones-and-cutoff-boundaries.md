# BL-066 - Clarify reporting periods time zones and cutoff boundaries

Translate a user's reporting period into an explicit, source-compatible time interval without silent boundary or finality assumptions.

**Force rank:** 8 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Clarification and query planning  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-QUERY; CAP-COST  
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

As a FinOps analyst, I want to translate a user's reporting period into an explicit, source-compatible time interval without silent boundary or finality assumptions so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Capture timezone, calendar or fiscal interpretation, inclusive/exclusive boundaries, reporting date basis and provisional/closed-period preference.
2. Translate the canonical interval into each source's documented boundary semantics and retain the original user meaning in provenance.
3. Do not replace missing periods, daylight-saving ambiguity, invoice-period differences or unavailable billing watermarks with guessed dates or a completeness claim.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-066-01 | core | September 2026 UTC is explicitly selected | Normalize and confirm the reporting interval and source cutoff | Normalize to 2026-09-01 inclusive through 2026-10-01 exclusive | canonical interval matches all approved adapters |
| FSC-066-02 | edge | Last month is requested without a reference timezone | Normalize and confirm the reporting interval and source cutoff | Ask for the timezone or an explicitly acknowledged default | no clock-dependent silent period |
| FSC-066-03 | boundary | The selected local interval crosses a daylight-saving transition | Normalize and confirm the reporting interval and source cutoff | Use the approved timezone database and preserve exact intended instants | no duplicated or omitted hour |
| FSC-066-04 | boundary | The interval includes February 29 in a leap year | Normalize and confirm the reporting interval and source cutoff | Retain the leap day and correct exclusive endpoint | expected day count verified |
| FSC-066-05 | edge | Usage date and invoice posting date imply different populations | Normalize and confirm the reporting interval and source cutoff | Ask which date basis the job requires | dateBasis confirmed before financial dispatch |
| FSC-066-06 | edge | A fiscal month differs from a calendar month | Normalize and confirm the reporting interval and source cutoff | Require the approved fiscal calendar mapping | no calendar-month substitution |
| FSC-066-07 | failure | The requested closed period has no source finality watermark | Normalize and confirm the reporting interval and source cutoff | Block a final-completeness claim or obtain explicit provisional scope | freshness/finality gap retained |
| FSC-066-08 | metamorphic | Two timezone-qualified expressions denote the same instants | Normalize and confirm the reporting interval and source cutoff | Produce the same canonical interval and equivalent queries | canonical endpoints equal |

## Priority and Kano rationale

- **Cost of delay:** A one-day or timezone mismatch can materially change spend and reconciliation.
- **Duration estimate:** A canonical time contract and boundary fixtures across the three financial evidence sources. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-063 - Resolve missing and ambiguous query intent](./bl-063-resolve-missing-and-ambiguous-query-intent.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-066 - Clarify reporting periods time zones and cutoff boundaries](../voc/voc-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-066-clarify-reporting-periods-time-zones-and-cutoff-boundaries.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
