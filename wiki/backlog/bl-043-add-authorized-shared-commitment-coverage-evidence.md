# BL-043 - Add authorized shared-commitment coverage evidence

Support central evaluation with existing global coverage and underutilization risk where permitted data is available.

**Force rank:** 89 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 5 = **1.800**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Next / R2 - validated local-product expansion  
**Roadmap initiative:** [RM-006 - Support business cost and portfolio decisions](../roadmap/rm-006-support-business-cost-and-portfolio-decisions.md)  
**Planning date:** 2026-10-28

## User story

As a central FinOps evaluator, I want authorized shared-coverage evidence so that I can assess a local purchase candidate in portfolio context.

## Acceptance criteria

1. The evaluation records existing shared commitment scope, coverage, utilization evidence, source dates, and missing portfolio inputs.
2. Unavailable global data blocks a definitive incremental-purchase recommendation and is not interpreted as zero coverage.
3. Tests distinguish team-level demand, shared coverage, underutilization risk, and central decision status.

## Priority and Kano rationale

- **Cost of delay:** A local saving can create portfolio waste if the existing shared commitment position is ignored.
- **Duration estimate:** A larger evidence-reconciliation slice with central-team data approval and uncertain portfolio availability.
- **Kano hypothesis:** New commitment advice should not ignore known shared coverage and underutilization exposure.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-042 - Route commitment purchase candidates to central evaluation](./bl-042-route-commitment-purchase-candidates-to-central-evaluation.md); [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-045 - Check shared global commitment utilization before adding purchases](../voc/voc-045-check-shared-global-commitment-utilization-before-adding-purchases.md) - source classification: Existing-state constraint.
- [VOC-044 - Route savings-plan and reservation purchases through the central team](../voc/voc-044-route-savings-plan-and-reservation-purchases-through-the-central-team.md) - source classification: Existing-state constraint.
- [VOC-047 - Account for reservation waste when resources change](../voc/voc-047-account-for-reservation-waste-when-resources-change.md) - source classification: Reported problem / risk.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Use explicitly permitted central data or approved exports; the Zava local assessment does not acquire global access implicitly.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
