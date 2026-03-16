<span class="chapter-number">Chapter 14</span>

# Fine-Tuning — When Prompting Isn't Enough {.chapter-title}

You've been driving a rental car across a familiar city. Prompt engineering (Chapter 11) was learning to give better directions to the GPS. RAG (Chapter 13) was mounting a local guidebook on the dashboard. Both made the rental car work well enough for most trips.

But what happens when you need a Formula 1 car instead of a rental? When you need a model that doesn't need to be told how to behave — it already knows, because the knowledge has been baked into its weights?

That's fine-tuning. And understanding when to use it — and when not to — separates builders who burn money from builders who build competitive moats.

## The Customization Spectrum

Every technique for making an AI model work better for your use case sits on a spectrum of cost, effort, and permanence:

```
The Model Customization Spectrum

Cost & Effort
     ▲
     │
     │  ┌─────────────────────┐
     │  │   PRE-TRAINING       │  $2M–$100M+
     │  │   Train from scratch  │  Months of work
     │  │   Needs TB of data    │  Own the model entirely
     │  └─────────────────────┘
     │
     │  ┌─────────────────────┐
     │  │   FULL FINE-TUNING   │  $1K–$100K
     │  │   Update all weights  │  Days–weeks
     │  │   Needs 1K–100K      │  Model learns new behavior
     │  │   quality examples    │
     │  └─────────────────────┘
     │
     │  ┌─────────────────────┐
     │  │   LoRA / QLoRA       │  $10–$1K
     │  │   Update <1% of      │  Hours–days
     │  │   weights             │  90%+ quality of full FT
     │  │   Consumer GPU ok     │
     │  └─────────────────────┘
     │
     │  ┌─────────────────────┐
     │  │   RAG                │  $0.01–$10/query
     │  │   Retrieve context    │  Hours to set up
     │  │   at query time       │  No training needed
     │  └─────────────────────┘
     │
     │  ┌─────────────────────┐
     │  │   PROMPT ENGINEERING │  $0 (just your time)
     │  │   Better instructions │  Minutes–hours
     │  │   No model changes    │  Fastest to iterate
     │  └─────────────────────┘
     │
     └──────────────────────────────────────────► Permanence of change
          Temporary                            Permanent
          (per request)                    (baked into weights)
```

Each step up the spectrum means more investment, more permanence, and less flexibility. A prompt can be changed in seconds. A fine-tuned model takes hours or days to retrain. A pre-trained model from scratch takes months and millions of dollars.

The builder's job is to start at the bottom and climb only when the layer below genuinely fails.

> **ANALOGY**: Think of teaching someone to cook. Prompt engineering is giving them a detailed recipe each time ("Add 2 tsp cumin, then..."). RAG is giving them a cookbook they can reference while cooking. Fine-tuning is sending them to culinary school — after that, they don't need the recipe for dishes in that cuisine; the knowledge is internalized. Pre-training is raising a child in a kitchen from birth — they absorb cooking as a native skill. Each level takes more investment but produces deeper, more automatic competence.

## What Fine-Tuning Actually Does

A large language model like Claude or GPT-4 is a neural network with billions of parameters — numbers (called **weights**) that determine how the model responds to any input. During pre-training, these weights are adjusted across trillions of tokens of text, learning the patterns of language, reasoning, and knowledge.

Fine-tuning takes this pre-trained model and continues the training process — but on a much smaller, more specific dataset. The weights shift slightly to encode the patterns in your data.

> **INTUITION**: Imagine a concert pianist who has spent 20 years mastering classical music. Their fingers, muscle memory, and musical intuition are extraordinary. Now they want to learn jazz. They don't start from scratch — they leverage everything they already know about timing, harmony, and finger technique. They practice jazz-specific patterns: syncopation, improvisation, blue notes. After a few months of focused jazz practice, they can play jazz fluently. They didn't forget classical — but jazz patterns are now also encoded in their muscles. That's fine-tuning. The pianist's 20 years of classical training is pre-training. The focused jazz practice is fine-tuning. The result is a musician with broad competence plus deep specialization.

Technically, here's what happens:

