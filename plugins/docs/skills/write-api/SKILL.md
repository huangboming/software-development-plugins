---
name: write-api
description: "Create or update API documentation that defines the system's external boundary — what consumers need to integrate. Produces an overview plus per-API detail docs. Triggers: 'document the API', 'API docs', 'API reference', 'what APIs exist', 'endpoint documentation'."
---

# Write API

Document the system's external API boundary: what the system exposes to outside consumers and what contracts they must follow.

## Output Structure

```
docs/apis/
  overview.md                <-- Landscape: what APIs exist, conventions, relationships
  <resource-group>.md        <-- Full contract detail per resource group / domain module
```

- `overview.md` is always produced. It is the entry point.
- One `<resource-group>.md` per domain module (e.g., `users.md`, `orders.md`, `payments.md`). Each file contains all protocols for that domain — REST endpoints, events, GraphQL operations — in one place.
- Name files after the domain, not the protocol or internal component.
- For a system with a single resource group, produce `overview.md` + one detail file. Keep the separation so the structure scales.

## Process

1. Determine **workflow** (init or update)
2. Load the [reference](references/api-reference.md): templates, discovery guide, quality checklist
3. Execute the workflow

## Step 1: Workflow

- Target docs **do not exist** or user asks to create from scratch -> **Init**
- Target docs **exist** and need refreshing -> **Update**
- Docs exist but are severely outdated -> treat as **Init**

## Step 2: Init — Create from Scratch

### Explore

1. **Survey the API surface.** Identify what types of APIs the system exposes externally — REST endpoints, GraphQL schemas, gRPC services, WebSocket channels, webhook callbacks, event contracts, CLI commands. Scan route registrations, schema files, and public exports.
2. **Decide file breakdown.** Group by resource domain or module (e.g., users, orders, billing). Each group becomes one `<resource-group>.md` containing all protocols for that domain. Aim for files under 300 lines; split further if a domain is large.
3. **Deep extraction.** For each resource group, follow the extraction guide in the reference. Trace routes to handlers, read request/response types, identify error paths and side effects.

### Draft

1. Create `docs/apis/` if needed.
2. Write `overview.md` using the overview template from the reference.
3. Write each `<resource-group>.md` using the detail template from the reference.
4. Ground every claim in concrete code — reference route files, schema definitions, handler implementations.
5. Include request/response examples for non-trivial contracts. Use realistic but anonymized data.
6. Omit template sections that don't apply.
7. Set "Last updated" to today's date in each file.

### Verify

1. Spot-check documented endpoints against actual code.
2. Verify input/output types match what the code actually expects and returns.
3. Apply the quality checklist from the reference.

## Step 3: Update — Sync with Changes

### Define Scope

**User specifies changes** (e.g., "I added a new endpoint"):
-> Use their description.

**User says "update it" without specifics:**
-> Scan recent git history for route, schema, or interface changes.

**Git history unavailable:**
-> Compare docs against current API surface. Look for discrepancies.

Summarize scope before proceeding.

### Apply Edits

1. Read current docs, then edit only affected sections.
2. Update "Last updated" date in modified files.
3. Add new entries following existing style; remove entries for deleted APIs.
4. If a new resource group appears, create a new `<resource-group>.md` and add it to the overview.
5. Match existing detail level.

### Verify

1. Re-read modified sections for coherence with surrounding content.
2. Check that cross-references between overview and detail files still hold.
3. Apply the quality checklist from the reference.
4. Summarize what was updated for the user.

## Edge Cases

- **No formal APIs** (library or CLI tool): Document exported public interfaces or CLI commands. Adapt templates accordingly.
- **GraphQL only**: Overview documents the schema landscape. Detail doc covers key queries, mutations, subscriptions with input/output types.
- **Event-driven only** (no REST/gRPC): Document event contracts — topics, payload schemas, producers, consumers.
- **Mixed API types**: Each resource group doc includes all protocol types for that domain (REST + events, etc.), with sections per protocol.
- **Single resource group** (< 10 endpoints): Still use overview + one detail file for consistency.
