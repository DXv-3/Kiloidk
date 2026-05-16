# Technical Context: Next.js Starter Template

## Technology Stack

| Technology   | Version | Purpose                         |
| ------------ | ------- | ------------------------------- |
| Next.js      | 16.x    | React framework with App Router |
| React        | 19.x    | UI library                      |
| TypeScript   | 5.9.x   | Type-safe JavaScript            |
| Tailwind CSS | 4.x     | Utility-first CSS               |
| Bun          | Latest  | Package manager & runtime       |

## Development Environment

### Prerequisites

- Bun installed (`curl -fsSL https://bun.sh/install | bash`)
- Node.js 20+ (for compatibility)

### Commands

```bash
bun install        # Install dependencies
bun dev            # Start dev server (http://localhost:3000)
bun build          # Production build
bun start          # Start production server
bun lint           # Run ESLint
bun typecheck      # Run TypeScript type checking
bun test           # Run tests
bun test:ui        # Run tests with UI
bun test:coverage  # Run tests with coverage
bun db:generate    # Generate migrations
bun db:migrate     # Run migrations (auto in sandbox)
```

## Project Configuration

### Next.js Config (`next.config.ts`)

- App Router enabled
- Default settings for flexibility

### TypeScript Config (`tsconfig.json`)

- Strict mode enabled
- Path alias: `@/*` → `src/*`
- Target: ESNext

### Tailwind CSS 4 (`postcss.config.mjs`)

- Uses `@tailwindcss/postcss` plugin
- CSS-first configuration (v4 style)

### ESLint (`eslint.config.mjs`)

- Uses `eslint-config-next`
- Flat config format

## Key Dependencies

### Production Dependencies

```json
{
  "next": "^16.1.3",
  "react": "^19.2.3",
  "react-dom": "^19.2.3",
  "zod": "^4.4.3",
  "clsx": "^2.1.1",
  "tailwind-merge": "^3.6.0",
  "react-hook-form": "^7.76.0",
  "zustand": "^5.0.13",
  "@tanstack/react-query": "^5.100.10",
  "drizzle-orm": "^0.45.2",
  "@kilocode/app-builder-db": "github:Kilo-Org/app-builder-db#main"
}
```

### Dev Dependencies

```json
{
  "typescript": "^5.9.3",
  "tailwindcss": "^4.1.17",
  "drizzle-kit": "^0.31.10",
  "vitest": "^4.1.6",
  "happy-dom": "^20.9.0",
  "@testing-library/react": "^16.3.2",
  "@vitest/coverage-v8": "^4.1.6",
  "@vitejs/plugin-react": "^6.0.2"
}
```

## File Structure

```
/
├── .gitignore              # Git ignore rules
├── package.json            # Dependencies and scripts
├── bun.lock                # Bun lockfile
├── next.config.ts          # Next.js configuration
├── tsconfig.json           # TypeScript configuration
├── vitest.config.ts        # Vitest configuration
├── drizzle.config.ts       # Drizzle ORM configuration
├── postcss.config.mjs      # PostCSS (Tailwind) config
├── eslint.config.mjs       # ESLint configuration
├── src/
│   ├── app/                # Next.js App Router
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Home page
│   │   ├── loading.tsx     # Loading state
│   │   ├── error.tsx       # Error boundary
│   │   ├── not-found.tsx   # 404 page
│   │   ├── globals.css     # Global styles
│   │   ├── api/            # API routes
│   │   │   ├── health/
│   │   │   ├── users/
│   │   │   └── posts/
│   ├── components/         # React components
│   │   └── ui/             # UI primitives
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Input.tsx
│   │       └── LoadingSpinner.tsx
│   ├── db/                 # Database layer
│   │   ├── index.ts
│   │   ├── schema.ts
│   │   └── migrate.ts
│   ├── hooks/              # Custom React hooks
│   ├── stores/             # Zustand stores
│   ├── providers/          # React context providers
│   ├── lib/                # Utilities and helpers
│   └── test/               # Test setup and tests
```

## Technical Constraints

### Starting Point

- Minimal structure - expand as needed
- No database by default (use recipe to add)
- No authentication by default (add when needed)

### Browser Support

- Modern browsers (ES2020+)
- No IE11 support

## Performance Considerations

### Image Optimization

- Use Next.js `Image` component for optimization
- Place images in `public/` directory

### Bundle Size

- Tree-shaking enabled by default
- Tailwind CSS purges unused styles

### Core Web Vitals

- Server Components reduce client JavaScript
- Streaming and Suspense for better UX

## Deployment

### Build Output

- Server-rendered pages by default
- Can be configured for static export

### Environment Variables

- None required for base template
- Add as needed for features
- Use `.env.local` for local development
