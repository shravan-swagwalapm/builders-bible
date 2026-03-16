<span class="chapter-number">How to Read This Book</span>

# Three Paths Through One Book {.chapter-title}

Not everyone starts from the same place. This book is designed for three types of readers, and you don't have to read every page.

## Path 1: The Complete Beginner

**You**: Have never written a line of code. "Terminal" sounds intimidating. You use apps but have no idea how they're built.

**Your path**: Read everything in order. Start with Part 0. Do every exercise. The book builds on itself — each chapter assumes you've read the ones before it. By Part III, you'll be building real applications with AI tools.

**Estimated time**: 6-8 weeks at 1-2 hours per day.

## Path 2: The Adjacent Professional

**You**: A product manager, designer, data analyst, or business professional. You work with engineers daily. You understand concepts like APIs and databases at a surface level but couldn't build anything yourself.

**Your path**: Skim Part 0 (you probably don't need terminal basics). Read Part I selectively — Chapter 3 (Backend) and Chapter 4 (Databases) are gold for PMs. Dive deep into Part II (AI). Part III is where you'll spend most of your time — this is where you start building.

**Skip**: Ch 0.1, Ch 0.2 (unless you haven't set up a dev environment before).

**Estimated time**: 4-5 weeks at 1-2 hours per day.

## Path 3: The PM-Founder

**You**: Building a startup or product. You need to ship, fast. You want to understand what's possible with AI and start building immediately.

**Your path**: Read the Foreword and State of the Art. Skim Part I for reference. Read Ch 10 (LLMs), Ch 11 (Prompt Engineering), Ch 13 (RAG), Ch 15 (Agents). Then go straight to Part III and start building. Come back to Part IV when you need production concepts.

**Skip**: Parts you already understand. Come back to them as reference.

**Estimated time**: 2-3 weeks, focused on building.

---

## What You'll Need

- **A laptop** — Mac, Windows, or Linux. Any computer made after 2018 will do.
- **An internet connection** — for downloading tools and accessing AI services.
- **A Claude Pro account** — $20/month for Claude.ai, which includes Claude Code access. You can also use free tiers of Cursor, GitHub Copilot, or Gemini CLI for most exercises.
- **Curiosity** — the only prerequisite that money can't buy.

You do NOT need: a Computer Science degree, math skills beyond basic arithmetic, prior programming experience, or a powerful computer.

## The Companion Repositories

Every milestone project in this book has a companion GitHub repository with:

- **Starter code**: The starting point for each project, so you don't have to type boilerplate.
- **Solution code**: The completed project, in case you get stuck.
- **CLAUDE.md files**: Pre-configured AI context for each project.
- **Exercise files**: Starting points for chapter exercises.

Find them all at: **github.com/builders-bible**

## How the Exercises Work

Every chapter ends with a hands-on exercise. These are not optional. You will learn more from 15 minutes of building than from 2 hours of reading. Each exercise is designed to be completable in 10-20 minutes using an AI coding tool.

The exercises use Claude Code by default, but every exercise can be done with Cursor, GitHub Copilot, or any AI coding assistant. When an exercise says "Ask Claude Code to...", you can substitute your tool of choice.

## A Note on AI Tools and Pricing

The AI tool landscape changes rapidly. Prices, features, and capabilities described in this book reflect March 2026. By the time you read this, some details may have shifted. The *concepts* will remain relevant even as specific tools evolve.

We use Claude Code as our primary tool throughout the book because it's what the authors use in production. This is not an advertisement — it's an honest reflection of our workflow. Every concept works with alternative tools, and we note alternatives throughout.

## Conventions Used in This Book

Throughout the book, you'll see several recurring patterns:

> **ANALOGY**: Text in yellow boxes like this uses a real-world analogy to explain a technical concept. Read these first — they're the foundation.

> **REAL-LIFE**: Blue boxes show how a concept appears in products you already use daily.

> **INTUITION**: Purple boxes explain *why* a concept exists — the human story behind the technology.

> **EXERCISE**: Green boxes are hands-on exercises. Do them. Seriously.

Code looks like this:

```javascript
// This line creates a simple greeting message
const greeting = "Hello, Builder!";

// This line displays the message in your terminal
console.log(greeting);
```

Every code example includes plain English comments explaining what each line does.

Technical terms appear in **bold** the first time they're introduced, with a plain English definition in parentheses. Every term is also in the Glossary (Appendix D).

---

Let's build something.
