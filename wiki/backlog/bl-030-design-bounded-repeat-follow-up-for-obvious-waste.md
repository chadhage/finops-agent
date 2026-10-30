# BL-030 - Design bounded repeat follow-up for obvious waste

Support owner-approved repeated reminders only for clearly supported waste, with closure and duplicate controls.

**Force rank:** 93 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 7 / 5 = **1.400**  
**Relative cost of delay:** 7/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Next / R2 - validated local-product expansion  
**Roadmap initiative:** [RM-005 - Improve contextual optimization and follow-up](../roadmap/rm-005-improve-contextual-optimization-and-follow-up.md)  
**Planning date:** 2026-10-28

## User story

As a FinOps operator, I want bounded repeat follow-up on clear waste so that owners can review it without creating an indiscriminate notification stream.

## Acceptance criteria

1. Only owner-validated obvious-waste findings enter the repeat path; ambiguous or disputed findings stay in human review.
2. Recipients, cadence, and stop conditions require customer approval; fixed or owner-justified findings stop and duplicate sends are detectable.
3. The local operator-triggered workflow records each proposed or confirmed send separately and does not claim delivery without evidence.

## Priority and Kano rationale

- **Cost of delay:** The customer describes a notifier under development, and unresolved obvious waste can persist without follow-up.
- **Duration estimate:** A larger local workflow slice covering finding lifecycle, approved communication, repeated invocations, and closure.
- **Kano hypothesis:** More reliable follow-up on clear waste should improve the chance that owners take useful action.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-028 - Coordinate report outreach with existing channels](./bl-028-coordinate-report-outreach-with-existing-channels.md); [BL-020 - Validate ownership freshness before report routing](./bl-020-validate-ownership-freshness-before-report-routing.md); [BL-031 - Create a human review path for ambiguous optimization](./bl-031-create-a-human-review-path-for-ambiguous-optimization.md); [BL-034 - Require owner validation for fix-versus-delete decisions](./bl-034-require-owner-validation-for-fix-versus-delete-decisions.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-031 - Repeat owner notifications for clearly obvious waste](../voc/voc-031-repeat-owner-notifications-for-clearly-obvious-waste.md) - source classification: Desired outcome.
- [VOC-032 - Handle ambiguous optimization findings with human judgment](../voc/voc-032-handle-ambiguous-optimization-findings-with-human-judgment.md) - source classification: Existing-state constraint.
- [VOC-035 - Leave the fix-versus-delete decision with the resource owner](../voc/voc-035-leave-the-fix-versus-delete-decision-with-the-resource-owner.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not deploy an always-on global agent or assume that a low-utilization signal authorizes deletion.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
