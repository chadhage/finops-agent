# Required Azure Portal parity validation

Portal equality is an executable acceptance gate, not an assumption inferred
from green unit tests. Two modes are supported:

For an interactive config/reference-index form, suite invocation, and outcome
display, use the [local verification setup page](../../../../wiki/verification-setup.md).
The page supports offline and captured-evidence checks only; live mode remains
an explicitly approved CLI workflow.

| Mode | Authoritative input | What runs | Passing status |
|---|---|---|---|
| `evidence` | Operator-supplied Portal request/response exports, displayed totals, and a saved invoker-bound agent query capture. | Local full-precision comparison; no Azure connection. | `CAPTURED_PORTAL_PARITY_PASS`; no fresh live query is claimed. |
| `live` | The same Portal evidence plus explicit, time-bounded identity/scope/plan approval. | Reauthenticate the confirmed invoker and issue fresh read-only Cost Management queries. | `LIVE_PORTAL_PARITY_PASS`. |

A missing config, example data, missing authority attestation, wrong scope/basis,
stale evidence, incomplete pages, or mismatch cannot pass. Another CLI query is
NOT a substitute for Portal-origin evidence.

## 1. Prepare the approved scope and plan

Follow the invoker-access and scope-resolution skills first:
Use the [scenario/scope stub](../assets/scenario.example.json) as a starting
schema, replacing every illustrative value with confirmed inputs.

1. Confirm the tenant and invoker object ID using the user's own Azure CLI login.
2. Obtain explicit approved subscription IDs, workload filters, complete UTC
   days, and ActualCost OR AmortizedCost.
3. Collect the complete current inventory. Supply an independent exact resource
   reference when resolving the manifest; `scopeReference.status` must be
   `exact-match`.
4. Show the resolved manifest and plan to the invoker for approval.
5. Retain the generated plan unchanged. Its `sha256` binds the identity,
   resource set, subscriptions, reporting period, basis, filters, and requests.

No live query is authorized merely by opening or copying a sample.

## 2. Copy the stubs into a private, new run directory

Use the four files under `assets` as schema examples:

- [Validation config](../assets/portal-validation.example.json)
- [Portal reference index](../assets/portal-reference.example.json)
- [Detail response format](../assets/portal-detail-response.example.json)
- [Aggregate control response format](../assets/portal-control-response.example.json)

The examples are deliberately marked `isExample: true`, contain placeholders,
and do not approve live access. Validation rejects them before any Azure login
inspection or cost query.

For example, from the project root:

```powershell
$run = '.finops-runs\portal-acceptance'
New-Item -ItemType Directory -Path $run -ErrorAction Stop | Out-Null
$assets = '.github\skills\finops-cost-evidence\assets'
Copy-Item -LiteralPath "$assets\portal-validation.example.json" -Destination "$run\portal-validation.json"
Copy-Item -LiteralPath "$assets\portal-reference.example.json" -Destination "$run\portal-reference.json"
```

Choose another directory if it already exists. Set `portalIndexPath` to
`portal-reference.json`; all paths are local paths relative to their containing
config/index file unless absolute. Never commit the populated files.

## 3. Collect authoritative Portal evidence

In Azure Portal **Cost Management > Cost analysis**:

1. Use the same confirmed identity, exact scope/resource IDs, custom UTC dates,
   cost basis, original currencies, and filters as the approved plan.
2. Capture the matching Cost Management query **request body**, exact URL, and
   **every raw response page**, including continuations and control queries.
   The supported response shape is the plan's daily
   ResourceId/ResourceLocation/UsageDate/PreTaxCost/Currency detail plus the
   ungrouped currency control.
3. Record the displayed full currency amounts, not shortened `K`/`M` values,
   screenshots alone, or a sum of rounded resource rows.
4. Preserve raw JSON numeric values exactly. Do not copy source costs through
   spreadsheet formatting, floats, or a formatter that changes precision.
5. Save only sanitized request bodies and response bodies. Do NOT save an
   unsanitized HAR, Authorization headers, cookies, tokens, or credentials.
