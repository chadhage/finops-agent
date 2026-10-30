# BL-062 - Review subscription resource costs with billing and invoice evidence

Present one approved subscription's resource costs with verified MCA billing/invoice evidence, grouped by resource group without confusing resource spend with invoice totals.

**Force rank:** 4 of 104  
**Priority basis:** Product-owner priority #4, explicitly requested on 2026-10-29; BL-059, BL-060, and BL-061 retain priorities #1-#3 without changing existing CD3 estimates.  
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

As an authenticated Azure user, I want resource costs and invoice evidence grouped by resource group so that I can understand resource spend without confusing it with invoice totals.

## Acceptance criteria

1. The sample uses Microsoft Customer Agreement (MCA) billing. The prompting user is authenticated and authorized to read inventory and costs for exactly one approved immutable subscription ID; another billing agreement requires its own reviewed contract rather than assumed MCA behavior.
2. The minimum linked billing-profile and invoice scope is separately authorized and explicitly approved. Subscription resource/cost access does not imply invoice access. Read billing records only within that linked approved scope and filter charge records by immutable subscription ID, not display name.
3. Use Azure Cost Management `ActualCost` in the original billing currency for September 1 through September 30, 2026, UTC: from `2026-09-01T00:00:00Z` to `2026-10-01T00:00:00Z` exclusive. Actual Spend is resource-attributed cost before invoice-level taxes/credits, not the invoice amount due, pricing currency, or an inferred USD conversion. The sample subscription and dates are fixtures, not runtime customer configuration.
4. Retrieve inventory only for the approved subscription, match costs using case-insensitive resource IDs rather than names, and aggregate signed amounts with decimal-safe arithmetic only within the same resource ID and currency. Preserve source inventory fields, original currency, legitimate negative charges, and supported invoice references.
5. Verify invoice references against authoritative billing and charge evidence; never infer linkage from matching names or dates alone. `Invoice Evidence` is a report linkage status, not an invoice payment-status field; do not invent invoice references or payment status.
6. Group detailed rows by the inventory resource group, case-insensitively. An invoice section is not an Azure resource group, and resource details are not replaced with group-only aggregates. Each resource-and-currency combination appears once in its group while retaining its supported invoice references.
7. Each section contains a Markdown table with exactly these columns, in order: Resource ID, Name, Type, Resource Group, Location, Subscription ID, Actual Spend, Currency, Invoice References, Invoice Evidence, Cost Status.
8. The complete fixture has exactly three resource rows across `rg-app` and `rg-data`: `vm-app-01 = 12.50 USD`, `web-app-01 = 5.00 USD`, and `storage-app-01 = 3.25 USD`. Every row references `INV-2026-09-001`, with Invoice Evidence `Linked` and Cost Status `Available`, supported by the fixture's authoritative linkage.
9. Known-spend subtotals are `rg-app / USD / 17.50` and `rg-data / USD / 3.25`. No subtotal combines different currencies and no unapproved currency conversion occurs.
10. For the issued fixture invoice containing only this subscription's charges, display `Resource charges before tax / 20.75 USD`, `Tax / 2.08 USD`, and `Invoice document total / 22.83 USD` only in a separate invoice summary. Do not add the invoice total to resource costs or count it again. Invoice-level taxes, credits, and fees are not allocated to resources without authoritative allocation evidence.
11. The report identifies inventory collection time, cost period, cost basis, and source freshness. Unknown freshness is explicitly unknown; current inventory is not presented as a historical billing-period snapshot or the latest billed-through time.
12. If an invoice includes other subscriptions, return only the selected subscription's resource and charge details without disclosing other subscriptions' identifiers or charges. Do not label the invoice-wide total as selected-subscription spend; reconciliation is limited to verifiable selected-subscription charges, with invoice-wide reconciliation explicitly outside scope.
13. Preserve source-supported amounts/currencies when invoice evidence is unavailable or unverified. The three outline cases are `Pending / Provisional` for no issued invoice with pending source costs, `Unlinked / Available` for no authoritative charge-to-invoice link, and `Access denied / Available` when invoice access is denied but costs remain readable. Explicitly report incomplete invoice verification and its reason; do not invent a reference/status, switch identity, or silently broaden billing scope.
14. Charges with no resource ID or referring to a resource no longer in current inventory are reported separately as "Unallocated or not in current inventory". Preserve their amounts, currencies, and supported invoice references without inventing a current resource/group, forcing them into a resource-group subtotal, or claiming current-inventory totals reconcile the entire invoice.
15. Preserve the exact cost-evidence cases below: explicit zero USD is `0.00`, `USD`, `Available`; no matching record is `Unavailable`, `Unavailable`, `No matching cost record`; an amount without currency is `Unavailable`, `Unavailable`, `Missing currency`. Missing evidence makes affected group coverage incomplete, not zero spend or an assumed invoice/profile currency.
16. Inventory, cost details, and invoices follow each source's approved continuation contract. Keep the selected subscription, separately approved billing scopes, reporting period, cost basis, and user authority unchanged. Complete subtotals require all required sources to finish; failed/truncated collection is visibly incomplete, and affected subtotals are not complete period or invoice totals.
17. No resource, permission, invoice, or payment is modified. The proposal does not authorize role/consent changes, broader billing reads, purchases, remediation, provisioning, or deployment; supported read-only reporting does not imply financial write authority.
18. Verification uses synthetic responses for all six supplied BDD scenario families and ten expanded examples. The fixtures and skill-installation documentation are not executable-test, live billing, financial-audit, implementation, MVP-scope, or release-acceptance evidence; incremental outcome, source/permission contracts, estimates, and an approved balanced candidate remain required.

