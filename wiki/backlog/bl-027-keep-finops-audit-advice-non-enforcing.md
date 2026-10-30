# BL-027 - Keep FinOps audit advice non-enforcing

Present costly configurations as validation questions rather than automatic policy violations.

**Force rank:** 48 of 104  
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

As an application owner, I want audit signals presented as evidence-backed questions so that I can validate my workload requirements before changing configuration.

## Acceptance criteria

1. Audit-only findings are labeled advisory and do not claim that hot storage or another costly option is prohibited.
2. The output can record a justified decision to retain a configuration after owner review.
3. No report assumes an available per-policy exception mechanism or automatically changes policy assignment or enforcement.

## Priority and Kano rationale

- **Cost of delay:** Incorrect enforcement language could trigger inappropriate changes across many otherwise legitimate configurations.
- **Duration estimate:** A small finding-type and message-rule guardrail using existing audit semantics.
- **Kano hypothesis:** Misrepresenting advisory findings as mandatory bans would undermine report correctness and owner trust.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-028 - Treat FinOps audit findings as advice, not enforced tier bans](../voc/voc-028-treat-finops-audit-findings-as-advice-not-enforced-tier-bans.md) - source classification: Existing-state constraint.
- [VOC-033 - Optimize storage tiers and replication only when they still fit the need](../voc/voc-033-optimize-storage-tiers-and-replication-only-when-they-still-fit-the-need.md) - source classification: Desired outcome.
- [VOC-058 - Keep per-policy exception automation in the separate future scope](../voc/voc-058-keep-per-policy-exception-automation-in-the-separate-future-scope.md) - source classification: Future / adjacent topic.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not create a new tier ban, enforcement policy, or exception engine.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
