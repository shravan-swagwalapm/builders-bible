<span class="chapter-number">Chapter 12</span>

# Embeddings & Vector Search — How AI Finds Meaning {.chapter-title}

In the previous chapter, you learned how large language models predict the next token. That's how AI *generates* language. But there's a different, equally important question: how does AI *find* things?

When you search Google for "best restaurants near me," the search engine doesn't match your exact words to a database of pages. It understands your *intent* — you want nearby, highly-rated places to eat — and returns pages that match that meaning, even if those pages never contain the phrase "best restaurants near me."

This chapter is about the technology that makes meaning-based search possible: **embeddings**. By the end, you'll understand how text gets converted to numbers, why similar meanings produce similar numbers, how vector databases store and search millions of these number-representations, and how products you use every day — from Spotify to Flipkart — rely on this technology at their core.

## The Big Idea: Meaning as Numbers

> **ANALOGY**: Imagine you run a spice shop. You have 200 spices, and customers constantly ask "What's similar to cardamom?" You could alphabetize your spices — but "cardamom" and "cinnamon" being close alphabetically doesn't mean they taste similar. Instead, you create a rating system. Every spice gets scores on dimensions like sweetness (1-10), heat (1-10), earthiness (1-10), and floral notes (1-10). Cardamom might be [sweetness: 6, heat: 2, earthiness: 3, floral: 8]. Cinnamon might be [sweetness: 7, heat: 1, earthiness: 4, floral: 5]. Now "similarity" means something real: spices with similar scores across all dimensions taste alike. You've turned a subjective question ("what tastes like cardamom?") into a mathematical one ("which score-lists are closest to cardamom's score-list?").

That's the core of embeddings. An **embedding** is a list of numbers that represents the meaning of a piece of text, an image, a song, or any other data. The numbers aren't random — they're arranged so that *things with similar meanings get similar numbers*.

> **REAL-LIFE**: When Spotify builds your Discover Weekly playlist, it doesn't match genre labels. It converts every song into a list of roughly 100-300 numbers that capture attributes no human explicitly defined — mood, energy, rhythm complexity, vocal texture, production style. Your listening history also becomes a list of numbers. Spotify then finds songs whose number-lists are close to your number-list but that you haven't heard yet. That's embedding-powered recommendation.

> **INTUITION**: The word "embedding" comes from the mathematical idea of embedding one space into another. You're taking something that lives in the messy, unstructured world of human language and *embedding* it into a clean, structured world of numbers where distance and direction have meaning. It's a translation from a world where computers struggle (language) into a world where they excel (math).

The **actual mechanism**: an embedding model is a neural network (typically a transformer, like the ones you learned about in Chapter 10) that has been trained on massive datasets to produce these number-lists. You feed it a sentence like "The restaurant had excellent biryani," and it outputs a list of, say, 1,536 numbers. Feed it "The food at the place was amazing biryani," and you get a *different* list of 1,536 numbers — but one that's very close to the first, because the meanings are nearly identical. Feed it "The stock market crashed on Tuesday," and you get a list of 1,536 numbers that's far away from both.

These lists of numbers are called **vectors** — a term from mathematics that means an ordered list of numbers. A vector with 1,536 numbers lives in "1,536-dimensional space." You can't visualize 1,536 dimensions, but the math works the same way as 2D or 3D space: things that are close in this high-dimensional space are similar in meaning.

## Seeing the Invisible: A Map of Meaning

To understand embeddings visually, let's crush those 1,536 dimensions down to two. This is what researchers do to inspect embeddings — they use techniques called **dimensionality reduction** (specifically t-SNE or UMAP) to flatten high-dimensional space into a 2D plot you can look at. The relationships aren't perfect in 2D, but the clusters and neighborhoods are preserved.

