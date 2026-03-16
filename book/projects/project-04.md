<div class="milestone-project">
<h2>Milestone Project 4: Multi-Agent AI Pipeline</h2>
<p>A system that researches, writes, edits, generates images, and publishes — with multiple models orchestrated by complexity, cost tracking per run, and evaluation at every stage.</p>
</div>

**Companion repo:** `builders-bible/project-04-multi-agent-pipeline`

**Time estimate:** 15-20 hours across 5-6 sessions

**What this proves you can build:** A production AI system where no single model does everything — where agents specialize, coordinate, and produce output greater than any one of them could alone.

---

## Why This Project

Projects 1-3 used AI as a single tool: one model, one prompt, one response. That's fine for simple tasks. But the most powerful AI systems in production today are orchestrated — multiple models, each chosen for a specific capability, working in sequence or parallel, with human-designed logic deciding what goes where.

This is how real content pipelines work. This is how AI-powered products at Anthropic, Google, and Netflix actually function. Not one giant model doing everything, but a system of specialized agents with routing logic, cost constraints, quality gates, and fallback mechanisms.

You're going to build a content generation pipeline. Feed it a topic, and it:

1. Researches the topic across the web
2. Writes a first draft
3. Edits and refines the draft
4. Generates a cover image
5. Formats and publishes to a CMS

Each step is a different agent. Some use Claude. Some use cheaper models for simpler tasks. The orchestrator routes based on complexity. Every step has cost tracking. Every output has quality evaluation.

This is the capstone. Everything from every part of this book converges here.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Orchestrator                            │
│              (decides routing, tracks costs,                 │
│               manages state, handles failures)               │
│                                                              │
│  Input: Topic + Parameters (tone, length, audience)          │
│                           │                                  │
│              ┌────────────┼────────────┐                     │
│              ▼            ▼            ▼                      │
│  ┌──────────────┐ ┌────────────┐ ┌──────────────┐          │
│  │  Research     │ │  Outline   │ │  Image Spec  │          │
│  │  Agent        │ │  Agent     │ │  Agent       │          │
│  │  (web search  │ │  (Claude   │ │  (generates  │          │
│  │   via MCP)    │ │   Haiku)   │ │   prompt)    │          │
│  └──────┬───────┘ └─────┬──────┘ └──────┬───────┘          │
│         │               │               │                    │
│         ▼               ▼               ▼                    │
│  ┌──────────────┐ ┌────────────┐ ┌──────────────┐          │
│  │  Writer       │ │  Editor    │ │  Image Gen   │          │
│  │  Agent        │ │  Agent     │ │  Agent       │          │
│  │  (Claude      │ │  (Claude   │ │  (DALL-E /   │          │
│  │   Sonnet)     │ │   Opus)    │ │   Flux)      │          │
│  └──────┬───────┘ └─────┬──────┘ └──────┬───────┘          │
│         │               │               │                    │
│         └───────────────┼───────────────┘                    │
│                         ▼                                    │
│              ┌──────────────────┐                            │
│              │  Publisher Agent  │                            │
│              │  (format + CMS   │                            │
│              │   integration)   │                            │
│              └──────────────────┘                            │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Cross-Cutting: Cost Tracker │ Eval Pipeline │ Logs  │   │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

**Tech stack:**
- **Framework:** Next.js 14 (App Router) + Node.js worker processes
- **Orchestration:** Custom state machine (no framework dependency)
- **Models:** Claude Opus (editing), Claude Sonnet (writing), Claude Haiku (outlining, classification), DALL-E or Flux (images)
- **Web research:** MCP server with web search + scraping
- **Storage:** Supabase (pipeline state, outputs, cost logs)
- **Evaluation:** LLM-as-judge + rule-based checks
- **Cost tracking:** Per-agent token counting + model pricing
- **Deployment:** Vercel (frontend) + Railway (worker processes)

---

## What You'll Build, Step by Step

### Phase 1: The Orchestrator (Session 1)

Before any agent exists, you build the brain. The orchestrator is a state machine that tracks:

- **Pipeline state:** Which step is active, which are complete, which failed
- **Accumulated context:** Research findings, outline, draft — each passed to the next agent
- **Cost budget:** A maximum spend per run (e.g., $0.50) with the ability to halt if exceeded
- **Quality gates:** Minimum quality scores an agent's output must hit before the pipeline advances

