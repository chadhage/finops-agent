# BL-028 - Coordinate report outreach with existing channels

Record how report communication complements portal, Sentinel, and CSOC processes without duplicating incident response.

**Force rank:** 79 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 6 / 2 = **3.000**  
**Relative cost of delay:** 6/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-003 - Prove finding-led workshops and support adoption](../roadmap/rm-003-prove-finding-led-workshops-and-support-adoption.md)  
**Planning date:** 2026-10-28

## User story

As a communication owner, I want the report handoff to acknowledge existing notification routes so that FinOps support does not conflict with security response.

## Acceptance criteria

1. The channel map identifies existing owner-facing visibility and security contact processes as reported by the customer.
2. The outreach artifact records recipient, finding IDs, purpose, and known related communication for duplicate review.
3. Unverified channel access or delivery remains explicit, and the product does not suppress or replace CSOC alerts.

## Priority and Kano rationale

- **Cost of delay:** Ignoring established channels can create noise and undermine trust in the new report workflow.
- **Duration estimate:** A small communication-routing and duplicate-review contract; no live messaging integration is assumed.
- **Kano hypothesis:** Conflicting or duplicate contact with owners would harm the baseline communication experience.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-006 - Validate finding communication and invitation tone](./bl-006-validate-finding-communication-and-invitation-tone.md); [BL-019 - Resolve accountable owners from ServiceNow records](./bl-019-resolve-accountable-owners-from-servicenow-records.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-029 - Account for existing portal and security-notification channels](../voc/voc-029-account-for-existing-portal-and-security-notification-channels.md) - source classification: Existing-state constraint.
- [VOC-006 - Calibrate finding communication and workshop invitations](../voc/voc-006-calibrate-finding-communication-and-workshop-invitations.md) - source classification: Customer ask.
- [VOC-020 - Maintain ownership changes in ServiceNow for correct routing](../voc/voc-020-maintain-ownership-changes-in-servicenow-for-correct-routing.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

No automatic Sentinel integration, new Teams bot, email sending permission, or security incident workflow redesign.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
