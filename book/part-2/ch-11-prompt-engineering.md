<span class="chapter-number">Chapter 11</span>

# Prompt Engineering → Context Engineering {.chapter-title}

You know that friend who walks into a restaurant and says "Give me something good" — and then complains about what arrives? Compare that to the friend who says: "I want something spicy, no dairy, under 500 calories, and similar to the Thai basil chicken I had last time."

Same restaurant. Same chef. Wildly different results. The difference is not the kitchen — it's the quality of the request.

Working with AI is the same. The model is the kitchen. Your prompt is the order. And most people are walking in and saying "give me something good" — then blaming the kitchen when they get bland soup.

This chapter will teach you to give precise, well-structured orders. More importantly, it will teach you that the real leverage isn't in the order itself — it's in the entire context you provide before the order is even placed.

---

## Part 1: Prompting Is a Skill, Not Typing

### The Illusion of Simplicity

> **ANALOGY**: Consider the difference between talking *to* someone and talking *with* someone. When you talk *to* someone, you say whatever comes to mind and hope they figure it out. When you talk *with* someone, you gauge their background, adjust your vocabulary, provide the right context, check understanding, and course-correct. Prompting AI well is talking *with* the model, not *at* it.

Here is a real test. Ask any LLM: "Write a product requirements document." You will get a generic template filled with placeholder text that could describe a weather app, a social network, or a tax calculator. The output is technically correct and practically useless.

Now try: "You are a senior PM at a B2B SaaS company serving mid-market Indian logistics firms. Write a PRD for a real-time fleet tracking dashboard. The primary users are fleet managers with 50-200 trucks who currently track via phone calls. The key metric is reducing average 'truck location unknown' time from 4 hours to 15 minutes. Include technical constraints: the solution must work on 3G networks in rural Rajasthan and integrate with Fasttag toll data. Format: problem statement, user personas, success metrics, feature prioritization using RICE, and technical requirements."

