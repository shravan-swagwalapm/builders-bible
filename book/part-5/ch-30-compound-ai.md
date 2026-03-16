<span class="chapter-number">Chapter 30</span>

# Compound AI Systems — Why Combinations Beat Bigger Models {.chapter-title}

In February 2024, a team at UC Berkeley's AI Research lab (BAIR) — led by Matei Zaharia, Omar Khattab, and others — published a blog post that reframed the entire AI industry. The title: "The Shift from Models to Compound AI Systems." Their argument was precise and backed by evidence: the highest-performing AI applications in production are not using a single large model. They are using systems of multiple components — smaller models, retrievers, code executors, verifiers, and memory stores — orchestrated together.

This wasn't a theoretical position. They pointed to Google Search (which combines retrieval, ranking models, knowledge graphs, and now Gemini-generated overviews), GitHub Copilot (which combines code retrieval, multiple model calls, and post-processing filters), and AlphaCode 2 (which generates one million candidate solutions, then uses a separate model to filter them down to a handful). In every case, the compound system outperformed any single model, no matter how large.

The implications for builders are profound. You don't need the biggest, most expensive model for every task. You need the right combination of components, each optimized for its role, working together through well-designed interfaces. This chapter teaches you how to think about, design, and build those systems.

## Why a Single Model Isn't Enough

Consider what happens when you ask a large language model a factual question about your company's Q3 revenue. The model doesn't know. It was trained on public internet data, not your internal financials. No amount of scaling — no larger context window, no better architecture — will give it access to data it has never seen.

> **ANALOGY**: Think of a brilliant consultant who graduated top of their class but started work today. They know everything published in textbooks and journals. But they don't know your company's org chart, your revenue numbers, your customer complaints, or the decision made in last Tuesday's meeting. To be useful, they need access to your internal documents, your databases, your colleagues' expertise. A compound AI system is that consultant plus a filing cabinet, a calculator, a research assistant, and a fact-checker — each doing what they're best at.

This is the fundamental limitation that drives compound systems. A single model, regardless of size, has:

- **Knowledge cutoff**: It doesn't know what happened after its training data ended
- **No access to private data**: Your databases, documents, and APIs are invisible to it
- **No ability to take actions**: It can suggest sending an email but cannot send one
- **No self-verification**: It cannot check whether its own output is correct
- **Fixed cost-quality tradeoff**: Every query pays the same price, whether it's "What's 2+2?" or "Design a distributed system architecture"

A compound system addresses each of these limitations with a dedicated component.

## The Reference Architecture

Every compound AI system, from a startup's chatbot to Google's search infrastructure, follows a recognizable pattern. The components vary in sophistication, but the roles are consistent:

```
                         Compound AI System — Reference Architecture

    ┌──────────────────────────────────────────────────────────────────┐
    │                        USER QUERY                                │
    │                  "What were our Q3 sales                         │
    │                   in the Mumbai region?"                         │
    └───────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                      1. ROUTER                                   │
    │  Classifies the query. Decides which pipeline to activate.       │
    │  Simple question? → Fast model.  Complex analysis? → Full pipeline│
    │  Inappropriate? → Reject.  Needs tools? → Route to tool executor.│
    └───────────────────────────┬──────────────────────────────────────┘
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
    ┌────────────────┐ ┌───────────────┐ ┌────────────────────┐
    │  2. RETRIEVER  │ │ 3. TOOL       │ │  4. MEMORY         │
    │  Searches docs,│ │ EXECUTOR      │ │  Stores past       │
    │  databases,    │ │ Runs SQL,     │ │  conversations,    │
    │  vector stores │ │ calls APIs,   │ │  user preferences, │
    │  for relevant  │ │ executes code │ │  learned facts     │
    │  context       │ │               │ │                    │
    └───────┬────────┘ └──────┬────────┘ └─────────┬──────────┘
            │                 │                     │
            └────────────┬────┴─────────────────────┘
                         ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                     5. GENERATOR                                 │
    │  The LLM. Receives: original query + retrieved context +         │
    │  tool results + conversation history. Produces a response.       │
    └───────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                     6. EVALUATOR                                 │
    │  Checks the response. Is it grounded in the retrieved context?   │
    │  Does it contain hallucinations? Is it safe? Is it complete?     │
    │  If it fails → loops back to Generator with corrections.         │
    └───────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
    ┌──────────────────────────────────────────────────────────────────┐
    │                    VERIFIED RESPONSE                              │
    │  "Q3 Mumbai region sales were ₹4.2Cr, up 18% from Q2.           │
    │   Top product: Widget Pro (₹1.8Cr). Source: sales_db, row 4471" │
    └──────────────────────────────────────────────────────────────────┘
```