You'll implement this as a simple state machine — not LangChain, not CrewAI, not any framework. A switch statement, a state object, and transition logic. Why? Because when your pipeline breaks at 2 AM, you need to understand every line of the orchestration code. Frameworks hide the logic. You can't debug what you can't see.

### Phase 2: Research Agent (Session 2)

The research agent takes a topic and returns structured findings. It uses an MCP server to search the web, scrape relevant pages, and synthesize what it finds.

This is where Chapter 17 (MCP) becomes real. Your agent doesn't just call an API — it discovers available tools (web search, page scraper, note-taker), decides which to use, executes them, and synthesizes results. The MCP protocol means you can swap in a different search provider without changing agent logic.

The research agent uses Claude Haiku — it's cheap, fast, and research synthesis doesn't need the reasoning depth of Opus.

### Phase 3: Writer and Editor Agents (Session 3)

The writer agent takes the research findings and outline, then produces a first draft. It uses Claude Sonnet — good at long-form generation, significantly cheaper than Opus.

The editor agent takes the draft and improves it. It uses Claude Opus — the strongest model, reserved for the task that benefits most from nuanced reasoning. The editor checks factual consistency against the research, improves flow, tightens prose, and ensures the tone matches the brief.

This is model routing by complexity. Not every task needs the most expensive model. The outline (Haiku: $0.002) doesn't need the same reasoning as the edit (Opus: $0.15). You'll see a 50x cost difference for tasks that, to a human, look similar but demand different cognitive loads from the model.

### Phase 4: Image Generation and Publishing (Session 4)

An image specification agent writes a detailed prompt for DALL-E or Flux based on the article content. The image generation agent executes it. The publisher agent formats the final article (markdown + frontmatter + image) and pushes it to a CMS or Git repository.

### Phase 5: Evaluation Pipeline (Session 5)

Every agent's output passes through an evaluation step:

- **Research agent:** Are sources real? Are facts verifiable? (Rule-based URL checking + LLM-as-judge for relevance)
- **Writer agent:** Does the draft cover all points from the outline? Is it the requested length? (Structural checks + coherence scoring)
- **Editor agent:** Is the final version better than the draft? Did it introduce errors? (Comparative evaluation)
- **Image agent:** Does the image match the article topic? (CLIP similarity scoring or LLM-as-judge on the prompt)

The eval pipeline runs after every stage and can halt the pipeline, trigger a retry, or escalate to human review. Without this, you're shipping whatever the model produces — and sometimes what it produces is confidently wrong.

### Phase 6: Cost Tracking and Dashboard (Session 6)

Every API call logs: model used, input tokens, output tokens, latency, cost. You'll build a dashboard that shows per-run cost breakdowns, average cost per article, cost trends over time, and which agent consumes the most budget.

This is where Chapter 25 (AI cost modeling) becomes operational. You'll discover that research (many small calls) can cost more than writing (one large call) because of per-request overhead. You'll find that retries from quality gate failures double your costs. You'll learn to set cost alarms before they become cost disasters.

---

## What Will Go Wrong (And What It Teaches)

- **The research agent returns hallucinated URLs.** Web search via MCP returned real results, but the synthesis step invented additional sources. This teaches you to validate every factual claim in AI output, even when the source is another AI step.
- **The editor makes the article worse.** More expensive model does not mean better output. Your eval pipeline catches this — the comparative score shows the draft was better. This teaches you that evaluation is not optional; it's the only way to know if your system is improving.
- **Pipeline costs spike unpredictably.** A retry loop in the writer agent burned through your budget. This teaches you to implement circuit breakers — maximum retries per agent, cost caps per stage, graceful degradation.
- **The orchestrator gets into an invalid state.** Your state machine transition logic has a bug where a failed retry doesn't reset the stage counter. This teaches you that orchestration code needs tests more than agent code does.

---

## Definition of Done

Run the pipeline on 5 different topics. For each:

1. The published article is factually accurate (spot-check 3 claims per article)
2. The total cost is under $0.75
3. The end-to-end time is under 3 minutes
4. The eval pipeline caught and corrected at least one issue
5. The cost dashboard shows a per-agent breakdown

Then run it on a topic you know well — deeply enough to catch subtle errors. The pipeline should produce something you'd be willing to publish under your name with minor edits, not a major rewrite.

That's the bar for production AI. Not "it generates text." It generates text you'd stake your reputation on.
