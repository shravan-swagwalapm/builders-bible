<span class="chapter-number">Chapter 23</span>

# Building Multi-Agent Systems — When One Brain Isn't Enough {.chapter-title}

You have built AI features. You have wired up prompts, connected APIs, and watched a single model handle tasks that used to require entire teams. And at some point — maybe you are there now — you hit a wall. The task is too complex for one model. The context window fills up. The model loses track of what it was doing halfway through. The quality degrades. You add more instructions to the system prompt and the model starts ignoring half of them.

You don't need a bigger model. You need more models, working together.

> **ANALOGY**: A single chef can cook a beautiful dinner for four. Ask that same chef to cook dinner for 400, and they will collapse — not because they lack skill, but because the task exceeds what one person can hold in their head simultaneously. A restaurant kitchen solves this by dividing labor: a sous chef preps ingredients, a line cook handles the grill, a pastry chef makes dessert, and an executive chef coordinates them all. Each specialist focuses on their domain. The executive chef doesn't need to know how to temper chocolate — they need to know who does, when to ask for it, and how to combine all the outputs into a coherent meal.

This is the core idea behind multi-agent systems: instead of one large model doing everything, you decompose the work into smaller tasks and assign each task to a specialized agent — a model instance with its own instructions, its own tools, and its own narrow focus. A coordinator agent (the executive chef) orchestrates the specialists, routes information between them, and synthesizes the final output.

The result is not incremental. Multi-agent systems can handle workflows that are fundamentally impossible for a single model — not because the model is dumb, but because the workflow has more moving parts than any single context window can track.

---

## When You Need Multiple Agents

Not every AI feature needs multiple agents. A chatbot that answers FAQs does not need an orchestrator. A summarization tool does not need a debate protocol. Multi-agent adds complexity, latency, and cost. Use it only when a single agent demonstrably fails.

Here are the signals that you need to move from one agent to many:

**Context window overflow.** Your task requires reading, reasoning over, and producing more content than fits in a single model's context window. Even with 200K-token windows (Claude's limit as of March 2026), complex research tasks, multi-document analysis, or long-form content generation can exceed this.

**Role conflict.** You need the same model to be simultaneously creative and critical, or simultaneously expansive and precise. A single model prompted to "brainstorm bold ideas AND rigorously fact-check them" will do neither well. It hedges. Separate agents with separate instructions resolve the conflict.

**Parallel execution.** Parts of the task are independent and could run simultaneously. A single model processes sequentially. Multiple agents can work in parallel, reducing wall-clock time from minutes to seconds.

**Quality degradation on long tasks.** The model performs well on step 1 but gets sloppy by step 7. This is not a hallucination — it is attention degradation over long outputs. Fresh agents for each step maintain quality throughout.

**Tool specialization.** Different parts of the workflow require different tools — one needs web search, another needs code execution, a third needs database access. Giving one model access to every tool increases the surface area for errors. Giving each agent only the tools it needs constrains behavior.

```
SINGLE AGENT vs. MULTI-AGENT DECISION MATRIX

┌──────────────────────────┬──────────────────────────────────┐
│     USE SINGLE AGENT     │      USE MULTI-AGENT             │
├──────────────────────────┼──────────────────────────────────┤
│ Short, self-contained    │ Long, multi-step workflows       │
│ One role (answer Q's)    │ Multiple conflicting roles       │
│ Fits in context window   │ Exceeds context window           │
│ Sequential is fine       │ Parallelism matters              │
│ One tool set             │ Specialized tool sets per step   │
│ Latency-sensitive (chat) │ Quality-sensitive (research)     │
│ Low budget               │ Budget allows multiple calls     │
└──────────────────────────┴──────────────────────────────────┘
```

> **INTUITION**: The question is not "can a single model do this?" It is "can a single model do this *reliably, every time, at the quality bar I need*?" If the answer is yes, stay with one agent. If the answer is "usually, but it sometimes misses step 4 or generates mediocre output for the last section," you have a multi-agent problem.

---

## Orchestration Patterns

There are four fundamental patterns for coordinating multiple agents. Every multi-agent system you will encounter — from AutoGPT to Devin to custom production pipelines — is a variation of one of these four, or a combination.

### Pattern 1: Sequential (Pipeline)

