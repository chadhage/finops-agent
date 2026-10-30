# FinOpsAgent purpose-built test strategy

## Objective and acceptance rules

Find false success, wrong identity/scope, missing resource membership, incorrect
money, unsupported validation claims, and unreliable output BEFORE accepting the
agent. A passing helper suite is not proof that the model follows instructions
or that a live subscription matches the portal.

The test boundary is the
[agent](.github/agents/FinOpsAgent.agent.md), its five reusable skills,
the shared [helper](.github/skills/finops-cost-evidence/scripts/finops.py), CLI
entry points, and their evidence/report artifacts. Production behavior is not
silently repaired or failures marked expected while testing; discoveries remain
visible in reports for a separately approved fix.

The [local setup page](wiki/verification-setup.md) has classified offline tests
for config generation, evidence snapshots/precision, explicit attestations,
path/origin/token checks, single-campaign execution, and report/exit consistency.
Its server and browser assets are included in campaign source fingerprints.
These unit tests mock process/network boundaries; actual browser interaction
and real runner invocation require a separate end-to-end check.

### Strict execution order

1. Discover the complete finite executable catalog. Every test must have an
   explicit negative/positive classification. Unknown or duplicate IDs block.
2. Execute ALL negative cases, including all requested repeated/shuffled sweeps.
   Do not fail fast, quarantine failures, retry to green, or start a positive
   sweep while any negative attempt remains pending.
3. A negative case passing means invalid/adversarial input was rejected with
   the expected explicit failure and no successful artifact. A negative case
   failing means a defect, missing guard, crash, or broken test was observed.
4. Once every negative attempt has run, execute positive sweeps, even if some
   negatives failed, to characterize valid behavior. Those failures still make
   the entire campaign FAIL. Execution exhaustion is not a pass gate.
5. Skips, expected-failure suppressions, worker crashes/timeouts, incomplete
   journals, or discovery errors are NOT exhausted coverage: block positives.
6. Persist Markdown AND machine-readable JSON after EVERY sweep and at campaign
   completion, including errors/interruption. Flush a per-case JSONL journal so
   a failed worker cannot erase completed evidence.

"Exhaust all negative tests" means the registered, bounded catalog and its
declared repetitions. It is not a claim to enumerate every possible malformed
input, all model behaviors, or every Azure configuration.

## How to run

Developer-only offline checks need no third-party packages, model invocation,
credentials, Azure subscription, network connection, or browser:

```powershell
$runner = '.github\skills\finops-cost-evidence\tests\run_tests.py'
python -B $runner --offline-only --repeat 10 --seed 1729
```

For the complete current executable catalog with measured line coverage:

```powershell
python -B $runner --offline-only --repeat 10 --seed 4701 --coverage
```

Coverage is collected with the Python standard library and merged across
worker sweeps. It reports bytecode executable lines for the helper, Portal
validator, runner, and setup server, with exact uncovered line numbers in JSON.
It is **not branch coverage**, and imports/entry points outside test execution
can remain uncovered. A high percentage is not proof of correct agent behavior.

The current pack contains five skills: invoker access, scope resolution, cost
evidence/analysis, reporting, and public Azure Cost Management documentation.
Static skill tests verify discovery metadata, relative links, agent tool
configuration, capability boundaries, and source-index integrity. Static tests
do not establish that a model will load or obey a skill.

Additional tool layers are executable separately:

```powershell
# Real CLI processes and real browser/PDF output from synthetic evidence only.
python -B '.github\skills\finops-cost-evidence\tests\run_local_integration.py' --browser '<installed-Chromium-compatible-executable>'
# Actual model refusal/clarification probes, with ALL tools disabled.
python -B '.github\skills\finops-cost-evidence\tests\run_agent_probes.py' --repeat 2
```

Both runners retain their own reports. The local-tool runner completes its
negative cases before positives. The restricted model runner exhausts negative
prompts/repetitions before positive prompts, records response/oracle/model
events, and marks behavior **PENDING HUMAN REVIEW**, not automatically passed.
Its isolated workspace uses the actual agent text and supplies all five skill
texts as reference context; automatic skill discovery and tool-enabled model
conversations are NOT tested by that restricted mode. No Azure data or
credentials are supplied. Disable configured MCP servers with repeated
`--disable-mcp-server` options when running those probes.

