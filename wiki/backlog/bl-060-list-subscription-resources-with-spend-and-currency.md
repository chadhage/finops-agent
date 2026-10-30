# BL-060 - List subscription resources with spend and currency

Enrich one approved subscription's Resource Graph inventory with resource-level actual spend, original billing currency, and explicit cost-data status for a defined period.

**Force rank:** 2 of 104  
**Priority basis:** Product-owner priority #2, explicitly requested on 2026-10-29; BL-059 remains priority #1 and existing CD3 estimates are unchanged.  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** Not estimated; product-owner priority is not a fabricated cost/duration ratio.  
**Relative cost of delay:** Not estimated.  
**Relative delivery duration:** Not estimated; engineering review is required before commitment.  
**Estimate confidence:** Unestimated; no financial delay rate, duration, date, or capacity commitment is inferred.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot; candidate assignment requires review.  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As an authenticated Azure user, I want a resource inventory with actual spend and billing currency so that I can review resource-level costs for a defined period.

## Acceptance criteria

1. The prompting user is authenticated and separately authorized to read inventory and cost data for one explicitly approved immutable subscription ID. Both source requests retain that subscription scope and user authority; a prompt, inventory permission, or subscription selection alone does not grant cost access.
2. Inventory comes from the approved Azure Resource Graph KQL template below; actual spend comes from Azure Cost Management `ActualCost` for the same subscription and reporting period. Do not invent billed-cost fields in the Resource Graph `Resources` table or substitute retail prices, estimates, amortized costs, another identity, or a wider billing scope.
3. The synthetic period is October 1 through October 28, 2026, UTC: from `2026-10-01T00:00:00Z` to `2026-10-29T00:00:00Z` exclusive. Cost basis remains `ActualCost` in the original billing currency across every page. These fixture dates and subscription ID are not runtime customer configuration.
4. Match costs to inventory by case-insensitive resource IDs, never names alone, while preserving source inventory fields for display. Do not force unmatched or unallocated cost records onto a current resource or claim the current-inventory table reconciles the entire subscription invoice.
5. Aggregate signed cost amounts using decimal-safe arithmetic only within the same normalized resource ID and currency; retain credits rather than clamping negative amounts. The supplied charges `10.00 USD` and `2.50 USD` for `vm-app-01` produce `12.50 USD`; `3.25 USD` for `storage-app-01` remains `3.25 USD`. The two-resource fixture produces exactly two data rows with Cost Status `Available`.
6. The Markdown table contains exactly these columns, in order: Resource ID, Name, Type, Resource Group, Location, Subscription ID, Actual Spend, Currency, Cost Status. The six inventory fields match source records, currency comes from cost evidence rather than location or locale, and no resource or amount is fabricated.
7. The response identifies the selected subscription, reporting period, and cost basis. It states cost-data freshness when supported by the source or explicitly marks freshness unknown; retrieval time alone is not represented as the latest billed-through time.
8. Retrieve all inventory and cost pages through each source's approved continuation contract without changing subscription, reporting period, cost basis, or user authority. The fixture with two inventory resources followed by one additional resource returns all three with corresponding cost evidence. Complete query coverage is claimed only after both sources legitimately finish.
9. Preserve the exact zero/missing-data distinctions in the table below: an explicit zero amount in USD is `0.00`, `USD`, `Available`; no matching record is `Unavailable`, `Unavailable`, `No matching cost record`; an amount without currency is `Unavailable`, `Unavailable`, `Missing currency`. Missing evidence is never silently converted to zero or an assumed currency.
10. If one resource has USD and EUR cost records, return separate rows for each resource-and-currency combination and separate any totals by currency. No conversion occurs without an explicitly approved conversion basis; this item does not itself approve a conversion or exchange rate.
11. If either Azure Resource Graph or Azure Cost Management denies access, explicitly identify the denied source. Denied data is not zero resources or zero spend; no retry uses another identity or subscription, privilege elevation, or a cached success in place of the failure.
12. If a later inventory or cost page fails, any displayed results are explicitly incomplete and affected spend is not presented as a complete period total. The failure remains visible rather than becoming zero. Invalid/repeated continuations, unresolved truncation, or exhausted approved bounds likewise cannot establish complete query coverage.
13. A successful terminal inventory response with zero resources returns the nine headers without fabricated resource rows and states exactly: "No resources visible to your account were returned by Azure Resource Graph." It does not infer that subscription spend is zero.
14. No resource from another subscription is queried or displayed, and no Azure resource, permission, purchase, or remediation state is modified. An approved read-only Cost Management query is not permission to perform resource writes or broaden billing access.
15. Verification uses synthetic responses for all seven supplied BDD scenario families and ten expanded examples. Those specifications and fixtures are not executable-test, live billing, customer-pilot, implementation, or release-acceptance evidence; prerequisites and a reviewed balanced candidate remain required.

## Approved prompt and inventory query example

