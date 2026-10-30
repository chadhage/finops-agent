# BL-050 - Preserve the local user-authenticated execution contract

Run existing analysis assets under terminal authentication without requiring new services or a mandatory MCP connector.

**Force rank:** 59 of 104  
**Kano tag:** `dissatisfier` (analyst hypothesis)  
**CD3:** 10 / 2 = **5.000**  
**Relative cost of delay:** 10/10 loss-of-value points per common delay interval  
**Relative delivery duration:** 2 normalized duration units; not calendar days or story points  
**Estimate confidence:** Low; no engineering duration or financial delay rate has been validated.  
**Work type:** enabler  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-28

## Hosted implementation disposition

The later implementation request explicitly selected an Azure-hosted microservices agent; [Iteration 0002](../iterations/iteration-0002.md#hosted-execution-override) plans the corresponding user-delegated execution contract. Preserve this card's original local-workflow evidence and acceptance criteria as the planning baseline. Hosting is an explicit subsequent override, not proof that the original local-only criteria were delivered. The prompting user's authority, no shared/developer-credential fallback, explicit scope and separate deployment approvals remain mandatory; the CD3 rank and Kano tag are unchanged.

## User story

As an analyst, I want existing local analysis assets to use my authenticated terminal context so that improvements do not require a new deployed architecture.

## Acceptance criteria

1. The execution contract identifies the existing harness and current user-authenticated context without embedding credentials.
2. Additional scripts can fit within the approved local asset path and surface authentication or permission errors explicitly.
3. The baseline workflow requires neither new Azure services nor a new MCP connector, global agent, or standing shared identity.

## Priority and Kano rationale

- **Cost of delay:** Premature infrastructure or connector assumptions would expand the POC and conflict with how the customer already runs it.
- **Duration estimate:** A small execution contract and existing-asset integration slice; new collector architectures are excluded.
- **Kano hypothesis:** Preserving the explicitly requested execution and identity boundary is a basic product fit requirement.
- **Reassessment:** Confirm with product, customer, engineering, and relevant control owners after the first evidence review. No score is a customer-stated priority, measured saving, or delivery promise.

See the [CD3 method and exact tie-breaks](./index.md#cd3) and [Kano definitions](./index.md#kano). Force rank is not an executable sequence.

## Dependencies and delivery gate

**Prerequisites:** [BL-007 - Agree the product goals and workflow contract](./bl-007-agree-the-product-goals-and-workflow-contract.md)

**Current readiness:** Dependency-blocked: prerequisites remain proposed, not completed.

**G1:** Zava-first pilot only: approved subscriptions, existing local execution, current user permissions, and customer-validated operating rules. No wider access or deployment is authorized.

## Evidence and interpretation

Analyst-proposed delivery slice derived from the linked VoCs. A source constraint, question, reported risk, or future topic is not automatically an approved feature commitment.

- [VOC-053 - Run within the existing local analysis assets and user permissions](../voc/voc-053-run-within-the-existing-local-analysis-assets-and-user-permissions.md) - source classification: Customer ask.
- [VOC-055 - Preserve the current user-authenticated terminal data path](../voc/voc-055-preserve-the-current-user-authenticated-terminal-data-path.md) - source classification: Existing-state constraint.
- [VOC-054 - Keep Zava as the current POC; defer regular global automation](../voc/voc-054-keep-zava-as-the-current-poc-defer-regular-global-automation.md) - source classification: Existing-state constraint.

Source claims and illustrative examples retain the [catalogue evidence limits](../voc/reference.md#evidence-limits). The underlying transcript and reported product or licensing behavior were not independently verified for this plan.

## Scope boundary

Do not deploy infrastructure, collect secrets into reports, or claim that a faster implementation design has already been selected.

---

[Back to force-ranked backlog](./index.md#force-ranked-backlog) | [Product roadmap](../roadmap/index.md) | [VoC index](../voc/index.md)
