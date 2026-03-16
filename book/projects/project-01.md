<div class="milestone-project">
<h2>Milestone Project 1: Personal Website + Blog</h2>
<p>Everything from Part I, integrated into one real product. A responsive personal site with dark mode, a contact form, a markdown-powered blog, and a real URL anyone in the world can visit.</p>
</div>

**Companion repo:** `builders-bible/project-01-personal-site`

**Time estimate:** 6-10 hours across 2-3 sessions

**What this proves you can build:** A complete, deployed, full-stack web application — the fundamental unit of the modern internet.

---

## Why This Project

Every concept in Part I was taught in isolation. You learned DNS, but you didn't configure a domain. You learned HTTP, but you didn't handle a form submission. You learned databases, but you didn't persist a blog post. You learned deployment, but you didn't push to a real URL.

This project forces integration. And integration is where things break.

When your contact form sends a POST request to your backend, you'll feel HTTP methods in your hands. When your dark mode toggle persists across page reloads because of `localStorage`, you'll understand client-side state in a way no diagram could teach. When your markdown blog post renders as HTML, you'll see the parser doing the exact text transformation you read about in Chapter 2.

More importantly, when something doesn't work — and something *will* not work — you'll debug it with the mental models from eight chapters of foundation. You'll check the Network tab and actually understand what you're seeing.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    Your Domain                       │
│              yourname.dev (via Vercel)               │
├─────────────────────────────────────────────────────┤
│                                                      │
│   ┌─────────────┐  ┌──────────────┐  ┌───────────┐ │
│   │  Home Page   │  │  Blog Index  │  │  Contact   │ │
│   │  (static)    │  │  (static)    │  │  (form)    │ │
│   └─────────────┘  └──────┬───────┘  └─────┬─────┘ │
│                           │                  │       │
│                    ┌──────┴───────┐   ┌──────┴─────┐│
│                    │  /blog/[slug]│   │  /api/      ││
│                    │  (MDX render)│   │  contact    ││
│                    └──────┬───────┘   └──────┬─────┘│
│                           │                  │       │
│                    ┌──────┴───────┐   ┌──────┴─────┐│
│                    │  /content/   │   │  Resend     ││
│                    │  *.mdx files │   │  (email)    ││
│                    └──────────────┘   └────────────┘│
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Tech stack:**
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Blog engine:** MDX (Markdown + JSX) with `next-mdx-remote`
- **Contact form:** Server Action + Resend API for email delivery
- **Dark mode:** CSS custom properties + `localStorage` + system preference detection
- **Deployment:** Vercel (free tier, connected to GitHub)
- **Domain:** Any registrar — Cloudflare recommended for DNS

---

## What You'll Build, Step by Step

### Phase 1: Scaffold and Layout (Session 1)

You'll start a conversation with Claude Code:

> "Create a Next.js 14 app with Tailwind CSS. I need a responsive layout with a header (logo, nav links: Home, Blog, Contact), a main content area, and a footer. Mobile-first. The nav should collapse to a hamburger menu on mobile."

This alone exercises Chapter 1 (HTTP and how pages load), Chapter 2 (HTML/CSS/responsive design), and Chapter 8 (project structure). Claude Code will generate the scaffold. Your job: review every file it creates. Understand the routing. Trace how a request to `/blog` maps to a file on disk.

### Phase 2: Design System and Dark Mode (Session 1)

Next, you'll implement a proper design system — not random color values scattered across files, but CSS custom properties that change when the theme switches.

The dark mode toggle teaches you client-side state management, the `prefers-color-scheme` media query, and the flash-of-unstyled-content problem (your page briefly flashes white before JavaScript runs and applies dark mode). The solution — a blocking script in `<head>` — is your first encounter with the render-blocking trade-off from Chapter 2.

### Phase 3: Blog Engine (Session 2)

Your blog posts live as `.mdx` files in a `/content` directory. Each file has frontmatter (title, date, description) and markdown body. The build process reads these files, parses the frontmatter, renders the markdown to HTML, and generates static pages.

This is the content pipeline pattern you'll see everywhere in production: content as data, transformation at build time, static delivery for performance.

You'll ask Claude Code to:
- Create a utility that reads all `.mdx` files and returns sorted metadata
- Build a blog index page that lists all posts
- Build a dynamic `[slug]` page that renders a single post
- Add syntax highlighting for code blocks (because your blog will have code)

### Phase 4: Contact Form (Session 2)

The contact form is your first server-side interaction. A user fills in their name, email, and message. They click submit. A Server Action processes the form data, validates it (never trust client input — Chapter 3), sends an email via the Resend API, and returns a success or error state.

This exercises: HTML forms, HTTP POST, server-side validation, API integration, environment variables for secrets, error handling, and user feedback (toast notification on success, error message on failure).

### Phase 5: Deployment (Session 3)

You'll connect your GitHub repository to Vercel, configure environment variables, deploy, and point a custom domain at it. Then you'll verify:

- The site loads over HTTPS (Chapter 1: TLS)
- DNS resolves correctly (Chapter 1: DNS)
- Pages load in under 2 seconds (Chapter 6: performance)
- The contact form works in production (Chapter 3: environment-specific config)
- Dark mode persists across sessions (Chapter 2: localStorage)
- The blog renders all posts (Chapter 8: build process)

### Phase 6: Polish and Ship (Session 3)

SEO metadata. Open Graph images so your links look good when shared on LinkedIn. A favicon. A 404 page. Lighthouse audit to verify performance, accessibility, and best practices. This is the difference between a project and a product.

---

## What Will Go Wrong (And What It Teaches)

Every builder hits these. They're not bugs — they're curriculum:

- **Hydration mismatch from dark mode.** Your server renders light mode. Your client applies dark mode. React complains. This teaches you server vs. client rendering — the most important architectural concept in modern web development.
- **Contact form works locally, fails in production.** You forgot to add the `RESEND_API_KEY` environment variable in Vercel. This teaches you environment configuration.
- **Blog post shows raw markdown instead of HTML.** The MDX processing step is missing or misconfigured. This teaches you build pipelines.
- **Mobile nav doesn't close after clicking a link.** State management on interactive components. This teaches you event handling.

Each failure is a chapter coming alive. Debug with the mental model, not by guessing.

---

## Definition of Done

Your project is complete when a stranger can:

1. Visit `yourname.dev` from their phone
2. Read a blog post you wrote
3. Toggle dark mode and have it stick when they refresh
4. Send you a message through the contact form — and you receive the email
5. Share a blog post link on WhatsApp and see a proper preview card

That's a real product. You built it. With AI as your co-pilot and eight chapters of understanding as your foundation.