Let's examine each component.

### 1. The Router: Traffic Control for Intelligence

The router is where cost optimization begins. Not every query needs a powerful model. "What time is the meeting?" doesn't require the same compute as "Analyze the competitive implications of our pricing strategy."

A well-designed router classifies incoming queries and directs them to the appropriate pipeline:

| Query Type | Route | Model | Approx. Cost |
|---|---|---|---|
| Simple factual ("When is the next holiday?") | Direct answer from knowledge base | No LLM needed | ~$0 |
| Moderate ("Summarize this document") | Retriever → Small model | Haiku / GPT-4o-mini | ~$0.001 |
| Complex ("Compare our strategy to competitor X") | Full pipeline with retrieval + tools | Opus / GPT-4o | ~$0.05 |
| Creative ("Write a product launch email") | Direct to generator, no retrieval needed | Sonnet / GPT-4o | ~$0.01 |
| Dangerous ("How do I bypass authentication?") | Safety filter → Reject | Classifier only | ~$0.0001 |

> **REAL-LIFE**: Cursor, the AI-powered code editor, uses exactly this pattern. When you type a simple autocomplete, it uses a fast, cheap model. When you ask it to refactor an entire file, it routes to a more powerful model. When you use their Agent mode to make changes across 20 files, it spawns up to 20 parallel sub-agents. The user experiences seamless intelligence. Behind the scenes, a router is making economic decisions hundreds of times per session.

### 2. The Retriever: Connecting Models to Reality

The retriever bridges the gap between what the model knows (its training data) and what it needs to know (your specific context). This is RAG — Retrieval-Augmented Generation — which Chapter 14 covered in depth. In a compound system, the retriever is one component among many, not the entire architecture.

Advanced retrieval in compound systems goes beyond simple vector search:

