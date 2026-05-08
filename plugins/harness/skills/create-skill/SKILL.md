---
name: create-skill
description: "Create or update a Claude Code skill. Triggers: 'create a skill', 'write a skill', 'add a skill for...', 'turn this into a skill', '/create-skill'."
---

# Skill Creator

Before starting, read `references/skill-anatomy.md` (folder shape, frontmatter contract, loading model). Skip any step below that manifestly doesn't apply (e.g., iterating on an existing skill).

## Principles

Apply to every line of every skill:

- **Push Claude off defaults.** A skill's value is in surprising lines — gotchas, opinions, conventions that contradict community defaults. If every line could be derived from "use sensible defaults," the skill is paying tokens for nothing.
- **Four signal-to-noise tests.** Cut a line unless (1) Claude would handle this incorrectly without it, (2) it's not duplicated elsewhere or in CLAUDE.md, (3) a concrete example wouldn't replace it, (4) Claude doesn't already know it from training.
- **Decay-vs-read.** A skill earns its place by being read more than its content decays. High-read + low-decay → keep. Low-read + high-decay → drop. High both → slim and link, don't mirror. When uncertain, drop.
- **Write-skill purity.** `write-*` and `create-*` skills emit artifacts; they don't interview, grill, or deliberate. Interrogation is a separate skill (`grill-me`). Q&A belongs upstream.
- **Match form to fragility.** Numbered steps for fragile sequences; prose for judgment tasks. Don't railroad flexible work; don't prose-describe fragile work.
- **SKILL.md ≤ 30–40 lines when there's content to defer to.** If a bundled file would always load anyway, inline it — a directory holding one always-loaded file is ceremony.

## 1. Plan resources

Imagine running this skill on 2–3 concrete invocations. For each, identify what would help on every repeat: code, schemas, templates, hard rules, ordered procedures. Map each to a directory using `references/skill-anatomy.md`. Skip a directory entirely if nothing fits — don't invent content to fill it.

Output: a short list of bundled resources to write.

## 2. Initialize

Create the skill directory and a SKILL.md from this template:

```bash
mkdir -p path/to/<skill-name> && cat > path/to/<skill-name>/SKILL.md <<'EOF'
---
name: <skill-name>
description: "TODO — one paragraph covering (1) what the skill does and (2) specific trigger phrases or contexts that should activate it; this is the routing signal, not a summary"
---

# <Skill Title>

[TODO: 1-2 sentences on what this skill enables.]

## [TODO: first main section]

[TODO: replace with the skill's core content. Keep SKILL.md short and promote detail to references/ as needed.]

## Gotchas

[TODO: capture specific failure modes — wrong defaults, footguns, surprising edge cases — as they emerge. Start empty or with known issues.]
EOF
```

Create only the resource subdirectories (`rules/`, `workflows/`, `references/`, `scripts/`, `assets/`) identified in step 1.

## 3. Build

Build order:

1. **Bundled resources first** — scripts, references, assets. Run scripts to confirm they work.
2. **SKILL.md last** — by then the resource inventory is concrete and can be indexed precisely.

While writing SKILL.md, apply the four signal-to-noise tests to every line.

For each bundled file: write its index entry — `path/to/file.md — what it contains. Read when X.`

## 4. Self-review

Walk SKILL.md and each bundled file once through these checks:

- Does the `description` open with one imperative sentence and list 3+ concrete trigger phrases?
- Is every line in SKILL.md justified by the four signal-to-noise tests?
- Does every file under `rules/`, `workflows/`, `references/` have an index entry naming *what* and *when*?
- Are there any "you should consider…" or "try to…" weasel phrases? Replace with imperatives.
- Does every conditional (`if X then Y`) have its `otherwise Z` or explicit "otherwise proceed"?

Validate with `claude plugin validate plugins/<plugin>`. Fix what fails. Don't ship known violations.

## Gotchas

- **Unreferenced files are invisible** — every file in `rules/`, `references/`, `scripts/`, `assets/` must have an index entry in SKILL.md.
- **Never mix content shapes in one directory** — imperatives in `rules/`, descriptive material in `references/`. (`workflows/` is the same idea but is rarely worth its own file — see Principles.)
- **Returning to a skill mid-session doesn't re-trigger routing** — if a new task arrives in the same conversation, re-read SKILL.md before acting; otherwise Claude may run on stale context.