The simplest pattern. Agent A finishes, passes its output to Agent B, who finishes and passes output to Agent C. Like a factory assembly line — each station does one thing, hands the workpiece to the next station.

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Agent A   │────▶│ Agent B   │────▶│ Agent C   │────▶│  Output  │
│ Research  │     │ Draft     │     │ Edit      │     │  Final   │
│           │     │           │     │           │     │  Article │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
    Step 1           Step 2           Step 3
```

**When to use it:** When each step depends on the previous step's output. Research must happen before drafting. Drafting must happen before editing. Order matters.

**Strengths:** Predictable, debuggable, easy to reason about. If the output is bad, you can inspect each stage to find where quality dropped.

**Weaknesses:** Total latency is the sum of all stages. If Agent B is slow, everything waits. No parallelism.

> **REAL-LIFE**: Anthropic's internal content pipeline uses a sequential pattern: one agent researches a topic using web search, a second agent writes a draft based on the research, a third agent reviews for factual accuracy, and a fourth agent polishes for style. Each stage has a different system prompt and different quality criteria.

### Pattern 2: Parallel (Fan-Out / Fan-In)

Multiple agents work simultaneously on independent subtasks. A coordinator dispatches work, waits for all agents to finish, then combines the results.

```
                    ┌──────────────┐
                    │ Coordinator  │
                    │  (dispatch)  │
                    └──┬───┬───┬──┘
                       │   │   │
              ┌────────┘   │   └────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Agent 1  │ │ Agent 2  │ │ Agent 3  │
        │ Research │ │ Research │ │ Research │
        │ Topic A  │ │ Topic B  │ │ Topic C  │
        └─────┬────┘ └─────┬────┘ └─────┬────┘
              │            │            │
              └────────┐   │   ┌────────┘
                       ▼   ▼   ▼
                    ┌──────────────┐
                    │ Coordinator  │
                    │  (combine)   │
                    └──────────────┘
```

**When to use it:** When subtasks are independent. Researching three different companies. Analyzing five documents. Generating content for separate sections.

**Strengths:** Total latency equals the slowest agent, not the sum. If three agents each take 30 seconds, total time is 30 seconds, not 90.

**Weaknesses:** You need a robust coordinator that can combine heterogeneous outputs. The combining step itself can be error-prone if agents return conflicting information.

> **REAL-LIFE**: Google's Gemini Deep Research uses a parallel fan-out pattern. When you ask a complex research question, it decomposes the question into subtopics, dispatches parallel research agents for each subtopic, and combines findings into a coherent report. This is why a Deep Research query that would take 15 minutes sequentially returns in 3-4 minutes.

### Pattern 3: Hierarchical (Manager → Workers)

A manager agent decomposes a complex task into subtasks, assigns them to worker agents, reviews their output, and may send work back for revision. This is the pattern closest to how human organizations operate.

```
                    ┌──────────────────┐
                    │   LEAD AGENT     │
                    │  (Opus-class)    │
                    │  Plans, reviews, │
                    │  makes decisions │
                    └──┬──────┬───┬───┘
                       │      │   │
                       │      │   │  Assigns tasks,
                       │      │   │  reviews output
                       ▼      ▼   ▼
                    ┌─────┐┌─────┐┌─────┐
                    │Work-││Work-││Work-│
                    │er 1 ││er 2 ││er 3 │
                    │Sonnt││Sonnt││Sonnt│
                    │(rsch)│(writ)│(post)│
                    └──┬──┘└──┬──┘└──┬──┘
                       │      │      │
                       ▼      ▼      ▼
                    Reports back to Lead
                    (may be sent back for revision)
```

**When to use it:** When the task requires judgment about what to do next based on intermediate results. The lead agent does not follow a fixed pipeline — it adapts. If the researcher finds unexpected information, the lead might add a new subtask, or skip a planned step, or ask the writer to change direction.

**Strengths:** Adaptive. The lead agent can handle edge cases, reprioritize work, and maintain quality by reviewing and rejecting subpar output.

**Weaknesses:** The lead agent becomes a bottleneck and a single point of failure. If the lead makes a bad plan, every worker executes the wrong thing. The lead also consumes expensive tokens (you want your smartest model here).

**Cost optimization insight:** The hierarchical pattern naturally maps to **model routing** — use your most capable (and expensive) model for the lead, and cheaper models for the workers. An Opus-class model plans and reviews. Sonnet-class models execute. This can reduce cost by 5-10x compared to running Opus for every step.

### Pattern 4: Debate (Adversarial)

Two or more agents argue opposing positions. A judge agent evaluates the arguments and selects or synthesizes the best answer. This is the most unusual pattern and the most powerful for tasks where correctness matters more than speed.

```
┌──────────────┐                    ┌──────────────┐
│  ADVOCATE A   │                    │  ADVOCATE B   │
│ "This feature │◀──────────────────▶│ "This feature │
│  should use   │   Argue back      │  should use   │
│  WebSockets"  │   and forth       │  SSE instead" │
└──────┬───────┘   (2-4 rounds)     └──────┬───────┘
       │                                    │
       └──────────────┬─────────────────────┘
                      ▼
              ┌──────────────┐
              │    JUDGE     │
              │  Evaluates   │
              │  arguments,  │
              │  picks best  │
              │  or combines │
              └──────────────┘
