<span class="chapter-number">Chapter 31</span>

# Reasoning Models — AI That Thinks Before Answering {.chapter-title}

Picture two students taking a math exam. Student A reads each question and immediately writes down an answer — no scratch work, no pausing, no checking. Student A is fast. Student A is confident. Student A gets about 60% of the questions right.

Student B reads each question, pauses, writes out their reasoning step by step on scratch paper, checks their work, reconsiders when something doesn't add up, and only then writes their final answer. Student B is slower — much slower. But Student B gets 92% of the questions right.

For the first seven years of the modern LLM era, every model was Student A. GPT-4, Claude 3 Opus, Gemini 1.5 — they all generated responses token by token, left to right, with no internal deliberation. The model predicted the next word, then the next, then the next. Whatever came out first was the answer. There was no mechanism for the model to stop, reconsider, explore alternatives, or check its reasoning.

In late 2024 and early 2025, a new category of model emerged: **reasoning models**. These are Student B. They think before they answer. And they're changing what AI can do.

## The Paradigm: Internal Thinking Traces

A reasoning model has a distinct two-phase response process:

1. **Thinking phase**: The model generates an internal chain of reasoning — exploring approaches, considering edge cases, checking intermediate steps, backtracking when it hits dead ends. This thinking trace can be hundreds or thousands of tokens long.
2. **Response phase**: The model synthesizes its thinking into a clean, final answer for the user.

```
Standard Model (Student A):
───────────────────────────────────────────────────
User: "Is 17 × 23 greater than 400?"
Model: "17 × 23 = 391. No, it is not greater than 400."
                                            ↑ generated directly
                                              (happens to be correct,
                                               but no verification)
───────────────────────────────────────────────────

Reasoning Model (Student B):
───────────────────────────────────────────────────
User: "Is 17 × 23 greater than 400?"

[Internal thinking — user may or may not see this]
  Let me calculate 17 × 23.
  17 × 20 = 340
  17 × 3 = 51
  340 + 51 = 391
  Is 391 > 400? No.
  Let me verify: 20 × 23 = 460, and 17 is 3 less than 20,
  so subtract 3 × 23 = 69. 460 - 69 = 391. Confirmed.

Model: "No. 17 × 23 = 391, which is less than 400."
                                            ↑ verified answer
───────────────────────────────────────────────────
```

> **ANALOGY**: Consider the difference between answering a question in a casual conversation versus answering the same question in a courtroom under oath. In conversation, you say the first thing that comes to mind. In court, you pause, consider the question carefully, think about whether your initial instinct is accurate, and only then speak. Reasoning models operate in "courtroom mode" — every answer is deliberated.

The thinking trace is not a gimmick. It fundamentally changes the model's capabilities on tasks that require multi-step logic, mathematical reasoning, planning, and careful analysis. On the GPQA benchmark (graduate-level science questions), standard models score around 50-60%. Reasoning models score 75-85%. On competition-level math (AIME), the gap is even wider.

## The Landscape: Who's Building What

As of early 2026, every major AI lab has released reasoning models. Here's the current field:

### OpenAI's o-Series

OpenAI pioneered the category with o1 (September 2024), followed by o3 and o4-mini (early 2025).

- **o3**: The flagship. Highest raw reasoning performance across most benchmarks. Expensive. Thinking traces can extend to tens of thousands of tokens.
- **o4-mini**: The cost-efficient option. Achieves 92% of o3's performance at roughly one-fifth the cost. Faster response times. For most production use cases, o4-mini is the better choice unless you need peak performance on the hardest problems.

### DeepSeek R1

DeepSeek, the Chinese AI lab, released R1 in January 2025 and it shook the industry. R1 matches o3's reasoning performance on most benchmarks — at one-twentieth the cost. It's open-source (MIT license), meaning you can download the weights, run it on your own infrastructure, and modify it without restrictions.

R1's significance goes beyond its performance. It demonstrated that reasoning capabilities are not locked behind proprietary approaches. The open-source community can build reasoning models that compete with the best commercial offerings.

### Google's Gemini 2.5 Pro

Gemini 2.5 Pro, released in March 2025, integrates reasoning as a native capability rather than a separate model family. It can dynamically allocate thinking effort — using minimal reasoning for simple queries and extended deliberation for complex ones. This adaptive approach avoids the latency penalty of reasoning on easy questions.

### Anthropic's Claude Extended Thinking

Claude's approach to reasoning, called "extended thinking," allows the model to use internal deliberation when the task warrants it. The thinking is visible to the user (unlike some implementations), promoting transparency. Claude's extended thinking is particularly strong on coding tasks, complex analysis, and multi-step planning.

## Performance Comparison

