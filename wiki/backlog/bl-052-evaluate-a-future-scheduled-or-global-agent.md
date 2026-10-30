# BL-052 - Evaluate a future scheduled or global agent

Produce a separate go-no-go case for recurring execution after local product value and reuse are demonstrated.

**Force rank:** 100 of 104  
**Kano tag:** `delighter` (analyst hypothesis)  
**CD3:** 4 / 5 = **0.800**  
**Relative cost of delay:** 4/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 5 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** discovery  
**Status:** Proposed / not started.  
**Horizon / release:** Later / Options register - discovery only  
**Roadmap initiative:** [RM-009 - Evaluate future execution and platform boundaries](../roadmap/rm-009-evaluate-future-execution-and-platform-boundaries.md)  
**Planning date:** 2026-10-28

## User story

As a product sponsor, I want an evidence-based decision about recurring wider execution so that any automation investment has a justified purpose and approved boundaries.

## Acceptance criteria

1. The option case records measured local demand, proposed target scope, identity and approval model, operational ownership, and cost uncertainties.
2. A sponsor explicitly chooses proceed to separately scoped implementation, defer, or stop.
3. No agent, schedule, service identity, or global scan is deployed during the study; reported estate counts remain unverified.

## Priority and Kano rationale

- **Cost of delay:** The customer treats this as a possible later step, not a present architecture requirement.
- **Duration estimate:** A bounded operating-model, access, cost, and architecture study; implementation is not included.
- **Kano hypothesis:** Optional recurring execution could add convenience beyond the requested local workflow if its value and controls are proven.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-058 - Validate a separately authorized second operating profile](./bl-058-validate-a-separately-authorized-second-operating-profile.md); [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md)

**Current readiness:** Horizon-gated (G4); prerequisites also remain proposed.

**G4:** Future execution and adjacent-platform options are discovery or handoff only. Any implementation needs separate scope, access, cost, architecture, and security approval plus a fresh estimate.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-054 - Keep Zava as the current POC; defer regular global automation](../voc/voc-054-keep-zava-as-the-current-poc-defer-regular-global-automation.md) - source classification: Existing-state constraint.
- [VOC-056 - Welcome faster and cheaper analysis without committing to a design](../voc/voc-056-welcome-faster-and-cheaper-analysis-without-committing-to-a-design.md) - source classification: Customer-confirmed opportunity.
- [VOC-050 - Respect PIM elevation and approval tiers for central access](../voc/voc-050-respect-pim-elevation-and-approval-tiers-for-central-access.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

The CD3 estimate covers discovery only. Building automation requires a new backlog slice, approval, and re-estimation.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
