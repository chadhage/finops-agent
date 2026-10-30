# BL-048 - Preflight actual RBAC capabilities and PIM state

Check current read capabilities and required approvals without assuming standing privilege or bespoke core roles.

**Force rank:** 71 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 3 = **3.333**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-28

## User story

As an operator, I want current permissions checked before collection so that read access and PIM approval requirements are respected.

## Acceptance criteria

1. The preflight records authenticated context, selected scope, effective supported read capabilities, and required but absent permissions.
2. Tests distinguish unchanged core roles from narrow custom roles, including a move-only role that does not imply broader access.
3. Missing elevation or approval is visible and blocks the affected operation; the product does not elevate itself or infer change authority from read access.

## Priority and Kano rationale

- **Cost of delay:** Incorrect permission assumptions can make collection fail or overstep the customer's established access model.
- **Duration estimate:** A moderate capability and approval preflight across selected scope, including negative permission cases.
- **Kano hypothesis:** Respecting actual access and approval boundaries is fundamental to safe data collection.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md); [BL-050 - Preserve the local user-authenticated execution contract](./bl-050-preserve-the-local-user-authenticated-execution-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-050 - Respect PIM elevation and approval tiers for central access](../voc/voc-050-respect-pim-elevation-and-approval-tiers-for-central-access.md) - source classification: Existing-state constraint.
- [VOC-052 - Distinguish standard core roles from narrow custom structural roles](../voc/voc-052-distinguish-standard-core-roles-from-narrow-custom-structural-roles.md) - source classification: Existing-state constraint.
- [VOC-037 - Validate application knowledge and read-access limits for architecture advice](../voc/voc-037-validate-application-knowledge-and-read-access-limits-for-architecture-advice.md) - source classification: Open validation question.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

No automatic PIM activation, owner grant, standing privileged identity, or approval bypass.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
