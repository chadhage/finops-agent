# BL-061 - Group resource spend and currency by resource group

Present one approved subscription's resource-level actual spend in resource-group sections, with separate known-spend subtotals for each currency and explicit coverage gaps.

**Force rank:** 3 of 104  
**Priority basis:** Product-owner priority #3, explicitly requested on 2026-10-29; BL-059 and BL-060 retain priorities #1 and #2 without changing existing CD3 estimates.  
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

As an authenticated Azure user, I want resource inventory and actual spend grouped by resource group so that I can review resource-level costs within each group.

## Acceptance criteria

1. The prompting user is authenticated and separately authorized to read inventory and cost data for one explicitly approved immutable subscription ID. Inventory uses approved Azure Resource Graph KQL; Azure Cost Management supplies `ActualCost` for the same subscription and reporting period under the same prompting user's authority.
2. The synthetic period is October 1 through October 28, 2026, UTC: from `2026-10-01T00:00:00Z` to `2026-10-29T00:00:00Z` exclusive. Both request scopes and the KQL subscription filter bind the approved ID; every page retains that scope, period, cost basis, and user authority. The fixture ID and dates are not runtime customer configuration.
3. Match costs using case-insensitive resource IDs, not names, and aggregate signed amounts using decimal-safe arithmetic only within the same normalized resource ID and currency. Preserve source inventory fields, original billing currency, and legitimate credits; no retail-price substitution, inferred currency, or unapproved conversion basis is introduced.
4. Group joined rows by the inventory resource group, with resource group names grouped case-insensitively. Each resource-and-currency combination appears once in its group section; do not move records between groups using cost-record names or replace resource details with group-only aggregate rows.
5. The supplied complete fixture produces exactly two resource-group sections, `rg-app` and `rg-data`, containing exactly four resource-level data rows in total. Their available costs are `vm-app-01 = 12.50 USD`, `web-app-01 = 5.00 USD`, `sql-app-01 = 4.00 EUR`, and `storage-app-01 = 3.25 USD`; the VM amount aggregates `10.00 + 2.50 USD`.
6. Every section contains a Markdown table with exactly these columns, in order: Resource ID, Name, Type, Resource Group, Location, Subscription ID, Actual Spend, Currency, Cost Status. Source fields remain faithful, all four complete-fixture rows have Cost Status `Available`, and no group, resource, amount, or permission is invented.
7. Known-spend subtotals are `rg-app / USD / 17.50`, `rg-data / EUR / 4.00`, and `rg-data / USD / 3.25`. No subtotal or grand total combines different currencies; no currency conversion occurs without an explicitly approved basis, and this item does not approve any exchange rate.
8. The response identifies the selected subscription, reporting period, and cost basis. It states cost-data freshness when supported or explicitly marks freshness unknown; retrieval time alone is not represented as the latest billed-through time.
9. A group's resources and costs may span multiple inventory and cost pages. Follow both sources' approved continuation contracts, retain one section for that group, and include each resource-and-currency combination once. Complete group subtotals are produced only after both sources legitimately finish, not at an intermediate page boundary.
10. Preserve the exact zero/missing-data distinctions below: an explicit zero amount in USD is `0.00`, `USD`, `Available`; no matching record is `Unavailable`, `Unavailable`, `No matching cost record`; an amount without currency is `Unavailable`, `Unavailable`, `Missing currency`. Missing evidence is never silently converted to zero.
11. If `rg-app` has one available resource costing `12.50 USD` and another with no matching cost record, show a known-spend subtotal of `12.50 USD` and explicitly mark group cost coverage incomplete. Do not treat the missing resource's spend as zero or present the subtotal as the complete group cost.
12. For access denial or a later-page failure from either Azure Resource Graph or Azure Cost Management, explicitly identify the failed source and reason. Any displayed, still-authorized rows and subtotals indicate affected coverage; denied/incomplete data is not zero, affected subtotals are not complete period totals, and no retry uses another identity or subscription. Invalid/repeated continuations, unresolved truncation, or exhausted approved bounds likewise cannot establish completeness.
13. Successful terminal empty inventory returns the nine headers without fabricated groups or resource rows and states exactly: "No resources visible to your account were returned by Azure Resource Graph." It does not infer that subscription spend is zero.
14. An authorized resource with an empty resource-group field is retained under "(No resource group reported)", preserving matching spend, currency, and cost-data status. The heading is explicitly a display label, not an actual Azure resource group or an invented source value.
15. No other subscription is queried or displayed, and no Azure resource or permission is modified. Grouping and subtotals reuse the approved inventory/cost contracts; they do not authorize a wider billing scope, another data source, consent, provisioning, purchases, remediation, or deployment.
16. Verification uses synthetic responses for all seven supplied BDD scenario families and twelve expanded examples. Those specifications and fixtures are not executable-test, live billing, customer-pilot, implementation, or release-acceptance evidence; incremental outcome boundaries, prerequisites, estimates, and a reviewed balanced candidate remain required.

## Approved prompt and inventory query example

```text
List the resources in subscription
11111111-1111-4111-8111-111111111111.
Include actual spend for October 1 through October 28, 2026, UTC.
Group the results by resource group.
Show resource details, spend, billing currency, and cost-data status.
Include a separate subtotal for each currency within each group.
```

```kql
Resources
| where subscriptionId =~ '11111111-1111-4111-8111-111111111111'
| project id, name, type, resourceGroup, location, subscriptionId
| order by resourceGroup asc, id asc
```

