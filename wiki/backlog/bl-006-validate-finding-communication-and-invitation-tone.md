# BL-006 - Validate finding communication and invitation tone

Make communication proportionate to supported findings without inventing escalation rules.

**Force rank:** 63 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 8 / 2 = **4.000**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-003 - Prove finding-led workshops and support adoption](../roadmap/rm-003-prove-finding-led-workshops-and-support-adoption.md)  
**Planning date:** 2026-10-28

## User story

As a report recipient, I want communication that explains relevant findings and available help without overstating risk or obligations.

## Acceptance criteria

1. Templates separate ordinary recommendations from conditional high-risk findings using the source report's supported labels.
2. The customer reviews tone, recipients, and invitation wording; unresolved escalation policy remains explicitly open.
3. Tests contain no invented severity, actual vulnerability assertion from an example, or mandatory workshop requirement.

## Priority and Kano rationale

- **Cost of delay:** Poor messaging can turn a useful report into noise or an unintended mandatory escalation.
- **Duration estimate:** A small template set and approval review using the agreed finding and support contracts.
- **Kano hypothesis:** Overstated risk or coercive invitations would erode trust even if the analysis were useful.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md); [BL-002 - Map findings to approved support offerings](./bl-002-map-findings-to-approved-support-offerings.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-006 - Calibrate finding communication and workshop invitations](../voc/voc-006-calibrate-finding-communication-and-workshop-invitations.md) - source classification: Customer ask.
- [VOC-012 - Tie workshop communication to the application's actual findings](../voc/voc-012-tie-workshop-communication-to-the-applications-actual-findings.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not redesign security incident response or silently override existing CSOC communication.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
