# FinOps evidence contract

## Scope and implementation boundary

This toolkit is a local Python 3.11+ standard-library CLI invoked by a VS Code
custom agent. It uses the confirmed user's Azure CLI ARM token in memory.
It is not a deployed service, app registration, new service principal, OBO
exchange implementation, invoice connector, or automatic ServiceNow integration.

Currently supported:

- Public Azure, enabled subscriptions, one confirmed resource tenant/invoker
  per scenario, explicit subscription allowlists.
- Current ARG resources and resource-group/MG/location metadata.
- Source-attested, completely evaluated RBAC/business owner evidence, with
  explicit provenance. Directory/CMDB reads and condition interpretation are
  performed through approved tools/connectors before normalization.
- Current-resource-set cost views or all-charge selected-subscription views.
- Cost Management Query API `2025-03-01`, ActualCost/AmortizedCost,
  daily PreTaxCost by resource/location, explicit complete UTC days.
- Complete raw query-reference capture/import and exact per-row reconciliation.
- Markdown, standalone HTML, and installed Chromium-compatible PDF output
  (Edge, Chrome, or Chromium headless shell).

Unsupported or unverified inputs block rather than falling back to estimates:
sovereign clouds, cross-tenant scenarios, historical ownership/tag membership
without a separate adapter, unresolved denies/conditions/group membership/PIM,
incomplete permissions, alternative cost-response schemas, and invoice finality.

## Data flow and files

| Artifact | Produced by | Purpose |
|---|---|---|
| Scenario | Invoker-approved inputs | Immutable identity, approved subscription UUIDs, period, basis, selectors. |
| Ownership evidence (optional) | Approved read-only sources | Directory identities, scope bindings, active/effective evaluation, source references and freshness rules. |
| Catalog | `inventory` | All caller-visible current resources/containers and locations, coverage flags, raw source pages. |
| Resource reference (optional) | Independent manual export | Complete same-definition current resource-ID set and scenario hash. |
| Manifest | `resolve` | Exact included/excluded subscriptions and resolved resource IDs; owner evidence and source hashes. |
| Plan | `plan` | Generated requests bound to that manifest; detail/control pairs and disjoint resource chunks. |
| Capture bundle | `query` or `import-reference` | Plan, unique capture ID, source, times, every raw response page and hash. |
| Comparison | `reconcile` | Exact-match/mismatch, zero tolerance, per-row differences, both capture hashes. |
| Report | `report` | A single evidence model serialized as Markdown/HTML/PDF. |

Output paths must not exist; the helper never overwrites a user's artifact.
Use a new per-run directory under an approved local evidence location.
The repository ignores `.finops-runs` and Python caches. Do not commit workload
evidence, directory personal data, tokens, invoices, or customer reports.

Hashes detect changes, not authenticity or factual completeness. Coverage flags
mean the source was evaluated over the declared caller-visible boundary; they
cannot prove unknown invisible resources do not exist. Source attestations and
independent references must not be manufactured by the model.

## Filter contract

Supported `selection` fields:

| Field | Values |
|---|---|
| `subscriptionIds`, `subscriptionNames` | Nonempty arrays of UUIDs/exact display names; combined with OR. |
| `managementGroupIds`, `managementGroupNames` | Full MG IDs/exact display names; approved ancestry only. |
| `resourceGroupIds`, `resourceGroupNames` | Full ARM IDs/exact names; ambiguous cross-subscription names block. |
| `resourceIds` | Full, currently inventoried resource ARM IDs inside selected subscriptions. |
| `owners` | `{"kind":"rbac|business|either","users":["object-id or exact name/UPN/mail"]}` |
| `tags` | Nonempty array of `{"key":"Application","values":["checkout","payments"]}`. |
| `regions` | Canonical Azure codes or authoritative location display names. |

OR within a category; AND across categories. AND across tag keys, OR across
values for one key. Resource/tag/region/owner filters produce a current-resource
ID set and query its historical period cost. This differs from filtering billed
historical tags or attribution. ARM IDs/tag keys are case-insensitive; tag
values are case-sensitive; names match exactly, case-insensitively, with a unique
ID required. Unknown fields and empty supplied selectors are errors.

Subscription/MG-only selection queries ALL charges in the selected subscriptions,
including blank resource IDs and historical resources absent from ARG. Any
resource-level filter queries only matching current resource IDs: non-resource
charges and deleted resources outside that current set are EXCLUDED, not
silently allocated. Reports state that this is not whole-workload allocation.

## Cost and pagination invariants

- Initial API version is pinned and retained in the plan. Follow only
  server-returned HTTPS continuation links at the same host and query path.
  A documented continuation may contain a different API version; retain it
  verbatim with the original POST body. Do not forward tokens on redirects.
- Query every disjoint resource chunk and every page. Count changes,
  duplication, missing pages, schema drift, unknown currency, cross-scope rows,
  or out-of-period dates block validation.
- Read raw JSON numeric lexemes into `Decimal`. Do not route money through
  floats, shell formatting, spreadsheet cells, or chart-library calculations.
- Aggregate at sufficient decimal precision with no rounding before aggregation.
  Preserve negative credits and isolate every ISO billing currency.
  Reports also provide an explicitly separate USD display, half-up to two
  decimals AFTER summation. Other currency display precision is not assumed.
- Compare detail sums with an independently issued aggregate query for the SAME
  parameters. If Azure refreshes between the requests, a mismatch blocks output;
  recollect, do not introduce a tolerance.
