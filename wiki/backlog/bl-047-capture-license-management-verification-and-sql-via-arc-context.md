# BL-047 - Capture license-management verification and SQL-via-Arc context

Record entitlement evidence and the customer's reported SQL licensing approach before generating benefit advice.

**Force rank:** 62 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 2 = **4.500**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** enabler  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-004 - Make commercial recommendations safe](../roadmap/rm-004-make-commercial-recommendations-safe.md)  
**Planning date:** 2026-10-28

## User story

As a licensing stakeholder, I want benefit assumptions reviewed by license management so that the report reflects the current authorized position.

## Acceptance criteria

1. The record distinguishes customer-reported, pending validation, confirmed eligible, confirmed ineligible, and expired or changed evidence.
2. The reported SQL-via-Arc arrangement is retained as context without asserting purchased licenses or a guaranteed discount.
3. The record identifies the responsible license-management confirmation route and evidence date, with unknown states explicit.

## Priority and Kano rationale

- **Cost of delay:** Without a licensing evidence record, the report cannot safely distinguish confirmed entitlement from customer reports or unknowns.
- **Duration estimate:** A small responsible-team handoff and evidence-state model, not an automated licensing audit.
- **Kano hypothesis:** A generic saving suggestion is not an acceptable substitute for verified licensing authority.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-007 - Agree the product goals and workflow contract](./bl-007-agree-the-product-goals-and-workflow-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-049 - Confirm entitlement with license management and account for SQL via Arc](../voc/voc-049-confirm-entitlement-with-license-management-and-account-for-sql-via-arc.md) - source classification: Existing-state constraint.
- [VOC-048 - Exclude Windows and SQL Hybrid Benefit advice under current entitlements](../voc/voc-048-exclude-windows-and-sql-hybrid-benefit-advice-under-current-entitlements.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not certify legal entitlement, buy licenses, alter Arc configuration, or independently assert the reported agreement terms.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
