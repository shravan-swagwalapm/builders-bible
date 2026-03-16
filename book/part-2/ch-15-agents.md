<span class="chapter-number">Chapter 15</span>

# AI Agents — AI That Acts, Not Just Answers {.chapter-title}

You text your human assistant: "Book me a flight to Mumbai for next Thursday, under ₹8,000, window seat, morning departure. If nothing's available, try Wednesday evening instead."

Your assistant doesn't text back asking what an airplane is. They don't send you a list of every airline that flies to Mumbai. They go *do the thing*. They open MakeMyTrip, search flights, compare prices, check your calendar for conflicts, find one that fits all the constraints, book it, and send you the confirmation. If the Thursday flights are sold out, they don't freeze — they adapt, try Wednesday, and tell you what they found.

That assistant is not answering questions. They are completing a task. They reason about what to do, take actions in the world, observe the results, and adjust their plan. They hold your goal in mind across many steps, use tools you'd use yourself, and exercise judgment when things don't go as expected.

This is the difference between a chatbot and an agent. And it is the most consequential shift happening in AI right now.

## From Answer Machines to Task Completers

Every AI tool you've used so far in this book has been reactive. You ask a question, it gives an answer. You write a prompt, it generates text. You feed it documents, it retrieves relevant chunks. The human remains in the loop for every decision, every step, every action.

Agents break this pattern.

An **AI agent** is a system where a large language model doesn't wait for your next instruction — it decides what to do next, does it, checks the result, and keeps going until the task is done or it needs your input.

> **ANALOGY**: Think about the difference between a search engine and a travel agent. Google will answer any question you type. "Flights Mumbai Thursday morning." It gives you ten blue links and waits. You click, compare, navigate booking forms, enter payment details, choose seats. You are the orchestrator, and Google is one of many tools you use. A travel agent takes a goal — "Get me to Mumbai Thursday morning, under ₹8,000" — and handles every step. They search, compare, call airlines, negotiate, book, and hand you a ticket. The search engine *answers*. The travel agent *acts*. LLMs in 2023–2024 were search engines. In 2025–2026, they're becoming travel agents.

> **REAL-LIFE**: In January 2025, Anthropic launched Claude with "computer use" — the ability to see a screen, move a mouse, click buttons, and type text, like a human sitting at a computer. A product manager could tell Claude: "Go to our Mixpanel dashboard, pull last week's retention numbers, compare them to the previous week, and draft a summary for our team standup." Claude would navigate to Mixpanel, find the right report, read the numbers, screenshot the charts, switch to a document, and write the summary. No human in the loop for any of those intermediate steps. The PM stated the goal. Claude figured out the path.

> **INTUITION**: The test for whether something is an agent is not how smart it is — it's whether it has **agency**. Can it decide its own next step? Can it use tools? Can it observe the results and change its plan? If yes, it's an agent. If it waits for you to tell it what to do after every response, it's a chatbot, no matter how intelligent.

## The Karpathy Framing: From Vibe Coding to Agentic Engineering

Andrej Karpathy — the former Director of AI at Tesla who helped build the Autopilot system, and one of the founding members of OpenAI — has a gift for naming the eras as they arrive.

In early 2025, he coined the term **"vibe coding"**: the practice of describing what you want to an AI in natural language and letting it write the code. You don't think about syntax or architecture — you describe the *vibe* of what you want, and the model generates it. "Make me a landing page with a dark hero section and animated gradient background." The human provides creative direction. The AI writes code.

By early 2026, Karpathy observed that something more fundamental was happening. Developers weren't writing individual prompts anymore. They were designing *systems of agents* — multiple AI models working together, each with specific roles, tools, and responsibilities. He called this **"agentic engineering"**: the discipline of designing, orchestrating, and supervising teams of AI agents that execute complex workflows.

The shift looks like this:

```
THE EVOLUTION OF HUMAN–AI COLLABORATION
════════════════════════════════════════════════════════════════

2023: MANUAL CODING           Human writes every line of code
      ┌─────────┐
      │  HUMAN  │ ──writes──▶ CODE
      └─────────┘
      100% human effort


2024: COPILOT ERA             AI suggests, human approves/edits
      ┌─────────┐     ┌─────────┐
      │  HUMAN  │ ◄──▶│   AI    │ ──▶ CODE
      └─────────┘     └─────────┘
      70% human, 30% AI


2025: VIBE CODING             Human describes intent, AI generates
      ┌─────────┐             ┌─────────┐
      │  HUMAN  │ ──intent──▶ │   AI    │ ──▶ CODE
      └─────────┘  "make it   └─────────┘
      30% human,    feel..."   70% AI


2026: AGENTIC ENGINEERING     Human orchestrates agent teams
      ┌─────────┐
      │  HUMAN  │ ──goal──▶  ┌──────────────────────┐
      └─────────┘            │  AGENT 1 (Research)   │
      10% human,             │  AGENT 2 (Design)     │──▶ PRODUCT
      90% agents             │  AGENT 3 (Code)       │
                             │  AGENT 4 (Test)       │
                             │  AGENT 5 (Deploy)     │
                             └──────────────────────┘
```