```
    A 2D EMBEDDING SPACE (simplified)
    ──────────────────────────────────────────────────────

              royalty                     food
              ·······                  ···········
         crown ·      · throne    pizza ·    · pasta
               · king ·                 ·  burger ·
         queen ·      · emperor   sushi ·    · ramen
               ········                 ···········
                                   banana ·
                                          · apple
                                    mango ·    · grape
                                          ··········
                                           fruit

    ──── (far away) ───────────────────────────────────

         python ·        · javascript
                · rust ·
           java ·        · typescript
                ··········
             programming
               languages

    ──────────────────────────────────────────────────────
    KEY:
    · = a word's position in embedding space
    Words CLOSE together = similar meaning
    Words FAR apart = unrelated meaning
    "king" is near "queen" (both royalty)
    "king" is far from "banana" (unrelated)
    "python" (the language) clusters with code, not snakes
```

Notice what happens in this map:
- **"King" and "queen"** are almost touching. They share the same neighborhood — royalty, power, monarchy.
- **"King" and "banana"** are on opposite ends. They have nothing in common.
- **"Pizza" and "burger"** are close — both fast food. "Sushi" and "ramen" are close — both Japanese cuisine. And all of them cluster in the "food" region.
- **"Python" the programming language** clusters with JavaScript and Rust, not with "snake." The embedding model learned from context that when people write about Python alongside "function," "variable," and "deploy," they mean the language. This is something a keyword search could never resolve.

## The Equation That Stunned the World

In 2013, Tomas Mikolov and his team at Google published a paper introducing **Word2Vec** — one of the first widely successful embedding models. Their most famous finding was an equation that made researchers do a double-take:

**king − man + woman ≈ queen**

What does this mean? The embedding for "king" minus the embedding for "man" plus the embedding for "woman" produces a vector that's closest to... "queen."

Break that down:
- Take the concept of "king" (a male monarch)
- Subtract the concept of "man" (maleness)
- Add the concept of "woman" (femaleness)
- You get: a female monarch. That's a queen.

> **ANALOGY**: Imagine a city map where every building has GPS coordinates. The vector from your house to the nearest coffee shop represents the direction and distance of "going to get coffee." If you apply that same vector from your friend's house — same direction, same distance — you'd expect to land near *their* nearest coffee shop. The embedding space works the same way: the "direction" from man to woman, when applied to king, lands you at queen. The direction *encodes a relationship*.

This wasn't programmed. Nobody told Word2Vec that kings and queens are gendered equivalents. The model discovered this structure by reading billions of words and noticing patterns in how these words appeared in context. Other relationships emerged too:

- Paris − France + Italy ≈ Rome (capitals)
- Walking − walked + swam ≈ swimming (tense)
- Big − bigger + smaller ≈ small (degree)

> **INTUITION**: This is why embeddings feel almost magical. They don't store definitions or rules. They capture *relationships* — the directional patterns between concepts. The space itself encodes human knowledge in a form that's both mathematically precise and semantically rich. As Vicki Boykis writes in her technical report "What Are Embeddings?", embeddings are "the fundamental unit of machine learning" — the lingua franca through which every modern AI system represents and reasons about the world.

## Why This Matters: Keywords vs. Meaning

Traditional search — the kind that powered Google in 2005, that powers most database queries, that runs every CTRL+F on your computer — works by **exact matching**. You type a word, the system finds that word.

This creates a gap between what you *mean* and what the system *finds*:

| What you search | What you mean | What keyword search finds | What vector search finds |
|---|---|---|---|
| "headache remedy" | Ways to treat a headache | Pages containing "headache" AND "remedy" | Pages about migraine relief, tension relief, pain management, aspirin, ibuprofen |
| "affordable laptop for college" | Budget-friendly student computers | Pages with all three keywords | Reviews of budget Chromebooks, student laptop comparisons, back-to-school deals |
| "my app keeps crashing" | How to fix app stability issues | Pages with "app" and "crashing" | Stack Overflow threads about memory leaks, error handling, debugging crashes |
| "feeling blue" | Being sad | Pages literally about the color blue | Articles about depression, mood, sadness |

Vector search closes this gap because it operates on *meaning*, not *spelling*. Two sentences that share zero words in common can be recognized as near-identical in meaning:

- "The cat sat on the mat" and "A feline rested on the rug" — zero words in common, but their embeddings are very close
- "Bank" (financial institution) and "bank" (river edge) — identical spelling, but their embeddings are far apart because the model disambiguates by context

> **REAL-LIFE**: This is how Flipkart's FK-CLIP visual search works. A customer photographs a dress they saw someone wearing on the street. FK-CLIP converts the photo into an embedding (a list of numbers representing the dress's visual features — color, pattern, silhouette, fabric texture). It then searches Flipkart's catalog of millions of products, each pre-converted into their own embeddings, to find the visually closest matches. The customer never typed a single keyword. The search happened entirely in embedding space — image-to-image, meaning-to-meaning.

## Embedding Models: The Translators

An embedding model's job is narrow but critical: take text in, put numbers out. Unlike LLMs that generate language, embedding models produce only vectors. They're smaller, faster, and cheaper to run.

Here are the major embedding models available in 2026:

| Model | Provider | Dimensions | Max Tokens | Best For | Cost (per 1M tokens) |
|---|---|---|---|---|---|
| text-embedding-3-large | OpenAI | 3,072 | 8,191 | General purpose, highest quality from OpenAI | $0.13 |
| text-embedding-3-small | OpenAI | 1,536 | 8,191 | Cost-efficient, strong quality | $0.02 |
| voyage-3-large | Voyage AI | 1,024 | 32,000 | Code retrieval, long documents | $0.18 |
| embed-v4.0 | Cohere | 1,024 | 512 | Multilingual, 100+ languages | $0.10 |
| BGE-large-en-v1.5 | BAAI (open source) | 1,024 | 512 | Free, self-hosted, English | Free |
| E5-mistral-7b | Microsoft (open source) | 4,096 | 32,768 | Free, self-hosted, long context | Free |
| Gemini embedding | Google | 768 | 2,048 | Tight integration with Google Cloud | $0.004 |

The key tradeoffs:

1. **Dimensions**: More dimensions means the embedding can capture finer distinctions. A 3,072-dimension embedding can distinguish between "machine learning engineer" and "machine learning researcher" more precisely than a 768-dimension one. But more dimensions means more storage and slower search.

2. **Max tokens**: How much text the model can embed at once. Models with 512-token limits force you to chunk long documents into small pieces before embedding. Models with 32,000-token limits can embed entire articles as a single vector.

3. **Cost vs. self-hosting**: API-based models (OpenAI, Voyage, Cohere) charge per token and require internet access. Open-source models (BGE, E5) are free but require your own hardware — a GPU with 8-16GB VRAM for the larger models.

> **INTUITION**: Choosing an embedding model is like choosing a translator for a United Nations session. Some translators (OpenAI, Voyage) are expensive but fast and accurate. Others (BGE, E5) work for free but you need to provide the booth and equipment yourself. Some specialize in legal language (Voyage for code), others in multilingual diplomacy (Cohere for 100+ languages). The "best" translator depends on what you're translating, how much you're translating, and your budget.

## Vector Databases: Where Embeddings Live

Once you've converted your data into embeddings, you need somewhere to store and search them. A traditional database like PostgreSQL stores rows of structured data and searches using SQL queries. A **vector database** stores embeddings and searches by similarity — "find me the 10 vectors closest to this query vector."

```
    HOW VECTOR SEARCH WORKS
    ═══════════════════════════════════════════════════════

    STEP 1: Indexing (done once, ahead of time)
    ──────────────────────────────────────
    "How to train a puppy"       → [0.12, 0.85, 0.33, ...]  ─┐
    "Best dog training methods"  → [0.14, 0.82, 0.31, ...]   │
    "Python training tutorial"   → [0.91, 0.04, 0.72, ...]   ├─► Vector DB
    "Cat care for beginners"     → [0.22, 0.71, 0.28, ...]   │
    "Puppy obedience classes"    → [0.11, 0.88, 0.35, ...]  ─┘

    STEP 2: Query (happens at search time)
    ──────────────────────────────────────
    User asks: "teach my new dog to behave"
                        ↓
              Embed the query
                        ↓
              [0.13, 0.84, 0.32, ...]
                        ↓
              Find nearest vectors
                        ↓
    RESULTS (ranked by closeness):
      1. "How to train a puppy"        (distance: 0.03)  ✓
      2. "Puppy obedience classes"     (distance: 0.05)  ✓
      3. "Best dog training methods"   (distance: 0.06)  ✓
      4. "Cat care for beginners"      (distance: 0.41)
      5. "Python training tutorial"    (distance: 0.89)  ✗

    ═══════════════════════════════════════════════════════
    NOTE: "Python training" is FAR from "dog training"
    because the *meaning* is different, despite sharing
    the word "training." This is the power of vectors.
```

