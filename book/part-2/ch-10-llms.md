<span class="chapter-number">Chapter 10</span>

# Large Language Models — The Engine of Modern AI {.chapter-title}

This is the most important technical chapter in the book.

Everything that follows — prompt engineering, RAG, agents, multi-modal AI, evaluations — builds on your understanding of how a large language model actually works. We won't use math. We won't wave our hands. We'll build genuine intuition, layer by layer, the way Jay Alammar explained transformers visually and the way Karpathy explained them through code.

By the end of this chapter, when someone says "The model attends to relevant tokens in its context window using multi-head self-attention," you'll know exactly what every word means — and more importantly, why it matters for the products you build.

## Tokens: The Atoms of Language

LLMs don't read words. They read **tokens** — word-pieces that are shorter than words but longer than individual characters.

The word "unhappiness" becomes three tokens: `["un", "happi", "ness"]`.
The word "the" is one token: `["the"]`.
A number like "2026" might be one token or two: `["20", "26"]`.

Why not use whole words? Because there are too many of them. The English language has roughly 170,000 words in current use, plus names, technical terms, code syntax, and words from other languages. A vocabulary of millions would be unmanageable. Tokens are a compromise: a vocabulary of 50,000-100,000 token-pieces that can be combined to represent any word in any language.

> **ANALOGY**: Think of alphabet blocks a child uses. The child has 26 blocks (letters) and can spell any English word. But spelling "consciousness" letter by letter is slow. Now imagine giving the child a bigger set of blocks — some with single letters, some with common pairs ("th", "ing", "tion"), and some with whole common words ("the", "and", "is"). With this mixed set, they can build words much faster while still handling rare words letter by letter. That's tokenization.

**Why this matters for you as a builder:**

1. **Cost**: AI APIs charge per token. Claude's pricing is per million input tokens and per million output tokens. A 1,000-word prompt is roughly 1,300 tokens. Understanding tokenization helps you estimate costs.

2. **Context window**: Every model has a maximum number of tokens it can process at once. Claude's 200K context window means it can hold roughly 150,000 words — about 500 pages of a book — in working memory simultaneously. GPT-4's standard context is 128K tokens. Google's Gemini 2.5 Pro reaches 1 million tokens.

3. **Performance**: Models are better at common tokens than rare ones. "Python" is one common token that the model has seen millions of times. An unusual variable name like "xylophoneManager" might be split into `["xy", "loph", "one", "Manager"]` — and the model has less experience with this combination.

> **REAL-LIFE**: When you use ChatGPT Plus ($20/month), OpenAI is subsidizing heavy users. Someone sending 500 messages per day costs OpenAI far more in compute (tokens processed) than someone sending 5 messages. This is why per-token pricing matters for AI businesses — and why Chapter 26 (Token Economics) is critical for anyone building AI products.

## The Transformer: AI's Greatest Architectural Innovation

In 2017, a team at Google published a paper titled "Attention Is All You Need." The paper introduced the **transformer** — an architecture that has since become the foundation of every major language model: GPT, Claude, Gemini, Llama, Mistral, and hundreds more.

To understand why the transformer was revolutionary, you need to understand what came before it.

### Before Transformers: Reading Through a Keyhole

> **ANALOGY**: Imagine reading a book by looking at it through a tiny keyhole that only shows one word at a time. You read left to right, one word at a time, trying to remember everything you've read so far. By the time you reach the end of a paragraph, you've partially forgotten the beginning. Long-distance connections — like a pronoun at the end of a paragraph referring to a noun at the beginning — become almost impossible to track.

That's how **RNNs (Recurrent Neural Networks)** and **LSTMs (Long Short-Term Memory networks)** worked. They processed text sequentially — one word at a time, left to right. Each word updated a "memory state" that tried to capture everything seen so far. But information decayed with distance. A reference to something 500 words ago was effectively invisible.

### The Transformer's Key Innovation: Attention

> **ANALOGY**: Now imagine you can see the entire page at once. Every word can look at every other word simultaneously and decide: "Which words on this page are most relevant to understanding *me*?" The word "it" looks at every other word and decides: "The word 'cat' three sentences back is very relevant to me. The word 'table' is not." This selective focus — this ability to **attend** to the relevant parts of the input — is what makes transformers powerful.

This is **self-attention**, and it's the core mechanism of the transformer. Let's build it up step by step.

### Self-Attention: The Cocktail Party

Consider the sentence: "The cat sat on the mat because it was tired."

What does "it" refer to? The cat? The mat? You know it's the cat — "tired" is a property of a living thing, not a floor covering. But how does a model figure this out?

In self-attention, every word creates three things:

1. **Query** (Q): "What am I looking for?" — like a question the word is asking
2. **Key** (K): "What do I contain?" — like a label describing what the word represents
3. **Value** (V): "What information do I carry?" — the actual content to pass along

