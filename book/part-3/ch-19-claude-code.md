<span class="chapter-number">Chapter 19</span>

# Claude Code Mastery — Your Technical Co-Founder in the Terminal {.chapter-title}

Open your terminal. Type a sentence describing what you want to build. Watch an AI agent read your codebase, plan the work, write the code, run the tests, fix the failures, and commit the result — while you sip your coffee.

That's not a demo. That's a Tuesday afternoon with Claude Code.

This chapter is about the most powerful AI coding tool available as of March 2026 — not because it writes the prettiest autocomplete suggestions, but because it operates on a fundamentally different paradigm from every other tool in this space. Claude Code is not an IDE plugin. It is not a fancy autocomplete. It is an **autonomous agent** that lives in your terminal, reads your entire codebase, and drives the development process while you describe intent and review output.

The difference matters. And understanding that difference — deeply, architecturally, practically — is the difference between using Claude Code like a chatbot and using it like the technical co-founder you wish you had.

---

## Part 1: The Paradigm Shift — Agent-First vs. IDE-First

### Two Philosophies of AI-Assisted Coding

Every AI coding tool falls into one of two camps. Understanding which camp you're in determines how you work, what you can build, and where the tool breaks down.

**IDE-First (Cursor, Copilot, Windsurf):** You sit in a code editor. The AI is a layer on top of that editor. You write code; the AI suggests completions, answers questions in a side panel, and makes edits when you ask. The human drives. The AI assists. The editor is the center of gravity.

**Agent-First (Claude Code, Codex CLI, Gemini CLI):** You sit in a terminal. The AI is not a layer on top of anything — it *is* the developer. You describe what you want in natural language. The agent reads files, writes code, runs commands, interprets errors, and iterates. The human describes and reviews. The AI drives. The conversation is the center of gravity.

> **ANALOGY**: IDE-first is like having a brilliant intern sitting next to you while you code — they can finish your sentences, look things up, and make suggestions, but you're the one with your hands on the keyboard. Agent-first is like hiring a contractor — you describe the renovation you want, they go do it, and you inspect the work when they're done. Same goal, radically different workflow.

Here's how the two approaches compare in practice:

| Dimension | IDE-First (Cursor) | Agent-First (Claude Code) |
|-----------|-------------------|--------------------------|
| **Primary interface** | Code editor with AI sidebar | Terminal conversation |
| **Who drives?** | You write, AI assists | AI writes, you review |
| **Context** | Current file + open tabs | Entire codebase via search |
| **Best for** | Rapid iteration within files | Multi-file changes, new features |
| **Weakness** | Complex cross-file refactors | Small single-line tweaks |
| **Mental model** | Pair programming | Delegation to a senior dev |
| **Token efficiency** | Higher token use per task | 5.5x fewer tokens (Anthropic data) |

The 5.5x token efficiency number comes from Anthropic's internal benchmarks comparing identical tasks across tools. The reason is architectural: Claude Code's agent reads only what it needs (searching, grepping, reading specific files), while IDE-first tools often send large chunks of open files as context whether or not they're relevant.

> **INTUITION**: Neither approach is "better." They're better for different moments. If you're deep in a file, tweaking CSS, and you want the AI to finish the property you're typing — IDE-first wins. If you need to add a new API endpoint, update the database schema, create the migration, write the tests, and update the frontend to call the new endpoint — agent-first wins. The best builders in 2026 use both.

### Why Agent-First Changes What's Possible

The agent-first model unlocks something that IDE-first cannot: **the AI can run its own work.**

When Claude Code writes a function, it can immediately run the test suite to see if it passes. If the test fails, it reads the error, diagnoses the problem, fixes the code, and runs the test again — all without you doing anything. This loop — write, run, read error, fix, repeat — is what software engineers spend 60-70% of their time doing. An agent-first tool automates the entire loop.

In an IDE-first tool, the AI writes code and hands it to you. You run the test. You read the error. You paste the error back into the AI. The AI suggests a fix. You apply it. You run the test again. Every iteration requires a human round trip.

