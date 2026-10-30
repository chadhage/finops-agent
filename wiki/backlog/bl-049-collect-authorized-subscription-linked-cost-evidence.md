# BL-049 - Collect authorized subscription-linked cost evidence

Use the current RBAC context for relevant cost records even when their storage is outside the subscription.

**Force rank:** 77 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 3 = **3.000**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-28

## User story

As a FinOps analyst, I want authorized cost data linked to selected subscriptions so that logical scope is preserved without excluding relevant external records.

## Acceptance criteria

1. Collected records retain subscription linkage, source, period, currency, retrieval time, and permission context.
2. Physical storage outside a subscription does not by itself exclude an authorized subscription-linked record.
3. Access failures and unavailable records are explicit; no broader billing permission or zero-cost fallback is inferred.

## Priority and Kano rationale

- **Cost of delay:** An incorrect physical-storage assumption could make the FinOps output incomplete despite valid subscription access.
- **Duration estimate:** A moderate scoped cost-collection adapter using current authentication and explicit permission errors.
- **Kano hypothesis:** An assessment should not omit relevant permitted cost data or overstate the access it actually has.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md); [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-051 - Collect subscription-linked cost data through the appropriate RBAC context](../voc/voc-051-collect-subscription-linked-cost-data-through-the-appropriate-rbac-context.md) - source classification: Existing-state constraint.
- [VOC-027 - Keep the assessment focused on the selected subscriptions](../voc/voc-027-keep-the-assessment-focused-on-the-selected-subscriptions.md) - source classification: Existing-state constraint.
- [VOC-050 - Respect PIM elevation and approval tiers for central access](../voc/voc-050-respect-pim-elevation-and-approval-tiers-for-central-access.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

No tenant-wide cost collection or automatic access expansion beyond the approved logical boundary.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