Here's how the models stack up on key benchmarks as of early 2026:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Reasoning Model Performance Comparison                │
├──────────────────┬──────────┬──────────┬──────────┬────────┬───────────┤
│                  │   GPQA   │   AIME   │  SWE-    │ Cost   │ Typical   │
│   Model          │ (Science)│  (Math)  │  bench   │ Index  │ Latency   │
│                  │          │          │ (Coding) │        │           │
├──────────────────┼──────────┼──────────┼──────────┼────────┼───────────┤
│ o3               │  87.7%   │  96.7%   │  71.7%   │ $$$$$  │ 45-90s    │
│ o4-mini          │  81.4%   │  93.4%   │  68.1%   │ $      │ 15-40s    │
│ DeepSeek R1      │  71.5%   │  79.8%   │  49.2%   │ ¢      │ 30-105s   │
│ Gemini 2.5 Pro   │  84.0%   │  92.0%   │  63.8%   │ $$     │ 20-60s    │
│ Claude (ext.     │  82.8%   │  90.2%   │  72.2%   │ $$$    │ 25-70s    │
│  thinking)       │          │          │          │        │           │
├──────────────────┼──────────┼──────────┼──────────┼────────┼───────────┤
│ Comparison:      │          │          │          │        │           │
│ GPT-4o (non-     │  53.6%   │  13.4%   │  33.2%   │ $$     │ 2-8s      │
│  reasoning)      │          │          │          │        │           │
│ Claude Sonnet    │  65.0%   │  27.4%   │  62.3%   │ $      │ 2-6s      │
│  (non-reasoning) │          │          │          │        │           │
└──────────────────┴──────────┴──────────┴──────────┴────────┴───────────┘

GPQA: Graduate-level science questions (physics, chemistry, biology)
AIME: American Invitational Mathematics Examination (competition math)
SWE-bench: Real GitHub issues requiring multi-file code changes
```

The numbers tell a stark story. On competition-level math, o3 scores 96.7% — roughly equivalent to a top-100 high school math competitor in the United States. GPT-4o, a non-reasoning model of comparable size and training, scores 13.4% on the same test. The reasoning mechanism is not a marginal improvement. It's a category shift.

## Cost-Performance Tradeoffs: The Builder's Decision Matrix

Reasoning models are powerful but expensive — not because the model itself costs more per token, but because the thinking phase generates many more tokens. A standard model might produce 200 tokens to answer a question. A reasoning model might produce 2,000 thinking tokens plus 200 response tokens — a 10x increase in total tokens.

The real tradeoffs that matter for builders:

### Tradeoff 1: Latency vs. Accuracy

```
Response Time Comparison (same complex coding question):

  o3            ████████████████████████████████████████████  ~90 seconds
  R1            ████████████████████████████████████████████████████  ~105 seconds
  Claude ext.   ██████████████████████████████████████        ~70 seconds
  Gemini 2.5    █████████████████████████████                 ~55 seconds
  o4-mini       ████████████████████                          ~35 seconds
  o3-mini       ███████████████                               ~27 seconds

  GPT-4o        ████                                          ~6 seconds
  (non-reasoning)
```

For a user waiting for a chatbot response, 90 seconds is an eternity. For an overnight batch job processing legal documents, 90 seconds per document is irrelevant. Your use case determines which tradeoff is acceptable.

> **REAL-LIFE**: DeepSeek R1 takes an average of 1 minute 45 seconds on complex reasoning tasks. o3-mini takes 27 seconds on comparable tasks. R1 costs 1/20th as much. If you're running a batch process where latency doesn't matter — analyzing 10,000 legal contracts overnight — R1's cost advantage is overwhelming. If you're powering an interactive coding assistant where developers expect sub-30-second responses, o4-mini or o3-mini is the better choice despite higher per-token costs.

### Tradeoff 2: Cost per Correct Answer

The metric that matters isn't cost per token — it's cost per correct answer. A cheaper model that gives wrong answers 30% of the time is more expensive than a pricier model that's right 95% of the time, because wrong answers require human review, retry cycles, or — worst case — reach the end user.

```
Cost per Correct Answer (hypothetical 1000 graduate-level questions):

  Model          Accuracy   Total Cost   Correct Answers   Cost/Correct
  ─────────────  ─────────  ──────────   ───────────────   ────────────
  o3             87.7%      $47.50       877               $0.054
  o4-mini        81.4%      $8.20        814               $0.010
  DeepSeek R1    71.5%      $2.40        715               $0.003
  Gemini 2.5 Pro 84.0%      $18.60       840               $0.022
  GPT-4o         53.6%      $9.80        536               $0.018
