"""Read-only, invoker-bound Azure FinOps evidence and deterministic reporting."""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal, localcontext
from pathlib import Path
from typing import Any


ARM = "https://management.azure.com"
API_VERSION = "2025-03-01"
OWNER_ROLE = "8e3af657-a8ff-443c-a75c-2fe8c4bcb635"
RESOURCE_QUERY = "Resources | project id, subscriptionId, location, tags | order by id asc"
CONTAINER_QUERY = (
    "ResourceContainers | project id, name, type, subscriptionId, properties | order by id asc"
)
Json = dict[str, Any]


class EvidenceError(Exception):
    """An explicit validation, authorization, collection, or reconciliation failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def timestamp(value: str) -> datetime:
    require(isinstance(value, str), "A UTC timestamp must be a string.")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise EvidenceError(f"Expected an explicit UTC timestamp, received {value!r}.") from exc
    require(parsed.strftime("%Y-%m-%dT%H:%M:%SZ") == value, "Use YYYY-MM-DDTHH:MM:SSZ.")
    return parsed


def guid(value: str) -> str:
    require(isinstance(value, str), "An identifier must be a UUID string.")
    try:
        normalized = str(uuid.UUID(value))
    except ValueError as exc:
        raise EvidenceError(f"Invalid UUID: {value!r}.") from exc
    require(normalized == value.lower(), "UUIDs must use the hyphenated representation.")
    return normalized


def arm_id(value: str) -> str:
    require(isinstance(value, str) and value.startswith("/"), "Expected a full ARM identifier.")
    require(not any(c in value for c in ("?", "#", "\\", "\r", "\n")), "Invalid ARM identifier.")
    normalized = value.rstrip("/").lower()
    require(bool(normalized) and "//" not in normalized and
            not any(part in (".", "..") for part in normalized.split("/")),
            "Invalid ARM identifier segments.")
    return normalized


def resource_id(value: str) -> str:
    identifier = arm_id(value)
    subscription_of(identifier)
    parts = identifier.split("/")[3:]
    if parts and parts[0] == "resourcegroups":
        require(len(parts) >= 2 and bool(parts[1]), "Incomplete resource group identifier.")
        parts = parts[2:]
    require(bool(parts), "Inventory requires a resource identifier, not a parent scope.")
    while parts:
        require(len(parts) >= 4 and parts[0] == "providers" and bool(parts[1]),
                "Incomplete provider resource identifier.")
        parts = parts[2:]
        pairs = 0
        while parts and parts[0] != "providers":
            require(len(parts) >= 2 and bool(parts[0]) and bool(parts[1]),
                    "Incomplete resource type/name pair.")
            parts = parts[2:]
            pairs += 1
        require(pairs > 0, "A provider must contain a resource type/name pair.")
    return identifier


def subscription_of(value: str) -> str:
    match = re.match(r"^/subscriptions/([^/]+)(?:/|$)", arm_id(value))
    require(match is not None, f"Not a subscription-bound ARM identifier: {value}.")
    return guid(match.group(1))


def unique(values: list[str], label: str) -> list[str]:
    require(len(values) == len(set(values)), f"Duplicate {label}.")
    return sorted(values)


def nonempty_strings(value: Any, label: str) -> list[str]:
    require(isinstance(value, list) and bool(value), f"{label} must be a nonempty array.")
    require(all(isinstance(v, str) and bool(v.strip()) for v in value), f"Invalid {label}.")
    return value


def _object(pairs: list[tuple[str, Any]]) -> Json:
    result: Json = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}.")
        result[key] = value
    return result


def parse_json(raw: str) -> Json:
    def invalid(value: str) -> None:
        raise EvidenceError(f"Non-finite JSON number: {value}.")

    try:
        result = json.loads(
            raw.lstrip("\ufeff"), parse_float=Decimal, parse_constant=invalid,
            object_pairs_hook=_object,
        )
    except json.JSONDecodeError as exc:
        raise EvidenceError(f"Invalid JSON at line {exc.lineno}, column {exc.colno}.") from exc
    require(isinstance(result, dict), "Expected a JSON object.")
    return result


def read_json(path: Path) -> Json:
    return parse_json(path.read_text(encoding="utf-8-sig"))


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def raw_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sealed(value: Json) -> Json:
    return {**value, "sha256": digest(value)}


def verify_seal(value: Json) -> None:
    require(value.get("sha256") == digest({k: v for k, v in value.items() if k != "sha256"}),
            "Evidence hash mismatch.")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def write_json(path: Path, value: Json) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False) + "\n")


def exact_sum(values: list[Decimal]) -> Decimal:
    if not values:
        return Decimal(0)
    require(all(v.is_finite() for v in values), "Non-finite cost.")
    # Precision spans every input place plus the possible carry from summation.
    precision = max(v.adjusted() for v in values) - min(v.as_tuple().exponent for v in values)
    with localcontext() as context:
        context.prec = max(28, precision + len(str(len(values))) + 3)
        return sum(values, Decimal(0))


def usd_display(amount: Decimal) -> str:
    with localcontext() as context:
        context.prec = max(28, len(amount.as_tuple().digits) + max(0, amount.adjusted()) + 4)
        return "$" + format(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")


def validate_scenario(scenario: Json) -> None:
    allowed = {"schemaVersion", "tenantId", "principalId", "approvedSubscriptionIds",
               "period", "costBasis", "selection"}
    require(not set(scenario) - allowed, "Unknown scenario fields; do not silently ignore filters.")
    require(type(scenario.get("schemaVersion")) is int and scenario["schemaVersion"] == 1,
            "Unsupported scenario schema.")
    guid(scenario["tenantId"])
    guid(scenario["principalId"])
    unique([guid(v) for v in nonempty_strings(scenario["approvedSubscriptionIds"], "subscriptions")],
           "approved subscription IDs")
    require(scenario["costBasis"] in ("ActualCost", "AmortizedCost"), "Choose one cost basis.")
    period = scenario["period"]
    require(isinstance(period, dict) and set(period) == {"from", "to"}, "Invalid period.")
    start, end = timestamp(period["from"]), timestamp(period["to"])
    require(start <= end, "The reporting period is reversed.")
    require(period["from"].endswith("T00:00:00Z") and period["to"].endswith("T23:59:59Z"),
            "Daily queries require explicitly approved complete UTC days, inclusive.")
    selection = scenario["selection"]
    require(isinstance(selection, dict), "selection must be an object.")
    allowed_filters = {"subscriptionIds", "subscriptionNames", "managementGroupIds",
                       "managementGroupNames", "resourceGroupIds", "resourceGroupNames",
                       "resourceIds", "owners", "tags", "regions"}
    require(not set(selection) - allowed_filters, "Unknown selection field; refusing a broader query.")
    for key, value in selection.items():
        if key not in ("owners", "tags"):
            nonempty_strings(value, key)
    if "owners" in selection:
        owners = selection["owners"]
        require(isinstance(owners, dict) and set(owners) == {"kind", "users"}, "Invalid owner filter.")
        require(owners["kind"] in ("rbac", "business", "either"), "Choose an explicit owner kind.")
        nonempty_strings(owners["users"], "owner users")
    if "tags" in selection:
        require(isinstance(selection["tags"], list) and bool(selection["tags"]), "Invalid tag filter.")
        keys = []
        for tag in selection["tags"]:
            require(isinstance(tag, dict) and set(tag) == {"key", "values"}, "Invalid tag selector.")
            require(isinstance(tag["key"], str) and bool(tag["key"]), "Invalid tag key.")
            nonempty_strings(tag["values"], "tag values")
            keys.append(tag["key"].casefold())
        unique(keys, "tag keys")


def resolve_names(values: list[str], records: list[Json], fields: tuple[str, ...], label: str) -> set[str]:
    resolved = set()
    for value in values:
        matches = {r["id"] for r in records
                   if any(isinstance(r.get(f), str) and r[f].casefold() == value.casefold()
                          for f in fields)}
        require(len(matches) == 1,
                f"{label} {value!r} resolved to {len(matches)} IDs; supply a unique immutable ID.")
        resolved.update(matches)
    return resolved


def scope_contains(scope: str, resource: str, ancestors: list[Json]) -> bool:
    scope, resource = arm_id(scope), arm_id(resource)
    if scope.startswith("/providers/microsoft.management/managementgroups/"):
        return scope in {arm_id(m["id"]) for m in ancestors}
    return resource == scope or resource.startswith(scope + "/")


def resolve_scope(scenario: Json, catalog: Json, reference: Json | None = None) -> Json:
    validate_scenario(scenario)
    tenant, principal = guid(scenario["tenantId"]), guid(scenario["principalId"])
    approved = {guid(v) for v in scenario["approvedSubscriptionIds"]}
    require(type(catalog.get("schemaVersion")) is int and catalog["schemaVersion"] == 1,
            "Unsupported catalog schema.")
    require(guid(catalog["tenantId"]) == tenant and guid(catalog["principalId"]) == principal,
            "Catalog identity does not match the confirmed invoker and tenant.")
    observed = timestamp(catalog["collectedAt"])
    require(observed <= timestamp(utc_now()), "Catalog collection time is in the future.")
    coverage, selectors = catalog["coverage"], scenario["selection"]
    require(isinstance(coverage, dict), "Catalog coverage must be an object.")
    for source in ("subscriptions", "resources", "resourceGroups"):
        require(coverage.get(source) is True, f"Incomplete or unavailable {source} evidence.")
    subscriptions = [{**s, "id": guid(s["id"])} for s in catalog["subscriptions"]]
    unique([s["id"] for s in subscriptions], "catalog subscription IDs")
    require({s["id"] for s in subscriptions} == approved,
            "Catalog subscriptions must match exactly the approved subscription boundary.")
    submap = {s["id"]: s for s in subscriptions}
    selected = set(approved)
    if "subscriptionIds" in selectors or "subscriptionNames" in selectors:
        requested = {guid(v) for v in selectors.get("subscriptionIds", [])}
        requested |= resolve_names(selectors.get("subscriptionNames", []), subscriptions,
                                   ("name",), "Subscription name")
        require(requested <= approved, "A subscription filter escaped the approved boundary.")
        selected &= requested
    if "managementGroupIds" in selectors or "managementGroupNames" in selectors:
        require(coverage.get("managementGroups") is True, "Management group ancestry is incomplete.")
        groups: dict[str, Json] = {}
        for sub in subscriptions:
            for group in sub["managementGroups"]:
                identifier = arm_id(group["id"])
                require(identifier.startswith("/providers/microsoft.management/managementgroups/"),
                        "Invalid management group identifier.")
                require(identifier not in groups or groups[identifier]["name"] == group["name"],
                        "Conflicting management group metadata.")
                groups[identifier] = {**group, "id": identifier}
        requested = {arm_id(v) for v in selectors.get("managementGroupIds", [])}
        requested |= resolve_names(selectors.get("managementGroupNames", []), list(groups.values()),
                                   ("name",), "Management group name")
        require(requested <= set(groups), "A management group has no verified approved descendants.")
        selected &= {s["id"] for s in subscriptions
                     if requested & {arm_id(m["id"]) for m in s["managementGroups"]}}
    require(bool(selected), "No approved subscriptions matched; no cost query will be produced.")
    resources = []
    seen = set()
    for resource in catalog["resources"]:
        identifier = resource_id(resource["id"])
        sid = subscription_of(identifier)
        require(sid in approved, "Resource inventory escaped the approved subscription boundary.")
        require("subscriptionId" not in resource or guid(resource["subscriptionId"]) == sid,
                "Inventory resource ID and subscription metadata disagree.")
        require(identifier not in seen, "Duplicate resource IDs; inventory may have changed during paging.")
        seen.add(identifier)
        require(isinstance(resource.get("location"), str) and isinstance(resource.get("tags"), dict),
                "Inventory resource location/tags are missing.")
        tags = resource["tags"]
        require(all(isinstance(k, str) and isinstance(v, str) for k, v in tags.items()), "Invalid tags.")
        unique([k.casefold() for k in tags], "case-insensitive resource tag keys")
        if sid in selected:
            resources.append({**resource, "id": identifier, "subscriptionId": sid})
    group_ids = None
    if "resourceGroupIds" in selectors or "resourceGroupNames" in selectors:
        require(all(subscription_of(g["id"]) in approved for g in catalog["resourceGroups"]),
                "Resource group inventory escaped the approved subscription boundary.")
        groups = [{**g, "id": arm_id(g["id"])} for g in catalog["resourceGroups"]
                  if subscription_of(g["id"]) in selected]
        unique([g["id"] for g in groups], "resource group IDs")
        group_ids = {arm_id(v) for v in selectors.get("resourceGroupIds", [])}
        group_ids |= resolve_names(selectors.get("resourceGroupNames", []), groups,
                                   ("name",), "Resource group name")
        require(group_ids <= {g["id"] for g in groups}, "An unverified resource group was requested.")
    region_ids = None
    if "regions" in selectors:
        require(coverage.get("locations") is True, "Location alias evidence is incomplete.")
        locations = [{**r, "id": r["name"].casefold()} for r in catalog["locations"]]
        region_ids = resolve_names(selectors["regions"], locations, ("name", "displayName"), "Region")
    owner_scopes: list[Json] | None = None
    if "owners" in selectors:
        owner_filter = selectors["owners"]
        kinds = ("rbac", "business") if owner_filter["kind"] == "either" else (owner_filter["kind"],)
        require(coverage.get("users") is True, "Directory identity evidence is incomplete.")
        for kind in kinds:
            require(coverage.get(kind + "Owners") is True, f"Incomplete {kind} ownership evidence.")
        users = [{**u, "id": guid(u["id"])} for u in catalog["users"]]
        unique([u["id"] for u in users], "directory object IDs")
        user_ids = resolve_names(owner_filter["users"], users,
                                 ("id", "displayName", "mail", "userPrincipalName"), "User")
        owner_scopes = []
        for binding in catalog["ownerBindings"]:
            if guid(binding["userId"]) not in user_ids or binding["kind"] not in kinds:
                continue
            require(binding.get("effective") in (True, False) and
                    isinstance(binding.get("effective"), bool), "Ownership effectiveness is unresolved.")
            require(isinstance(binding.get("source"), str) and bool(binding["source"].strip()),
                    "An owner binding has no authoritative source.")
            require(timestamp(binding["validatedAt"]) <= observed, "Owner evidence is from the future.")
            if binding["kind"] == "business":
                require(isinstance(binding.get("freshnessRule"), str) and bool(binding["freshnessRule"].strip()),
                        "A customer-approved freshness rule is required.")
                require(observed <= timestamp(binding["freshUntil"]), "Business ownership evidence is stale.")
            else:
                require(guid(binding["roleDefinitionId"].split("/")[-1]) == OWNER_ROLE,
                        "RBAC ownership requires the built-in Owner role, not Contributor or a guessed role.")
                require(binding.get("exclusionsChecked") is True, "RBAC conditions/denies are unresolved.")
            if binding["effective"]:
                if arm_id(binding["scopeId"]).startswith("/providers/microsoft.management/managementgroups/"):
                    require(coverage.get("managementGroups") is True,
                            "Inherited management group ownership requires complete ancestry.")
                owner_scopes.append({**binding, "scopeId": arm_id(binding["scopeId"])})
        require(bool(owner_scopes), "No verified effective owner bindings matched.")
    requested_resources = None
    if "resourceIds" in selectors:
        requested_resources = {arm_id(v) for v in selectors["resourceIds"]}
        require(requested_resources <= {r["id"] for r in resources},
                "Requested resources are outside the selected boundary or absent from current inventory.")
    matched = []
    for resource in resources:
        identifier = resource["id"]
        ancestors = submap[resource["subscriptionId"]].get("managementGroups", [])
        if group_ids is not None and not any(scope_contains(g, identifier, []) for g in group_ids):
            continue
        if region_ids is not None and resource["location"].casefold() not in region_ids:
            continue
        if requested_resources is not None and identifier not in requested_resources:
            continue
        tags = {k.casefold(): v for k, v in resource["tags"].items()}
        if not all(tags.get(t["key"].casefold()) in t["values"] for t in selectors.get("tags", [])):
            continue
        if owner_scopes is not None and not any(
                scope_contains(b["scopeId"], identifier, ancestors) for b in owner_scopes):
            continue
        matched.append(identifier)
    resource_filter = bool(set(selectors) & {
        "resourceGroupIds", "resourceGroupNames", "resourceIds", "regions", "tags", "owners"})
    require(not resource_filter or bool(matched), "No resources matched; refusing an unfiltered cost query.")
    resource_ids = sorted(matched)
    scope_reference: Json = {"status": "not-verified"}
    if reference is not None:
        require(reference["scenarioSha256"] == digest(scenario), "Resource reference scenario mismatch.")
        require(bool(reference.get("source")), "Resource reference source is required.")
        require(timestamp(reference["capturedAt"]) <= timestamp(utc_now()),
                "Resource reference capture time is in the future.")
        expected = unique([arm_id(v) for v in reference["resourceIds"]], "reference resource IDs")
        require(expected == resource_ids, "Resource reference mismatch: exact resource sets differ.")
        scope_reference = {"status": "exact-match", "sha256": digest(reference),
                           "source": reference["source"], "capturedAt": reference["capturedAt"]}
    return sealed({
        "schemaVersion": 1, "tenantId": tenant, "principalId": principal,
        "approvedSubscriptionIds": sorted(approved), "subscriptionIds": sorted(selected),
        "excludedSubscriptionIds": sorted(approved - selected), "resourceIds": resource_ids,
        "scopeMode": "current-resource-set" if resource_filter else "subscription-charges",
        "scopeReference": scope_reference, "inventoryAsOf": catalog["collectedAt"],
        "scenarioSha256": digest(scenario), "catalogSha256": digest(catalog),
        "scenario": scenario, "ownerEvidence": owner_scopes or [],
        "period": scenario["period"], "costBasis": scenario["costBasis"],
    })


def make_plan(manifest: Json) -> Json:
    verify_seal(manifest)
    require(type(manifest.get("schemaVersion")) is int and manifest["schemaVersion"] == 1,
            "Unsupported manifest schema.")
    validate_scenario(manifest["scenario"])
    scenario = manifest["scenario"]
    require(manifest["scenarioSha256"] == digest(scenario), "Manifest scenario hash mismatch.")
    require(manifest["tenantId"] == guid(scenario["tenantId"]) and
            manifest["principalId"] == guid(scenario["principalId"]), "Manifest identity mismatch.")
    require(manifest["period"] == scenario["period"] and manifest["costBasis"] == scenario["costBasis"],
            "Manifest reporting parameters differ from the approved scenario.")
    approved = {guid(v) for v in scenario["approvedSubscriptionIds"]}
    selected = unique([guid(v) for v in manifest["subscriptionIds"]], "selected subscriptions")
    require(bool(selected) and set(selected) <= approved, "Plan escaped the approved subscriptions.")
    require(manifest["approvedSubscriptionIds"] == sorted(approved) and
            manifest["excludedSubscriptionIds"] == sorted(approved - set(selected)),
            "Manifest included/excluded subscription metadata is inconsistent.")
    resources = unique([resource_id(v) for v in manifest["resourceIds"]], "selected resources")
    require(all(subscription_of(r) in selected for r in resources), "A resource escaped the selected scope.")
    mode = manifest["scopeMode"]
    require(mode in ("subscription-charges", "current-resource-set"), "Unsupported scope mode.")
    resource_filter = bool(set(scenario["selection"]) & {
        "resourceGroupIds", "resourceGroupNames", "resourceIds", "regions", "tags", "owners"})
    require((mode == "current-resource-set") == resource_filter,
            "A resource-filtered scenario cannot become a subscription-wide query.")
    require(mode != "current-resource-set" or bool(resources), "Empty resource filters are forbidden.")
    requests = []
    for sid in selected:
        ids = [r for r in resources if subscription_of(r) == sid]
        chunks = [ids[n:n + 100] for n in range(0, len(ids), 100)] if mode == "current-resource-set" else [None]
        for chunk in chunks:
            for kind in ("detail", "control"):
                dataset: Json = {"aggregation": {"totalCost": {"name": "PreTaxCost", "function": "Sum"}}}
                if kind == "detail":
                    dataset.update({"granularity": "Daily", "grouping": [
                        {"type": "Dimension", "name": "ResourceId"},
                        {"type": "Dimension", "name": "ResourceLocation"}]})
                if chunk is not None:
                    dataset["filter"] = {"dimensions": {"name": "ResourceId", "operator": "In", "values": chunk}}
                scope = f"/subscriptions/{sid}"
                body = {"type": manifest["costBasis"], "timeframe": "Custom",
                        "timePeriod": manifest["period"], "dataset": dataset}
                request = {"scope": scope, "kind": kind, "body": body}
                requests.append({**request, "id": digest(request),
                                 "url": f"{ARM}{scope}/providers/Microsoft.CostManagement/query?api-version={API_VERSION}"})
    require(bool(requests), "The query plan has no requests.")
    return sealed({"schemaVersion": 1, "manifest": manifest, "requests": requests})


def verify_plan(plan: Json) -> None:
    verify_seal(plan)
    require(type(plan.get("schemaVersion")) is int and plan["schemaVersion"] == 1, "Unsupported plan schema.")
    require(plan == make_plan(plan["manifest"]), "The plan contains non-generated or modified operations.")


def validate_next_url(url: str, initial: str) -> None:
    parsed, original = urllib.parse.urlsplit(url), urllib.parse.urlsplit(initial)
    require(parsed.scheme == "https" and parsed.netloc == "management.azure.com" and
            parsed.path.casefold() == original.path.casefold() and not parsed.fragment,
            "Continuation URL escaped its original Azure endpoint.")
    parameters = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    require(set(parameters) <= {"api-version", "$skiptoken", "$skipToken"} and
            len(parameters.get("api-version", [])) == 1, "Unexpected continuation parameters.")
    require(all(len(v) == 1 and bool(v[0]) for v in parameters.values()), "Invalid continuation parameter.")
    require(re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:-preview)?", parameters["api-version"][0]) is not None,
            "Invalid continuation API version.")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        raise EvidenceError("HTTP redirect refused; invoker tokens must not leave the original endpoint.")


def cli_json(arguments: list[str]) -> Json:
    executable = shutil.which("az")
    require(executable is not None, "Azure CLI is missing. Install it separately; no automatic installation.")
    result = subprocess.run([executable, *arguments, "--only-show-errors", "--output", "json"],
                            capture_output=True, text=True, encoding="utf-8", timeout=90, check=False)
    require(result.returncode == 0,
            "Azure CLI authentication/context command failed. Sign in as the intended invoker; "
            "no alternate identity or account switching was attempted.")
    return parse_json(result.stdout)


def azure_identity(tenant: str, subscription: str, principal: str | None = None) -> tuple[Json, str]:
    tenant, subscription = guid(tenant), guid(subscription)
    profile = cli_json(["account", "show", "--subscription", subscription])
    require(guid(profile["id"]) == subscription and guid(profile["tenantId"]) == tenant,
            "Azure CLI subscription/tenant differs from the confirmed selection.")
    require(profile.get("environmentName") == "AzureCloud", "This helper currently supports AzureCloud only.")
    require(profile.get("state") == "Enabled", "The selected subscription is not enabled.")
    user = profile.get("user")
    require(isinstance(user, dict) and isinstance(user.get("type"), str) and
            user["type"].casefold() == "user",
            "An interactive invoker identity is required; application/developer identity substitution is forbidden.")
    result = cli_json(["account", "get-access-token", "--subscription", subscription, "--resource", ARM + "/"])
    token = result["accessToken"]
    require(isinstance(token, str) and len(token.split(".")) == 3, "Azure CLI returned a non-JWT ARM token.")
    try:
        encoded = token.split(".")[1]
        claims = parse_json(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)).decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise EvidenceError("Cannot inspect the Azure CLI token identity.") from exc
    oid = guid(claims["oid"])
    require(guid(claims["tid"]) == tenant and (principal is None or oid == guid(principal)),
            "Token identity differs from the confirmed invoker.")
    require(claims.get("idtyp") != "app" and claims.get("exp", 0) > time.time() + 60,
            "The invoker token is application-only or expired.")
    require(claims.get("aud", "").rstrip("/") in (ARM, "https://management.core.windows.net"),
            "Unexpected ARM token audience.")
    return {"tenantId": tenant, "principalId": oid, "subscriptionId": subscription,
            "subscriptionName": profile["name"], "verifiedAt": utc_now(),
            "identityType": "interactive-user"}, token


class AzureClient:
    def __init__(self, tenant: str, principal: str, subscriptions: list[str]):
        self.tenant, self.principal = guid(tenant), guid(principal)
        self.subscriptions = [guid(s) for s in subscriptions]
        self.contexts: dict[str, Json] = {}
        self.tokens: dict[str, str] = {}
        self.opener = urllib.request.build_opener(NoRedirect())
        for sid in self.subscriptions:
            self.contexts[sid], self.tokens[sid] = azure_identity(self.tenant, sid, self.principal)

    def request(self, method: str, url: str, sid: str, body: Json | None = None) -> Json:
        require(sid in self.subscriptions, "A request escaped the approved subscriptions.")
        parsed = urllib.parse.urlsplit(url)
        require(parsed.scheme == "https" and parsed.netloc == "management.azure.com" and not parsed.fragment,
                "Only the public Azure ARM endpoint is supported.")
        if method == "POST":
            is_graph = parsed.path == "/providers/Microsoft.ResourceGraph/resources"
            is_cost = parsed.path.casefold() == f"/subscriptions/{sid}/providers/microsoft.costmanagement/query"
            require(is_graph or is_cost, "Non-query POST operation refused.")
            if is_graph:
                require(body is not None and body.get("subscriptions") == self.subscriptions and
                        body.get("query") in (RESOURCE_QUERY, CONTAINER_QUERY), "Non-allowlisted inventory query.")
        else:
            require(method == "GET" and parsed.path.casefold() == f"/subscriptions/{sid}/locations",
                    "Non-allowlisted read operation.")
        for attempt in range(2):
            request = urllib.request.Request(
                url, data=canonical(body).encode("utf-8") if body is not None else None, method=method,
                headers={"Authorization": "Bearer " + self.tokens[sid], "Content-Type": "application/json"},
            )
            try:
                with self.opener.open(request, timeout=120) as response:
                    raw = response.read().decode("utf-8-sig")
                    return {"url": url, "status": response.status, "raw": raw,
                            "sha256": raw_digest(raw), "retrievedAt": utc_now(),
                            "azureRequestId": response.headers.get("x-ms-request-id", "")}
            except urllib.error.HTTPError as exc:
                status, headers = exc.code, exc.headers
                exc.close()
                retry = headers.get("x-ms-ratelimit-microsoft.costmanagement-entity-retry-after",
                                    headers.get("Retry-After", "1"))
                if status in (429, 503) and attempt == 0 and retry.isdigit() and int(retry) <= 60:
                    time.sleep(int(retry))
                    continue
                raise EvidenceError(
                    f"Azure HTTP {status} at {parsed.path}; request ID "
                    f"{headers.get('x-ms-request-id', 'unavailable')}. "
                    "No partial result accepted; permissions, throttling, and no data are distinct."
                ) from exc
            except urllib.error.URLError as exc:
                raise EvidenceError(f"Azure transport failed at {parsed.path}: {exc.reason}.") from exc
        raise EvidenceError("Azure request did not complete.")


def collect_graph(client: AzureClient, query: str) -> tuple[list[Json], list[Json]]:
    data: list[Json] = []
    pages = []
    options: Json = {"$top": 1000, "resultFormat": "objectArray"}
    tokens = set()
    total = None
    while True:
        require(len(pages) < 10000, "Inventory page safety limit reached; collection is incomplete.")
        body = {"subscriptions": client.subscriptions, "query": query, "options": options}
        page = client.request("POST", ARM + "/providers/Microsoft.ResourceGraph/resources?api-version=2022-10-01",
                              client.subscriptions[0], body)
        require(page["status"] == 200, "Resource Graph returned no usable inventory.")
        result = parse_json(page["raw"])
        require(isinstance(result["data"], list) and type(result["count"]) is int and
                result["count"] == len(result["data"]),
                "Resource Graph row count/schema mismatch.")
        require(type(result["totalRecords"]) is int and result["totalRecords"] >= 0 and
                (type(result.get("resultTruncated")) is bool or
                 isinstance(result.get("resultTruncated"), str) and
                 result["resultTruncated"] in ("true", "false")),
                "Resource Graph completeness metadata is missing.")
        if total is None:
            total = result["totalRecords"]
        require(result["totalRecords"] == total, "Inventory changed during pagination; collect it again.")
        data.extend(result["data"])
        pages.append({**page, "requestBody": body})
        token = result.get("$skipToken")
        truncated = result.get("resultTruncated") in (True, "true")
        if not token:
            require(not truncated and len(data) == total, "Truncated or incomplete Resource Graph response.")
            break
        require(isinstance(token, str) and token not in tokens, "Repeated/invalid inventory continuation token.")
        tokens.add(token)
        options = {**options, "$skipToken": token}
    unique([arm_id(r["id"]) for r in data], "paged inventory IDs")
    return data, pages


def collect_inventory(scenario: Json, client: AzureClient, owners: Json | None = None) -> Json:
    validate_scenario(scenario)
    require(client.tenant == guid(scenario["tenantId"]) and client.principal == guid(scenario["principalId"]) and
            set(client.subscriptions) == {guid(s) for s in scenario["approvedSubscriptionIds"]},
            "Inventory client differs from the approved scenario.")
    resources, resource_pages = collect_graph(client, RESOURCE_QUERY)
    containers, container_pages = collect_graph(client, CONTAINER_QUERY)
    subscriptions, groups, locations, location_pages = [], [], {}, []
    for sid in client.subscriptions:
        matches = [r for r in containers if r["type"].casefold() == "microsoft.resources/subscriptions" and
                   guid(r["subscriptionId"]) == sid]
        require(len(matches) == 1, "An approved subscription is absent/ambiguous in inventory; access may be partial.")
        properties = matches[0].get("properties", {})
        ancestors = [{"id": "/providers/Microsoft.Management/managementGroups/" + g["name"],
                      "name": g["displayName"]} for g in properties.get("managementGroupAncestorsChain", [])]
        subscriptions.append({"id": sid, "name": client.contexts[sid]["subscriptionName"],
                              "managementGroups": ancestors,
                              "ancestryComplete": "managementGroupAncestorsChain" in properties})
        url = f"{ARM}/subscriptions/{sid}/locations?api-version=2022-12-01"
        initial, seen = url, set()
        while url:
            require(url not in seen and len(seen) < 10000, "Incomplete location pagination.")
            seen.add(url)
            parsed, original = urllib.parse.urlsplit(url), urllib.parse.urlsplit(initial)
            require(parsed.netloc == original.netloc and parsed.scheme == "https" and
                    parsed.path.casefold() == original.path.casefold(), "Location continuation escaped its scope.")
            page = client.request("GET", url, sid)
            require(page["status"] == 200, "Location metadata is unavailable.")
            result = parse_json(page["raw"])
            for location in result["value"]:
                locations[location["name"]] = {"name": location["name"], "displayName": location["displayName"]}
            location_pages.append(page)
            url = result.get("nextLink")
    for row in containers:
        require(guid(row["subscriptionId"]) in client.subscriptions, "Inventory escaped the selected scope.")
        if row["type"].casefold() == "microsoft.resources/subscriptions/resourcegroups":
            groups.append({"id": row["id"], "name": row["name"]})
    for row in resources:
        require(subscription_of(row["id"]) in client.subscriptions, "Inventory escaped the selected scope.")
        require("tags" in row and (row["tags"] is None or isinstance(row["tags"], dict)),
                "Inventory tags are missing or malformed.")
        if row["tags"] is None:
            row["tags"] = {}
        require(isinstance(row.get("location"), str), "Inventory resource location is missing.")
        if row["location"] and row["location"] not in locations:
            locations[row["location"]] = {"name": row["location"], "displayName": row["location"]}
    owner_coverage = {"users": False, "rbacOwners": False, "businessOwners": False}
    if owners is not None:
        require(guid(owners["tenantId"]) == client.tenant and guid(owners["principalId"]) == client.principal,
                "Ownership evidence belongs to another invoker/tenant.")
        require(set(owners["subscriptionIds"]) == set(client.subscriptions), "Ownership evidence scope mismatch.")
        require(timestamp(owners["collectedAt"]) <= timestamp(utc_now()), "Ownership evidence is from the future.")
        owner_coverage = {k: owners["coverage"].get(k) is True for k in owner_coverage}
    return {
        "schemaVersion": 1, "tenantId": client.tenant, "principalId": client.principal, "collectedAt": utc_now(),
        "coverage": {"subscriptions": True, "resources": True, "resourceGroups": True, "locations": True,
                     "managementGroups": all(s["ancestryComplete"] for s in subscriptions), **owner_coverage},
        "coverageBasis": "Invoker-visible current inventory; independent resource-set reference required.",
        "subscriptions": subscriptions, "resourceGroups": groups, "resources": resources,
        "locations": sorted(locations.values(), key=lambda r: r["name"]),
        "users": owners["users"] if owners is not None else [],
        "ownerBindings": owners["ownerBindings"] if owners is not None else [],
        "ownershipEvidenceSha256": digest(owners) if owners is not None else None,
        "sourcePages": resource_pages + container_pages + location_pages,
    }


def page_next(page: Json) -> str | None:
    require(page.get("sha256") == raw_digest(page["raw"]), "Raw response hash mismatch.")
    timestamp(page["retrievedAt"])
    if page["status"] == 204:
        require(not page["raw"].strip(), "A 204 response unexpectedly contains data.")
        return None
    require(page["status"] == 200, "Non-success cost response; no partial report is permitted.")
    result = parse_json(page["raw"])
    require(isinstance(result.get("properties"), dict) and "error" not in result, "Invalid Cost Management response.")
    following = result["properties"].get("nextLink")
    require(following is None or isinstance(following, str), "Invalid cost continuation.")
    return following or None


def execute_plan(plan: Json, client: AzureClient) -> Json:
    verify_plan(plan)
    manifest = plan["manifest"]
    require(client.tenant == manifest["tenantId"] and client.principal == manifest["principalId"] and
            set(client.subscriptions) == set(manifest["subscriptionIds"]), "Query client identity/scope mismatch.")
    captures = []
    for request in plan["requests"]:
        pages, seen = [], set()
        url = request["url"]
        while url:
            require(url not in seen and len(seen) < 10000, "Repeated continuation/page limit; result is incomplete.")
            validate_next_url(url, request["url"])
            seen.add(url)
            page = client.request("POST", url, subscription_of(request["scope"]), request["body"])
            pages.append(page)
            url = page_next(page)
        captures.append({"requestId": request["id"], "pages": pages})
    bundle = sealed({"schemaVersion": 1, "captureId": str(uuid.uuid4()), "source": "invoker-azure-cli-arm",
                     "capturedAt": utc_now(), "plan": plan, "captures": captures})
    validate_bundle(bundle)
    return bundle


def validate_bundle(bundle: Json) -> Json:
    verify_seal(bundle)
    require(type(bundle.get("schemaVersion")) is int and bundle["schemaVersion"] == 1,
            "Unsupported cost evidence schema.")
    guid(bundle["captureId"])
    captured_at = timestamp(bundle["capturedAt"])
    require(captured_at <= timestamp(utc_now()), "Cost capture time is in the future.")
    plan = bundle["plan"]
    verify_plan(plan)
    captures = bundle["captures"]
    unique([c["requestId"] for c in captures], "captured requests")
    require({c["requestId"] for c in captures} == {r["id"] for r in plan["requests"]},
            "A query response is missing or unexpected.")
    by_id = {c["requestId"]: c for c in captures}
    ledger: dict[tuple[str, str, str, str, str], Decimal] = {}
    controls: dict[str, dict[str, Decimal]] = {}
    details: dict[str, dict[str, Decimal]] = {}
    dates = []
    empty_requests = []
    for request in plan["requests"]:
        pages = by_id[request["id"]]["pages"]
        require(bool(pages), "A cost query has no captured response.")
        url, schema = request["url"], None
        sums: dict[str, list[Decimal]] = defaultdict(list)
        seen_urls: set[str] = set()
        control_currencies: set[str] = set()
        rows_seen = 0
        sid = subscription_of(request["scope"])
        chunk = request["body"]["dataset"].get("filter", {}).get("dimensions", {}).get("values")
        for page in pages:
            require(url is not None and page["url"] == url, "Missing, reordered, or unexpected cost page.")
            require(page["url"] not in seen_urls, "Repeated cost response URL; evidence may be replayed.")
            seen_urls.add(page["url"])
            validate_next_url(page["url"], request["url"])
            require(timestamp(page["retrievedAt"]) <= captured_at,
                    "A response retrieval time is later than the completed capture.")
            dates.append(page["retrievedAt"])
            url = page_next(page)
            if page["status"] == 204:
                require(len(pages) == 1, "A continuation unexpectedly returned no content.")
                continue
            properties = parse_json(page["raw"])["properties"]
            columns = properties["columns"]
            require(isinstance(columns, list), "Missing cost columns.")
            names = [c["name"] for c in columns]
            unique(names, "cost column names")
            types = {c["name"]: c["type"] for c in columns}
            expected = {"PreTaxCost": "Number", "Currency": "String"}
            if request["kind"] == "detail":
                expected.update({"ResourceId": "String", "ResourceLocation": "String", "UsageDate": "Number"})
            require(all(types.get(k) == v for k, v in expected.items()), "Required cost columns/types are missing.")
            if schema is None:
                schema = columns
            require(schema == columns, "Cost schema changed during pagination.")
            require(isinstance(properties["rows"], list), "Missing cost rows.")
            for values in properties["rows"]:
                require(isinstance(values, list) and len(values) == len(names), "Cost row width mismatch.")
                row = dict(zip(names, values))
                amount, currency = row["PreTaxCost"], row["Currency"]
                require(type(amount) in (int, Decimal), "Cost must remain an exact JSON number, never a float/string.")
                amount = Decimal(amount)
                require(amount.is_finite() and isinstance(currency, str) and
                        re.fullmatch(r"[A-Z]{3}", currency) is not None, "Invalid cost/currency.")
                if request["kind"] == "control":
                    require(currency not in control_currencies, "Duplicate ungrouped control currency row.")
                    control_currencies.add(currency)
                sums[currency].append(amount)
                rows_seen += 1
                if request["kind"] == "detail":
                    resource = row["ResourceId"]
                    require(resource is None or isinstance(resource, str), "Invalid billed resource ID.")
                    resource = arm_id(resource) if resource else ""
                    require(not resource or subscription_of(resource) == sid, "A cost row escaped its subscription.")
                    require(chunk is None or resource in chunk, "A cost row escaped its exact resource filter.")
                    location = row["ResourceLocation"]
                    require(location is None or isinstance(location, str), "Invalid billed location.")
                    day = str(row["UsageDate"])
                    require(re.fullmatch(r"\d{8}", day) is not None, "Invalid usage date.")
                    try:
                        datetime.strptime(day, "%Y%m%d")
                    except ValueError as exc:
                        raise EvidenceError("Invalid calendar date in cost response.") from exc
                    period = plan["manifest"]["period"]
                    require(period["from"][:10].replace("-", "") <= day <= period["to"][:10].replace("-", ""),
                            "A cost row escaped the approved reporting period.")
                    key = (sid, resource, location or "", day, currency)
                    require(key not in ledger, "Duplicate aggregated cost row; pagination/chunks may overlap.")
                    ledger[key] = amount
        require(url is None, "The last cost page still has a continuation; evidence is incomplete.")
        if not rows_seen:
            empty_requests.append(request["id"])
        totals = {c: exact_sum(v) for c, v in sums.items()}
        pair = digest({"scope": request["scope"], "filter": chunk})
        (details if request["kind"] == "detail" else controls)[pair] = totals
    require(details == controls, "Detail/control totals differ exactly; data may have refreshed or pages are missing.")
    totals_by_currency: dict[str, list[Decimal]] = defaultdict(list)
    for key, amount in ledger.items():
        totals_by_currency[key[4]].append(amount)
    return {"ledger": ledger, "totals": {c: exact_sum(v) for c, v in totals_by_currency.items()},
            "retrievedFrom": min(dates), "retrievedTo": max(dates), "emptyRequests": empty_requests}


def reconcile(actual: Json, reference: Json) -> Json:
    left, right = validate_bundle(actual), validate_bundle(reference)
    require(actual["captureId"] != reference["captureId"], "A capture cannot independently validate itself.")
    require(actual["plan"]["sha256"] == reference["plan"]["sha256"],
            "Reference plan differs: identity, scope, dates, basis, filters, or API requests are not identical.")
    differences = []
    for key in sorted(set(left["ledger"]) | set(right["ledger"])):
        a, b = left["ledger"].get(key), right["ledger"].get(key)
        if a != b:
            differences.append({"key": list(key), "actual": str(a) if a is not None else None,
                                "reference": str(b) if b is not None else None})
    return sealed({"status": "exact-match" if not differences else "mismatch", "tolerance": "0",
                   "actualSha256": actual["sha256"], "referenceSha256": reference["sha256"],
                   "planSha256": actual["plan"]["sha256"], "differences": differences})


def import_reference(plan: Json, index: Json, directory: Path) -> Json:
    verify_plan(plan)
    require(index["source"] in ("manual-azure-cli", "portal-query-export"), "Unknown manual reference source.")
    require(index["tenantId"] == plan["manifest"]["tenantId"] and
            index["principalId"] == plan["manifest"]["principalId"], "Manual reference identity mismatch.")
    timestamp(index["capturedAt"])
    captures = []
    for capture in index["captures"]:
        pages = []
        for entry in capture["pages"]:
            path = directory / entry["path"]
            require(not str(path).startswith("\\\\"), "Network-share reference files are not supported.")
            raw = path.read_text(encoding="utf-8-sig")
            pages.append({"url": entry["url"], "status": entry["status"], "raw": raw,
                          "sha256": raw_digest(raw), "retrievedAt": index["capturedAt"], "azureRequestId": ""})
        captures.append({"requestId": capture["requestId"], "pages": pages})
    bundle = sealed({"schemaVersion": 1, "captureId": str(uuid.uuid4()), "source": index["source"],
                     "capturedAt": index["capturedAt"], "plan": plan, "captures": captures})
    validate_bundle(bundle)
    return bundle


def report_model(bundle: Json, reference: Json | None = None) -> Json:
    evidence = validate_bundle(bundle)
    parity = "not-verified"
    if reference is not None:
        comparison = reconcile(bundle, reference)
        require(comparison["status"] == "exact-match",
                f"Cost reference mismatch in {len(comparison['differences'])} resource/date/location/currency rows.")
        parity = "exact-match"
    manifest = bundle["plan"]["manifest"]
    validated = parity == "exact-match" and manifest["scopeReference"]["status"] == "exact-match"
    return {"evidence": evidence, "manifest": manifest, "costParity": parity,
            "status": "VALIDATED AGAINST CAPTURED REFERENCES" if validated else "UNVERIFIED",
            "bundleSha256": bundle["sha256"], "planSha256": bundle["plan"]["sha256"],
            "referenceSha256": reference["sha256"] if reference is not None else "not supplied",
            "referenceSource": reference["source"] if reference is not None else "not supplied",
            "referenceCapturedAt": reference["capturedAt"] if reference is not None else "not supplied"}


def display_rows(model: Json) -> list[list[str]]:
    return [[*key, format(amount, "f")] for key, amount in sorted(model["evidence"]["ledger"].items())]


def markdown_report(model: Json) -> str:
    def escape(value: Any) -> str:
        text = html.escape(str(value)).replace("|", "&#124;").replace("\r", " ").replace("\n", " ")
        return re.sub(r"([\\`*_\[\]()!])", r"\\\1", text)

    manifest, evidence = model["manifest"], model["evidence"]
    lines = ["# FinOps workload consumption", "", f"**Status: {model['status']}**", "",
             f"- Tenant: {escape(manifest['tenantId'])}",
             f"- Confirmed invoker object ID: {escape(manifest['principalId'])}",
             f"- Approved subscriptions: {', '.join(manifest['approvedSubscriptionIds'])}",
             f"- Included subscriptions: {', '.join(manifest['subscriptionIds'])}",
             f"- Excluded approved subscriptions: {', '.join(manifest['excludedSubscriptionIds']) or 'none'}",
             f"- Period (inclusive UTC): {manifest['period']['from']} to {manifest['period']['to']}",
             f"- Basis: {manifest['costBasis']}; measure: PreTaxCost; original billing currencies; no FX",
             f"- Selection: {escape(canonical(manifest['scenario']['selection']))}",
             f"- Scope definition: {manifest['scopeMode']}; current inventory as of {manifest['inventoryAsOf']}",
             f"- Current selected resource count: {len(manifest['resourceIds'])}",
             f"- Resource-set reference: {manifest['scopeReference']['status']}",
             f"- Resource reference source/time: {escape(manifest['scopeReference'].get('source', 'not supplied'))} / "
             f"{manifest['scopeReference'].get('capturedAt', 'not supplied')}",
             f"- Exact cost reference: {model['costParity']}; numeric tolerance: 0",
             f"- Cost reference source/time: {escape(model['referenceSource'])} / {model['referenceCapturedAt']}",
             f"- Cost capture interval: {evidence['retrievedFrom']} to {evidence['retrievedTo']}", "",
             "## Exact amounts", "", "| Billing currency | Exact API amount | USD display after aggregation |",
             "|---|---:|---:|"]
    for currency, amount in sorted(evidence["totals"].items()):
        lines.append(f"| {currency} | {format(amount, 'f')} | {usd_display(amount) if currency == 'USD' else 'Not assumed'} |")
    if not evidence["totals"]:
        lines.append("\nNo cost records returned. This is not proof of zero spend.")
    lines += ["", "## Selected current resource IDs", ""]
    lines.extend("- " + escape(r) for r in manifest["resourceIds"])
    if not manifest["resourceIds"]:
        lines.append("No current inventory resources; historical/non-resource billing can still exist.")
    lines += ["", "## Ownership provenance", "",
              "| Kind | Directory object ID | Scope | Source | Validated UTC | Business fresh until |",
              "|---|---|---|---|---|---|"]
    for binding in manifest["ownerEvidence"]:
        lines.append("| " + " | ".join(escape(v) for v in (
            binding["kind"], binding["userId"], binding["scopeId"], binding["source"],
            binding["validatedAt"], binding.get("freshUntil", "Not a business-owner assertion"))) + " |")
    if not manifest["ownerEvidence"]:
        lines.append("\nNo owner filter was requested; no accountable owner is inferred.")
    lines += ["", "## Resource/day evidence", "",
              "| Subscription | Resource ID | Billed region | Usage date | Currency | Exact amount |",
              "|---|---|---|---|---|---:|"]
    for row in display_rows(model):
        row[1] = row[1] or "Unallocated/non-resource charge"
        row[2] = row[2] or "Not supplied by billing"
        lines.append("| " + " | ".join(escape(v) for v in row) + " |")
    lines += ["", "## Coverage and limitations", "",
              "- Current inventory and historical billing are different sets. Deleted resources can remain in billing.",
              "- Current tag, region, and owner filters select current resource IDs, not historical ownership/tags.",
              "- Resource-filtered reports exclude charges without a matching resource ID; they are not whole-workload allocation.",
              "- Subscription-wide reports retain unallocated charges without inventing a resource owner.",
              "- RBAC Owner describes access, not business accountability; business records retain their own source/freshness.",
              "- Amounts are unrounded; portal display rounding is not applied before aggregation.",
              "- The additional USD display uses two-decimal half-up rounding AFTER aggregation; other currency precision is not guessed.",
              "- Cost Management can refresh or be rerated. Exact parity applies only to the captured references, not future data.",
              "- These are cost/usage records, not real-time utilization, forecasts, savings guarantees, or final invoice totals.",
              f"- Empty query responses: {len(evidence['emptyRequests'])}; inaccessible/incomplete requests block the report.",
              "", "## Evidence fingerprints", "",
              f"- Scenario: `{manifest['scenarioSha256']}`",
              f"- Catalog: `{manifest['catalogSha256']}`",
              f"- Query plan: `{model['planSha256']}`",
              f"- Capture: `{model['bundleSha256']}`",
              f"- Cost reference: `{model['referenceSha256']}`",
              f"- Resource reference: `{manifest['scopeReference'].get('sha256', 'not supplied')}`", ""]
    return "\n".join(lines)


def html_report(model: Json) -> str:
    escape = html.escape
    markdown = markdown_report(model)
    headings = ["Subscription", "Resource ID", "Billed region", "Usage date", "Currency", "Exact amount"]
    rows = display_rows(model)
    table = "".join("<tr>" + "".join(f"<td>{escape(v or 'Not allocated/supplied')}</td>" for v in r) + "</tr>"
                    for r in rows)
    totals = "".join(
        f"<tr><td>{currency}</td><td>{format(amount, 'f')}</td>"
        f"<td>{usd_display(amount) if currency == 'USD' else 'Not assumed'}</td></tr>"
        for currency, amount in sorted(model["evidence"]["totals"].items())
    )
    if not totals:
        totals = '<tr><td colspan="3">No records returned; not proof of zero spend.</td></tr>'
    manifest = model["manifest"]
    charts = []
    for currency in sorted(model["evidence"]["totals"]):
        amounts = [(key, amount) for key, amount in model["evidence"]["ledger"].items() if key[4] == currency]
        amounts.sort(key=lambda item: item[1].copy_abs(), reverse=True)
        largest = max((a.copy_abs() for _, a in amounts), default=Decimal(0))
        bars = []
        for index, (key, amount) in enumerate(amounts[:10]):
            width = int(amount.copy_abs() / largest * 400) if largest else 0
            label = f"{key[1] or 'Unallocated'} / {key[3]}: {format(amount, 'f')} {currency}"
            y = index * 42
            bars.append(f'<text x="0" y="{y + 13}">{escape(label)}</text>'
                        f'<rect x="0" y="{y + 20}" width="{width}" height="12" '
                        f'fill="{"#b45309" if amount < 0 else "#0369a1"}"/>')
        charts.append(f"<h2>{currency}: top 10 resource/day magnitudes (credits in orange)</h2>"
                      f'<svg role="img" aria-label="Relative cost magnitudes; exact values in table" '
                      f'viewBox="0 0 1100 {max(42, len(bars) * 42)}">{"".join(bars)}</svg>')
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; '
        'img-src data:; base-uri \'none\'; form-action \'none\'">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>FinOps workload consumption</title><style>"
        "body{font:14px system-ui,sans-serif;margin:2rem;color:#172033}"
        "pre{white-space:pre-wrap;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%}"
        "td,th{border:1px solid #ccd3de;padding:.4rem;text-align:left;overflow-wrap:anywhere}"
        "th{white-space:nowrap}"
        "svg{width:100%;font-size:11px}@media print{body{margin:0}tr{break-inside:avoid}svg{max-height:22rem}}"
        "</style></head><body>"
        f"<h1>FinOps workload consumption</h1><p><strong>{escape(model['status'])}</strong></p>"
        f"<p>{manifest['costBasis']} / PreTaxCost / {manifest['period']['from']} to {manifest['period']['to']} "
        f"(inclusive UTC). Scope: {manifest['scopeMode']}. No FX conversion.</p>"
        "<h2>Exact billing-currency totals</h2><table><thead><tr><th>Currency</th><th>Exact API amount</th>"
        "<th>USD display after aggregation</th></tr></thead><tbody>" + totals + "</tbody></table>"
        + "".join(charts) + "<h2>Complete resource/day table</h2><table><thead><tr>"
        + "".join(f"<th>{h}</th>" for h in headings) + "</tr></thead><tbody>" + table
        + "</tbody></table><h2>Full report and provenance</h2><pre>" + escape(markdown)
        + "</pre></body></html>"
    )


def export_pdf(document: str, output: Path, browser: Path) -> None:
    require(browser.is_file(), "PDF export requires an explicitly selected installed Chromium-compatible executable.")
    require(not output.exists(), "Output already exists; it will not be overwritten.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="finops-print-") as directory:
        root = Path(directory)
        source, target = root / "report.html", root / "report.pdf"
        source.write_text(document, encoding="utf-8")
        result = subprocess.run(
            [str(browser), "--headless", "--disable-gpu", "--no-pdf-header-footer",
             "--disable-background-networking", "--disable-extensions", "--no-first-run",
             "--user-data-dir=" + str(root / "profile"), "--print-to-pdf=" + str(target), source.as_uri()],
            capture_output=True, timeout=120, check=False,
        )
        valid_pdf = target.is_file() and target.stat().st_size > 100 and target.read_bytes().startswith(b"%PDF-")
        require(result.returncode == 0 and valid_pdf,
                f"Browser PDF export failed (exit {result.returncode}; valid PDF: {valid_pdf}). "
                "Choose a working Edge, Chrome, or Chromium headless-shell runtime; no PDF was accepted.")
        with output.open("xb") as stream:
            stream.write(target.read_bytes())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    identity = commands.add_parser("identity", help="Inspect current invoker context; never sign in or switch accounts.")
    identity.add_argument("--tenant", required=True)
    identity.add_argument("--subscription", required=True)
    inventory = commands.add_parser("inventory", help="Collect complete caller-visible inventory in approved subscriptions.")
    inventory.add_argument("--scenario", type=Path, required=True)
    inventory.add_argument("--owners", type=Path)
    scope = commands.add_parser("resolve", help="Resolve exact identifiers and deterministic filter intersections.")
    scope.add_argument("--scenario", type=Path, required=True)
    scope.add_argument("--catalog", type=Path, required=True)
    scope.add_argument("--resource-reference", type=Path)
    plan = commands.add_parser("plan", help="Generate read-only Cost Management detail/control requests.")
    plan.add_argument("--manifest", type=Path, required=True)
    query = commands.add_parser("query", help="Run an approved plan as the confirmed invoker.")
    query.add_argument("--plan", type=Path, required=True)
    capture = commands.add_parser("import-reference", help="Import all raw manual portal/API or Azure CLI query pages.")
    capture.add_argument("--plan", type=Path, required=True)
    capture.add_argument("--index", type=Path, required=True)
    compare = commands.add_parser("reconcile", help="Compare every resource/day/location/currency amount exactly.")
    compare.add_argument("--actual", type=Path, required=True)
    compare.add_argument("--reference", type=Path, required=True)
    report = commands.add_parser("report", help="Render one evidence model as Markdown, standalone HTML, or PDF.")
    report.add_argument("--actual", type=Path, required=True)
    report.add_argument("--reference", type=Path)
    report.add_argument("--format", choices=("markdown", "html", "pdf"), default="markdown")
    report.add_argument("--browser", type=Path)
    for command in (identity, inventory, scope, plan, query, capture, compare, report):
        command.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        require(not args.out.exists(), "Output already exists; choose a new path.")
        if args.command == "identity":
            context, _ = azure_identity(args.tenant, args.subscription)
            result = context
        elif args.command == "inventory":
            scenario = read_json(args.scenario)
            validate_scenario(scenario)
            client = AzureClient(scenario["tenantId"], scenario["principalId"], scenario["approvedSubscriptionIds"])
            result = collect_inventory(scenario, client, read_json(args.owners) if args.owners else None)
        elif args.command == "resolve":
            result = resolve_scope(read_json(args.scenario), read_json(args.catalog),
                                   read_json(args.resource_reference) if args.resource_reference else None)
        elif args.command == "plan":
            result = make_plan(read_json(args.manifest))
        elif args.command == "query":
            query_plan = read_json(args.plan)
            verify_plan(query_plan)
            manifest = query_plan["manifest"]
            client = AzureClient(manifest["tenantId"], manifest["principalId"], manifest["subscriptionIds"])
            result = execute_plan(query_plan, client)
        elif args.command == "import-reference":
            result = import_reference(read_json(args.plan), read_json(args.index), args.index.resolve().parent)
        elif args.command == "reconcile":
            result = reconcile(read_json(args.actual), read_json(args.reference))
            write_json(args.out, result)
            if result["status"] != "exact-match":
                print(f"FinOps mismatch: {len(result['differences'])} monetary rows differ; see {args.out}.",
                      file=sys.stderr)
                return 2
            return 0
        else:
            model = report_model(read_json(args.actual), read_json(args.reference) if args.reference else None)
            if args.format == "pdf":
                require(args.browser is not None, "Supply --browser for PDF export; no browser will be installed.")
                export_pdf(html_report(model), args.out, args.browser)
            else:
                write_text(args.out, html_report(model) if args.format == "html" else markdown_report(model))
            return 0
        write_json(args.out, result)
        return 0
    except (EvidenceError, OSError, KeyError, TypeError, ValueError, subprocess.SubprocessError) as exc:
        print(f"FinOps blocked: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
