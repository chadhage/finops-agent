# BL-016 - Dry-run current outputs on the two FinOps subscriptions

Test the current reports as an application-owner handoff and record actionable gaps.

**Force rank:** 69 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 3 = **3.333**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 3 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** validation  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-003 - Prove finding-led workshops and support adoption](../roadmap/rm-003-prove-finding-led-workshops-and-support-adoption.md)  
**Planning date:** 2026-10-28

## User story

As a product lead, I want to walk through the existing two-subscription reports as an application team so that gaps are found before broader use.

## Acceptance criteria

1. The dry run covers both FinOps and security outputs for the two named pilot subscriptions using authorized data.
2. The review records actionable recommendations, missing evidence, confusing presentation, and support gaps against stable finding IDs.
3. The result is a reviewed gap list and go/no-go input, not a claim that fixes or workshops have already occurred.

## Priority and Kano rationale

- **Cost of delay:** Without a real walkthrough, design assumptions can persist until owners encounter them in a workshop.
- **Duration estimate:** A bounded review of two existing outputs with explicit evidence and safeguard checks.
- **Kano hypothesis:** Demonstrating that the basic handoff works is expected before claiming the pilot is useful or ready to expand.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-014 - Package reusable report evidence for workshop handoff](./bl-014-package-reusable-report-evidence-for-workshop-handoff.md); [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md); [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md); [BL-034 - Require owner validation for fix-versus-delete decisions](./bl-034-require-owner-validation-for-fix-versus-delete-decisions.md); [BL-046 - Suppress unentitled Windows and SQL Hybrid Benefit advice](./bl-046-suppress-unentitled-windows-and-sql-hybrid-benefit-advice.md); [BL-042 - Route commitment purchase candidates to central evaluation](./bl-042-route-commitment-purchase-candidates-to-central-evaluation.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-016 - Dry-run the current output using the two FinOps subscriptions](../voc/voc-016-dry-run-the-current-output-using-the-two-finops-subscriptions.md) - source classification: Customer ask.
- [VOC-014 - Use pre-analysis to avoid repeating basic discovery](../voc/voc-014-use-pre-analysis-to-avoid-repeating-basic-discovery.md) - source classification: Desired outcome.
- [VOC-003 - Design for the other Zava teams, not only the FinOps team](../voc/voc-003-design-for-the-other-zava-teams-not-only-the-finops-team.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

A successful FinOps walkthrough does not replace validation with another Zava application team.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
