---
name: finops-reporting
description: "Produce evidence-backed Azure FinOps Markdown reports and optionally repack the same data as a standalone HTML webpage or PDF. Use for cost visualization, provenance, coverage warnings, currency-preserving output, and validation-status communication."
---

# Evidence-preserving FinOps reporting

Use the [shared helper](../finops-cost-evidence/scripts/finops.py) and
[evidence contract](../finops-cost-evidence/references/evidence-contract.md).
This skill depends on `finops-cost-evidence`; keep the dependency when reusing it.

## Procedure

1. Validate the complete captured bundle and exact internal controls. If a
   reference is supplied, require its plan and every monetary row to match.
   Do not turn a mismatch into a successful-looking report.
2. Default to Markdown:

   ```powershell
   $helper = '.github\skills\finops-cost-evidence\scripts\finops.py'
   python $helper report --actual '.finops-runs\actual.json' --out '.finops-runs\report.md'
   ```

   Add `--reference '.finops-runs\manual-reference.json'` when available.
   Missing cost/resource references retain `UNVERIFIED`; neither absence nor
   a valid hash counts as exact comparison.
3. Optionally repackage the SAME capture/reference without any new Azure queries:

   ```powershell
   python $helper report --actual '.finops-runs\actual.json' --format html --out '.finops-runs\report.html'
   python $helper report --actual '.finops-runs\actual.json' --format pdf --browser 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' --out '.finops-runs\report.pdf'
   ```

   Supply the same `--reference` to every format if it was used for Markdown.
   PDF requires an explicitly selected installed Chromium-compatible executable:
   Edge, Chrome, or an existing Chromium headless-shell runtime.
   No automatic installation, silent HTML fallback, external upload, hosting,
   public deployment, or browser sandbox disabling.

## Output contract

Include:

- Status first: blocked, unverified, or validated against captured references.
- Confirmed tenant/invoker and approved, included, and excluded subscription IDs.
- Explicit inclusive UTC period, ActualCost/AmortizedCost basis, PreTaxCost
  measure, original currencies, current inventory time, and capture interval.
- Exact totals per billing currency, with no implicit FX or sum of rounded rows.
  An additional USD-only display rounds the aggregate half-up to two decimals;
  it does not replace full-precision values or guess other currency precision.
- Complete selected-current-resource IDs, owner-source/freshness provenance,
  and resource/day/billed-region/currency monetary rows.
- Resource-set reference status AND independent cost-reference status.
- Empty results, non-resource charges, deleted/historical resources,
  current-tag/owner versus historical-billing semantics, and inaccessible sources.
- Scenario/catalog/plan/capture/reference fingerprints and links to the retained
  local artifacts. A fingerprint detects changes; it is not proof of source truth.
- Measured findings separately from hypotheses and optional advisory remedies.
  For owner handoff, preserve the existing ServiceNow/self-service workflow.
- For each factual finding, identify its supporting capture/rows or helper-emitted
  totals, scope, period, basis, and currency. Apply the
  [analyst capability boundaries](../finops-cost-evidence/references/analyst-capabilities.md)
  to comparisons and AKS/AI allocation; do not manufacture derived metrics or
  promote a spike, recommendation, or hypothesis into a measured cause/saving.

The HTML page is self-contained, escapes source text, has no external assets
or JavaScript, and includes top-ten resource/day magnitude charts per currency,
the complete evidence table, and the full report/provenance. Charts do not
discard rows from the report or imply a cross-currency total.
Negative credits remain negative; chart magnitude is explicitly labeled.

PDF prints that same self-contained HTML in an isolated temporary browser
profile. The helper verifies an actual PDF was produced and cleans temporary
files. A missing browser or failed print is an explicit error. A browser's
zero exit code without a valid PDF is still a failure; select a different
installed compatible runtime explicitly rather than claiming success.

## Accuracy language

Do not claim Portal amounts were validated from a second CLI capture or
synthetic tests. Link the cost skill's required Portal validation report and
state whether it compared supplied captures or performed a freshly authenticated
live query. Missing/blocked Portal evidence is not a successful acceptance run.

Unrounded API costs can differ visually from rounded portal display. Compare
raw evidence under identical parameters; apply display rounding only AFTER
aggregation and label it separately if requested. Do not claim invoice
finality, real-time resource utilization, complete historical workload
allocation, or future data parity.

Do not rewrite monetary facts in prose. Reuse emitted exact values.
Absent/denied/partial data is not zero or "clean"; unsupported claims require
abstention, not a model-generated estimate.
