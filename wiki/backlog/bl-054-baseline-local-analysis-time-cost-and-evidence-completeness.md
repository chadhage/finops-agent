# BL-054 - Baseline local analysis time cost and evidence completeness

Measure the current workflow before claiming that any change makes analysis faster or cheaper.

**Force rank:** 88 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 7 / 3 = **2.333**  
**Relative cost of delay:** 7/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** enabler  
**Status:** Proposed / not started.  
**Horizon / release:** Next / R2 - validated local-product expansion  
**Roadmap initiative:** [RM-007 - Generalize and measure the local product](../roadmap/rm-007-generalize-and-measure-the-local-product.md)  
**Planning date:** 2026-10-28

## User story

As a product lead, I want a repeatable local baseline so that faster or cheaper analysis claims can be checked against unchanged evidence quality.

## Acceptance criteria

1. Three comparable local runs use the same approved input set, scope, and recorded environment, with raw timings and evidence counts retained.
2. Observable processing cost and its measurement basis are recorded; unavailable cost is explicitly unknown and cannot support a cheaper claim.
3. Any later comparison reports variance and evidence parity rather than inventing a percentage target, measured saving, or delivery SLA.

## Priority and Kano rationale

- **Cost of delay:** Without a comparable baseline, optimization claims and later architecture decisions cannot be evaluated credibly.
- **Duration estimate:** A moderate repeatable benchmark and measurement record, not a new telemetry service.
- **Kano hypothesis:** Measured improvements in analysis efficiency should increase value when evidence quality is preserved.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-016 - Dry-run current outputs on the two FinOps subscriptions](./bl-016-dry-run-current-outputs-on-the-two-finops-subscriptions.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-056 - Welcome faster and cheaper analysis without committing to a design](../voc/voc-056-welcome-faster-and-cheaper-analysis-without-committing-to-a-design.md) - source classification: Customer-confirmed opportunity.
- [VOC-016 - Dry-run the current output using the two FinOps subscriptions](../voc/voc-016-dry-run-the-current-output-using-the-two-finops-subscriptions.md) - source classification: Customer ask.
- [VOC-055 - Preserve the current user-authenticated terminal data path](../voc/voc-055-preserve-the-current-user-authenticated-terminal-data-path.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

No new always-on monitoring deployment, external telemetry sharing, or preselected connector architecture.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
