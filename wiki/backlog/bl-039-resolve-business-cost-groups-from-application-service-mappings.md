# BL-039 - Resolve business cost groups from application-service mappings

Preserve ServiceNow business grouping and team-specific stage conventions for selected subscriptions.

**Force rank:** 91 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 5 = **1.600**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Next / R2 - validated local-product expansion  
**Roadmap initiative:** [RM-006 - Support business cost and portfolio decisions](../roadmap/rm-006-support-business-cost-and-portfolio-decisions.md)  
**Planning date:** 2026-10-28

## User story

As a business cost stakeholder, I want recorded application-service groups preserved so that rollups reflect the team's actual charging model.

## Acceptance criteria

1. The mapping records ServiceNow application-service references, selected subscription IDs, source dates, and declared stage conventions.
2. Fixtures cover combined stages, per-stage groups, per-subscription groups, and common production versus non-production splits.
3. Conflicting or incomplete membership is explicit and is not silently normalized into one universal schema.

## Priority and Kano rationale

- **Cost of delay:** Azure hierarchy alone does not provide the business grouping the customer uses for cost visibility.
- **Duration estimate:** A larger mapping and validation slice covering flexible grouping, provenance, and ambiguous records.
- **Kano hypothesis:** More accurate business grouping should improve cross-charge and management visibility.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-008 - Build an explicit project-to-subscription assessment manifest](./bl-008-build-an-explicit-project-to-subscription-assessment-manifest.md); [BL-019 - Resolve accountable owners from ServiceNow records](./bl-019-resolve-accountable-owners-from-servicenow-records.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-041 - Use ServiceNow application services for business cost grouping](../voc/voc-041-use-servicenow-application-services-for-business-cost-grouping.md) - source classification: Existing-state constraint.
- [VOC-042 - Do not assume one uniform application-service convention](../voc/voc-042-do-not-assume-one-uniform-application-service-convention.md) - source classification: Existing-state constraint.
- [VOC-040 - Allow a workload to span multiple subscriptions](../voc/voc-040-allow-a-workload-to-span-multiple-subscriptions.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Consume permitted mappings or approved exports; do not redesign ServiceNow policy or assume a live API integration.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
