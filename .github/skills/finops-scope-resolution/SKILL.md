---
name: finops-scope-resolution
description: "Resolve exact Azure FinOps workload resource sets by subscription or management group names/IDs, resource group names/ARM IDs, one or more named users or owner emails, tags, and region names. Use for ownership provenance, scope boundaries, ambiguous names, or resource-precision validation."
---

# Deterministic workload scope resolution

Use the [shared helper](../finops-cost-evidence/scripts/finops.py) from
`finops-cost-evidence`. This dependency is explicit: reuse the skills together,
not by copying an untracked script into each skill.

## Resolve intent before collecting data

- Approve one tenant, the invoker object ID, and a nonempty allowlist of exact
  subscription UUIDs. MG selection only narrows that allowlist.
- Ask for complete UTC days and ActualCost/AmortizedCost.
- Distinguish current-inventory selection from historical billing attribution.
  This helper resolves CURRENT resource IDs and then queries their period cost.
  It does not reconstruct past tags, past owners, or deleted resource membership.
- OR together values within a category; AND across categories. Within tags, AND
  keys and OR values. Subscription IDs and names are one category, as are MG
  IDs/names and resource-group IDs/names. No contains/fuzzy name matching.
- Ask which owner semantics apply: `rbac`, `business`, or explicit `either`.
  An array of users is OR; all other workload selectors still intersect it.

Create a scenario from the
[example](../finops-cost-evidence/assets/scenario.example.json).
Remove unused selectors; an empty supplied selector is invalid, not "ignore."
MG identifiers are full `/providers/Microsoft.Management/managementGroups/...`
IDs; resource-group identifiers are full ARM IDs.

## Collect complete current inventory

```powershell
$helper = '.github\skills\finops-cost-evidence\scripts\finops.py'
python $helper inventory --scenario '.finops-runs\scenario.json' --out '.finops-runs\catalog.json'
```

`inventory` uses fixed Resource Graph queries, exact approved subscription IDs,
all `$skipToken` pages, stable counts, unique resource IDs, subscription
containers/MG ancestry, resource groups, and location alias metadata.
Truncation without continuation, count drift, duplicate IDs, and missing selected
subscriptions block collection. Record source pages and hashes.

ARG is eventually consistent and caller-visible. Complete pagination is not
proof that the user can see every existing resource or that inventory is an
atomic snapshot. Independent resource-set comparison is still required for the
requested precision acceptance gate.

## Resolve owners without guessing

When owner filtering is requested, collect and normalize an approved read-only
ownership evidence file, then pass `inventory --owners <file>`. Do not manually
construct matching resource lists. The helper performs exact intersections.

1. Resolve each supplied user name/email against authoritative directory data,
   comparing exact object ID, display name, UPN, and mail. Enumerate all pages.
   Resolve aliases only with directory evidence; ambiguous names/emails block.
2. For RBAC, enumerate active assignments at applicable selected subscription,
   resource group, resource, and verified ancestor scopes. Resolve transitive
   group membership, including nested groups, before materializing user bindings.
   Use built-in Owner role ID `8e3af657-a8ff-443c-a75c-2fe8c4bcb635`.
3. Do not count merely eligible PIM assignments, Contributor, or similarly
   named/custom roles as Owner. Record group/assignment source references.
   Resolve applicable deny assignments and conditions. An inability to evaluate
   effective ownership is UNKNOWN and blocking, not `effective: false`.
4. For business ownership, prefer authoritative ServiceNow technical-owner
   records, approved subscription/application mapping, and record references.
   Record retrieval/validation time and a customer-approved freshness rule.
   Derive `freshUntil` from that rule, never an invented TTL.
   Keep stale evidence distinct from owner nonresponse.
5. Owner-tag data is a separate, provisional source unless the user explicitly
   authorizes it. Never promote Azure access into business accountability or
   silently fall back from ServiceNow to RBAC/tags.

Ownership evidence schema (all IDs/source references must come from real reads):

```json
{
  "tenantId": "<confirmed-tenant-uuid>",
  "principalId": "<confirmed-invoker-object-uuid>",
  "subscriptionIds": ["<approved-subscription-uuid>"],
  "collectedAt": "2026-09-30T12:00:00Z",
  "coverage": {"users": true, "rbacOwners": true, "businessOwners": true},
  "users": [
    {"id": "<resolved-user-object-uuid>", "displayName": "<exact-name>", "mail": "<email>", "userPrincipalName": "<upn>"}
  ],
  "ownerBindings": [
    {
      "kind": "rbac",
      "userId": "<resolved-user-object-uuid>",
      "scopeId": "/subscriptions/<approved-subscription-uuid>",
      "roleDefinitionId": "8e3af657-a8ff-443c-a75c-2fe8c4bcb635",
      "effective": true,
      "exclusionsChecked": true,
      "validatedAt": "2026-09-30T12:00:00Z",
      "source": "<assignment ID; active-state, transitive-membership and exclusion evidence references>"
    },
    {
      "kind": "business",
      "userId": "<resolved-user-object-uuid>",
      "scopeId": "/subscriptions/<approved-subscription-uuid>",
      "effective": true,
      "validatedAt": "2026-09-30T12:00:00Z",
      "freshUntil": "<UTC timestamp derived from approved freshness rule>",
      "freshnessRule": "<customer-approved rule and approval reference>",
      "source": "<ServiceNow record and approved scope mapping references>"
    }
  ]
}
```

Set a coverage flag to true ONLY after that source is completely evaluated for
the approved boundary. Unsupported/unavailable sources remain false. Retain the
underlying read responses securely; normalized flags are attestations, not
cryptographic proof of ownership. This pack does not provision a ServiceNow
connector or automate arbitrary RBAC condition interpretation.

## Resolve and compare the exact set

```powershell
python $helper resolve --scenario '.finops-runs\scenario.json' --catalog '.finops-runs\catalog.json' --out '.finops-runs\manifest.json'
```

The helper canonicalizes ARM IDs case-insensitively with scope-segment boundaries.
Tag keys are case-insensitive; tag values are case-sensitive. Region display
names resolve through authoritative aliases to location codes. Ambiguous
subscription/resource-group/MG/user names block rather than selecting all matches.
No matching resources blocks resource-filtered cost plans; it never broadens them.

For independent scope validation, supply `--resource-reference` with:

```json
{
  "scenarioSha256": "<hash of the approved scenario, emitted in the initial manifest>",
  "capturedAt": "2026-09-30T12:00:00Z",
  "source": "<independent portal/ARG resource-set export and same-definition provenance>",
  "resourceIds": ["<every matching full ARM resource ID>"]
}
```

Capture the independently resolved COMPLETE set, not just its count. Re-run
`resolve` to a new manifest with this reference before generating the cost plan.
Mismatched or duplicate IDs block validation. Without the reference, scope
precision is explicitly unverified.

Show the manifest's included/excluded subscriptions, exact IDs, source timestamps,
owner provenance, period, and cost basis to the invoker for approval before
cost queries. Non-resource charges and historical/deleted resources are not
invented members of a current-resource workload.