1. **Start with a pre-trained model**: It already understands language, reasoning, and broad world knowledge
2. **Prepare training data**: Pairs of inputs and desired outputs (more on data quality later)
3. **Run training**: The model processes your examples. For each one, it generates its own response, compares it to the desired output, calculates the error, and adjusts its weights slightly to reduce that error
4. **Repeat across your dataset**: Multiple passes (called **epochs** — complete cycles through your data) until the model reliably produces outputs that match your desired patterns
5. **Evaluate**: Test on examples the model hasn't seen to verify it generalized, rather than memorizing your training data

The math is gradient descent — the same algorithm used to train the original model — but applied with a much smaller **learning rate** (the size of each weight adjustment). You want the model to learn your patterns without forgetting what it already knows. Too high a learning rate and the model "forgets" its pre-training (this is called **catastrophic forgetting**). Too low and it doesn't learn your data.

```
Fine-Tuning Visualized:

Pre-trained model         Your data              Fine-tuned model
┌─────────────────┐      ┌──────────────┐      ┌─────────────────┐
│ General language │      │ 1,000 pairs  │      │ General language │
│ Broad knowledge  │  +   │ of input →   │  =   │ + YOUR specific  │
│ General style    │      │ ideal output │      │   patterns/style │
│ No specialization│      │              │      │   /knowledge     │
└─────────────────┘      └──────────────┘      └─────────────────┘

What changes: The model's weights shift slightly
What stays: 99%+ of the model's original capabilities
What you get: A model that natively "knows" your domain
```

## When to Fine-Tune (and When Not To)

This is the most important section of this chapter. Most builders fine-tune too early or for the wrong reasons. Here's a decision framework:

### Fine-tune when:

**1. You need consistent style or format that prompts can't reliably enforce.**
If you've written detailed prompts and the model still produces outputs that vary in tone, structure, or format — and you've tried RAG with examples — fine-tuning can lock in consistency. A customer service bot that needs to always respond in your brand's specific voice. A medical note generator that must follow a precise format every single time.

**2. You need the model to learn domain-specific behavior patterns.**
Not domain knowledge (that's RAG's job) — domain *behavior*. A model fine-tuned on how financial analysts reason about quarterly reports will approach a new report like a financial analyst, not like a general assistant trying to follow instructions.

**3. Latency or cost per query matters at scale.**
A well-fine-tuned smaller model (7B or 13B parameters) can often match a larger model (70B+) on a narrow task — while being 5-10x cheaper and faster per query. If you're making millions of API calls per month on a specific task, fine-tuning a smaller model can cut costs dramatically.

**4. You want to reduce prompt length.**
Long system prompts with many examples, rules, and edge cases are expensive (you pay per token on every call) and fragile (one more rule can break the balance). Fine-tuning encodes those rules into the weights, letting you use shorter prompts.

**5. You're building a competitive moat.**
A fine-tuned model on proprietary data is something competitors cannot replicate by writing better prompts. Bloomberg's financial LLM (BloombergGPT) is valuable not because of its architecture but because of the 40+ years of proprietary financial data it was trained on.

### Do NOT fine-tune when:

**1. Your problem is actually a retrieval problem.**
If the model gives wrong answers because it lacks specific knowledge — product details, documentation, recent events — that's a RAG problem. Fine-tuning on your documentation will be expensive and go stale the moment the docs change. RAG is dynamic; fine-tuning is static.

**2. You haven't exhausted prompt engineering.**
Before spending days on data preparation and training, have you tried: few-shot prompting with 5-10 examples? Chain-of-thought prompting? System prompts with detailed rules? Structured output formats? Most teams skip these and jump straight to fine-tuning. Bad idea.

**3. Your data is small or low quality.**
Below 500 high-quality examples, fine-tuning is unlikely to generalize. And if your data is noisy, inconsistent, or wrong, you'll fine-tune a confidently incorrect model. That's worse than the base model.

**4. The task is broad or general.**
Fine-tuning narrows. It makes a model better at specific things, sometimes at the cost of general ability. If you need a model that handles customer service *and* code generation *and* creative writing, don't fine-tune — use the best general model with good prompts.

**5. Your domain knowledge changes frequently.**
A model fine-tuned on your product catalog from January won't know about products launched in March. If your knowledge base changes weekly, use RAG. Fine-tune only on patterns that are stable over time.

> **REAL-LIFE**: Stitch Fix, the online personal styling service, fine-tuned models on their proprietary data — not product descriptions (those change constantly and are handled by retrieval) but *stylist behavior patterns*. How do experienced stylists match clothing items to client preferences? What makes a great outfit recommendation? These behavioral patterns are stable over years. By fine-tuning on stylist reasoning patterns rather than product catalogs, they got a model that "thinks like a stylist" while using RAG to stay current on inventory. That's the correct split.