- Empty/204 success means "no records returned", not proof of zero spend.
  `401`/`403`, unavailable billing data, and truncation are not empty success.
- A safety limit of 10,000 pages blocks rather than returning a truncated success.
- HTTP 429/503 can retry once when the server's numeric delay is at most 60
  seconds. Other errors surface HTTP status and Azure request ID.

## Independent Portal/Azure CLI reference import

Portal equality additionally requires the executable
[Portal validation gate](./portal-validation.md): genuine operator-attested
Portal request/response exports, displayed totals, matching plan/scope, explicit
freshness limits, and (for live mode) current invoker authentication and approval.
The general CLI reference workflow below proves captured-query parity, NOT
Portal parity by itself. Sample inputs cannot pass the required gate.

The simplest manual CLI reference is a separate `query` invocation with the
same saved plan and confirmed identity. Its capture ID must differ.
For raw Portal Query API or `az rest` output, save all responses without editing
numeric values and provide an index next to the files:

```json
{
  "source": "manual-azure-cli",
  "tenantId": "<same-confirmed-tenant-uuid>",
  "principalId": "<same-confirmed-invoker-object-uuid>",
  "capturedAt": "2026-09-30T12:00:00Z",
  "captures": [
    {
      "requestId": "<first request id from plan.requests>",
      "pages": [
        {
          "path": "detail-page-1.json",
          "url": "<exact first request URL>",
          "status": 200
        },
        {
          "path": "detail-page-2.json",
          "url": "<exact nextLink from detail-page-1.json>",
          "status": 200
        }
      ]
    },
    {
      "requestId": "<control request id from plan.requests>",
      "pages": [
        {
          "path": "control-page-1.json",
          "url": "<exact control request URL>",
          "status": 200
        }
      ]
    }
  ]
}
```

Include every request in the actual plan, not just the two illustrative entries.
`source` is `manual-azure-cli` or `portal-query-export`. HTTP 204 requires an
empty response file. `path` is relative to the index directory; network-share
reference paths are unsupported. The import records user-supplied identity/
capture-time provenance; it cannot independently authenticate a portal export.
Do not present that attestation as token-signature verification.

To replay one request through Azure CLI after confirming its identity:

```powershell
$plan = Get-Content -LiteralPath '.finops-runs\plan.json' -Raw | ConvertFrom-Json
$request = $plan.requests[0]
$request.body | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath '.finops-runs\request-body.json' -Encoding utf8
az rest --method post --url $request.url --body '@.finops-runs\request-body.json' --output json |
    Set-Content -LiteralPath '.finops-runs\detail-page-1.json' -Encoding utf8
```

Repeat for all requests and follow every `properties.nextLink` with the SAME
body. Never use a default CLI account different from the confirmed invoker.
Some CLI formatters reserialize/round numeric values; if full source precision
is not retained, use the raw-preserving helper capture instead. A screenshot or
rounded CSV aggregate is not an exact resource/day/location/currency reference.

```powershell
$helper = '.github\skills\finops-cost-evidence\scripts\finops.py'
python $helper import-reference --plan '.finops-runs\plan.json' --index '.finops-runs\reference-index.json' --out '.finops-runs\manual-reference.json'
python $helper reconcile --actual '.finops-runs\actual.json' --reference '.finops-runs\manual-reference.json' --out '.finops-runs\comparison.json'
```

The comparison requires the identical sealed plan, so differences in invoker,
tenant, manifest, resource IDs, UTC dates, cost basis, currency-bearing rows,
filters, grouping, and requests cannot be silently ignored. Monetary tolerance
is zero. It checks row-key sets and values, not just grand totals. Matching
capture/reference artifacts do not guarantee future data will remain unchanged.

## Validation status

- **Blocked**: invalid/missing/ambiguous inputs, source/permission failure,
  incomplete collection, control mismatch, or supplied reference mismatch.
  No successful validated report. The CLI exits 2; `reconcile` persists explicit
  row differences with `status: mismatch` before exiting 2.
- **Unverified**: internally consistent complete evidence, but an independent
  exact resource-set reference or cost reference is absent.
- **Validated against captured references**: independent current resource sets
  match exactly AND all separately captured cost rows match with zero tolerance.

Scope matching, complete query collection, raw numeric cost parity, portal display
rounding, workload allocation, and final invoices are SEPARATE assertions.
The model must not certify universal 100% accuracy, hidden resource coverage,
real-time usage, or future billing parity.

## Authoritative references

- [Cost Management Query API](https://learn.microsoft.com/en-us/rest/api/cost-management/query/usage?view=rest-cost-management-2025-03-01)
- [Cost Management data, rounding, updates, tags and historical resources](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data)
- [Resource Graph pagination](https://learn.microsoft.com/en-us/azure/governance/resource-graph/concepts/work-with-data)
- [Azure role assignments](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments)
- [Azure CLI role assignment list](https://learn.microsoft.com/en-us/cli/azure/role/assignment#az-role-assignment-list)

Microsoft's optional `cost-analysis` skill is available in the `azure-cost`
plugin. It is not required or automatically installed. In Copilot CLI, opt-in
installation is `/plugin marketplace add microsoft/azure-skills`, then
`/plugin install azure-cost@azure-skills`. If used, preserve this contract's
scope/precision/reference gates; do not treat a rounded tool summary as raw
reconcilable evidence.