The word "it" creates a Query: "I'm a pronoun. Who am I referring to?" Every other word presents its Key. The system computes a compatibility score between the Query of "it" and the Key of every other word. "Cat" gets a high score (animate noun, subject of the sentence). "Mat" gets a lower score. "The" gets almost zero.

```
Self-Attention for the word "it":

  The   cat   sat   on   the   mat   because   it   was   tired
  0.02  0.71  0.04  0.01 0.01  0.12  0.02      —    0.03  0.04
        ^^^^                    ^^^^
        highest attention       some attention
        ("it" = "cat")         (mat is possible
                                but less likely)
```

The attention scores become weights. "It" now carries a representation that's 71% influenced by "cat", 12% by "mat", and small amounts by everything else. The model has "understood" the reference — not through a grammar rule, but through learned patterns about which words tend to relate to which other words.

> **INTUITION**: Why is this called "attention"? The metaphor comes from human cognition. At a noisy cocktail party, you can focus on one conversation while filtering out all the background noise. Your brain "attends" to the relevant signal. Transformers do the same thing with words — they focus on the words that matter and ignore the noise. The 2017 paper's title, "Attention Is All You Need," was making a bold claim: this single mechanism, applied at scale, is sufficient to understand language. They were right.

### Multi-Head Attention: Looking at the Same Text in Different Ways

A single attention computation captures one type of relationship. But language has many simultaneous relationships:

- **Syntactic**: "The cat sat" — "sat" relates to "cat" as verb to subject
- **Semantic**: "tired" relates to "cat" because cats can be tired
- **Positional**: "it" relates to "cat" because "cat" was the most recent animate noun
- **Referential**: "the mat" relates to "the" as article to noun

**Multi-head attention** runs multiple attention computations in parallel — typically 32, 64, or 96 "heads." Each head independently learns to focus on a different type of relationship. One head might specialize in subject-verb agreement. Another in pronoun resolution. Another in long-range dependencies.

```
Multi-Head Attention (simplified):

Head 1 (syntax):    "sat" attends strongly to "cat" (subject-verb)
Head 2 (reference): "it" attends strongly to "cat" (pronoun resolution)
Head 3 (proximity): "mat" attends strongly to "on" and "the" (phrase structure)
Head 4 (semantic):  "tired" attends to "cat" and "sat" (tiredness context)

All heads combined → rich, multi-dimensional understanding of each word
```

### The Full Transformer Architecture

A transformer stacks many of these attention layers on top of each other. Claude Opus uses dozens of these layers. Each layer refines the model's understanding:

```
Input: "The cat sat on the mat because it was tired"
        ↓
   ┌─────────────────────────┐
   │  Tokenization           │  Convert words to token IDs
   │  + Positional Encoding  │  Add position information
   └────────────┬────────────┘
                ↓
   ┌─────────────────────────┐
   │  Transformer Layer 1    │  Basic word relationships
   │  (Multi-Head Attention  │
   │   + Feed Forward)       │
   └────────────┬────────────┘
                ↓
   ┌─────────────────────────┐
   │  Transformer Layer 2    │  Deeper patterns
   └────────────┬────────────┘
                ↓
        ... (many layers) ...
                ↓
   ┌─────────────────────────┐
   │  Transformer Layer N    │  Complex reasoning
   └────────────┬────────────┘
                ↓
   ┌─────────────────────────┐
   │  Output Layer           │  Probability over all tokens
   │  "Next token is..."     │  "also": 0.3, "very": 0.25,
   │                         │  "especially": 0.08, ...
   └─────────────────────────┘
```

Each layer has two sub-components:
1. **Multi-head self-attention**: Words look at each other (as described above)
2. **Feed-forward network**: Each word's representation is independently transformed through a small neural network — this adds "thinking" capacity beyond the relationships between words

The output is a probability distribution over the entire vocabulary. "The most likely next token is 'also' (30% probability), followed by 'very' (25%), followed by 'especially' (8%)."

## Context Windows: The Model's Working Memory

> **ANALOGY**: Imagine a desk. A small desk can hold 3 open books. A large desk can hold 50. The **context window** is the model's desk — it determines how much text the model can "see" simultaneously while generating a response. Your prompt, the system instructions, any retrieved documents, and the ongoing conversation all share this desk.

Context windows have grown dramatically:

| Model | Context Window | Approximate Pages |
|-------|---------------|-------------------|
| GPT-3 (2020) | 4,096 tokens | ~6 pages |
| GPT-4 (2023) | 128,000 tokens | ~200 pages |
| Claude 3 (2024) | 200,000 tokens | ~300 pages |
| Gemini 2.5 Pro (2025) | 1,000,000 tokens | ~1,500 pages |

