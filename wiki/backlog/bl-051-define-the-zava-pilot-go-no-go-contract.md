# BL-051 - Define the Zava pilot go-no-go contract

Specify evidence required to complete the current POC before broader product investment.

**Force rank:** 53 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 1 = **9.000**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 1 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** enabler  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-28

## User story

As a sponsor, I want explicit pilot exit criteria so that a broader product is considered only after the Zava-first outcome is reviewed.

## Acceptance criteria

1. The contract requires scoped local access, trustworthy reports, commercial guardrails, the two-subscription dry run, and representative Zava-team feedback.
2. The record names responsible decision functions and distinguishes proposed, evidenced, accepted, and blocked criteria.
3. Wider scope, scheduled automation, and new infrastructure require a separate approval decision after R1 evidence review.

## Priority and Kano rationale

- **Cost of delay:** An undefined exit gate can let scope drift into a wider estate before the customer workflow is validated.
- **Duration estimate:** A small acceptance and decision-authority contract, separate from performing the actual pilot.
- **Kano hypothesis:** A credible expansion decision needs explicit pilot evidence rather than an assumed successful POC.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-007 - Agree the product goals and workflow contract](./bl-007-agree-the-product-goals-and-workflow-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-054 - Keep Zava as the current POC; defer regular global automation](../voc/voc-054-keep-zava-as-the-current-poc-defer-regular-global-automation.md) - source classification: Existing-state constraint.
- [VOC-003 - Design for the other Zava teams, not only the FinOps team](../voc/voc-003-design-for-the-other-zava-teams-not-only-the-finops-team.md) - source classification: Customer ask.
- [VOC-007 - Make the intended process and goals explicit before diving in](../voc/voc-007-make-the-intended-process-and-goals-explicit-before-diving-in.md) - source classification: Customer ask.
- [VOC-016 - Dry-run the current output using the two FinOps subscriptions](../voc/voc-016-dry-run-the-current-output-using-the-two-finops-subscriptions.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Writing the contract does not mark the pilot complete, verify customer-reported estate counts, or approve a global rollout.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