The loopback setup UI additionally needs actual-browser checks for invalid
inputs, explicit API errors, stale review invalidation, preparation, starting
the real runner, polling, history, filtering, and artifact download. Use a new
test tab/run rather than changing another user's prepared setup. Start a bounded
local helper when the shared page's previous server is no longer running, and
stop only that helper after validation.

For fault discovery without any positive execution:

```powershell
python -B $runner --negative-only --repeat 10 --seed 1729
```

Normal acceptance additionally REQUIRES Portal parity, using one of:

```powershell
python -B $runner --repeat 10 --portal-config '.finops-runs\portal-acceptance\portal-validation.json' --portal-mode evidence
python -B $runner --repeat 10 --portal-config '.finops-runs\portal-acceptance\portal-validation.json' --portal-mode live --confirm-live-plan '<exact-approved-plan-sha256>'
```

The [Portal validation guide](.github/skills/finops-cost-evidence/references/portal-validation.md)
defines authoritative inputs, rejected stubs, scope/identity approval, freshness,
raw zero-tolerance comparison, and display rounding. Missing Portal inputs block
acceptance. Evidence mode cannot claim a fresh Azure query; live mode requires
real invoker authentication and explicit matching plan confirmation.
No live stage runs while offline failures remain.

The runner prints the unique output directory under
`.finops-runs\tests\<UTC-run-id>`. Files are:

- `report.md` / `report.json`: aggregate verdict, provenance, coverage limits,
  counts, order, every case outcome, first failure traces, and flake analysis.
- `negative-01.md` / `.json`, etc.: reports immediately after each sweep.
- `positive-01.md` / `.json`, etc.: only after negative execution is exhausted.
- `negative-01.jsonl`, etc.: flushed per-test results including captured output.

Exit codes: `0` all requested checks passed (offline-only is explicitly NOT
acceptance); `1` test/parity failures or incomplete execution; `2` blocked
Portal acceptance or runner/discovery/configuration failure; `130` interruption.
An output filesystem failure is an explicit runner failure, never an assertion
that a report was saved. No program can promise persistence after forced process
termination/power loss; the last flushed journal/checkpoint is recoverable.

Use the workspace-selected Python executable. Direct `unittest discover` is
for debugging only: it bypasses campaign ordering and reporting and is not an
acceptance run.

## Layers, oracles, and failure modes

