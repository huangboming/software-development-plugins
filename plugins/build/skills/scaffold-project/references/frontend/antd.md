# Ant Design Setup

Ant Design v6 is a CSS-in-JS component library. It needs no CSS imports or PostCSS plugins — styles are injected at runtime. Use `StyleProvider` with `layer` for Tailwind v4 compatibility.

## Install

```bash
pnpm add antd @ant-design/icons @ant-design/cssinjs
```

- `antd` — core components
- `@ant-design/icons` — icon library (must be v6 to match antd v6)
- `@ant-design/cssinjs` — needed for `StyleProvider` with CSS layer support

## Tailwind v4 Compatibility

antd v6 uses `:where()` selectors for low specificity, but Tailwind v4's base reset can still conflict. Fix this with CSS layer ordering and `StyleProvider layer`.

Update the CSS entry point (`src/index.css` for Vite, `app/globals.css` for Next.js):

```css
@layer theme, base, antd, components, utilities;

@import "tailwindcss";
```

This ensures antd styles sit between Tailwind's base and utility layers.

## Provider Setup: React + Vite

Update `src/main.tsx`:

```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { StyleProvider } from '@ant-design/cssinjs'
import { ConfigProvider } from 'antd'
import App from './App'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <StyleProvider layer>
      <ConfigProvider>
        <App />
      </ConfigProvider>
    </StyleProvider>
  </StrictMode>,
)
```

`StyleProvider layer` tells antd to inject styles into the `antd` CSS layer.

## Provider Setup: Next.js

For Next.js, add an SSR registry to prevent flash-of-unstyled-content.

Create `app/antd-registry.tsx`:

```tsx
'use client'

import { createCache, extractStyle, StyleProvider } from '@ant-design/cssinjs'
import { useServerInsertedHTML } from 'next/navigation'
import { useState } from 'react'

export function AntdRegistry({ children }: { children: React.ReactNode }) {
  const [cache] = useState(() => createCache())

  useServerInsertedHTML(() => (
    <style id="antd" dangerouslySetInnerHTML={{ __html: extractStyle(cache, true) }} />
  ))

  return (
    <StyleProvider cache={cache} layer>
      {children}
    </StyleProvider>
  )
}
```

Update `app/layout.tsx`:

```tsx
import './globals.css'
import type { Metadata } from 'next'
import { ConfigProvider } from 'antd'
import { AntdRegistry } from './antd-registry'

export const metadata: Metadata = {
  title: '<project-name>',
  description: '<project-name>',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AntdRegistry>
          <ConfigProvider>{children}</ConfigProvider>
        </AntdRegistry>
      </body>
    </html>
  )
}
```

## Notes

- No PostCSS changes needed — antd uses CSS-in-JS, not PostCSS
- No CSS imports needed — styles are injected at runtime
- The Vite and Next.js base scaffolds (vite.config.ts, postcss.config.mjs) remain unchanged
- `ConfigProvider` accepts an optional `theme` prop for customization (colors, border radius, etc.)
