"use strict";

const $ = (id) => document.getElementById(id);
let token = "";
let plan = null;
let preparedId = null;
let selectedId = null;
let currentRun = null;
let pollTimer = null;
let busy = false;

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function showError(error) {
  $("error").textContent = error.message || String(error);
  $("error").hidden = false;
}

function clearError() {
  $("error").hidden = true;
  $("error").textContent = "";
}

async function request(path, payload) {
  const options = payload === undefined ? {} : {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Setup-Token": token },
    body: JSON.stringify(payload),
  };
  const response = await fetch(path, options);
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || `Local server returned HTTP ${response.status}.`);
  return body;
}

function setStep(step) {
  for (const name of ["setup", "review", "results"]) {
    $(`step-${name}`).classList.toggle("current", name === step);
  }
}

function invalidateReview() {
  preparedId = null;
  $("run").disabled = true;
  if (!$("review-content").hidden) $("review-id").textContent = "Inputs changed. Generate a new setup before running.";
}

function syncMode() {
  const evidence = $("mode").value === "evidence";
  $("evidence-fields").disabled = !evidence;
  $("evidence-fields").hidden = !evidence;
  $("mode-help").textContent = evidence
    ? "Compare genuine Portal exports with a saved invoker-bound query after all offline checks pass."
    : "Run the complete synthetic negative-first suite without customer inputs. A passing result is not Portal acceptance.";
  const create = $("reference-mode").value === "create";
  $("new-reference").hidden = !create;
  $("new-reference").disabled = !create;
  $("existing-reference").hidden = create;
  $("existing-reference").disabled = create;
}

function labeledInput(parent, label, options = {}) {
  const wrapper = element("div");
  const input = element("input");
  input.id = `field-${crypto.randomUUID()}`;
  input.type = options.type || "text";
  input.required = true;
  for (const [key, value] of Object.entries(options)) input[key] = value;
  const caption = element("label", label);
  caption.htmlFor = input.id;
  wrapper.append(caption, input);
  parent.append(wrapper);
  return input;
}

function addCurrency() {
  const row = element("div", undefined, "currency-row");
  labeledInput(row, "Currency", { placeholder: "USD", className: "currency-code", pattern: "[A-Z]{3}", maxLength: 3 });
  labeledInput(row, "Full amount (text)", { placeholder: "1234.56", className: "currency-amount", inputMode: "decimal" });
  labeledInput(row, "Decimals", { type: "number", min: "0", max: "8", step: "1", className: "currency-places" });
  const remove = element("button", "X", "remove-button");
  remove.type = "button";
  remove.setAttribute("aria-label", "Remove currency");
  remove.addEventListener("click", () => { row.remove(); invalidateReview(); });
  row.append(remove);
  $("currencies").append(row);
}

function addPage(container, requestInfo) {
  const row = element("div", undefined, "page-entry");
  labeledInput(row, "Raw Portal response JSON path", {
    className: "page-path", placeholder: ".finops-runs\\my-evidence\\portal-page.json",
  });
  labeledInput(row, "Exact response URL (including continuation when present)", {
    className: "page-url", placeholder: requestInfo.url, type: "url",
  });
  const last = element("div", undefined, "page-last-row");
  const selectWrapper = element("div");
  const label = element("label", "HTTP status");
  const select = element("select");
  select.id = `status-${crypto.randomUUID()}`;
  select.className = "page-status";
  label.htmlFor = select.id;
  for (const code of ["200", "204"]) {
    const option = element("option", code);
    option.value = code;
    select.append(option);
  }
  selectWrapper.append(label, select);
  const remove = element("button", "Remove page", "remove-button");
  remove.type = "button";
  remove.addEventListener("click", () => { row.remove(); invalidateReview(); });
  last.append(selectWrapper, remove);
  row.append(last);
  container.append(row);
}