### The Decision Flowchart

```
Is the model giving wrong answers?
├── Wrong KNOWLEDGE? ──────────────────────► Use RAG (Chapter 13)
│   (doesn't know your products/docs)
│
├── Wrong FORMAT/STYLE? ──────────────────► Try prompt engineering first
│   │                                        Did it work?
│   │                                        ├── Yes ──► Stop here
│   │                                        └── No ───► Fine-tune
│
├── Wrong REASONING PATTERN? ─────────────► Fine-tune
│   (doesn't think like your domain expert)
│
└── Too SLOW or EXPENSIVE? ───────────────► Fine-tune smaller model
    (need to run at scale cheaply)
```

## Types of Fine-Tuning

### Full Fine-Tuning

In full fine-tuning, you update every weight in the model. For a 7-billion parameter model, that means adjusting 7 billion numbers. For a 70-billion parameter model, 70 billion.

This requires enormous GPU memory. A 7B model in full precision (FP32 — 32-bit floating point, meaning each weight takes 32 bits of memory) requires ~28 GB of GPU memory for the model weights alone. During training, you also need memory for gradients, optimizer states, and activations — roughly 4x the model size. So full fine-tuning a 7B model requires ~112 GB of GPU memory. A 70B model? Over a terabyte.

Full fine-tuning produces the highest quality results because every weight can adapt. But it's expensive, requires enterprise-grade hardware, and creates a complete copy of the model for every variant you train.

### LoRA: The 90% Solution at 10% Cost

**LoRA (Low-Rank Adaptation)** was introduced by Edward Hu and colleagues at Microsoft in 2021, and it changed fine-tuning from an enterprise-only activity to something a graduate student could do.

> **ANALOGY**: Imagine you're renovating a house. Full fine-tuning is tearing down every wall and rebuilding from the floor up — you can change anything, but it's extremely expensive and time-consuming. LoRA is more like adding a few strategically placed rooms: you leave the existing structure intact and attach small additions that change the house's behavior. The original plumbing, electrical, and foundation (99%+ of the model) stay untouched. The additions (0.1%-1% of parameters) provide the new capabilities.

Here's what LoRA does technically:

In a transformer, the attention mechanism uses large **weight matrices** — tables of numbers that determine how tokens relate to each other. These matrices might be 4096×4096 (about 16 million numbers each). In full fine-tuning, you'd update all 16 million numbers.

LoRA's insight: the changes needed for fine-tuning are **low-rank**. Instead of updating the full 4096×4096 matrix, you can decompose the update into two much smaller matrices — say, 4096×16 and 16×4096. When multiplied together, they produce an update of the same shape (4096×4096) but are parameterized by only ~130,000 numbers instead of 16 million. That's a 99% reduction in trainable parameters.

```
Full Fine-Tuning vs LoRA:

Full Fine-Tuning:
┌───────────────────────────────────┐
│  Original Weight Matrix W         │
│  (4096 × 4096 = 16.7M params)    │
│  ← ALL parameters updated         │
└───────────────────────────────────┘

LoRA:
┌───────────────────────────────────┐
│  Original Weight Matrix W         │
│  (4096 × 4096 = 16.7M params)    │   FROZEN — not updated
│  ← stays FROZEN                   │
└────────────────┬──────────────────┘
                 │ + (added at inference)
┌────────────┐   │   ┌────────────┐
│ Matrix A   │ × │ × │ Matrix B   │
│ (4096 × r) │   │   │ (r × 4096) │
│  r = 16    │   │   │  r = 16    │
│ 65K params │   │   │ 65K params │
└────────────┘   │   └────────────┘
                 │
Total trainable: ~130K params (0.8% of original)
Quality: 90-97% of full fine-tuning
```

The rank `r` is a hyperparameter (a setting you choose before training) that controls the expressiveness of the adaptation. Common values are 8, 16, 32, or 64. Higher rank = more parameters = more expressive = more expensive. Most tasks work well with r=16 or r=32.

Why is this so powerful?

