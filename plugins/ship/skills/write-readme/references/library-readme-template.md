# Library/Package README Template

For npm packages, PyPI libraries, Go modules, crates, etc. Audience: developers integrating the library.

```markdown
# <Package Name>

<!-- Badges: version, CI, coverage, license. These are trust signals on registries. -->

<One-line functional description. e.g., "Type-safe SQL query builder for TypeScript and JavaScript.">

## Installation

<Single install command. This is often the most important line in a library README.>

## Quick Start

<5-15 lines: import, configure (if needed), call, see output. Must work copy-paste immediately after install.>

**Output:**

<Show expected output so the reader knows it worked.>

## Features

- <What it supports>
- <What it supports>
- <What it does NOT support, if scope clarity helps evaluation>

## API Overview

<Brief orientation to the main classes, functions, or patterns. Not exhaustive — link to full reference.>

### <Primary Function/Class>

<3-5 line example with inline comments.>

### <Secondary Function/Class>

<3-5 line example.>

## Configuration

<Key options and their defaults. Table format.>

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<option>` | `<type>` | `<default>` | <what it controls> |

## Examples

<2-3 additional use case examples beyond quick start. Each with a brief description of the scenario.>

## Compatibility

- <Language/runtime versions supported>
- <OS requirements if any>
- <Peer dependencies if any>

## Documentation

<Link to full API reference, hosted docs, or wiki.>

## Contributing

<Brief guidance or link to CONTRIBUTING.md.>

## License

<License name. e.g., "MIT" or "Licensed under Apache 2.0. See [LICENSE](LICENSE).">
```

## Section Guidance

**Installation comes before everything else.** On registries (npm, PyPI, crates.io), the README *is* the product page. Developers evaluating the library want to see how to install it and a working example within 10 seconds.

**Quick Start is the conversion moment.** If a developer can't copy-paste a working example from the README, adoption drops. This section has the highest ROI of any section.

**API Overview is not API Reference.** Show the 2-3 most common entry points with examples. Link to the full reference for everything else. Inlining a full API reference makes the README unusable.

**Omit sections that don't apply:**
- No Configuration section if the library is zero-config
- No Compatibility section if it runs everywhere
- No Examples section if Quick Start covers the main use cases

**Adapt to ecosystem conventions:**
- npm packages: include `npx` usage if applicable, mention ESM/CJS support
- PyPI packages: note Python version support, mention type stub availability
- Go modules: show `go get` import path, note minimum Go version
- Rust crates: show `Cargo.toml` dependency and feature flags