> **REAL-LIFE**: In 2023, a product team at a fintech startup spent two weeks manually writing regulatory compliance documentation. A colleague fed the same requirements to Claude with detailed context about the specific regulations (RBI's digital lending guidelines), the company's loan products, their risk categories, and three examples of compliant documentation from similar companies. The model produced a first draft in four minutes that required one day of review instead of two weeks of writing. The difference was not the model's intelligence. The same model was available to the entire team. The difference was one person's ability to construct context.

> **INTUITION**: Prompting is not typing. Typing is pressing keys. Prompting is the deliberate construction of an information environment that makes it easy for the model to produce the right output. A well-constructed prompt is an act of empathy — you are thinking from the model's perspective about what it needs to know. This is a skill, and like all skills, it improves with practice and degrades with assumption.

### The Three Eras of Talking to AI

The way humans communicate with AI models has evolved through three distinct phases:

**Era 1: Keyword Search (2000–2022)**
You gave machines keywords. "best biryani Bangalore delivery." The machine matched keywords against a database index. No understanding. No conversation. Retrieval, not reasoning.

**Era 2: Prompt Engineering (2023–2025)**
Transformer-based models arrived, and people discovered that *how* you asked mattered enormously. "Write me a poem" and "Write a melancholic haiku about Mumbai monsoons in the style of Gulzar" produced fundamentally different outputs from the same model. An entire discipline emerged: prompt engineering. People studied which words, formats, and structures extracted the best outputs. It was an era of clever tricks — chain-of-thought, few-shot examples, role prompts, temperature tuning.

**Era 3: Context Engineering (2026–present)**
The frontier moved beyond the prompt itself. Researchers and practitioners realized that the single most important factor in AI output quality was not the prompt — it was the *total context* surrounding the prompt. This includes: what the model was told about itself (system prompts), what examples it was shown (few-shot), what documents were retrieved and injected (RAG), what tools the model could access, what memory it had from previous interactions, and what structured constraints governed its output.

Simon Willison, one of the most respected voices in practical AI engineering, coined the shift: "Prompt engineering is about the question. Context engineering is about the entire information environment in which the question is asked." The prompt is one line. The context is the architecture.

```
THE EVOLUTION OF TALKING TO AI

┌────────────────────────────────────────────────────────────┐
│                                                            │
│  ERA 1: KEYWORD SEARCH (2000-2022)                        │
│  ┌──────────────────────────────────────────┐              │
│  │ Input: "best biryani bangalore"          │              │
│  │ Engine: Match keywords → rank by SEO     │              │
│  │ Output: 10 blue links                    │              │
│  │ Intelligence: None (pattern matching)    │              │
│  └──────────────────────────────────────────┘              │
│                         ↓                                  │
│  ERA 2: PROMPT ENGINEERING (2023-2025)                     │
│  ┌──────────────────────────────────────────┐              │
│  │ Input: Carefully worded natural language  │              │
│  │ Engine: LLM processes prompt → generates  │              │
│  │ Output: Coherent, customized text        │              │
│  │ Intelligence: Prompt (the question)      │              │
│  └──────────────────────────────────────────┘              │
│                         ↓                                  │
│  ERA 3: CONTEXT ENGINEERING (2026+)                        │
│  ┌──────────────────────────────────────────┐              │
│  │ Input: System prompt + retrieved docs +  │              │
│  │        memory + tools + few-shot + prompt│              │
│  │ Engine: LLM with full knowledge infra    │              │
│  │ Output: Accurate, grounded, constrained  │              │
│  │ Intelligence: The entire environment     │              │
│  └──────────────────────────────────────────┘              │
│                                                            │
│  Key insight: Prompt engineering tweaks the question.      │
│  Context engineering builds the knowledge infrastructure.  │
└────────────────────────────────────────────────────────────┘
```

---

## Part 2: The Six Core Prompting Techniques

Before you engineer context, you need to master the prompt itself. Six techniques form the foundation. Each one is a distinct tool, and the best practitioners combine them fluently.

### Technique 1: Zero-Shot — Ask Directly

**Zero-shot prompting** means asking the model to do something without providing any examples of what "done well" looks like. You rely entirely on the model's training data.

> **ANALOGY**: Imagine handing a task to a new hire on their first day without showing them any examples of past work. You say: "Write a customer email about our delayed shipment." They have general knowledge of email writing, but no idea about your company's tone, format, or what previous apology emails looked like. They will produce something reasonable and generic.

**When it works:** Simple, well-defined tasks where the model's general knowledge is sufficient.

**Example:**

```
Summarize this customer feedback into 3 bullet points:
"I love the app design but the checkout flow is confusing. I abandoned my
cart twice because I couldn't find where to enter my coupon code. Also,
the app crashes on my Samsung Galaxy M31 running Android 12 every time I
try to upload a profile picture."
```

The model will produce a competent summary. No examples needed because summarization is a well-understood task with clear expectations.

**When it fails:** Complex, domain-specific, or format-sensitive tasks. If you ask "Classify this support ticket by priority" with no examples, the model will guess at what your priority levels are and apply its own logic, which will rarely match your company's triage criteria.

### Technique 2: Few-Shot — Show, Don't Tell

**Few-shot prompting** means providing 2-5 examples of the input-output pattern you want before giving the actual task. The model learns the pattern from your examples and applies it to the new input.

> **ANALOGY**: Instead of telling the new hire "write a customer email," you hand them three emails that your team sent in similar situations. "Read these. Notice the tone, the structure, the way we acknowledge the issue before offering a solution. Now write one for this new case." The examples do more work than any instruction ever could.

This is one of the most powerful and underused techniques. Sander Schulhoff's research demonstrated that on certain classification tasks, models went from 0% accuracy with zero-shot prompting to over 90% accuracy with well-chosen few-shot examples — using the exact same model, the exact same task, with the only difference being three examples in the prompt.

**Example — Classifying support tickets by priority:**

```
Classify each support ticket into: P0 (service down), P1 (major feature broken),
P2 (minor bug), P3 (feature request).

Examples:

Ticket: "I can't log in. The login page shows a 500 error for all users
in our organization. We have 200 people blocked."
Priority: P0
Reasoning: Complete authentication failure affecting all users in an org.

Ticket: "The CSV export is missing the 'date created' column that was
there last week."
Priority: P1
Reasoning: Feature that existed is now broken, affects data workflows.

Ticket: "When I resize the browser window to less than 400px, the sidebar
overlaps the main content area."
Priority: P2
Reasoning: Visual bug affecting edge case screen size, no data loss.

Ticket: "It would be great if we could set custom colors for each project
in the dashboard."
Priority: P3
Reasoning: Enhancement request, no existing functionality is broken.

Now classify:

Ticket: "The Stripe webhook isn't processing subscription renewals. We've
had 47 failed renewals in the last 3 hours and customers are losing access
to paid features."
Priority:
```

The model will output P0 with correct reasoning — not because it was told the definition of P0 in an abstract way, but because it saw the pattern. The examples carry information that definitions cannot: implicit thresholds, tone of urgency, the relationship between impact scope and priority level.

> **INTUITION**: Few-shot examples work because they exploit the model's core capability: pattern recognition. The model does not memorize your examples as rules. It identifies the underlying pattern — "ah, when the impact is broad and the functionality is completely broken, the human assigns P0" — and applies that pattern to new inputs. The better your examples span the edge cases, the more robust the model's pattern extraction becomes.

### Technique 3: Chain-of-Thought — Think Step by Step

**Chain-of-thought (CoT) prompting** asks the model to show its reasoning process, step by step, before arriving at a final answer. The landmark paper by Wei et al. (2022) demonstrated that adding the phrase "Let's think step by step" to a math problem increased accuracy from 17.7% to 78.7% on a standard benchmark — a 4x improvement from five additional words.

> **ANALOGY**: Two students take an exam. Student A reads "What is 17 × 24?" and writes "408" — correct. Student B reads the same problem and writes: "17 × 24 = 17 × 20 + 17 × 4 = 340 + 68 = 408." Both get the right answer, but Student B's approach works more reliably on harder problems. When the question becomes "What is 347 × 892?", Student A's "guess the answer" approach breaks down while Student B's step-by-step decomposition still works. Chain-of-thought turns the model into Student B.

**Why does this work?** The model generates tokens sequentially. Each token depends on all previous tokens. When you ask for reasoning steps, the model's intermediate tokens (the reasoning) become scaffolding for the final answer. Without reasoning steps, the model must leap directly from question to answer — and longer leaps have higher error rates.

**Example — Pricing decision analysis:**

```
We're considering raising the price of our SaaS product from ₹999/month to
₹1,499/month. We have 2,400 paying customers. Our monthly churn rate is 4%.
Customer acquisition cost is ₹3,200. Average customer lifetime is 25 months.

Should we raise the price? Think through this step by step, considering:
the revenue impact, expected churn increase from price sensitivity, break-even
analysis, and the effect on customer lifetime value.
```

Without CoT, the model might say "Yes, raising prices is generally beneficial if your product delivers value." With CoT, the model will calculate current MRR (₹23,97,600), project new MRR at different churn rates, calculate the break-even churn increase (the point where increased revenue per customer is offset by increased customer loss), and arrive at a quantified recommendation with specific thresholds: "You can afford up to X% additional churn before the price increase becomes net negative."

### Technique 4: System Prompts — The Job Description

A **system prompt** is a special instruction block sent to the model before the user's message, typically invisible to the end user. It defines the model's behavior, constraints, tone, and scope.

> **ANALOGY**: A system prompt is a job description handed to a new employee on day one. It says: "You work at a healthcare company. You speak in simple, reassuring language. You never give medical diagnoses. You always recommend consulting a doctor for specific symptoms. You respond in Hindi if the user writes in Hindi." The employee (model) internalizes this context and applies it to every interaction that follows.

System prompts are where organizations encode their product's personality, safety constraints, and behavioral guardrails.

**Example — a customer support bot for an edtech company:**

```
SYSTEM PROMPT:
You are a support assistant for Rethink, an online education platform for
product managers. Your role:

1. TONE: Warm, professional, encouraging. These are working professionals
   investing in their career growth. Respect their time.

2. SCOPE: You can help with:
   - Course content questions and clarifications
   - Technical issues (login, video playback, assignment submission)
   - Billing and refund policies (refund within 7 days, no questions asked)
   - Session scheduling and recording access

3. BOUNDARIES: You CANNOT:
   - Promise placement or salary outcomes
   - Share other students' information
   - Make claims about course rankings or "guaranteed" results
   - Discuss internal business metrics

4. ESCALATION: If a user is angry, frustrated, or mentions legal action,
   respond empathetically and offer: "I'd like to connect you with our
   student success team directly. Can I have them reach out to you within
   2 hours?"

5. FORMAT: Keep responses under 150 words unless the user asks for detail.
   Use numbered steps for troubleshooting. End each response with a clear
   next action.
```

This system prompt transforms a general-purpose language model into a specific, bounded, on-brand support agent. Without it, the model would answer questions accurately but inconsistently — sometimes formal, sometimes casual, sometimes overstepping into promises the company cannot keep.

### Technique 5: Role Prompting — "You Are..."

**Role prompting** assigns the model a specific identity, expertise, or perspective. It overlaps with system prompts but can also be used inline within a conversation.

> **REAL-LIFE**: A product manager at a healthtech startup used role prompting to pressure-test a feature spec. She sent the same PRD to Claude four times, each with a different role: "You are a senior backend engineer — find every technical risk in this spec," "You are a regulatory compliance officer — identify every HIPAA concern," "You are a first-time user with low tech literacy — walk through this flow and tell me where you get confused," and "You are the CFO — challenge the ROI assumptions." Four perspectives from one model, each surfacing blindspots the others missed. The backend engineer role caught a race condition in the payment flow. The compliance role flagged three missing consent checkpoints. The naive user role revealed that the onboarding assumed familiarity with medical terminology. The CFO role questioned a customer acquisition cost that assumed organic growth rates that the company had never achieved.

**Example:**

```
You are a senior data analyst at a Series B fintech startup. You've seen
three companies scale from 10K to 500K users. You're skeptical of vanity
metrics and always push for actionable insights.

I'm going to share our product dashboard metrics from last month. For each
metric, tell me: (1) whether it's a leading or lagging indicator, (2) what
action it suggests, and (3) what additional data you'd want before making
a decision.
```

### Technique 6: Structured Output — "Respond in JSON with Keys..."

**Structured output prompting** constrains the model's response format to a specific schema — JSON, XML, Markdown tables, YAML, or any defined structure.

> **ANALOGY**: Imagine you ask five people to describe their commute. Without structure, you get: a rambling story, a single sentence, a numbered list, a time breakdown, and a complaint about traffic. Each is valid. None is comparable. Now imagine you give each person a form: origin, destination, mode of transport, duration in minutes, one-sentence summary. The responses become structured, comparable, and machine-readable. Structured output prompting is giving the model a form to fill out instead of a blank page.

This matters enormously for building AI into products. If your backend expects JSON, a well-formatted but unstructured paragraph is useless.

**Example:**

```
Analyze this user feedback and respond in JSON with the following schema:

{
  "sentiment": "positive" | "negative" | "mixed",
  "primary_issue": "string (one sentence)",
  "feature_mentioned": "string or null",
  "urgency": "low" | "medium" | "high",
  "suggested_action": "string (one sentence)",
  "confidence": 0.0-1.0
}

Feedback: "Your new AI search feature is incredible — it found exactly what
I needed in seconds. But it completely breaks when I search in Hindi. I type
in Devanagari script and get English results that have nothing to do with my
query. This is a dealbreaker for our team since 60% of our users search in
Hindi."
```

The model returns a clean JSON object that your code can parse, store, and act on. Without structured output constraints, the model would write a paragraph — useful for a human reading it, useless for a system processing it.

### Comparison Table: The Six Techniques

```
┌─────────────────┬───────────────────────────┬──────────────────────────┬──────────────────┐
│ Technique       │ What You Provide          │ Best For                 │ Key Risk          │
├─────────────────┼───────────────────────────┼──────────────────────────┼──────────────────┤
│ Zero-shot       │ Task description only     │ Simple, common tasks     │ Generic output    │
│                 │                           │ (summaries, translations)│                  │
├─────────────────┼───────────────────────────┼──────────────────────────┼──────────────────┤
│ Few-shot        │ 2-5 input/output examples │ Classification, format-  │ Bad examples      │
│                 │ + task description        │ sensitive tasks, domain- │ teach bad         │
│                 │                           │ specific work            │ patterns          │
├─────────────────┼───────────────────────────┼──────────────────────────┼──────────────────┤
│ Chain-of-thought│ "Think step by step" or   │ Math, logic, multi-step  │ Slower, more      │
│                 │ explicit reasoning request│ analysis, comparisons    │ tokens, higher    │
│                 │                           │                          │ cost              │
├─────────────────┼───────────────────────────┼──────────────────────────┼──────────────────┤
│ System prompt   │ Behavioral instructions   │ Product bots, consistent │ Overly rigid      │
│                 │ before the conversation   │ tone, safety constraints │ rules = brittle   │
│                 │                           │                          │ responses         │
├─────────────────┼───────────────────────────┼──────────────────────────┼──────────────────┤
│ Role prompting  │ "You are a [persona]..."  │ Perspective-taking,      │ Role conflicts    │
│                 │                           │ expertise simulation,    │ with system       │
│                 │                           │ stress-testing ideas     │ prompt            │
├─────────────────┼───────────────────────────┼──────────────────────────┼──────────────────┤
│ Structured      │ Output schema (JSON,      │ API responses, data      │ Schema too        │
│ output          │ table, YAML)              │ extraction, pipeline     │ complex = model   │
│                 │                           │ integration              │ hallucinates      │
│                 │                           │                          │ fields            │
└─────────────────┴───────────────────────────┴──────────────────────────┴──────────────────┘
```

These six techniques are not mutually exclusive. The most effective prompts combine several of them. A production AI feature might use a system prompt (Technique 4) that assigns a role (Technique 5), includes few-shot examples (Technique 2), requests chain-of-thought reasoning (Technique 3), and demands structured JSON output (Technique 6). That combination — layered, deliberate, and specific — is what separates a proof-of-concept from a production-grade AI feature.

---

## Part 3: From Prompt Engineering to Context Engineering

### The Ceiling of Prompting

Here is the uncomfortable truth: no matter how brilliant your prompt is, it operates within the model's context window — and the prompt itself is a vanishingly small fraction of what determines output quality.

Consider a customer support bot. You can write the perfect system prompt with the perfect tone guidelines and the perfect escalation rules. But when a customer asks "Where is my order #4821?", the prompt alone cannot help. The model needs access to your order database. It needs the customer's order history. It needs your shipping provider's tracking API. It needs your return policy document from last month (not the one from two years ago that's been superseded).

This is the shift from prompt engineering to **context engineering** — designing the entire information environment the model operates within, not tweaking the instructions.

> **ANALOGY**: Prompt engineering is writing a better exam question. Context engineering is designing the entire classroom — the textbooks on the desk, the reference materials allowed, the calculator policy, the time constraints, and the scoring rubric. The question matters, but the environment shapes performance far more.

### The Four Pillars of Context Engineering

**Pillar 1: Persistent Instructions (CLAUDE.md, System Prompts)**

These are instructions that persist across every interaction. In Claude Code, the `CLAUDE.md` file serves this function — it tells the model about your project's architecture, coding conventions, past decisions, and known pitfalls *before* any specific task is given.

A well-crafted CLAUDE.md file for a SaaS dashboard project might contain:

```
## Architecture
- Next.js 15 App Router, TypeScript strict mode
- Supabase for auth and database, RLS enabled on all tables
- Server Components by default, Client Components only for interactivity

## Conventions
- API routes in app/api/, grouped by domain (users/, sessions/, analytics/)
- All database queries go through typed helper functions in lib/db/
- Error handling: never expose internal errors to client, use AppError class

## Known Issues
- Supabase RLS + service role key: always use service role for admin operations
- The sessions table has a composite primary key — ORM doesn't handle this well
- Rate limiting is NOT implemented on /api/auth/* — do not deploy without it

## Past Mistakes
- 2026-02-14: Used client-side date formatting, caused timezone bugs for
  users in IST vs UTC. Fix: always store and compare in UTC, format on display.
- 2026-03-01: Forgot to invalidate cache after bulk user import. 200 users
  saw stale dashboard data for 6 hours.
```

This file means the model never makes those mistakes again. It never suggests client-side date formatting. It never forgets about RLS. It never uses the wrong key for admin operations. The context prevents the error class, not individual error instances.

**Pillar 2: Retrieval-Augmented Generation (RAG)**

RAG injects relevant documents into the model's context at query time. Instead of relying on the model's training data (which has a knowledge cutoff), RAG pulls live information from your databases, documents, or APIs and feeds it into the prompt.

> **REAL-LIFE**: A legal tech startup built an AI contract reviewer. Without RAG, the model applied general legal knowledge — accurate for US contract law but wrong for Indian contract law under the Indian Contract Act, 1872. With RAG, the system retrieved the relevant sections of Indian law, SEBI regulations, and the company's own clause library before generating each review. Accuracy on Indian-specific clauses went from 34% to 91%. The model did not become smarter. It became better informed.

**Pillar 3: Tool Use**

Modern LLMs can call external tools — APIs, databases, calculators, code interpreters, search engines. Instead of hallucinating an answer about your current stock price, the model calls a financial data API and returns the real number.

Tool use transforms the model from a "know-it-all who sometimes lies" into a "reasoning engine with access to truth." The model decides *when* to use a tool, *which* tool to use, and how to incorporate the tool's output into its response.

**Pillar 4: Memory**

Memory allows models to retain information across conversations. Without memory, every conversation starts from zero — you re-explain your project, your preferences, your constraints. With memory, the model accumulates context over time: "This user prefers TypeScript over JavaScript, works on a healthcare product, has strict HIPAA requirements, and tends to ask follow-up questions about edge cases."

Memory is the difference between a stranger and a colleague. A stranger needs a full briefing every time. A colleague knows your context and can jump straight to the problem.

```
CONTEXT ENGINEERING: THE FOUR PILLARS

             ┌─────────────────────────────────────────┐
             │           MODEL + PROMPT                 │
             │   (the question you're asking today)     │
             └──────────────────┬──────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  PERSISTENT  │     │     RAG      │     │    TOOLS     │
│ INSTRUCTIONS │     │  Retrieved   │     │   APIs,      │
│              │     │  documents   │     │   databases, │
│ CLAUDE.md    │     │  injected at │     │   code exec, │
│ System       │     │  query time  │     │   search     │
│ prompts      │     │              │     │              │
│ Memory       │     │ Your docs,   │     │ Live data,   │
│              │     │ your data    │     │ real actions  │
└──────────────┘     └──────────────┘     └──────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
                    ┌──────────────────┐
                    │  HIGH-QUALITY    │
                    │  GROUNDED        │
                    │  OUTPUT          │
                    └──────────────────┘

The prompt is one input. Context engineering designs ALL the inputs.
```

---

## Part 4: Common Mistakes (and How to Fix Them)

### Mistake 1: Vague Prompts

**Bad:** "Help me with my product strategy."
**Better:** "I'm the PM for a B2B expense management tool targeting 50-200 employee Indian startups. Our activation rate (first expense report submitted within 7 days of signup) dropped from 38% to 22% last quarter. Revenue is ₹18L MRR. Help me diagnose the three most likely causes and propose one experiment for each."

The bad prompt forces the model to guess your industry, company size, stage, problem, and desired output format. Every guess is a coin flip. Five guesses = 2^5 = 32 possible interpretation combinations. The odds of the model guessing your exact situation are roughly 3%.

### Mistake 2: No Examples

When you need a specific format or judgment call, abstract instructions fail where examples succeed. "Classify customer feedback by sentiment" is ambiguous. Does "The app works but could be faster" count as positive (it works) or negative (could be faster) or mixed? An example resolves the ambiguity instantly.

### Mistake 3: No Constraints

Without constraints, models produce the average of their training distribution. That average is verbose, generic, and hedged. Constraints create specificity:

- "Under 100 words" (length)
- "For a non-technical audience" (complexity)
- "Using only data from the attached CSV" (source)
- "Do not suggest solutions that require engineering changes" (scope)
- "In the format of a Slack message to your engineering lead" (format + audience)

### Mistake 4: Too Much Noise

The opposite of too little context is too much irrelevant context. Dumping your entire company wiki into a prompt does not help — it hurts. The model's attention mechanism (Chapter 10) distributes focus across all input tokens. Irrelevant tokens dilute attention from relevant ones.

> **INTUITION**: Think of context like ingredients in a dish. A good cook selects five or six ingredients that work together. A bad cook dumps everything in the pantry into the pot, hoping quantity compensates for lack of curation. Context engineering is curation — selecting the *right* information, not the *most* information.

### Mistake 5: Not Iterating

Most people write one prompt, evaluate the output, and either accept it or give up. Effective prompting is iterative. You send a prompt, evaluate the output, identify the gap between what you got and what you wanted, diagnose why the gap exists, modify the prompt to close that gap, and repeat. This loop typically takes 3-7 iterations to converge on a high-quality result.

---

## Part 5: The Anatomy of Iteration — A Prompt in Five Versions

Here is a real task: you need an AI to generate a weekly product metrics summary for your team's Slack channel. Watch how the prompt evolves.

**Version 1: The Starting Point**

```
Summarize our product metrics for this week.
```

**Output:** A generic paragraph about the importance of tracking metrics, with no actual data, no structure, no actionable insight.

**What went wrong:** No data provided. No format specified. No context about what "our product" is.

---

**Version 2: Adding Context**

```
Here are our product metrics for the week of March 10-16, 2026:
- DAU: 12,400 (prev week: 11,800)
- Signup-to-activation rate: 23% (prev week: 28%)
- Weekly revenue: ₹4.2L (prev week: ₹3.9L)
- Support tickets: 340 (prev week: 280)
- NPS score: 42 (prev week: 45)

Summarize these for the team.
```

**Output:** A decent paragraph restating the numbers with basic directional commentary ("DAU increased, activation rate decreased"). Accurate but not insightful.

**What went wrong:** No format. No analysis depth. The model treated "summarize" as "restate."

---

**Version 3: Adding Format and Depth**

```
Here are our product metrics for the week of March 10-16, 2026:
[same data as above]

Write a Slack message for the #product-updates channel. Format:
- One emoji + one sentence headline (good news or bad news lead)
- Each metric on its own line with ↑/↓ arrows and % change
- A "Watch" section for any metric that moved more than 10%
- End with one specific question for the team to discuss

Keep it under 200 words. Our team is 8 PMs and engineers who
prefer direct, data-first communication.
```

**Output:** Good structure, correct arrows, identifies activation rate as the one to watch. But the question at the end is generic: "What's driving the activation drop?"

**What went wrong:** No context about what might be causing changes. The model cannot connect metrics to product events without being told.

---

**Version 4: Adding Causal Context**

```
Here are our product metrics for the week of March 10-16, 2026:
[same data as above]

Context for this week:
- We launched a new onboarding flow on March 11 (redesigned signup → first action)
- A competitor (ExpenseBot) launched a free tier on March 12
- We had 3 hours of API downtime on March 14 (payments service)
- We ran a LinkedIn campaign that drove 2,100 signups (vs normal ~800/week)

Write a Slack message for the #product-updates channel.
[same format instructions as V3]

When analyzing, connect metrics to these events where the connection
is plausible. Flag connections you're uncertain about.
```

**Output:** Now the model connects the activation drop to the LinkedIn campaign (higher volume but lower-intent signups diluting the rate), notes that DAU growth correlates with the campaign, flags that support ticket increase might relate to the API downtime, and marks the competitor launch as a potential factor worth monitoring. The discussion question is specific: "Should we segment activation by acquisition channel before deciding if the new onboarding flow is working?"

**What went wrong:** Almost nothing. But the model occasionally hallucinated specific percentages for channel-level breakdowns that were not in the data.

---

**Version 5: Adding Constraints and Guardrails**

```
Here are our product metrics for the week of March 10-16, 2026:
[same data]

Context for this week:
[same events]

Write a Slack message for the #product-updates channel.

Format:
- Headline: one emoji + one sentence (lead with the most important signal)
- Metrics: each on its own line with ↑/↓ arrows, absolute numbers, and
  week-over-week % change
- "Watch" section: any metric that moved >10%, with a one-sentence
  hypothesis connecting it to this week's events
- "Unknown" section: call out anything you'd want to investigate but
  don't have data for
- End with one specific, falsifiable question for the team

Rules:
- ONLY use numbers from the data I provided. Do not invent breakdowns
  or channel-specific numbers.
- If a causal connection is uncertain, say "possibly linked to" not
  "caused by"
- Under 250 words
- No jargon the team wouldn't use in daily conversation
```

**Output:** A crisp, trustworthy weekly summary that the PM could copy-paste into Slack with minimal editing. Metrics are accurate, hypotheses are hedged appropriately, the "Unknown" section asks about channel-level activation data, and the discussion question is sharp and testable.

**The lesson:** Five versions. Same model, same data. The output quality improved not because the model got smarter between versions, but because the prompt got more precise about *what good looks like*.

---

## Part 6: Context Engineering in the Wild

### How Professional Teams Use Context Engineering Today

**Claude Code with CLAUDE.md files:** Engineering teams maintain project-level instruction files that encode architectural decisions, coding standards, and past mistakes. The model reads these files before every task. The result: an AI pair programmer that knows your codebase's conventions, avoids your team's known pitfalls, and improves over time as the file is updated.

**RAG-powered support systems:** Companies like Intercom, Zendesk, and dozens of startups use retrieval-augmented generation to power customer support. When a customer asks a question, the system retrieves the three most relevant help articles, the customer's account history, and their recent support interactions — then feeds all of this into the model alongside the system prompt. The model answers with specific, accurate, account-aware information instead of generic help text.

**Agentic workflows with tool use:** AI agents that can book meetings, query databases, send emails, and update project management tools. These agents do not rely on prompts alone — they rely on tool definitions, access permissions, and orchestration logic that constitute the full context of what the agent can and cannot do.

**Memory-augmented personal assistants:** Systems that remember your preferences, your project history, your communication style, and your recurring tasks. Each conversation builds on previous ones. The memory layer means the 100th conversation is qualitatively different from the 1st — not because the model changed, but because the accumulated context is richer.

---

<div class="exercise">
<div class="exercise-title">Exercise: The Prompt Improvement Challenge</div>

Take this deliberately bad prompt and improve it through five iterations. After each iteration, run the prompt against any LLM (ChatGPT, Claude, Gemini — it does not matter) and evaluate the output. Write down what improved and what still needs work before writing the next version.

**The bad prompt:**

```
Write a competitive analysis.
```

**Your iterations:**

1. **Add context:** What product? What market? What competitors? What is the analysis for (board presentation? Sprint planning? Investor meeting?)

2. **Add format:** What structure should the output follow? A comparison table? SWOT per competitor? Feature-by-feature matrix?

3. **Add examples:** Show one row of the comparison table filled in. Show the level of detail you want for each competitor.

4. **Add constraints:** How many competitors? How long should the output be? What sources should the model draw from (and what should it not fabricate)? What time period?

5. **Add guardrails:** What should the model *not* do? (Don't speculate on competitor revenue if not public. Don't recommend strategic decisions — present data and let the reader decide. Flag low-confidence claims.)

**Grading yourself:** If your Version 5 output is specific enough that a colleague could take action on it without asking you clarifying questions, you have succeeded. If the colleague would need to ask "but what do you mean by..." even once, iterate further.

**Bonus:** Apply the same five-step improvement process to a prompt you use in your actual work. The gap between your current prompt and Version 5 is the value of this chapter.

</div>

---

## What We Covered

This chapter traced the evolution from typing keywords into a search engine to engineering the full information environment around an AI model:

1. **Prompting is a skill** — the quality of your input determines the quality of the output, and the gap between a lazy prompt and a crafted prompt is the gap between a useless response and an actionable one.

2. **Six techniques** form the foundation: zero-shot (direct questions), few-shot (learning from examples), chain-of-thought (step-by-step reasoning), system prompts (persistent behavioral instructions), role prompting (perspective simulation), and structured output (format-constrained responses). The best prompts combine several techniques.

3. **Context engineering is the frontier** — beyond the prompt itself, the total information environment matters more: persistent instructions (CLAUDE.md), retrieved documents (RAG), tool access, and memory. Prompt engineering tweaks the question. Context engineering builds the knowledge infrastructure.

4. **Common mistakes** cluster around five patterns: vague inputs, missing examples, absent constraints, information overload, and failure to iterate.

5. **Iteration is the method** — the path from a bad prompt to a great one is not inspiration, it is five rounds of diagnosis and refinement.

The next chapter on Retrieval-Augmented Generation (RAG) builds directly on this foundation. RAG is context engineering's most powerful implementation — the system that connects your AI to your data, your documents, and your truth.

---

**Chapter endnotes**

[1] Wei, Jason, et al. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." Advances in Neural Information Processing Systems, 2022. The paper demonstrated that appending "Let's think step by step" to a prompt improved accuracy on the GSM8K math benchmark from 17.7% to 78.7% using PaLM 540B. This result established chain-of-thought as a fundamental prompting technique and spawned an entire research subfield on reasoning in LLMs.

[2] Sander Schulhoff's "The Prompt Report: A Systematic Survey of Prompting Techniques" (2024) cataloged over 60 distinct prompting techniques with benchmarks. The few-shot results cited in this chapter — 0% to 90% accuracy improvements — come from his survey of classification tasks where the model's zero-shot performance was near-random but few-shot performance approached human-level accuracy.

[3] Anthropic's prompt engineering documentation (docs.anthropic.com) provides the most thorough guide to prompting Claude models specifically, with detailed examples of system prompts, few-shot formatting, and structured output patterns. Their "Claude 4 Prompt Engineering Guide" (2026) introduced the concept of "prompt layering" — combining multiple techniques in a specific order for maximum effect.

[4] OpenAI's "Prompt Engineering Guide" and "OpenAI Cookbook" (GitHub) remain widely-referenced practical resources for GPT-family models. While model-specific, the core techniques — few-shot, chain-of-thought, structured output — transfer across model families.

[5] Simon Willison, "Context Engineering is the New Prompt Engineering," simonwillison.net, 2025. Willison, a prolific writer on practical AI engineering, articulated the shift from optimizing individual prompts to designing the entire information environment around the model. His formulation — "It's not about the question, it's about everything the model knows when it answers the question" — has become widely adopted in the AI engineering community.

[6] The CLAUDE.md pattern referenced in Part 3 was popularized by Anthropic's Claude Code tool and the broader AI-assisted development community in 2025-2026. The practice of maintaining project-level instruction files for AI tools represents one of the earliest forms of formalized context engineering in production software development.

[7] Chip Huyen, "AI Engineering" (O'Reilly, 2025), Chapter 7 covers RAG architectures and the relationship between context quality and output quality. Her framework for evaluating retrieval quality — relevance, coverage, and freshness — directly applies to the context engineering principles discussed in this chapter.