1. **Memory**: Instead of 112 GB for a 7B model, LoRA needs ~14-20 GB — fits on a single consumer GPU
2. **Speed**: Training is 2-3x faster because you're updating far fewer parameters
3. **Storage**: The LoRA adapter (the two small matrices) is typically 10-100 MB, while the full model is 14-140 GB. You can store hundreds of LoRA adapters for different tasks alongside one base model
4. **Composability**: You can swap adapters at runtime. One base model, different LoRA adapters for different customers or tasks

Sebastian Raschka, one of the foremost researchers on LLM fine-tuning and author of *Build a Large Language Model (From Scratch)*, has written extensively on why LoRA works so well. His research confirms that for most practical tasks, LoRA achieves 90-97% of full fine-tuning quality. The remaining 3-10% gap matters for cutting-edge research models but rarely matters for production applications.

### QLoRA: Fine-Tuning on Your Laptop

**QLoRA (Quantized LoRA)**, introduced by Tim Dettmers and colleagues at the University of Washington in 2023, combined two techniques: **quantization** (reducing the precision of model weights to use less memory) and LoRA.

> **INTUITION**: Quantization is like reducing the resolution of an image. A full-resolution photo might be 20 megapixels. Compress it to 5 megapixels and you lose some detail, but for most practical purposes — posting on social media, sending in an email — the compressed version is indistinguishable. Quantization does the same for model weights: instead of storing each weight as a 32-bit or 16-bit number (high precision), you store it as a 4-bit number (much lower precision). A 7B parameter model goes from ~28 GB (FP32) to ~3.5 GB (4-bit quantization).

QLoRA freezes the base model in 4-bit quantized form (using minimal memory) and then applies LoRA adapters in higher precision (16-bit) on top. The result:

- A 7B model can be fine-tuned on a single GPU with 8 GB VRAM — a consumer gaming GPU
- A 70B model can be fine-tuned on a single 48 GB GPU (like the NVIDIA A6000)
- Quality loss from quantization is surprisingly small — Dettmers' paper showed QLoRA matching full 16-bit fine-tuning on standard benchmarks

This was the democratization moment. Before QLoRA, fine-tuning a 70B model required a cluster of A100 GPUs costing hundreds of thousands of dollars. After QLoRA, a researcher with a $1,500 GPU could do meaningful fine-tuning work.

## Data Quality Over Data Quantity

If there is one message to take from this chapter, it's this: **the quality of your fine-tuning data matters more than the quantity, by an order of magnitude.**

The research is consistent on this point. Teams at Meta, Google, and Anthropic have all shown that models fine-tuned on 1,000 carefully curated, expert-verified examples outperform models fine-tuned on 100,000 scraped, noisy examples.

Why? Because a language model is a pattern-matching machine of extraordinary sensitivity. Feed it inconsistent patterns and it learns inconsistency. Feed it errors and it learns to make errors — confidently. Feed it 100,000 examples where 5% have subtle mistakes, and the model might learn those mistakes as deliberate patterns.

### What "High Quality" Means

1. **Correct**: Every output is factually accurate and complete
2. **Consistent**: All examples follow the same format, tone, and conventions
3. **Representative**: Examples cover the full range of inputs the model will encounter, including edge cases
4. **Diverse**: Not 1,000 variations of the same example — genuine variety in inputs while maintaining consistency in output quality
5. **Unambiguous**: For each input, the output is the best response, not one of several acceptable responses that differ significantly

### The Data Preparation Process

```
Raw Data                    Filtered Data              Training Data
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ 50,000 examples  │       │ 5,000 examples   │       │ 1,000 examples   │
│ from production   │──────►│ after removing   │──────►│ expert-reviewed  │
│ logs, documents,  │ Clean │ duplicates, low  │Review │ verified correct │
│ existing data     │       │ quality, errors  │       │ gold standard    │
└──────────────────┘       └──────────────────┘       └──────────────────┘
                    90% removed              80% removed
                    (noise, duplicates)      (not good enough)
```

> **REAL-LIFE**: When Hugging Face released Zephyr, one of the highest-performing 7B chat models of 2023, they didn't collect the most data. They collected the best data. Their training dataset was carefully filtered using AI-assisted ranking (a technique called DPO — Direct Preference Optimization). The model trained on this curated data outperformed models trained on datasets 10x larger. The open-source community took note: the arms race shifted from "who has the most data" to "who has the cleanest data."

### Common Data Mistakes

1. **Including sensitive data**: Personal information, credentials, internal communications. Fine-tuning on this means the model might generate it for other users. Always scrub PII (Personally Identifiable Information) before training.

