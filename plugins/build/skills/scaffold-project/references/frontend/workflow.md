# Frontend Workflow

Use `pnpm` as the package manager.

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| framework | yes | — | `react` (React + Vite) or `nextjs` (Next.js App Router) |
| library | no | none | Component library: `shadcn`, `mantine`, `antd`, or `none` |

## Steps

1. If the user hasn't expressed a preference for component library, offer the choice: shadcn/ui, Mantine, Ant Design, or none.
2. Read the framework-specific reference for the complete project structure and every file to create:
   - **React + Vite**: See [react.md](react.md). Read when framework is `react`.
   - **Next.js**: See [nextjs.md](nextjs.md). Read when framework is `nextjs`.
3. Create all files as specified. Replace `<project-name>` with the actual project name.
4. If the user chose a component library, read the matching reference and apply its setup on top of the base scaffold:
   - **shadcn/ui**: See [shadcn.md](shadcn.md) — Radix UI primitives styled with Tailwind. Native Tailwind v4 support. Read when library is `shadcn`.
   - **Mantine**: See [mantine.md](mantine.md) — Full-featured component library. Requires CSS layer ordering and PostCSS changes for Tailwind v4. Read when library is `mantine`.
   - **Ant Design**: See [antd.md](antd.md) — Enterprise component library (CSS-in-JS). Requires StyleProvider with layer for Tailwind v4. Read when library is `antd`.

## What Frontend Scaffolds Include

| Component | Purpose |
|-----------|---------|
| Tailwind CSS v4 | Utility-first styling |
| ESLint + Prettier | Linting and formatting with Tailwind plugin |
| Vitest + Testing Library | Unit and component testing |
| Playwright | End-to-end testing |
| Home page | Styled landing page with `<project-name>` heading |
| Example tests | One passing component test and one passing E2E test |
| Husky + lint-staged | Pre-commit hook running ESLint and Prettier on staged files |
| `build` Makefile target | Production build |

## Edge Cases

- **pnpm not installed**: Suggest installing with `npm install -g pnpm` or `corepack enable` before proceeding.
- **User wants features beyond the scaffold**: Scaffold first, then help add routing, state management, API integration, etc. separately.
