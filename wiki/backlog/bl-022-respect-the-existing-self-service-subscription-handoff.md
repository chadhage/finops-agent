# BL-022 - Respect the existing self-service subscription handoff

Use current provisioning metadata and accountable approvals without inserting a new central vending process.

**Force rank:** 55 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 6 / 1 = **6.000**  
**Relative cost of delay:** 6/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 1 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-28

## User story

As a central FinOps operator, I want the product to consume existing self-service ownership and cost metadata so that it does not replace subscription vending.

## Acceptance criteria

1. The handoff identifies existing technical-owner, cost-center, and application-service inputs without creating a new approval chain.
2. Assessment prerequisites are separate from subscription creation prerequisites.
3. The product does not assume that central FinOps created each subscription or certified its owner's Azure skills.

## Priority and Kano rationale

- **Cost of delay:** A mistaken central-provisioning assumption could send product design down an unnecessary operating-model detour.
- **Duration estimate:** A small handoff contract and boundary review rather than any provisioning implementation.
- **Kano hypothesis:** The assessment should not disrupt the established subscription creation and accountability workflow.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-007 - Agree the product goals and workflow contract](./bl-007-agree-the-product-goals-and-workflow-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-022 - Respect self-service subscription vending and accountable approvals](../voc/voc-022-respect-self-service-subscription-vending-and-accountable-approvals.md) - source classification: Existing-state constraint.
- [VOC-023 - Do not equate subscription issuance with Azure expertise](../voc/voc-023-do-not-equate-subscription-issuance-with-azure-expertise.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

No ServiceNow vending redesign, subscription provisioning, or new user qualification barrier.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
