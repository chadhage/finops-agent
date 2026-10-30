# BL-011 - Expose the largest defensible report opportunities

Make significant opportunities visible while separating measured, estimated, and unknown impact.

**Force rank:** 82 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 3 = **2.667**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want the biggest supported opportunities highlighted so that I can focus on the most worthwhile validated actions.

## Acceptance criteria

1. The report identifies the evidence and assumptions used to highlight an opportunity.
2. Measured amounts, scenario estimates, and unknown impact are visibly different; missing cost is not zero.
3. A deterministic display order handles unknown or incomparable impacts without fabricating savings or combining unrelated security and cost scales.

## Priority and Kano rationale

- **Cost of delay:** Owners can overlook higher-value actions when the report gives every finding the same visual weight.
- **Duration estimate:** A moderate ranking and evidence-presentation slice over current findings and authorized cost inputs.
- **Kano hypothesis:** Better visibility of meaningful opportunities should improve how owners allocate their attention.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md); [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-011 - Make the largest opportunities visible](../voc/voc-011-make-the-largest-opportunities-visible.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Report opportunity ordering is separate from this product backlog's relative CD3 ranking.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