2. **Inconsistent formatting**: Some examples use JSON, others use plain text, others use XML. The model gets confused about which format to use.

3. **Including "bad" examples**: Training on customer service conversations that include agent mistakes teaches the model to make those same mistakes.

4. **Imbalanced distribution**: 900 examples of one category and 100 of another. The model becomes excellent at the dominant category and terrible at the underrepresented one.

5. **Synthetic data without verification**: Using GPT-4 to generate fine-tuning data for a smaller model (a technique called distillation) works well — if you verify the synthetic data. Without verification, you're amplifying GPT-4's mistakes into a smaller model that lacks the capability to self-correct.

## Real-World Fine-Tuning: Three Case Studies

### Bloomberg's Financial LLM (BloombergGPT)

In 2023, Bloomberg published a paper on **BloombergGPT** — a 50-billion parameter model trained on 40+ years of financial data from the Bloomberg Terminal: SEC filings, earnings reports, financial news, analyst reports, and market data. This was a hybrid approach: roughly half the training data was financial, and half was general-purpose (to maintain broad language abilities).

The result: BloombergGPT outperformed GPT-3 on every financial NLP benchmark — sentiment analysis of earnings calls, named entity recognition in financial texts, financial question answering — while remaining competitive on general benchmarks. The model understood that "long" in a financial context means holding a position, not the opposite of short. That "bearish" isn't about animals. That "leveraged" has a specific financial meaning involving borrowed capital.

Bloomberg's competitive advantage wasn't the model architecture. It was the data. No competitor has 40 years of curated financial data. This is fine-tuning as a moat.

### Code Llama

Meta's **Code Llama** (2023) started with Llama 2, a strong general-purpose model, and fine-tuned it on 500 billion tokens of code. Then they created further specializations: Code Llama - Python (fine-tuned additionally on 100 billion tokens of Python code) and Code Llama - Instruct (fine-tuned on instruction-following data for coding tasks).

This demonstrates the layered approach: general model → domain fine-tuning → task-specific fine-tuning. Each layer narrows the model's focus while deepening its expertise. Code Llama - Python was better at Python than Code Llama, which was better than Llama 2, which was better than a model trained from scratch on the same amount of Python code alone.

### Stitch Fix's Stylist Model

Stitch Fix fine-tuned models not on their product catalog (which changes constantly) but on **stylist behavior patterns** — how expert human stylists match clothing to client preferences, body types, style preferences, and lifestyle descriptions. The fine-tuned model could then reason about styling the way a human stylist does, while retrieving current inventory through RAG.

This split — fine-tune on stable reasoning patterns, retrieve dynamic knowledge — is a pattern worth remembering. It combines the permanence of fine-tuning with the freshness of retrieval.

## The Open-Source Revolution

Before 2023, fine-tuning was a corporate activity. You needed proprietary models (GPT-3, GPT-4), expensive API access, or massive compute infrastructure. The open-source revolution changed this completely.

### The Stack

1. **Base models**: Meta's Llama 3, Mistral's models, Google's Gemma, Microsoft's Phi, Alibaba's Qwen — powerful models with open weights that you can fine-tune without permission or per-token fees

2. **Hugging Face**: The GitHub of machine learning. Hosts 800,000+ models and 200,000+ datasets. Their `transformers` and `peft` libraries make loading a model, preparing data, and running fine-tuning a matter of 30-50 lines of code. Hugging Face turned fine-tuning from a research project into a software engineering task.

3. **LoRA and QLoRA via PEFT**: The `peft` library (Parameter-Efficient Fine-Tuning) from Hugging Face implements LoRA, QLoRA, and other efficient methods. What once required custom research code now requires a configuration file.

4. **Training frameworks**: Hugging Face's `trl` (Transformer Reinforcement Learning) library handles supervised fine-tuning, DPO, RLHF, and other training paradigms with standardized interfaces.

5. **Hardware access**: RunPod, Lambda Cloud, Vast.ai, and even Google Colab provide GPU access from $0.50/hour. A QLoRA fine-tune of a 7B model on 1,000 examples takes 1-4 hours — costing $2-$8 in cloud compute.

> **REAL-LIFE**: In January 2024, a solo developer named Eric Hartford fine-tuned a series of "uncensored" Llama models using QLoRA on a single GPU. These models, released on Hugging Face as "Dolphin," became some of the most downloaded open-source models — used by thousands of developers worldwide. One person, one GPU, a few hundred dollars of compute. That's the democratization of fine-tuning.