The human's role didn't disappear — it transformed. From *writing code* to *writing prompts* to *defining goals and constraints*. The skill that matters in 2026 is decomposing goals into agent-sized tasks, providing the right tools, and setting guardrails.

This is why this chapter matters for product managers. You will be the person who decides: "Should this workflow be agentic? Where do humans stay in the loop? What happens when the agent fails?" Those are product decisions, not engineering decisions.

## The Agent Architecture: Five Components

Every agent is built from five components. You don't need to build them yourself, but you need to understand what each does if you're making product decisions about agents.

```
THE AGENT ARCHITECTURE
═══════════════════════════════════════════════════════════════════

                    ┌─────────────────────────────────────────┐
                    │            GUARDRAILS (Safety)           │
                    │  "Don't spend >$50" "Never delete prod  │
                    │   data" "Ask human before sending email" │
                    └────────────────────┬────────────────────┘
                                         │ constrains every step
                                         ▼
┌──────────────┐    ┌─────────────────────────────────────────┐
│              │    │          ORCHESTRATOR (Workflow)          │
│   MEMORY     │◄──▶│                                          │
│  (Context)   │    │  Decides: What do I do next?             │
│              │    │  Manages: Task queue, step tracking       │
│ • Chat       │    │  Routes: Which agent handles which task   │
│   history    │    │  Evaluates: Did that step succeed?        │
│ • Task       │    │                                          │
│   state      │    └──────────────────┬──────────────────────┘
│ • Retrieved  │                       │
│   knowledge  │              ┌────────┴────────┐
│ • Past       │              ▼                  ▼
│   results    │    ┌──────────────┐   ┌──────────────────┐
│              │    │   BRAIN      │   │    TOOLS          │
└──────────────┘    │   (LLM)     │   │    (Actions)      │
                    │              │   │                    │
                    │ Reasons      │   │ • Web search       │
                    │ Plans        │   │ • Code execution   │
                    │ Decides      │   │ • File read/write  │
                    │ Generates    │   │ • API calls        │
                    │ text         │   │ • Database queries  │
                    │              │   │ • Browser control   │
                    └──────────────┘   └──────────────────┘
```

Let's walk through each component.

### 1. Brain (The LLM)

The brain is the large language model at the center of the agent. It does the reasoning, planning, and decision-making. When the agent encounters a situation — "The API returned a 403 error" — the brain decides what to do: "That means I don't have permission. I should check if the API key is correct, and if not, ask the user for a new one."

The choice of brain matters. A more capable model (Claude Opus, GPT-4.5) makes better decisions but costs more and runs slower. A smaller model (Claude Haiku, GPT-4o-mini) is faster and cheaper but makes more mistakes on complex reasoning. For many agent workflows, you use a powerful model for planning and a cheaper model for execution.

### 2. Memory (The Context)

Humans take memory for granted. When your travel agent books your flight, they remember that you prefer window seats, that you're vegetarian, and that your passport expires in six months. They carry that context across every interaction.

LLMs don't have persistent memory by default. Each API call starts fresh — the model doesn't know what happened in the previous call unless you tell it. Agent memory is the system that solves this, and it comes in three types:

- **Short-term memory**: The conversation history and current task state. "I've searched three flight options. The first was too expensive. The second had a layover."
- **Long-term memory**: Persistent facts stored in a database or file. "This user prefers window seats. Their budget is ₹8,000." Claude Code uses `CLAUDE.md` files as long-term memory — persistent instructions that survive across conversations.
- **Working memory**: Retrieved information relevant to the current step. "The MakeMyTrip API returned these five flights for Thursday morning."

The challenge is the **context window** — the maximum text the LLM can process at once. Even with 200K token windows, an agent on a complex task can accumulate more information than fits. This is why agent memory systems include strategies for *summarizing*, *compressing*, and *selectively retrieving* — keeping relevant context in view and archiving the rest.

### 3. Tools (The Actions)

