# BL-009 - Improve report readability using existing content

Present existing findings in a consistent owner-facing summary and detailed evidence layout.

**Force rank:** 81 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 3 = **2.667**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want a readable report that makes the important information easy to find without hiding its evidence.

## Acceptance criteria

1. The layout separates scope and coverage, owner-facing summary, recommendations, evidence, and unresolved questions.
2. Finding IDs, source attribution, uncertainty, and navigation remain visible in representative outputs.
3. A customer review records readability issues and verifies that formatting has not altered the underlying finding meaning.

## Priority and Kano rationale

- **Cost of delay:** Hard-to-read output weakens report uptake even when most of the required content already exists.
- **Duration estimate:** A moderate template and review slice; report rendering surfaces have not been inspected as application code.
- **Kano hypothesis:** Improved clarity and formatting should increase the value owners get from the same underlying evidence.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-009 - Improve report presentation, not just finding content](../voc/voc-009-improve-report-presentation-not-just-finding-content.md) - source classification: Existing-state constraint.
- [VOC-011 - Make the largest opportunities visible](../voc/voc-011-make-the-largest-opportunities-visible.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not expand the finding catalogue or replace existing report formats without checking their current consumers.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