```

R1 is the cheapest per correct answer despite lower accuracy, because its per-token cost is so low. But if you need 85%+ accuracy and can't afford the human review cost for wrong answers, o3 or Gemini 2.5 Pro might be the rational choice.

### Tradeoff 3: When NOT to Use Reasoning Models

Reasoning models are the wrong tool for many common tasks. Here's a decision framework:

| Task | Use Reasoning Model? | Why |
|---|---|---|
| Creative writing | No | Creativity benefits from fluency, not deliberation |
| Simple Q&A ("What's the capital of France?") | No | Wastes compute on problems that don't need it |
| Translation | No | Pattern matching, not multi-step reasoning |
| Summarization | No | Compression, not logic |
| Chatbot conversation | No | Latency kills the conversational experience |
| Multi-step math | **Yes** | Exactly the strength of reasoning models |
| Complex code generation | **Yes** | Needs planning, error checking, multi-file awareness |
| Legal/medical analysis | **Yes** | Precision and careful reasoning are critical |
| Strategic planning | **Yes** | Benefits from exploring multiple approaches |
| Scientific reasoning | **Yes** | Requires chaining logical steps accurately |
| Ambiguous problems | **Yes** | Needs to consider multiple interpretations |

> **INTUITION**: Ask yourself: "Would a human expert pause and think carefully before answering this question?" If yes, a reasoning model will probably help. If a human would answer instantly from memory, a reasoning model adds cost and latency without improving quality.

## Inference-Time Compute Scaling: A New Paradigm

For years, the AI scaling paradigm was simple: more training compute = better model. Bigger datasets, more parameters, longer training runs. This was **training-time scaling**, and it produced GPT-4, Claude 3, and Gemini 1.5.

Reasoning models introduce a second dimension: **inference-time compute scaling**. Instead of spending more at training time, you spend more at inference time — giving the model more "thinking time" per query. The model's performance scales with the compute you allow it to use during inference.

```
The Two Dimensions of AI Scaling:

                        ▲ Inference-Time Compute
                        │  (thinking time per query)
                        │
                        │          ★ o3 (high effort)
                        │       ★ o4-mini
                        │    ★ Gemini 2.5 Pro
                        │ ★ Claude ext. thinking
                        │
    ────────────────────┼──────────────────────► Training-Time Compute
                        │                        (model size & data)
                        │
                 Standard│models live here:
                  GPT-4o ★  Claude Sonnet ★
                        │
```

This has profound implications:

1. **Adaptive difficulty**: You can dial inference compute up or down per query. Easy question? Minimal thinking. Hard question? Extended deliberation. This is what Gemini 2.5 Pro does natively.

2. **Diminishing returns on model size**: If you can improve performance by thinking longer at inference time, you may not need a bigger base model. DeepSeek R1 demonstrates this — a smaller base model with extended reasoning matches much larger models.

3. **User-controlled quality**: Some APIs let you set the "thinking budget" — how many tokens the model is allowed to use for internal reasoning. More budget = better answers = higher cost = longer wait. The user (or the application developer) gets to choose.

## Deep Research: Reasoning at Scale

The most dramatic application of reasoning models is **deep research** — systems that spend minutes or hours reasoning through complex, multi-source research tasks.

OpenAI's Deep Research, Gemini's Deep Research, and similar offerings from other labs take a research question and spend 5-30 minutes:

1. Decomposing the question into sub-questions
2. Searching the web and internal documents for relevant information
3. Reading and synthesizing dozens of sources
4. Reasoning through contradictions and conflicts in the sources
5. Producing a comprehensive, cited research report

> **REAL-LIFE**: A venture capital analyst used Gemini Deep Research to analyze the competitive landscape for a fintech startup. The system spent 12 minutes reading 47 web sources, cross-referencing financial data, identifying three competitors the analyst hadn't considered, and producing a 3,000-word report with citations. The analyst estimated the equivalent manual research would have taken 4-6 hours. The report wasn't perfect — it missed some nuances that required industry expertise — but it was a 90% solution in 2% of the time.

Deep research represents a frontier where reasoning models transition from answering questions to conducting investigations. The compound AI pattern from Chapter 30 is at work here: a reasoning model orchestrating retrieval, synthesis, and verification in a multi-step pipeline.

## Building with Reasoning Models: Practical Patterns

### Pattern 1: Reasoning as a Judge

Use a reasoning model as the evaluator in your compound system, not the generator. Have a fast model generate responses, then use a reasoning model to evaluate whether the response is correct. This gives you reasoning-level quality at a fraction of the cost, because the evaluator processes fewer tokens than the generator.

```
Cost-Efficient Architecture with Reasoning Judge:

  User Query → Fast Model (Haiku/Flash) → Response
                                              │
                                              ▼
                              Reasoning Model (o4-mini)
                              "Is this response correct,
                               complete, and well-supported?"
                                              │
                                    ┌─────────┴──────────┐
                                    ▼                    ▼
                                  PASS                 FAIL
                               (serve to user)    (retry with larger
                                                   model or more context)