This is where agents become transformatively different from chatbots. A chatbot can only produce text. An agent can *do things* in the real world.

**Tools** (also called **functions**) are capabilities that an agent can invoke. Search the web. Read a file. Execute code. Send an email. Query a database. Call an API. Navigate a browser. Each tool has a name, a description of what it does, and a specification of what inputs it needs.

> **INTUITION**: Think of tools like apps on a smartphone. The phone's operating system (the LLM) is intelligent, but without apps, it's a brick. Install Google Maps and the phone can navigate. Install a camera app and it can take photos. Install Slack and it can send messages. Each tool extends what the agent can do. The agent doesn't need to know *how* the tool works internally — it needs to know *when* to use it and *what inputs to provide*. A PM using Google Maps doesn't understand the routing algorithm. They know that if they give it a destination, it gives back directions.

### 4. Orchestrator (The Workflow)

The orchestrator is the traffic controller. It decides the sequence of steps, routes tasks to the right agent or tool, manages handoffs between agents, and tracks progress toward the goal.

In a single-agent system, the orchestrator is a loop: think → do → check → repeat. In a multi-agent system, it routes tasks between agents and manages handoffs. Product managers should care most about the orchestrator because it determines workflow design, decision points, failure handling, and human-in-the-loop checkpoints.

### 5. Guardrails (The Safety Layer)

Guardrails are the constraints that prevent the agent from doing something harmful, expensive, or foolish. They sit above all other components and can veto any action before it happens.

Examples of guardrails:

- **Budget limits**: "Don't make API calls that cost more than $5 total"
- **Scope constraints**: "Only access files in the /project directory, never /system"
- **Human-in-the-loop gates**: "Draft the email, but don't send it until the user approves"
- **Content filters**: "Never generate content that includes personal medical information"
- **Action blockers**: "Never execute `DROP TABLE` or `rm -rf` commands"

> **REAL-LIFE**: When Anthropic designed Claude Code, they built guardrails directly into the agent architecture. The tool needs explicit user permission before running bash commands. Destructive operations (like `git reset --hard`) require additional confirmation. The agent won't modify files it hasn't read first. These aren't afterthoughts — they're first-class architectural components. A product manager who ships an agent without guardrails is like a product manager who ships a payments feature without fraud detection. The happy path works great. The failure modes are catastrophic.

## Tool Use and Function Calling: How Agents Touch the Real World

When you ask a chatbot "What's the weather in Bangalore?", it either knows (from training data, which is outdated) or doesn't. When you ask an *agent*, it calls a weather API, gets current data, and tells you. This is **tool use** (also called **function calling**) — the single capability that turns a text-generator into an agent.

Here's how it works:

1. **You define the tools**: Each tool has a name, description, and parameter schema. Example: `search_web(query: string)` — "Searches the web and returns top results."
2. **The LLM decides to use a tool**: Instead of guessing "probably 28°C," it generates: `search_web(query="current weather Bangalore")`.
3. **Your code executes the tool**: Your application runs the function, hits the API, gets the result: "31°C, partly cloudy."
4. **The result goes back to the LLM**: The model now has real data to work with.
5. **The LLM generates a response**: "It's 31°C in Bangalore, partly cloudy."

> **ANALOGY**: Imagine sitting in an exam hall with a phone on your desk. You can't leave the room (the LLM can't access the internet directly), but you can call specific numbers: a librarian for facts, a calculator for numbers, a lab technician for experiments. You decide *which* number to call and *what to ask*. They do the work and report back. You incorporate their answer. That's tool use.

The power of tool use is that it's composable. Give an agent 10 tools and it can combine them in ways you never anticipated. An agent with `search_web`, `read_file`, `write_file`, and `execute_code` can research a topic, draft a report, write a Python script to generate charts, run it, and embed the charts — all from a single goal.

This is also what makes tool use dangerous. An agent with `send_email` and `query_database` could email your entire customer list to the wrong person if it misunderstands the goal. This is why guardrails aren't optional — they're structural.

## The ReAct Pattern: How Agents Think

The most foundational pattern in agent design comes from a 2023 paper by Shunyu Yao and colleagues at Princeton: **ReAct** (Reasoning + Acting). Before ReAct, researchers tried reasoning and acting separately. Pure reasoning models thought beautifully but couldn't act. Pure action models acted without thinking. ReAct interleaves both in a loop:

```
THE ReAct LOOP
═══════════════════════════════════════════════════════

  ┌──────────┐
  │  GOAL    │  "Find the CEO of the company that
  │          │   acquired WhatsApp and their net worth"
  └────┬─────┘
       │
       ▼
  ┌──────────────────────────────────────────────┐
  │  REASON (Think)                               │
  │  "I need to find which company acquired       │
  │   WhatsApp. I'll search for this first."      │
  └──────┬───────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────────────────────┐
  │  ACT (Do)                                     │
  │  search_web("company that acquired WhatsApp") │
  └──────┬───────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────────────────────┐
  │  OBSERVE (Check)                              │
  │  "Facebook (now Meta) acquired WhatsApp       │
  │   in 2014 for $19 billion."                   │
  └──────┬───────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────────────────────┐
  │  REASON (Think again)                         │
  │  "Good, Facebook/Meta acquired WhatsApp.      │
  │   The CEO of Meta is Mark Zuckerberg.         │
  │   Now I need his current net worth."          │
  └──────┬───────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────────────────────┐
  │  ACT (Do)                                     │
  │  search_web("Mark Zuckerberg net worth 2026") │
  └──────┬───────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────────────────────┐
  │  OBSERVE (Check)                              │
  │  "Mark Zuckerberg's net worth is estimated    │
  │   at approximately $217 billion (2026)."      │
  └──────┬───────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────────────────────┐
  │  REASON (Conclude)                            │
  │  "I have both pieces of information.          │
  │   I can now answer the question."             │
  └──────┬───────────────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────────────────────┐
  │  FINAL ANSWER                                 │
  │  "The company that acquired WhatsApp is Meta  │
  │   (formerly Facebook). Its CEO, Mark          │
  │   Zuckerberg, has an estimated net worth      │
  │   of $217 billion as of 2026."                │
  └──────────────────────────────────────────────┘
```

The key insight: the model doesn't plan all actions upfront. It takes one step, observes the result, reasons about what it learned, and *then* decides the next step. This makes agents adaptive.

> **INTUITION**: This is how you find a restaurant. Think: "I want Thai food." Search Zomato. Top result has bad reviews. Think: "Filter by 4.0+." Filter. Good one, but 12 km away. Think: "Too far, search within 3 km." Each observation changes your next action. ReAct formalizes this natural process into a pattern LLMs can follow.

## The Framework Landscape: Choosing Your Agent Toolkit (2026)

If you're building an agent in 2026, you don't start from scratch. Several frameworks have emerged, each with a different philosophy and sweet spot. Understanding these is essential for product decisions, because the framework you choose constrains what's easy and what's hard.

| Framework | Creator | Philosophy | Best For | Key Feature |
|-----------|---------|-----------|----------|-------------|
| **Claude Agent SDK** | Anthropic | Subagent teams with safety-first design | Production enterprise agents | Native MCP integration, subagent spawning, built-in guardrails |
| **OpenAI Agents SDK** | OpenAI | Successor to "Swarm" prototype | Multi-agent handoffs | Agent-to-agent handoffs, built-in guardrails, tracing |
| **LangGraph** | LangChain | Graph-based state machines | Complex cyclic workflows with conditional paths | Nodes-and-edges model, persistent state, human-in-the-loop |
| **CrewAI** | Joao Moura | Role-based collaboration | Content pipelines, research teams | Agents have roles (Researcher, Writer), task delegation |
| **AutoGen** | Microsoft | Multi-agent conversation | Debate, review, iteration patterns | Agents converse with each other, GroupChat manager |

Let's look at each in enough detail to make product decisions.

### Claude Agent SDK (Anthropic)

Anthropic's framework treats agents as a hierarchy: a **main agent** spawns **subagents** for parallel or specialized work. The defining feature is **MCP (Model Context Protocol)** integration — a standard way to connect agents to external tools and data sources. Connect to a GitHub MCP server, a database MCP server, and a Slack MCP server, and all tools are available seamlessly. (Chapter 16 covers MCP in depth.) Safety is embedded: every tool call passes through a guardrail layer, and subagents inherit their parent's constraints.

**When to choose it**: Production agents connecting to many external services, enterprise customers who need a strong safety story, or teams already using Claude.

### OpenAI Agents SDK

Evolved from the **"Swarm"** prototype, OpenAI's production SDK centers on **handoffs** — one agent completing its part and passing control to another. A Triage Agent determines the issue, then hands off to Billing, Technical Support, or Returns depending on category. Each agent has its own instructions and tools, and the handoff includes context. Built-in **guardrails** check inputs/outputs at each step, and a **tracing** system records every decision for debugging.

**When to choose it**: Linear workflows where tasks pass between specialists, or teams wanting strong observability in the OpenAI ecosystem.