```

**When to use it:** Code review (one agent writes, another critiques), factual verification (one agent claims, another challenges), design decisions (one agent proposes, another stress-tests), risk assessment.

**Strengths:** Dramatically reduces errors. The advocate agents are incentivized to find flaws in each other's reasoning. The judge sees the strongest version of each argument.

**Weaknesses:** Slow. Multiple rounds of debate mean multiple LLM calls. Expensive. Best reserved for high-stakes decisions where correctness justifies the cost.

> **REAL-LIFE**: Anthropic uses a debate-style pattern internally for constitutional AI training. Two model instances generate responses. A third evaluates which response better adheres to Anthropic's principles. This adversarial setup catches failure modes that single-model evaluation misses.

### Combining Patterns

Production systems rarely use a single pattern. The most common combination is **hierarchical + parallel**: a lead agent plans the work, dispatches parallel workers for independent subtasks, reviews the results, then dispatches sequential steps for dependent work.

```
COMBINED PATTERN: Hierarchical + Parallel + Sequential

         ┌─────────────────────────────┐
         │         LEAD AGENT          │
         │  1. Decompose task          │
         │  2. Identify dependencies   │
         │  3. Dispatch + review       │
         └───┬──────┬──────┬───────────┘
             │      │      │
    ┌────────┘      │      └────────┐     PARALLEL
    ▼               ▼               ▼     (independent)
┌────────┐   ┌────────┐   ┌────────┐
│Worker A│   │Worker B│   │Worker C│
└───┬────┘   └───┬────┘   └───┬────┘
    │            │            │
    └────────────┼────────────┘
                 ▼
         ┌──────────────┐
         │  Lead reviews │                SEQUENTIAL
         │  combines     │                (dependent)
         └───────┬──────┘
                 ▼
         ┌──────────────┐
         │  Worker D     │
         │  (depends on  │
         │   A+B+C)      │
         └───────┬──────┘
                 ▼
         ┌──────────────┐
         │  Lead reviews │
         │  final output │
         └──────────────┘
```

---

## Building Multi-Agent Systems with the Claude Agent SDK

The **Claude Agent SDK** (Anthropic's open-source framework for building agentic applications, released in late 2025) provides the primitives for multi-agent orchestration. It handles the infrastructure — message passing, tool execution, context management — so you focus on the agent design.

### Core Concepts

**Agent**: A configured model instance with a system prompt, a list of tools it can use, and optional guardrails. You define an agent by specifying what it knows, what it can do, and what it should refuse.

**Tool**: A function the agent can call. Tools can be anything: web search, file operations, API calls, database queries, or — critically — invoking another agent.

**Handoff**: The mechanism for one agent to transfer control to another. Agent A can hand off to Agent B, passing along context and instructions. This is how you implement sequential pipelines and hierarchical coordination.

**Guardrails**: Rules that constrain agent behavior. Input guardrails validate what goes into an agent. Output guardrails validate what comes out. You can use these to prevent prompt injection, enforce format requirements, or block unsafe outputs.

Here is the conceptual structure of a multi-agent system using the SDK:

```python
from agents import Agent, Runner, handoff

# Define specialized agents
researcher = Agent(
    name="Researcher",
    model="claude-sonnet-4-20250514",
    instructions="""You are a research specialist.
    Given a topic, find key facts, statistics, and expert opinions.
    Return structured research with sources.""",
    tools=[web_search, read_document]
)

writer = Agent(
    name="Writer",
    model="claude-sonnet-4-20250514",
    instructions="""You are a content writer.
    Given research notes, produce a well-structured draft.
    Match the specified tone and format.""",
    tools=[format_document]
)

