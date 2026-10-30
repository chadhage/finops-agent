# BL-014 - Package reusable report evidence for workshop handoff

Give facilitators the scope, findings, ownership, prior context, and open questions needed to avoid basic rediscovery.

**Force rank:** 74 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 9 / 3 = **3.000**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-003 - Prove finding-led workshops and support adoption](../roadmap/rm-003-prove-finding-led-workshops-and-support-adoption.md)  
**Planning date:** 2026-10-28

## User story

As a facilitator, I want a trustworthy pre-analysis packet so that I can start from known findings instead of repeating basic exploration.

## Acceptance criteria

1. The packet includes the approved subscription manifest, finding IDs, evidence timestamps, owners, proposed steps, cost assumptions, and known gaps.
2. Ownership freshness, licensing suppression, and central purchase routing are preserved in the exported artifact.
3. Unresolved application questions are explicit; the packet never promises that all discovery has been eliminated.

## Priority and Kano rationale

- **Cost of delay:** Repeated basic discovery consumes the workshop time the customer wants to spend on useful action.
- **Duration estimate:** A moderate evidence-packaging slice over scoped reports and already-defined safeguards.
- **Kano hypothesis:** A more complete handoff should reduce wasted workshop time and improve relevance.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-008 - Build an explicit project-to-subscription assessment manifest](./bl-008-build-an-explicit-project-to-subscription-assessment-manifest.md); [BL-009 - Improve report readability using existing content](./bl-009-improve-report-readability-using-existing-content.md); [BL-010 - Produce ordered remediation steps with intended outcomes](./bl-010-produce-ordered-remediation-steps-with-intended-outcomes.md); [BL-011 - Expose the largest defensible report opportunities](./bl-011-expose-the-largest-defensible-report-opportunities.md); [BL-020 - Validate ownership freshness before report routing](./bl-020-validate-ownership-freshness-before-report-routing.md); [BL-027 - Keep FinOps audit advice non-enforcing](./bl-027-keep-finops-audit-advice-non-enforcing.md); [BL-046 - Suppress unentitled Windows and SQL Hybrid Benefit advice](./bl-046-suppress-unentitled-windows-and-sql-hybrid-benefit-advice.md); [BL-042 - Route commitment purchase candidates to central evaluation](./bl-042-route-commitment-purchase-candidates-to-central-evaluation.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-014 - Use pre-analysis to avoid repeating basic discovery](../voc/voc-014-use-pre-analysis-to-avoid-repeating-basic-discovery.md) - source classification: Desired outcome.
- [VOC-008 - Report across each project area, not only one subscription](../voc/voc-008-report-across-each-project-area-not-only-one-subscription.md) - source classification: Customer ask.
- [VOC-019 - Use the named ServiceNow technical owner, not RBAC alone](../voc/voc-019-use-the-named-servicenow-technical-owner-not-rbac-alone.md) - source classification: Existing-state constraint.
- [VOC-020 - Maintain ownership changes in ServiceNow for correct routing](../voc/voc-020-maintain-ownership-changes-in-servicenow-for-correct-routing.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Reuse only authorized evidence and approved distribution routes; do not copy credentials or assume raw data may be shared externally.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
