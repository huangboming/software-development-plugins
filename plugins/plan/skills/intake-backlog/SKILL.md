---
name: intake-backlog
description: "Capture new requirements and add them to the product backlog. Triggers: 'new requirement', 'feature request', 'customer feedback', 'capture this requirement', 'intake', 'triage', 'add to backlog', 'update backlog', 'update backlog item', '/intake-backlog'."
---

# Intake & Add to Backlog

Capture incoming requirements from any source — customer feedback, stakeholder requests, support patterns, market signals — and add them to the product backlog.

## References

- [references/intake-template.md](references/intake-template.md) — Template for intake records (`docs/product/intakes/<slug>.md`) and field guidance. Read before writing an intake record.
- [references/triage-guide.md](references/triage-guide.md) — Elicitation questions, duplicate detection, assessment calibration, and batch intake handling. Read at the start of every intake.
- [references/backlog-template.md](references/backlog-template.md) — Template for the backlog document (`docs/product/backlog/backlog.md`). Read when creating or first updating the backlog.
- [references/item-quality-guide.md](references/item-quality-guide.md) — Backlog item quality standards: descriptions, sources, granularity checks. Read when adding items to the backlog.

## Process

1. Capture the requirement (intake)
2. Add/update backlog items

### Step 1: Capture the Requirement

Read [triage-guide.md](references/triage-guide.md) for elicitation questions and limits.

1. Read what the user has provided.
2. Identify what is already known (the what, who, and source).
3. Ask only for what is missing — 2-4 questions max in the first round.
4. If the user provides multiple requirements at once, acknowledge the batch and process each individually.

Stop gathering when the minimum viable intake is covered: what is the need, who has it, and where did it come from.

#### Check for Duplicates

Follow the duplicate detection process in [triage-guide.md](references/triage-guide.md). Compare by **underlying problem and user need**, not surface wording. If an exact duplicate is found, stop and surface it to the user before continuing.

#### Assess the Requirement

Using the triage guide's calibration aids:

- **Category:** Use the decision tree (new-capability / enhancement / pain-point / compliance / technical-enabler)
- **Rough size:** Use the heuristic signals (small-days / medium-weeks / large-months). Round up when uncertain.
- **Clarity:** Judge whether this is clear, partial, or vague

#### Write the Intake Record

Read [intake-template.md](references/intake-template.md) for the template and field guidance.

1. Create `docs/product/intakes/` if it does not exist.
2. Write the intake record at `docs/product/intakes/<slug>.md` where `<slug>` is a short kebab-case name derived from the requirement.
3. Fill all template sections. Leave Raw Notes empty if there is nothing to capture.

#### Present and Confirm

Present the intake record with a brief summary. Ask the user to confirm or correct before finalizing.

**Example:**

"Captured intake: **CSV export for reports** (`docs/product/intakes/csv-export.md`)

- **Requirement:** Users need to export report data as CSV — currently copy-pasting manually
- **Overlaps:** Related to 'Data export' in backlog (broader scope, this is a specific increment)
- **Assessment:** enhancement, small (days), clear

Any corrections before I finalize?"

For batch intakes, present a summary table after all items are processed:

```
| # | Intake | Category | Size | Clarity | Overlaps |
|---|--------|----------|------|---------|----------|
```

### Step 2: Add or Update Backlog Items

After the user confirms the intake, proceed directly to add the item to the backlog.

If the user's original request was to add directly to the backlog (e.g., "add X to the backlog"), skip the intake record and go directly to this step.

#### Locate or Create the Backlog

1. Check if `docs/product/backlog/backlog.md` exists.
2. If it exists, read it. If not, read [backlog-template.md](references/backlog-template.md) and create it.

#### Determine Action

| User Intent | Action |
|---|---|
| New item from intake or user description | **Add items** |
| "Update X", "change the description", "mark X as done" | **Update items** |
| Provides a PRD or requirement doc | **Add items** — extract candidate items |

#### Add Items

Read [item-quality-guide.md](references/item-quality-guide.md) for quality standards.

For each new item, capture:

| Field | Required | Description |
|-------|----------|-------------|
| **Item** | Yes | Short name (2-5 words) |
| **Description** | Yes | One sentence: what and why |
| **Source** | Yes | Where this came from — specific enough to trace back |
| **Status** | Auto | Set to `New` |
| **Added** | Auto | Today's date |

**Quality gate:** Check specificity, duplicates, and granularity before adding. See [item-quality-guide.md](references/item-quality-guide.md).

When extracting items from a PRD or requirement doc:
1. Pull each distinct feature or user story as a separate backlog item.
2. Use the document path as the Source (e.g., "Extracted from docs/product/prd/reporting/v2.md, user story #3").
3. Exclude implementation details, technical architecture, and test cases.

Present added items in a table and confirm before writing.

**Example:**

"I'll add these two items to the backlog:

| Item | Description | Source |
|------|-------------|--------|
| CSV export | Export reports as CSV — top customer request, eliminates manual copy-paste | Customer feedback — 12 requests in Q1 |
| Onboarding redesign | Simplify onboarding flow for new users — current flow has 40% drop-off | User feedback (this conversation) |

Any changes before I write them?"

#### Update Items

1. Identify the item(s) to update by name or description.
2. Apply the change (description, status, source).
3. Update "Last updated" on the backlog doc.

Status lifecycle: `New` → `Ready` → `In Progress` → `Done` (or `New` → `Dropped`). See [backlog-template.md](references/backlog-template.md) for definitions and transition criteria.

## Edge Cases

If the user describes a solution instead of a problem ("we need a dropdown for X"):
  → Acknowledge the solution idea. Ask what problem it solves. Capture the need in the intake, note the proposed solution in Raw Notes.

If the requirement is too vague to assess:
  → Ask 1-2 grounding questions. If still vague after one round, set clarity to `vague` and capture what exists.

If the user says "just capture it, don't ask questions":
  → Write the intake with what is available. Set clarity to `partial` or `vague`. Note gaps in Raw Notes.

If an existing intake record with the same slug already exists:
  → Append a date suffix: `<slug>-YYYY-MM-DD.md`.

If an item duplicates an existing backlog entry:
  → Surface the existing item. Ask whether to merge (combine descriptions and sources) or keep separate (clarify the distinction).

If the backlog mixes granularity levels (epics alongside stories):
  → Normalize before adding. Either break epics into stories, or note the inconsistency and ask the user how to proceed.
