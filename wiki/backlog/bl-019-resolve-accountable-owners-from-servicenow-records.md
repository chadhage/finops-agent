# BL-019 - Resolve accountable owners from ServiceNow records

Attach the named technical owner to report scope without confusing delegated RBAC with accountability.

**Force rank:** 70 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 3 = **3.333**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-28

## User story

As a FinOps operator, I want the named ServiceNow technical owner attached to selected scope so that findings reach the accountable person.

## Acceptance criteria

1. The owner record includes its ServiceNow reference, named technical owner, applicable subscription IDs, and retrieval or validation date.
2. Delegated RBAC owners and contributors are not silently promoted to accountable owner.
3. Missing or conflicting records produce an explicit ownership gap and a validation route.

## Priority and Kano rationale

- **Cost of delay:** Wrong ownership can misroute every report and undermine the customer's established operating model.
- **Duration estimate:** A moderate validated ownership-input adapter; approved exports can avoid assuming a new live ServiceNow integration.
- **Kano hypothesis:** Correct accountability is a basic requirement for credible owner-directed reports.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-038 - Confirm Zava subscription coverage using explicit IDs](./bl-038-confirm-zava-subscription-coverage-using-explicit-ids.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-019 - Use the named ServiceNow technical owner, not RBAC alone](../voc/voc-019-use-the-named-servicenow-technical-owner-not-rbac-alone.md) - source classification: Existing-state constraint.
- [VOC-021 - Keep remediation responsibility with the owning team](../voc/voc-021-keep-remediation-responsibility-with-the-owning-team.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Use permitted current records or approved exports; do not assume new ServiceNow API access or change the customer's ownership system.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
