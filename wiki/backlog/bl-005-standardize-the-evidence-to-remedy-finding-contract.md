# BL-005 - Standardize the evidence-to-remedy finding contract

Require each finding to explain the issue, evidence, candidate remedy, owner, uncertainty, and support.

**Force rank:** 56 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 2 = **5.000**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** enabler  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want each reported problem to include its evidence and a practical next step so that I can make an informed response.

## Acceptance criteria

1. The versioned contract includes a stable finding ID, selected scope, evidence and collection time, observed condition, proposed action, intended outcome, owner, support route, and uncertainty.
2. Required missing evidence or ownership is labeled explicitly rather than filled with an invented value.
3. Representative FinOps and security outputs preserve source content and distinguish observations, examples, and analyst proposals.

## Priority and Kano rationale

- **Cost of delay:** The finding contract is the shared basis for reporting, action steps, support mapping, and handoff.
- **Duration estimate:** A bounded schema and representative-output adaptation; it reuses existing finding content.
- **Kano hypothesis:** A report that identifies problems without trustworthy evidence or a next step fails the basic usefulness expectation.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-007 - Agree the product goals and workflow contract](./bl-007-agree-the-product-goals-and-workflow-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-005 - Offer help and a solution alongside each problem](../voc/voc-005-offer-help-and-a-solution-alongside-each-problem.md) - source classification: Customer ask.
- [VOC-009 - Improve report presentation, not just finding content](../voc/voc-009-improve-report-presentation-not-just-finding-content.md) - source classification: Existing-state constraint.
- [VOC-010 - Provide an actionable, ordered sequence of changes](../voc/voc-010-provide-an-actionable-ordered-sequence-of-changes.md) - source classification: Customer ask.
- [VOC-014 - Use pre-analysis to avoid repeating basic discovery](../voc/voc-014-use-pre-analysis-to-avoid-repeating-basic-discovery.md) - source classification: Desired outcome.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Standardize existing findings before adding unrelated detectors; schema adoption is not proof of remediation.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
