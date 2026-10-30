# BL-024 - Support deployment-neutral remediation guidance

Respect portal, script, and infrastructure-as-code approaches without requiring one toolchain.

**Force rank:** 65 of 104  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** 8 / 2 = **4.000**  
**Relative cost of delay:** 8/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-002 - Deliver actionable owner-accountable reports](../roadmap/rm-002-deliver-actionable-owner-accountable-reports.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want guidance compatible with my deployment approach so that I can make changes through the process my team actually uses.

## Acceptance criteria

1. The owner-selected deployment method is recorded rather than inferred from subscription ownership.
2. Applicable guidance distinguishes portal and deployment-script implications, including whether a direct change must be reflected in the team's source.
3. Unsupported methods or unknown automation are explicit gaps, not a reason to require a new toolchain.

## Priority and Kano rationale

- **Cost of delay:** Assuming mandatory IaC or one platform can prevent owners from using otherwise correct recommendations.
- **Duration estimate:** A small guidance-selection and method-labeling slice over the finding contract.
- **Kano hypothesis:** Guidance that fits the owner's existing deployment method should be more useful and actionable.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-024 - Allow teams to remediate through their own deployment method](../voc/voc-024-allow-teams-to-remediate-through-their-own-deployment-method.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

IaC remains recommended rather than mandatory; the assessment does not execute either portal or pipeline changes.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