### LangGraph (LangChain)

LangGraph models workflows as **graphs** — nodes (steps) connected by edges (transitions). A code review agent reads code (node 1), identifies issues (node 2), generates fixes (node 3), runs tests (node 4), and if tests fail, loops back to node 3. Cyclic workflows like this are natural as graphs but awkward in linear frameworks. LangGraph also provides **persistent state** — checkpointed at each node, so crashed agents can resume.

**When to choose it**: Workflows with loops, branches, or conditional paths. Long-running tasks needing checkpointing. Fine-grained flow control.

### CrewAI

CrewAI takes a metaphor-driven approach: agents are **crew members** with roles, goals, and backstories. You don't define a graph or a handoff chain — you define a team.

```python
researcher = Agent(
    role="Senior Research Analyst",
    goal="Find comprehensive data on the Indian EV market",
    backstory="You are a market research expert with 15 years of "
              "experience in the Indian automotive industry.",
    tools=[web_search, document_reader]
)

writer = Agent(
    role="Content Strategist",
    goal="Write a compelling report from the research data",
    backstory="You are a McKinsey-trained writer who turns complex "
              "data into executive-ready narratives.",
    tools=[write_file]
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential
)
```

This approach is intuitive for non-engineers to understand and configure. The role, goal, and backstory fields shape each agent's behavior without complex prompt engineering.

**When to choose it**: You're building content pipelines (research → write → edit), your team includes non-engineers who need to understand and configure the agents, or you want rapid prototyping of multi-agent workflows.

### AutoGen (Microsoft)

AutoGen treats multi-agent systems as **conversations**. Agents don't hand off tasks — they talk to each other. A UserProxy agent represents the human. An AssistantAgent represents the AI. A GroupChat manager moderates conversations between multiple agents.

This is powerful for workflows that benefit from *debate and iteration*. A code-writing agent writes code, a review agent critiques it, the writer revises, and the cycle repeats. The adversarial dynamic produces better results than a single agent alone.

**When to choose it**: Your workflow benefits from iterative refinement through agent dialogue, or you need agents to challenge each other's work.

## The Five Agent Failure Modes Every PM Must Know

Here is the section of this chapter you should bookmark, highlight, and come back to every time someone on your team proposes an agentic feature. These are not edge cases. These are the *primary* ways agents fail in production, and understanding them is the difference between shipping an agent that works and shipping one that embarrasses your company.

### Failure Mode 1: Cascading Errors

One mistake propagates through every subsequent step.

> **ANALOGY**: A row of dominoes. Knock over the first one, and every domino after it falls. Agents work in sequences — the output of step 3 becomes the input of step 4. If step 3 produces an error, step 4 doesn't get good input, and its output is worse, and step 5 is worse still. By step 10, the final result is nonsense, and none of the intermediate steps raised a flag.

**What it looks like**: An agent is tasked with researching a competitor and writing a report. In step 2, it searches the web and retrieves an article about the wrong company (a different company with a similar name). Every subsequent step — summarizing, analyzing, comparing — builds on this wrong data. The final report is polished, well-written, and entirely about the wrong company.

**Why it happens**: Each step *locally* makes sense. The agent summarized the article well. It analyzed the data correctly. It wrote a compelling report. The error happened at the foundation, and nothing in the pipeline verified the foundation was correct.

**How to prevent it**:
- **Verification checkpoints**: After critical steps, add an explicit verification step. "Before proceeding, confirm that the company you found matches: name, industry, and headquarters city."
- **Human-in-the-loop gates**: For high-stakes tasks, require human approval after the research step before proceeding to analysis.
- **Confidence thresholds**: If the agent's confidence in a step's output is below a threshold, pause and ask for clarification.

### Failure Mode 2: Context Overflow

The agent accumulates too much information and loses focus.

> **ANALOGY**: Imagine trying to write an essay while someone keeps handing you more documents to read. After a while, your desk is so covered with papers that you can't find the outline you wrote at the start. You're drowning in information. Your essay starts well-structured and ends as a confused ramble.

**What it looks like**: After 20 steps, the agent's context is stuffed with search results, API responses, and intermediate reasoning. It loses track of its original goal, repeats steps, gives contradictory instructions, and forgets initial constraints.

**Why it happens**: Context windows are finite. An agent on a complex task can fill even a 200K token window. Old information gets truncated or the model's attention becomes diluted.

**How to prevent it**:
- **Context summarization**: Periodically compress detailed history into summaries.
- **Scoped context**: Only include information relevant to the current step.
- **Subagent delegation**: Spawn a subagent with a clean, focused context for each subtask.

