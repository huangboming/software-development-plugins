# Next.js Scaffold

## Table of Contents

1. [Package Manager](#package-manager-pnpm)
2. [Key Details](#key-details) (Next.js 16 specifics)
3. [Project Structure](#project-structure)
4. [package.json](#packagejson)
5. [next.config.ts](#nextconfigts)
6. [tsconfig.json](#tsconfigjson)
7. [postcss.config.mjs](#postcssconfigmjs)
8. [vitest.config.mts](#vitestconfigmts) / [vitest.setup.ts](#vitestsetupts)
9. [playwright.config.ts](#playwrightconfigts)
10. [eslint.config.mjs](#eslintconfigmjs)
11. [.prettierrc](#prettierrc)
12. [Makefile](#makefile)
13. [Husky + lint-staged](#huskypre-commit)
14. [.gitignore](#gitignore)
15. [CI workflow](#githubworkflowsciyml)
16. [Source files](#appglobalscss) (globals.css, layout.tsx, page.tsx)
17. [Test files](#apppagetesttsx) (page.test.tsx, home.spec.ts)
18. [CLAUDE.md](#claudemd)

---

## Package Manager: pnpm

Initialize with `pnpm init`, then customize `package.json`.

## Key Details

- Next.js 16 uses **Turbopack by default** for both `next dev` and `next build` — no `--turbopack` flag needed
- **`next lint` is removed** in v16 — run `eslint .` directly
- App Router is the default routing pattern
- Tailwind v4 uses CSS-first configuration via `@import "tailwindcss"` — no `tailwind.config.js`

## Project Structure

```
<project-name>/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── page.test.tsx
│   └── globals.css
├── e2e/
│   └── home.spec.ts
├── public/
│   └── favicon.ico
├── package.json
├── next.config.ts
├── tsconfig.json
├── postcss.config.mjs
├── vitest.config.mts
├── vitest.setup.ts
├── playwright.config.ts
├── eslint.config.mjs
├── .prettierrc
├── Makefile
├── .husky/
│   └── pre-commit
├── .lintstagedrc.json
├── .gitignore
├── .github/workflows/ci.yml
└── CLAUDE.md
```

## package.json

```json
{
  "name": "<project-name>",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint .",
    "format": "prettier --write 'app/**/*.{ts,tsx,css}' '*.{json,mjs,mts,ts}'",
    "test": "vitest run",
    "test:e2e": "playwright test",
    "check": "pnpm lint && pnpm test",
    "prepare": "husky"
  },
  "dependencies": {
    "next": "^16.1.6",
    "react": "^19.2.4",
    "react-dom": "^19.2.4"
  },
  "devDependencies": {
    "@playwright/test": "^1.58.2",
    "@tailwindcss/postcss": "^4.2.1",
    "@testing-library/jest-dom": "^6.9.1",
    "@testing-library/react": "^16.3.2",
    "@types/node": "^22.0.0",
    "@types/react": "^19.2.4",
    "@types/react-dom": "^19.2.4",
    "@vitejs/plugin-react": "^5.1.4",
    "eslint": "^9.39.3",
    "eslint-config-next": "^16.1.6",
    "eslint-config-prettier": "^10.1.0",
    "husky": "^9.1.7",
    "lint-staged": "^15.5.0",
    "jsdom": "^26.0.0",
    "prettier": "^3.5.3",
    "prettier-plugin-tailwindcss": "^0.7.2",
    "tailwindcss": "^4.2.1",
    "typescript": "^5.9.3",
    "vite-tsconfig-paths": "^5.0.0",
    "vitest": "^4.0.18"
  }
}
```

## next.config.ts

```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {}

export default nextConfig
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## postcss.config.mjs

Tailwind v4 for Next.js uses the PostCSS plugin (not the Vite plugin).

```javascript
const config = {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}

export default config
```

## vitest.config.mts

Note: Async React Server Components cannot be unit-tested with Vitest. Use Playwright for those. Vitest covers synchronous Server Components and all Client Components.

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    include: ['**/*.{test,spec}.{ts,tsx}'],
    exclude: ['e2e/**', 'node_modules/**', '.next/**'],
  },
})
```

## vitest.setup.ts

```typescript
import '@testing-library/jest-dom/vitest'
```

## playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test'

const PORT = process.env.PORT || 3000
const baseURL = `http://localhost:${PORT}`

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL,
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: process.env.CI ? 'pnpm build && pnpm start' : 'pnpm dev',
    url: baseURL,
    timeout: 120 * 1000,
    reuseExistingServer: !process.env.CI,
  },
})
```

## eslint.config.mjs

Note: Pin to ESLint 9 — `eslint-plugin-react` (used by `eslint-config-next`) is not yet compatible with ESLint 10.

```javascript
import { dirname } from 'path'
import { fileURLToPath } from 'url'
import { FlatCompat } from '@eslint/eslintrc'
import prettier from 'eslint-config-prettier'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const compat = new FlatCompat({
  baseDirectory: __dirname,
})

const eslintConfig = [
  ...compat.extends('next/core-web-vitals', 'next/typescript'),
  prettier,
]

export default eslintConfig
```

Note: add `@eslint/eslintrc` to devDependencies:

```json
"devDependencies": {
  "@eslint/eslintrc": "^3.0.0"
}
```

## .prettierrc

```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "all",
  "printWidth": 100,
  "plugins": ["prettier-plugin-tailwindcss"],
  "tailwindStylesheet": "./app/globals.css"
}
```

## Makefile

```makefile
.PHONY: install dev build format lint test test\:e2e check

install:
	pnpm install

dev:
	pnpm dev

build:
	pnpm build

format:
	pnpm format

lint:
	pnpm lint

test:
	pnpm test

test\:e2e:
	pnpm exec playwright install --with-deps chromium && pnpm test:e2e

check: lint test
```

## .husky/pre-commit

```bash
pnpm exec lint-staged
```

Note: Create the `.husky` directory and file. The file does not need a shebang — Husky v9 handles execution.

## .lintstagedrc.json

```json
{
  "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.{json,css,mjs,mts}": ["prettier --write"]
}
```

## .gitignore

```
node_modules/
.next/
out/
.env
*.log
coverage/
test-results/
playwright-report/
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
          version: 10
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "pnpm"
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm format --check
      - run: pnpm test
```

## app/globals.css

```css
@import "tailwindcss";
```

## app/layout.tsx

```tsx
import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '<project-name>',
  description: '<project-name>',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

## app/page.tsx

```tsx
export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900">
          <project-name>
        </h1>
        <p className="mt-2 text-gray-600">Edit app/page.tsx to get started.</p>
      </div>
    </main>
  )
}
```

## app/page.test.tsx

```tsx
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import Home from './page'

describe('Home', () => {
  it('renders heading', () => {
    render(<Home />)
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('<project-name>')
  })
})
```

## e2e/home.spec.ts

```typescript
import { test, expect } from '@playwright/test'

test('home page displays heading', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('<project-name>')
})
```

## CLAUDE.md

```markdown
# CLAUDE.md

## Commands

\```bash
make install    # Install dependencies
make dev        # Start Next.js dev server (Turbopack)
make build      # Build for production
make format     # Format with Prettier
make lint       # Lint with ESLint
make test       # Run unit tests with Vitest
make test:e2e   # Run E2E tests with Playwright
make check      # Run lint + test
\```

## Architecture

Next.js App Router with TypeScript, Tailwind CSS v4, ESLint for linting, Prettier for formatting, Vitest + Testing Library for unit tests, Playwright for E2E tests.

\```
app/
  layout.tsx      # Root layout
  page.tsx        # Home page
  page.test.tsx   # Component test
  globals.css     # Tailwind entry
e2e/
  home.spec.ts    # E2E test
\```
```