6. Populate the reference index with the request IDs from the approved plan,
   the ACTUAL Portal request bodies, response paths, URLs, HTTP statuses,
   capture time, Portal view URL, and displayed totals.

The actual Portal requests must match the generated plan; arbitrary Portal
views, different grouping/billing measures/API versions, rounded CSVs, and
unsupported schemas are rejected, not silently normalized into a match.
If the Portal export does not have the required full-precision shape, collect
a compatible view/export or add a separately reviewed adapter before claiming
validation. Do not relabel a CLI response as a Portal export.

For each currency, `displayedTotals` contains:

```json
{"currency": "USD", "amount": "1234.56", "decimalPlaces": 2}
```

`amount` is the observed full Portal amount as a normalized decimal STRING,
without currency symbols or thousands separators. `decimalPlaces` is the
actual display precision for that view/currency, not an assumed two decimals.
Comparison uses half-up rounding AFTER aggregation, separately from zero-
tolerance raw resource/day/location/currency comparison. Other rounding/view
conventions require a verified adapter.

Only after replacing samples with real evidence may the operator set
`isExample: false` in the config/index and attest the three authority/scope/
sanitization flags. Raw example responses must be replaced with actual exports,
not made "real" by editing their markers or fabricated amounts.

These are operator attestations, not cryptographic proof that a browser export
originated in Portal. The agent must not invent or self-approve them.

## 4a. Compare supplied authoritative inputs

Set `actualPath` to a saved capture produced by the invoker-bound `query`
command, not a Portal capture or synthetic fixture. Set `approvedPlanSha256`
to the approved plan hash. Choose `maxEvidenceAgeSeconds` explicitly; future
or older evidence is blocked.

```powershell
$runner = '.github\skills\finops-cost-evidence\tests\run_tests.py'
python -B $runner --repeat 10 --portal-config '.finops-runs\portal-acceptance\portal-validation.json' --portal-mode evidence
```

This runs every negative sweep before positive sweeps, then the required
Portal comparison. Passing status is explicitly **captured evidence parity**,
not a claim that Azure was queried again or that identity was verified this run.

## 4b. Run approved read-only live validation

In addition to the Portal inputs, populate `liveApproval` with:

- `confirmed: true`, only after explicit user approval.
- The exact tenant ID, invoker object ID, sorted selected subscription IDs, and
  approved plan hash.
- Actual UTC approval and expiry times.

Then pass the same plan hash as a runtime confirmation:

```powershell
python -B $runner --repeat 10 --portal-config '.finops-runs\portal-acceptance\portal-validation.json' --portal-mode live --confirm-live-plan '<exact-approved-plan-sha256>'
```

The live stage runs only after the offline suite passes. It uses the real clock,
not the offline worker's frozen clock; verifies the Azure CLI user/token for
each selected subscription; executes only the generated read-only plan; and
preserves every raw page and request ID.

There is no automatic login, account switch, role grant, resource write, or
service-identity fallback. The selected user must have resource/cost read access.
Tenant policy, billing-offer support, directory/CMDB permissions, and source
freshness still apply.

## Reports and failures

Each validation run saves Markdown/JSON reports. The Portal stage also saves the
raw actual capture, imported Portal reference, exact per-row differences, display
comparisons, plan/index fingerprints, mode, and whether identity/live queries
were performed in that run.

- Exact raw costs are compared with **tolerance 0** at each row key.
- Portal displays are compared only AFTER exact per-currency aggregation.
- Missing/extra rows or currencies fail even if grand totals happen to match.
- A query with no records cannot prove zero spend; real zero-cost rows can match.
- A genuine Azure refresh/rerating difference remains a mismatch. Refresh both
  references in a new run; never add a tolerance or retry away the red report.

For developer-only tests, explicitly use:

```powershell
python -B $runner --offline-only --repeat 10
```

That result says **PORTAL PARITY NOT VALIDATED**. Running the normal acceptance
command without authoritative Portal inputs is blocked and nonzero.
Direct Portal-only diagnosis is also available through
`scripts\portal_validation.py --config <file> --mode evidence|live`; its report
does not substitute for passing the complete offline acceptance suite.