### Failure Mode 3: Tool Selection Errors

The agent picks the wrong tool for the job.

> **ANALOGY**: You ask someone to hang a picture on the wall, and they reach for a chainsaw. Not because they're malicious, but because the toolbox was poorly labeled, or they misunderstood the task, or the chainsaw was described as "a tool for making changes to walls."

**What it looks like**: An agent needs internal database data but calls a web search tool instead, getting plausible but wrong answers. Or it calls `delete` instead of `update`. Or it passes wrong parameters — searching "revenue Q4" when the field is "quarterly_income_q4."

**Why it happens**: The LLM chooses tools based on descriptions and context. If descriptions are ambiguous or tools sound similar (`search_documents` vs. `search_web`), the model picks wrong.

**How to prevent it**:
- **Crystal-clear tool descriptions**: Specify *when* to use it and *when not to*. "Searches internal docs. Do NOT use for current events or external data."
- **Fewer tools, better coverage**: 5 well-described tools beat 50 ambiguous ones.
- **Tool use confirmation**: For destructive actions, require the agent to state *why* it's choosing this tool before executing.

### Failure Mode 4: Instruction Drift

The agent forgets its original goal after many steps.

> **ANALOGY**: You're driving from Delhi to Mumbai with a co-driver giving directions. After four hours, the co-driver starts giving directions to Jaipur instead — not intentionally, but because they got confused by a road sign somewhere around Udaipur. They're still confident. They're still giving precise directions. They've lost the plot on where you're actually going.

**What it looks like**: Tasked with "Research competitor pricing in the Indian B2B SaaS market — no consumer products," the agent gradually starts including consumer pricing, then global pricing. By the end: a polished report about worldwide consumer electronics. Well-researched. Not what was asked.

**Why it happens**: As steps accumulate, original instructions become a smaller fraction of context. Recent steps are more "attention-grabbing" than instructions from the beginning. Off-topic but interesting search results pull the agent sideways.

**How to prevent it**:
- **Goal repetition**: Include the original goal in every step's prompt, not only the first.
- **Self-check prompts**: Every N steps: "Re-read the original goal. Are you still on track?"
- **Structured output**: Require the agent to restate its understanding of the goal alongside each action.

### Failure Mode 5: Infinite Loops

The agent keeps trying the same failed approach without adapting.

> **ANALOGY**: Someone trying to open a locked door by pushing harder, then pushing harder again, then pushing even harder — never considering that they should pull, or try a different door, or look for a key.

**What it looks like**: An API returns a timeout. The agent retries. Timeout. Retries. Timeout. It burns through API credits retrying the same failing request 200 times. Or: an agent generates code that fails a test, modifies one line, fails again, modifies the same line differently, fails again — never stepping back to reconsider its approach.

**Why it happens**: LLMs are trained to be helpful and persistent. For agents, persistence without strategic variation is a death spiral.

**How to prevent it**:
- **Retry limits**: Cap retries per action (3 is a reasonable default).
- **Escalation logic**: After N failures, change strategy or escalate to a human.
- **Cost budgets**: Set a maximum token or dollar budget per task.
- **Loop detection**: If the same action appears 3 times in a row, force a different action.

## Agents in the Real World (2026)

The gap between agent demos and agent reality is wide — but it is narrowing faster than most people realize. Here is where things stand.

### Karpathy's AutoResearch (March 2026)

In March 2026, Andrej Karpathy published AutoResearch — an open-source agent for automating machine learning research. The system is remarkable for how small it is: **630 lines of Python**. That's it.

AutoResearch works by running a ReAct loop against ML experiments. It formulates a hypothesis, writes experiment code, runs it, reads the results, reasons about what worked and what didn't, and designs the next experiment. In Karpathy's tests, it ran **12 experiments per hour** — roughly one every 5 minutes — and could execute **approximately 100 experiments overnight** while he slept.

Tobi Lutke, the CEO of Shopify, adapted AutoResearch for Shopify's recommendation systems and reported a **19% improvement** in recommendation quality — achieved through automated experimentation that would have taken his team weeks to run manually. Lutke mandated that teams use AI agents to explore solution spaces before committing engineering resources: run 50 experiments automatically before a human decides which direction to pursue.

> **INTUITION**: AutoResearch is not artificial general intelligence. It's a focused loop: hypothesize → code → run → observe → hypothesize again. The same loop a human researcher runs, but without needing to eat, sleep, check email, or lose motivation after the 40th experiment. The insight is that most research isn't creative leaps — it's systematic exploration of a space. Agents excel at systematic exploration.