The major vector databases in 2026:

| Database | Type | Best For | Scale | Notable Users |
|---|---|---|---|---|
| FAISS | Library (Meta) | In-memory search, research, single-machine apps | Millions of vectors | Meta, PrabhupadaAI |
| Pinecone | Managed cloud | Production apps, zero DevOps | Billions of vectors | Notion, Gong |
| Weaviate | Open source / cloud | Hybrid search (vectors + keywords) | Billions of vectors | Stackla, Instabase |
| Chroma | Open source | Prototyping, lightweight local apps | Thousands to millions | Popular in AI tutorials |
| Qdrant | Open source / cloud | High performance, filtering | Billions of vectors | Many European startups |
| pgvector | PostgreSQL extension | Adding vector search to existing Postgres | Millions of vectors | Supabase users |

The key decision: **library vs. managed vs. self-hosted**.

**FAISS** (Facebook AI Similarity Search) is a library, not a database. You import it into your Python code and it runs in your process's memory. It's blindingly fast — Meta built it for searching billions of vectors internally — but you manage everything yourself: loading data, saving indexes, handling restarts. Think of it as a powerful engine with no car around it.

**Pinecone** is a fully managed service. You send vectors through an API, Pinecone stores them, indexes them, and returns search results. You never think about infrastructure. It's the "Stripe of vector databases" — you pay for convenience. Great for production, expensive at scale.

**Chroma** and **Qdrant** are open-source options that you can run locally for free or deploy to your own servers. They offer a balance between FAISS's raw power and Pinecone's convenience.

**pgvector** is the pragmatist's choice: if you already use PostgreSQL (and in 2026, most web applications do), you can add vector search capabilities to your existing database without introducing a new system. The performance isn't as good as dedicated vector databases, but "good enough in the same database you already manage" beats "perfect in a new system you have to learn and maintain" for many teams.

## Cosine Similarity: How Closeness Gets Measured

When a vector database says "these two embeddings are similar," how does it decide? The most common method is **cosine similarity** — and you can understand it without any math.

