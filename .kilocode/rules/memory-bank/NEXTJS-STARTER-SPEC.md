# Next.js Starter Template - Complete Specification

## Overview

A comprehensive Next.js 16 starter template with full-stack capabilities, designed for AI-assisted development and rapid iteration.

## Current State

- **Template Status**: Base setup complete, ready for expansion
- **Home Page**: Empty dark background awaiting content
- **Tech Stack**: Next.js 16 + React 19 + Tailwind CSS 4 + TypeScript strict mode

## Core Requirements

### Application Structure
- `src/app/page.tsx` - Home page with hero section and feature showcase
- `src/app/not-found.tsx` - 404 error page
- `src/app/error.tsx` - Global error boundary
- `src/app/loading.tsx` - Global loading state
- `src/app/api/health/route.ts` - Health check endpoint

### UI Components (`src/components/`)
- `ui/Button.tsx` - Reusable button with variants
- `ui/Card.tsx` - Container component
- `ui/Input.tsx` - Form input component
- `ui/LoadingSpinner.tsx` - Loading indicator
- `ui/Modal.tsx` - Modal dialog system
- `layout/Header.tsx` - Navigation header
- `layout/Footer.tsx` - Site footer
- `layout/ThemeToggle.tsx` - Dark/light mode switcher

### Database Integration
- `src/db/schema.ts` - Table definitions with Drizzle ORM
- `src/db/index.ts` - Database client singleton
- `src/db/migrate.ts` - Migration runner
- `drizzle.config.ts` - Drizzle configuration
- Package scripts: `db:generate`, `db:migrate`

### API Routes
- `/api/users` - User CRUD operations
- `/api/posts` - Post CRUD operations
- `/api/auth/login` - Authentication endpoint
- `/api/auth/register` - Registration endpoint
- `/api/upload` - File upload handler
- `/api/search` - Search functionality

### React Hooks (`src/hooks/`)
- `useApi` - Data fetching abstraction
- `useLocalStorage` - Persistent state hook
- `useMediaQuery` - Responsive breakpoint hook
- `useDebounce` - Input debouncing
- `usePagination` - Pagination logic
- `useForm` - Form state management

### State Management (`src/stores/`)
- `useAuthStore` - Authentication state
- `useUserStore` - User profile state
- `useUIStore` - UI preferences state

### Providers (`src/providers/`)
- `QueryProvider` - TanStack Query for server state
- `SessionProvider` - User session context
- `ThemeProvider` - Theme switching context
- `ToastProvider` - Notification system

### Utilities (`src/lib/`)
- `utils.ts` - Common utilities (cn, format)
- `validators.ts` - Zod schemas
- `constants.ts` - App constants
- `api.ts` - API client wrapper

### Recipe System
Required recipes to implement:
- Add Database (Drizzle + SQLite)
- Add Authentication (Auth.js)
- Add Testing (Vitest)
- Add Email (Resend)
- Add Payments (Stripe)
- Add Search (Algolia)

### Missing Configuration
- `tsconfig.json` paths for `@/*` alias
- `components.json` for component registry
- `.env.example` environment template
- Dockerfile for containerization

## Development Commands

```bash
bun typecheck  # Type checking
bun lint       # Lint checking
bun build      # Production build
bun db:generate    # Generate migrations
bun db:migrate     # Run migrations (auto in sandbox)
```

## Next Steps

1. Choose feature set based on application type
2. Implement selected recipes in order of dependency
3. Add component library (shadcn/ui recommended)
4. Configure testing infrastructure
5. Set up deployment pipeline