# BL-041 - Produce traceable business cost rollups

Aggregate authorized cost evidence using validated application-service membership and visible accounting assumptions.

**Force rank:** 92 of 104  
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

As a business cost owner, I want a reconciled rollup for my validated application-service group so that I can explain what is included and excluded.

## Acceptance criteria

1. Every rollup declares membership, source, time window, currency, coverage, and the treatment of subscription costs versus commitment charges.
2. Fixtures detect duplicate membership, missing subscriptions, incompatible currencies or periods, and incomplete cost access without double counting.
3. Displayed totals reconcile to the included source records, and unknown or excluded amounts remain explicit rather than zero.

## Priority and Kano rationale

- **Cost of delay:** Without a traceable rollup, teams may continue to depend on ad hoc grouping workarounds.
- **Duration estimate:** A larger aggregation and reconciliation slice covering membership, billing context, and incomplete data.
- **Kano hypothesis:** Reliable grouped costs should improve business decision usefulness.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-039 - Resolve business cost groups from application-service mappings](./bl-039-resolve-business-cost-groups-from-application-service-mappings.md); [BL-040 - Verify MCA cost visibility and permitted aggregation paths](./bl-040-verify-mca-cost-visibility-and-permitted-aggregation-paths.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-041 - Use ServiceNow application services for business cost grouping](../voc/voc-041-use-servicenow-application-services-for-business-cost-grouping.md) - source classification: Existing-state constraint.
- [VOC-042 - Do not assume one uniform application-service convention](../voc/voc-042-do-not-assume-one-uniform-application-service-convention.md) - source classification: Existing-state constraint.
- [VOC-043 - Address reported MCA management-group cost visibility limitations](../voc/voc-043-address-reported-mca-management-group-cost-visibility-limitations.md) - source classification: Reported problem / risk.
- [VOC-051 - Collect subscription-linked cost data through the appropriate RBAC context](../voc/voc-051-collect-subscription-linked-cost-data-through-the-appropriate-rbac-context.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not assume management-group cost visibility or convert a local report into a new billing control plane.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
