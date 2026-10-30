# BL-040 - Verify MCA cost visibility and permitted aggregation paths

Distinguish the reported management-group limitation from current capabilities, permissions, and available exports.

**Force rank:** 87 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 7 / 3 = **2.333**  
**Relative cost of delay:** 7/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** discovery  
**Status:** Proposed / not started.  
**Horizon / release:** Next / R2 - validated local-product expansion  
**Roadmap initiative:** [RM-006 - Support business cost and portfolio decisions](../roadmap/rm-006-support-business-cost-and-portfolio-decisions.md)  
**Planning date:** 2026-10-28

## User story

As a FinOps analyst, I want current cost visibility verified so that business rollups use a supported and authorized data path.

## Acceptance criteria

1. The record separates customer-reported behavior, currently observed capabilities, access failures, and unavailable evidence.
2. The review documents approved subscription, billing, invoice-section, or export paths without assuming new privileges.
3. A supported path or an explicit blocked decision is recorded before rollup implementation.

## Priority and Kano rationale

- **Cost of delay:** An unverified billing assumption can invalidate the chosen cost-rollup design.
- **Duration estimate:** A bounded capability and access review using the selected billing context; no billing hierarchy changes.
- **Kano hypothesis:** Cost features must be honest about supported visibility and actual access rather than promising a nonexistent product fix.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-043 - Address reported MCA management-group cost visibility limitations](../voc/voc-043-address-reported-mca-management-group-cost-visibility-limitations.md) - source classification: Reported problem / risk.
- [VOC-051 - Collect subscription-linked cost data through the appropriate RBAC context](../voc/voc-051-collect-subscription-linked-cost-data-through-the-appropriate-rbac-context.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not label the customer report a verified Azure defect, promise a product fix, or rearrange invoice sections.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
