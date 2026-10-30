# BL-020 - Validate ownership freshness before report routing

Identify stale or changed ServiceNow ownership instead of treating misrouting as owner nonresponse.

**Force rank:** 61 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 9 / 2 = **4.500**  
**Relative cost of delay:** 9/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-28

## User story

As a report sender, I want current ownership confirmed so that a changed responsibility record does not send findings to the wrong person.

## Acceptance criteria

1. The routing artifact includes ownership validation time and the customer-approved freshness rule, which remains undecided until agreed.
2. An owner change or conflict triggers ServiceNow record validation rather than an untracked local overwrite.
3. Stale ownership and recipient nonresponse are separate states in the communication record.

## Priority and Kano rationale

- **Cost of delay:** Stale ownership can repeat misdirected communication and delay both cost and security action.
- **Duration estimate:** A small freshness and change-validation slice over the ownership record.
- **Kano hypothesis:** Contacting the correct current owner is an expected baseline, not a bonus capability.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-019 - Resolve accountable owners from ServiceNow records](./bl-019-resolve-accountable-owners-from-servicenow-records.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-020 - Maintain ownership changes in ServiceNow for correct routing](../voc/voc-020-maintain-ownership-changes-in-servicenow-for-correct-routing.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not invent a freshness threshold or automatically alter ServiceNow records.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