| Layer | Negative tests first | Positive controls after negatives | Exact oracle |
|---|---|---|---|
| Invoker/auth | Wrong tenant/user/audience/cloud, app-only identity, disabled subscription, missing CLI, expired/near-expiry token, malformed profile, login failure. | Confirmed interactive identity; tokens remain out of artifacts. | Bound tenant/object/subscription IDs; explicit exit 2, no fallback or account mutation. |
| Input schema | Missing required fields, unknown filters, null/wrong shapes, boolean/decimal schema versions, empty arrays, invalid UTC/calendar days, reversed/partial days. | Approved UUIDs, complete UTC days, either supported cost basis. | Fail closed with a diagnostic; no crash or success-shaped output. |
| Resource scope | Unapproved subscription, ambiguous names/emails, MG expansion, malformed/duplicate ARM IDs, missing inventory/regions, empty matches, case-sensitive tag mismatch. | AND across categories, OR within values/users, multiple tags, nested-group provenance, disjoint multi-subscription plans. | Exact normalized resource-ID set, not just resource count. |
| Ownership | Inactive Owner, Contributor/custom role confusion, incomplete groups/ancestry/denies/PIM, stale CMDB record, blank source/freshness. | Distinct RBAC/business semantics with source references and customer-approved freshness. | Effective ownership is proven or blocked; no invented accountability. |
| Resource Graph | Missing continuation, repeated token, count drift, invalid metadata types, duplicate IDs, truncated result. | Stable all-page enumeration. | Every page and unique ID; exact count and complete metadata. |
| Cost transport | 400/401/403/404/500/504, exhausted 429/503 retry, excessive delay, timeout, cross-host/scope continuation, redirect. | One bounded retry, complete same-body pagination. | Explicit status/request ID; bounded calls; no partial success, token leakage, or scope change. |
| Cost evidence | Missing/extra requests/pages, duplicate rows/URLs, schema drift, 204 body, null/boolean/string cost, missing currency, out-of-scope/date records, control mismatch. | Chunk boundaries 1/99/100/101/199/200/201; zero records versus real zero charges; credits and multiple currencies. | Full raw numeric evidence, no floats, exact internal controls per currency. |
| Reconciliation | Self-reference, different plan/basis/currency/resource/day/region, equal grand total with changed allocation. | Independently captured identical plans and exact rows in any order. | Zero tolerance AND identical resource/day/location/currency keys. |
| Required Portal parity | Samples, CLI data relabeled as Portal, absent attestation, stale evidence, mismatched Portal requests/display totals, missing/expired live approval, changed invoker or scope. | Authoritative saved capture comparison and explicitly approved fresh live query; raw rows and declared-currency displays match. | No full acceptance without Portal evidence; no live claim in evidence-only mode; source row tolerance exactly zero. |
| Report | False validated status, malicious source markup, overwrite/write denial, missing browser, exit-zero/no PDF, print timeout. | End-to-end resolve/plan/import/reconcile/Markdown/HTML; exact credits/currencies and hashes. | Same amounts and lineage; no false success, implicit FX, public upload, or silent fallback. |
| Test harness | Unclassified tests, negative skip/expected failure, partial journal, discovery failure, early positive scheduling, retry-to-green. | Each sweep emits both reports; all negatives precede positives. | Persisted execution order and nonzero final verdict on any failure. |

Negative cases are independently named where possible; data-driven mutations
become individual unittest IDs, rather than one aggregate assertion that stops
at the first bad input. Existing mixed tests are classified by their primary
rejection/guard objective; valid setup/calibration inside them is not a positive
suite running early.

### Money and resource truth

- Use synthetic immutable UUIDs and `example.test` identities only.
- Compare complete sorted ID sets with explicit expected members.
- Include two subscriptions, same display names, overlapping resource-group
  names, MG ancestors, two users, owner kinds, two tag keys, and region aliases.
- Include fractions below one cent, many significant digits, large cancellation,
  negative credits, zero rows/zero records, USD and EUR, and ordering permutations.
- Preserve raw numeric lexemes. Assert `0.004 + 0.004 = 0.008` in exact evidence
  and only then `$0.01` in the labeled USD display.
- Intentionally swap allocation while keeping totals equal. A total-only
  comparison must fail. Separate resource precision from query completeness,
  monetary parity, portal display rounding, allocation, and final invoices.

## Finding and identifying flaky tests

### Automated observation

The runner repeats each case with unchanged source fingerprints, interpreter,
business clock, and fixtures, but different seeded within-phase order and
`PYTHONHASHSEED`. Each sweep uses a fresh process. Keep every failure; never
overwrite it with a successful retry.

- **Observed flaky**: the SAME test both passes and fails/errors in this sample.
- **Consistent failure**: failure/error without a passing attempt; investigate
  as a reproducible defect or broken test, not a flake.
- **Stable in sample**: every repetition passed; does not prove zero flakiness.
- **Incomplete**: skip/expected-failure or missing execution; no green coverage.
- **Insufficient repetitions**: one passing attempt cannot establish stability.

The detector itself is calibrated with an injected pass/fail sequence. A
synthetic calibrator detecting flakiness is not evidence that production tests
are flaky. Changes in code, fixtures, model, clock, or browser are separate
experiments, not interchangeable repetitions.

### Targeted susceptibility checks

