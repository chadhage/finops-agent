# BL-012 - Create finding-specific workshop invitations

Explain which workshop topic addresses the recipient application's actual report findings.

**Force rank:** 68 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 7 / 2 = **3.500**  
**Relative cost of delay:** 7/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-003 - Prove finding-led workshops and support adoption](../roadmap/rm-003-prove-finding-led-workshops-and-support-adoption.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want a workshop invitation tied to my findings so that I understand why attending would help.

## Acceptance criteria

1. Each generated invitation references actual finding IDs, the relevant topic, and the validated support route.
2. A finding without a confirmed workshop match is not assigned an invented topic or scheduled session.
3. The wording remains invitational unless the customer separately approves a different communication policy.

## Priority and Kano rationale

- **Cost of delay:** Generic invitations miss the requested connection between an application's current problem and practical support.
- **Duration estimate:** A small invitation-generation slice using approved communication and offering mappings.
- **Kano hypothesis:** More relevant invitations should increase the usefulness and discoverability of available help.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-006 - Validate finding communication and invitation tone](./bl-006-validate-finding-communication-and-invitation-tone.md); [BL-002 - Map findings to approved support offerings](./bl-002-map-findings-to-approved-support-offerings.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-012 - Tie workshop communication to the application's actual findings](../voc/voc-012-tie-workshop-communication-to-the-applications-actual-findings.md) - source classification: Customer ask.
- [VOC-002 - Increase use of available Microsoft resources](../voc/voc-002-increase-use-of-available-microsoft-resources.md) - source classification: Desired outcome.
- [VOC-005 - Offer help and a solution alongside each problem](../voc/voc-005-offer-help-and-a-solution-alongside-each-problem.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Generate a relevant invitation artifact; do not claim delivery, attendance, booking, or remediation.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
