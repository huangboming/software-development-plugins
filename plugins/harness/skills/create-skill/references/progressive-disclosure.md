# Progressive Disclosure

Skills use a three-level loading system to manage context efficiently.

## The Three Levels

1. **Metadata (name + description)** — Always in context (~100 words). Used by Claude to decide whether to trigger the skill.
2. **SKILL.md body** — Loaded when the skill triggers. Target: under 500 lines.
3. **Bundled resources** (scripts, references, assets) — Loaded or executed on demand. Effectively unlimited in size, because scripts run without loading and references load only when needed.

## Key Principle

When a skill supports multiple variations, frameworks, or options, keep only the core workflow and selection guidance in SKILL.md. Move variant-specific details (patterns, examples, configuration) into separate reference files.

**The justification test at this level:** "If 90% of invocations don't need this content, why is it in SKILL.md?" If it's needed infrequently, move it to a reference and link it.

## Three Disclosure Patterns

See `references/progressive-disclosure-patterns.md` for full worked examples of:

- Pattern 1: High-level guide with references (core workflow + optional deep-dives)
- Pattern 2: Domain-specific organization (references split by domain/framework/provider)
- Pattern 3: Conditional details (common-case inline, advanced-case linked)

## Guidelines

- **Avoid deeply nested references.** Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md so Claude can find them without traversing a tree.
- **Structure longer reference files.** For files longer than 100 lines, include a table of contents at the top so Claude can see the full scope when previewing.
- **Unreferenced files are invisible.** Every file in `references/`, `rules/`, or `workflows/` should be mentioned by name and purpose in SKILL.md (or in the workflow that routes to it). A file Claude doesn't know exists will never be loaded.
