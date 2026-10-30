---
name: finops-invoker-access
description: "Use when connecting to Azure for FinOps on behalf of an invoker, confirming tenant/user/subscription identity, diagnosing cost-query permission gaps, or preventing developer/service-identity substitution."
---

# Invoker-bound Azure access

## Contract

Use the invoker's interactive Azure CLI context, never a service principal or a
machine/developer identity assumed to represent the user. This skill does not
register an app, implement server-side OAuth OBO, change accounts, grant access,
or store tokens. Public Azure (`AzureCloud`) is currently supported; other clouds
must stop explicitly.

Use Python 3.11+ and the [shared helper](../finops-cost-evidence/scripts/finops.py).
This skill depends on `finops-cost-evidence`; copy both when reusing it.

## Procedure

1. Obtain the intended tenant and an explicitly approved subscription ID.
   Subscription/MG name discovery is an authorized metadata-only step; it does
   not authorize workload collection across every visible subscription.
2. If authentication is needed, have the user sign in as themselves with
   `az login --tenant <tenant-id>`. Do not request credentials in chat.
   Do not run `az account set`, clear shared caches, or substitute another identity.
3. Inspect the selected context without changing global CLI state:

   ```powershell
   $helper = '.github\skills\finops-cost-evidence\scripts\finops.py'
   python $helper identity --tenant '<tenant-id>' --subscription '<subscription-id>' --out '.finops-runs\identity.json'
   ```

4. Ask the invoker to confirm the returned tenant/object ID. Bind those IDs
   immutably into the scenario. On guest accounts, use the object ID in the
   selected resource tenant, not a guessed home-tenant ID or email.
5. Before collection/query, check that the user approved the exact subscription
   list. The helper validates every subscription profile and token `tid`/`oid`,
   user identity type, audience, cloud, subscription state, and token expiry.
   ARM validates the token; local JWT claim inspection is not signature verification.
6. Require least-privilege access appropriate to the requested sources:

   | Source | Permission consideration |
   |---|---|
   | Resource inventory | Reader/equivalent resource-read access at approved scope; ARG is caller-visible, not proof of tenant-wide completeness. |
   | Cost Management | Cost Management Reader/equivalent cost-read permission and applicable billing policies/offer support. Resource read alone is insufficient. |
   | Directory/groups | Approved Microsoft Graph user and transitive-membership read access. Do not request directory-wide grants automatically. |
   | RBAC ownership | Read assignments, role definitions, active PIM and applicable conditions/denies. Owner role is not needed to perform this analysis. |
   | Business ownership | Invoker-authorized read-only ServiceNow connector or approved export; source and freshness are mandatory. |
   | Invoice | Separate billing/invoice entitlement; subscription access is not proof of invoice access. |

7. Treat `401`, `403`, identity mismatch, missing directory access, unsupported
   cloud, and inactive subscriptions as explicit blocked states. Empty cost
   data is different from denied access. Never retry as another identity.

## Handling evidence

Only metadata (tenant, principal, subscription, verification time) is written by
`identity`. Tokens remain in process memory and must not enter artifacts, logs,
prompts, URLs, source control, or reports. Repeat identity validation for each
new run; if a token expires mid-run, restart collection with a new capture rather
than accepting a partial result.

These are a local agent's controls. A multi-user web service would require a
separate delegated-auth and isolation implementation before it can claim to act
on behalf of each invoker.
