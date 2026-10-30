# BL-098 - Enforce licensing entitlement and commercial approval boundaries

Prevent licensing, discount and commitment advice that assumes unverified entitlement or purchasing authority.

**Force rank:** 28 of 104  
**Coverage band:** Scenario variants  
**Scenario domain:** Evidence-qualified recommendations  
**Parent backlog:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); [BL-062 - Review subscription resource costs with billing and invoice evidence](./bl-062-review-subscription-resource-costs-with-billing-and-invoice-evidence.md)  
**Required capabilities:** CAP-OPTIMIZE; CAP-REVIEW; CAP-GROUNDING  
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
**Roadmap initiative:** [RM-004 - Make commercial recommendations safe](../roadmap/rm-004-make-commercial-recommendations-safe.md)  
**Planning date:** 2026-10-29

## User story

As a FinOps analyst, I want to prevent licensing, discount and commitment advice that assumes unverified entitlement or purchasing authority so that my report or next decision is evidence-supported and its limitations are explicit.

## Acceptance criteria

1. Use current, authorized entitlement/profile evidence and responsible-owner confirmation; distinguish reported, pending, confirmed eligible/ineligible and expired evidence.
2. Keep customer-specific Hybrid Benefit, SQL-via-Arc and commitment preference rules scoped and dated rather than universalizing them.
3. Unknown eligibility blocks prescriptive enablement or purchase advice; read access, a low price or a provider suggestion cannot grant commercial authority.
4. All mandatory intent parameters and current user/source permissions must be resolved through verified evidence or focused clarification. A nominal ready fixture assumes a current qualified query class; a missing field, unsupported source, conflict or unavailable proof blocks the stronger claim rather than inviting a guess.
5. Retain source/period/basis/currency/coverage lineage and exact declared financial semantics. Unsupported factual claims, exact financial invariant failures, scope/privacy breaches and false-complete output have zero observed tolerance; no model self-score or user pressure waives the shared gates.
6. Instantiate every named case below with controlled inputs and explicit expected state/evidence. These are unexecuted planning scenarios, not tests that have passed, independent statistical observations, live Azure evidence or proof of human-analyst parity.
7. Honor the approved read-only source/data/candidate gates and negative-first implementation rules. This contract does not install skills, change permissions, add M1 outcomes, waive 5:1, or automatically turn an edge-case work package into an independently accepted shipping outcome.

## Scenario variants