function renderPlan(loaded) {
  $("plan-summary").replaceChildren();
  const heading = element("strong", "Plan loaded - review immutable scope");
  const list = element("dl");
  const fields = {
    "SHA-256": loaded.sha256,
    "Tenant / invoker": `${loaded.tenantId} / ${loaded.principalId}`,
    "Approved subscriptions": loaded.subscriptionIds.join(", "),
    "Reporting period": `${loaded.period.from} through ${loaded.period.to}`,
    "Cost basis / selection": `${loaded.costBasis} / ${loaded.scopeMode}`,
    "Current resources / resource reference": `${loaded.resourceCount} / ${loaded.scopeReference}`,
    "Generated requests": loaded.requests.length,
  };
  for (const [name, value] of Object.entries(fields)) list.append(element("dt", name), element("dd", String(value)));
  $("plan-summary").append(heading, list);
  $("plan-summary").hidden = false;
  $("requests").replaceChildren();
  for (const info of loaded.requests) {
    const card = element("section", undefined, "request-card");
    card.dataset.requestId = info.id;
    card.append(element("div", `${info.kind.toUpperCase()} / ${info.id}`, "request-title"));
    const expected = element("details");
    expected.append(element("summary", "Expected request body (reference only)"), element("pre", info.expectedBody));
    card.append(expected);
    labeledInput(card, "Actual sanitized Portal request-body JSON path", {
      className: "request-body-path", placeholder: ".finops-runs\\my-evidence\\portal-request-body.json",
    });
    const pages = element("div", undefined, "response-pages");
    addPage(pages, info);
    const add = element("button", "+ Add continuation page", "text-button");
    add.type = "button";
    add.addEventListener("click", () => { addPage(pages, info); invalidateReview(); });
    card.append(pages, add);
    $("requests").append(card);
  }
}

function integer(id) {
  const value = Number($(id).value);
  if (!$(id).value.trim() || !Number.isSafeInteger(value)) throw new Error(`${$(id).previousElementSibling?.textContent || id} must be a safe integer.`);
  return value;
}

function formPayload() {
  const payload = {
    mode: $("mode").value,
    runner: { repeat: integer("repeat"), seed: integer("seed"), clock: $("clock").value.trim(), sweepTimeout: integer("timeout") },
  };
  if (payload.mode === "offline") return payload;
  Object.assign(payload, {
    planPath: $("plan-path").value.trim(), actualPath: $("actual-path").value.trim(),
    approvedPlanSha256: $("approved-hash").value.trim(), maxEvidenceAgeSeconds: integer("max-age"),
    referenceMode: $("reference-mode").value, confirmedAt: $("confirmed-at").value.trim(),
    attestations: {
      exportedFromAzurePortal: $("attest-origin").checked,
      sameViewScopeAndFilters: $("attest-scope").checked,
      noSecretsIncluded: $("attest-secrets").checked,
      actualCaptureIsAuthentic: $("attest-actual").checked,
    },
  });
  if (payload.referenceMode === "existing") {
    payload.portalIndexPath = $("index-path").value.trim();
  } else {
    if (!plan) throw new Error("Load and review the approved plan before building the Portal index.");
    const displayedTotals = [...$("currencies").children].map((row) => {
      const precision = row.querySelector(".currency-places").value;
      if (!precision.trim()) throw new Error("Enter the actual display precision for each currency.");
      return {
        currency: row.querySelector(".currency-code").value.trim(),
        amount: row.querySelector(".currency-amount").value.trim(),
        decimalPlaces: Number(precision),
      };
    });
    const captures = [...$("requests").querySelectorAll(".request-card")].map((card) => ({
      requestId: card.dataset.requestId,
      requestBodyPath: card.querySelector(".request-body-path").value.trim(),
      pages: [...card.querySelectorAll(".page-entry")].map((page) => ({
        path: page.querySelector(".page-path").value.trim(),
        url: page.querySelector(".page-url").value.trim(),
        status: Number(page.querySelector(".page-status").value),
      })),
    }));
    payload.reference = { capturedAt: $("captured-at").value.trim(), portalViewUrl: $("portal-url").value.trim(), displayedTotals, captures };
  }
  return payload;
}

function renderReview(run) {
  $("review-content").hidden = false;
  $("review-empty").hidden = true;
  $("review-id").textContent = `Setup ${run.id} / ${run.mode}`;
  $("command").textContent = run.commandPreview;
  $("config-previews").replaceChildren();
  for (const [name, text] of Object.entries(run.previews)) {
    const details = element("details");
    details.open = name === "portal-validation.json";
    details.append(element("summary", name), element("pre", text));
    $("config-previews").append(details);
  }
  if (run.mode === "offline") $("config-previews").append(element("p", "Offline mode requires no Portal JSON and cannot validate acceptance.", "callout"));
  $("run").disabled = run.state !== "prepared";
}

