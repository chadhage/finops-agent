# BL-056 - Clarify future per-policy exception handoff

Record current reported exception limits and refer granular automation decisions to the separate platform program.

**Force rank:** 98 of 104  
**Kano tag:** `delighter` (analyst hypothesis)  
**CD3:** 3 / 3 = **1.000**  
**Relative cost of delay:** 3/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** parked discovery  
**Status:** Proposed / not started.  
**Horizon / release:** Later / Options register - discovery only  
**Roadmap initiative:** [RM-009 - Evaluate future execution and platform boundaries](../roadmap/rm-009-evaluate-future-execution-and-platform-boundaries.md)  
**Planning date:** 2026-10-28

## User story

As a platform policy owner, I want current exception behavior and future approval ownership documented so that the assessment does not assume unavailable per-policy automation.

## Acceptance criteria

1. The record distinguishes the reported all-or-nothing current behavior from independently validated capability and proposed future automation.
2. Any future option identifies who would approve it and which separate platform activity owns implementation.
3. The assessment never grants an exception, changes a policy assignment, or treats the proposed mechanism as currently deployed.

## Priority and Kano rationale

- **Cost of delay:** The source describes this as not in place and part of the separate 2.0 conversation rather than current delivery.
- **Duration estimate:** A bounded current-state and approval-handoff study, not construction of an exception engine.
- **Kano hypothesis:** Future granular exception capability could add flexibility, but it is outside the current product promise and remains unvalidated.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-027 - Keep FinOps audit advice non-enforcing](./bl-027-keep-finops-audit-advice-non-enforcing.md); [BL-029 - Hand preventive policy candidates to the existing rollout process](./bl-029-hand-preventive-policy-candidates-to-the-existing-rollout-process.md)

**Current readiness:** Horizon-gated (G4); prerequisites also remain proposed.

**G4:** Future execution and adjacent-platform options are discovery or handoff only. Any implementation needs separate scope, access, cost, architecture, and security approval plus a fresh estimate.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-058 - Keep per-policy exception automation in the separate future scope](../voc/voc-058-keep-per-policy-exception-automation-in-the-separate-future-scope.md) - source classification: Future / adjacent topic.
- [VOC-057 - Park landing-zone redesign; capture only supported high-benefit insights](../voc/voc-057-park-landing-zone-redesign-capture-only-supported-high-benefit-insights.md) - source classification: Future / adjacent topic.
- [VOC-028 - Treat FinOps audit findings as advice, not enforced tier bans](../voc/voc-028-treat-finops-audit-findings-as-advice-not-enforced-tier-bans.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

The estimate covers clarification and handoff only; implementing exceptions requires separate scope and prioritization.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
