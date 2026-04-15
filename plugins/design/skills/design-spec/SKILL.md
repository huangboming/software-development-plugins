---
name: design-spec
description: "Design backend or frontend features through structured spec-driven development. Produces a design-focused spec with mermaid diagrams (architecture, data flow, sequence, component, state) and intentionally excludes detailed code. Triggers: 'design an API for...', 'design a UI for...', 'create a tech spec', 'plan the architecture for...', 'design-spec for [feature]', 'write a spec for [feature]', 'I need to implement [feature]'."
---

# Design Spec

Create a design-focused technical specification for a backend or frontend feature through a structured workflow.

The spec describes **what to build and why**, not how to type it. Visualize structure and behavior with mermaid diagrams; omit implementation-level code (function bodies, full SQL DDL, exhaustive JSON payloads).

```
Step 1: Receive Requirement      → Understand the initial idea
Step 2: Classify Scope           → Backend, frontend, or both
Step 3: Explore Codebase         → Launch agents, read key files
Step 4: Clarify Requirements     → Ask multiple-choice questions
Step 5: Research (If Needed)     → Mature solutions for unfamiliar domains
Step 6: Design & Propose Plans   → Analyze constraints, present options
Step 7: Write Spec               → Generate spec with mermaid diagrams
Step 8: Review (Multi-Axis)      → Ask user, then launch spec-reviewer agents in parallel
Step 9: Reconcile & Deliver      → Consolidate findings, apply fixes, deliver
```

## References

This skill bundles three on-demand reference files. Load them at the step noted:

- **[references/clarification-questions.md](references/clarification-questions.md)** — multiple-choice question patterns grouped by Shared / Backend / Frontend, plus domain sets (auth, payments, search, dashboards, forms, real-time, …). Read at **Step 4** to pick 3-5 questions.
- **[references/design-guide.md](references/design-guide.md)** — decision frameworks for backend runtime patterns, frontend rendering/state/styling, code architecture (layering, encapsulation, testability), and a common-spec-mistakes checklist. Read at **Step 6** when analyzing constraints and trade-offs.
- **[references/spec-template.md](references/spec-template.md)** — section-by-section template for the delivered spec, including which mermaid diagram type to use where. Read at **Step 7** when writing the spec file.

## Hard constraints

Apply to every run of this skill; do not relax them without the user's explicit instruction.

- **Design-first, code-light** — describe structure and shapes with tables and mermaid diagrams. No function bodies, no full SQL DDL, no large JSON payload examples. A ≤10-line snippet is acceptable only when shape is otherwise ambiguous.
- **Diagrams are required** — every non-trivial spec contains at least one architecture/component diagram *and* one behavior diagram (sequence or state), rendered in mermaid.
- **Dependencies are explicit** — list every third-party library, infrastructure component, and external service by name. Assume nothing is already deployed.
- **Confirm before delegating** — Step 8 spawns `spec-reviewer` subagents; always ask the user and wait for confirmation before launching.

## Step 1: Receive Requirement

Initial request: $ARGUMENTS

If the request is too vague to explore the codebase (e.g., "I need a dashboard" with no specifics):
  → Ask 2-3 scoping questions before proceeding: what domain, what problem, what users.

## Step 2: Classify Scope

Decide which track(s) this feature covers so later steps target the right patterns:

- **Backend** — APIs, data models, background jobs, integrations, infrastructure
- **Frontend** — UI flows, components, client state, routing, rendering strategy
- **Full-stack** — both; design each track's concerns explicitly and show the contract between them

State the classification to the user in one line before Step 3 so they can correct it early.

## Step 3: Codebase Exploration

Launch 2-3 explorer agents in parallel, each targeting a different aspect. Tailor the prompts to the scope from Step 2:

**Backend-leaning features:**
1. Similar features — "Find backend features similar to [feature] and trace their implementation comprehensively"
2. Architecture — "Map the service/module architecture and abstractions for [feature area]"
3. Data & integrations — "Analyze data models, external integrations, and background jobs around [area]"