- **Multi-source retrieval**: Search across documents, databases, and APIs simultaneously
- **Re-ranking**: Use a separate model to re-rank retrieval results by relevance
- **Query decomposition**: Break a complex question into sub-questions, retrieve for each, then synthesize
- **Adaptive retrieval**: Decide whether retrieval is even needed (some queries don't require external context)

### 3. The Tool Executor: Hands for the Brain

The tool executor gives the system the ability to act, not merely talk. It can run SQL queries against databases, call external APIs, execute Python code for calculations, send emails, update CRM records, or trigger workflows.

The key design principle: tools should be **narrow and safe**. A tool that can "execute any SQL" is dangerous. A tool that can "query the sales database with read-only access, limited to aggregate functions" is useful and contained.

### 4. Memory: Learning from Interactions

Memory gives the system persistence across conversations. Without memory, every interaction starts from zero. With memory, the system knows that this user prefers concise answers, works in the Mumbai office, and asked about Q3 sales yesterday (so today's follow-up about Q4 comparisons has context).

Memory in compound systems operates at multiple levels:

- **Session memory**: The current conversation (stored in the context window)
- **User memory**: Long-term facts about this specific user (stored in a database)
- **System memory**: Patterns learned across all users (stored as updated prompts or fine-tuned weights)

### 5. The Generator: The LLM at the Center

The generator is the LLM itself — the component most people think of when they hear "AI." But in a compound system, it's one piece, not the whole puzzle. The generator receives the original query enriched with retrieved context, tool results, memory, and routing decisions. Its job is synthesis: combining all these inputs into a coherent, accurate response.

### 6. The Evaluator: The Quality Gate

The evaluator is what separates production systems from demos. It checks the generator's output against the retrieved context (Does the response match the source documents?), against safety criteria (Is the response appropriate?), and against quality standards (Is it complete, well-structured, and accurate?).

When the evaluator detects a problem, the system loops: the generator tries again, perhaps with additional context or different instructions. This evaluate-and-retry loop is what gives compound systems their reliability edge over single-model architectures.

## DSPy: Programming — Not Prompting — AI Systems

The most important framework for compound AI systems comes from Stanford's NLP group. It's called **DSPy** (pronounced "dee-ess-pie"), created by Omar Khattab, and it represents a fundamental shift in how we build with LLMs.

The core insight: writing prompts by hand is like writing assembly code. It works, but it doesn't scale, it's fragile, and small changes in one place break things in unexpected other places.

> **INTUITION**: Consider how web development evolved. In the early days, developers wrote raw HTML strings in their server code. Then came templates. Then component frameworks. Each layer of abstraction made it possible to build more complex applications without managing every detail by hand. DSPy does the same for AI systems — it replaces hand-written prompts with declarative modules that are automatically optimized.

DSPy introduces three key concepts:

**Signatures**: Define what a module does (input → output) without specifying how.
```
question -> answer                      # Simple Q&A
context, question -> answer             # RAG-style Q&A
document -> summary                     # Summarization
claim, evidence -> verdict, reasoning   # Fact-checking
```

**Modules**: Composable building blocks that implement signatures.
```
retrieve = dspy.Retrieve(k=5)           # Retrieve top-5 passages
generate = dspy.ChainOfThought("context, question -> answer")
```

**Optimizers (formerly Teleprompters)**: Algorithms that automatically find the best prompts, few-shot examples, and even fine-tuning data for your modules — given a set of training examples and a quality metric.

The result: instead of spending weeks tweaking prompts, you define what you want, provide examples of good output, and let DSPy's optimizer figure out the prompts. When you switch from one model to another (say, from GPT-4o to Claude Sonnet), the optimizer re-tunes automatically. The prompts that work best for GPT-4o are different from those that work best for Claude, and DSPy handles this without human intervention.

> **REAL-LIFE**: In benchmarks published by the DSPy team, optimized pipelines consistently outperform hand-crafted prompts — often by 10-20% on accuracy metrics. More importantly, they're robust to model changes. A hand-crafted prompt tuned for GPT-4 might degrade when you switch to Claude. A DSPy pipeline re-optimizes and maintains performance.

## The Optimization Game: Right Model for the Right Task

The most powerful lever in compound AI systems is model selection per task. Not every component needs the most powerful (and expensive) model. The economics are dramatic:

```
Model Cost Comparison (per million tokens, approximate, March 2026):

    Claude Opus 4      ████████████████████████████████████████  $15.00 / $75.00
    GPT-4o             ██████████████████                        $2.50 / $10.00
    Claude Sonnet 4    ████████████████                          $3.00 / $15.00
    Gemini 2.5 Pro     █████████████                             $1.25 / $10.00
    Claude Haiku 3.5   ██                                        $0.80 / $4.00
    GPT-4o-mini        █                                         $0.15 / $0.60
    Gemini 2.0 Flash   █                                         $0.10 / $0.40
    DeepSeek V3        ▎                                         $0.27 / $1.10

    (Input / Output pricing shown)
```

A compound system that routes intelligently can achieve near-Opus quality at near-Haiku cost:

| Component | Best Model Choice | Why |
|---|---|---|
| Router / Classifier | Flash / Haiku / GPT-4o-mini | Classification is a simple task; fast models excel |
| Retrieval re-ranking | Haiku / Sonnet | Needs good judgment but not creativity |
| Simple generation | Haiku / GPT-4o-mini | Summarization, formatting, extraction |
| Complex reasoning | Opus / GPT-4o / Gemini Pro | Only 5-15% of queries typically need this |
| Evaluation / fact-check | Sonnet / GPT-4o | Needs accuracy but not deep reasoning |
| Safety classification | Fine-tuned small model | Fastest, cheapest, most consistent |

> **ANALOGY**: Think of a hospital. Not every patient needs the chief surgeon. A triage nurse handles the initial assessment. A general practitioner handles routine cases. A specialist handles complex cases. The chief surgeon is reserved for the cases where their expertise is irreplaceable. The hospital doesn't become worse because it uses different skill levels — it becomes better, because each professional is doing what they're best at, and the chief surgeon isn't exhausted from treating sprained ankles.

The math is compelling. Suppose 70% of your queries are simple (route to Haiku at $0.80/M tokens), 20% are moderate (route to Sonnet at $3.00/M), and 10% are complex (route to Opus at $15.00/M). Your blended cost:

```
Blended cost = (0.70 × $0.80) + (0.20 × $3.00) + (0.10 × $15.00)
             = $0.56 + $0.60 + $1.50
             = $2.66 per million input tokens

vs. sending everything to Opus:
             = $15.00 per million input tokens

Savings: 82% cost reduction with minimal quality loss
```

That's not a 10% optimization. That's a 5-6x cost reduction. For a product handling millions of queries per day, this is the difference between a viable business and one that bleeds money.

## AlphaCode 2: The Power of Generate-Then-Filter

Google DeepMind's AlphaCode 2 is the most extreme example of compound AI thinking. Its approach to competitive programming problems is radically different from a single model's attempt:

1. **Generate**: Produce approximately 1,000,000 candidate solutions using a large code generation model
2. **Filter**: Use a separate model to cluster similar solutions and eliminate obviously wrong ones
3. **Evaluate**: Run surviving candidates against test cases
4. **Select**: Use another model to pick the best solution from the survivors

The result: AlphaCode 2 performs at the 85th percentile of human competitive programmers — better than 85% of humans who compete in these contests. No single model call, no matter how powerful, achieves this. The system's intelligence emerges from the combination of generation, filtering, and evaluation.

> **INTUITION**: This is how expert human problem-solving often works too. A novelist doesn't write one perfect draft. They write many drafts, evaluate each one, combine the best parts, and iterate. A chess grandmaster doesn't consider one move — they consider dozens and prune the bad ones. AlphaCode 2 automates this generate-and-filter process at a scale no human could match.

The builder's lesson: sometimes the best approach isn't a better prompt or a bigger model. It's generating many candidates and selecting the best one. This pattern — **sample then filter** — appears across frontier AI systems.

## Compound Systems in Production: Three Case Studies

### Case Study 1: Zomato's Firefly Orchestrator

Zomato, India's largest food delivery platform, processes millions of customer support queries daily. Their AI system, internally called Firefly, is a textbook compound architecture:

- **Intent classifier** (small, fast model): Determines whether the query is about order status, refund request, restaurant complaint, or general inquiry
- **Entity extractor**: Pulls out order IDs, restaurant names, dates, and amounts from the user's message
- **Database connector**: Fetches real-time order status, delivery partner location, payment records
- **Policy engine**: Checks company policies for refund eligibility, compensation rules, escalation criteria
- **Response generator** (larger model): Synthesizes all the above into a natural, empathetic response
- **Safety checker**: Ensures the response doesn't make unauthorized promises or share sensitive data

No single model could do all of this. The system's effectiveness comes from each component being purpose-built and the orchestration layer connecting them intelligently.

### Case Study 2: Google Overviews (Search Generative Experience)

When you search Google in 2026, the AI-generated overview at the top of the page is produced by a compound system:

- **Query understanding**: Classifies the query type and intent
- **Traditional search**: Retrieves relevant web pages using Google's existing search infrastructure
- **Knowledge graph**: Pulls structured facts from Google's knowledge base
- **Gemini generation**: Synthesizes retrieved information into a coherent overview
- **Grounding verification**: Checks that every claim in the overview is supported by a source
- **Safety and quality filters**: Multiple layers of checking before display

The system serves billions of queries per day. The economic impossibility of using a single large model for every query — at Google's scale, that would cost billions per month — made the compound approach not a choice but a necessity.

### Case Study 3: Cursor's Parallel Agent Architecture

Cursor, the AI-powered code editor that has become the fastest-growing developer tool of 2025-2026, demonstrates compound thinking in software engineering:

- **Tab completion**: Tiny, fast model for real-time autocomplete (responds in <100ms)
- **Inline edit**: Medium model for single-file changes
- **Chat**: Large model for explaining code, answering questions
- **Agent mode**: Orchestrator that spawns up to 20 parallel sub-agents, each working on a different file, coordinated by a planning model
- **Linting and verification**: Non-AI code analysis tools checking the AI's output
- **Context engine**: Retrieves relevant code from across the codebase to feed into each model call

The 20-parallel-agent architecture is remarkable. When you ask Cursor's agent to "refactor the authentication system," the planning model breaks the task into independent sub-tasks (update the auth middleware, modify the login component, adjust the API routes, update the tests), assigns each to a parallel agent, and coordinates the results. Work that would take a single model call minutes happens in seconds.

## Designing Your Own Compound System

Here's a practical framework for designing compound AI systems. Not every system needs every component — the art is knowing which components to include and which to skip.

### Step 1: Map Your Query Distribution

Before building anything, understand what your users actually ask. Sample 1,000 real queries (or realistic synthetic ones) and classify them:

```
Query Distribution Analysis:

    Simple/factual     ████████████████████████████████  62%
    Moderate complexity ████████████████                  24%
    Complex reasoning   ██████                             9%
    Out-of-scope        ███                                5%
                        ─────────────────────────────────────
                        0%    20%    40%    60%    80%   100%
```

This distribution determines your architecture. If 62% of queries are simple, a powerful router that handles those cheaply is your highest-leverage investment.

### Step 2: Design the Router First

The router is the most important component because it determines the cost and quality of everything downstream. A misrouted simple query wastes money. A misrouted complex query produces bad results.

Start with a simple classifier — even a rule-based one — and upgrade to a model-based router when you have enough data to train it. Common routing signals:

- Query length (longer queries tend to be more complex)
- Presence of specific keywords ("compare," "analyze," "why" suggest complexity)
- User tier (premium users might always get the best model)
- Task type (code generation vs. summarization vs. conversation)

### Step 3: Add Components Incrementally

Don't build the full six-component architecture on day one. Start with:

1. Router + Generator (minimum viable compound system)
2. Add Retriever when the model needs external knowledge
3. Add Evaluator when accuracy is critical
4. Add Memory when users have repeat interactions
5. Add Tool Executor when the system needs to take actions

Each addition should be justified by a specific failure mode you're observing. "The model hallucinated company financials" justifies adding a retriever. "The model gave an unsafe response" justifies adding an evaluator. Build because you need to, not because the architecture diagram looks incomplete.

### Step 4: Instrument Everything

Compound systems are harder to debug than single-model calls because failures can occur at any component and propagate through the chain. Instrument each component with:

- **Latency**: How long does each component take?
- **Cost**: How much does each model call cost?
- **Quality**: Does the evaluator pass or fail? On what criteria?
- **Route distribution**: Are queries being routed correctly?

```
Compound System Observability Dashboard:

Component       Avg Latency    p99 Latency    Cost/Query    Error Rate
─────────────   ───────────    ───────────    ──────────    ──────────
Router          12ms           45ms           $0.0001       0.1%
Retriever       89ms           340ms          $0.0003       0.8%
Generator       1,240ms        4,200ms        $0.0089       0.3%
Evaluator       430ms          1,100ms        $0.0012       0.2%
Tool Executor   210ms          890ms          $0.0000       1.2%
─────────────   ───────────    ───────────    ──────────    ──────────
Total           1,981ms        6,575ms        $0.0105       2.6%
```

### Step 5: Optimize the Bottleneck

Once instrumented, you'll see where the time and money go. Typical findings:

- The generator is the latency bottleneck → consider streaming the response while the evaluator runs in parallel
- The retriever is the quality bottleneck → invest in better chunking, re-ranking, or hybrid search
- The router is misclassifying → collect routing errors and retrain
- Most cost goes to one component → right-size the model for that component

## Common Pitfalls

**Over-engineering**: Building a six-component system when a single API call would suffice. If your use case is "summarize this document," you probably don't need a router, retriever, evaluator, and memory system. Start simple.

**Under-engineering the router**: Using the same expensive model for every query because it's easier than building a router. This works at prototype scale. It bankrupts you at production scale.

**Tight coupling**: Building components that are deeply dependent on each other's internal implementation. When you swap one model for another, the whole system breaks. Design clean interfaces between components.

**Ignoring latency**: Each component adds latency. A six-component chain where each component takes 500ms means a 3-second response time before the user sees anything. Use streaming, parallelism, and caching aggressively.

**Evaluator theater**: Adding an evaluator that always passes. If your evaluator approves 99.9% of responses, it's not doing anything useful. A good evaluator catches 5-15% of responses and sends them back for improvement.

## The Economics of Compound Systems

The business case for compound systems rests on two pillars:

**Pillar 1: Cost reduction through routing.** As shown above, intelligent routing can reduce costs by 80%+ compared to using a single powerful model for every query. At scale (millions of queries per day), this is the difference between profitability and unsustainability.

**Pillar 2: Quality improvement through specialization.** A system where each component is optimized for its specific role outperforms a single generalist model. The retriever finds better context than the model's memory alone. The evaluator catches errors that the generator misses. The tool executor performs calculations with perfect accuracy instead of the model's approximate arithmetic.

The BAIR team summarized this insight concisely: "State-of-the-art AI results are increasingly obtained by compound systems with multiple components, not monolithic models."

This doesn't mean single model calls are dead. For many applications — creative writing, brainstorming, casual conversation — a single powerful model is the right architecture. But for production systems where accuracy, cost, and reliability matter, compound systems are where the industry is heading.

<div class="exercise">
<div class="exercise-title">Try It Yourself</div>

1. **Query distribution mapping**: Take any product you use regularly (email, food delivery, banking). Write down 20 queries a user might ask an AI assistant for that product. Classify each as simple, moderate, or complex. What percentage falls into each category? Does this match the typical 60/25/15 distribution?

2. **Router design exercise**: For the same product, design a routing strategy. What signals would you use to classify query complexity? What model would you assign to each tier? Estimate the cost savings compared to using one model for everything.

3. **Compound system sketch**: Pick a real-world AI feature you admire (Cursor's Agent, Google's AI Overviews, any chatbot you've used). Sketch the compound architecture you think powers it. What components does it need? Draw the flow from user query to final response, labeling each component.

4. **Failure mode analysis**: For your compound system sketch, identify three ways it could fail. For each failure, which component is responsible? How would you detect the failure? How would you fix it?

</div>

---

**Chapter endnotes**

[1] Matei Zaharia, Omar Khattab, Lingjiao Chen, Jared Quincy Davis, Heather Miller, Chris Potts, James Zou, Michael Carbin, Jonathan Frankle, Naveen Rao, and Ali Ghodsi. "The Shift from Models to Compound AI Systems." Berkeley AI Research blog, February 2024. The post that crystallized the compound AI paradigm, arguing that state-of-the-art results increasingly come from multi-component systems rather than single models.

[2] Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang, Keshav Santhanam, Sri Vardhamanan, Saiful Haq, Ashutosh Sharma, Thomas T. Joshi, Hanna Moazam, Heather Miller, Matei Zaharia, and Christopher Potts. "DSPy: Compiling Declarative Language Model Calls into State-of-the-Art Pipelines." International Conference on Learning Representations (ICLR), 2024. The foundational DSPy paper demonstrating automated prompt optimization.

[3] AlphaCode 2 details from Google DeepMind's technical report, December 2023. The system generates ~1 million candidate solutions per problem, then uses filtering and clustering to select the best few — performing at the 85th percentile of competitive programmers.

[4] Cursor's architecture details drawn from public statements by the Cursor team and analysis of the product's behavior. As of March 2026, Cursor's Agent mode supports up to 20 parallel sub-agents for complex codebase-wide operations.

[5] Model pricing data sourced from official pricing pages of Anthropic, OpenAI, Google DeepMind, and DeepSeek as of March 2026. Pricing changes frequently — always verify current rates before making architectural decisions.

[6] Zomato's AI customer support system details based on public presentations and engineering blog posts from the Zomato technology team, 2025.
