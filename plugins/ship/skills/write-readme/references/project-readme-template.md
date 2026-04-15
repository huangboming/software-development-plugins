# Project README Template

For applications, services, tools, and CLIs. Audience: end users and contributors.

```markdown
# <Project Name>

<One-sentence description: what it does, for whom, and what makes it distinct.>

<!-- Badges: 2-4 max. CI status, version, license. -->

<!-- Screenshot or GIF here if the project has a UI. Place above the fold. -->

## About

<2-4 sentences expanding on the description. What problem does this solve? Why does it exist? What's the key insight or approach?>

## Features

- <Feature 1 — lead with the user benefit>
- <Feature 2>
- <Feature 3>

## Getting Started

### Prerequisites

- <Runtime and version, e.g., "Node.js 18+">
- <Required tools, e.g., "Docker" or "PostgreSQL 15+">
- <OS requirements if any>

### Installation

<Single-command happy path first. Then platform variants if needed.>

## Quick Start

<5-15 lines of code or commands that produce visible output. Show expected output.>

## Usage

<Key usage patterns beyond the quick start. Link to full docs for detailed reference.>

### Configuration

<Table of key options, environment variables, or config file settings. Reference a separate doc for complex config.>

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<option>` | `<type>` | `<default>` | <what it controls> |

## Architecture

<Brief overview of how the project is structured. 3-5 sentences or a diagram. Link to docs/development/architecture/ for details. Omit for simple projects.>

## Contributing

<How to set up a dev environment, run tests, and submit changes. Link to CONTRIBUTING.md if it exists.>

## License

<License name. e.g., "MIT" or "Licensed under Apache 2.0. See [LICENSE](LICENSE).">

## Acknowledgements

<Credits, inspirations, major dependencies. Omit if not applicable.>
```

## Section Guidance

**Omit sections that don't apply** — not every project needs Architecture or Acknowledgements. The template is a menu, not a checklist.

**Section ordering is intentional:**
1. Name + description + badges + visual → "What is this?"
2. About + Features → "Should I care?"
3. Getting Started + Quick Start → "How do I try it?"
4. Usage + Configuration → "How do I use it for real?"
5. Architecture + Contributing → "How do I contribute?"
6. License → Legal clarity

**Adapt to project complexity:**
- Simple CLI tool: skip Architecture, trim Configuration
- Complex service: expand Getting Started with environment setup, add Architecture
- Monorepo: add a "Repository Structure" section after About