editor = Agent(
    name="Editor",
    model="claude-sonnet-4-20250514",
    instructions="""You are an editor. Review the draft for:
    - Factual accuracy against the research
    - Clarity and readability
    - Grammar and style consistency
    Return the edited version with change notes.""",
    tools=[]  # Editor only reads and critiques
)

# Define the lead agent with handoffs
lead = Agent(
    name="Lead",
    model="claude-opus-4-20250514",
    instructions="""You are the content pipeline lead.
    1. Send the topic to the Researcher
    2. Review the research for completeness
    3. Send research to the Writer with tone guidance
    4. Send the draft to the Editor
    5. Review the final output
    If any step produces subpar output, send it back.""",
    handoffs=[
        handoff(researcher),
        handoff(writer),
        handoff(editor)
    ]
)

# Run the pipeline
result = Runner.run(lead, input="Write a 2000-word article on...")
```

### State Management

The hardest problem in multi-agent systems is not orchestration — it is state. Where does the research live after the researcher finishes? How does the writer access it? What happens if the editor rejects the draft and the writer needs to revise — does the writer see the editor's notes AND the original research?

There are three approaches:

**1. Context passing (message-based).** Each agent's output is passed as input to the next agent. The research becomes part of the writer's prompt. The draft becomes part of the editor's prompt. This is the simplest approach and works well for sequential pipelines. The downside: context accumulates. By the time you reach the fourth agent, the prompt contains the entire history of all previous agents, and you may hit context limits.

**2. Shared memory (external store).** Agents read and write to a shared data store — a database, a file, a key-value cache. The researcher writes research to memory under a key like `research_notes`. The writer reads from that key. The editor reads the draft from another key. This decouples agents from each other's context windows. The downside: you need to design the memory schema carefully, and agents must know what keys to read and write.

**3. Blackboard pattern.** A hybrid of the above. A central "blackboard" (a structured shared state) holds the evolving work product. Agents read from and write to specific sections of the blackboard. A controller monitors the blackboard and triggers the next agent when a section is updated. This is the most flexible pattern and scales to complex workflows — but it is also the most complex to implement.

```
BLACKBOARD PATTERN

┌─────────────────────────────────────────────┐
│              SHARED BLACKBOARD              │
│                                             │
│  ┌───────────┐  ┌──────────┐  ┌─────────┐  │
│  │ Research   │  │  Draft   │  │ Review  │  │
│  │ Notes     │  │          │  │ Notes   │  │
│  │ [filled]  │  │ [filled] │  │ [empty] │  │
│  └───────────┘  └──────────┘  └─────────┘  │
│                                             │
│  ┌────────────────────────────────────────┐ │
│  │ Status: DRAFT_COMPLETE → EDITOR_NEXT  │ │
│  └────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────┘
                       │
           ┌───────────┼───────────┐
           │           │           │
      ┌────▼────┐ ┌────▼────┐ ┌───▼─────┐
      │Research │ │ Writer  │ │ Editor  │
      │ Agent   │ │  Agent  │ │  Agent  │
      └─────────┘ └─────────┘ └─────────┘
      Reads: task   Reads:      Reads:
      Writes:       research    draft,
      research      Writes:     research
                    draft       Writes:
                                review
```

> **INTUITION**: Think of state management like a relay race. Context passing is handing the baton directly — fast but the runner must carry everything. Shared memory is a locker room where runners drop off and pick up gear. The blackboard is a war room with a whiteboard that everyone updates and reads. Each works for different team sizes and complexity levels.

---

## Error Handling: When Agents Fail

Single-model errors are annoying. Multi-agent errors are cascading. If the researcher returns garbage, the writer writes garbage, the editor polishes garbage, and you ship garbage. The system amplifies failure.

### The Circuit Breaker Pattern

Borrowed from electrical engineering: a **circuit breaker** is a mechanism that detects when a component is failing and stops sending it work, preventing cascade failures.

In multi-agent systems, this means:

1. **Monitor each agent's output quality.** This can be a simple validation (did the researcher return at least 500 words? Does the output contain the expected JSON structure?) or an LLM-based quality check (a small, fast model evaluating whether the output is coherent).

2. **Set failure thresholds.** If an agent fails 3 times consecutively, the circuit breaker "trips" — no more work is sent to that agent.

3. **Provide fallback behavior.** When the circuit breaks: retry with a different model, use cached results from a previous successful run, or escalate to a human.

```
CIRCUIT BREAKER STATES

   ┌──────────┐    Failure    ┌──────────┐
   │  CLOSED  │──────────────▶│   OPEN   │
   │ (normal) │    threshold  │ (blocked)│
   │ Passes   │    reached    │ Returns  │
   │ requests │               │ fallback │
   └──────────┘               └────┬─────┘
        ▲                          │
        │   Success                │ After cooldown
        │                          ▼
        │                    ┌───────────┐
        └────────────────────│HALF-OPEN  │
                             │(testing)  │
                             │Sends ONE  │
                             │request    │
                             └───────────┘
