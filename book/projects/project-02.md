<div class="milestone-project">
<h2>Milestone Project 2: AI-Powered Data Dashboard</h2>
<p>Upload a CSV, ask questions in plain English, get charts and insights. Everything from Parts I and II, working together — your first AI-integrated product.</p>
</div>

**Companion repo:** `builders-bible/project-02-ai-dashboard`

**Time estimate:** 10-15 hours across 3-4 sessions

**What this proves you can build:** A product where AI is not a gimmick but the core value proposition — the user gets answers they couldn't get without it.

---

## Why This Project

Part I taught you how software works. Part II taught you how AI works. This project is the collision.

You've read about tokens, context windows, temperature, and prompt engineering. You've understood how an LLM generates text one token at a time, how embeddings capture semantic meaning, and how structured output forces a model to return JSON instead of prose.

Now you'll feel it. When your dashboard takes 8 seconds to respond because your CSV has 50,000 rows and you're stuffing all of them into the prompt, you'll *feel* the context window limit. When the model generates a chart config that references a column named `"revenue"` but your CSV calls it `"Rev (INR, Cr.)"`, you'll understand why column name normalization matters. When Claude confidently calculates a wrong average because you sent it stringified numbers with commas, you'll learn that LLMs don't do math — they predict text that *looks* like math.

These lessons don't stick from reading. They stick from debugging at midnight.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                   │
│                                                           │
│  ┌──────────┐  ┌────────────────┐  ┌──────────────────┐ │
│  │  Upload   │  │  Chat Interface │  │  Chart Display   │ │
│  │  (drag &  │  │  (question →    │  │  (Recharts/      │ │
│  │  drop)    │  │   answer)       │  │   Chart.js)      │ │
│  └─────┬────┘  └───────┬────────┘  └────────┬─────────┘ │
│        │               │                     │            │
├────────┴───────────────┴─────────────────────┴────────────┤
│                      API Layer                            │
│                                                           │
│  /api/upload          /api/query           /api/charts    │
│  Parse CSV →          User question →      Chart config → │
│  Extract schema →     Build prompt →       Validate →     │
│  Store in Supabase    Call Claude API      Return spec    │
│                       Parse response                      │
│                       Generate chart                      │
├───────────────────────────────────────────────────────────┤
│                    Data & AI Layer                         │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │  Supabase    │  │  Claude API  │  │  Data Processing│ │
│  │  (store CSV  │  │  (reasoning  │  │  (Papa Parse,   │ │
│  │   + metadata)│  │   + charting)│  │   stats calc)   │ │
│  └──────────────┘  └──────────────┘  └────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

**Tech stack:**
- **Framework:** Next.js 14 (App Router)
- **Database:** Supabase (PostgreSQL + Row Level Security)
- **AI:** Claude API (Anthropic SDK) with structured output
- **Charts:** Recharts (React charting library)
- **CSV parsing:** Papa Parse (client-side) + server-side validation
- **Auth:** Supabase Auth (so each user sees only their data)
- **Deployment:** Vercel + Supabase (both free tier)

---

## What You'll Build, Step by Step

### Phase 1: CSV Upload and Parsing (Session 1)

The user drags a CSV file onto your dashboard. Your app parses it client-side with Papa Parse, extracts the schema (column names, data types, sample values), and uploads the raw data to Supabase.

This phase exercises: file handling APIs, data validation (what if the CSV is malformed?), Supabase storage, and the principle that you never trust user input. A CSV file is user input. It can contain formulas designed to exploit spreadsheet software. It can be 2GB. It can have inconsistent column counts. You handle all of this.

### Phase 2: Schema Intelligence (Session 1)

Before the user asks a single question, your app should understand the data. You'll build a schema analysis step that:

- Detects column types (numeric, categorical, datetime, text)
- Calculates basic statistics (min, max, mean, median for numeric columns)
- Identifies the likely "key" columns (dates, IDs, categories)
- Generates a natural language summary: "This dataset has 12,847 rows and 8 columns covering e-commerce transactions from January to December 2024. Key metrics include revenue, order count, and customer satisfaction score."

This summary becomes part of every prompt you send to Claude. It's your system context — and it's the difference between a model that gives generic answers and one that gives specific, data-grounded answers.

### Phase 3: Natural Language Query Engine (Session 2)

The user types: "What was the highest revenue month?" Your backend:

1. Takes the user's question
2. Builds a prompt that includes the schema summary, column definitions, sample rows, and the question
3. Sends it to Claude with structured output (JSON schema for the response)
4. Parses the response — which includes both a text answer and a chart configuration
5. Returns both to the frontend

The prompt engineering here is where Part II becomes real. You'll learn that sending all 50,000 rows doesn't work (context window), so you'll precompute aggregations and send summaries. You'll learn that asking for "a chart" gets unpredictable results, so you'll define a strict JSON schema for chart configs. You'll learn that the model hallucinates column names, so you'll include the exact column list in every prompt.

### Phase 4: Chart Generation (Session 3)

Claude returns a chart specification — chart type, x-axis, y-axis, data series, colors. Your frontend takes this spec and renders it with Recharts. The user sees their answer as both text and a visual.

You'll handle: bar charts, line charts, pie charts, and scatter plots. Each chart type has constraints (pie charts need categorical data, line charts need sequential x-axis). Claude picks the chart type; your frontend validates the choice and falls back gracefully if the spec is invalid.

### Phase 5: Conversation Memory (Session 3)

The user asks a follow-up: "Break that down by region." Your system needs to understand that "that" refers to the previous answer about revenue. You'll implement conversation memory — a sliding window of previous question-answer pairs included in each new prompt.

This is your first encounter with context management at a practical level. You'll balance context quality against token cost. You'll learn that including the last 5 full exchanges burns through your budget, but including compressed summaries of the last 5 exchanges is both cheaper and more effective.

### Phase 6: Auth, Polish, and Deploy (Session 4)

Supabase Auth so each user's data is private. Row Level Security so a database breach doesn't expose everyone's CSVs. Loading states while Claude thinks. Error boundaries when the API fails. Rate limiting so one user can't drain your API budget. Cost tracking so you know exactly how much each query costs.

---

## What Will Go Wrong (And What It Teaches)

- **Claude returns a chart config referencing a column that doesn't exist.** Hallucination. Your system needs a validation layer between AI output and rendering. Never trust model output without verification.
- **Queries on large datasets timeout.** You're sending too much data in the prompt. This teaches you the precomputation pattern: aggregate first, query the aggregation, not the raw data.
- **The model gives different answers to the same question.** Temperature is too high, or your prompt lacks specificity. This teaches you determinism in AI systems.
- **Charts look wrong on mobile.** Responsive design for data visualization is its own skill. Recharts handles some of it; the rest is your layout code.

---

## Definition of Done

Upload a real dataset — your Swiggy order history, your company's sales data, a public Kaggle dataset. Ask five questions in plain English. Get five accurate, visualized answers. Share the URL with someone who has never seen a terminal in their life and watch them use it without instructions.

That's the bar. Not "it works on my machine." It works for someone who doesn't know what a CSV is.