```

### Pattern 2: Reasoning for Planning, Fast Models for Execution

Use a reasoning model to create a plan, then use fast models to execute each step of the plan. The reasoning model thinks through the approach once; the fast models carry it out.

This works well for code generation: a reasoning model plans the architecture and file structure, then fast models generate each file according to the plan.

### Pattern 3: Conditional Reasoning

Don't make every query go through reasoning. Build a classifier that detects when reasoning is needed and routes accordingly. Most queries — 80-90% in typical applications — don't benefit from extended thinking.

```
Conditional Reasoning Router:

  Query → Complexity Classifier
               │
       ┌───────┼───────┐
       ▼       ▼       ▼
    Simple  Moderate  Complex
       │       │       │
       ▼       ▼       ▼
    Haiku   Sonnet   o4-mini
    (~2s)   (~4s)    (~30s)
```

### Pattern 4: Thinking Budget Control

When using APIs that support thinking budget parameters, set different budgets for different contexts:

| Context | Thinking Budget | Rationale |
|---|---|---|
| Real-time chat | Low (1,024 tokens) | Latency matters more than depth |
| Code review | Medium (4,096 tokens) | Balance of speed and thoroughness |
| Security audit | High (16,384 tokens) | Thoroughness matters more than speed |
| Batch analysis | Maximum | No latency constraint, maximize quality |

## The Philosophical Shift

Reasoning models force a rethinking of what we mean by "AI capability." Before reasoning models, AI capability was roughly a function of model size and training data. Capability was fixed at deployment — the model could do what it could do, and more compute at inference time didn't help.

Reasoning models decouple capability from model size. A smaller model that thinks for two minutes can outperform a larger model that answers immediately. This means:

- **Capability becomes a budget decision**, not a model selection decision
- **The same model can perform at different levels** depending on how much thinking time you allocate
- **The cost of intelligence is becoming elastic** — you pay for exactly the level of reasoning you need

This is a profound shift for builders. You're no longer choosing between "smart and expensive" and "fast and cheap." You're choosing how smart you need this particular response to be, and paying accordingly.

<div class="exercise">
<div class="exercise-title">Try It Yourself</div>

1. **Reasoning comparison**: Take a complex logic puzzle or math problem. Submit it to a standard model (Claude Sonnet, GPT-4o) and a reasoning model (Claude with extended thinking, o4-mini). Compare the answers and the time taken. Where does the reasoning model's advantage appear most clearly?

2. **Thinking trace analysis**: When using a reasoning model with visible thinking, read the thinking trace carefully. Where does the model consider alternative approaches? Where does it catch and correct its own mistakes? This reveals the mechanism behind the performance improvement.

3. **Cost calculator**: Estimate the monthly cost of your application using (a) a standard model for everything, (b) a reasoning model for everything, and (c) a compound approach that routes simple queries to standard models and complex queries to reasoning models. What's the cost difference?

4. **When-not-to-reason exercise**: List ten tasks your product or workflow requires AI for. For each, decide whether a reasoning model would improve the result. For the ones where reasoning wouldn't help, articulate why — is it a pattern-matching task? A creativity task? A speed-critical task?

</div>

---

**Chapter endnotes**

[1] OpenAI's o1 system card (September 2024) introduced the concept of "reasoning tokens" — internal chain-of-thought tokens that the model generates before producing its visible response. The o3 and o4-mini models extended this paradigm with controllable thinking budgets.

[2] DeepSeek-R1: "Incentivizing Reasoning Capability in LLMs via Reinforcement Learning" (DeepSeek AI, January 2025). The paper demonstrated that reasoning capabilities can emerge through reinforcement learning without explicit chain-of-thought supervision, and that the resulting open-source model matches proprietary reasoning models.

[3] Benchmark data compiled from official model cards, published evaluations, and independent benchmarks (Chatbot Arena, LMSYS). Individual benchmark scores vary across evaluation runs and specific configurations — treat them as approximate indicators rather than precise measurements.

[4] Inference-time compute scaling concept described in Snell et al., "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters" (2024). The paper demonstrated that allocating more compute at inference time can outperform training larger models on reasoning tasks.

[5] Deep Research capabilities evaluated based on publicly available features from OpenAI, Google, and Perplexity as of March 2026. These systems are evolving rapidly — specific capabilities and pricing may have changed since publication.

[6] Latency and cost comparisons based on real-world testing across multiple queries and difficulty levels. Your actual experience will vary based on query complexity, API load, and configuration settings. Treat these numbers as representative ranges rather than guaranteed performance.