### Devin: The First AI Software Engineer

Cognition's Devin, launched as the first "AI software engineer" in early 2024, represented a new category of agent — one with its own virtual machine, browser, terminal, and code editor. Devin operates in the same environment a human developer would: reading codebases, writing code, running tests, debugging failures, navigating documentation.

On SWE-bench — a standardized benchmark of real GitHub issues — Devin achieves approximately **14% autonomous issue resolution**: 14 out of 100 real bugs and feature requests solved without human intervention. These require reading unfamiliar codebases, writing correct code, and passing test suites. A year earlier, the best agents solved under 5%. The trajectory matters more than the current number.

### Claude Code Subagents and Cursor's Parallel Agents

Claude Code uses **subagent architecture** — the main agent spawns lightweight agents for parallel subtasks. One researches the authentication system, another searches for function references, a third analyzes tests. Each subagent has a narrow, clean context — reducing context overflow and instruction drift. Results flow back to the main agent for synthesis.

Cursor pushed parallelism further: up to **20 agents simultaneously** on different parts of a codebase — refactoring, updating APIs, writing tests, updating docs. The human reviews the collective output, not the individual keystrokes.

### India Examples: Swiggy Driver Dost and Freshworks Freddy AI

Indian technology companies have been among the most aggressive adopters of agentic AI, driven by the scale challenges unique to a market of 1.4 billion people.

**Swiggy's Driver Dost** assists Swiggy's delivery partners when problems arise — a restaurant is closed, a customer is unreachable, a payment hasn't processed. The distinction from a chatbot: Driver Dost doesn't *suggest* actions — it *takes* them. It calls the customer, waits, tries again, sends an SMS, checks alternate contact info, and only then asks the driver to wait or return the order. Multiple steps, multiple tools, autonomous execution.

**Freshworks' Freddy AI** evolved from a chatbot into a genuine agent in 2025. When a customer reports a billing issue, Freddy looks up the account, identifies the discrepancy, calculates the correct charge, issues a refund if warranted, sends a confirmation email, and updates the ticket — without a human agent touching the case. Freshworks reports Freddy resolves over **40% of support tickets** autonomously — not automated responses, but full resolutions with no human intervention.

> **REAL-LIFE**: At 100,000 tickets per day, even 30% automation has enormous impact. But the deeper insight: routine tasks go to agents, nuanced tasks stay with humans. Human agents handle *harder* problems — needing more skill, not less. Agents don't replace support teams. They restructure them.

## The Supervision Problem: The Math PMs Must Internalize

Agents in 2026 need supervision. Even the best models make errors roughly 3–5% of the time per step. That sounds small until you do the math. A 20-step agent with 96% per-step success:

```
0.96^20 = 0.44  →  56% chance of at least one error
0.96^50 = 0.13  →  87% chance of at least one error
```

Per-step reliability is high. End-to-end reliability for long chains is not. This means your agent architecture must account for errors: checkpoints, human review gates, rollback capabilities, and graceful degradation. The agent that works is designed to fail safely, not designed never to fail.

## How Agents Work at the API Level

Under the hood, every agent is a **loop**. Each iteration: send context to the LLM API → receive either a text response or a tool call → if it's a tool call, execute it and feed the result back → repeat until done.

```python
# Simplified agent loop (pseudocode)
context = [system_prompt, user_goal]

while not done:
    response = llm.generate(context)

    if response.has_tool_call:
        tool_name = response.tool_call.name      # e.g., "search_web"
        tool_args = response.tool_call.arguments  # e.g., {"query": "..."}
        result = execute_tool(tool_name, tool_args)
        context.append({"role": "tool", "content": result})
    else:
        final_answer = response.text
        done = True
```

Every framework listed in the comparison table is a more sophisticated version of this loop — adding state management, error handling, multi-agent coordination, and observability.

## The Cost and Latency Reality

Agents are expensive. A 15-step agent task costs 15x a single LLM call. A complex workflow with 50 LLM calls and 20 tool calls can cost $1–$5 per run — fine for a developer tool used 50 times a day, devastating for a consumer product used 50 million times a day.

