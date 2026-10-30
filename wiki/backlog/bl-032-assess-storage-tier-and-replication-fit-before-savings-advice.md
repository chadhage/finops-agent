# BL-032 - Assess storage tier and replication fit before savings advice

Compare cheaper storage options only after recording the workload's access and replication requirements.

**Force rank:** 94 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 7 / 5 = **1.400**  
**Relative cost of delay:** 7/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Next / R2 - validated local-product expansion  
**Roadmap initiative:** [RM-005 - Improve contextual optimization and follow-up](../roadmap/rm-005-improve-contextual-optimization-and-follow-up.md)  
**Planning date:** 2026-10-28

## User story

As a storage owner, I want cheaper tier or replication candidates checked against my requirements so that cost advice does not undermine the workload.

## Acceptance criteria

1. The assessment records observed configuration, available usage evidence, owner access requirements, and replication requirements.
2. Missing requirements produce a validation question rather than a prescriptive downgrade.
3. Approved fixtures cover a valid cheaper candidate, a required expensive configuration, and insufficient evidence without invented savings.

## Priority and Kano rationale

- **Cost of delay:** Storage optimization is an explicitly requested example, but generic downgrades could violate application needs.
- **Duration estimate:** A larger rule-and-evidence slice covering two configuration dimensions, owner requirements, and cost assumptions.
- **Kano hypothesis:** More accurate fit-for-purpose storage advice should increase the usefulness of optimization reports.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-031 - Create a human review path for ambiguous optimization](./bl-031-create-a-human-review-path-for-ambiguous-optimization.md); [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-033 - Optimize storage tiers and replication only when they still fit the need](../voc/voc-033-optimize-storage-tiers-and-replication-only-when-they-still-fit-the-need.md) - source classification: Desired outcome.
- [VOC-028 - Treat FinOps audit findings as advice, not enforced tier bans](../voc/voc-028-treat-finops-audit-findings-as-advice-not-enforced-tier-bans.md) - source classification: Existing-state constraint.
- [VOC-032 - Handle ambiguous optimization findings with human judgment](../voc/voc-032-handle-ambiguous-optimization-findings-with-human-judgment.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not assert that hot storage or geo-replication is always waste, and do not change either setting.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