> **REAL-LIFE**: Anthropic's internal data shows that Claude Code autonomously resolves 72.2% of Anthropic's own internal bug reports — from reading the ticket, finding the relevant code, writing the fix, running tests, to creating the pull request. Not cherry-picked demos. Actual production bugs on a real codebase. This is the agent-first advantage in its purest form: the AI doesn't stop at suggesting a fix. It *proves* the fix works.

---

## Part 2: Under the Hood — Claude Code's Multi-Agent Architecture

### The Hidden Architecture

When you type a message into Claude Code, you're talking to a **main agent**. But the main agent is not working alone. Claude Code is a **multi-agent system** — a hidden orchestra of specialized agents coordinated by the one you interact with.

Here's the architecture:

```
┌─────────────────────────────────────────────────────┐
│                    YOU (Terminal)                     │
│              "Add user authentication"               │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                   MAIN AGENT                         │
│  Reads your message, loads CLAUDE.md, plans work     │
│  Decides: do it myself, or dispatch subagents?       │
└──────┬──────────┬──────────┬───────────┬────────────┘
       │          │          │           │
       ▼          ▼          ▼           ▼
┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│ Subagent ││ Subagent ││ Subagent ││ Subagent │
│    #1    ││    #2    ││    #3    ││    #4    │
│  Search  ││  Write   ││  Test    ││  Review  │
│  code    ││  auth    ││  auth    ││  changes │
│  patterns││  routes  ││  routes  ││          │
└──────────┘└──────────┘└──────────┘└──────────┘
```

