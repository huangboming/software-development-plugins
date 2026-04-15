# Mantine Setup

Mantine v8 is a full-featured React component library. It requires CSS layer ordering to coexist with Tailwind v4.

## Install

```bash
pnpm add @mantine/core @mantine/hooks
pnpm add -D postcss-preset-mantine postcss-simple-vars
```

## Tailwind v4 Compatibility

Tailwind v4's base reset can override Mantine's component styles. Fix this with explicit CSS layer ordering and Mantine's layered stylesheet.

Update the CSS entry point (`src/index.css` for Vite, `app/globals.css` for Next.js):

```css
@layer theme, base, mantine, components, utilities;

@import "tailwindcss";
@import "@mantine/core/styles.layer.css";
```

Use `styles.layer.css` (not `styles.css`) — this outputs Mantine styles into the `mantine` layer, ensuring Tailwind utilities can override Mantine but Tailwind's base reset doesn't nuke Mantine's styles.

## PostCSS Config

Both frameworks need PostCSS with Mantine plugins alongside Tailwind's PostCSS plugin.

For **React + Vite**: Remove `@tailwindcss/vite` from `vite.config.ts` plugins and use `@tailwindcss/postcss` instead (Mantine requires PostCSS, so both tools must go through the same pipeline).

```bash
pnpm add -D @tailwindcss/postcss
```

Create `postcss.config.mjs`:

```javascript
const config = {
  plugins: {
    'postcss-preset-mantine': {},
    'postcss-simple-vars': {
      variables: {
        'mantine-breakpoint-xs': '36em',
        'mantine-breakpoint-sm': '48em',
        'mantine-breakpoint-md': '62em',
        'mantine-breakpoint-lg': '75em',
        'mantine-breakpoint-xl': '88em',
      },
    },
    '@tailwindcss/postcss': {},
  },
}

export default config
```

For **Next.js**: Update the existing `postcss.config.mjs` to add Mantine plugins before the Tailwind plugin:

```javascript
const config = {
  plugins: {
    'postcss-preset-mantine': {},
    'postcss-simple-vars': {
      variables: {
        'mantine-breakpoint-xs': '36em',
        'mantine-breakpoint-sm': '48em',
        'mantine-breakpoint-md': '62em',
        'mantine-breakpoint-lg': '75em',
        'mantine-breakpoint-xl': '88em',
      },
    },
    '@tailwindcss/postcss': {},
  },
}

export default config
```

## MantineProvider: React + Vite

Update `src/main.tsx`:

```tsx
import '@mantine/core/styles.layer.css'
import './index.css'
import { MantineProvider } from '@mantine/core'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MantineProvider>
      <App />
    </MantineProvider>
  </StrictMode>,
)
```

Note: Import `styles.layer.css` before `index.css` so the layer declaration in `index.css` takes effect.

## MantineProvider: Next.js

Update `app/layout.tsx`:

```tsx
import '@mantine/core/styles.layer.css'
import './globals.css'
import type { Metadata } from 'next'
import { ColorSchemeScript, MantineProvider, mantineHtmlProps } from '@mantine/core'

export const metadata: Metadata = {
  title: '<project-name>',
  description: '<project-name>',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" {...mantineHtmlProps}>
      <head>
        <ColorSchemeScript />
      </head>
      <body>
        <MantineProvider>{children}</MantineProvider>
      </body>
    </html>
  )
}
```

- `ColorSchemeScript` prevents flash-of-wrong-color-scheme on SSR
- `mantineHtmlProps` adds the required `data-mantine-color-scheme` attribute

## Vite Config Change

When using Mantine, update `vite.config.ts` to remove `@tailwindcss/vite` (replaced by PostCSS):

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
})
```
