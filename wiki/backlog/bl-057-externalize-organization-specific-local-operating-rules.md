# BL-057 - Externalize organization-specific local operating rules

Make ownership grouping licensing and commitment assumptions explicit in validated local profiles rather than hard-coding Zava behavior.

**Force rank:** 96 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 6 / 5 = **1.200**  
**Relative cost of delay:** 6/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** enabler  
**Status:** Proposed / not started.  
**Horizon / release:** Next / R2 - validated local-product expansion  
**Roadmap initiative:** [RM-007 - Generalize and measure the local product](../roadmap/rm-007-generalize-and-measure-the-local-product.md)  
**Planning date:** 2026-10-28

## User story

As an analyst serving another approved operating model, I want organization-specific assumptions explicit so that reuse does not silently inherit Zava rules.

## Acceptance criteria

1. A validated local profile declares scope selection, ownership source, application-service conventions, entitlement state, commitment routing, and execution constraints.
2. Missing required values and conflicting mappings fail explicitly rather than using silent Zava defaults.
3. The current Zava profile reproduces baseline behavior, and an isolated second-profile fixture demonstrates different permitted rules without cross-profile data leakage.

## Priority and Kano rationale

- **Cost of delay:** A broader product could produce incorrect advice if it silently carries one customer's business rules into another context.
- **Duration estimate:** A larger profile and validation slice across existing ownership, grouping, licensing, commitment, and execution contracts.
- **Kano hypothesis:** Better fit to a second operating model should increase reuse without forcing every team into Zava-specific assumptions.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-039 - Resolve business cost groups from application-service mappings](./bl-039-resolve-business-cost-groups-from-application-service-mappings.md); [BL-044 - Encode customer-specific commitment preference rules](./bl-044-encode-customer-specific-commitment-preference-rules.md); [BL-046 - Suppress unentitled Windows and SQL Hybrid Benefit advice](./bl-046-suppress-unentitled-windows-and-sql-hybrid-benefit-advice.md); [BL-050 - Preserve the local user-authenticated execution contract](./bl-050-preserve-the-local-user-authenticated-execution-contract.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-derived broader-product extension. The user approved broader product planning with a Zava-first release; these VoCs motivate reuse but are not a customer request for a generic SaaS product.

- [VOC-003 - Design for the other Zava teams, not only the FinOps team](../voc/voc-003-design-for-the-other-zava-teams-not-only-the-finops-team.md) - source classification: Customer ask.
- [VOC-042 - Do not assume one uniform application-service convention](../voc/voc-042-do-not-assume-one-uniform-application-service-convention.md) - source classification: Existing-state constraint.
- [VOC-046 - Prefer savings plans unless reservation conditions are well established](../voc/voc-046-prefer-savings-plans-unless-reservation-conditions-are-well-established.md) - source classification: Existing-state constraint.
- [VOC-048 - Exclude Windows and SQL Hybrid Benefit advice under current entitlements](../voc/voc-048-exclude-windows-and-sql-hybrid-benefit-advice-under-current-entitlements.md) - source classification: Customer ask.
- [VOC-054 - Keep Zava as the current POC; defer regular global automation](../voc/voc-054-keep-zava-as-the-current-poc-defer-regular-global-automation.md) - source classification: Existing-state constraint.
- [VOC-053 - Run within the existing local analysis assets and user permissions](../voc/voc-053-run-within-the-existing-local-analysis-assets-and-user-permissions.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

This user-approved broader-product extension does not imply a hosted multi-tenant control plane, shared credentials, or a request by Zava for a generic SaaS product.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