function renderTests(report) {
  const container = $("test-results");
  const openIds = new Set([...container.querySelectorAll("details[open]")].map((node) => node.dataset.testId));
  container.replaceChildren();
  const attempts = new Map();
  for (const attempt of report.results || []) {
    if (!attempts.has(attempt.id)) attempts.set(attempt.id, []);
    attempts.get(attempt.id).push(attempt);
  }
  for (const [id, records] of attempts) {
    const nonPassing = records.some((item) => item.status !== "pass");
    if ($("result-filter").value === "failures" && !nonPassing) continue;
    const outcomes = {};
    for (const item of records) outcomes[item.status] = (outcomes[item.status] || 0) + 1;
    const details = element("details", undefined, `test-case${nonPassing ? " non-passing" : ""}`);
    details.dataset.testId = id;
    details.open = openIds.has(id);
    details.append(element("summary", `${id} / ${Object.entries(outcomes).map(([name, count]) => `${name}: ${count}`).join(", ")}`));
    for (const item of records) {
      details.append(element("p", `${item.phase} sweep ${item.iteration} / ${item.status} / ${item.seconds}s / seed ${item.seed}`));
      const output = [...(item.diagnostics || []), ...(item.warnings || []), item.stdout, item.stderr].filter(Boolean).join("\n");
      if (output) details.append(element("pre", output));
    }
    container.append(details);
  }
  if (!container.childElementCount) container.append(element("p", "No matching test outcomes recorded.", "help"));
}

function renderParity(report) {
  const section = $("parity-comparison");
  section.replaceChildren();
  const comparison = report.portalParity?.comparison;
  if (!comparison) return;
  section.append(element("h3", "Portal display and exact-currency comparison"));
  const wrap = element("div", undefined, "table-wrap");
  const table = element("table");
  const head = element("tr");
  for (const text of ["Currency", "Query exact", "Portal displayed", "Query display", "Match"]) head.append(element("th", text));
  table.append(head);
  for (const item of comparison.displayComparisons || []) {
    const row = element("tr");
    for (const value of [item.currency, item.queryExact, item.portalDisplayed, item.queryDisplay, item.match ? "Yes" : "No"]) {
      row.append(element("td", value === null ? "Missing" : String(value)));
    }
    table.append(row);
  }
  wrap.append(table);
  section.append(wrap, element("p", `Raw row comparison: ${comparison.rawRowComparison?.status || "not established"}. Tolerance: ${comparison.tolerance}.`, "help"));
  if (comparison.rawRowComparison?.differences?.length) {
    const details = element("details");
    details.append(element("summary", "Exact row differences"), element("pre", JSON.stringify(comparison.rawRowComparison.differences, null, 2)));
    section.append(details);
  }
}

function renderRun(run) {
  currentRun = run;
  const report = run.report;
  const status = $("run-status");
  const verdict = report?.verdict || (run.state === "prepared" ? "Prepared - tests have not run." : run.state);
  status.textContent = `${run.state.toUpperCase()} / ${verdict}${run.exitCode !== null ? ` / exit ${run.exitCode}` : ""}`;
  status.className = "status-box";
  if (run.state === "running") status.classList.add("running");
  else if (run.error || verdict.startsWith("FAIL")) status.classList.add("failed");
  else if (verdict.startsWith("BLOCKED")) status.classList.add("blocked");
  else if (report?.acceptanceValidated) status.classList.add("passed");
  $("runner-log").textContent = run.log || "No runner output yet.";
  $("artifacts").replaceChildren();
  for (const name of run.artifacts) {
    const link = element("a", name);
    link.href = `/api/runs/${run.id}/artifacts/${name.split("/").map(encodeURIComponent).join("/")}`;
    link.download = name.split("/").at(-1);
    $("artifacts").append(link);
  }
  $("outcomes").hidden = !report;
  const errors = [run.error, ...(report?.errors || []), report?.portalParity?.error].filter(Boolean);
  $("run-errors").textContent = errors.join("\n\n");
  $("run-errors").hidden = !errors.length;
  if (!report && errors.length) status.textContent += ` / ${errors.join(" ")}`;
  if (report) {
    const records = report.results || [];
    const passed = records.filter((item) => item.status === "pass").length;
    $("attempt-count").textContent = records.length;
    $("pass-count").textContent = passed;
    $("failure-count").textContent = records.length - passed;
    $("negative-state").textContent = report.negativeComplete ? "Yes" : "Not established";
    $("positive-state").textContent = report.positiveStatus || "Not started";
    $("source-state").textContent = report.sourceStable === true ? "Yes" : "No / not established";
    $("portal-state").textContent = report.portalParity?.status || "NOT RUN";
    $("acceptance-state").textContent = report.acceptanceValidated === true ? "Yes - captured references only" : "No";
    $("live-state").textContent = report.livePortalValidated === true ? "Unexpected live claim - inspect error" : "NOT RUN";
    $("sweeps").replaceChildren();
    for (const sweep of report.sweeps || []) {
      const row = element("tr");
      for (const value of [`${sweep.phase} / ${sweep.iteration}`, `${sweep.attempted} / ${sweep.planned}`, sweep.exitCode]) row.append(element("td", String(value)));
      $("sweeps").append(row);
    }
    renderTests(report);
    renderParity(report);
  }
}

