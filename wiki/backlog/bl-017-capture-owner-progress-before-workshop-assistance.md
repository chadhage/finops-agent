# BL-017 - Capture owner progress before workshop assistance

Record completed, attempted, ignored, and blocked recommendations so help starts at the right point.

**Force rank:** 64 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 2 = **4.000**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-003 - Prove finding-led workshops and support adoption](../roadmap/rm-003-prove-finding-led-workshops-and-support-adoption.md)  
**Planning date:** 2026-10-28

## User story

As a facilitator, I want to know what the owner has already tried so that I can quickly identify the current solution state.

## Acceptance criteria

1. The intake captures recommendation IDs, attempted and completed steps, questions, blockers, and the owner's selected deployment method.
2. Unverified self-reported progress remains distinguishable from a verified outcome.
3. The workshop view can identify the next unresolved decision without resetting every finding to the initial state.

## Priority and Kano rationale

- **Cost of delay:** Ignoring prior owner work risks repeating steps and wasting the limited workshop time.
- **Duration estimate:** A small intake artifact and finding-linked progress model, not an enterprise ticketing integration.
- **Kano hypothesis:** Better knowledge of a team's progress should improve the relevance and efficiency of help.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-010 - Produce ordered remediation steps with intended outcomes](./bl-010-produce-ordered-remediation-steps-with-intended-outcomes.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-017 - Recognize what teams have already done before the workshop](../voc/voc-017-recognize-what-teams-have-already-done-before-the-workshop.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not interpret non-attendance or unrecorded progress as a confirmed refusal to remediate.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
