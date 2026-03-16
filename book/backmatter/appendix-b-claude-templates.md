<span class="chapter-number">Appendix B</span>

# CLAUDE.md Templates {.chapter-title}

The CLAUDE.md file is the single highest-leverage file in any AI-assisted project. It's the persistent instruction set that shapes every interaction between you and Claude Code. A good CLAUDE.md turns a general-purpose AI into a domain-specific collaborator that knows your codebase, your conventions, and your quality bar.

These three templates progress from simple to sophisticated. Start with the one that matches your experience level. Evolve it as your projects grow.

---

## Template 1: Starter

For beginners and small projects. Covers the essentials: what the project is, how it runs, and what you care about.

```markdown
# CLAUDE.md

## Project
[Project name] — [One sentence describing what it does]

## Tech Stack
- Framework: [e.g., Next.js 14 with App Router]
- Styling: [e.g., Tailwind CSS]
- Database: [e.g., Supabase]
- Deployment: [e.g., Vercel]

## Getting Started
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

## Project Structure
- /app — Pages and routes (App Router)
- /components — Reusable UI components
- /lib — Utility functions and API clients
- /public — Static assets

## Conventions
- Use TypeScript for all new files
- Use Server Components by default; add "use client" only when needed
- Use Tailwind CSS for styling — no inline styles, no CSS modules
- All components go in /components with PascalCase naming
- All utility functions go in /lib with camelCase naming

## Quality
- Handle loading, empty, error, and success states in every component
- Validate all user input on the server side
- Use environment variables for API keys — never hardcode secrets
- Mobile-first responsive design
- Test the happy path and at least one error path

## Current Focus
[What you're working on right now — update this regularly]
```

**Why each section matters:**

- **Project** tells Claude the domain, so it makes contextually appropriate suggestions instead of generic ones.
- **Tech Stack** prevents Claude from suggesting incompatible libraries or outdated patterns.
- **Getting Started** lets Claude run your project without asking how. This eliminates back-and-forth.
- **Project Structure** tells Claude where to put new files. Without this, you'll get components created in random directories.
- **Conventions** prevents style drift across sessions. What Claude does in session 1 should match session 10.
- **Quality** sets the bar Claude should hold you to. Without explicit quality standards, Claude defaults to "it works."
- **Current Focus** provides session context without re-explaining every time. Update it at the start of each work session.

---

## Template 2: Advanced

For production projects. Adds architectural constraints, security requirements, testing standards, and patterns to follow or avoid.

```markdown
# CLAUDE.md

## Project
[Project name] — [One sentence]
[One paragraph of context: who uses it, what problem it solves, what stage it's at]

## Tech Stack
- Framework: Next.js 14 (App Router, Server Components default)
- Database: Supabase (PostgreSQL + pgvector + RLS)
- Auth: Supabase Auth (email + OAuth)
- AI: Anthropic Claude API (via @anthropic-ai/sdk)
- Styling: Tailwind CSS + design system tokens in /styles/tokens.css
- Deployment: Vercel (frontend) + Supabase (backend)
- CI: GitHub Actions (type-check, lint, test on every PR)

## Commands
npm run dev          # Start dev server (port 3000)
npm run build        # Production build (catches type errors)
npm run test         # Run test suite
npm run test:watch   # Tests in watch mode
npm run lint         # ESLint + Prettier check
npm run db:types     # Regenerate Supabase types

## Architecture Rules
- Server Components for data fetching. Client Components only for interactivity.
- All database queries go through /lib/db/ — never call Supabase directly
  from components.
- API routes handle auth verification, input validation, then delegate to
  /lib/services/.
- Business logic lives in /lib/services/ — not in routes, not in components.
- Types live in /types/ — one file per domain (user.ts, session.ts, etc.).

## Patterns to Follow
- Error handling: try/catch at the API boundary, return typed error responses.
- Loading states: use Suspense boundaries with skeleton components.
- Forms: Server Actions with Zod validation. Inline errors. Toast on success.
- Data fetching: batch queries where possible. N+1 queries are bugs.

## Patterns to Avoid
- No console.log in committed code (use /lib/logger.ts).
- No `any` types. Use `unknown` + type guard if you need escape hatch.
- No direct DOM manipulation.
- No CSS outside of Tailwind classes and /styles/tokens.css.
- No installing new dependencies without discussing the tradeoff first.

## Security
- Validate all input with Zod schemas at the API boundary.
- All database tables have RLS policies. Verify before marking migration done.
- Admin routes check role server-side. Never trust client-side role checks.
- Rate limit: auth endpoints (5/min), AI endpoints (20/min), general (100/min).
- Environment variables: .env.local for dev, Vercel env for prod. Never
  commit secrets.

## Testing
- Unit tests for /lib/services/ (business logic).
- Integration tests for API routes (request in, response out).
- No tests for pure UI components unless they contain logic.
- Test the unhappy path: invalid input, missing auth, expired tokens,
  API failures.

## Database
- Migration files in /supabase/migrations/ with timestamp prefix.
- Always generate types after migration: npm run db:types.
- Use transactions for multi-table writes.
- Add indexes for any column in WHERE or ORDER BY with >1000 rows.

## Current Work
[Active task or feature — update each session]

## Known Issues
[List of known bugs or tech debt — helps Claude avoid related areas]
```

