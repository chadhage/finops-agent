# BL-036 - Test whether authorized evidence supports architecture advice

Establish what can and cannot be inferred from read access, infrastructure metadata, and owner-supplied application facts.

**Force rank:** 95 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 7 / 5 = **1.400**  
**Relative cost of delay:** 7/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** discovery  
**Status:** Proposed / not started.  
**Horizon / release:** Later / R3 option - feasibility-gated advanced advice  
**Roadmap initiative:** [RM-008 - Validate advanced architecture and regional advice](../roadmap/rm-008-validate-advanced-architecture-and-regional-advice.md)  
**Planning date:** 2026-10-28

## User story

As a product lead, I want a feasibility matrix for architecture advice so that advanced work starts only where the current evidence and permissions are sufficient.

## Acceptance criteria

1. The matrix distinguishes readable control-plane metadata, required owner facts, unavailable data-plane evidence, and actual permission gaps.
2. Representative candidate scenarios receive a supported, conditional, or not-supported decision with evidence.
3. Any proposed additional access is a separate approval request; the spike does not obtain it automatically or claim feasibility without it.

## Priority and Kano rationale

- **Cost of delay:** Without this decision, advanced recommendation work could be infeasible or based on unsupported assumptions.
- **Duration estimate:** A bounded technical feasibility study across representative authorized inputs and explicit missing-data cases.
- **Kano hypothesis:** A product must not overstate application understanding or request unapproved access to justify its recommendations.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md); [BL-058 - Validate a separately authorized second operating profile](./bl-058-validate-a-separately-authorized-second-operating-profile.md)

**Current readiness:** Horizon-gated (G3); prerequisites also remain proposed.

**G3:** Advanced advice is an option after R2 review, explicit sponsor approval, and sufficient permitted evidence. The feasibility spike must precede architecture candidate implementation.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-037 - Validate application knowledge and read-access limits for architecture advice](../voc/voc-037-validate-application-knowledge-and-read-access-limits-for-architecture-advice.md) - source classification: Open validation question.
- [VOC-036 - Identify cheaper service or replatforming candidates where defensible](../voc/voc-036-identify-cheaper-service-or-replatforming-candidates-where-defensible.md) - source classification: Customer-confirmed opportunity.
- [VOC-050 - Respect PIM elevation and approval tiers for central access](../voc/voc-050-respect-pim-elevation-and-approval-tiers-for-central-access.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

The study may conclude that a candidate cannot be supported; that is an explicit decision, not a hidden fallback.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
