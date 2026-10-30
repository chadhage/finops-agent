# BL-037 - Model regional candidates using total scenario cost

Include minimum units and cross-region network effects instead of recommending moves from unit prices alone.

**Force rank:** 104 of 104  
**Kano tag:** `delighter` (analyst hypothesis)  
**CD3:** 5 / 8 = **0.625**  
**Relative cost of delay:** 5/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 8 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Later / R3 option - feasibility-gated advanced advice  
**Roadmap initiative:** [RM-008 - Validate advanced architecture and regional advice](../roadmap/rm-008-validate-advanced-architecture-and-regional-advice.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want a regional comparison that includes relevant total costs so that a lower resource price is not misrepresented as a guaranteed saving.

## Acceptance criteria

1. The scenario records resource prices, minimum consumption, cross-region data flow and transfer assumptions, and owner constraints.
2. Unknown required inputs produce an insufficient-evidence result rather than a numeric saving.
3. Approved fixtures include a cheaper unit-price region with higher total scenario cost and preserve source dates and assumptions.

## Priority and Kano rationale

- **Cost of delay:** The customer found this interesting but warned that apparently cheaper regions can introduce offsetting costs.
- **Duration estimate:** A substantial scenario-modeling slice with workload, region, minimum-consumption, and transfer-cost inputs.
- **Kano hypothesis:** A defensible regional scenario may reveal useful opportunities not present in the basic report.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-036 - Test whether authorized evidence supports architecture advice](./bl-036-test-whether-authorized-evidence-supports-architecture-advice.md); [BL-041 - Produce traceable business cost rollups](./bl-041-produce-traceable-business-cost-rollups.md)

**Current readiness:** Horizon-gated (G3); prerequisites also remain proposed.

**G3:** Advanced advice is an option after R2 review, explicit sponsor approval, and sufficient permitted evidence. The feasibility spike must precede architecture candidate implementation.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-038 - Assess regional optimization on total cost, not unit price alone](../voc/voc-038-assess-regional-optimization-on-total-cost-not-unit-price-alone.md) - source classification: Customer-confirmed opportunity.
- [VOC-037 - Validate application knowledge and read-access limits for architecture advice](../voc/voc-037-validate-application-knowledge-and-read-access-limits-for-architecture-advice.md) - source classification: Open validation question.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not move resources, assert that illustrated East or West US examples are actual opportunities, or promise a migration benefit.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
