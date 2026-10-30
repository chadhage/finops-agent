# BL-044 - Encode customer-specific commitment preference rules

Reflect the reported savings-plan preference while making reservation eligibility a validated exception.

**Force rank:** 66 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 8 / 2 = **4.000**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-004 - Make commercial recommendations safe](../roadmap/rm-004-make-commercial-recommendations-safe.md)  
**Planning date:** 2026-10-28

## User story

As a central FinOps reviewer, I want recommendation rules to reflect our current commitment guidance so that exceptions require explicit evidence.

## Acceptance criteria

1. The Zava profile records the reported savings-plan preference and the need to validate reservation conditions.
2. A reservation candidate requires recorded fit assumptions and central review rather than becoming the default purchase instruction.
3. The rule is labeled customer-specific and revalidatable, not a universal Azure product recommendation.

## Priority and Kano rationale

- **Cost of delay:** Defaulting to reservations would conflict with the customer's current guidance and recurring utilization concerns.
- **Duration estimate:** A small profile rule and explanation slice, separate from cost forecasting or purchase execution.
- **Kano hypothesis:** Commercial advice should respect the customer's stated decision policy rather than generic defaults.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-042 - Route commitment purchase candidates to central evaluation](./bl-042-route-commitment-purchase-candidates-to-central-evaluation.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-046 - Prefer savings plans unless reservation conditions are well established](../voc/voc-046-prefer-savings-plans-unless-reservation-conditions-are-well-established.md) - source classification: Existing-state constraint.
- [VOC-044 - Route savings-plan and reservation purchases through the central team](../voc/voc-044-route-savings-plan-and-reservation-purchases-through-the-central-team.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not assert savings-plan suitability for every workload or claim any purchase has been approved.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
