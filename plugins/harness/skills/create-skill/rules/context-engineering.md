# Context Engineering for Skills

Context engineering is the discipline of curating what information occupies the context window and when. For skills, this means deciding what goes in SKILL.md (always loaded), bundled resources — `rules/`, `workflows/`, `references/` (on-demand), `scripts/` (executed without reading), and `assets/` (used without reading).

## The Core Principle

Context is a finite resource with diminishing marginal returns. More tokens does not mean better results — research shows that the "Maximum Effective Context Window" is drastically smaller than the nominal window size (by as much as 99% in some tasks), because model attention degrades as irrelevant tokens accumulate. The goal is to minimize tokens while maximizing signal.

**Every token has an opportunity cost.** A token spent on redundant explanation is a token not available for the user's actual request, conversation history, or other tools' output.

## Four Strategies for Managing Context

### 1. Store — Persist Outside the Context Window

Bundle information in the skill so it's available but not always loaded. Separate by content shape:

- **rules/** — Imperative constraints loaded when Claude needs to enforce invariants. Moderate context cost, paid only when used.
- **workflows/** — Ordered procedures loaded when Claude executes a specific task. Moderate context cost, paid only when used.
- **references/** — Explanatory material loaded when Claude needs domain knowledge. Moderate context cost, paid only when used.
- **scripts/** — Deterministic code that can be executed without reading into context. Zero context cost, full reliability.
- **assets/** — Templates, images, boilerplate used in output. Zero context cost — Claude uses these files without reading them.

**When to store externally:** When the information is needed for some tasks but not all, or when it's large enough that its token cost outweighs the benefit of always having it available.

### 2. Retrieve — Pull In Just-in-Time

Design skill content so Claude can retrieve what it needs, when it needs it:

- File descriptions in SKILL.md act as an index. Claude reads these descriptions to decide what to load.
- Directory names (`rules/`, `workflows/`, `references/`) signal content shape — Claude knows a rule file contains constraints, a workflow file contains steps.
- File names serve as navigation signals — Claude sees the file name before deciding to open it. `references/aws-deployment.md` is more discoverable than `references/guide-3.md`.
- Section headers within files enable Claude to scan and locate relevant content without reading the entire file.

**The skill architecture is inherently a hybrid retrieval system:** SKILL.md body is pre-loaded (stable, always-needed content), while `rules/`, `workflows/`, and `references/` enable just-in-time retrieval (dynamic, variant-specific content). Pre-load what's small and always relevant, retrieve everything else on demand.

**When to retrieve:** When content is domain-specific, variant-specific, or only relevant to certain user requests. This is the default strategy for most bundled resource files.

### 3. Compress — Maximize Information Density

Keep loaded content lean and high-signal:

- Move variant-specific details from SKILL.md to bundled resource files. The body should contain only the core workflow and selection guidance.
- Replace verbose explanations with concise examples. Examples communicate format, style, and reasoning in fewer tokens than prose descriptions.
- Use scripts instead of inline code blocks when the same code would be reproduced across sessions. A `scripts/validate.py` file costs zero context tokens; a 50-line code block in SKILL.md costs ~200 tokens every time the skill loads.
- Omit what Claude already knows. General programming concepts, standard library usage, and common tool syntax don't need to be in the skill.

**When to compress:** Always. Compression is not a one-time optimization — revisit loaded content regularly and ask: "Is every line earning its token cost?"

### 4. Isolate — Scope Context Per Agent

For skills that delegate work to sub-agents, each agent should receive only the context relevant to its specific task:

- A code review skill might spawn one agent per file or concern, each with only the relevant code and criteria.
- A research skill might spawn agents for different topics, each with only the relevant domain context.
- Sub-agents return condensed summaries (not full conversation history) to the orchestrating skill.

**When to isolate:** When a skill handles multiple independent concerns, works with large codebases, or delegates to parallel sub-agents.

## Context Allocation Decision Framework

Use this decision tree when placing content:

| Content Type | Where it Goes | Why |
|-------------|---------------|-----|
| Core workflow (always needed, <50 lines) | SKILL.md body | Loaded once, guides every invocation |
| Imperative constraints ("you must do X") | rules/ | Loaded when enforcing invariants |
| Ordered procedures ("do step 1, then 2") | workflows/ | Loaded when executing a specific task |
| Explanatory material ("X happens because Y") | references/ | Loaded only for relevant requests |
| Deterministic, repeatable code | scripts/ | Executed without reading into context |
| Output templates, boilerplate files | assets/ | Used without reading into context |
| General knowledge Claude already has | Nowhere | Wastes tokens without adding value |

**The 50-line rule of thumb:** If a section of SKILL.md exceeds ~50 lines and applies to only a subset of use cases, it should be a bundled resource file. The few tokens spent describing it in SKILL.md save the many tokens of loading it when it's not needed.

## Designing Bundled Resources for Efficient Retrieval

Bundled resource files (`rules/`, `workflows/`, `references/`) are only useful if Claude knows they exist and can find the right content within them. Design for discoverability:

### File Naming

File names are the first thing Claude sees. Make them descriptive:

| Weak | Strong |
|------|--------|
| `guide.md` | `python-scaffold-guide.md` |
| `reference.md` | `api-design-patterns.md` |
| `notes.md` | `database-schema.md` |

### File Descriptions in SKILL.md

The description next to each file link in SKILL.md is Claude's "index entry." It should answer two questions:
1. **What** does this file contain?
2. **When** should Claude read it?

```markdown
## File Index

- `rules/api-conventions.md` — API naming and versioning constraints.
  Read on every invocation that touches API endpoints.
- `workflows/deploy-release.md` — Step-by-step release deployment procedure.
  Read when the user asks to deploy or release.
- `references/python-scaffold-guide.md` — Python-specific project structure
  and tooling configuration. Read when the user selects Python.
```

### Internal Structure

For files over 100 lines, include a table of contents at the top so Claude can see the full scope when previewing. Use clear section headers that describe the content, not just label it.

For files over 10k words, include grep search patterns in SKILL.md so Claude can search without loading the entire file:

```markdown
- **API documentation**: See references/api-docs.md. For specific endpoints,
  grep for `## GET /` or `## POST /` patterns.
```

### One Topic Per File

Don't bundle unrelated content in a single file. If a file covers both "deployment patterns" and "testing strategies," split it. This allows Claude to load only the relevant topic.

## Maximizing Signal-to-Noise Ratio

Apply these tests to every piece of content in your skill:

1. **The justification test:** "Would Claude handle this incorrectly without this information?" If no, cut it.
2. **The duplication test:** "Does this information exist elsewhere in the skill?" If yes, keep it in one place only.
3. **The example test:** "Can I replace this explanation with a worked example?" If yes, the example likely communicates more in fewer tokens.
4. **The knowledge test:** "Does Claude already know this?" General programming, standard libraries, and well-known tools don't need documentation in a skill.
5. **The front-loading test:** "Is the most critical information near the top?" Models pay more attention to the beginning and end of context — bury nothing important in the middle.

## Context Anti-Patterns

Avoid these common mistakes:

- **Context stuffing** — Loading everything "just in case" rather than making content available on-demand. The skill body should be lean; bundled resources handle the depth.
- **Orphaned files** — Files in `rules/`, `workflows/`, or `references/` with no description in SKILL.md. If Claude doesn't know a file exists, it will never load it.
- **Mixed content shapes** — Combining imperative constraints, ordered procedures, and explanatory material in one directory. Separate by shape: `rules/`, `workflows/`, `references/`.
- **Bundled topics** — Combining unrelated topics in one file, forcing Claude to load irrelevant content to access what it needs.
- **Inline code that should be scripts** — Large code blocks in SKILL.md that are executed the same way every time. Move them to scripts/ for zero context cost.
- **Duplicated content** — The same information in both SKILL.md and a bundled resource file. When it drifts, Claude gets conflicting signals.
- **Explaining the obvious** — Documenting standard tool usage, common programming patterns, or basic concepts that Claude handles natively.
- **Context confusion** — Mixing instructions, data, and examples without clear structural separation (headers, code blocks, delimiters). When Claude can't distinguish what is an instruction from what is example data, behavior becomes unpredictable.