**What the Advanced template adds:**

- **Architecture Rules** prevent structural drift. Without them, Claude will put business logic in API routes one session and in components the next. These rules act as guardrails across sessions.
- **Patterns to Follow/Avoid** encode team decisions. They're faster than debating the same choice in every conversation. "Should I use console.log for debugging?" is answered once, permanently.
- **Security** as a first-class section means it's never an afterthought. Every AI-generated endpoint inherits your security standards.
- **Known Issues** prevent Claude from "fixing" a bug by introducing a different one in the same area. Context about existing problems is context about where to be careful.

---

## Template 3: Team Collaboration

For multi-person projects where multiple developers use Claude Code on the same codebase. Adds ownership, PR conventions, and conflict prevention.

```markdown
# CLAUDE.md

## Project
[Project name] — [Description]
Team: [names and roles]
Repo: [GitHub URL]

## Tech Stack
[Same structure as Advanced template]

## Commands
[Same structure as Advanced template]

## Architecture
[Same structure as Advanced template]

## Team Conventions

### Ownership
- /app/(admin)/ — [Name] owns admin features
- /app/(public)/ — [Name] owns public-facing pages
- /lib/services/ai/ — [Name] owns AI integration
- /lib/services/billing/ — [Name] owns billing logic
- If you need to modify another owner's area, flag it in the PR description.

### Git Workflow
- Branch naming: [type]/[ticket]-[description]
  (e.g., feat/DASH-42-add-export)
- Commit messages: conventional commits (feat:, fix:, refactor:, test:, docs:)
- PRs require 1 approval. PRs touching billing require [Name]'s approval.
- Squash merge to main. Delete branch after merge.
- Never force push to main. Never push directly to main.

### PR Standards
- Title: clear, under 70 characters, conventional commit prefix
- Description: what changed, why, how to test, screenshots for UI changes
- Every PR must pass CI (type-check, lint, test) before review
- If a PR changes an API contract, update /docs/api/

### Communication
- Before starting a new feature: check the project board for existing work
- Before refactoring shared code: discuss in Slack first
- Before adding a dependency: open a discussion PR with package, rationale,
  and alternatives considered

### Conflict Prevention
- Lock files (package-lock.json) — rebase, never manually resolve
- Shared types in /types/ — additive changes only. Never rename or remove
  without a migration plan.
- Database migrations — number sequentially, never reorder. Coordinate order
  if two people create migrations simultaneously.
- Environment variables — add to .env.example with a comment. Notify team.

## Quality & Security
[Same structure as Advanced template]

## Current Sprint
[Active sprint goals — keeps Claude aligned with team priorities]

## Decision Log
- [Date]: Chose Supabase over Firebase because [reason]
- [Date]: Decided against LangChain because [reason]
- [Date]: Adopted conventional commits for automated changelog
[Append decisions as they're made — prevents relitigating resolved debates]
```

**What the Team template adds:**

- **Ownership** prevents one developer's Claude session from trampling another's work. When Claude knows that `/lib/services/billing/` belongs to someone else, it will flag proposed changes instead of making them silently.
- **Git Workflow** ensures AI-generated commits follow the same conventions as human ones. Without this, you get commits like "update stuff" mixed with carefully crafted conventional commits.
- **Conflict Prevention** addresses the specific ways parallel AI-assisted development can create merge nightmares. Two developers using Claude Code on the same codebase will generate conflicting migrations, conflicting type changes, and conflicting lock files unless the rules are explicit.
- **Decision Log** is the most underrated section. When Claude knows *why* you chose Supabase, it won't suggest Firebase. When it knows you rejected LangChain, it won't propose it. Decisions without recorded rationale get relitigated endlessly — by humans and AI alike.

---

## Evolving Your CLAUDE.md

Your CLAUDE.md is a living document. It should change every week. After each session, ask:

- Did Claude make a mistake I've seen before? Add a rule that prevents it.
- Did I have to repeat context? Add it to the file permanently.
- Is there a rule I've been ignoring? Remove it — dead rules erode trust in living ones.
- Is the file over 100 lines? Compress ruthlessly. The best CLAUDE.md is the shortest one that prevents all the mistakes you've already made.

One anti-pattern to avoid: don't try to write the perfect CLAUDE.md before your first session. Start with the Starter template. Let the project teach you what rules it needs. The Advanced template emerged from hundreds of sessions, not from careful planning. Yours will too.