## Approved prompt example

```text
Using Azure Cost Management and the authorized billing and
invoice records, show resource costs for subscription
11111111-1111-4111-8111-111111111111 for September 2026.

Group the resources by resource group.
Include actual spend, billing currency, invoice references,
invoice evidence status, and cost-data status.
Show separate subtotals for each currency.
Clearly disclose missing data and reconciliation limitations.
```

## Synthetic resource and invoice fixtures

The resource names identify fixtures with shared inventory/charge IDs; they are not join keys. The issued fixture invoice contains only this subscription's charges.

| Resource Group | Name | Actual Spend | Currency | Invoice References | Invoice Evidence | Cost Status |
| --- | --- | --- | --- | --- | --- | --- |
| rg-app | vm-app-01 | 12.50 | USD | INV-2026-09-001 | Linked | Available |
| rg-app | web-app-01 | 5.00 | USD | INV-2026-09-001 | Linked | Available |
| rg-data | storage-app-01 | 3.25 | USD | INV-2026-09-001 | Linked | Available |

| Resource Group | Currency | Known-spend subtotal |
| --- | --- | --- |
| rg-app | USD | 17.50 |
| rg-data | USD | 3.25 |

| Invoice summary component | Amount | Currency |
| --- | --- | --- |
| Resource charges before tax | 20.75 | USD |
| Tax | 2.08 | USD |
| Invoice document total | 22.83 | USD |

## BDD acceptance examples

| Supplied scenario family | Expanded examples | Observable result |
| --- | ---: | --- |
| Return resource costs with verified invoice references | 1 | Three detailed rows, eleven exact columns, authoritative invoice links, two currency-specific group subtotals, and a separate invoice summary without double counting. |
| An invoice includes other subscriptions | 1 | Only selected-subscription details are disclosed; invoice-wide totals are not selected-subscription spend or an in-scope full reconciliation. |
| Invoice evidence is unavailable or unverified | 3 | Source-supported costs/currencies remain; pending, unlinked, and denied invoice evidence have the distinct statuses below and visible verification gaps. |
| Charges do not map to current resource inventory | 1 | A separate "Unallocated or not in current inventory" section preserves evidence without inventing resources/groups or forcing charge allocation. |
| Missing cost evidence is not zero spend | 3 | Explicit zero, no matching cost record, and missing currency retain the distinct values/statuses below; missing evidence marks affected group coverage incomplete. |
| Resource groups and financial evidence span multiple pages | 1 | All required sources retain their approved scopes and period/basis/authority; no duplicate resource/currency rows or complete-looking failed/truncated subtotals. |

