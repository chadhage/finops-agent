# BL-033 - Prototype configuration-defect versus unused-resource diagnosis

Identify supported misconfiguration candidates without automatically classifying them as deletable waste.

**Force rank:** 102 of 104  
**Kano tag:** `delighter` (analyst hypothesis)  
**CD3:** 6 / 8 = **0.750**  
**Relative cost of delay:** 6/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 8 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Next / R2 - validated local-product expansion  
**Roadmap initiative:** [RM-005 - Improve contextual optimization and follow-up](../roadmap/rm-005-improve-contextual-optimization-and-follow-up.md)  
**Planning date:** 2026-10-28

## User story

As a resource owner, I want possible configuration defects distinguished from genuinely unused resources so that I can investigate a fix before considering deletion.

## Acceptance criteria

1. The prototype states which permitted evidence supports a possible configuration defect and which facts remain unknown.
2. Approved examples distinguish a supported defect candidate, genuinely unused owner-confirmed resource, legitimate low use, and insufficient evidence.
3. The gateway example is labeled illustrative, and any proposed fix still requires owner validation and appropriate expertise.

## Priority and Kano rationale

- **Cost of delay:** The customer welcomed diagnosis, but feasibility and the frequency of relevant cases are not established.
- **Duration estimate:** A substantial diagnostic prototype with evidence sufficiency checks and realistic negative cases; application-specific context is uncertain.
- **Kano hypothesis:** Explaining why an apparently unused resource is not working could add value beyond a basic waste report.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-031 - Create a human review path for ambiguous optimization](./bl-031-create-a-human-review-path-for-ambiguous-optimization.md); [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-034 - Distinguish configuration defects from genuinely unused resources](../voc/voc-034-distinguish-configuration-defects-from-genuinely-unused-resources.md) - source classification: Customer-confirmed opportunity.
- [VOC-035 - Leave the fix-versus-delete decision with the resource owner](../voc/voc-035-leave-the-fix-versus-delete-decision-with-the-resource-owner.md) - source classification: Existing-state constraint.
- [VOC-037 - Validate application knowledge and read-access limits for architecture advice](../voc/voc-037-validate-application-knowledge-and-read-access-limits-for-architecture-advice.md) - source classification: Open validation question.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not assume traffic telemetry or data-plane access exists, assert a real Zava incident, or perform a fix.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
