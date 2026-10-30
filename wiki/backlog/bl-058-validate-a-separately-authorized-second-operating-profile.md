# BL-058 - Validate a separately authorized second operating profile

Prove broader local-product fit beyond the initial Zava scenario before considering global execution.

**Force rank:** 97 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 6 / 5 = **1.200**  
**Relative cost of delay:** 6/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** validation  
**Status:** Proposed / not started.  
**Horizon / release:** Next / R2 - validated local-product expansion  
**Roadmap initiative:** [RM-007 - Generalize and measure the local product](../roadmap/rm-007-generalize-and-measure-the-local-product.md)  
**Planning date:** 2026-10-28

## User story

As a product sponsor, I want a separately approved second-profile pilot so that wider investment follows evidence of reusable local value.

## Acceptance criteria

1. A second operating profile and its data use are explicitly approved by the responsible owner; no approval means the pilot stays blocked.
2. The local run validates scope, ownership, grouping, licensing, commercial handoff, evidence completeness, and profile isolation against the recorded baseline.
3. The review records gaps and a broader-release decision; fixture-only testing is not represented as a successful real pilot.

## Priority and Kano rationale

- **Cost of delay:** Broader investment risks scaling untested customer-specific assumptions unless a second model is validated.
- **Duration estimate:** A bounded authorized pilot and review; participant availability, access, and local integration effort remain unknown.
- **Kano hypothesis:** Validated reuse should improve product value; a single-customer success is not enough evidence for broad applicability.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-003 - Validate the journey with another Zava application team](./bl-003-validate-the-journey-with-another-zava-application-team.md); [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md); [BL-057 - Externalize organization-specific local operating rules](./bl-057-externalize-organization-specific-local-operating-rules.md)

**Current readiness:** Horizon-gated (G2); prerequisites also remain proposed.

**G2:** Broader local-product work is gated on reviewed R1 evidence and sponsor approval of the next scope. Use only separately authorized business and portfolio data.

## Evidence and interpretation

Analyst-derived broader-product extension. The user approved broader product planning with a Zava-first release; these VoCs motivate reuse but are not a customer request for a generic SaaS product.

- [VOC-003 - Design for the other Zava teams, not only the FinOps team](../voc/voc-003-design-for-the-other-zava-teams-not-only-the-finops-team.md) - source classification: Customer ask.
- [VOC-054 - Keep Zava as the current POC; defer regular global automation](../voc/voc-054-keep-zava-as-the-current-poc-defer-regular-global-automation.md) - source classification: Existing-state constraint.
- [VOC-056 - Welcome faster and cheaper analysis without committing to a design](../voc/voc-056-welcome-faster-and-cheaper-analysis-without-committing-to-a-design.md) - source classification: Customer-confirmed opportunity.
- [VOC-042 - Do not assume one uniform application-service convention](../voc/voc-042-do-not-assume-one-uniform-application-service-convention.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

This is a user-approved broader-product planning hypothesis, not a global scan, new tenant permission, or deployment authorization.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