**Frontend-leaning features:**
1. Similar UI — "Find UI flows similar to [feature], trace components, state, and routing"
2. Component architecture — "Map the component hierarchy, shared primitives, and styling system for [area]"
3. Client data layer — "Trace data fetching, caching, and client state management for [area]"

**Full-stack features:** mix the two — include at least one backend agent and one frontend agent, plus the contract/boundary between them.

Each agent should return a list of 5-10 key files to read. After agents return, read all identified files to build deep understanding. Present a summary of findings and patterns discovered.

## Step 4: Clarify Requirements

Complete this step before designing — unresolved ambiguities lead to wasted effort.

1. Review codebase findings and original request
2. Identify underspecified aspects. For backend: edge cases, error handling, integration points, consistency, backward compatibility, performance. For frontend: target devices, accessibility, loading/empty/error states, offline behavior, design-system reuse, SEO/SSR needs
3. Present 3-5 multiple-choice questions to the user (not open-ended) to reduce cognitive load

   See [references/clarification-questions.md](references/clarification-questions.md) for question patterns organized by topic (backend, frontend, and domain-specific sets).

   **Format:**
   ```
   **[Topic]**: [Question]?
   - A) [Option with brief description]
   - B) [Option with brief description]
   - C) [Option with brief description]
   ```

4. Wait for answers before proceeding

If answers reveal the feature is significantly different from initial understanding:
  → Revisit Step 3 with refined scope before designing.

## Step 5: Research (If Needed)

Research when the feature involves unfamiliar domains (payments, search infrastructure, real-time systems, complex UI patterns like virtualization, rich-text editing, drag-and-drop, offline-first sync) or when the codebase exploration revealed no existing patterns to follow.

Use Researcher agents to investigate mainstream approaches, common pitfalls, and relevant libraries. Skip this step when the feature is a straightforward extension of existing patterns already discovered in Step 3.

## Step 6: Design & Propose Plans

### 6.1 Design Thinking (Internal)

Before presenting options, systematically analyze:

1. **Constraints** — Hard technical constraints, business/timeline constraints, existing systems to integrate with
2. **System architecture fit** — What runtime patterns fit this problem? Monolith vs microservice, sync vs async, SSR vs CSR, storage choice, transport choice. See [references/design-guide.md](references/design-guide.md) for backend and frontend decision frameworks
3. **Code architecture fit** — How should the source be organized inside whatever runtime you pick? Layering (domain / application / adapters / infrastructure), dependency direction (inward only), module boundaries and their public APIs, separation of concerns, testability seams. See the "Code Architecture" section in [references/design-guide.md](references/design-guide.md)
4. **Trade-offs** — Consistency vs availability, simplicity vs flexibility, speed-to-market vs maintainability, build vs buy; for frontend add: SSR vs CSR, shared state vs local state, custom vs design-system primitives; for code structure: strict layering vs velocity, one public entry point vs convenience of deep imports
5. **Risks** — What could go wrong? What are the unknowns? Where might a pivot be needed?

### 6.2 Propose Plans

Present 2-3 options:

```
### Option [N]: [Name]

**Approach:** [brief summary]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Best for:** [When to choose this option]
```

End with: **Recommendation:** [Recommended option with clear justification based on the constraints and trade-offs analyzed]

Ask the user which approach they prefer.

If the user asks for an option not presented:
  → Evaluate it against the same constraints and trade-offs, then present a comparison with the recommended option.

## Step 7: Write Spec

After the user selects a plan, generate `docs/development/specs/<feature-name>.md` following the template in [references/spec-template.md](references/spec-template.md). Derive `<feature-name>` from the spec topic, slugified to kebab-case (e.g., "User Authentication" becomes `user-authentication`). Create the `docs/development/specs/` directory if it does not exist.

Honor the "design-first, code-light" hard constraint above. Pick the mermaid flavor that matches what you are visualizing:

