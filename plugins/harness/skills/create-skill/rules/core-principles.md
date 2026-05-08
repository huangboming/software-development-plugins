# Core Principles for Skill Authoring

Hard rules. Apply on every line of every skill.

## Radical minimalism

A skill earns its tokens by encoding what Claude does *not* already know. Generic coding advice, restatements of training, and catalogs of public best-practice dilute signal.

Before keeping any line, ask the **four signal-to-noise tests:**

1. **Justification** — Would Claude handle this incorrectly without this line? If no, cut.
2. **Duplication** — Does this exist elsewhere in the skill (or in CLAUDE.md, or in this file's frontmatter)? If yes, keep one copy.
3. **Example** — Can a concrete example replace this explanation? If yes, prefer the example.
4. **Knowledge** — Does Claude already know this from training? If yes, cut.

**Procedural skill SKILL.md ≤ 30–40 lines.** Past that, content belongs in `rules/`, `workflows/`, or `references/` — or it's not earning its keep.

## Decay-vs-read test for keep / drop / slim

A skill earns its place by being read more often than its content decays. For each skill or sub-file:

- **High read, low decay** — keep. (Stable conventions, frontmatter contracts, gotchas that don't move.)
- **Low read, high decay** — drop. (Catalogs of "current best practices," lists of public reference products, anything that goes stale faster than it gets consulted.)
- **High read, high decay** — slim aggressively and link to a moving source instead of mirroring it.

When uncertain, drop. A missing skill is a smaller cost than a misleading one.

## Write-skill purity

`write-*` and `create-*` skills emit artifacts. They do not interview, grill, debate, or deliberate. Interrogation is a separate skill (`grill-me`). Mixing the two produces a skill that won't fire when the user wants pure emission, and won't ask enough questions when they want alignment.

If a skill's intake feels like it needs a long Q&A, that Q&A belongs upstream of this skill, not inside it.

## Push Claude off its defaults

A skill's most valuable lines are the surprising ones — non-obvious gotchas, internal conventions that contradict community defaults, opinions that override Claude's usual taste.

If every line of a skill could have been derived from "use sensible defaults," the skill is paying tokens for nothing.

## Set degrees of freedom deliberately

- **Numbered steps + scripts** — fragile sequences where consistency is critical.
- **Prose guidance** — judgment-heavy tasks where multiple approaches are valid.

Don't railroad a flexible task with rigid steps; don't prose-describe a fragile sequence. Match the form to the fragility.