Why does this matter? Because larger context windows mean:
- The model can read your entire codebase at once (Claude Code does this)
- You can feed entire documents for analysis, not small excerpts
- Conversations can be longer before the model "forgets" earlier messages
- RAG systems (Chapter 13) can provide more context to ground their answers

But there's a catch: **attention is quadratic**. If you double the context window, the computation required for self-attention quadruples (each token must attend to every other token). This is why longer context = more expensive = more time. Various optimizations (sparse attention, sliding window attention, linear attention) reduce this cost, but the fundamental tradeoff remains: more context = more compute = more money.

> **REAL-LIFE**: When Claude Code reads your project, it doesn't read every file. It strategically selects relevant files to stay within the context window — like a researcher who skims an entire library's catalog but reads only the most relevant books in full. The art of fitting the right information into a limited context window is called **context engineering** (Chapter 11).

## Temperature: The Creativity Dial

When the model generates the next token, it produces a probability distribution. Temperature controls how that distribution is interpreted:

- **Temperature 0**: Always pick the most probable token. Deterministic — same input always produces same output. Good for: code generation, factual answers, structured output.
- **Temperature 0.7**: Mostly pick probable tokens, but allow some randomness. Good for: creative writing, brainstorming, conversational AI.
- **Temperature 1.0**: Sample proportionally to the probabilities. More varied, sometimes surprising. Good for: poetry, fiction, exploring unusual ideas.
- **Temperature >1.0**: Amplify randomness. Low-probability tokens become more likely. Can produce creative gems or complete nonsense.

> **ANALOGY**: Temperature is like the "adventurous" dial on a restaurant ordering kiosk. At 0, you always get your safe favorite (chicken tikka). At 0.5, you usually get your favorite but occasionally try the paneer. At 1.0, you're genuinely exploring the menu. At 2.0, you're ordering the weirdest thing and hoping for the best.

## The Model Landscape: March 2026

The models available to you as a builder:

### Anthropic's Claude Family

| Model | Best For | Context | Relative Cost |
|-------|----------|---------|---------------|
| Claude Opus 4.6 | Complex reasoning, architecture decisions, code review | 200K | $$$$$ |
| Claude Sonnet 4.6 | Daily coding, writing, analysis — the workhorse | 200K | $$$ |
| Claude Haiku 4.5 | Classification, routing, simple Q&A — fast and cheap | 200K | $ |

### OpenAI's GPT Family

| Model | Best For | Context | Relative Cost |
|-------|----------|---------|---------------|
| GPT-5.2 | General tasks, multi-modal | 128K | $$$$ |
| o3 | Complex reasoning, math, logic — "thinking" model | 128K | $$$$$ |
| o4-mini | Reasoning at lower cost | 128K | $$ |

### Google's Gemini Family

| Model | Best For | Context | Relative Cost |
|-------|----------|---------|---------------|
| Gemini 2.5 Pro | Massive context, multi-modal | 1M | $$$$ |
| Gemini 2.5 Flash | Fast responses, good quality | 1M | $$ |

### Open Source

| Model | Org | Best For | Can Run Locally? |
|-------|-----|----------|-----------------|
| Llama 4 | Meta | General purpose, fine-tuning base | Yes (high-end GPU) |
| DeepSeek R1 | DeepSeek | Reasoning at 1/20th the cost | Yes |
| DeepSeek V3 | DeepSeek | General purpose, 685B parameters | Needs multiple GPUs |
| Mistral Large 2 | Mistral AI | European data compliance | Yes |

## Reasoning Models: Thinking Before Answering

> **ANALOGY**: Two students take a math test. Student A reads the question and writes an answer immediately. Student B reads the question, writes out their reasoning step by step in the margin, checks their work, then writes the final answer. Student B takes longer but gets more questions right. **Reasoning models** are Student B — they generate an internal "thinking" trace before producing the final answer.

OpenAI's o3 and o4-mini, DeepSeek's R1, and Claude's extended thinking all follow this pattern. When you ask a reasoning model "What's 127 × 43?", it doesn't predict the answer directly. It generates hidden steps:

```
Thinking:
- 127 × 40 = 5,080
- 127 × 3 = 381
- 5,080 + 381 = 5,461

Answer: 5,461
```

On the AIME 2024 math competition, this "think before answering" approach improved accuracy from around 17% (direct prediction) to over 78% (chain-of-thought reasoning). On coding benchmarks, the improvement is similarly dramatic.

The cost tradeoff is real: reasoning models use 3-10x more tokens (for the thinking trace) and take 2-5x longer to respond. But for complex problems — multi-step math, architectural decisions, legal analysis, code debugging — the accuracy improvement is worth the cost.

> **INTUITION**: Reasoning models represent a fundamental insight: you can trade compute time for accuracy. Traditional models are fast but sometimes wrong. Reasoning models are slower but more reliable for complex tasks. This tradeoff — called **inference-time compute scaling** — is one of the most important developments in AI. Instead of making models bigger (which requires billions in training cost), you make them think longer at inference time (which anyone can do).

