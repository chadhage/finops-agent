# BL-001 - Define the report-to-owner decision path

Give each evaluation a clear action, support, or justified no-change outcome.

**Force rank:** 60 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 9 / 2 = **4.500**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want to see whether to act, seek help, or make no change so that an evaluation leads to an accountable decision.

## Acceptance criteria

1. The workflow defines proposed action, owner review, support requested, and justified no-change outcomes with explicit transition evidence.
2. A satisfactory assessment can end in no change without being marked failed or forced into a workshop.
3. Each decision records the accountable owner, related finding IDs, rationale, and unresolved validation questions.

## Priority and Kano rationale

- **Cost of delay:** An unclear handoff can stall every report even when its findings are correct.
- **Duration estimate:** A small decision-state and report-presentation slice built on the finding and ownership contracts.
- **Kano hypothesis:** A clearer decision path should make evaluation results more useful to owners.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md); [BL-021 - Make owner remediation responsibility explicit](./bl-021-make-owner-remediation-responsibility-explicit.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-001 - Define the evaluation-to-action or no-action path](../voc/voc-001-define-the-evaluation-to-action-or-no-action-path.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Define and present owner decisions; do not execute remediation or make the workshop compulsory.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
