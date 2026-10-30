# BL-025 - Route hub and spoke findings to the correct owners

Preserve central hub responsibility and application-team spoke responsibility within approved assessment scope.

**Force rank:** 75 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 3 = **3.000**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-28

## User story

As a connectivity stakeholder, I want findings routed to the responsible hub or spoke owner so that coordination follows the existing operating model.

## Acceptance criteria

1. Supported fixtures route hub findings to the hub owner and spoke-origin issues to the appropriate coordination path.
2. A shared dependency does not automatically make every dependent application responsible for a hub finding.
3. A hub outside selected authorized scope is recorded as unassessed context; the product does not scan it implicitly.

## Priority and Kano rationale

- **Cost of delay:** Incorrect connectivity routing can leave findings unresolved or assign unrelated hub issues to every application.
- **Duration estimate:** A moderate ownership-routing slice requiring resource context and multi-subscription boundaries.
- **Kano hypothesis:** Assigning connectivity findings to the responsible owner is a basic correctness requirement.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-019 - Resolve accountable owners from ServiceNow records](./bl-019-resolve-accountable-owners-from-servicenow-records.md); [BL-008 - Build an explicit project-to-subscription assessment manifest](./bl-008-build-an-explicit-project-to-subscription-assessment-manifest.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-025 - Route hub and spoke findings to their respective owners](../voc/voc-025-route-hub-and-spoke-findings-to-their-respective-owners.md) - source classification: Existing-state constraint.
- [VOC-021 - Keep remediation responsibility with the owning team](../voc/voc-021-keep-remediation-responsibility-with-the-owning-team.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not transfer connectivity ownership or use a routing need as permission to expand data collection.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