```

### Retry Strategies

Not all failures are equal. A timeout is different from a hallucinated response.

| Failure Type | Retry Strategy |
|---|---|
| API timeout | Retry with exponential backoff (wait 1s, then 2s, then 4s) |
| Rate limit hit | Wait for the specified retry-after period |
| Model hallucination | Retry with a more explicit prompt or a different model |
| Invalid output format | Retry with stricter format instructions + example |
| Logical error caught by validator | Send error feedback to agent, ask it to correct |
| Repeated failures (3+) | Trip circuit breaker, use fallback |

### Idempotency

**Idempotent** operations (operations that produce the same result whether you run them once or ten times) are essential in multi-agent systems because retries are common. If the writer agent fails and you retry, the writer should produce a new draft from the research — not append to a half-finished draft or duplicate sections.

Design each agent's task as a self-contained transformation: input → output. The agent receives everything it needs in its input and produces a complete output. No side effects. No reliance on previous partial state.

---

## Cost Management: Making Multi-Agent Systems Economical

Multi-agent systems multiply your LLM costs. If a single-agent workflow costs $0.05 per run, a four-agent pipeline might cost $0.20-$0.50 depending on the models used. At 10,000 runs per day, that is $2,000-$5,000 per day — and that is before retries.

### Route by Complexity

The most effective cost optimization is **model routing** — using the cheapest model that can handle each subtask. Not every agent needs your most capable model.

```
COST COMPARISON: Uniform vs. Routed (per pipeline run)

UNIFORM (all Opus):
  Lead:       1K input + 2K output = $0.045
  Researcher: 3K input + 5K output = $0.135
  Writer:     5K input + 8K output = $0.225
  Editor:     8K input + 4K output = $0.180
  TOTAL: ~$0.59 per run

ROUTED (Lead=Opus, Workers=Sonnet):
  Lead:       1K input + 2K output = $0.045     (Opus)
  Researcher: 3K input + 5K output = $0.027     (Sonnet)
  Writer:     5K input + 8K output = $0.042     (Sonnet)
  Editor:     8K input + 4K output = $0.039     (Sonnet)
  TOTAL: ~$0.15 per run

SAVINGS: 75% cost reduction
  At 10K runs/day: $1,500/day saved
```

The rule of thumb: **use your best model for planning and evaluation, use cheaper models for execution.** The lead agent needs judgment — it decides what work to do, reviews quality, and makes architectural decisions. The workers need competence — they execute well-defined tasks with clear instructions.

### Prompt Caching

If multiple agents share common context (e.g., a company style guide, product documentation, or research notes), use **prompt caching** — a feature where the API stores frequently-used prompt prefixes and charges reduced rates for cached tokens.

With Anthropic's API, cached prompt tokens cost 90% less than fresh tokens. If your system prompt is 3,000 tokens and you call 4 agents, caching saves you 90% on 9,000 tokens (3 of the 4 calls use the cached version).

### Batch Where Possible

If your pipeline processes multiple items (10 articles, 50 support tickets, 100 code reviews), batch them. Instead of running the full pipeline for each item sequentially, dispatch all researcher agents in parallel, wait for results, then dispatch all writer agents in parallel.

This exploits the **parallel pattern** for throughput. The cost per item is the same, but the wall-clock time drops from N * pipeline_time to pipeline_time (assuming sufficient parallelism).

---

## Case Study: The OpenClaw Pattern

**OpenClaw** is a multi-agent content engine built in production (running as of March 2026) that demonstrates the hierarchical pattern with model routing. Here is its architecture:

```
USER REQUEST: "Create a LinkedIn post about AI pricing models"
         │
         ▼
┌──────────────────────────────────────────┐
│          LEAD AGENT (Claude Opus)        │
│                                          │
│  1. Analyze request                      │
│  2. Decide: needs research? (yes/no)     │
│  3. Plan content strategy                │
│  4. Dispatch workers                     │
│  5. Review and approve                   │
└────┬──────────┬──────────┬───────────────┘
     │          │          │
     ▼          ▼          ▼