The main agent has a **system prompt** (the instructions that define how it behaves — think of it as the agent's personality and rulebook). This system prompt tells it: you have access to tools. Those tools include reading files, writing files, running shell commands, searching code, and — critically — **spawning subagents**.

A **subagent** is a separate Claude instance with its own context, its own tool access, and a specific task. The main agent can say: "Read the entire authentication module and summarize the current patterns." That task goes to a subagent. The main agent continues planning. When the subagent returns its summary, the main agent incorporates it and moves on.

### Why This Architecture Matters

Three reasons:

**1. Context efficiency.** The main agent doesn't need to hold your entire codebase in memory. It dispatches subagents to read and summarize specific sections, keeping only the summaries in its own context window. This is why Claude Code can work on massive codebases that would overflow any single model's context.

**2. Parallelism.** The main agent can dispatch multiple subagents simultaneously. "Read the auth module" and "read the database schema" and "check what test framework we're using" can all happen in parallel. This cuts wait time significantly.

**3. Specialization.** Each subagent gets a focused prompt tailored to its specific task. A subagent searching for code patterns gets instructions optimized for search. A subagent writing tests gets instructions optimized for test generation. The main agent is the coordinator; the subagents are the specialists.

> **INTUITION**: Think of it like a startup CEO (main agent) who has a team (subagents). The CEO doesn't read every document in the company. They ask their team: "Sarah, summarize last quarter's metrics. Raj, draft the product spec. Priya, check if our CI pipeline is green." Each team member works independently and reports back. The CEO synthesizes everything into a decision. Claude Code's main agent works the same way — except the team members are disposable Claude instances that exist only for the duration of their task.

### The Tool System

The main agent and subagents interact with your codebase through **tools** — functions the model can call. Claude Code's tool set includes:

| Tool | What It Does |
|------|-------------|
| **Read** | Opens and reads a file from your filesystem |
| **Write** | Creates or overwrites a file |
| **Edit** | Makes surgical text replacements in a file |
| **Bash** | Runs any terminal command (npm, git, python, etc.) |
| **Grep** | Searches file contents with regex patterns |
| **Glob** | Finds files by name patterns |
| **Agent** (subagent) | Spawns a new Claude instance for a subtask |

When Claude Code decides to edit a file, it calls the Edit tool with the exact text to find and the exact text to replace it with. When it needs to run your test suite, it calls the Bash tool with `npm test`. When it needs to understand a module it hasn't read yet, it might call Agent to dispatch a subagent that reads the module and summarizes it.

Every tool call is visible to you in the terminal. You can see exactly what Claude Code is reading, writing, and running. This transparency is deliberate — agent-first doesn't mean blind trust. It means informed delegation.

---

## Part 3: Boris Cherny's 10 Principles for Claude Code Mastery

Boris Cherny is an engineer at Anthropic who helped build Claude Code. In early 2026, he published a set of principles for getting the most out of the tool — not generic AI tips, but specific practices distilled from watching thousands of developers use Claude Code. These principles separate the developers who say "Claude Code is okay" from the developers who say "Claude Code replaced half my team."

Let's go through each one.

### Principle 1: Parallel Work with Worktrees

**The problem:** You're working on a feature. A bug report comes in. You need to context-switch, but you don't want to stash your current work, switch branches, fix the bug, switch back, and unstash. That workflow is fragile and slow.

**The solution:** Git **worktrees** — a feature that lets you check out multiple branches of the same repository simultaneously, each in its own directory. Think of it as having two copies of your project open at once, each on a different branch, sharing the same git history.

Claude Code integrates worktrees natively. You can tell Claude Code: "Open a new worktree for this bugfix." It creates a separate directory, checks out a new branch, and you (or a second Claude Code instance) can work on the bugfix while the original worktree continues the feature work.

```
~/project/              ← main worktree (feature branch)
    └── Claude Code instance #1 working on user-profiles

~/project-bugfix/       ← second worktree (bugfix branch)
    └── Claude Code instance #2 fixing payment crash
```

**New in 2026: `worktree.sparsePaths`** — You can configure which paths are checked out in each worktree. Working on the API? Your worktree only contains `src/api/`, `tests/api/`, and shared utilities. The frontend code isn't even present. This reduces disk usage, speeds up git operations, and — critically — keeps Claude Code focused on the relevant code.

> **REAL-LIFE**: A solo developer at a YC startup reported running three Claude Code instances simultaneously — one on a feature branch, one on a bugfix, one writing tests for an older module. All three shared the same git history. When the bugfix was ready, a simple `git merge` brought it into the feature branch. Total wall-clock time for all three tasks: 12 minutes. Sequential time would have been over an hour.

### Principle 2: Plan Mode First for Complex Tasks

**The problem:** You tell Claude Code "Add Stripe payments to my app." It immediately starts writing code. Ten minutes later, you realize it chose a payment architecture you don't want — server-side sessions instead of client-side Stripe Elements. You've wasted time and tokens.

**The solution:** Start with plan mode. Before Claude Code writes a single line of code, ask it to plan.

```
You: "I need to add Stripe payments. Before writing any code,
      analyze the current codebase and propose a plan. Include:
      - Which files need to change
      - What the data flow looks like
      - What dependencies we need
      - What could go wrong
      Do NOT write code yet."
```

Claude Code will read your codebase, understand your existing patterns, and produce a structured plan. You review the plan, adjust it, and only then say "Execute." This saves massive amounts of rework.

The rule of thumb: **if the task requires changes to more than 3 files, start with plan mode.** For single-file edits, direct execution is fine. For anything architectural, plan first.

> **INTUITION**: Plan mode is the equivalent of an architect drawing blueprints before construction begins. You wouldn't tell a contractor "build me a house" and walk away — you'd review the blueprints first. Same principle applies. The cost of a plan (a few hundred tokens and 30 seconds of your review time) is trivial compared to the cost of ripping out and redoing incorrect work.

### Principle 3: Invest Heavily in CLAUDE.md

**CLAUDE.md** is a markdown file at the root of your project that Claude Code reads at the start of every conversation. It is the single highest-leverage thing you can do to improve Claude Code's output.

Think of CLAUDE.md as the onboarding document you'd give a new senior engineer joining your team. It tells Claude Code:

- **Project architecture:** "This is a Next.js 14 app with App Router, Supabase for auth and database, Tailwind for styling."
- **Conventions:** "We use server components by default. Client components are marked with 'use client'. We never use console.log in production code."
- **Patterns:** "API routes follow this structure: validate input → check auth → execute query → return response."
- **Gotchas:** "Supabase RLS policies must be verified after any table change. The `profiles` table has a trigger that syncs with `auth.users` — never update it directly."
- **Preferences:** "Use named exports, not default exports. Prefer early returns over nested conditionals. Always handle loading, error, empty, and success states."

A well-written CLAUDE.md transforms Claude Code from a generic AI into a team member who understands *your* project. Without it, Claude Code has to guess your conventions. With it, Claude Code follows them consistently.

```markdown
# CLAUDE.md — Project: Rethink Dashboard

## Stack
- Next.js 14 (App Router, Server Components default)
- Supabase (Auth, Postgres, RLS enabled)
- Tailwind CSS + shadcn/ui
- TypeScript (strict mode)

## Conventions
- Server Components by default. Mark client components explicitly.
- API routes: validate → auth → query → respond
- No console.logs in committed code
- Handle all states: loading, empty, error, success

## Database Gotchas
- RLS is enabled on ALL tables. Verify policies after schema changes.
- The `profiles` table syncs via trigger from `auth.users` — never UPDATE directly.
- Always batch queries. Never N+1.

## Quality Bar
- Mobile-first. 44px touch targets minimum.
- Confirm destructive actions with a modal.
- Toast feedback for all async operations.
```

**How Claude Code uses CLAUDE.md:** It loads the file into the system prompt at the start of every conversation. Every decision Claude Code makes is influenced by what you've written here. If your CLAUDE.md says "use server components by default," Claude Code will use server components. If it says "never use `any` in TypeScript," Claude Code will use proper types.

There are three levels of CLAUDE.md:

1. **Global** (`~/.claude/CLAUDE.md`): Applies to everything you do with Claude Code. Your universal preferences.
2. **Project** (`./CLAUDE.md` at repo root): Project-specific conventions, architecture, gotchas.
3. **Directory** (`./src/api/CLAUDE.md`): Narrow instructions for a specific part of the codebase.

Claude Code merges all three, with more specific files taking priority.

### Principle 4: Custom Skills and Slash Commands

**Skills** are reusable workflows you teach Claude Code. Instead of explaining the same multi-step process every time, you encode it as a skill that Claude Code can execute with a single command.

A skill is a markdown file in your `.claude/skills/` directory. It describes a workflow in natural language, and Claude Code follows it like a recipe.

Example — a skill for creating new API endpoints:

```markdown
# Skill: new-api-endpoint

When asked to create a new API endpoint:

1. Create the route file at `app/api/{name}/route.ts`
2. Follow this template:
   - Import `createRouteHandlerClient` from `@supabase/auth-helpers-nextjs`
   - Validate input with zod schema
   - Check authentication
   - Execute database query
   - Return NextResponse.json with appropriate status
3. Create corresponding test file at `__tests__/api/{name}.test.ts`
4. Add the endpoint to the API documentation in `docs/api.md`
5. Run the test suite to verify
```

You invoke this with `/new-api-endpoint` in your Claude Code session. Claude Code reads the skill file and follows the steps exactly, adapted to the specific endpoint you're creating.

Skills compound. Over weeks and months, you build a library of skills that encode your team's best practices. Every new team member who uses Claude Code automatically inherits these practices.

### Principle 5: Autonomous Bug Fixing

This is where the agent-first model truly shines.

You paste an error message. Claude Code reads it, searches your codebase for the relevant file, understands the surrounding code, hypothesizes the cause, writes a fix, runs the test, and — if the test passes — commits the result. The entire cycle can happen without a single additional input from you.

The workflow:

```
You: "Fix this error: TypeError: Cannot read properties of
      undefined (reading 'email') at /app/api/users/route.ts:47"

Claude Code:
  1. Reads /app/api/users/route.ts (Edit tool)
  2. Sees line 47: `const email = user.email`
  3. Searches for where `user` is defined (Grep tool)
  4. Finds: `const user = await getUser(session.id)`
  5. Reads getUser function — it can return null
  6. Diagnosis: missing null check
  7. Adds: `if (!user) return NextResponse.json({ error: 'User not found' }, { status: 404 })`
  8. Runs test suite (Bash tool: npm test)
  9. All tests pass
  10. "Fixed: Added null check for user lookup in /app/api/users/route.ts"
```

For this to work well, you need two things: good error messages (the more context, the better) and a working test suite (so Claude Code can verify its fix). If your project has no tests, Claude Code can still fix bugs, but it can't *prove* the fix is correct.

### Principle 6: Advanced Prompting Within Claude Code

Claude Code responds to the same prompting techniques that work with any LLM, but the stakes are higher because it's executing code, not generating text.

**Be specific about constraints:**
- Bad: "Make the dashboard faster"
- Good: "The dashboard page at `/app/dashboard/page.tsx` takes 4.2 seconds to load. The main bottleneck is the analytics query. Optimize the query or add caching. Do not change the UI. Do not add new dependencies."

**Reference files explicitly:**
- Bad: "Fix the auth bug"
- Good: "There's a bug where expired sessions aren't being caught. Check `middleware.ts`, `lib/auth.ts`, and `app/api/auth/callback/route.ts`. The session should redirect to `/login` if the token is expired."

**Set the success criteria:**
- Bad: "Add tests"
- Good: "Add tests for the `/api/payments` endpoint. Cover: successful payment, insufficient funds, invalid card, expired session, missing required fields. All tests must pass with `npm test`."

> **INTUITION**: The prompting principle with Claude Code is the same as delegating to a human: the more clearly you describe the desired outcome, the less back-and-forth you need. Vague instructions produce vague results. Specific instructions produce precise results. The five extra seconds you spend writing a detailed prompt save five minutes of rework.

### Principle 7: Terminal Optimizations

Claude Code lives in your terminal, and a well-configured terminal makes Claude Code faster and more capable.

**Key optimizations:**

1. **Use a fast terminal emulator.** Claude Code outputs a lot of text. A slow terminal creates visual lag. iTerm2 (macOS), Warp, or Ghostty all handle high-throughput text well.

2. **Increase your scrollback buffer.** Claude Code's output can be long. Set your scrollback to at least 10,000 lines so you can review what happened earlier in the session.

3. **Enable shell integration.** Tools like Warp and iTerm2 offer shell integration that makes it easier to navigate Claude Code's output — jumping between command outputs, copying specific sections.

4. **Use tmux or screen for long sessions.** If you're running Claude Code on a remote server (or want to detach and reattach sessions), a terminal multiplexer keeps your session alive.

### Principle 8: Subagents for Parallelization

You can explicitly ask Claude Code to use subagents for parallel work:

```
You: "I need three things done independently:
      1. Refactor the user service to use the repository pattern
      2. Add pagination to the /api/products endpoint
      3. Write integration tests for the auth flow

      Use subagents to work on all three in parallel."
```

Claude Code dispatches three subagents, each working in its own context. The main agent monitors progress and merges results. Tasks that would take 30 minutes sequentially complete in 10-12 minutes.

**When to use subagents:**
- Tasks that touch different parts of the codebase (low overlap)
- Tasks that don't depend on each other's output
- Read-heavy tasks (analyzing code, summarizing modules, searching for patterns)

**When NOT to use subagents:**
- Tasks where step 2 depends on step 1's output
- Tasks that modify the same files (risk of merge conflicts)
- Small tasks where the overhead of spawning a subagent exceeds the time saved

### Principle 9: Data Analysis Capabilities

Claude Code isn't limited to writing application code. It can analyze data directly in your terminal.

```
You: "Read the CSV at data/user_signups_2026.csv.
      Tell me: weekly signup trends, top acquisition channels,
      and cohort retention rates. Generate charts as SVG files."
```

Claude Code will:
1. Read the CSV using Python (or Node, depending on your environment)
2. Analyze the data with pandas or equivalent
3. Generate SVG charts
4. Summarize findings in plain language

This is powerful for product managers who need quick data analysis without switching to a Jupyter notebook or waiting for a data team.

### Principle 10: Learning Mode for Understanding Codebases

When you join a new project — or when you're trying to understand a module you didn't write — use Claude Code as a learning tool.

```
You: "I'm new to this codebase. Walk me through how a request
      flows from the frontend to the database when a user
      creates a new post. Read the relevant files and explain
      each step."
```

Claude Code will trace the flow: frontend component → API call → route handler → service layer → database query → response. It reads the actual code and explains what each piece does, with references to specific files and line numbers.

This is not the same as reading documentation (which may be outdated) or asking a teammate (who may be busy). It's the actual code, explained in real time.

---

## Part 4: The Technical Co-Founder Framework

Here's the workflow that transforms Claude Code from a tool into a technical co-founder. Five phases, each with a distinct purpose.

### Phase 1: Discovery

**Goal:** Understand the current state before changing anything.

```
You: "I want to add a notification system. Before we start:
      1. What notification-related code already exists?
      2. What messaging infrastructure do we have?
      3. What would need to change in the database schema?
      4. Are there any existing patterns for async jobs?"
```

Claude Code reads your codebase, dispatches subagents to search for relevant code, and returns a comprehensive assessment. You now have a map of the territory.

### Phase 2: Planning

**Goal:** Agree on the approach before writing code.

```
You: "Based on your analysis, propose a plan for the
      notification system. Include:
      - Database schema changes
      - New API endpoints needed
      - Frontend components
      - Which existing code needs modification
      - Potential risks

      Do NOT write code yet."
```

Review the plan. Push back on parts you disagree with. Adjust scope. This is where you exercise product judgment — what's essential for v1 vs. what can wait.

### Phase 3: Building

**Goal:** Execute the plan in stages.

```
You: "Execute phase 1 of the plan: database schema changes
      and migrations. Run the migration and verify it works."
```

Then:

```
You: "Phase 2: Create the notification API endpoints.
      Follow our existing patterns. Write tests for each."
```

Build in stages, not all at once. Each stage should be independently verifiable. If something goes wrong in phase 3, you don't want to undo phases 1 and 2.

### Phase 4: Polish

**Goal:** Bring the implementation to production quality.

```
You: "Review all the notification code we've written. Check for:
      - Edge cases we missed
      - Missing error handling
      - Performance concerns (N+1 queries, missing indexes)
      - Security issues (auth checks, input validation)
      - Accessibility on the frontend components"
```

Claude Code reviews its own work with fresh eyes (a new subagent that wasn't involved in the writing). This catches issues the original implementation missed.

### Phase 5: Handoff

**Goal:** Document and communicate.

```
You: "Create a pull request with:
      - Summary of changes
      - Screenshots of the new UI
      - Migration instructions
      - Test plan for QA"
```

Claude Code generates the PR description, runs the full test suite one final time, and creates the commit.

> **REAL-LIFE**: A product manager at a Series A startup used this five-phase framework to ship a complete analytics dashboard in 3 days — from zero existing code to production deployment. The same feature was estimated at 2 weeks of engineering time. The PM didn't write a single line of code manually. They described, reviewed, and directed. Claude Code built.

---

## Part 5: Agent Teams — The Experimental Frontier

In late 2025, Anthropic introduced **agent teams** — an experimental feature where multiple Claude Code instances work together on different aspects of the same project, coordinated by a team lead agent.

### How Agent Teams Work

```
┌───────────────────────────────────────────┐
│              TEAM LEAD AGENT              │
│  Reads the task, decomposes it, assigns   │
│  subtasks to teammates, merges results    │
└────┬──────────────┬──────────────┬────────┘
     │              │              │
     ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Teammate │  │ Teammate │  │ Teammate │
│    #1    │  │    #2    │  │    #3    │
│ Backend  │  │ Frontend │  │  Tests   │
│ API work │  │ UI work  │  │ + QA     │
│          │  │          │  │          │
│ Own git  │  │ Own git  │  │ Own git  │
│ worktree │  │ worktree │  │ worktree │
└──────────┘  └──────────┘  └──────────┘
```

Each teammate runs in its own **worktree** — an independent checkout of the repository on its own branch. The team lead assigns tasks, monitors progress, and orchestrates merges. Teammates work in parallel, each with their own context and tool access.

This is conceptually different from subagents. Subagents are short-lived — they complete a task and return a result. Teammates are long-lived — they maintain context across multiple interactions and build up understanding of their assigned domain.

### When Agent Teams Make Sense

- **Large features** that naturally decompose into backend, frontend, and test work
- **Refactoring projects** where different modules can be updated independently
- **Sprint-level work** where multiple tickets can be worked simultaneously

### When They Don't

- **Tightly coupled changes** where every file depends on every other file
- **Small tasks** where the coordination overhead exceeds the parallelism benefit
- **Projects without tests** where merge conflicts can't be automatically resolved

Agent teams are experimental in March 2026. The coordination is imperfect. Merge conflicts happen. But the trajectory is clear: the future of AI-assisted development is not one AI helping one human — it's teams of AI agents working together, directed by human intent.

---

## Part 6: New in 2026

Claude Code evolves rapidly. Here are the features that shipped in the first quarter of 2026, each addressing a real limitation of earlier versions.

### worktree.sparsePaths

Configure which directories exist in each worktree. Instead of checking out the entire repository:

```json
{
  "worktree": {
    "sparsePaths": ["src/api/", "tests/api/", "lib/shared/", "package.json"]
  }
}
```

Your worktree contains only the API code. Claude Code can't accidentally modify frontend files. The git operations are faster because there's less to track. And Claude Code's context stays focused on the relevant code.

### PostCompact Hooks

When Claude Code runs for a long time, its context window fills up. At that point, it performs **compaction** — summarizing the conversation so far to free up context space. PostCompact hooks let you run custom logic after compaction happens.

Why this matters: compaction can lose important details. A PostCompact hook can re-inject critical context — open file paths, current task state, failing test output — ensuring Claude Code doesn't lose track of what it was doing.

```json
{
  "hooks": {
    "PostCompact": [
      {
        "command": "cat .claude/compact-context.md",
        "description": "Re-inject critical context after compaction"
      }
    ]
  }
}
```

### autoMemoryDirectory

Claude Code can now automatically write memories to a directory — things it learned during a session that should persist across sessions. This creates a growing knowledge base about your project.

```json
{
  "autoMemoryDirectory": ".claude/memory/"
}
```

After a session where Claude Code discovers that "the payments service requires a specific header format," it writes that to a memory file. In the next session, it reads all memory files and knows this fact without being told.

### MCP OAuth

**MCP (Model Context Protocol)** is the protocol Claude Code uses to connect to external tools and services — databases, APIs, browsers, Slack, GitHub. In early 2026, MCP added OAuth support, meaning Claude Code can authenticate with third-party services using standard OAuth flows.

Before MCP OAuth, connecting Claude Code to a service required API keys hardcoded in configuration. Now it can use the same authentication flow as a web browser — redirect to the service's login page, get a token, use it. This is more secure and works with services that don't offer API keys.

---

## Part 7: Token Efficiency — Why It Matters More Than You Think

Anthropic published data showing Claude Code uses **5.5x fewer tokens** than Cursor for identical tasks. This sounds like a marketing number, but the mechanism behind it is worth understanding because it affects your costs, your speed, and the quality of output.

### Why Claude Code Uses Fewer Tokens

**1. Selective reading.** Claude Code doesn't send your entire codebase to the model. It searches (Grep, Glob), reads specific files, and reads specific line ranges. An IDE-first tool often sends all open tabs plus the current file as context — whether or not they're relevant to the current task.

**2. Tool-based interaction.** Instead of embedding large blocks of code in the conversation, Claude Code uses structured tool calls. "Read lines 45-60 of auth.ts" is far fewer tokens than pasting those 15 lines into the chat.

**3. Subagent isolation.** When a subagent reads a 500-line file to answer a question, those 500 lines exist in the subagent's context, not the main agent's. The main agent receives only the subagent's summary — maybe 50 tokens instead of 2,000.

### What This Means for You

On Claude Pro ($20/month), token efficiency means you can do more before hitting usage limits. On API pricing, it means lower costs per task. On long sessions, it means Claude Code can work longer before needing context compaction.

> **INTUITION**: Token efficiency in AI coding tools is like fuel efficiency in cars. A car that gets 50 km/L and a car that gets 9 km/L both get you to the same destination. But the efficient car goes further on the same tank, costs less per trip, and doesn't need to refuel as often. Claude Code's architectural choices — search instead of send, subagents instead of context loading, tools instead of text — are the engineering decisions that produce that fuel efficiency.

---

## Part 8: Putting It All Together

<div class="exercise">

### Exercise: Build Your Claude Code Environment

This exercise walks you through setting up a production-grade Claude Code environment. You'll need Claude Code installed (via `npm install -g @anthropic-ai/claude-code` or the standalone installer).

**Step 1: Create Your Global CLAUDE.md**

Create `~/.claude/CLAUDE.md` with your universal preferences:

```markdown
# Global CLAUDE.md

## Identity
You are my technical co-founder. I describe what to build.
You decide how and hold the quality bar.

## Universal Conventions
- TypeScript strict mode, always
- No console.logs in production code
- Handle every state: loading, empty, error, success
- Mobile-first design. 44px minimum touch targets.
- Confirm destructive actions. Toast feedback for async ops.

## Communication Style
- Lead with recommendation, then tradeoffs
- If something seems wrong, push back with evidence
- One issue per question
```

**Step 2: Create Your Project CLAUDE.md**

In your project root, create `CLAUDE.md` with project-specific details:

```markdown
# CLAUDE.md — [Your Project Name]

## Stack
[Your tech stack]

## Architecture
[Key architectural decisions and patterns]

## Database
[Schema gotchas, RLS policies, trigger behaviors]

## Quality Bar
[Your project's specific quality requirements]
```

**Step 3: Use Plan Mode**

Start Claude Code in your project directory. Give it a task, but ask for a plan first:

```
"I need to add [feature]. Before writing code:
 1. Analyze the codebase for related patterns
 2. Propose a plan with files to change
 3. Identify risks
 Do NOT write code yet."
```

Review the plan. Adjust it. Then: "Execute the plan, starting with [phase 1]."

**Step 4: Deploy Subagents**

Give Claude Code a task with independent subtasks:

```
"Do these in parallel using subagents:
 1. Search the codebase for all TODO comments and summarize them
 2. Check which dependencies are outdated (run npm outdated)
 3. Analyze the test coverage and identify untested files"
```

Watch Claude Code dispatch three subagents and synthesize their results.

**Step 5: Create a Custom Skill**

Create `.claude/skills/new-component.md`:

```markdown
# Skill: new-component

When creating a new React component:
1. Create file at `src/components/{name}/{name}.tsx`
2. Use Server Component by default (no 'use client')
3. Add TypeScript interface for props
4. Handle loading, error, empty, and success states
5. Create test at `src/components/{name}/{name}.test.tsx`
6. Run tests to verify
```

Test it: "Use the new-component skill to create a UserProfile component."

**What you should observe:** Claude Code reading your CLAUDE.md, following your conventions, using subagents for parallel work, and executing skills as reusable workflows. This is the difference between using Claude Code as a chatbot and using it as a technical co-founder.

</div>

---

**Chapter endnotes**

1. Claude Code was first released as a research preview in February 2025 and reached general availability in March 2025. The agent-first terminal interface was a deliberate design choice by Anthropic to differentiate from IDE-based approaches.

2. Boris Cherny's 10 principles were originally published on the Anthropic blog in early 2026 under the title "Tips for getting the most out of Claude Code." Cherny is a software engineer at Anthropic who contributed to Claude Code's development.

3. The 5.5x token efficiency comparison comes from Anthropic's benchmarking data, comparing identical coding tasks performed in Claude Code vs. Cursor. The methodology measured total tokens consumed (input + output) across both tools for the same set of 50 programming tasks.

4. The 72.2% autonomous bug resolution rate is from Anthropic's internal metrics on their own codebase, as reported in their February 2026 engineering blog post.

5. Git worktrees were introduced in Git 2.5 (July 2015) but saw limited adoption until AI coding tools made parallel development workflows practical. The `git worktree add` command creates a new linked working tree.

6. MCP (Model Context Protocol) was open-sourced by Anthropic in November 2024 as a standard for connecting AI models to external tools and data sources. OAuth support was added in the 1.1 specification in early 2026.

7. Agent teams were announced as an experimental feature in Anthropic's October 2025 release notes. As of March 2026, they remain in beta with known limitations around merge conflict resolution.

8. PostCompact hooks and autoMemoryDirectory were introduced in the Claude Code 2.x release series in January-February 2026, addressing the persistent challenge of context loss during long coding sessions.

9. The "Technical Co-Founder Framework" (Discovery → Planning → Building → Polish → Handoff) is the author's synthesis of patterns observed across hundreds of Claude Code sessions, not an official Anthropic framework.

10. The $20/month Claude Pro pricing includes Claude Code access with usage limits. Anthropic also offers Claude Max at $100/month and $200/month tiers with higher limits, and Team/Enterprise plans with per-seat pricing.