| Intent | Mermaid type |
|--------|--------------|
| Architecture / component layout | `flowchart` or `graph` |
| Module boundaries & dependency direction | `flowchart` with subgraphs per layer |
| Data flow through the system | `flowchart` with directional arrows |
| Request/response or interaction sequence | `sequenceDiagram` |
| Entities and relationships | `erDiagram` (instead of full SQL DDL) |
| Lifecycle / status transitions | `stateDiagram-v2` |
| Frontend component tree | `flowchart` top-down |

Name fields, types, and constraints in tables; name endpoints and their request/response shapes in tables.

## Step 8: Review (Multi-Axis)

Before delivering, offer the user a parallel multi-axis review using the `spec-reviewer` subagent. Do **not** launch the reviewers without confirmation — review is opt-in.

Prompt the user exactly once, in this shape:

```
The spec is drafted at docs/development/specs/<feature-name>.md.

Run a parallel review with spec-reviewer agents? Each focuses on a different axis:

- A) Completeness — sections, error/empty/loading states, capacity, dependencies,
     migration plan, Phase 1 minimality, diagrams consistent with text, no code leaked
- B) Architecture — system architecture (does the design solve the problem?
     alternatives, pattern fit, scope, phase dependencies) AND code architecture
     (layering, module boundaries, dependency direction, encapsulation, testability)
- C) Risk — security, scalability, performance budgets, failure modes, operability

Reply with: "all" (default, recommended) · a subset like "A, C" · or "skip" for a
quick self-review instead.
```

Then branch:

- **User selects one or more axes** → launch the `spec-reviewer` agent *in parallel*, one Task call per selected axis. Each call must pass (1) the absolute spec path, (2) the single axis name, and (3) the scope (`backend` / `frontend` / `full-stack`) from Step 2. Do not bundle multiple axes into one invocation — the reviewer is scoped to one axis per run so findings stay focused.
- **User replies "skip"** → perform a fast self-review against the "Common Spec Mistakes" list in [references/design-guide.md](references/design-guide.md) and proceed to Step 9.

Wait for all parallel reviewers to return before proceeding.

## Step 9: Reconcile & Deliver

Consolidate the reviewers' findings:

1. **Merge and dedupe** — collapse findings that different axes raised about the same line (rare but possible; keep the clearest wording)
2. **Group by severity** — Critical → Major → Minor, preserving the axis tag on each finding
3. **Present to the user** — show the consolidated list with the verdict from each axis (e.g. "Completeness: approve with changes · Architecture: approve · Risk: needs revision"). For each Critical and Major finding, show the proposed fix inline
4. **Apply agreed fixes to the spec** — edit the spec file directly for fixes the user accepts; skip or park fixes the user declines
5. **Deliver** — confirm the final spec path and mark status as `In Review` or `Approved` per the user's call

If the user wants to implement the spec after approval, hand off to the appropriate coding workflow.

## Edge cases

- **Codebase exploration returns nothing similar** (greenfield feature or fresh repo): skip pattern matching, design from first principles, call this out explicitly in the spec's "Proposed Solution" reasoning, and lean on Step 5 research.
- **User selects an option that conflicts with a stated constraint** (e.g. microservices for a 3-person team, global state for a single-route feature): surface the conflict, restate the trade-off, and ask the user to confirm the override — do not silently proceed.
- **Reviewers return conflicting verdicts at Step 9** (e.g. completeness approves, risk needs revision): present every verdict with its axis tag; let the user adjudicate. Do not average or hide disagreement.
- **A reviewer reports the file is not a design spec** (wrong shape, missing sections): stop Step 8, relay the reviewer's message, and return to Step 7 to fix the structure before re-running the review.
- **Scope is genuinely too large for one document**: offer to split into a parent spec plus one child spec per subsystem rather than produce one monolithic, unreviewable file.
- **User skips the clarification step** ("just design it"): proceed, but record every assumption you had to make in a dedicated "Assumptions" subsection under Introduction & Context, so reviewers can flag wrong ones.
