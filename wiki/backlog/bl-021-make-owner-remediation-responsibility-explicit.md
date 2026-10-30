# BL-021 - Make owner remediation responsibility explicit

State who must decide and act while separating Microsoft guidance from remediation ownership.

**Force rank:** 47 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 1 = **10.000**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 1 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want the report to distinguish my decision responsibility from available Microsoft help so that next steps are not assigned to the wrong team.

## Acceptance criteria

1. Every routed recommendation identifies the owning team or an explicit unresolved ownership gap.
2. Report and workshop wording state that guidance does not transfer decision or remediation responsibility.
3. No output implies centrally enforced remediation, an executed change, or delegated authority without separate approval.

## Priority and Kano rationale

- **Cost of delay:** Ambiguous responsibility can block action or create an unintended expectation that a central team will fix everything.
- **Duration estimate:** A small owner-responsibility field and reviewed message pattern over resolved ownership.
- **Kano hypothesis:** Preserving the established responsibility boundary is essential to trusted advice.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-019 - Resolve accountable owners from ServiceNow records](./bl-019-resolve-accountable-owners-from-servicenow-records.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-021 - Keep remediation responsibility with the owning team](../voc/voc-021-keep-remediation-responsibility-with-the-owning-team.md) - source classification: Existing-state constraint.
- [VOC-019 - Use the named ServiceNow technical owner, not RBAC alone](../voc/voc-019-use-the-named-servicenow-technical-owner-not-rbac-alone.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Clarify the current operating model; do not redesign it or assign new responsibility to named individuals.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
