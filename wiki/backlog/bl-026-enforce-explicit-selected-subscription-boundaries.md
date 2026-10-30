# BL-026 - Enforce explicit selected-subscription boundaries

Keep collection and findings within the approved logical scope and expose excluded context.

**Force rank:** 57 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 2 = **5.000**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-28

## User story

As an operator, I want an enforced selected-subscription boundary so that the assessment does not drift into management-group redesign or unapproved estate analysis.

## Acceptance criteria

1. Every collection request is associated with an approved subscription ID or an explicitly authorized supporting data source.
2. An unselected subscription request fails with a visible scope error and is not silently assessed.
3. The report lists included, excluded, inaccessible, and unavailable scope without calling missing coverage clean.

## Priority and Kano rationale

- **Cost of delay:** Unbounded analysis could violate the customer's stated POC boundary and invalidate report coverage claims.
- **Duration estimate:** A small scope-validation and collector-boundary slice using an explicit manifest.
- **Kano hypothesis:** Respecting approved scope is a fundamental trust and access expectation.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-038 - Confirm Zava subscription coverage using explicit IDs](./bl-038-confirm-zava-subscription-coverage-using-explicit-ids.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-027 - Keep the assessment focused on the selected subscriptions](../voc/voc-027-keep-the-assessment-focused-on-the-selected-subscriptions.md) - source classification: Existing-state constraint.
- [VOC-051 - Collect subscription-linked cost data through the appropriate RBAC context](../voc/voc-051-collect-subscription-linked-cost-data-through-the-appropriate-rbac-context.md) - source classification: Existing-state constraint.
- [VOC-054 - Keep Zava as the current POC; defer regular global automation](../voc/voc-054-keep-zava-as-the-current-poc-defer-regular-global-automation.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

This is a logical authorized-data boundary, not a rule that relevant cost records must physically reside inside an Azure subscription.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
