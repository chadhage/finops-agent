# BL-059 - List subscription resources with Azure Resource Graph

Query one approved subscription through Azure Resource Graph and return a faithful, paginated Markdown resource table under the prompting user's authority.

**Force rank:** 1 of 104  
**Priority basis:** Product-owner priority #1, explicitly requested on 2026-10-29; overrides the CD3 ordering without changing existing estimates.  
**Kano tag:** `satisfier` (analyst hypothesis)  
**CD3:** Not estimated; priority is an explicit product-owner decision, not a fabricated ratio.  
**Relative cost of delay:** Not estimated.  
**Relative delivery duration:** Not estimated; engineering review is required before commitment.  
**Estimate confidence:** Unestimated; no financial delay rate, duration, date, or capacity commitment is inferred.  
**Work type:** feature  
**Status:** Proposed / not started.  
**Horizon / release:** Now / R1 - Zava-first pilot; candidate assignment requires review.  
**Roadmap initiative:** [RM-001 - Establish trusted local analysis](../roadmap/rm-001-establish-trusted-local-analysis.md)  
**Planning date:** 2026-10-29

## User story

As an authenticated Azure user, I want to request a specific subscription's resource inventory through the agent so that I can review its resources in a clear table.

## Acceptance criteria

1. The prompting user is authenticated, has delegated read access to the selected subscription, and has approved its immutable subscription ID as the only query scope. Missing, malformed, ambiguous, or unauthorized scope prevents dispatch; a prompt is not authorization.
2. The agent queries Azure Resource Graph, not Log Analytics, using the fixed approved KQL template below. Both the request's subscription scope and the KQL subscription filter bind the same approved ID; user-supplied arbitrary KQL cannot replace that contract.
3. The response identifies the selected subscription and contains a Markdown table with exactly these columns, in order: Resource ID, Name, Type, Resource Group, Location, Subscription ID. Values map faithfully to `id`, `name`, `type`, `resourceGroup`, `location`, and `subscriptionId`; no values or resources are invented.
4. With the supplied synthetic two-resource response, the table has exactly two data rows, sorted by resource ID. No resource from another subscription is queried or displayed, and no Azure resource is modified.
5. Pagination retains the approved query, subscription, and user authority. A fixture with two resources on the first page and one additional resource on the final page produces exactly three distinct resource rows. Completeness is claimed only after the legitimate final page is processed.
6. A successful zero-record response with no remaining pages returns the table headers without fabricated rows and states exactly: "No resources visible to your account were returned by Azure Resource Graph."
7. An authorization failure is reported as access denied, not zero resources. The agent does not retry through another identity or subscription, elevate privileges, or substitute a cached success.
8. A later-page failure explicitly marks any displayed inventory as incomplete and never claims that all resources were returned. Invalid or repeated continuations, truncation that cannot be resolved, or exhausted approved collection bounds likewise cannot establish completeness.
9. Coverage is limited to indexed resources visible to the caller through Azure Resource Graph. Neither completed pagination nor Reader access establishes an atomic, exhaustive, real-time Azure snapshot.
10. Tests use synthetic responses and verify all five supplied BDD scenarios. Passing those tests is not live Azure access, product acceptance, or deployment evidence; no resource writes, purchases, or changes to permissions are authorized.

## Approved prompt and query example

The subscription below is a synthetic fixture. Runtime scope selection must validate and bind the actual approved subscription ID rather than configuring this sample as customer scope.

```text
List the resources in subscription
11111111-1111-4111-8111-111111111111.
Return a Markdown table showing Resource ID, Name, Type,
Resource Group, Location, and Subscription ID.
```

```kql
Resources
| where subscriptionId =~ '11111111-1111-4111-8111-111111111111'
| project id, name, type, resourceGroup, location, subscriptionId
| order by id asc
```

## BDD acceptance examples

| Supplied scenario | Observable result |
| --- | --- |
| Return the requested subscription's resources as a table | Approved request scope and KQL filter; selected-subscription label; six exact columns; two source-faithful rows; no cross-subscription data or writes. |
| Retrieve all result pages | Same query and scope across the continuation; two plus one resources become three distinct rows; no premature completeness claim. |
| The subscription has no visible indexed resources | Successful terminal zero result; headers only; the exact no-visible-resources message. |
| Access is denied | Explicit authorization error; no zero-resource result or alternate identity/subscription fallback. |
| A later page cannot be retrieved | Any retained table is visibly incomplete; no claim that all resources were returned. |

## Priority and Kano rationale

- **Priority:** The product owner explicitly requested this behavior as priority number 1. The original 58 cards retain their CD3 estimates and relative ordering at ranks 47-104.
- **Estimate:** Obtain engineering duration and relative cost-of-delay inputs separately; the priority instruction does not supply either.
- **Kano hypothesis:** A directly usable inventory table is a utility outcome. Authorization, selected scope, truthful coverage, and read-only behavior remain mandatory acceptance controls, not extra value outcomes.
- **Reassessment:** Review the incremental Resource Graph contract, prerequisites, and overlap with M1 before candidate scope freeze. Do not double-count an existing outcome or retag safeguards to satisfy the release ratio.

See the [priority override and CD3 method](./index.md#cd3), [Kano definitions](./index.md#kano), and [5:1 candidate policy](../roadmap/delivery-plan.md#delivery-policy).

## Dependencies and delivery gate

**Prerequisites:** [BL-026 - Enforce explicit selected-subscription boundaries](./bl-026-enforce-explicit-selected-subscription-boundaries.md); [BL-048 - Preflight actual RBAC capabilities and PIM state](./bl-048-preflight-actual-rbac-capabilities-and-pim-state.md); reviewed Resource Graph source contract and explicit candidate-scope approval.

**Current readiness:** Dependency-blocked: prerequisite cards remain proposed; source-contract, estimate, and balanced-candidate review are required.

**G1:** One explicitly approved Zava pilot subscription under the prompting user's delegated authority. The later hosted-agent direction applies; this planning priority grants no live data access, consent, provisioning, or deployment approval.

## Evidence and interpretation

- [VOC-059 - Request a subscription resource table through the agent](../voc/voc-059-request-a-subscription-resource-table-through-the-agent.md) - source classification: Product-owner ask; supplied BDD and explicit priority instruction, 2026-10-29.

This is new product-owner evidence, not an additional quotation or requirement attributed to the September 23 customer session. The original 58 source cards and their evidence limits remain unchanged.

## Scope boundary

Inventory only: no cost assessment, WorkIQ, email, remediation, wider-estate discovery, or alternate credential fallback. The current [M1 inventory contract](../../specs/bdd/17-m1-inventory-comparison-negative.feature) uses ARM Resources List. This proposed Resource Graph behavior does not silently replace that source contract, add a seventh RC-01 outcome, change its accepted scope, or establish that either implementation has passed acceptance. Resolve overlap and obtain a reviewed six-outcome candidate before implementation.

---

[Back to priority #1](./index.md#priority-1) | [Product roadmap](../roadmap/index.md) | [VoC item](../voc/voc-059-request-a-subscription-resource-table-through-the-agent.md)
