# Local verification setup page

The [setup utility](../tools/verification_setup/server.py) provides a local
browser form for the existing negative-first test suite. It generates the
verification config and, optionally, the Portal reference index, invokes the
unchanged runner, and displays its saved results and diagnostics.

## Start the page

From the workspace root, using the existing Python 3.11+ interpreter:

```powershell
python -B 'tools\verification_setup\server.py'
```

Open the printed loopback address, normally `http://127.0.0.1:8765`.
If that port is in use, choose another with `--port 8766`, or use `--port 0`
for an available port. No packages, Node.js, MCP server, Azure login, or
deployment are required to start the page.

Evidence defaults to the ignored `.finops-runs` directory. Paths in the form
can be workspace-relative or absolute. To approve another local input directory
explicitly at startup:

```powershell
python -B 'tools\verification_setup\server.py' --evidence-root 'C:\PrivateEvidence\finops'
```

The server binds only to `127.0.0.1`, rejects other hosts/cross-origin requests,
and uses a per-server token for mutations. Files outside approved evidence
roots, UNC paths, and parent-directory traversal are rejected. Only run-local
JSON, JSONL, Markdown, and log artifacts can be downloaded.
This is a single-user local utility, not a production or multi-user service;
it does not isolate files from other users/processes with local OS access.
Do not expose it through a proxy, tunnel, or public listener.

## Option A: offline developer checks

1. Select **Offline developer checks**.
2. Set repetitions per phase, shuffle seed, frozen offline-test clock, and
   per-sweep timeout. Defaults match the runner's default settings.
3. Select **Generate setup for review**; inspect the command.
4. Select **Run verification suite**.

This mode needs no customer evidence. It executes all requested negative sweeps
before positives, but explicitly reports **PORTAL PARITY NOT VALIDATED**.
A green offline suite is not acceptance, live Azure parity, model-conversation
qualification, or installed-browser PDF validation.

## Option B: captured Portal evidence

First follow the [Portal validation guide](../.github/skills/finops-cost-evidence/references/portal-validation.md)
to obtain genuine, sanitized evidence and an approved plan. The setup page
does not collect inventory, generate/approve a resource scope, authenticate
Azure, or capture Portal traffic for you.

Enter:

| Input | Meaning |
|---|---|
| Approved plan JSON path | Unchanged helper-generated plan with an independent `exact-match` resource-set reference. Load it to inspect tenant, invoker, subscriptions, dates, cost basis, and every generated request. |
| Approved plan SHA-256 | Paste the exact hash after reviewing the immutable plan. |
| Actual capture path | Saved capture from the approved invoker-bound Azure query, not synthetic data or relabeled Portal evidence. |
| Maximum evidence age | Explicit positive seconds; applies to real evidence/attestation timestamps, not the frozen offline clock. |
| Portal capture time and view URL | Actual UTC capture time and `https://portal.azure.com/` view URL without query parameters/credentials. |
| Displayed totals | One entry per original billing currency. Amounts remain decimal **strings**, with the actual observed display precision (0..8). No FX, K/M abbreviations, or sum of rounded rows. |
| Request-body files | The actual sanitized Portal request-body JSON for every detail/control request; they must match the plan. Expected plan bodies are shown only as references, never fabricated as exports. |
| Raw response pages | Every unmodified response-body JSON file, its exact initial/continuation URL, and HTTP status. Add all continuation pages. |
| Attestations and confirmation time | Four explicit confirmations: genuine Portal exports, matching approved scope/view, no credentials, and genuine saved invoker query. None are pre-checked. |

UTC times use `YYYY-MM-DDTHH:MM:SSZ`. **Use current UTC** fills only the
confirmation time in response to your click; it does not fabricate a capture time
or approve any attestation.

Alternatively, choose **Use an existing authoritative reference index**.
Its page paths are resolved relative to the original index. Samples remain
rejected. The operator must explicitly reconfirm the attestations.

### Review, then run

**Generate setup for review** validates the inputs with the existing helpers
and creates a new private directory under
`.finops-runs\verification-setup\<setup-id>`. It snapshots:

- The approved plan and actual capture, unchanged.
- The raw Portal response bytes, without numeric parsing/reserialization.
- A portable `portal-reference.json` using run-local page paths.
- `portal-validation.json` with schema version 1, `isExample: false`, relative
  paths, the approved hash, and the chosen age limit. No `liveApproval` is added.
- `setup.json` recording the selected mode and runner options.

Input files are never overwritten. Invalid or incomplete inputs produce explicit
errors, not an accepted setup. JSON previews are review-only. Changing the form
requires generating a new setup.
Preparation records the same source fingerprint as the campaign runner and
Portal validator. A source change after review blocks starting that setup;
generate and review a new one. A restarted server persists an interrupted state
instead of leaving an untracked run marked running.

**Run verification suite** invokes the existing runner using the current Python
executable and an argument array, never a shell or worker-only flags:

```powershell
python -B '.github\skills\finops-cost-evidence\tests\run_tests.py' --repeat 5 --seed 1729 --portal-config '<setup-directory>\portal-validation.json' --portal-mode evidence --out-dir '<setup-directory>\reports'
```

The actual command also retains the selected offline clock and sweep timeout.
Only one campaign can be active per server. A setup can be invoked once;
generate a new one for another campaign. All negatives precede positives,
and offline failures block the Portal acceptance stage. Freshness is checked
again at execution, so evidence can expire while offline sweeps run.

## Inspect and reopen outcomes

The page polls saved reports while a campaign runs. Sweep counts become
available after each sweep; they are not simulated progress. Results include:

- Exact saved verdict, runner exit code, and log tail.
- Attempt/pass/non-pass counts, sweep order, and negative-phase completion.
- Source stability, Portal status, acceptance status, and a separate
  **fresh live verification NOT RUN** indicator.
- Every test's attempts, warnings, diagnostics, and captured output.
- Original-currency raw/display comparisons and exact row differences, when
  the Portal stage produced them.
- Downloadable configs, evidence snapshots, JSON/Markdown reports, and logs.

Use the saved-run selector to reopen an outcome, including after server restart.
An interrupted/untracked process or missing completed report is never presented
as a completed passing run. **Refresh** retries status retrieval after an error.
Runner errors, mismatches, blocked evidence, skips, and incomplete execution
remain visible; nothing is retried to green.

`CAPTURED_PORTAL_PARITY_PASS` means equality against supplied operator-attested
evidence. It does not claim a fresh Azure login/query, browser-origin
authentication, invoice finality, or future data parity.

No live-mode control is offered. If a separate, approved live verification is
needed, use the existing CLI and its identity/scope/exact-plan confirmation
workflow; opening this page grants no such approval.

Stop with **Ctrl+C**. Normal shutdown waits for any active campaign to finish
rather than silently discarding outcomes. Preserve private outputs locally and
do not commit evidence, costs, identities, or populated configs.
