---
name: write-architecture
description: "Create or update architecture documentation at system level or component level. System scope covers the whole codebase (backend or frontend); component scope covers a specific bounded context's internals. Triggers: 'document the architecture', 'architecture overview', 'create/update arch docs', 'arch docs are outdated', 'how does the system work', 'document this component', 'component architecture'."
---

## Process Overview

1. Determine **scope** (system or component), **domain** (backend or frontend, system scope only), and **workflow** (init or update)
2. Load the matching reference
3. Execute the init or update workflow

## Step 1: Scope, Domain, and Workflow

### Scope

Determine from the user's request:

- User asks about the overall system, full codebase, or doesn't specify a component → **System**
- User names a specific bounded context, module, service, or package → **Component**

If ambiguous, ask: "Do you want to document the overall system architecture, or a specific component?"

### Output

| Scope | Output path |
|-------|-------------|
| System | `docs/development/system/architecture.md` |
| Component | `docs/development/system/components/<component-name>/architecture.md` |

### Domain (system scope only)

Detect from package manifests and framework config files. If the project is full-stack, ask which aspect to document first. Component scope is domain-agnostic.

### Workflow

- Target document **does not exist** or user asks to create from scratch → **Init**
- Target document **exists** and needs refreshing → **Update**
- Document exists but is severely outdated (missing multiple sections) → treat as **Init**

### Load Reference

**System scope** — read the reference matching the domain:

- **Backend** → [references/backend.md](references/backend.md): Backend system template, exploration guide for services/APIs/infra, quality checklist.
- **Frontend** → [references/frontend.md](references/frontend.md): Frontend app template, exploration guide for components/routing/state/styling, quality checklist.

**Component scope** → [references/component.md](references/component.md): Component architecture template, bounded context exploration guide, quality checklist.

## Step 2a: Init — Create from Scratch

### Explore

Start broad, then go deep — building a mental model of the whole system first prevents tunnel vision and ensures each component is understood in its larger context. Use parallel exploration agents for large codebases.

1. **Survey:** Orient yourself to the project — read README, CLAUDE.md, package manifests, and scan top-level directories. Identify the system type and primary frameworks. The goal is to form a high-level picture before diving into any single area.
2. **Deep exploration:** Follow the exploration guide from the loaded reference. Spend more time where architecture is non-obvious or complex; skip areas that clearly don't apply. Use judgment about depth — a simple CRUD service needs less exploration than a distributed system with multiple communication patterns.

### Draft

1. Create the output directory if needed.
2. Follow the template structure from the loaded reference.
3. Write each section as soon as you've gathered its information. Context is freshest right after exploration — waiting risks confabulating details from other parts of the codebase.
4. Include Mermaid diagrams for non-trivial relationships and flows. Use actual line breaks in node labels (not `\n` escapes, which render as literal text in most Markdown viewers).
5. Ground architectural claims in concrete code — reference specific files and directories so readers can verify and so the document stays anchored to reality as the codebase evolves.
6. Omit template sections that don't apply — a shorter, accurate document is more useful than one padded with empty headings.
7. Set "Last updated" to today's date.

### Verify

1. Re-read the full document and check for contradictions between sections. Sections written at different times can drift, especially if the codebase itself has inconsistencies.
2. Spot-check a handful of file/directory references to confirm they exist and point where expected.
3. Remove sections that ended up empty or contain only boilerplate.
4. Apply the quality checklist from the loaded reference.
5. Confirm the document answers the navigational questions new developers ask first: "Where does X live?" and "How does Y flow?"

## Step 2b: Update — Sync with Changes

### Define Scope

The goal is to find changes that affect the document's accuracy — not to exhaustively catalog every recent commit.

**User specifies changes** (e.g., "I added a payments module"):
→ Use their description.

**User says "update it" without specifics:**
→ Scan recent git history to identify changes that could affect the document's accuracy.

**Git history unavailable:**
→ Compare document against current codebase structure. Look for discrepancies.

Summarize scope before proceeding: "These areas have changed: [list]. I'll update these sections." This alignment step prevents wasted work if the user had something different in mind.

### Explore Changes

1. Read changed files and their immediate context.
2. Check cascading effects — does this change affect other documented sections?
3. Note new patterns introduced or old patterns removed.
4. Stay focused on the defined scope — resist the urge to rewrite unaffected sections.

### Apply Edits

1. Read the current document, then edit only affected sections.
2. Update "Last updated" date.
3. Add new sections following existing style; remove sections no longer relevant.
4. Update Mermaid diagrams if relationships or flows changed.
5. Match existing detail level and writing style — consistency matters more than any one section being perfect.

### Verify

1. Re-read modified sections in context of surrounding sections for coherence.
2. Check that cross-references still hold (e.g., renamed modules mentioned elsewhere).
3. Apply the quality checklist from the loaded reference.
4. Summarize what was updated for the user.