async function loadHistory() {
  const runs = await request("/api/runs");
  $("history").replaceChildren(element("option", "Select a saved setup or run"));
  $("history").firstChild.value = "";
  for (const run of runs) {
    const option = element("option", `${run.createdAt} / ${run.mode} / ${run.verdict || run.state} / ${run.id.slice(0, 8)}`);
    option.value = run.id;
    $("history").append(option);
  }
  $("history").value = selectedId || "";
}

async function refreshSelected() {
  clearTimeout(pollTimer);
  if (!selectedId) return;
  const run = await request(`/api/runs/${selectedId}`);
  renderRun(run);
  if (run.state === "running") {
    $("run").disabled = true;
    pollTimer = setTimeout(() => refreshSelected().catch(showError), 1500);
  } else {
    await loadHistory();
  }
}

function setBusy(value) {
  busy = value;
  $("prepare").disabled = value;
  $("load-plan").disabled = value;
}

$("setup-form").addEventListener("input", invalidateReview);
$("mode").addEventListener("change", syncMode);
$("reference-mode").addEventListener("change", syncMode);
$("plan-path").addEventListener("input", () => {
  plan = null;
  $("plan-summary").hidden = true;
  $("requests").replaceChildren(element("p", "Load the changed plan to configure its requests.", "empty-note"));
});
$("add-currency").addEventListener("click", () => { addCurrency(); invalidateReview(); });
$("confirm-now").addEventListener("click", () => { $("confirmed-at").value = new Date().toISOString().replace(/\.\d{3}Z$/, "Z"); invalidateReview(); });
$("load-plan").addEventListener("click", async () => {
  if (busy) return;
  clearError();
  setBusy(true);
  try {
    plan = await request("/api/plan", { planPath: $("plan-path").value.trim() });
    renderPlan(plan);
    invalidateReview();
  } catch (error) { showError(error); }
  finally { setBusy(false); }
});
$("setup-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (busy) return;
  clearError();
  setBusy(true);
  $("prepare").textContent = "Validating and snapshotting inputs...";
  try {
    const run = await request("/api/prepare", formPayload());
    preparedId = run.id;
    selectedId = run.id;
    renderReview(run);
    renderRun(run);
    setStep("review");
    await loadHistory();
    $("review-title").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) { showError(error); }
  finally { setBusy(false); $("prepare").textContent = "Generate setup for review"; }
});
$("run").addEventListener("click", async () => {
  if (!preparedId) return;
  clearError();
  $("run").disabled = true;
  try {
    const run = await request(`/api/runs/${preparedId}/start`, {});
    selectedId = run.id;
    preparedId = null;
    renderRun(run);
    setStep("results");
    await refreshSelected();
  } catch (error) { showError(error); $("run").disabled = !preparedId; }
});
$("history").addEventListener("change", async () => {
  clearError();
  selectedId = $("history").value || null;
  preparedId = null;
  $("run").disabled = true;
  clearTimeout(pollTimer);
  if (!selectedId) return;
  try {
    const run = await request(`/api/runs/${selectedId}`);
    preparedId = run.state === "prepared" ? run.id : null;
    renderReview(run);
    renderRun(run);
    setStep(run.state === "prepared" ? "review" : "results");
    await refreshSelected();
  } catch (error) { showError(error); }
});
$("refresh").addEventListener("click", async () => {
  clearError();
  try { await loadHistory(); await refreshSelected(); }
  catch (error) { showError(error); }
});
$("result-filter").addEventListener("change", () => {
  if (currentRun?.report) renderTests(currentRun.report);
});

async function initialize() {
  const boot = await request("/api/bootstrap");
  token = boot.token;
  $("mode").value = boot.defaults.mode;
  for (const [id, key] of [["repeat", "repeat"], ["seed", "seed"], ["clock", "clock"], ["timeout", "sweepTimeout"], ["max-age", "maxEvidenceAgeSeconds"]]) {
    $(id).value = boot.defaults[key];
  }
  $("roots").textContent = `Approved evidence roots: ${boot.evidenceRoots.join("; ")}. Additional roots must be explicitly supplied when starting the server.`;
  $("output-root").textContent = boot.outputRoot;
  $("connection").textContent = "Connected to the loopback server. Evidence is not uploaded; no credentials are collected.";
  addCurrency();
  syncMode();
  await loadHistory();
}

initialize().catch((error) => {
  $("connection").textContent = "Local setup server unavailable. Start the Python server and reload this page.";
  $("prepare").disabled = true;
  showError(error);
});
