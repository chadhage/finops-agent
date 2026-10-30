# BL-046 - Suppress unentitled Windows and SQL Hybrid Benefit advice

Prevent enablement recommendations under the reported current Zava profile or an unverified entitlement state.

**Force rank:** 51 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 1 = **10.000**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 1 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** guardrail  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-004 - Make commercial recommendations safe](../roadmap/rm-004-make-commercial-recommendations-safe.md)  
**Planning date:** 2026-10-28

## User story

As an application owner, I want licensing recommendations gated by confirmed entitlement so that the report does not tell me to enable a benefit we do not have.

## Acceptance criteria

1. Fixtures for the reported current Zava position produce no Windows or SQL Hybrid Benefit enablement recommendation.
2. Unknown, stale, or unconfirmed entitlement also blocks enablement advice and points to license-management validation.
3. A changed profile requires evidence and responsible-team confirmation before the rule is reconsidered.

## Priority and Kano rationale

- **Cost of delay:** The customer explicitly rejects this advice under current entitlements, so delaying the guardrail directly risks incorrect reports.
- **Duration estimate:** A small eligibility gate in the existing recommendation path; entitlement discovery is a separate prerequisite.
- **Kano hypothesis:** Avoiding inapplicable or unentitled licensing advice is a basic requirement for credible optimization.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-047 - Capture license-management verification and SQL-via-Arc context](./bl-047-capture-license-management-verification-and-sql-via-arc-context.md); [BL-005 - Standardize the evidence-to-remedy finding contract](./bl-005-standardize-the-evidence-to-remedy-finding-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-048 - Exclude Windows and SQL Hybrid Benefit advice under current entitlements](../voc/voc-048-exclude-windows-and-sql-hybrid-benefit-advice-under-current-entitlements.md) - source classification: Customer ask.
- [VOC-049 - Confirm entitlement with license management and account for SQL via Arc](../voc/voc-049-confirm-entitlement-with-license-management-and-account-for-sql-via-arc.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not enable benefits, certify entitlement, or infer SQL discounts from a portal switch.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