┌─────────┐┌─────────┐┌─────────┐
│RESEARCH ││ WRITER  ││ POSTER  │
│ AGENT   ││  AGENT  ││  AGENT  │
│(Sonnet) ││(Sonnet) ││(Sonnet) │
│         ││         ││         │
│Searches ││Drafts   ││Formats  │
│web,     ││content  ││for      │
│reads    ││based on ││platform,│
│sources, ││research ││schedules│
│extracts ││+ brand  ││post,    │
│facts    ││voice    ││adds     │
│         ││         ││hashtags │
└────┬────┘└────┬────┘└────┬────┘
     │          │          │
     └──────────┼──────────┘
                ▼
     ┌──────────────────┐
     │  Lead reviews    │
     │  final output    │
     │  (approve/reject)│
     └──────────────────┘
```

The key design decisions:

**1. The Lead makes judgment calls.** "Does this topic need fresh research, or can we work from the brand's existing knowledge?" A post about a company's own product might skip research. A post about industry trends needs it. The lead decides based on the request, not a fixed rule.

**2. Workers are constrained.** The researcher can search the web and read documents, but cannot write content. The writer can produce text, but cannot search the web. The poster can format and schedule, but cannot modify the content. Each agent has the minimum tool set for its role.

**3. The Lead reviews before publishing.** The Lead (Opus) reads the writer's draft and evaluates it against the original request, the research, and the brand voice guidelines. If the draft misses key points or diverges from the brand voice, the Lead sends it back with specific feedback. This quality gate is why the Lead uses the most capable model — it needs to evaluate nuance.

**4. Cost is managed through routing.** Opus handles 15-20% of total tokens (planning + review). Sonnet handles 80-85% (execution). Total cost per content piece: approximately $0.08-$0.15, compared to $0.50+ if all steps used Opus.

> **REAL-LIFE**: OpenClaw processes 50-100 content pieces per day. The multi-agent design reduced per-piece cost by 70% compared to the single-agent prototype, while improving quality scores (measured by a human review panel) by 35%. The quality improvement came not from better models but from specialization — the researcher stopped trying to write, and the writer stopped trying to research.

---

## Case Study: AutoResearch as Multi-Agent

**AutoResearch** (exemplified by tools like Google Deep Research, Perplexity Deep Research, and open-source implementations like GPT-Researcher) is the multi-agent pattern applied to information synthesis. The architecture:

```
USER QUESTION: "Compare AI pricing strategies across
                SaaS companies in 2025-2026"
         │
         ▼
┌──────────────────────────────────────┐
│         PLANNER AGENT                │
│  Decomposes question into:           │
│  - Q1: What pricing models exist?    │
│  - Q2: Who uses each model?          │
│  - Q3: What are the margins?         │
│  - Q4: What trends are emerging?     │
└───┬────────┬────────┬────────┬───────┘
    │        │        │        │
    ▼        ▼        ▼        ▼        PARALLEL
┌───────┐┌───────┐┌───────┐┌───────┐
│Searcher││Searcher││Searcher││Searcher│
│  Q1   ││  Q2   ││  Q3   ││  Q4   │
│       ││       ││       ││       │
│10 web ││10 web ││10 web ││10 web │
│sources││sources││sources││sources│
└───┬───┘└───┬───┘└───┬───┘└───┬───┘
    │        │        │        │
    └────────┴────┬───┴────────┘
                  ▼
         ┌──────────────┐
         │  SYNTHESIZER │
         │  Combines 40 │
         │  sources into│
         │  coherent    │
         │  report      │
         └──────────────┘
