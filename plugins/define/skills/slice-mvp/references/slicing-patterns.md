# Slicing Patterns

Catalog of MVP slicing shapes. Read when selecting a shape in SKILL.md Step 3, and when a chosen shape feels like a poor fit for the load-bearing risk.

Each pattern lists: what-it-tests, when-to-pick, gotchas, and a minimal example.

## Selection table

| Load-bearing risk | Primary shapes | Secondary |
|---|---|---|
| **Desirability** (will the target user adopt?) | Vertical slice, Concierge | Wizard of Oz |
| **Feasibility** (can we build and operate it?) | Walking skeleton, Read-only slice | Batch-before-real-time |
| **Viability** (does the economics work?) | Concierge, Configuration-only | Vertical slice in one segment |
| **Mixed / low risk** | Vertical slice | — |

The table is a starting point, not a rule. Always check the chosen shape's preconditions before committing.

## Walking skeleton

**What it tests:** End-to-end technical integration — that every layer can talk to the next, even if each layer is trivial.

**When to pick:** Multiple systems must integrate. The team has never shipped the full pipeline together. Fast iteration depends on knowing the happy path works.

**Gotchas:**

- Easy to mistake for a real MVP. A walking skeleton has no user value on its own — it is scaffolding. Always pair with a user-observable capability as the first fleshing-out.
- Do not stub what is cheap to build real. If the "skeleton" of the payments layer is a mocked API, payments becomes the late risk, not the early one.

**Example:** A new AI feature spans ingestion → inference → UI render. v1 passes one real request through every layer with a fixed prompt; the UI shows the raw output. No prompt tuning, no caching, no streaming. Just that the pipe works.

## Vertical slice

**What it tests:** Whether the target segment adopts a complete, narrow capability.

**When to pick:** Desirability is the load-bearing risk. The product has a clear primary user and a sharp job-to-be-done. Edge cases and secondary segments can wait.

**Gotchas:**

- The slice must be truly complete for the segment. A vertical slice with "minus onboarding" or "minus error handling" is a prototype, not a slice.
- Segment choice is the real decision. A sharp segment + sharp job beats a broad feature every time.

**Example:** A reporting tool will eventually serve sales, marketing, and product. v1 ships for marketing managers only, Monday executive reports only, with full polish — templates, export, share link. Sales and product see nothing.

## Concierge

**What it tests:** Whether the value hypothesis holds when the service is delivered by humans before being automated.

**When to pick:** Automating is expensive and value is unproven. Willingness-to-pay or willingness-to-engage is the viability question. Small initial scale is acceptable.

**Gotchas:**

- Transparency matters. Users should know a human is in the loop (or not care). Hiding human labor creates brittleness when scaling.
- Measure the *pull*, not the *satisfaction*. Every concierge user is grateful because they are early and feel special. What matters is whether they would pay or return.

**Example:** A tax-prep SaaS will eventually auto-categorize transactions. v1 has no ML — a human operator reviews each new user's transactions by hand within 24 hours. Measures whether users will pay $X/month for categorized books.

## Wizard of Oz

**What it tests:** UX and desirability when the automation looks real but is manual behind the scenes.

**When to pick:** The UX is unproven and automating it would be expensive. Users need to believe the thing is real to respond authentically.

**Gotchas:**

- Does not test feasibility. A convincing Wizard of Oz says nothing about whether the team can actually build it.
- Often conflated with Concierge. Concierge is transparent ("a human is doing this"); Wizard of Oz is opaque ("it looks automated"). They test different things.

**Example:** An AI resume-screening product. v1 has a real UI that scores resumes in 30 seconds. Behind the curtain, a recruiter scores each one by hand inside the 30-second window. Measures whether the user experience is acceptable before the ML is built.

## Configuration-only

**What it tests:** Whether value is delivered in a narrow configuration, deferring customization capabilities.

**When to pick:** The full product will customize across many dimensions (industries, sizes, integrations). v1 can hard-code one.

**Gotchas:**

- Pick the configuration where the first customer already lives. Configuring for a hypothetical modal customer wastes the slice.
- Hard-coding is a choice, not a limitation. If v1 has customization disguised as hard-coding (a JSON config file users can edit), it is not really a configuration-only slice.

**Example:** A CRM will eventually support 50 integrations. v1 integrates with Gmail only. Users who need Salesforce are told "v2."

## Read-only slice

**What it tests:** Whether the display / insight / query value is worth using, independent of the write path.

**When to pick:** The full product reads and writes. Writes are expensive, risky, or unproven. The read path alone has value.

**Gotchas:**

- Watch for users who need the write to trust the read. "I would use the dashboard but I cannot fix what it shows me" means the slice is missing the value.
- The read-only slice is a trap when the real product is transactional. A read-only banking app is a statement viewer, not a product.

**Example:** A deployment tool will eventually trigger and roll back deploys. v1 only shows the current deploy state across environments. Users still deploy via the old scripts.

## Batch-before-real-time

**What it tests:** Whether async or delayed delivery of the value meets user needs.

**When to pick:** Real-time is technically expensive. The user's job tolerates delay (daily, hourly). Shipping async unblocks everything else.

**Gotchas:**

- Ask the user what the real latency budget is. "Real-time" often means "within an hour" — do not over-engineer.
- The migration path to real-time is part of the slice. If the batch architecture cannot evolve to streaming, the slice is a dead end, not a stepping stone.

**Example:** A fraud-detection product will eventually score transactions in <100ms. v1 scores transactions in a nightly batch; flagged transactions are surfaced to analysts the next morning. Measures whether analysts catch fraud faster than the previous workflow.