> **ANALOGY**: Imagine two arrows pinned to the same point, like clock hands. If both arrows point in the same direction (both at 12 o'clock), they're perfectly aligned — cosine similarity is 1.0, meaning maximum similarity. If they point in opposite directions (one at 12, one at 6), cosine similarity is -1.0, meaning maximum dissimilarity. If they're perpendicular (one at 12, one at 3), cosine similarity is 0.0, meaning they're unrelated.

> **REAL-LIFE**: When you paste a sentence into a "semantic search" tool and it returns related documents, the system has: (1) embedded your sentence into a vector (an arrow in high-dimensional space), (2) compared your arrow's direction to the direction of every document's arrow, and (3) returned the documents whose arrows point most similarly to yours. The *length* of the arrow doesn't matter — only the *direction*. A 10-page document and a 2-sentence summary on the same topic will point in the same direction, even though the document's arrow might be "longer" (more content).

> **INTUITION**: Why direction and not distance? Because embeddings encode *what something is about*, not *how much of it there is*. A 500-word essay about machine learning and a 5,000-word textbook chapter about machine learning should be recognized as similar. Cosine similarity ignores magnitude (length) and focuses on angle (direction) — making it robust to differences in document length. This is why it's the default similarity metric for text embeddings in production systems.

Other similarity metrics exist — **Euclidean distance** (straight-line distance between two points), **dot product** (a faster calculation that works well when vectors are normalized) — but cosine similarity is the industry standard for text embeddings. Jay Alammar's "Illustrated Word2Vec" walkthrough provides an excellent visual guide to how these distance calculations work in practice.

## Embeddings in the Wild: Real Products, Real Scale

Embeddings power features you use daily, often without realizing it.

### Spotify Discover Weekly

Spotify's recommendation engine represents every song, podcast, and user as an embedding. But it goes beyond audio features. Spotify combines multiple signals:

1. **Audio embeddings**: Raw audio converted to vectors capturing tempo, key, timbre, energy
2. **Collaborative filtering embeddings**: Patterns from what 600+ million users listen to. If Users A, B, and C all love songs X, Y, and Z, and User D loves X and Y, then Z gets recommended to User D
3. **Natural language embeddings**: Spotify crawls blogs, reviews, and social media for text about songs and converts those descriptions into embeddings. A song described as "perfect for late-night drives" gets an embedding that's close to other "nighttime mood" songs

The result: 30 fresh songs every Monday, tailored to your taste, for each of Spotify's 600+ million users. That's billions of embedding comparisons happening weekly.

### Flipkart's FK-CLIP

Flipkart, India's largest e-commerce platform, built FK-CLIP — a multimodal embedding system that places images and text in the *same* embedding space. Upload a photo of a red kurta, and FK-CLIP produces a vector. That vector lives in the same space as the text description "red embroidered kurta for women." Photo-to-text, text-to-photo, photo-to-photo — all possible because images and text share one unified embedding space.

This powers visual search (photograph something, find it on Flipkart), style recommendations (find products that "look like" products you've browsed), and catalog deduplication (identify when two sellers have listed the same product with different photos).

### PrabhupadaAI: Production Numbers

PrabhupadaAI — a project covered later in this book — provides AI-powered answers grounded in the teachings of A.C. Bhaktivedanta Swami Prabhupada. The system embeds 161,724 passages from books, lectures, and conversations into FAISS vectors. When a user asks a question, the system:

1. Embeds the question into a vector (takes ~0.05 seconds)
2. Searches 161,724 FAISS vectors for the most similar passages (takes ~0.19 seconds)
3. Feeds the top passages to an LLM to generate a grounded answer

Total retrieval latency: **0.24 seconds** to search through 161,724 vectors and return the most relevant passages. This is not a toy demo. This is a production system serving real users, running on a single Railway instance with no GPU — FAISS runs on CPU for datasets of this size. The entire FAISS index fits in about 950MB of RAM.

These numbers matter because they show what's achievable without a massive budget. You don't need Pinecone's billion-vector infrastructure for most applications. A well-configured FAISS index on modest hardware handles hundreds of thousands of vectors with sub-second latency.

## How Embedding Models Are Trained

Understanding how embedding models learn produces better intuition for when they'll succeed and when they'll fail.

> **ANALOGY**: Imagine a teacher training students using flashcards. The teacher shows a card with a sentence and asks: "Is this next sentence a genuine continuation, or did I make it up?" Sentence: "The patient reported chest pain." Next: "An ECG was ordered immediately" (genuine) vs. "The cafeteria served pasta today" (fake). Over millions of flashcards, the student learns what "related" means — not by memorizing pairs, but by developing a deep sense of conceptual proximity.

Modern embedding models use a training technique called **contrastive learning**. The model sees:
- **Positive pairs**: Two texts that should be similar (a question and its answer, a title and its abstract, a search query and a relevant document)
- **Negative pairs**: Two texts that should be different (a question and an unrelated passage)

The training objective: make positive pairs' embeddings close and negative pairs' embeddings far apart. After processing billions of pairs, the model develops a nuanced sense of semantic similarity.

This training approach explains several important behaviors:

1. **Domain sensitivity**: An embedding model trained mostly on web text will struggle with medical or legal jargon. The texts it saw during training shape its notion of "similarity." This is why Voyage AI offers specialized models for code — their code model was trained on code-specific positive and negative pairs.

2. **Recency**: Embedding models have training cutoffs. A model trained in 2023 won't know about events or terminology from 2025. It might embed "RAG" as "rag" (a cloth) rather than "Retrieval Augmented Generation" if its training data predates the term's popularity.

3. **Language bias**: Most embedding models work best in English because their training data skews English. Cohere's multilingual models address this by training on parallel text across 100+ languages — the same sentence in Hindi and English produces similar embeddings.

## The Chunking Problem: How to Prepare Text for Embedding

In practice, you rarely embed a single sentence. You embed documents — articles, PDF pages, support tickets, product descriptions. But embedding models have token limits (512 to 32,000 tokens depending on the model). Long documents must be split into **chunks**.

Chunking strategy matters more than most teams realize:

- **Too large** (entire document as one vector): The embedding becomes a vague average of everything in the document. Searching for a specific detail returns the whole document with a mediocre similarity score.
- **Too small** (individual sentences): Each embedding lacks context. The sentence "It exceeded expectations" scores high for any positive query, but you've lost what "it" refers to.
- **The sweet spot**: 200-500 tokens per chunk, with 50-100 tokens of overlap between consecutive chunks. The overlap ensures that ideas spanning a chunk boundary aren't lost.

> **REAL-LIFE**: In PrabhupadaAI, the 161,724 vectors come from passages chunked at approximately 300 tokens with 50-token overlaps. Each chunk also stores metadata — which book it's from, which chapter, the page number — so the LLM can cite its sources. The chunking strategy was iterated three times before settling on this configuration, because the first two attempts produced either too-vague or too-fragmentary retrievals. Chunking is an engineering decision with outsized impact on retrieval quality.

Lilian Weng's blog at lilianweng.github.io provides a thorough technical survey of chunking strategies, overlap techniques, and their measured impact on retrieval accuracy for readers who want to go deeper.

## The RAG Connection

Embeddings are the foundation of **RAG (Retrieval Augmented Generation)** — the technique covered in depth in the next chapter. RAG solves a fundamental LLM limitation: models have training cutoffs and can't access your private data.

The RAG pipeline:
1. **Embed** your documents and store vectors in a vector database
2. **Embed** the user's question
3. **Search** the vector database for the most relevant document chunks
4. **Feed** those chunks to an LLM alongside the question
5. The LLM **generates** an answer grounded in your actual data

Without embeddings, RAG doesn't exist. Without RAG, LLMs can only answer from their training data. This is why embeddings are a foundational technology, not a niche one — they're the bridge between "AI that knows what the internet knows" and "AI that knows what *your company* knows."

## Common Pitfalls

Builders encounter recurring issues when working with embeddings in production:

**1. Mixing embedding models.** Vectors from OpenAI's model and vectors from Cohere's model exist in completely different spaces. You cannot search a Cohere-embedded database with an OpenAI-embedded query. Choose one embedding model for your entire system. If you switch models, you must re-embed everything.

**2. Ignoring the garbage-in problem.** Embedding models faithfully represent whatever you give them — including messy, unstructured, or irrelevant text. HTML tags, navigation menus, cookie consent banners, and boilerplate disclaimers all become part of the embedding. Clean your text before embedding it.

**3. Over-relying on vector search alone.** Vector search is powerful for semantic similarity but weak for exact matching. If a user searches for "error code E-4072," vector search might return results about error handling in general rather than the specific code. The solution: **hybrid search** — combine vector search (for meaning) with keyword search (for exact matches). Weaviate and other databases support this natively.

**4. Neglecting evaluation.** How do you know if your embeddings are working well? Most teams deploy vector search and never measure its accuracy. Build a test set: 50-100 questions with known correct answers. Measure how often the correct document appears in the top 3, top 5, and top 10 results. This metric — called **recall@k** — is your ground truth for embedding quality.

**5. Not updating embeddings.** If your source documents change, your embeddings become stale. A product description updated last week should have a fresh embedding. Build a pipeline that re-embeds changed documents automatically.

<div class="exercise">
<div class="exercise-title">Exercise: Embed Sentences and Find Similar Pairs with Claude Code</div>

Open your terminal and navigate to your exercises folder:

```
cd ~/Desktop/builders-bible-exercises
```

Ask Claude Code:

> "Create a Python script called embedding_explorer.py that does the following:
> 1. Define these 10 sentences as a list:
>    - 'The cat sat on the warm windowsill'
>    - 'A kitten rested by the sunny window'
>    - 'The stock market crashed on Tuesday'
>    - 'Financial markets experienced a sharp decline'
>    - 'She enjoyed a delicious plate of biryani'
>    - 'The spicy rice dish was her favorite meal'
>    - 'Python is a popular programming language'
>    - 'Many developers prefer coding in Python'
>    - 'The sunset painted the sky orange and pink'
>    - 'It rained heavily throughout the entire night'
> 2. Use the `sentence-transformers` library with the 'all-MiniLM-L6-v2' model (free, runs locally, no API key needed) to embed all 10 sentences
> 3. Compute cosine similarity between every pair
> 4. Print the top 5 most similar pairs and the top 5 least similar pairs
> 5. Add comments explaining what's happening at each step"

Install the dependency first: `pip install sentence-transformers`

**What to notice:**
- The cat/kitten sentences will have high similarity (~0.8+) despite different words
- The cat sentences and stock market sentences will have low similarity (~0.1 or lower)
- "Python is a popular programming language" and "Many developers prefer coding in Python" will be highly similar
- The sunset sentence and the rain sentence — both about weather/sky — might be moderately similar, more than you'd expect

**Stretch goal:** Add an 11th sentence — "The python slithered through the grass" — and observe where it falls. Is it closer to the cat sentences (animals) or the programming sentences (Python)? The answer reveals how well the embedding model disambiguates context.

</div>

---

**Chapter endnotes**

[1] Tomas Mikolov et al., "Efficient Estimation of Word Representations in Vector Space" (2013), introduced Word2Vec and the famous king − man + woman ≈ queen analogy. This paper, along with Mikolov's follow-up "Distributed Representations of Words and Phrases and their Compositionality" (2013), demonstrated that word embeddings could capture linguistic regularities as linear relationships in vector space — a finding that reshaped the entire field of NLP.

[2] Vicki Boykis, "What Are Embeddings?" (2023), is a 77-page technical report that provides the most comprehensive and accessible explanation of embeddings available. Boykis traces the concept from one-hot encoding through Word2Vec to modern transformer-based embeddings, with clear diagrams and practical code examples. Essential reading for anyone working with embeddings in production.

[3] Jay Alammar, "The Illustrated Word2Vec" (2019), provides step-by-step visual explanations of how word embeddings are trained and why vector arithmetic works. His diagram showing how the "royal" direction in embedding space connects king to queen remains one of the best visual explanations of the concept.

[4] Lilian Weng, "Generalized Language Models" and her embedding-focused survey posts at lilianweng.github.io provide rigorous technical treatment of embedding architectures, training objectives (contrastive learning, masked language modeling), and evaluation benchmarks. For readers who want the mathematical foundations without losing accessibility, Weng's writing is the gold standard.

[5] FAISS (Facebook AI Similarity Search) was open-sourced by Meta in 2017. The library supports multiple index types — flat (exact search), IVF (approximate search with clustering), and HNSW (graph-based approximate search) — each trading accuracy for speed. The PrabhupadaAI production numbers cited in this chapter use an IVFFlat index with 256 clusters.

[6] FK-CLIP is Flipkart's adaptation of OpenAI's CLIP (Contrastive Language-Image Pre-training) model, fine-tuned on Flipkart's catalog of Indian e-commerce products. CLIP's key innovation is training image and text encoders jointly so that images and their descriptions produce similar embeddings — enabling cross-modal search.

[7] The embedding model comparison table reflects pricing and specifications as of March 2026. OpenAI and Cohere update their models and pricing periodically. The open-source models (BGE, E5) are available on Hugging Face and can be run locally without cost — the "Free" pricing reflects zero per-token charges, not zero infrastructure cost.
