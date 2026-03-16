<span class="chapter-number">Chapter 9</span>

# What AI Actually Is — A History of Machines That Learn {.chapter-title}

The term "Artificial Intelligence" was coined at a conference at Dartmouth College in 1956. Seven researchers gathered for a summer workshop based on the proposal that "every aspect of learning or any other feature of intelligence can in principle be so precisely described that a machine can be made to simulate it."

That was 70 years ago. The field has been through cycles of euphoria and disappointment — "AI summers" and "AI winters" — ever since. Understanding this history isn't academic nostalgia. It's the map that explains why the current breakthrough happened *now*, what's genuinely different this time, and what the real limitations are.

## The Family Tree of AI

Before we dig into the history, here's the big picture. These terms get thrown around interchangeably, but they're actually a nested hierarchy — each one fits inside the previous one:

```
┌─────────────────────────────────────────────────────┐
│  Artificial Intelligence (AI)                        │
│  Any system that performs tasks normally requiring    │
│  human intelligence                                  │
│                                                      │
│  ┌─────────────────────────────────────────────┐    │
│  │  Machine Learning (ML)                       │    │
│  │  Systems that learn patterns from data        │    │
│  │  instead of following programmed rules        │    │
│  │                                               │    │
│  │  ┌─────────────────────────────────────┐     │    │
│  │  │  Deep Learning                       │     │    │
│  │  │  ML using neural networks with       │     │    │
│  │  │  many layers                         │     │    │
│  │  │                                      │     │    │
│  │  │  ┌─────────────────────────────┐    │     │    │
│  │  │  │  Foundation Models          │    │     │    │
│  │  │  │  Large models trained on    │    │     │    │
│  │  │  │  massive datasets that can  │    │     │    │
│  │  │  │  be adapted to many tasks   │    │     │    │
│  │  │  │                             │    │     │    │
│  │  │  │  ┌───────────────────┐     │    │     │    │
│  │  │  │  │  LLMs / Agents    │     │    │     │    │
│  │  │  │  │  ChatGPT, Claude, │     │    │     │    │
│  │  │  │  │  Gemini, etc.     │     │    │     │    │
│  │  │  │  └───────────────────┘     │    │     │    │
│  │  │  └─────────────────────────────┘    │     │    │
│  │  └─────────────────────────────────────┘     │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

Let's trace each layer from the outside in.

## Era 1: Rule-Based AI (1950s–1980s) — "If This, Then That"

> **ANALOGY**: Imagine a restaurant where the chef has no creativity whatsoever but has a massive recipe book covering every possible order. Customer says "chicken tikka"? The chef looks up page 347 and follows the instructions exactly. Customer says "chicken tikka but make it spicy and also add paneer"? The chef freezes — that exact combination isn't in the book.

The first wave of AI was **rule-based systems** (also called **expert systems**). Humans wrote explicit rules: "IF the patient has a fever AND a cough AND has traveled recently, THEN test for malaria." These systems worked brilliantly for narrow, well-defined problems. MYCIN (1976) diagnosed blood infections better than most doctors. DENDRAL (1965) identified chemical compounds from mass spectrometry data.

But they had a fundamental limitation: **every rule had to be written by a human**. The real world is messy, ambiguous, and full of edge cases. Try writing rules for "identify a cat in a photo" — you'd need millions of rules for every possible angle, lighting condition, breed, and pose. And you'd still miss cases.

> **INTUITION**: The breaking point came when researchers tried to build systems that could understand natural language — everyday English. Consider the sentence: "Time flies like an arrow; fruit flies like a banana." A rule-based system would need separate rules for "flies" as a verb (to fly), "flies" as a noun (the insect), and "like" as a preposition vs. "like" as a verb. Human language is so rich with ambiguity that no finite set of rules could capture it. This realization — that intelligence might need to be *learned*, not *programmed* — launched the next era.

## Era 2: Machine Learning (1990s–2010s) — "Show Me, Don't Tell Me"

> **ANALOGY**: Instead of giving the chef a recipe book, you give them 10,000 examples of great biryani. They taste each one, note what the good ones have in common (spice ratios, rice texture, cooking time), and gradually develop an intuition for what makes biryani excellent. No explicit recipe needed — they've *learned* the pattern from examples.

**Machine Learning (ML)** flipped the approach entirely. Instead of programming rules, you show the system thousands (or millions) of examples and let it discover the patterns itself.

The process:

1. **Training data**: Thousands of labeled examples. "This email is spam. This one isn't. This one is. This one isn't."
2. **Model**: A mathematical function that takes an input (email text) and produces an output (spam or not spam)
3. **Training**: The model makes predictions. When it's wrong, it adjusts its internal numbers to be slightly less wrong. Repeat millions of times
4. **Result**: A model that can classify new emails it's never seen before

> **REAL-LIFE**: Every time Netflix recommends a show you end up loving, that's machine learning. Netflix has collected billions of data points — what you watched, when you paused, what you rewatched, what you quit after 5 minutes. From all those examples, its ML models learned patterns: "People who watched *Money Heist* and *Narcos* tend to enjoy *Gangs of London*." No human programmed that rule. The system discovered it from data.

The key types of ML:

- **Supervised learning**: You give the model labeled examples. "This image is a cat. This image is a dog." After seeing enough examples, it can classify new images. Used in: spam filters, medical diagnosis, fraud detection
- **Unsupervised learning**: You give the model unlabeled data and say "find patterns." Used in: customer segmentation (Spotify grouping users by listening habits), anomaly detection (banks spotting unusual transactions)
- **Reinforcement learning**: The model learns by trial and error, receiving rewards for good actions. Used in: game-playing AI (AlphaGo), robotics, recommendation systems

ML was powerful, but it had a limitation: **feature engineering**. A human had to decide *what* to feed the model. For spam detection, a human chose features like "contains the word 'free'", "has many exclamation marks", "sent from unknown domain." The model learned which features mattered, but the features themselves were human-designed.

What if the model could discover its own features?

## Era 3: Deep Learning (2012–2020) — "Neural Networks Get Deep"

> **ANALOGY**: Imagine a factory assembly line with 100 stations. Raw material enters at station 1. Each station does one tiny transformation. By station 100, the raw material has become a finished product. No single station understands the whole product — each one handles its small piece. But together, the assembly line produces remarkable results. A **deep neural network** is this assembly line. Each "station" is a layer of mathematical operations. Raw data enters layer 1, and by layer 100, it's been transformed into a prediction.

**Neural networks** are computational systems loosely inspired by the human brain — very loosely. They consist of layers of interconnected nodes (called **neurons** or **units**) that transform inputs into outputs. "Deep" learning means many layers (tens, hundreds, or thousands).

The critical moment: **ImageNet 2012**. The ImageNet competition challenged teams to classify 1.2 million images into 1,000 categories (cat, dog, car, ship, etc.). For years, the best systems achieved about 74% accuracy using traditional ML with hand-crafted features. Then Alex Krizhevsky, Ilya Sutskever, and Geoffrey Hinton entered a deep neural network called **AlexNet** — it achieved 85% accuracy, demolishing the competition by a margin that shocked the entire field.

What made deep learning different? The model discovered its own features. Early layers learned to detect edges. Middle layers combined edges into textures and shapes. Late layers recognized complete objects. No human told it "look for edges first, then shapes." It figured this out on its own by processing millions of images.

> **REAL-LIFE**: Google Photos can find every photo of your face across thousands of images, in any lighting, any angle, whether you're wearing sunglasses or not. This is deep learning — specifically, a type of neural network called a **CNN (Convolutional Neural Network)**, which is designed to process visual information. Google's face recognition model was trained on hundreds of millions of face images. It learned features no human would have explicitly programmed — the distance between your eyes, the shape of your jawline, the way shadows fall on your specific face geometry.

The deep learning era gave us:

| Year | Breakthrough | Why it mattered |
|------|-------------|-----------------|
| 2012 | AlexNet | Deep learning beats traditional ML on vision |
| 2014 | GANs (Generative Adversarial Networks) | AI generates realistic images |
| 2015 | ResNet (152 layers) | Solved the "vanishing gradient" problem, enabling very deep networks |
| 2016 | AlphaGo beats Lee Sedol | AI masters a game with more possible positions than atoms in the universe |
| 2017 | Transformer architecture | The paper that changed everything (next chapter) |
| 2018 | BERT (Google) | Transformers applied to understanding language |
| 2018 | GPT-1 (OpenAI) | Transformers applied to generating language |

## The Training Process — How Machines Learn

Let's demystify training, because it's the foundation of everything that follows.

> **ANALOGY**: Imagine a student taking a multiple-choice exam every day, getting their score back instantly, and being allowed to retake the exam the next day. On day 1, they score 10% — basically random guessing. But they learn from each mistake: "Whenever I see a question about photosynthesis, the answer tends to involve chlorophyll." By day 100, they score 70%. By day 10,000, they score 95%. They haven't memorized the answers — they've learned the underlying patterns.

The training process has three stages (for modern AI systems like ChatGPT, Claude, and Gemini):

### Stage 1: Pre-training — "Read Everything"

The model reads a massive amount of text from the internet — books, Wikipedia, code, news articles, forum discussions. Trillions of words. The training objective is deceptively powerful: **predict the next word**.

Given: "The capital of France is ___"
Target: "Paris"

Given: "def fibonacci(n):\n    if n <= 1:\n        return ___"
Target: "n"

By predicting the next word across trillions of examples, the model absorbs grammar, facts, reasoning patterns, code syntax, and cultural knowledge. It doesn't "understand" in the human sense — it builds a sophisticated statistical model of how language works.

Pre-training costs millions of dollars in compute. GPT-4's training is estimated at over $100 million. This is why only a handful of organizations can train frontier models.

### Stage 2: Fine-tuning — "Learn to Be Helpful"

The pre-trained model is a next-word predictor, not an assistant. It might continue "How do I fix this bug?" with "he asked his colleague" (predicting the next part of a story) rather than actually helping you fix the bug.

Fine-tuning teaches the model to be a helpful assistant by training it on examples of high-quality conversations:

```
Human: How do I reverse a list in Python?
Assistant: You can reverse a list in Python using several methods:
1. list.reverse() — modifies the list in place
2. list[::-1] — creates a new reversed copy
3. reversed(list) — returns an iterator
```

Thousands of these example conversations teach the model the *format* of being helpful.

### Stage 3: RLHF — "Learn From Human Preferences"

**RLHF (Reinforcement Learning from Human Feedback)** is the secret ingredient that makes modern AI assistants feel helpful rather than mechanical.

The process: the model generates two different responses to the same question. Human raters (or increasingly, AI judges) pick which response is better. Over thousands of comparisons, the model learns to generate responses that humans prefer — more accurate, more helpful, safer, better formatted.

> **INTUITION**: RLHF is like a cooking competition. The chef (model) prepares two versions of a dish. Judges taste both and pick the better one. Over hundreds of rounds, the chef learns: "Judges prefer balanced seasoning over heavy salt. They prefer clear explanations over jargon. They prefer admitting uncertainty over bluffing." The chef's own "taste" aligns with human preferences.

Anthropic (the maker of Claude) developed **Constitutional AI (CAI)** — a variant of RLHF where the model also evaluates its own outputs against a set of principles (a "constitution"). This is how Claude learns to be helpful while avoiding harmful outputs.

## The Honest Assessment: What AI Is and Isn't

Let's be precise about what we're dealing with:

**AI is**: A system of statistical patterns learned from enormous amounts of data. When Claude writes code, it's not "understanding" your problem the way a human colleague does. It's generating the most likely sequence of tokens given your input and its training data — but it does this so well that the distinction often doesn't matter practically.

**AI is not**: Sentient, conscious, or "thinking." It has no experiences, no desires, no understanding of the physical world. When it says "I think..." this is a language pattern, not introspection. When it makes a confident mistake, it's not lying — it's generating the most probable next tokens, which happen to be wrong.

**The practical implications**:
- AI output must always be reviewed by a human for critical decisions
- AI is most valuable for well-defined tasks with clear success criteria
- AI hallucinations (confidently wrong outputs) are not bugs — they're a fundamental property of the technology. Chapter 18 covers how to measure and mitigate them
- The technology is improving rapidly. Limitations described here may not apply in two years. But the *type* of limitation — statistical pattern matching, not true understanding — is likely to persist

## From Models to Agents — Where We're Going

The history we've traced — rules → learning → deep learning → foundation models — has one more step that's unfolding right now: **agents**.

A foundation model (like Claude or GPT) is a brain. It can think about problems. But it can't *do* anything — it can't browse the web, run code, query a database, or send an email. It's a brilliant mind trapped in a room with no doors.

**Agents** add tools, memory, and autonomy. An agent can:
- Read files on your computer
- Run code and see the results
- Search the internet for information
- Make API calls to external services
- Remember what happened in previous conversations
- Chain together multiple steps to achieve a complex goal

Claude Code is an agent. It reads your codebase, writes code, runs commands, tests results, and iterates — all guided by your instructions but executing autonomously. This is the paradigm Karpathy calls "agentic engineering," and it's the subject of Chapter 15.

But first, we need to understand the engine that makes all of this possible: the transformer architecture and the large language models built on it.

<div class="exercise">
<div class="exercise-title">Try It Yourself</div>

This is a conceptual exercise, no coding required:

1. Open ChatGPT, Claude, or any AI assistant.
2. Ask it: "Explain how you were trained, as if I'm a smart 15-year-old."
3. Compare its explanation to what you read in this chapter. What did it get right? What did it oversimplify?
4. Now ask: "What are you not good at?" A well-tuned model will give you an honest answer. Notice how its self-assessment matches the limitations we described.
5. Finally, ask it to solve a riddle that requires common sense: "A man pushes his car to a hotel and realizes he's bankrupt. Why?" (Answer: he's playing Monopoly.) Did the AI get it? This tests reasoning beyond pattern matching.

</div>

---

**Chapter endnotes**

[1] Andrej Karpathy's "Intro to Large Language Models" lecture (November 2023) provides an accessible 1-hour overview of the entire field. His "Let's Build GPT from Scratch" video walks through building a transformer from first principles in Python. Both are freely available and are among the best educational resources in the field.

[2] Michael Nielsen's "Neural Networks and Deep Learning" is a free online textbook that provides mathematical intuition for neural networks without drowning in equations. For visual learners, 3Blue1Brown's (Grant Sanderson) YouTube series on neural networks is the gold standard — beautiful animations that make gradient descent and backpropagation intuitive.

[3] The "pre-training → fine-tuning → RLHF" pipeline was popularized by OpenAI's InstructGPT paper (2022) and refined by Anthropic's Constitutional AI paper (2022). For a production-oriented treatment, see Chip Huyen's "AI Engineering" (O'Reilly, 2025), Chapters 3-5.

[4] The AlexNet breakthrough at ImageNet 2012 is widely considered the moment deep learning became the dominant paradigm. Ilya Sutskever, one of AlexNet's creators, went on to co-found OpenAI. Geoffrey Hinton, the other, won the Nobel Prize in Physics in 2024 for foundational work on neural networks — the first time the Nobel committee recognized AI research.
