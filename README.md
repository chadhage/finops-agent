# FinOpsAgent

A workspace-scoped, read-only VS Code custom agent for Azure workload cost
analysis using the confirmed invoker's identity.

**[Explore the FinOpsAgent microsite](https://chadhage.github.io/finops-agent/)**:
why this repository exists, why Zava should care, how the code works, and who
should use it.

## Getting started

### 1. Prepare your environment

Install VS Code with GitHub Copilot agent support, Python 3.11+, and Azure CLI.
You need resource-read and Cost Management-read access to the subscriptions you
intend to assess; do not request Owner just to run an analysis.

Open a PowerShell terminal in this project folder and check your tools:

```powershell
python --version
az version
```

No Python packages, Azure MCP server, or Azure deployment are required for the
core local workflow. See [local prerequisites](#local-prerequisites) for optional
ownership sources and PDF support.

### 2. Sign in as the intended invoker

Replace `<tenant-id>` with the approved Azure tenant UUID, then sign in using
your own interactive account:

```powershell
az login --tenant '<tenant-id>'
```

Do not use a shared developer login or service principal. Signing in does not
authorize the agent to inspect every visible subscription: you must explicitly
approve the tenant, invoker identity, and subscription IDs for the assessment.

### 3. Select FinOpsAgent and make your first request

Open this folder in VS Code and select **FinOpsAgent** in the Chat agent picker.
If it is missing, reload the VS Code window or start a new chat.

Adapt this example with your approved IDs, reporting period, and workload
filters before sending it:

> For tenant `<tenant-id>` and subscription `<subscription-id>`, analyze
> September 2026 ActualCost for resources tagged Application=checkout in East US.
> Use complete UTC reporting days. First confirm my Azure identity and show
> the resolved resource scope for my approval before querying costs.
> Produce a Markdown report with exact amounts separated by billing currency.
> Mark results UNVERIFIED unless independent resource and cost references match.

The agent will clarify missing inputs. For a first run, leave out owner filters
unless you have the authoritative identity and ownership evidence described in
the [scope-resolution skill](.github/skills/finops-scope-resolution/SKILL.md).

### 4. Approve the scope and review the evidence

Check the tenant, invoker object ID, exact subscription/resource IDs, reporting
dates, and ActualCost/AmortizedCost basis before approving cost collection.
Review coverage warnings and validation status; an empty or inaccessible result
is not proof of zero spend.

Save evidence and reports in a new local per-run folder; do not commit them.
Markdown is the default. Request standalone HTML or PDF when needed; PDF
requires an explicitly selected installed Chromium-compatible browser.
No Azure resource or agent service is deployed by this pack.

**Next steps:** [CLI quick start](#cli-quick-start) for direct helper commands,
[validation](#validation) for offline negative-first tests, and the
[accuracy contract](#accuracy-contract) for exact-match acceptance requirements.

For an offline visual preview, open the
[workload experience mockup](wiki/mockups/Zava_FinOps_Workload_Experience.html).
Its data is fictional and it does not connect to Azure.

## Reusable skills

| Skill | Responsibility |
|---|---|
| [Invoker access](.github/skills/finops-invoker-access/SKILL.md) | Confirm interactive user, tenant, approved subscriptions, and source permissions. |
| [Scope resolution](.github/skills/finops-scope-resolution/SKILL.md) | Exact subscription/MG/resource-group/user-email/tag/region filtering and ownership provenance. |
| [Cost evidence and analysis](.github/skills/finops-cost-evidence/SKILL.md) | Historical spend/bill-change investigation, bounded AKS/AI resource costs, exact queries and zero-tolerance reconciliation. |
| [Reporting](.github/skills/finops-reporting/SKILL.md) | Markdown by default; the same evidence as a standalone HTML webpage or PDF. |
| [Azure Cost Management documentation](.github/skills/azure-cost-management/SKILL.md) | On-demand Microsoft Learn guidance for APIs, access/errors, data limits, and configuration concepts; no live billing adapter or writes. |

Copy all five skill directories together to reuse the full pack without the
agent. The executable implementation lives only in `finops-cost-evidence`;
the other evidence skills declare that dependency rather than duplicating
helpers. Documentation-only use needs network access but no Azure login.
Nothing depends on a particular model or a paid Python package.

For the verification setup page and its tests, also include
[`tools/verification_setup`](tools/verification_setup/). Cost collection itself
does not depend on the web utility.

See [skill references and usage](wiki/references.md) for documentation-only
prompts, tool fallback, source attribution, and the read-only integration boundary.

### Incorporated analyst guidance

Useful guidance from the [cost-analysis guide](wiki/tooling/cost-analysis-skill.md)
and [analyst capability register](wiki/tooling/finops-analyst-capabilities.md)
is ported into the existing cost-evidence skill and its
[capability boundaries](.github/skills/finops-cost-evidence/references/analyst-capabilities.md).
The agent now routes spend breakdowns, bill changes, and AKS/AI resource-cost
questions through that guidance. No separate overlapping skill or upstream
plugin installation is required; the wiki originals remain planning references.

Native analysis is limited to resource/day/billed-location evidence and exact
reported amounts, including side-by-side comparison periods. Cross-period
deltas/percentages, namespace/model/token allocation, forecasts, invoice linkage,
FX, budget reads, utilization-based rightsizing, and business allocation require
separately reviewed sources/calculation adapters. The capability register is not
a claim that those features are installed or qualified.

## Accuracy contract

The agent does not promise unqualified 100% LLM accuracy. It enforces
measurable acceptance gates:

1. Resolve exact, invoker-approved subscription/resource identities.
2. Match the complete current resource-ID set against an independent reference.
3. Capture every query page and reconcile detail/control amounts exactly by
   original billing currency, without floats or pre-aggregation rounding.
4. Match every resource/day/location/currency amount against a separately
   captured identical query plan with **zero tolerance**.

Missing independent references retain **UNVERIFIED**. Ambiguity, inaccessible
sources, incomplete pages, stale ownership, and mismatches block validation.
Even an exact match is only **VALIDATED AGAINST CAPTURED REFERENCES**: Azure
costs can lag or be rerated, and portal display rounding differs from raw data.
Cost Management is not automatically a final invoice or real-time utilization.

RBAC Owner is distinct from accountable business ownership. ServiceNow-backed
business ownership requires an approved read-only source and customer-defined
freshness rule; this pack does not configure that connector or infer it from RBAC.

## Local prerequisites

- Python 3.11+ and Azure CLI, authenticated interactively as the intended invoker.
- Resource and Cost Management read access at explicitly approved scopes.
  Directory/group and ServiceNow/invoice access are separate when needed.
- Public Azure (`AzureCloud`); one tenant/invoker per scenario.
- An explicitly selected installed Chromium-compatible executable (Edge, Chrome,
  or Chromium headless shell) only for PDF export.

There are no Python package dependencies. Do not grant Owner just for analysis.
Agent instructions are not an authorization boundary; Azure RBAC and local
execution controls must enforce least privilege.

## Example request

> Analyze September 2026 ActualCost for workload tag Application=checkout in
> East US, limited to my approved subscription IDs. Filter by these business
> owner emails using approved ServiceNow evidence. Show exact amounts per
> billing currency, reconcile against my manual query reference, and produce
> Markdown plus a standalone HTML page.

The agent asks for missing immutable IDs, identity confirmation, explicit
owner/filter semantics, dates/basis, and resolved-scope approval before querying.
Management-group filters never silently expand the approved subscription list.
Current-inventory filtering does not reconstruct historical ownership or tags.

## CLI quick start

Use the workspace's selected Python executable instead of `python` if needed.
Store evidence in an approved local location; do not commit it.
Replace every illustrative UUID/name/date in the
[scenario example](.github/skills/finops-cost-evidence/assets/scenario.example.json)
with confirmed inputs. Remove unused selectors rather than using empty arrays.

```powershell
$helper = '.github\skills\finops-cost-evidence\scripts\finops.py'
python $helper identity --tenant '<tenant-id>' --subscription '<subscription-id>' --out '.finops-runs\identity.json'
# Confirm the returned identity; create and approve scenario.json.
python $helper inventory --scenario '.finops-runs\scenario.json' --out '.finops-runs\catalog.json'
python $helper resolve --scenario '.finops-runs\scenario.json' --catalog '.finops-runs\catalog.json' --out '.finops-runs\manifest.json'
# Inspect and approve the resolved manifest before cost collection.
python $helper plan --manifest '.finops-runs\manifest.json' --out '.finops-runs\plan.json'
python $helper query --plan '.finops-runs\plan.json' --out '.finops-runs\actual.json'
python $helper report --actual '.finops-runs\actual.json' --out '.finops-runs\report.md'
```

This initial report is **UNVERIFIED**. Follow the scope/cost skills to supply
independent resource and cost references. With owner selectors, also supply
normalized authoritative evidence to `inventory --owners`; absent permissions
or incomplete owner evidence are blocking, not an empty match.

For HTML, add `--format html` and use an HTML output path. For PDF, add
`--format pdf --browser '<installed-browser-executable>'`. Pass the same
`--reference` to every report format. The webpage is a local self-contained
file, not an automatically published website.

Outputs are create-only: use a new per-run directory or distinct file names.
Final artifacts require a local filesystem supporting hard links (such as NTFS
or ext4) for complete, atomic create-only publication. Rebuild older exact-match
manifests/plans with their original independent resource reference before using
the strengthened provenance gate; review and approve the new plan hash.
The [evidence contract](.github/skills/finops-cost-evidence/references/evidence-contract.md)
defines supported schemas, reference import and reproducibility limits.

## Validation

### Local setup page

Generate verification JSON, review it, run the existing suite, and inspect
persisted outcomes in a local browser:

```powershell
python -B 'tools\verification_setup\server.py'
```

Open the printed loopback URL. The page supports full Portal-reference setup
from genuine exported files, reuse of an existing reference index, or offline
developer checks. It adds no packages or live Azure execution. Inputs are
snapshotted and all outputs stay under ignored `.finops-runs`.
See [setup-page usage and required inputs](wiki/verification-setup.md).

### Command-line validation

**Portal-to-query parity is required for acceptance.** Choose either supplied
authoritative evidence or a freshly authenticated read-only live query:

```powershell
$runner = '.github\skills\finops-cost-evidence\tests\run_tests.py'
# Compare Portal exports/display amounts with a saved agent query capture.
python -B $runner --repeat 10 --portal-config '.finops-runs\portal-acceptance\portal-validation.json' --portal-mode evidence
# Or, after explicit identity/scope/plan approval, issue fresh read-only queries.
python -B $runner --repeat 10 --portal-config '.finops-runs\portal-acceptance\portal-validation.json' --portal-mode live --confirm-live-plan '<exact-approved-plan-sha256>'
```

Follow the [Portal validation guide](.github/skills/finops-cost-evidence/references/portal-validation.md)
to populate the [config stub](.github/skills/finops-cost-evidence/assets/portal-validation.example.json)
and [Portal evidence sample](.github/skills/finops-cost-evidence/assets/portal-reference.example.json).
Samples are explicitly non-authoritative and cannot enable live access or pass
validation. A second CLI query is not Portal evidence.

Raw resource/day/region/currency amounts must match exactly, with zero tolerance.
Displayed Portal amounts must also match declared display precision after
aggregation. Evidence mode reports captured-reference parity only; live mode
additionally verifies the current invoker and performs a fresh query.
Without Portal inputs, normal acceptance is **BLOCKED**, not green.

For developer-only offline checks:

```powershell
python -B $runner --offline-only --repeat 10 --seed 1729
```

That mode explicitly reports **PORTAL PARITY NOT VALIDATED**.
The [core regression workflow](.github/workflows/verification.yml) runs ten
negative-first repetitions on Windows/Linux with Python 3.11 and the latest
stable Python, retains synthetic diagnostics, and runs real local CLI controls.
It is credential-free and does not qualify browser PDF, model conversations, or
live Azure parity. Remote CI must actually execute; adding the workflow is not
a passing run or branch-protection configuration.
Add `--coverage` to retain executable-line coverage and uncovered line numbers
for the Python helper, Portal validator, runner, and setup server; this is not
branch coverage or proof of model compliance.

The [test strategy](TEST-STRATEGY.md#how-to-run) also includes separate real
local-CLI/browser/PDF integration checks and restricted actual-model decision
probes for the agent and all five skills. Each layer has its own report and
limitations; mocked API calls, restricted model responses, and real customer
Portal parity are never treated as equivalent evidence.

The [purpose-built test strategy](TEST-STRATEGY.md) requires every negative
sweep to finish before any positive sweep. Each sweep and campaign writes
Markdown/JSON reports under a unique `.finops-runs\tests` directory. Failures
are retained, repeated pass/fail outcomes identify observed flakes, and
incomplete negative coverage blocks positive execution.

Synthetic tests cover exact scope/filtering, ambiguous identities, owner-source
separation/freshness, auth binding, read-only requests, pagination, malformed
inputs, missing data, decimal amounts, credits/currencies, raw reference
comparison, output failures, and reporting controls. They can expose existing
defects; a test strategy does not imply the current agent passes.

Real model conversations, directory/CMDB integrations, billing-offer coverage
beyond the selected live scenario, and installed-browser PDF behavior remain
separate acceptance layers. Reports distinguish captured Portal parity, fresh
live Portal parity, and NOT RUN checks; none is silently inferred from mocks.

Existing product/workflow context remains in [the wiki](wiki/); this pack does
not add enforcement, deployment, subscription vending, or policy rollout.

## Public microsite

The [microsite](site/index.html) is a self-contained explanation of the project,
not a live billing dashboard or the local verification utility. It contains
only public-safe, illustrative content. It does not collect credentials, query
Azure, or upload customer evidence.

Preview it locally:

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:8000/`. Validate the static publication boundary with:

```powershell
python tools\validate_microsite.py
```

The [Pages workflow](.github/workflows/pages.yml) validates and publishes only
the [site directory](site/) on relevant pushes to `main` or manual dispatch.
The wiki, local configuration, test-run evidence, and application code are not
included in the Pages artifact. This site check is not FinOps/live-cost acceptance.

## License and notices

This repository, including its original code, agents, skills, tests, and
documentation, is licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE), not MIT.
Retain attribution and identify modifications when sharing or adapting material.
Separately identified upstream material retains its applicable terms; see
[ThirdPartyNotices.txt](ThirdPartyNotices.txt).

See [NOTICE.md](NOTICE.md) for warranty, support, trademark, and non-endorsement
notices. The material is provided as-is and as-available under the license.
Microsoft product references and upstream documentation do not make this an
officially supported or Microsoft-endorsed product. No rights to Microsoft or
other third-party trademarks are granted.