| Candidate | Why it can vary | Control / diagnosis |
|---|---|---|
| Catalog/capture timestamp tests and `resolve_scope` consumers | Fixed dated fixtures can become future/past under the wall clock or clock skew. | Freeze business clock by default; record it; use explicit clock-boundary fault cases. |
| JWT/identity and token-expiry tests | Near-expiry timing, clock drift, shared CLI cache, user changes. | Synthetic claims and frozen `time.time`; explicit safety-boundary test; no real CLI cache in offline runs. |
| Retry tests | Real sleep, throttling, Azure ingestion refresh and latency. | Mock sleep/transport; assert call counts; live tests have a separately recorded environment. |
| Legacy inventory/owner merge test | CMDB freshness depends on collection time. | The existing exact as-of patch remains active; test stale and valid intervals independently. |
| Decimal/permutation tests | Global decimal precision, unordered inputs, leaked global state. | Low-precision/permutation controls and shuffled repeated sweeps. |
| Browser/PDF integration | Installed runtime behavior, startup races, locks, fonts, OS, profile state. | Mock failures offline; separately pin executable/version and validate actual PDF text/page output. |
| Customization discovery | Skill count, workspace state, harness tool inventory. | Record customization/source hashes; do not label a changed workspace as a random flake. |
| Real conversational agent | Model nondeterminism, tool availability, retrieval order, approval state. | Restricted decision probes record the selected model and replies; full tool-enabled traces still need explicit harness integration and invariant oracles, not prose snapshots. |

No external/browser/model-dependent test is silently marked passed by this
offline campaign. Report missing execution explicitly.

## Actual bot conversations: separate required acceptance layer

The [conversation matrix](.github/skills/finops-cost-evidence/tests/agent_conversations.json)
contains negative prompts AG-N01..AG-N24 and positive prompts AG-P01..AG-P10.
They are deliberately **NOT RUN** by the deterministic helper runner.
Static existence of agent instructions cannot prove model compliance.
The ported analyst guidance adds cases for capability/tool confusion,
comparison validity, causal claims, AKS/AI allocation, invoice boundaries,
and magnitude-chart versus complete signed-cost evidence.
Documentation-skill cases also cover public-source retrieval and web fallback
without Azure authentication, private-data disclosure, and refusal to execute
upstream configuration/deployment examples.

To run this layer:

1. Use a fresh VS Code agent conversation per case with recorded model/harness,
   agent/skill hashes, tool inventory, settings, and deterministic synthetic tool
   responses. Do not grant live write access or expose real credentials.
2. Execute every negative conversation and requested repetition BEFORE positive
   conversations. Record the whole request, clarifications, approvals, tool
   calls/arguments/results, and final artifacts; evaluate trace invariants.
3. Evaluate scope/identity/approval ordering on actual tool traces, not just a
   final sentence promising to be careful. Treat attempted forbidden operations
   as failures even if the tool denies them.
4. Compare final resource IDs, every monetary row, status, currencies, provenance
   and artifact existence with golden fixtures. Do not score exact prose wording.
5. Emit a per-run report with each case's expected/actual trace and repeated
   outcomes. Keep this layer NOT RUN until real trace evidence is retained.

Portal-to-query parity is a required executable acceptance layer, not merely an
opt-in future test. Supplied evidence compares authoritative Portal exports with
a saved invoker-bound query; live mode verifies the current invoker and re-queries
Azure after approval. Keep the two statuses distinct. Neither fabricated stubs
nor a second CLI query can establish Portal origin.
Directory/CMDB permissions, historical scope, offer-specific schemas outside the
selected scenario, final invoices, and real browser output cannot be certified
by mocks or by one successful Portal scenario.

## Release decision

Accept only when all required layers have executed with:

- Zero unauthorized identity/scope/write operations.
- Exact resource sets and exact monetary parity under the approved definition.
- No false successful artifact or unsupported validated/invoice claim.
- No unresolved failing/flaky cases, skips, expected-failure suppression, or
  missing negative coverage.
- Successful positive controls and documented independent live/reference
  acceptance where the deployment requires it.

The report must say **FAIL** when defects are found and **NOT RUN** for excluded
layers. A useful strategy can discover a red system; it must not manufacture a
green result.
