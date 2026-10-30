# BL-035 - Prototype evidence-qualified cheaper-service candidates

Flag potential replatforming alternatives only when required application behavior and cost assumptions can be assessed.

**Force rank:** 103 of 104  
**Kano tag:** `delighter` (analyst hypothesis)  
**CD3:** 6 / 8 = **0.750**  
**Relative cost of delay:** 6/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 8 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Later / R3 option - feasibility-gated advanced advice  
**Roadmap initiative:** [RM-008 - Validate advanced architecture and regional advice](../roadmap/rm-008-validate-advanced-architecture-and-regional-advice.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want qualified cheaper-service candidates so that I can investigate alternatives without mistaking a lower unit price for a validated migration.

## Acceptance criteria

1. Each approved candidate lists required functional behavior, evidence of possible equivalence, missing application facts, and owner validation questions.
2. The comparison records pricing and commitment assumptions and does not claim savings where inputs are unavailable.
3. Insufficient evidence produces no prescriptive recommendation; examples such as static web apps remain candidates rather than actual migration findings.

## Priority and Kano rationale

- **Cost of delay:** The customer welcomed cheaper equivalents, but application knowledge and access feasibility remain open.
- **Duration estimate:** A substantial candidate-comparison prototype covering functional fit, architecture context, and commercial assumptions.
- **Kano hypothesis:** A credible alternative architecture could provide unexpected value beyond configuration-level findings.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-036 - Test whether authorized evidence supports architecture advice](./bl-036-test-whether-authorized-evidence-supports-architecture-advice.md); [BL-043 - Add authorized shared-commitment coverage evidence](./bl-043-add-authorized-shared-commitment-coverage-evidence.md)

**Current readiness:** Horizon-gated (G3); prerequisites also remain proposed.

**G3:** Advanced advice is an option after R2 review, explicit sponsor approval, and sufficient permitted evidence. The feasibility spike must precede architecture candidate implementation.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-036 - Identify cheaper service or replatforming candidates where defensible](../voc/voc-036-identify-cheaper-service-or-replatforming-candidates-where-defensible.md) - source classification: Customer-confirmed opportunity.
- [VOC-037 - Validate application knowledge and read-access limits for architecture advice](../voc/voc-037-validate-application-knowledge-and-read-access-limits-for-architecture-advice.md) - source classification: Open validation question.
- [VOC-045 - Check shared global commitment utilization before adding purchases](../voc/voc-045-check-shared-global-commitment-utilization-before-adding-purchases.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

No automatic migration, service deployment, assumed application equivalence, or data-plane access expansion.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