Resource Graph supplies inventory, not billed costs. Match the same-scope/period Cost Management evidence by resource ID before grouping for presentation; do not use a `summarize`-only inventory rollup that discards resource details. Group subtotals cover matched, retrieved evidence, not the entire subscription invoice.

## Synthetic resource and subtotal fixtures

Resource names identify fixtures whose inventory and cost records share stable IDs; names are not join keys.

| Resource Group | Name | Actual Spend | Currency | Cost Status |
| --- | --- | --- | --- | --- |
| rg-app | vm-app-01 | 12.50 | USD | Available |
| rg-app | web-app-01 | 5.00 | USD | Available |
| rg-data | sql-app-01 | 4.00 | EUR | Available |
| rg-data | storage-app-01 | 3.25 | USD | Available |

| Resource Group | Currency | Known-spend subtotal |
| --- | --- | --- |
| rg-app | USD | 17.50 |
| rg-data | EUR | 4.00 |
| rg-data | USD | 3.25 |

## BDD acceptance examples

| Supplied scenario family | Expanded examples | Observable result |
| --- | ---: | --- |
| Return resource-level tables and currency subtotals for each group | 1 | Exactly two sections and four detailed rows; nine exact columns; the resource amounts and three currency-specific subtotals above; no mixed-currency total or writes. |
| A resource group spans multiple inventory and cost pages | 1 | One section per case-insensitive group across both sources' pages; one row per resource/currency; complete subtotals only after both sources finish. |
| Preserve zero and unavailable costs within a group | 3 | Explicit zero, no matching cost record, and missing currency retain the distinct values and statuses below. |
| Missing resource costs make the group subtotal incomplete | 1 | Known-spend subtotal `12.50 USD` with explicit incomplete group coverage; no zero imputation or complete-group-cost claim. |
| Source failures cannot produce complete-looking groups | 4 | Each source's access denial and later-page failure identify source/reason and affected coverage, without zero-data or alternate-authority fallbacks. |
| No visible indexed resources are returned | 1 | Headers only and the exact no-visible-resources message; no fabricated group or inference of zero subscription spend. |
| A resource has no reported resource group | 1 | Retain the resource and matched cost evidence under the explicitly display-only "(No resource group reported)" heading. |

| Cost evidence | Actual Spend | Currency | Cost Status |
| --- | --- | --- | --- |
| An explicit zero amount in USD | 0.00 | USD | Available |
| No matching cost record | Unavailable | Unavailable | No matching cost record |
| An amount without currency | Unavailable | Unavailable | Missing currency |

| Failed source | Failure |
| --- | --- |
| Azure Resource Graph | access denied |
| Azure Cost Management | access denied |
| Azure Resource Graph | later-page failure |
| Azure Cost Management | later-page failure |

These are seven scenario families, including outlines with three and four examples: twelve expanded synthetic examples, not twelve passing tests.

## Priority and Kano rationale

- **Priority:** The product owner explicitly requested this behavior as priority number 3. BL-059 remains inventory-only priority #1; BL-060 remains resource spend/currency priority #2. The original 58 cards retain their estimates and relative ordering at ranks 47-104.
- **Estimate:** Engineering duration and relative cost-of-delay inputs remain unestimated; the priority instruction does not supply either.
- **Kano hypothesis:** Group-level cost review is a proposed utility job. Validate its incremental user value and acceptance boundary rather than counting headings, subtotals, report sections, or a formatting variant as additional independently accepted outcomes.
- **Reassessment:** Reuse BL-060's resource-level evidence and review overlap with the existing inventory/cost jobs before candidate scope freeze. Do not double-count the baseline or retag safeguards to satisfy the release ratio.

See the [priority overrides and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [5:1 candidate policy](../roadmap/delivery-plan.md#delivery-policy).

## Dependencies and delivery gate

**Prerequisites:** [BL-060 - List subscription resources with spend and currency](./bl-060-list-subscription-resources-with-spend-and-currency.md); reviewed grouping/subtotal acceptance boundary and explicit candidate-scope approval. BL-060 retains its inventory and authorized cost-collection prerequisites.

**Current readiness:** Dependency-blocked: resource-level spend evidence remains proposed; incremental outcome, grouping contract, estimate, and balanced-candidate review are required.

**G1:** One explicitly approved Zava pilot subscription under the prompting user's delegated inventory and cost authority. The hosted-agent direction applies; priority grants no live data access, permission expansion, provisioning, or deployment approval.

## Evidence and interpretation

- [VOC-061 - Review resource spend by resource group](../voc/voc-061-review-resource-spend-by-resource-group.md) - source classification: Product-owner ask; supplied BDD and explicit priority #3 instruction, 2026-10-29.

This is new product-owner evidence, not an additional Zava interview or a quotation from the September 23 working session. The original 58 source cards and their evidence limits remain unchanged.

## Scope boundary

Grouped presentation of authorized resource-level actual spend only: no invoice reconciliation, forecasting, optimization advice, WorkIQ, email, remediation, purchases, or wider-estate discovery. The current [M1 inventory contract](../../specs/bdd/17-m1-inventory-comparison-negative.feature) uses ARM Resources List and does not enable this capability. This priority does not alter BL-059/BL-060 acceptance boundaries, replace the M1 source contract, add outcomes to RC-01, or establish that any implementation has passed acceptance. Review incremental outcome boundaries and approve a six-outcome candidate before implementation.

---

[Back to priority #3](./index.md#priority-3) | [Product roadmap](../roadmap/index.md) | [VoC item](../voc/voc-061-review-resource-spend-by-resource-group.md)