### The Practical Workflow

For a builder who wants to fine-tune today, the workflow looks like this:

1. **Choose a base model**: Llama 3 8B for most tasks, Llama 3 70B if you need more capability, Mistral 7B or Qwen 2.5 for specific strengths
2. **Prepare data**: JSONL format — one JSON object per line, each with an "instruction" or "input" field and an "output" field
3. **Configure LoRA**: Set rank (r=16 is a good default), alpha (scaling factor, typically 2× rank), target modules (the attention matrices to adapt)
4. **Train**: Use Hugging Face `trl`'s `SFTTrainer`. Monitor loss curves. Stop when validation loss stops improving.
5. **Evaluate**: Test on held-out examples. Compare against the base model and against prompted-only approaches.
6. **Deploy**: Merge LoRA weights into base model for simplest deployment, or serve the adapter separately for flexibility.

<div class="exercise">

### Exercise: Evaluate the Fine-Tuning Decision

You're building a customer support chatbot for a mid-sized SaaS company (50,000 customers, 500 support tickets per day). The support team has 3 years of ticket history — about 500,000 resolved tickets.

**Part 1:** Using the decision framework from this chapter, determine whether you should: (a) use prompt engineering only, (b) use RAG, (c) fine-tune, or (d) combine approaches. Justify your choice.

**Part 2:** If you decide to fine-tune, answer:
- What data would you use? (All 500K tickets? A curated subset?)
- What would you fine-tune on — knowledge or behavior?
- Would you use full fine-tuning, LoRA, or QLoRA? Why?
- How would you handle the fact that product features change quarterly?

**Part 3:** Estimate the cost and time for your approach. Include data preparation, training compute, and ongoing maintenance.

**Suggested approach**: Start with the decision flowchart. Recognize that "wrong knowledge" (not knowing the product) is a RAG problem, while "wrong behavior" (not responding like your support team) is a fine-tuning problem. The best solution likely combines both.

</div>

## Key Takeaways

1. **Start at the bottom of the spectrum.** Prompt engineering, then RAG, then fine-tuning. Each layer has diminishing returns — don't climb before you've exhausted the layer below.

2. **Fine-tuning changes behavior, not knowledge.** Use it to teach a model how to think and respond, not what to know. Knowledge changes; behavior patterns are more stable.

3. **1,000 excellent examples beat 100,000 mediocre ones.** Data curation is the real work of fine-tuning. Budget more time for data preparation than for training.

4. **LoRA has made fine-tuning accessible to everyone.** 90%+ of full fine-tuning quality at a fraction of the cost. Unless you have a specific reason to do full fine-tuning, start with LoRA.

5. **Fine-tuning is a moat when your data is proprietary.** Competitors can copy your prompts. They can't copy your fine-tuned model trained on data they don't have.

6. **The open-source stack is production-ready.** Hugging Face + LoRA + a single rented GPU = a fine-tuning capability that was enterprise-only two years ago.

**Chapter endnotes**

The fine-tuning landscape is evolving rapidly. Key references for going deeper:

- **Sebastian Raschka**, *Build a Large Language Model (From Scratch)* (2024) — The most rigorous and practical treatment of LLM training and fine-tuning from first principles. Raschka's blog posts on LoRA comparisons are essential reading.
- **Tim Dettmers et al.**, "QLoRA: Efficient Finetuning of Quantized Language Models" (2023) — The paper that made fine-tuning a consumer GPU activity. Dettmers' blog post "Which GPU(s) to Get for Deep Learning" is the definitive hardware guide.
- **Edward Hu et al.**, "LoRA: Low-Rank Adaptation of Large Language Models" (2021) — The original LoRA paper. Concise and well-written.
- **Hugging Face documentation** on PEFT, TRL, and the Alignment Handbook — The practical "how to" once you understand the "why."
- **Shawn Wu et al.**, "BloombergGPT: A Large Language Model for Finance" (2023) — The case study for domain-specific fine-tuning at scale.
- **Chip Huyen**, "Building LLM Applications for Production" (2023) — Excellent framing of when to fine-tune vs. other approaches.
- **Hamel Husain's fine-tuning guides** — Practical, opinionated, and battle-tested workflows for fine-tuning open-source models.
