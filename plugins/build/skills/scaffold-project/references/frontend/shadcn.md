# shadcn/ui Setup

shadcn/ui is a collection of copy-paste Radix UI components styled with Tailwind CSS. It has native Tailwind v4 support — no conflicts or workarounds needed.

## Setup: React + Vite

Ensure `@types/node` is in devDependencies (needed for the path alias in vite.config.ts).

Update `vite.config.ts` to add explicit path alias (shadcn CLI requires it):

```typescript
import path from 'node:path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [react(), tailwindcss(), tsconfigPaths()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

Run the initializer:

```bash
pnpx shadcn@latest init
```

The CLI prompts for style (default/new-york) and base color, then generates `components.json` and rewrites `src/index.css` with Tailwind v4 theme variables (OKLCH colors, `@theme inline`, `tw-animate-css`).

Add components as needed:

```bash
pnpx shadcn@latest add button
pnpx shadcn@latest add dialog card input
```

## Setup: Next.js

Run the initializer in the project root:

```bash
pnpx shadcn@latest init
```

The CLI detects Next.js and Tailwind v4 automatically. It rewrites `app/globals.css` with theme variables and generates `components.json` with `"rsc": true`.

Add components the same way:

```bash
pnpx shadcn@latest add button
```

## components.json

The CLI generates this file. Key fields for Tailwind v4:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/index.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

- `"config": ""` — empty string signals Tailwind v4 (no JS config file)
- `"css"` — points to your CSS entry (`src/index.css` for Vite, `app/globals.css` for Next.js)
- `"rsc"` — `true` for Next.js, `false` for Vite

## What the CLI Adds to Your CSS

The CSS entry point is rewritten to include theme variables:

```css
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  /* ... more color mappings ... */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
}

:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.141 0.005 285.823);
  /* ... full OKLCH palette ... */
}

.dark {
  --background: oklch(0.141 0.005 285.823);
  /* ... dark palette ... */
}
```

## Additional Dependencies

The `shadcn init` CLI automatically installs what it needs. `tw-animate-css` replaces the old `tailwindcss-animate` plugin for Tailwind v4.
