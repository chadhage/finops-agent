---
name: finops-cost-evidence
description: "Analyze historical Azure spend, cost breakdowns, bill increases, cost spikes, and resource-level AKS or AI costs as the confirmed invoker. Use for read-only ActualCost/AmortizedCost queries, deterministic decimals, full pagination, currency isolation, evidence provenance, and exact Portal/Azure CLI reconciliation. Not forecasting, budgets, pricing, commitments, or utilization-based rightsizing."
---

# Exact Azure cost evidence and analysis

## Reusable executable toolkit

[finops.py](./scripts/finops.py) is a Python 3.11+ standard-library CLI, with no
pip dependencies. It is shared by the access, scope, and reporting skills.
The [contract](./references/evidence-contract.md) documents evidence shapes,
reference import, precision, supported boundaries, and source documentation.

Use the runtime selected for the workspace. Do not install dependencies or
CLI extensions automatically. Never process rounded MCP summaries into
supposedly exact source evidence.

For documented API selection, access/error troubleshooting, latency, or billing
semantics, load [Azure Cost Management documentation](../azure-cost-management/SKILL.md)
on demand and cite current official pages. This documentation skill is not a new
query adapter and does not change the helper's pinned API or validation contract.

## Preconditions

1. Complete invoker access and deterministic scope resolution.
2. Have the invoker approve the exact manifest before querying cost.
3. Choose ActualCost OR AmortizedCost, explicit inclusive UTC days, and
   original billing currencies. Do not combine bases, convert currencies,
   equate resource cost with an invoice, or invent missing cost.
4. Record whether the scope is all charges in selected subscriptions or the
   cost of an explicitly resolved CURRENT resource set. Historical billing
   tags/ownership are not silently substituted for current metadata.

## Route and qualify the analysis

Use the [analyst capability boundaries](./references/analyst-capabilities.md)
before choosing a workflow. This is a workspace-native port of useful
cost-analysis guidance, not an installation of the upstream Azure cost plugin
or its MCP tools. Keep the existing raw-evidence/Decimal helper; do not transform
rounded MCP summaries into exact costs or replace full pagination with top-N
query results.

### Historical spend and cost breakdowns

Confirm the question and requested breakdown. The helper supplies exact
resource/day/billed-location rows and original-currency totals. Use its emitted
values and complete evidence table. A top-ten HTML chart shows magnitude,
including credits; it is neither the complete population nor a highest-expense
ranking. Service, meter, invoice, or usage-unit breakdowns require a separately
reviewed adapter, not invented dimensions or a guessed tool call.

### Bill changes and cost spikes

1. Approve both complete UTC reporting windows, cost basis, currency partitions,
   population, and scope semantics before querying either period.
2. For current-resource comparisons, approve one fixed resource-ID population
   and verify both resolved manifests contain exactly that set. An all-charge
   subscription comparison can include new/deleted resources; disclose that
   population change rather than pretending it is a fixed-resource comparison.
3. Keep each period's plan, capture, internal controls, independent references,
   freshness, and validation status separate. `reconcile` compares independent
   captures of the SAME plan, never two different reporting periods.
4. Present helper-emitted exact amounts side by side. Different day counts,
   bases, membership, currencies, or incomplete periods do not establish a
   like-for-like trend. The helper does not calculate cross-period deltas,
   percentages, daily normalization, or anomaly scores; do not do that arithmetic
   in prose or an ad-hoc interpreter. Requests for those derived metrics need a
   reviewed deterministic calculation adapter.
5. Link observations to retained rows. A cost spike is not proof of cause,
   waste, fraud, an incident, or a measured saving. Keep possible explanations
   explicitly hypothetical unless independent authorized evidence supports them.

### AKS and AI service spend

Resolve and approve the exact resource membership using the scope skill.
Cluster-resource charges alone may omit separately billed nodes, disks, and
networking. Likewise, an AI resource total does not establish per-model,
per-deployment, or per-token spend. Report only the approved resources' measured
costs and disclose exclusions. Namespace/pod/model allocation, utilization, and
unit economics require authoritative additional sources and reviewed adapters.
Do not enable AKS cost analysis, monitoring, exports, or other configuration to
obtain missing data; those are Azure writes, outside this read-only workflow.

## Generate, inspect, and execute

```powershell
$helper = '.github\skills\finops-cost-evidence\scripts\finops.py'
python $helper plan --manifest '.finops-runs\manifest.json' --out '.finops-runs\plan.json'
python $helper query --plan '.finops-runs\plan.json' --out '.finops-runs\actual.json'
```

The helper:

- Pins the initial Cost Management Query API to `2025-03-01` for reproducibility.
- Generates only subscription-bound query POSTs, fixed Resource Graph query
  POSTs, and location-metadata GETs. No resource, policy, budget, or role writes.
- Queries exact resource-ID filters in disjoint chunks of 100 without truncating
  the workload; subscription-wide queries retain charges without a resource ID.
