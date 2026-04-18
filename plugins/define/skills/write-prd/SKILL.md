---
name: write-prd
description: "Generate product-level or feature-level PRDs. For standalone backlog-ready user stories after the PRD exists, use write-user-story. Triggers: 'write a PRD', 'create a product spec', 'spec out this feature', 'I need a PRD for...', 'collect requirements', 'write requirements', 'draft user stories as part of the spec', 'document requirements from code', '/write-prd'."
---

# PRD Writer

## References

- [references/product-prd-template.md](references/product-prd-template.md) — Template for product-level PRDs (`.product/define/specs/prd.md`). Read when drafting a product-level PRD.
- [references/feature-prd-template.md](references/feature-prd-template.md) — Template for feature-level PRDs (`.product/define/specs/<feature-name>/v<N>.md`). Read when drafting a feature-level PRD.
- [references/writing-guide.md](references/writing-guide.md) — Working Backwards approach, user story and acceptance criteria guidance, SMART metrics, quality checklists. Read before drafting (Step 3) and during review (Step 4).
- [references/codebase-exploration.md](references/codebase-exploration.md) — Exploration priority order and code-pattern-to-requirement translation table. Read only for the **Codebase Exploration** workflow.

## Process

PRD creation involves these steps:

1. Determine **PRD level** and **workflow**
2. Gather information (conversation, synthesis, or code exploration)
3. Draft the PRD
4. Verify and present to the user

### Step 1: Determine PRD Level and Workflow

**PRD level:**

- User describes a product initiative, multi-feature effort, or asks for a "product PRD" → **Product-level PRD** (output: `.product/define/specs/prd.md`)
- User describes a specific feature, or asks to "spec out this feature" → **Feature-level PRD** (output: `.product/define/specs/<feature-name>/v1.md`)
- If ambiguous, ask: "Is this a product-level spec covering the full initiative, or a feature-level spec for one specific capability?"

**Versioning (feature-level PRDs):**

- New feature with no existing PRD → create `.product/define/specs/<feature-name>/v1.md`
- Revising an existing PRD (significant scope change, pivot, or post-launch rethink) → check `.product/define/specs/<feature-name>/` for existing versions, create the next version (`v2.md`, `v3.md`, etc.). Add a `Supersedes` link to the previous version. Do not modify previous versions.
- Minor edits (typos, clarifications, updating status) → edit the current version in place.

**Workflow:**

- User describes an idea, concept, or rough vision → **Conversational Elicitation** (Step 2a)
- User provides existing artifacts (requirement docs, user stories, notes, feedback) → **Synthesis** (Step 2b)
- User asks to document what existing code does, extract requirements from a codebase, or points to a specific module → **Codebase Exploration** (Step 2c — feature-level PRDs only)
- Mixed input (some ideas + some existing docs) → combine approaches as needed.

### Step 2a: Conversational Elicitation

#### Initial Understanding

1. Read whatever the user has provided (description, notes, context).
2. Restate the core idea in one sentence to confirm understanding.
3. Propose a name for the PRD and confirm.

#### Clarifying Questions

Ask 2-4 questions per round. Prioritize by what blocks progress most. Frame questions around these areas:

**For product-level PRDs:**

| Area | Ask About |
|------|-----------|
| Problem | What specific customer pain? Who experiences it? What do they do today? |
| Vision | When this is done, what's different for the customer? |
| Scope | What's the boundary? What are we explicitly *not* building? |
| Users | Who are the distinct user types? How do their needs differ? |
| Features | Key capabilities? Which are must-haves vs. nice-to-haves? |
| Success | How will we know this worked? |
| Risks | What could derail this? What are we uncertain about? |

**For feature-level PRDs:**

| Area | Ask About |
|------|-----------|
| Problem | What user problem does this feature solve? |
| Scope | What's in vs. out? |
| Who | What user roles interact with this feature? |
| Behavior | What does the user do and see? Key flows? What are the inputs and outputs? |
| Edge cases | What happens when things go wrong? Empty states? Limits? |
| Dependencies | Does this depend on other features or external services? |
| Metrics | How will we measure impact? |

**Transition to drafting** when the problem, scope, and key features/behaviors are clear. Remaining unknowns become open questions.

Proceed to Step 3.

### Step 2b: Synthesis from Existing Artifacts

1. Read all provided artifacts. Check for existing documents at `.product/define/specs/` that relate to this product/feature.
2. Extract and organize:
   - **Problem signals** — pain points, user complaints, motivations mentioned across artifacts
   - **Feature/capability inventory** — what's described or implied
   - **Personas** — user roles mentioned
   - **Constraints and non-goals** — scope boundaries stated or implied
   - **Open questions** — contradictions, gaps, ambiguities across artifacts