```

The planner uses the **parallel fan-out** pattern — dispatching independent search agents simultaneously. The synthesizer uses a **sequential reduction** — taking all findings and producing a single coherent document.

The critical engineering challenge is **source deduplication and conflict resolution**. Four parallel searchers will find overlapping sources. The synthesizer must handle contradictions ("Source A says margins are 60%, Source B says 45%") by citing both, noting the discrepancy, and providing context for why the numbers differ.

---

## Devin and the Fully Autonomous Agent

**Devin** (by Cognition Labs, launched 2024, iterated through 2025-2026) represents the extreme end of multi-agent systems: a fully autonomous software engineering agent that operates its own computer environment. Devin is not one model — it is an orchestra of agents with access to a full development environment: browser, terminal, code editor, and deployment tools.

What makes Devin architecturally interesting:

**1. Environment as tool.** Unlike most multi-agent systems that interact through APIs, Devin's agents interact through a full virtual machine. One agent writes code in the editor. Another runs it in the terminal. Another opens a browser to test the UI. This mirrors how a human developer works — across multiple tools simultaneously.

**2. Long-running autonomy.** Devin can work for hours on a task. This requires robust state management (the virtual machine itself is the state), error recovery (if a test fails, debug and retry), and progress tracking (regular checkpoints so the work is not lost).

**3. Planning and replanning.** Devin does not execute a fixed pipeline. It makes a plan, starts executing, encounters unexpected results, and replans. This is the hierarchical pattern with dynamic task decomposition — the plan evolves as the work reveals new information.

The lesson for builders: Devin is not magic. It is the orchestration patterns from this chapter — hierarchical, parallel, sequential, with shared state — implemented at scale with a rich tool environment. You can build a simpler version of this for your domain.

## Replit Agent: Parallel Construction at Speed

**Replit Agent** takes a different approach from Devin. Where Devin mimics a single developer working across tools, Replit Agent mimics a *team* of developers building components in parallel.

Given a natural language description ("build me a todo app with authentication and a dashboard"), Replit Agent:

1. **Architect agent** designs the file structure, technology stack, and database schema — before any code is written.
2. **Builder agents** (parallel) each construct one component: the auth module, the database layer, the UI components, the API routes. These run simultaneously.
3. **Integration agent** connects the components, resolves import errors, and ensures the system works end-to-end.
4. **Deployment agent** configures hosting, environment variables, and deploys the working application.

The parallel builder step is what makes Replit Agent fast. Building four components simultaneously instead of sequentially cuts wall-clock time by 3-4x. The integration agent then handles the seams — the places where independently built components must connect.

> **INTUITION**: Every fully autonomous agent system is, under the hood, a multi-agent system where one agent plans and others execute. The difference between a toy demo and a production system is the quality of error handling, the sophistication of replanning, and the rigor of the quality gates between steps. Both Devin and Replit Agent demonstrate this: the most effective AI coding agents are not single models with large prompts. They are orchestrated teams of specialized models, because task decomposition and specialization genuinely produce better results for complex work.

---

## Building Your Own: Design Principles

Before you start coding, internalize these principles:

**1. Start with one agent. Add agents only when the one agent demonstrably fails.** Premature decomposition is as dangerous as premature optimization. Each agent adds latency, cost, and failure surface. Prove that a single agent cannot handle the task before splitting.

**2. Define agent boundaries by capability, not by step.** Bad: "Agent 1 does step 1, Agent 2 does step 2." Good: "Agent 1 has web search tools and finds information. Agent 2 has writing tools and creates content." Capability boundaries create natural interfaces that are robust to workflow changes.

**3. Each agent should be testable in isolation.** If you cannot give the researcher agent a topic and get back useful research without running the rest of the pipeline, your agent is too coupled to the system.

**4. The lead agent's instructions are your most important artifact.** The lead determines quality. Its system prompt should specify: what constitutes acceptable output from each worker, when to retry vs. accept, how to combine results, and when to escalate to a human.

**5. Log everything.** Every agent call, every input, every output, every retry. When the pipeline produces bad output (and it will), your logs are the only way to diagnose where it went wrong. A multi-agent system without comprehensive logging is a black box that will betray you at the worst possible moment.

**6. Set cost budgets per run.** Define maximum tokens per agent per run. If the researcher exceeds 10,000 output tokens, something is wrong — it is probably summarizing entire web pages instead of extracting key facts. Token budgets act as guardrails against runaway costs.

---

<div class="exercise">
<div class="exercise-title">Exercise: Build a 3-Agent Content Pipeline</div>

You will build a multi-agent content pipeline that takes a topic and produces a polished LinkedIn post. This exercise uses the hierarchical pattern with three agents.

**What you will build:**

```
Topic → Researcher → Writer → Editor → Polished Post
         (Sonnet)    (Sonnet)  (Sonnet)
              ↑          ↑         ↑
              └──── Lead Agent (coordinates) ────┘
                        (Opus or Sonnet)
