# BL-042 - Route commitment purchase candidates to central evaluation

Prevent report instructions that tell application owners to buy savings plans or reservations directly.

**Force rank:** 50 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 1 = **10.000**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 1 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-004 - Make commercial recommendations safe](../roadmap/rm-004-make-commercial-recommendations-safe.md)  
**Planning date:** 2026-10-28

## User story

As a central FinOps decision maker, I want commitment candidates routed to my evaluation so that local reports cannot bypass portfolio controls.

## Acceptance criteria

1. Every purchase candidate identifies central evaluation as the next step and records the relevant scope and assumptions.
2. Missing global coverage or approval leaves the candidate pending, not recommended for immediate self-purchase.
3. Tests produce no owner-facing direct-purchase instruction or executed purchase.

## Priority and Kano rationale

- **Cost of delay:** The customer reports historical waste from uninformed commitment purchases and explicitly centralizes purchase authority.
- **Duration estimate:** A small recommendation-routing and message guardrail, not a purchase workflow engine.
- **Kano hypothesis:** Respecting established purchase authority is a basic commercial safety expectation.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-044 - Route savings-plan and reservation purchases through the central team](../voc/voc-044-route-savings-plan-and-reservation-purchases-through-the-central-team.md) - source classification: Existing-state constraint.
- [VOC-045 - Check shared global commitment utilization before adding purchases](../voc/voc-045-check-shared-global-commitment-utilization-before-adding-purchases.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not buy, renew, exchange, or cancel commitments and do not imply central approval has already occurred.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