3. Present a brief summary of what was extracted and ask the user to confirm or correct before drafting.
4. Ask 1-2 targeted follow-up questions for critical gaps (e.g., missing success metrics, unclear personas).

Proceed to Step 3.

### Step 2c: Codebase Exploration (Feature-Level PRDs Only)

Read [references/codebase-exploration.md](references/codebase-exploration.md) for exploration priority order and the code-pattern-to-requirement translation table.

#### Explore

1. Ask the user which part of the codebase to analyze, or identify the feature boundary from the directory/module they point to.
2. Read entry points, data models, and tests first — these reveal the most about intended behavior.
3. Trace user-facing flows end-to-end. Note validation rules, error handling, and business logic.
4. Translate code patterns into user-facing requirements using the translation table. Express every finding from the user's perspective.

#### Synthesize

1. Group discovered behaviors into logical user stories — each representing a coherent user-facing capability.
2. Distinguish between what the code **does** and what it **should do**. Record apparent bugs or incomplete features as open questions, not requirements.
3. Strip all implementation details. The output should read as if written by a product manager who has never seen the code.
4. Present a summary of discovered requirements to the user for validation before drafting.

Proceed to Step 3.

### Step 3: Draft the PRD

Read the appropriate template and [references/writing-guide.md](references/writing-guide.md).

1. Create the PRD at the appropriate path:
   - Product-level: `.product/define/specs/prd.md`
   - Feature-level: `.product/define/specs/<feature-name>/v<N>.md` (use `v1.md` for new PRDs; increment version when revising an existing PRD)
2. Fill each section following the writing guide. The two sections most commonly written poorly are problem statement and non-goals — calibrate quality using these examples:

   **Problem statement** — start with the customer pain, not the solution:

   | Weak | Strong |
   |------|--------|
   | "We need a dashboard to display analytics data." | "Marketing managers spend 2+ hours each Monday manually compiling performance data from three tools, often missing trends because data is stale by the time they finish." |

   **Non-goals** — list things a reader would *reasonably assume* are included:

   | Weak | Strong |
   |------|--------|
   | "Not building a mobile app" | "Real-time collaboration — initial version is single-user; we'll evaluate based on adoption data in Q3" |
3. For feature-level PRDs: write full user stories with acceptance criteria inline. For standalone backlog-ready stories (one file per story under `.product/define/stories/<feature>/`), the user can follow up with `write-user-story` after the PRD is drafted — that skill formalizes and grain-checks the inline stories rather than inventing a parallel set.
4. Add a Mermaid flowchart for multi-step user flows in feature-level PRDs.
5. For product-level PRDs: list features with priorities (must-have / should-have / nice-to-have). Note which features have or need their own feature-level PRDs.
6. Capture unresolved questions in Open Questions. State assumptions explicitly.
7. Set "Last updated" to today's date.

### Step 4: Review, Revise, and Present

1. Review the draft against the quality checklist in [references/writing-guide.md](references/writing-guide.md). Check specifically:
   - Problem statement names a specific persona and a specific pain — not generic "users need X"
   - Non-goals would genuinely surprise someone reading the PRD for the first time
   - Every success metric has a definition, target, and timeframe
   - User stories use specific roles and real benefits (feature-level PRDs)
   - Each acceptance criterion is independently testable — it should pass or fail unambiguously (feature-level PRDs)
   - Zero implementation details — no technologies, architecture, or system internals
   - Mermaid diagrams use valid syntax (feature-level PRDs only)
2. Revise the draft to fix any issues found. Do not present a draft that fails the checklist.
3. Present the final PRD to the user and ask for feedback.

## Edge Cases

If the user provides contradictory goals or requirements:
  → Surface the contradiction explicitly. Ask which direction is intended, and move the other to non-goals.

If success metrics can't be defined (no data, no baseline):
  → Write "TBD — measure baseline before launch" and add an open question about instrumentation.

If the scope is too large for a single product PRD (more than ~8 features):
  → Propose splitting into sub-initiatives, each with its own product PRD. Confirm with the user.

If a feature-level PRD has too many user stories (more than ~10):
  → Propose splitting into sub-features, each with its own feature-level PRD. Confirm with the user.

If the user asks for a single feature and a product-level PRD doesn't exist yet:
  → Write the feature-level PRD standalone. Note in the document that a parent product PRD may be created later.

If the user wants implementation details in the PRD:
  → Explain that PRDs capture *what* and *why* from the user's perspective. Suggest `write-architecture` for technical architecture decisions.

If a requirement is ambiguous and the user cannot clarify:
  → State the assumed interpretation in the Notes section of the affected story, and add an open question.

If extracting from a codebase with no tests or documentation:
  → Rely on entry points, validation logic, and error handling. Flag low-confidence inferences as open questions.