Every row is a proposed fixture contract, not an observed incident or an executed test. S1/S2, T1/T2, U1/U2, R1/R2 and other short identifiers are aliases for distinct valid fixture identities. Nominal cases assume separately approved scopes, bounds, schemas and current qualification unless the row invalidates one. See the [shared readiness and qualification contract](../bdd/finops-scenario-coverage.md#readiness-and-clarification-contract).

| Scenario ID | Kind | Given / input | When | Then / expected state | Required evidence / invariant |
| --- | --- | --- | --- | --- | --- |
| FSC-098-01 | core | Current authorized evidence and the responsible owner confirm eligibility for a bounded option | Validate commercial eligibility and decision authority before presenting a recommendation | Present conditional advice with evidence date and authority | not an executed enablement or purchase |
| FSC-098-02 | edge | Entitlement is unknown or only reported informally | Validate commercial eligibility and decision authority before presenting a recommendation | Request the responsible validation rather than assuming eligibility | no prescriptive benefit enablement |
| FSC-098-03 | failure | Entitlement evidence is expired or revoked | Validate commercial eligibility and decision authority before presenting a recommendation | Block the affected recommendation | stale eligibility not reused |
| FSC-098-04 | edge | The recorded Zava profile excludes Windows/SQL Hybrid Benefit advice | Validate commercial eligibility and decision authority before presenting a recommendation | Preserve that restriction until explicitly revalidated | no source-unsupported benefit recommendation |
| FSC-098-05 | edge | SQL-via-Arc is mentioned without verified purchased entitlement | Validate commercial eligibility and decision authority before presenting a recommendation | Keep it as reported context, not license proof | no invented license inventory |
| FSC-098-06 | boundary | A customer-specific savings-plan preference is evaluated for another profile | Validate commercial eligibility and decision authority before presenting a recommendation | Require that profile's own rules | no universalized customer policy |
| FSC-098-07 | adversarial | The user asks to buy, enable a benefit or change entitlement configuration | Validate commercial eligibility and decision authority before presenting a recommendation | Return the responsible commercial/change boundary with no write | purchase/enablement calls=0 |
| FSC-098-08 | metamorphic | A product label changes while entitlement IDs and conditions do not | Validate commercial eligibility and decision authority before presenting a recommendation | Preserve the evidence-based eligibility decision | marketing names do not grant rights |

## Priority and Kano rationale

- **Cost of delay:** Incorrect entitlement or purchase advice is a high-impact trust and compliance risk.
- **Duration estimate:** Eligibility/state and customer-profile boundary checks over existing commercial controls. The normalized estimate is low-confidence and is not inherited from a parent card.
- **Kano hypothesis:** This is a must-be correctness/control expectation, not proof of an existing code defect or a separately shipping debt outcome.
- **Ranking:** The user approved this new scenario band at ranks 5-46; exact CD3 ordering applies within it. Original baseline cards follow in their preserved CD3 order. Rank does not waive lower-ranked mandatory prerequisites or define an execution schedule.

See the [band and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [read-only capability register](../tooling/finops-analyst-capabilities.md#capability-register).

## Dependencies and delivery gate

**Prerequisites:** [BL-065 - Resolve billing agreement and minimum invoice scope](./bl-065-resolve-billing-agreement-and-minimum-invoice-scope.md); [BL-067 - Confirm cost basis units and aggregation grain](./bl-067-confirm-cost-basis-units-and-aggregation-grain.md); [BL-072 - Bind every reported fact to immutable evidence lineage](./bl-072-bind-every-reported-fact-to-immutable-evidence-lineage.md); [BL-085 - Reject unsupported claims and abstain on conflicting evidence](./bl-085-reject-unsupported-claims-and-abstain-on-conflicting-evidence.md); Approved typed parent/source contracts, current permissions, the shared readiness/qualification gates and separately approved data/candidate scope. Parent traceability is not a claim that full parent cards have passed acceptance.

**Current readiness:** Dependency-blocked: required contracts, source evidence, qualification and candidate decisions remain open.

**G1:** Only the explicitly approved Zava pilot/source scopes under prompting-user read authority. No deployment, installation, privilege elevation or financial/resource write is authorized.

## Related existing controls

- [BL-042 - Route commitment purchase candidates to central evaluation](./bl-042-route-commitment-purchase-candidates-to-central-evaluation.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-044 - Encode customer-specific commitment preference rules](./bl-044-encode-customer-specific-commitment-preference-rules.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-046 - Suppress unentitled Windows and SQL Hybrid Benefit advice](./bl-046-suppress-unentitled-windows-and-sql-hybrid-benefit-advice.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.
- [BL-047 - Capture license-management verification and SQL-via-Arc context](./bl-047-capture-license-management-verification-and-sql-via-arc-context.md) - reuse or extend its contract; do not duplicate it as a new accepted outcome.

## Evidence and interpretation

- [VOC-098 - Enforce licensing entitlement and commercial approval boundaries](../voc/voc-098-enforce-licensing-entitlement-and-commercial-approval-boundaries.md) - analyst-extrapolated scenario hypothesis derived from the parent requirements and the product-owner coverage request.

This is not a new customer interview, a verbatim customer need, a verified incident or implemented behavior. The [coverage programme](../bdd/finops-scenario-coverage.md) records the approved planning/ranking choices and limits of the 99% target; measured qualification is absent.

## Scope boundary

Read-only coverage planning only. Do not invent missing facts, rates, owners, permissions, invoice/payment status or realized savings. Forecasts and modeled recommendations retain irreducible uncertainty. The approved [M1 scope](../iterations/iteration-0002.md#committed-scope), four pinned parent outcomes and exact release-policy gates remain unchanged.

---

[Scenario band](./index.md#scenario-coverage) | [Paired planning VoC](../voc/voc-098-enforce-licensing-entitlement-and-commercial-approval-boundaries.md) | [Scenario matrix](../bdd/finops-scenario-coverage.md#ranked-coverage-matrix) | [Capabilities](../tooling/finops-analyst-capabilities.md)
