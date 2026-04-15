# React + Vite Scaffold

## Table of Contents

1. [Package Manager](#package-manager-pnpm)
2. [Project Structure](#project-structure)
3. [package.json](#packagejson)
4. [tsconfig.json](#tsconfigjson) / [tsconfig.app.json](#tsconfigappjson) / [tsconfig.node.json](#tsconfignodejson)
5. [vite.config.ts](#viteconfigts)
6. [vitest.config.ts](#vitestconfigts)
7. [playwright.config.ts](#playwrightconfigts)
8. [eslint.config.mjs](#eslintconfigmjs)
9. [.prettierrc](#prettierrc)
10. [Makefile](#makefile)
11. [Husky + lint-staged](#huskypre-commit)
12. [.gitignore](#gitignore)
13. [CI workflow](#githubworkflowsciyml)
14. [Source files](#indexhtml) (index.html, main.tsx, App.tsx, index.css)
15. [Test files](#srctestsetupts) (setup.ts, App.test.tsx, home.spec.ts)
16. [CLAUDE.md](#claudemd)

---

## Package Manager: pnpm

Initialize with `pnpm init`, then customize `package.json`.

## Project Structure

```
<project-name>/
├── src/
│   ├── App.tsx
│   ├── App.test.tsx
│   ├── index.css
│   ├── main.tsx
│   └── test/
│       └── setup.ts
├── e2e/
│   └── home.spec.ts
├── public/
│   └── vite.svg
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── vite.config.ts
├── vitest.config.ts
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
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "lint": "eslint .",
    "format": "prettier --write 'src/**/*.{ts,tsx,css}' '*.{json,mjs,ts}'",
    "test": "vitest run",
    "test:e2e": "playwright test",
    "check": "pnpm lint && pnpm test",
    "prepare": "husky"
  },
  "dependencies": {
    "react": "^19.2.4",
    "react-dom": "^19.2.4"
  },
  "devDependencies": {
    "@playwright/test": "^1.58.2",
    "@tailwindcss/vite": "^4.2.1",
    "@testing-library/jest-dom": "^6.9.1",
    "@testing-library/react": "^16.3.2",
    "@types/react": "^19.2.4",
    "@types/react-dom": "^19.2.4",
    "@vitejs/plugin-react": "^5.1.4",
    "eslint": "^9.39.3",
    "eslint-plugin-react-hooks": "^7.0.1",
    "globals": "^16.0.0",
    "husky": "^9.1.7",
    "lint-staged": "^15.5.0",
    "jsdom": "^26.0.0",
    "prettier": "^3.5.3",
    "prettier-plugin-tailwindcss": "^0.7.2",
    "tailwindcss": "^4.2.1",
    "typescript": "^5.9.3",
    "typescript-eslint": "^8.56.1",
    "vite": "^7.2.7",
    "vite-tsconfig-paths": "^5.0.0",
    "vitest": "^4.0.18"
  }
}
```

## tsconfig.json

```json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ]
}
```

## tsconfig.app.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedSideEffectImports": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"]
}
```

## tsconfig.node.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2023"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "strict": true,
    "skipLibCheck": true,
    "types": ["node"]
  },
  "include": ["vite.config.ts", "vitest.config.ts", "playwright.config.ts"]
}
```

## vite.config.ts

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [react(), tailwindcss(), tsconfigPaths()],
})
```

## vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
  },
})
```

## playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
})
```

## eslint.config.mjs

Note: Pin to ESLint 9 — `eslint-plugin-react` is not yet compatible with ESLint 10.

```javascript
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import reactHooks from 'eslint-plugin-react-hooks'
import globals from 'globals'

export default tseslint.config(
  { ignores: ['dist/**'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    plugins: {
      'react-hooks': reactHooks,
    },
    languageOptions: {
      globals: { ...globals.browser },
    },
    rules: {
      ...reactHooks.configs['recommended-latest'].rules,
    },
  },
)
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
  "tailwindStylesheet": "./src/index.css"
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
  "*.{json,css,mjs}": ["prettier --write"]
}
```

## .gitignore

```
node_modules/
dist/
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

## index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title><project-name></title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

## src/main.tsx

```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

## src/index.css

```css
@import "tailwindcss";
```

## src/App.tsx

```tsx
export default function App() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900">
          <project-name>
        </h1>
        <p className="mt-2 text-gray-600">Edit src/App.tsx to get started.</p>
      </div>
    </main>
  )
}
```

## src/test/setup.ts

```typescript
import '@testing-library/jest-dom/vitest'
```

## src/App.test.tsx

```tsx
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders heading', () => {
    render(<App />)
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

## public/vite.svg

Copy the default Vite SVG favicon:

```svg
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--logos" width="31.88" height="32" preserveAspectRatio="xMidYMid meet" viewBox="0 0 256 257"><defs><linearGradient id="IconifyId1813088fe1fbc01fb466" x1="-.828%" x2="57.636%" y1="7.652%" y2="78.411%"><stop offset="0%" stop-color="#41D1FF"></stop><stop offset="100%" stop-color="#BD34FE"></stop></linearGradient><linearGradient id="IconifyId1813088fe1fbc01fb467" x1="43.376%" x2="50.316%" y1="2.242%" y2="89.03%"><stop offset="0%" stop-color="#FFBD4F"></stop><stop offset="100%" stop-color="#FF9640"></stop></linearGradient></defs><path fill="url(#IconifyId1813088fe1fbc01fb466)" d="M255.153 37.938L134.897 252.976c-2.483 4.44-8.862 4.466-11.382.048L.875 37.958c-2.746-4.814 1.371-10.646 6.827-9.67l120.385 21.517a6.537 6.537 0 0 0 2.322-.004l117.867-21.483c5.438-.991 9.574 4.796 6.877 9.62Z"></path><path fill="url(#IconifyId1813088fe1fbc01fb467)" d="M185.432.063L96.44 17.501a3.268 3.268 0 0 0-2.634 3.014l-5.474 92.456a3.268 3.268 0 0 0 3.997 3.378l24.777-5.718c2.318-.535 4.413 1.507 3.936 3.838l-7.361 36.047c-.495 2.426 1.782 4.5 4.151 3.78l15.304-4.649c2.372-.72 4.652 1.36 4.15 3.788l-11.698 56.621c-.732 3.542 3.979 5.473 5.943 2.437l1.313-2.028l72.516-144.72c1.215-2.423-.88-5.186-3.54-4.672l-25.505 4.922c-2.396.462-4.435-1.77-3.759-4.114l16.646-57.705c.677-2.35-1.37-4.583-3.769-4.113Z"></path></svg>
```

## CLAUDE.md

```markdown
# CLAUDE.md

## Commands

\```bash
make install    # Install dependencies
make dev        # Start Vite dev server
make build      # Type-check and build for production
make format     # Format with Prettier
make lint       # Lint with ESLint
make test       # Run unit tests with Vitest
make test:e2e   # Run E2E tests with Playwright
make check      # Run lint + test
\```

## Architecture

React SPA using Vite, TypeScript, Tailwind CSS v4, ESLint for linting, Prettier for formatting, Vitest + Testing Library for unit tests, Playwright for E2E tests.

\```
src/
  main.tsx       # Entry point
  App.tsx        # Root component
  App.test.tsx   # Component test
  index.css      # Tailwind entry
e2e/
  home.spec.ts   # E2E test
\```
```
