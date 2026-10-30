# BL-045 - Surface resource-change risk in commitment candidates

Ask about expected resource changes before treating reservation coverage as stable.

**Force rank:** 83 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 8 / 3 = **2.667**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-004 - Make commercial recommendations safe](../roadmap/rm-004-make-commercial-recommendations-safe.md)  
**Planning date:** 2026-10-28

## User story

As a commitment evaluator, I want planned resource changes visible so that I do not mistake today's configuration for guaranteed future demand.

## Acceptance criteria

1. Candidate intake asks about planned resource, service, and usage changes relevant to commitment fit.
2. Unknown stability is explicit and prevents an unconditional reservation recommendation.
3. A fixture with a changed resource shows potential underutilization exposure without inventing estate-wide financial loss.

## Priority and Kano rationale

- **Cost of delay:** The customer reports recurring underutilization when resources change, making stability a relevant decision input.
- **Duration estimate:** A moderate candidate-intake and risk-presentation slice; it does not build a demand forecasting engine.
- **Kano hypothesis:** Ignoring a known source of commitment waste would undermine basic commercial trust.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-044 - Encode customer-specific commitment preference rules](./bl-044-encode-customer-specific-commitment-preference-rules.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-047 - Account for reservation waste when resources change](../voc/voc-047-account-for-reservation-waste-when-resources-change.md) - source classification: Reported problem / risk.
- [VOC-046 - Prefer savings plans unless reservation conditions are well established](../voc/voc-046-prefer-savings-plans-unless-reservation-conditions-are-well-established.md) - source classification: Existing-state constraint.
- [VOC-045 - Check shared global commitment utilization before adding purchases](../voc/voc-045-check-shared-global-commitment-utilization-before-adding-purchases.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not forecast guaranteed demand, calculate unsupported losses, or execute a reservation transaction.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