## Token Economics: Why AI Costs Money Per Use

> **ANALOGY**: Traditional software is like a bus pass — you pay a flat fee and ride as much as you want. AI is like a taxi — every trip costs proportional to the distance traveled. This fundamental difference shapes everything about AI product economics.

Every time you send a message to Claude, the model processes your input tokens and generates output tokens. Each token requires GPU computation. GPUs are expensive — a single NVIDIA H100 costs $30,000-$40,000, and training frontier models requires thousands of them.

The pricing as of March 2026 (per million tokens):

| Model | Input Price | Output Price |
|-------|------------|-------------|
| Claude Haiku 4.5 | $0.80 | $4.00 |
| Claude Sonnet 4.6 | $3.00 | $15.00 |
| Claude Opus 4.6 | $15.00 | $75.00 |
| GPT-4o | $2.50 | $10.00 |
| DeepSeek V3 | $0.27 | $1.10 |

Why are output tokens more expensive? Because generating each output token requires a full forward pass through the model. Input tokens are processed in parallel (the model reads your entire prompt at once), but output tokens are generated one at a time, sequentially. Each new token depends on all previous tokens.

A practical example: your RAG chatbot handles 10,000 queries per day. Each query uses roughly 2,000 input tokens (system prompt + retrieved context + user question) and 500 output tokens (the answer). Using Claude Sonnet:

- Input: 10,000 × 2,000 = 20M tokens/day × $3/M = $60/day
- Output: 10,000 × 500 = 5M tokens/day × $15/M = $75/day
- **Total: $135/day = ~$4,050/month**

This is real money. Chapter 26 covers optimization strategies in depth — model routing (use Haiku for easy queries, Opus for hard ones), prompt caching (90% savings on repeated context), semantic caching (serve cached answers for similar questions).

## The Open Source Revolution

The most consequential shift in AI since the transformer itself may be the open-source revolution.

Meta's Llama models, DeepSeek's R1 and V3, Mistral's models, and dozens of others are free to download, modify, and deploy. DeepSeek R1 matches the reasoning performance of models that cost 20x more to access via API. Llama 4 runs on a high-end laptop.

This means:
- **Startups** can build AI products without paying per-token API costs
- **Privacy-sensitive applications** can run models locally — no data leaves the building
- **Researchers** can study and improve models without corporate gatekeepers
- **Countries** can build sovereign AI capabilities

The tradeoff: open-source models require infrastructure expertise. Running a 70-billion parameter model needs serious hardware (multiple GPUs, significant RAM). For most builders, API access to Claude/GPT/Gemini is more practical. But the option to go local exists and is improving rapidly.

<div class="exercise">
<div class="exercise-title">Try It Yourself</div>

1. **Token counting**: Go to any AI chat interface. Ask: "How many tokens is this sentence?" Then ask: "How many tokens would a 1000-word essay use?" Compare the model's estimates with the rule of thumb (1 token ≈ 0.75 words in English).

2. **Temperature experiment**: Ask Claude the same question at different temperatures (if your tool allows temperature control). Try: "Write a one-sentence description of rain." At temperature 0, you'll get the same response every time. At temperature 1, each response will be different. Notice how creativity increases alongside unpredictability.

3. **Context window awareness**: Open Claude Code and ask it to summarize a large file in your project. Then ask it about a detail from the beginning of the file. Can it remember? Now try with a very large file. At what point does it start losing details? This is the context window in action.

</div>

---

**Chapter endnotes**

[1] Jay Alammar's "The Illustrated Transformer" blog post remains the gold standard for visual explanation of the transformer architecture. His step-by-step walkthrough with diagrams makes the attention mechanism intuitive in a way that the original paper does not.

[2] Andrej Karpathy's "Let's Build GPT from Scratch" YouTube video (January 2023) builds a working transformer in Python, line by line, explaining every component. If you want to understand transformers at the code level, this is the single best resource.

[3] Lilian Weng's "Attention? Attention!" blog post at lilianweng.github.io provides a comprehensive survey of attention mechanisms from 2014 through the present, with mathematical notation for those who want the formal treatment.

[4] For production-oriented understanding of LLMs, Chip Huyen's "AI Engineering" (O'Reilly, 2025) covers model selection, tokenization strategies, cost optimization, and deployment patterns in detail.

[5] The "Attention Is All You Need" paper (Vaswani et al., 2017) introduced the transformer architecture with the famously bold title. Eight authors from Google Brain and Google Research. As of March 2026, the paper has over 130,000 citations — one of the most-cited papers in all of computer science.

[6] Token pricing data sourced from official pricing pages of Anthropic, OpenAI, and Google as of March 2026. Prices change frequently — always check the current pricing before making architectural decisions.
