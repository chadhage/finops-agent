# BL-015 - Pair guided fixes with recurrence-prevention explanations

Help owners understand both how to address current findings and how to avoid repeating the same issue.

**Force rank:** 90 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 5 = **1.600**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-003 - Prove finding-led workshops and support adoption](../roadmap/rm-003-prove-finding-led-workshops-and-support-adoption.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want finding-specific guidance and a prevention explanation so that I can resolve the issue and understand what to avoid next time.

## Acceptance criteria

1. Each selected workshop example has a proposed fix, owner verification step, and explanation of how the same problem can recur.
2. Guidance supports the team's permitted deployment method and keeps audit findings advisory.
3. General personnel training and automatic policy rollout are explicitly excluded from the material.

## Priority and Kano rationale

- **Cost of delay:** Reports without practical learning can leave problems unresolved or recurring.
- **Duration estimate:** A larger content-validation slice across representative finding types and multiple deployment methods.
- **Kano hypothesis:** Useful remediation and prevention guidance should produce greater ongoing value than problem identification alone.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-024 - Support deployment-neutral remediation guidance](./bl-024-support-deployment-neutral-remediation-guidance.md); [BL-027 - Keep FinOps audit advice non-enforcing](./bl-027-keep-finops-audit-advice-non-enforcing.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-015 - Support remediation now and avoidance of repeat problems](../voc/voc-015-support-remediation-now-and-avoidance-of-repeat-problems.md) - source classification: Desired outcome.
- [VOC-005 - Offer help and a solution alongside each problem](../voc/voc-005-offer-help-and-a-solution-alongside-each-problem.md) - source classification: Customer ask.
- [VOC-024 - Allow teams to remediate through their own deployment method](../voc/voc-024-allow-teams-to-remediate-through-their-own-deployment-method.md) - source classification: Existing-state constraint.
- [VOC-026 - Keep organizational skilling outside this engagement](../voc/voc-026-keep-organizational-skilling-outside-this-engagement.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

This is finding-specific enablement, not a company-wide Azure curriculum or enforcement program.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