```text
List the resources in subscription
11111111-1111-4111-8111-111111111111.
Include actual spend for October 1 through October 28, 2026, UTC.
Return a Markdown table with resource details, spend,
billing currency, and cost-data status.
```

```kql
Resources
| where subscriptionId =~ '11111111-1111-4111-8111-111111111111'
| project id, name, type, resourceGroup, location, subscriptionId
| order by id asc
```

The approved Cost Management request supplies `ActualCost` for the same subscription and period. Resource Graph alone does not supply billed costs. An all-KQL alternative would require separately approved cost-export ingestion into a KQL-accessible store; no such ingestion or infrastructure is authorized here.

## BDD acceptance examples

| Supplied scenario family | Expanded examples | Observable result |
| --- | ---: | --- |
| Return resource inventory with aggregated spend and currency | 1 | Two source-faithful rows; nine exact columns; `vm-app-01` has `12.50 USD`, `storage-app-01` has `3.25 USD`; both statuses are `Available`; subscription, period, basis, and freshness are explicit. |
| Retrieve all inventory and cost pages | 1 | Both sources retain scope, period, basis, and authority; two plus one inventory resources are returned; neither source ends prematurely. |
| Distinguish zero spend from unavailable cost evidence | 3 | Explicit zero, no matching cost record, and missing currency retain the distinct values and statuses below. |
| Preserve different billing currencies | 1 | Separate resource-and-currency rows and currency-specific totals; no unapproved conversion or mixed-currency sum. |
| Access to a required source is denied | 2 | Azure Resource Graph and Azure Cost Management failures identify the denied source without zero-data or alternate-authority fallbacks. |
| A later inventory or cost page fails | 1 | Visible incomplete results; affected spend is not a complete period total; the error is not replaced with zero. |
| No visible indexed resources are returned | 1 | Headers only and the exact no-visible-resources message; no inference of zero subscription spend. |

| Cost evidence | Actual Spend | Currency | Cost Status |
| --- | --- | --- | --- |
| An explicit zero amount in USD | 0.00 | USD | Available |
| No matching cost record | Unavailable | Unavailable | No matching cost record |
| An amount without currency | Unavailable | Unavailable | Missing currency |

These are seven scenario families, including two outlines with three and two examples respectively: ten expanded synthetic examples, not ten passing tests.

## Priority and Kano rationale

- **Priority:** The product owner explicitly requested this behavior as priority number 2. BL-059 remains the separate inventory-only priority #1; the original 58 cards retain their CD3 estimates and relative ordering at ranks 47-104.
- **Estimate:** Engineering duration and relative cost-of-delay inputs remain unestimated; the priority instruction does not supply either.
- **Kano hypothesis:** Reviewing actual spend alongside inventory is a distinct utility job. Currency correctness, authorized scope, truthful coverage, and failure handling are mandatory acceptance controls, not additional value outcomes.
- **Reassessment:** Review incremental cost enrichment, existing BL-049 cost collection, and overlap with BL-059 and M1 before candidate scope freeze. Do not double-count the inventory baseline or retag safeguards to satisfy the release ratio.

See the [priority overrides and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [5:1 candidate policy](../roadmap/delivery-plan.md#delivery-policy).

## Dependencies and delivery gate

**Prerequisites:** [BL-059 - List subscription resources with Azure Resource Graph](./bl-059-list-subscription-resources-with-azure-resource-graph.md); [BL-049 - Collect authorized subscription-linked cost evidence](./bl-049-collect-authorized-subscription-linked-cost-evidence.md); reviewed Cost Management source/permission contract and explicit candidate-scope approval.

**Current readiness:** Dependency-blocked: inventory and cost-collection prerequisites remain proposed; source-contract, estimate, and balanced-candidate review are required.

**G1:** One explicitly approved Zava pilot subscription under the prompting user's delegated inventory and cost authority. The later hosted-agent direction applies; priority grants no live data access, consent, billing-permission expansion, provisioning, or deployment approval.

## Evidence and interpretation

- [VOC-060 - Request resource-level spend and currency](../voc/voc-060-request-resource-level-spend-and-currency.md) - source classification: Product-owner ask; supplied BDD and explicit priority #2 instruction, 2026-10-29.

This is new product-owner evidence, not an additional Zava interview or a quotation from the September 23 working session. The original 58 source cards and their evidence limits remain unchanged.

## Scope boundary

Resource inventory and matching actual-spend evidence only: no invoice reconciliation, forecasting, optimization advice, WorkIQ, email, remediation, purchases, or wider-estate discovery. The current [M1 inventory contract](../../specs/bdd/17-m1-inventory-comparison-negative.feature) uses ARM Resources List and does not enable this cost-enriched capability. This priority does not silently replace that contract, alter BL-059's inventory-only acceptance criteria, add outcomes to RC-01, or establish that any implementation has passed acceptance. Review overlap and approve a six-outcome candidate before implementation.

---

[Back to priority #2](./index.md#priority-2) | [Product roadmap](../roadmap/index.md) | [VoC item](../voc/voc-060-request-resource-level-spend-and-currency.md)
