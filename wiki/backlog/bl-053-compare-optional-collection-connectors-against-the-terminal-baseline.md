# BL-053 - Compare optional collection connectors against the terminal baseline

Test whether a permitted alternative such as MCP improves efficiency without losing evidence or changing access boundaries.

**Force rank:** 101 of 104  
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

As an analyst, I want an optional connector compared with the current path so that architectural change follows evidence rather than assumption.

## Acceptance criteria

1. Any alternative is separately authorized and tested on the same permitted scope and comparable inputs as the terminal baseline.
2. The comparison reports run time, observable cost, evidence completeness, authentication behavior, and failure handling.
3. The decision can retain the current path, approve further work, or reject the alternative; MCP is never assumed to be a prerequisite.

## Priority and Kano rationale

- **Cost of delay:** Efficiency is welcomed, but the source does not establish a need for a new connector or a chosen design.
- **Duration estimate:** A bounded comparative experiment with parity, authentication, and processing-cost checks; no production connector rollout.
- **Kano hypothesis:** A demonstrably more efficient connector could add value beyond the existing adequate terminal path.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-054 - Baseline local analysis time cost and evidence completeness](./bl-054-baseline-local-analysis-time-cost-and-evidence-completeness.md); [BL-050 - Preserve the local user-authenticated execution contract](./bl-050-preserve-the-local-user-authenticated-execution-contract.md)

**Current readiness:** Horizon-gated (G4); prerequisites also remain proposed.

**G4:** Future execution and adjacent-platform options are discovery or handoff only. Any implementation needs separate scope, access, cost, architecture, and security approval plus a fresh estimate.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-055 - Preserve the current user-authenticated terminal data path](../voc/voc-055-preserve-the-current-user-authenticated-terminal-data-path.md) - source classification: Existing-state constraint.
- [VOC-056 - Welcome faster and cheaper analysis without committing to a design](../voc/voc-056-welcome-faster-and-cheaper-analysis-without-committing-to-a-design.md) - source classification: Customer-confirmed opportunity.
- [VOC-053 - Run within the existing local analysis assets and user permissions](../voc/voc-053-run-within-the-existing-local-analysis-assets-and-user-permissions.md) - source classification: Customer ask.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

No mandatory MCP migration, secret-bearing shared connector, or inference that a study authorizes infrastructure deployment.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