```

**Step 1: Define the Researcher Agent**

Create an agent with these characteristics:
- System prompt: "You are a research specialist. Given a topic, find 5-7 key facts, statistics, or insights. Return them as a numbered list with source attribution where possible. Do not write prose — only structured research notes."
- Tools: Web search (if available) or a mock function that returns hardcoded research for testing
- Output format: Numbered list of facts

Test the researcher in isolation. Give it three different topics. Does it return structured, factual, source-attributed notes every time?

**Step 2: Define the Writer Agent**

Create an agent with these characteristics:
- System prompt: "You are a LinkedIn content writer. Given research notes and a topic, write a 150-200 word LinkedIn post. Use a hook in the first line. Include one specific number or statistic from the research. End with a question to drive engagement. Tone: professional but conversational."
- Tools: None (the writer only needs text in, text out)
- Input: The researcher's output + the original topic

Test the writer in isolation with sample research notes. Does the output match the format requirements?

**Step 3: Define the Editor Agent**

Create an agent with these characteristics:
- System prompt: "You are an editor. Review the LinkedIn post for: (1) factual accuracy against the research notes, (2) hook quality — does the first line grab attention? (3) length — is it 150-200 words? (4) engagement — does it end with a compelling question? Return the edited post and a brief change log."
- Tools: None
- Input: The writer's draft + the original research notes

**Step 4: Wire Them Together**

Create a lead agent (or a simple script) that:
1. Sends the topic to the researcher
2. Sends the research to the writer
3. Sends the draft + research to the editor
4. Returns the final post

**Step 5: Add Error Handling**

- If the researcher returns fewer than 3 facts, retry once with a more specific prompt
- If the writer exceeds 250 words, ask it to cut to 200
- If the editor's change log contains "factual error," send the draft back to the writer with the correction

**Step 6: Measure**

Run the pipeline on 5 different topics. Record:
- Total latency (wall-clock time)
- Total tokens used (input + output for each agent)
- Total cost
- Quality score (rate each output 1-5 for accuracy, engagement, and format compliance)

Compare the multi-agent output to a single-agent output (one model, one prompt, same topics). Where does the multi-agent version win? Where does it lose?

This exercise should take 2-3 hours. You will learn more about agent design from building this pipeline than from reading about it.

</div>

---

**Chapter endnotes**

[1] The "kitchen brigade" system (brigade de cuisine) was formalized by Auguste Escoffier in the late 19th century. It decomposed the chaotic kitchen into specialized stations (saucier, poissonnier, patissier) coordinated by an executive chef — the first documented "multi-agent system" for food production. The parallels to software agent architectures are not coincidental; both solve the same fundamental problem of coordinating specialized workers on a complex task.

[2] The Claude Agent SDK was released by Anthropic in 2025 as an open-source framework. Documentation and source code are available at https://github.com/anthropics/agent-sdk. The SDK supports Python and TypeScript, with handoff, tool use, and guardrail primitives.

[3] The circuit breaker pattern was popularized in software engineering by Michael Nygard in "Release It!" (2007). The pattern was adapted from electrical engineering, where circuit breakers prevent cascading failures by interrupting current flow when a fault is detected.

[4] Google's Gemini Deep Research, launched in late 2024 and iteratively improved through 2025-2026, uses a multi-agent architecture for complex research queries. Google's technical blog posts describe the fan-out/fan-in pattern for parallel web search and synthesis.

[5] Cognition Labs' Devin was announced in March 2024 as the "first AI software engineer." Subsequent versions (2025-2026) expanded its capabilities from code generation to full-stack development including deployment. Devin operates in a sandboxed virtual environment with access to browser, terminal, and code editor tools.

[5b] Replit Agent's architecture for building full applications from natural language descriptions was announced in late 2024. The parallel builder pattern — where multiple agents construct independent components simultaneously — and the integration + deployment automation were demonstrated in Replit's product launches through 2025.

[6] The OpenClaw content engine architecture described in this chapter is based on a production system processing 50-100 content pieces daily as of March 2026. The cost and quality metrics cited are from production monitoring data.

[7] Model routing as a cost optimization strategy is documented in research from multiple organizations. The general principle — using smaller models for routine tasks and larger models for complex reasoning — is sometimes called "model cascading" or "tiered inference." Anthropic's own documentation recommends this approach for production workloads.

[8] The blackboard architecture pattern originates from AI research in the 1970s-1980s, notably the Hearsay-II speech understanding system at Carnegie Mellon University. It was formalized by H. Penny Nii in "The Blackboard Model of Problem Solving and the Evolution of Blackboard Architectures" (1986).
