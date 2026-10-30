# BL-038 - Confirm Zava subscription coverage using explicit IDs

Create a customer-validated pilot population rather than treating mutable names as a complete inventory.

**Force rank:** 58 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 2 = **5.000**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** enabler  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-28

## User story

As a pilot sponsor, I want the selected Zava subscription IDs explicitly validated so that report completeness is not inferred from naming conventions.

## Acceptance criteria

1. The manifest records exact IDs, approved selection origin, validation date, and intended pilot boundary.
2. Names remain descriptive metadata and a rename does not change subscription identity or silently drop coverage.
3. Customer-reported estate counts are not used as a verified inventory or permission to scan the wider environment.

## Priority and Kano rationale

- **Cost of delay:** A name-only population could omit subscriptions or falsely imply complete Zava coverage.
- **Duration estimate:** A small manifest validation and provenance slice, not discovery of the wider estate.
- **Kano hypothesis:** Correctly identifying the intended population is basic assessment correctness.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-007 - Agree the product goals and workflow contract](./bl-007-agree-the-product-goals-and-workflow-contract.md); [BL-051 - Define the Zava pilot go-no-go contract](./bl-051-define-the-zava-pilot-go-no-go-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-039 - Do not rely on subscription names for complete Zava coverage](../voc/voc-039-do-not-rely-on-subscription-names-for-complete-zava-coverage.md) - source classification: Existing-state constraint.
- [VOC-027 - Keep the assessment focused on the selected subscriptions](../voc/voc-027-keep-the-assessment-focused-on-the-selected-subscriptions.md) - source classification: Existing-state constraint.
- [VOC-054 - Keep Zava as the current POC; defer regular global automation](../voc/voc-054-keep-zava-as-the-current-poc-defer-regular-global-automation.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Validate the selected population with the customer; do not claim a complete tenant inventory from names.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
