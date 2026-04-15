# README Writing Guide

## The One Rule

A README answers first-contact questions without becoming the full documentation. Every section earns its place by helping someone decide "is this for me?" and "how do I start?" If a section doesn't serve those questions, it belongs in linked docs.

## Writing for Two Audiences

### Project READMEs (Applications, Services, Tools)

**Reader's mindset:** "What does this do, and how do I run it?"

- Tone can be conversational and mission-driven — explain *why* this exists
- Lead with the problem being solved, not the technology stack
- Visual evidence (screenshots, GIFs) is high-value for anything with a UI
- Installation means "clone and run," not "install as a dependency"

### Library READMEs (Packages, Modules)

**Reader's mindset:** "Can I drop this into my code, and how?"

- Tone should be precise and reference-oriented — developers are evaluating, not being inspired
- Lead with what it does and how to install it
- The quick-start example is the conversion moment — it must work copy-paste
- Installation means `pip install x` or `npm install x`
- Link to full API docs rather than inlining them

## Tagline Formula

The one-line description is the highest-leverage sentence in the README.

**Pattern:** [What it is] + [primary capability] + [key differentiator or target context]

| Quality | Example |
|---------|---------|
| Weak | "A powerful and easy-to-use tool" |
| Weak | "MyProject" |
| Strong | "Fast, zero-dependency CSV parser for Node.js" |
| Strong | "CLI tool that generates database migrations from schema diffs" |

**Rules:**
- Write for someone who has never heard of the project
- Avoid hollow adjectives: "powerful," "simple," "easy," "amazing"
- Include: language/runtime, primary use case, key differentiator
- Test: read only the tagline — do you know what this does and whether it's for you?

## Badge Guidance

Badges are trust signals, not decoration.

**High-value badges** (use 2-4 at most):

| Badge | Why It Matters |
|-------|----------------|
| CI/build status | Shows the project is not broken |
| Version/latest release | Tells you what you'd get |
| License | Legal requirement for many evaluators |
| Code coverage | Proxy for test quality (libraries especially) |

**Avoid:**
- More than 4-5 badges — diminishing returns, visual clutter
- Badges for defunct services or broken links
- Decorative technology logos without functional information
- Badges that duplicate information in the text

Use [Shields.io](https://shields.io/) for visual consistency.

## Quick-Start Effectiveness

The quick-start is the "try before you buy" moment. Structure:

1. Prerequisites (one line if any: "Requires Node 18+")
2. Install command (exact, copy-pasteable)
3. Minimal working code (5-15 lines, produces visible output)
4. Expected output (show what success looks like)
5. Next step ("See examples/ for more" or "Read the full docs")

**Must pass these tests:**
- Works copy-paste with zero modification for the happy path
- No unresolved placeholders (`YOUR_API_KEY`) without explaining where to get them
- Shows expected output — the reader needs to know what "it worked" looks like
- Does not require reading another section first

| Quality | Example |
|---------|---------|
| Weak | "First, configure your environment, then..." |
| Weak | Code with `YOUR_TOKEN_HERE` and no setup instructions |
| Strong | Three commands: install → run → see output |

## Section Quality Benchmarks

### Project Name + Description

- One sentence. Answers "what is this?" for someone with zero context.
- No jargon unless the audience is guaranteed to know it.

### Installation

- Single-command happy path first, then platform variants.
- Explicitly list prerequisites (runtime version, OS, required tools).
- Never assume ecosystem knowledge ("just install the deps").

### Features

- Bulleted list of capabilities, not a paragraph.
- Each bullet stands alone — the reader is scanning.
- Lead with the user benefit, not the implementation.

### Configuration

- Table format for options (name, type, default, description).
- Environment variables grouped logically.
- Reference a separate config doc for complex setups.

### Contributing

- Tells newcomers exactly how to set up a dev environment and run tests.
- "PRs welcome" alone is not a contributing section.

### License

- One line, explicit. "MIT" or "Licensed under Apache 2.0."

## Screenshots and Demos

**Include when:**
- The project has a UI (web app, CLI, desktop app, dashboard)
- The output is visual (charts, generated files, design tools)
- A screenshot replaces 10 paragraphs of description

**Skip when:**
- The project is a pure library with no UI
- The screenshot is outdated
- Multiple screenshots show the same concept

**Best practices:**
- Place the most compelling visual immediately after the tagline/badges
- GIFs for CLI tools and interactive demos; screenshots for static UIs
- Keep GIFs under 15 seconds, cropped to the relevant area
- Store images in the repo, not hotlinked to external services

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| No description — just a title | Reader leaves immediately | Add a one-sentence tagline |
| "See the docs" with no quick-start | No reason to click through | Add a minimal working example |
| Full API reference inline | README becomes unusable | Link to hosted docs |
| Installation assumes expertise | "Just run `make`" skips 5 prereqs | List every prerequisite explicitly |
| Outdated screenshots | Erodes trust | Update or remove |
| Changelog in README | Buries the useful sections | Use CHANGELOG.md |
| Badge wall (10+ badges) | Visual noise, no signal | Keep 2-4 meaningful badges |
| No license | Legally ambiguous — some orgs can't use it | Always state the license |
| Marketing language without substance | "Revolutionary AI-powered platform" tells nothing | Describe what it actually does |
| Tutorial embedded in README | Too long, wrong place | Link to a tutorial doc |

## Quality Checklists

### Project README

- [ ] Title and one-sentence description — someone unfamiliar knows what this is
- [ ] Description explains the problem being solved, not just the solution
- [ ] Prerequisites listed explicitly (runtime, OS, required tools)
- [ ] Installation is copy-pasteable and works on a fresh machine
- [ ] Quick start produces visible output with no configuration
- [ ] Features are bulleted and scannable
- [ ] Screenshot or demo included (if the project has a UI)
- [ ] Contributing section explains dev setup and how to run tests
- [ ] License stated explicitly
- [ ] No stale information (version numbers, screenshots, links)
- [ ] Length is appropriate — all first-contact questions answered, details linked out

### Library README

- [ ] Package name and one-line functional description
- [ ] Installation command is the first actionable line
- [ ] Quick-start example works copy-paste immediately after install
- [ ] Expected output shown
- [ ] Key API surface documented or linked
- [ ] Compatibility/requirements stated (language versions, OS)
- [ ] Badges provide real signal (CI, version, coverage, license)
- [ ] Full API reference linked, not inlined
- [ ] License stated explicitly
- [ ] No stale information
