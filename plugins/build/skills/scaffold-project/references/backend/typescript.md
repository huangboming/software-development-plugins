# TypeScript Backend Scaffold

## Package Manager: pnpm

Initialize with `pnpm init`, then customize `package.json`.

## Project Structure

```
<project-name>/
├── src/
│   └── index.ts
├── tests/
│   └── health.test.ts
├── package.json
├── tsconfig.json
├── eslint.config.mjs
├── Makefile
├── .gitignore
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
└── CLAUDE.md
```

## package.json

```json
{
  "name": "<project-name>",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "format": "prettier --write 'src/**/*.ts' 'tests/**/*.ts'",
    "lint": "eslint 'src/**/*.ts' 'tests/**/*.ts'",
    "test": "vitest run",
    "check": "pnpm lint && pnpm test"
  },
  "dependencies": {
    "hono": "^4.0.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "eslint": "^9.0.0",
    "@eslint/js": "^9.0.0",
    "typescript-eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.7.0",
    "vitest": "^2.0.0"
  }
}
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

## eslint.config.mjs

```javascript
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    ignores: ["dist/", "node_modules/"],
  }
);
```

## Makefile

```makefile
.PHONY: install dev format lint test check

install:
	pnpm install

dev:
	pnpm dev

format:
	pnpm format

lint:
	pnpm lint

test:
	pnpm test

check: lint test
```

## .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files
      - id: detect-private-key
  - repo: local
    hooks:
      - id: lint
        name: eslint
        entry: pnpm lint
        language: system
        pass_filenames: false
      - id: format-check
        name: prettier
        entry: pnpm format
        language: system
        pass_filenames: false
```

## .gitignore

```
node_modules/
dist/
.env
*.log
coverage/
```

## .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "pnpm"
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm format --check
      - run: pnpm test
```

## src/index.ts

```typescript
import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) => {
  return c.json({ status: "ok" });
});

serve({ fetch: app.fetch, port: 8080 }, (info) => {
  console.log(`listening on http://localhost:${info.port}`);
});
```

Note: add `@hono/node-server` to dependencies:
```json
"dependencies": {
  "hono": "^4.0.0",
  "@hono/node-server": "^1.0.0"
}
```

## tests/health.test.ts

```typescript
import { describe, expect, it } from "vitest";
import { Hono } from "hono";

const app = new Hono();

app.get("/health", (c) => {
  return c.json({ status: "ok" });
});

describe("health", () => {
  it("returns ok", async () => {
    const res = await app.request("/health");
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ status: "ok" });
  });
});
```

## CLAUDE.md

```markdown
# CLAUDE.md

## Commands

\```bash
make install    # Install dependencies
make dev        # Start dev server (auto-reload via tsx)
make format     # Format with prettier
make lint       # Lint with eslint
make test       # Run tests with vitest
make check      # Run lint + test
\```

## Architecture

TypeScript backend using Hono, eslint for linting, prettier for formatting, vitest for testing.

\```
src/
  index.ts      # Entry point, routing, handlers
tests/
  health.test.ts
\```
```
