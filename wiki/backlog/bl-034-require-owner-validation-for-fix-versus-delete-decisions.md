# BL-034 - Require owner validation for fix-versus-delete decisions

Keep resource deletion authority with the owning team regardless of utilization signals.

**Force rank:** 49 of 104  
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

As a resource owner, I want fix or delete recommendations presented for my validation so that utilization alone never becomes authorization to remove a resource.

## Acceptance criteria

1. Every deletion candidate states that the owner must validate whether the resource is needed.
2. Low utilization or a suspected defect cannot produce an approved-for-deletion state without explicit owner evidence.
3. The report preserves fix, retain, investigate, and delete-as-owner-decision alternatives without executing any of them.

## Priority and Kano rationale

- **Cost of delay:** Confusing apparent waste with deletion permission creates a high-consequence trust failure.
- **Duration estimate:** A small decision-authority field and report guardrail; no deletion engine or approval service is built.
- **Kano hypothesis:** Owners expect advisory analysis not to authorize destructive decisions on their behalf.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-021 - Make owner remediation responsibility explicit](./bl-021-make-owner-remediation-responsibility-explicit.md); [BL-027 - Keep FinOps audit advice non-enforcing](./bl-027-keep-finops-audit-advice-non-enforcing.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-035 - Leave the fix-versus-delete decision with the resource owner](../voc/voc-035-leave-the-fix-versus-delete-decision-with-the-resource-owner.md) - source classification: Existing-state constraint.
- [VOC-021 - Keep remediation responsibility with the owning team](../voc/voc-021-keep-remediation-responsibility-with-the-owning-team.md) - source classification: Existing-state constraint.
- [VOC-034 - Distinguish configuration defects from genuinely unused resources](../voc/voc-034-distinguish-configuration-defects-from-genuinely-unused-resources.md) - source classification: Customer-confirmed opportunity.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

No automatic delete operation, permission grant, or implied central decision authority.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