- Requests daily PreTaxCost by ResourceId and ResourceLocation, plus a separate
  ungrouped control query with IDENTICAL basis, period, scope, and filter.
- Parses raw numeric JSON directly into `Decimal`, never binary floating point.
  Aggregates at sufficient precision; monetary tolerance is exactly zero.
- Retains original currencies, negative credits, raw pages, hashes, Azure
  request IDs, response times, and the immutable plan.
- Follows every server continuation with the same POST body; preserves a
  server-returned API version rather than rewriting the URL. Rejects cross-host
  or cross-scope continuation, redirects, loops, unexpected rows/schema, missing
  pages, and detail/control mismatch.
- Distinguishes empty/204 responses, no matching current resources, access denial,
  unsupported billing schemas, transport errors, and incomplete collection.
  A successful empty response is not proof of zero spend.

Respect rate limits: one bounded retry is permitted for 429/503 when the numeric
retry delay is at most 60 seconds. Otherwise stop with the request ID.
Do not retry through a different identity or accept a partial bundle.

## Independently capture the manual reference

Preferred full-precision manual CLI comparison: have the invoker separately
execute the SAME saved plan, producing a different capture:

```powershell
python $helper query --plan '.finops-runs\plan.json' --out '.finops-runs\manual-reference.json'
python $helper reconcile --actual '.finops-runs\actual.json' --reference '.finops-runs\manual-reference.json' --out '.finops-runs\comparison.json'
```

Alternatively, import every raw Portal Query API or `az rest` response page
using `import-reference` and the documented index format. The helper compares
every resource/day/billed-location/currency row, including credits and
unallocated charges, not just totals. Missing/extra rows are mismatches even
when grand totals agree.

Identical plans bind tenant/invoker, manifest, scope, filters, UTC period,
cost basis, aggregation and API requests. A capture cannot validate itself.
CLI display formatters and rounded portal screenshots/CSV totals can lose
precision; they are not substitutes for raw numeric evidence. Do not massage
source values, add an epsilon, or round each row to force equality.

A mismatch yields a `mismatch` artifact and exit code 2. A reference with a
different plan or incomplete evidence is blocked. Retain all diagnostics.

## Acceptance and analysis

- Passing detail/control totals is INTERNAL consistency, not independent proof.
- Exact cost reference parity alone does not establish exact resource selection.
  The scope skill must also match an independent complete resource-ID set.
- `VALIDATED AGAINST CAPTURED REFERENCES` is bounded to those captures.
  Azure refreshes/rerates data; no claim of eternal parity or invoice finality.
- Use only preserved rows for measured cost drivers and trends. Keep hypotheses,
  Advisor savings, forecasts, retail estimates, and utilization metrics separate.
  Do not sum unrelated usage units or represent incurred spend as live utilization.

## Tests

Portal amounts versus query results are a REQUIRED acceptance check. Follow the
[Portal validation guide](./references/portal-validation.md) and populate the
[config stub](./assets/portal-validation.example.json) and
[Portal reference sample](./assets/portal-reference.example.json) with real
operator-approved evidence. Examples are rejected before Azure access.

```powershell
python -B '.github\skills\finops-cost-evidence\tests\run_tests.py' --repeat 10 --portal-config '.finops-runs\portal-acceptance\portal-validation.json' --portal-mode evidence
python -B '.github\skills\finops-cost-evidence\tests\run_tests.py' --repeat 10 --portal-config '.finops-runs\portal-acceptance\portal-validation.json' --portal-mode live --confirm-live-plan '<exact-approved-plan-sha256>'
```

Evidence mode compares supplied authoritative Portal exports/display totals
against a saved agent query; it does not freshly query Azure or authenticate the
invoker. Live mode additionally requires exact user/tenant/subscription/plan
approval and executes real read-only queries as that user.
Raw rows must match with zero tolerance AND the Portal displays must match
after aggregation at explicitly declared currency precision. A second CLI query
does not establish Portal equality. Missing evidence blocks normal acceptance.

Developer-only offline tests remain available:

```powershell
python -B '.github\skills\finops-cost-evidence\tests\run_tests.py' --offline-only --repeat 10 --seed 1729
```

Follow the [negative-first strategy](../../../TEST-STRATEGY.md): exhaust all
registered negative cases/repetitions before positives. Every sweep and campaign
persists Markdown/JSON reports; repeated pass/fail outcomes flag observed flakes,
and failures cannot be retried into a green verdict. Use `--negative-only` for
fault discovery without switching to positive cases.

Offline tests use synthetic data and mocked Azure boundaries; their passing
status explicitly says PORTAL PARITY NOT VALIDATED. Actual model conversations,
broader billing-offer/ownership-source coverage, and installed-browser behavior
still need separate evidence. Never promote a fixture-only Portal test into
CAPTURED_PORTAL_PARITY_PASS or LIVE_PORTAL_PARITY_PASS for a customer scenario.
