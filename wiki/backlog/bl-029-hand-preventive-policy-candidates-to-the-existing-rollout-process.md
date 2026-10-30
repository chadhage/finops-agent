# BL-029 - Hand preventive policy candidates to the existing rollout process

Prepare evidence for ring-based governance review instead of deploying new policy from the assessment.

**Force rank:** 84 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 5 / 2 = **2.500**  
**Relative cost of delay:** 5/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Next / R2 - validated local-product expansion  
**Roadmap initiative:** [RM-005 - Improve contextual optimization and follow-up](../roadmap/rm-005-improve-contextual-optimization-and-follow-up.md)  
**Planning date:** 2026-10-28

## User story

As a policy owner, I want preventive candidates handed to the established governance process so that audit or enforcement decisions use the correct rollout controls.

## Acceptance criteria

1. The handoff records the observed problem, proposed preventive benefit, uncertainty, and accountable policy owner.
2. The existing ring framework and audit-versus-enforcement decision are explicitly preserved.
3. No assessment output deploys policy, changes a ring, or claims approval for an estate-wide rollout.

## Priority and Kano rationale

- **Cost of delay:** A later prevention proposal could bypass the customer's blast-radius controls without an explicit handoff.
- **Duration estimate:** A small policy-candidate review artifact, not policy authoring or rollout automation.
- **Kano hypothesis:** Respecting established policy rollout safeguards is expected whenever a preventive follow-on is proposed.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-015 - Pair guided fixes with recurrence-prevention explanations](./bl-015-pair-guided-fixes-with-recurrence-prevention-explanations.md); [BL-027 - Keep FinOps audit advice non-enforcing](./bl-027-keep-finops-audit-advice-non-enforcing.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-030 - Respect the staged rollout model for any policy-related follow-on](../voc/voc-030-respect-the-staged-rollout-model-for-any-policy-related-follow-on.md) - source classification: Existing-state constraint.
- [VOC-015 - Support remediation now and avoidance of repeat problems](../voc/voc-015-support-remediation-now-and-avoidance-of-repeat-problems.md) - source classification: Desired outcome.
- [VOC-057 - Park landing-zone redesign; capture only supported high-benefit insights](../voc/voc-057-park-landing-zone-redesign-capture-only-supported-high-benefit-insights.md) - source classification: Future / adjacent topic.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Only prepare a governance handoff; landing-zone redesign and policy implementation remain separately authorized work.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