| Invoice condition | Invoice Evidence | Cost Status |
| --- | --- | --- |
| No issued invoice and source costs are pending | Pending | Provisional |
| No authoritative charge-to-invoice link | Unlinked | Available |
| Invoice access denied while costs are readable | Access denied | Available |

| Cost evidence | Actual Spend | Currency | Cost Status |
| --- | --- | --- | --- |
| An explicit zero amount in USD | 0.00 | USD | Available |
| No matching cost record | Unavailable | Unavailable | No matching cost record |
| An amount without currency | Unavailable | Unavailable | Missing currency |

These are six scenario families, including two outlines with three examples each: ten expanded synthetic examples, not ten passing tests.

## Priority and Kano rationale

- **Priority:** The product owner explicitly requested this behavior as priority number 4. BL-059, BL-060, and BL-061 retain priorities #1-#3; the original 58 cards retain their estimates and relative ordering at ranks 47-104.
- **Estimate:** Engineering duration and relative cost-of-delay inputs remain unestimated; the priority instruction does not supply either.
- **Kano hypothesis:** Verifying resource spend against permitted invoice evidence is a proposed utility job. Validate incremental user value separately from inventory, cost enrichment, and grouping; report columns or invoice labels do not automatically become extra accepted outcomes.
- **Reassessment:** Review overlap, the MCA source/permission contract, linked billing scope, invoice-data privacy, and reconciliation limits before candidate scope freeze. Do not double-count the baseline or retag safeguards to satisfy the release ratio.

See the [priority overrides and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [5:1 candidate policy](../roadmap/delivery-plan.md#delivery-policy).

## Dependencies and delivery gate

**Prerequisites:** [BL-061 - Group resource spend and currency by resource group](./bl-061-group-resource-spend-and-currency-by-resource-group.md); reviewed MCA billing/invoice source and separately approved permission/scope contract; incremental outcome and explicit candidate-scope approval. Existing inventory and authorized cost-collection prerequisites remain in force.

**Current readiness:** Dependency-blocked: grouped resource-cost evidence remains proposed; MCA billing/invoice access, authoritative linkage, estimate, and balanced-candidate review are required.

**G1:** One explicitly approved Zava pilot subscription plus only the separately approved minimum linked billing/invoice scope. The hosted-agent direction applies; priority grants no live data access, permission expansion, provisioning, or deployment approval.

## Supporting developer guidance

The [Azure cost-analysis skill guide](../tooling/cost-analysis-skill.md) documents the exact requested installation command without running it. This optional development-assistant skill is not a deployed agent feature, a runtime dependency, an Azure permission grant, or an independently accepted delivery outcome.

## Evidence and interpretation

- [VOC-062 - Review subscription costs with invoice evidence](../voc/voc-062-review-subscription-costs-with-invoice-evidence.md) - source classification: Product-owner ask; supplied BDD and explicit priority #4 instruction, 2026-10-29.

This is new product-owner evidence, not an additional Zava interview or a quotation from the September 23 working session. The original 58 source cards and their evidence limits remain unchanged.

## Scope boundary

MCA resource-cost reporting with bounded invoice-linkage evidence only: no invoice payment/change, generalized billing-account reconciliation, financial audit assertion, forecasting, optimization advice, WorkIQ, email, remediation, purchases, or unapproved subscription/billing discovery. Other billing agreements need their own reviewed scope and source contract.

The [approved M1 scope](../iterations/iteration-0002.md#committed-scope) remains private inventory and its five utility outcomes. This priority and the optional skill guide do not change that scope, alter BL-059/BL-060/BL-061 acceptance boundaries, replace the current ARM collection contract, add outcomes to RC-01, or establish that any implementation has passed acceptance. Review incremental outcome boundaries and approve a six-outcome candidate before implementation.

---

[Back to priority #4](./index.md#priority-4) | [Product roadmap](../roadmap/index.md) | [VoC item](../voc/voc-062-review-subscription-costs-with-invoice-evidence.md) | [Skill guide](../tooling/cost-analysis-skill.md)