Latency compounds similarly. If each LLM call takes 2 seconds across 15 steps, your agent takes 30 seconds minimum. Users tolerate this for high-value tasks ("research this topic" — they'll wait 2 minutes) but not for low-value ones ("what's the weather?" — they won't wait 30 seconds when Google answers in 200 milliseconds).

The product decision: agents should handle tasks where the value of automation justifies the cost and latency. Researching a competitor? Worth $2 and 3 minutes. Answering a simple FAQ? Use a RAG pipeline for $0.01 and 1 second.

<div class="exercise">

### Exercise: Build a Research Agent

**Goal**: Build an agent that takes a topic, searches the web for information, summarizes what it finds, and saves a report to a file.

**If you can code (30–45 minutes)**:

1. Choose a framework: Claude Agent SDK, OpenAI Agents SDK, or LangGraph
2. Define three tools:
   - `search_web(query: str)` — returns search results
   - `read_url(url: str)` — returns the content of a web page
   - `save_file(filename: str, content: str)` — saves content to a file
3. Write a system prompt that instructs the agent to:
   - Search for 3–5 sources on the given topic
   - Read the most promising 2–3 sources
   - Write a 500-word summary with key findings
   - Save the summary to a markdown file
4. Add a guardrail: the agent should stop after 15 steps maximum
5. Test it with the topic: "Current state of AI agents in Indian enterprise software"

**If you don't code (20–30 minutes)**:

1. Open Claude (claude.ai) and prompt: "You are a research agent with these tools: web_search, read_article, save_report. Plan how you would research [topic]. For each step: which tool, what input, what you expect back, and what you'd do next."
2. Observe the ReAct pattern in action — reasoning, tool selection, observation, adaptation
3. Ask yourself: Where would I add a human-in-the-loop checkpoint? What's the most likely failure mode? (Hint: cascading errors from a bad initial search, or the agent reading a paywalled page and getting garbage)

</div>

## Looking Ahead

The agent ecosystem is moving faster than any other area of AI. Frameworks will come and go. What won't change: the five-component architecture, the five failure modes (they're structural, not bugs), and the PM's role in deciding what should be agentic, where humans stay in the loop, and what happens when things go wrong.

The most important mental model for agents: **think of them as extremely capable but unreliable junior employees.** They can do remarkable work. They will occasionally make remarkable mistakes. Your job as a product leader is to build the systems — the guardrails, the checkpoints, the fallbacks — that capture the value while containing the risk.

The companies that get agents right won't be the ones with the most sophisticated AI. They'll be the ones with the most thoughtful product design around what happens when the AI is wrong.

---

**Chapter endnotes**

1. **Anthropic, "Building Effective Agents" (2024)**. The definitive guide to agent architecture from the makers of Claude. Covers the spectrum from augmented LLMs to fully autonomous agents, with the crucial insight that simpler agentic patterns should be preferred over complex multi-agent systems unless the task genuinely demands it. Available at anthropic.com/research.

2. **Yao, S. et al., "ReAct: Synergizing Reasoning and Acting in Language Models" (ICLR 2023)**. The foundational paper that established the Reason-Act-Observe loop used by virtually every agent framework. The key finding: interleaving reasoning traces with tool actions dramatically outperforms either chain-of-thought reasoning or tool-only approaches on knowledge-intensive tasks.

3. **Karpathy, A., "AutoResearch" (March 2026)**. Open-source repository demonstrating that a 630-line Python script can automate ML experimentation at 12 experiments/hour and ~100 overnight. Shopify's adaptation under Tobi Lutke yielded a 19% improvement in recommendation quality, demonstrating the practical economics of agentic research.

4. **Chase, H., "LangGraph: Building Stateful, Multi-Agent Applications" (2025)**. Harrison Chase's framework documentation and blog posts on graph-based agent orchestration. Essential reading for understanding how to model cyclic workflows, persistent state, and human-in-the-loop checkpoints in agent systems.

5. **swyx (Shawn Wang), "The Rise of Agent Engineering" (2025–2026)**. A series of essays and talks that shaped practical vocabulary around agent design — including the distinction between "agent" as a noun (a product) and "agentic" as an adjective (a property of a workflow). Swyx's framing of agents as "software 3.0" — where the behavior is specified in natural language rather than code — is essential context for product leaders.

6. **Anthropic, "Claude Agent SDK Documentation" (2026)**. Framework documentation covering subagent architecture, MCP integration, tool definition patterns, and safety-first agent design.

7. **OpenAI, "Agents SDK Documentation" (2026)**. Technical documentation for the Swarm successor, covering agent-to-agent handoffs, built-in guardrails, and the tracing system for observability.

8. **Cognition Labs, Devin technical reports and SWE-bench results (2024–2026)**. Architecture documentation and benchmark results for the most-referenced autonomous coding agent, tracking progression from initial launch through current capabilities.
