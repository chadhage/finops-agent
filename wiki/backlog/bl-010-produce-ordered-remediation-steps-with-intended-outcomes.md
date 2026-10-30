# BL-010 - Produce ordered remediation steps with intended outcomes

Turn recommendations into an explicit sequence an owner can follow and validate.

**Force rank:** 73 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
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

As an application owner, I want ordered, verifiable steps so that I can understand what to change and the outcome each change is intended to produce.

## Acceptance criteria

1. Each actionable recommendation identifies prerequisites, ordered steps, intended outcome, and a verification check.
2. Unknown application constraints or required owner decisions block prescriptive instructions and become explicit questions.
3. The output distinguishes a proposed step from a completed change and supports the team's chosen deployment method.

## Priority and Kano rationale

- **Cost of delay:** A table of information without actionable steps can leave reported opportunities unaddressed.
- **Duration estimate:** A moderate step-generation and validation slice using the finding contract and supported execution paths.
- **Kano hypothesis:** More actionable sequencing should improve the practical value of recommendations.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md); [BL-024 - Support deployment-neutral remediation guidance](./bl-024-support-deployment-neutral-remediation-guidance.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-010 - Provide an actionable, ordered sequence of changes](../voc/voc-010-provide-an-actionable-ordered-sequence-of-changes.md) - source classification: Customer ask.
- [VOC-005 - Offer help and a solution alongside each problem](../voc/voc-005-offer-help-and-a-solution-alongside-each-problem.md) - source classification: Customer ask.
- [VOC-015 - Support remediation now and avoidance of repeat problems](../voc/voc-015-support-remediation-now-and-avoidance-of-repeat-problems.md) - source classification: Desired outcome.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Provide guidance, not automatic resource changes or a promise that every finding is safely fixable from infrastructure metadata alone.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
