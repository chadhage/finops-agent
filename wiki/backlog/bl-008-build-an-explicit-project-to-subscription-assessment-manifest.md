# BL-008 - Build an explicit project-to-subscription assessment manifest

Run FinOps and security analysis for an owner-validated project area that can span multiple subscriptions.

**Force rank:** 72 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 3 = **3.000**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want one explicit assessment boundary for my selected subscriptions so that multi-subscription workloads are represented correctly.

## Acceptance criteria

1. The manifest lists owner-approved project areas and exact subscription IDs, allowing one workload to span multiple subscriptions.
2. Both FinOps and security coverage are recorded per included subscription, including access failures and unavailable outputs.
3. A missing subscription or analysis result is visible as incomplete coverage, not silently excluded or treated as clean.

## Priority and Kano rationale

- **Cost of delay:** A subscription-only assumption can omit relevant findings and route an incomplete report to owners.
- **Duration estimate:** A moderate manifest and coverage-adapter slice using authorized scope rather than a new inventory platform.
- **Kano hypothesis:** Missing part of the selected workload would make a supposedly complete project report untrustworthy.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md); [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-008 - Report across each project area, not only one subscription](../voc/voc-008-report-across-each-project-area-not-only-one-subscription.md) - source classification: Customer ask.
- [VOC-040 - Allow a workload to span multiple subscriptions](../voc/voc-040-allow-a-workload-to-span-multiple-subscriptions.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not infer workload membership from names or impose one universal application-service convention.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
