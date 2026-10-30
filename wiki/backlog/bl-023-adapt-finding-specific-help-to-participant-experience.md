# BL-023 - Adapt finding-specific help to participant experience

Offer appropriate assistance without assuming that subscription ownership proves Azure expertise.

**Force rank:** 86 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 7 / 3 = **2.333**  
**Relative cost of delay:** 7/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-003 - Prove finding-led workshops and support adoption](../roadmap/rm-003-prove-finding-led-workshops-and-support-adoption.md)  
**Planning date:** 2026-10-28

## User story

As a workshop participant, I want help appropriate to my current understanding so that I can act on findings without a general training prerequisite.

## Acceptance criteria

1. Intake records finding-specific assistance needs without treating a subscription as proof of Azure knowledge.
2. The facilitator can choose an explanatory or more advanced path for the same selected finding and deployment method.
3. The content remains tied to current findings and does not create mandatory certification or broad personnel training.

## Priority and Kano rationale

- **Cost of delay:** A technically mismatched workshop can fail the intended audience even with correct report findings.
- **Duration estimate:** A moderate guidance and intake-adaptation slice, limited to selected findings and supported methods.
- **Kano hypothesis:** Guidance that better fits the participant's experience should improve workshop usefulness.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-017 - Capture owner progress before workshop assistance](./bl-017-capture-owner-progress-before-workshop-assistance.md); [BL-024 - Support deployment-neutral remediation guidance](./bl-024-support-deployment-neutral-remediation-guidance.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-023 - Do not equate subscription issuance with Azure expertise](../voc/voc-023-do-not-equate-subscription-issuance-with-azure-expertise.md) - source classification: Existing-state constraint.
- [VOC-026 - Keep organizational skilling outside this engagement](../voc/voc-026-keep-organizational-skilling-outside-this-engagement.md) - source classification: Existing-state constraint.
- [VOC-017 - Recognize what teams have already done before the workshop](../voc/voc-017-recognize-what-teams-have-already-done-before-the-workshop.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not solve company-wide skilling gaps or change who is allowed to receive a subscription.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
