<span class="chapter-number">Chapter 13</span>

# RAG — Teaching AI What It Doesn't Know {.chapter-title}

Here's a scenario that plays out thousands of times a day at every company using AI.

A product manager opens ChatGPT and types: "What is our refund policy for enterprise customers?" ChatGPT responds with a confident, well-structured, completely wrong answer. It invents a refund policy that sounds plausible — 30-day money-back guarantee, prorated refunds for annual contracts — but none of it matches the actual policy buried in a Google Doc that was last updated six months ago.

The model isn't broken. It's doing exactly what it was trained to do: predict the most likely next words based on everything it read during training. The problem is that "everything it read during training" doesn't include your company's internal documents, your product specs, your customer conversations, your knowledge base articles, or anything written after its training cutoff date.

This is the foundational problem that RAG solves.

## The Knowledge Gap

Large language models know an extraordinary amount about the world. They've read Wikipedia, textbooks, code repositories, news archives, and billions of web pages. Ask Claude about the French Revolution, Python decorators, or the chemical structure of caffeine, and you'll get accurate, detailed answers.

But ask it about:

- Your company's Q4 pricing changes
- The internal engineering RFC from last Tuesday
- A customer support ticket from this morning
- Your organization's specific security compliance requirements
- A research paper published after the model's training cutoff

And the model will either admit it doesn't know (the good outcome) or hallucinate an answer that sounds correct but isn't (the dangerous outcome).

> **ANALOGY**: Think about a brilliant new hire on their first day. They graduated top of their class. They know the theory, the frameworks, the industry trends. But they don't know where the bathroom is, what your company's OKRs are, who approves budget requests, or why the team switched from Jira to Linear last quarter. They have general intelligence but lack specific, institutional knowledge. RAG is the onboarding program that gives this brilliant new hire access to the company's knowledge base — while they're answering questions.

> **REAL-LIFE**: When Notion launched Notion AI in 2023, users immediately wanted it to answer questions about *their* notes, not generic knowledge. "Summarize my meeting notes from last week." "What did the design team decide about the homepage redesign?" Without access to the user's actual Notion workspace, the AI was a parlor trick — impressive but useless for real work. Notion built a RAG system that retrieves relevant pages from the user's workspace and feeds them to the LLM alongside the question. The AI went from "generically smart" to "specifically helpful."

## RAG: The Open-Book Exam

**RAG** stands for **Retrieval-Augmented Generation**. The name tells you everything:

- **Retrieval**: Find relevant information from an external knowledge source
- **Augmented**: Add that information to the model's context
- **Generation**: Let the model generate an answer using both its training knowledge and the retrieved information

> **ANALOGY**: You've taken two kinds of exams in your life. In a **closed-book exam**, you rely entirely on what you've memorized. You either know the answer or you don't. In an **open-book exam**, you can flip through your notes, textbooks, and reference materials to find the relevant information before writing your answer. You still need intelligence to interpret the material and construct a good answer — but you're not limited to what's in your head. RAG turns every LLM interaction into an open-book exam. The model still needs its training (intelligence, reasoning, language ability) but it can now look up specific facts before answering.

The term was coined by Patrick Lewis and colleagues at Meta AI in a 2020 paper, but the core idea — "give the model relevant documents before asking it to answer" — is older than the name. What made RAG powerful was the combination of modern retrieval techniques (semantic search using embeddings) with modern generation capabilities (large language models). Neither component alone is sufficient. Search without generation gives you a list of documents. Generation without retrieval gives you hallucinations. Together, they give you grounded, accurate, specific answers.

> **INTUITION**: Why not fine-tune the model on your data instead? Fine-tuning — retraining the model on your specific documents — is like sending the new hire to a week-long training camp about your company before they start. They'll internalize some knowledge, but they can't memorize everything, and anything that changes after training camp is invisible to them. RAG is like giving them a searchable company wiki they can check in real time. Fine-tuning changes the model's *weights* (permanent memory). RAG changes the model's *context* (working memory). For most applications, RAG is cheaper, faster to implement, easier to update, and more auditable — you can see exactly which documents the model used.

## The RAG Pipeline: Five Steps from Question to Answer

Every RAG system follows the same fundamental pipeline. The specifics vary — the chunking strategy, the embedding model, the vector store, the retrieval algorithm — but the architecture is universal.

```
THE RAG PIPELINE
═══════════════════════════════════════════════════════════════════

 YOUR DOCUMENTS                        USER'S QUESTION
 (PDFs, docs, wikis,                   "What's our refund
  Slack messages, etc.)                 policy for enterprise?"
        │                                       │
        ▼                                       │
 ┌──────────────┐                               │
 │  1. CHUNK    │  Split documents into          │
 │              │  digestible pieces              │
 └──────┬───────┘                               │
        │                                       │
        ▼                                       ▼
 ┌──────────────┐                      ┌──────────────┐
 │  2. EMBED    │  Convert chunks      │  2. EMBED    │  Convert question
 │              │  into vectors        │              │  into a vector
 └──────┬───────┘                      └──────┬───────┘
        │                                     │
        ▼                                     │
 ┌──────────────┐                             │
 │  3. STORE    │  Save vectors in             │
 │              │  a vector database            │
 └──────┬───────┘                             │
        │                                     │
        │◄────────────────────────────────────┘
        │         similarity search
        ▼
 ┌──────────────┐
 │  4. RETRIEVE │  Find the most relevant
 │              │  chunks to the question
 └──────┬───────┘
        │
        ▼
 ┌──────────────────────────────────────────┐
 │  5. GENERATE                             │
 │                                          │
 │  Prompt to LLM:                          │
 │  "Given this context: [retrieved chunks] │
 │   Answer this question: [user query]     │
 │   Only use information from the context" │
 └──────────────┬───────────────────────────┘
                │
                ▼
         ┌─────────────┐
         │   ANSWER     │
         │  "Our refund │
         │   policy for │
         │   enterprise │
         │   is..."     │
         └─────────────┘

 ◄─── INDEXING (done once) ───►◄─── QUERYING (every request) ──►
```

Let's walk through each step in detail.

### Step 1: Chunking — Breaking Documents into Pieces

An LLM's context window is finite. You can't feed it your entire knowledge base at once. Even if you could, you wouldn't want to — drowning the model in irrelevant information hurts answer quality. So the first step is to break your documents into **chunks**: smaller passages of text that each contain a coherent piece of information.

> **ANALOGY**: Imagine you're organizing a library. You wouldn't file entire books under a single subject heading — a 400-page book on marketing covers dozens of topics. Instead, you'd want each chapter, or even each section, to be individually findable. "Chapter 7: Email Marketing Metrics" should be retrievable when someone asks about open rates, even if the rest of the book is about social media. Chunking is this process of breaking books into individually retrievable sections.

**Chunk size matters — a lot.**

**Too big** (entire documents or long chapters): The retrieved chunk contains the answer buried inside paragraphs of irrelevant text. The model has to sift through noise, which dilutes accuracy and wastes tokens (which costs money).

**Too small** (individual sentences): Each chunk lacks context. The sentence "The rate is 15%" is meaningless without knowing *what* rate and *for whom*. The model gets puzzle pieces without the picture on the box.

The sweet spot for most applications is **200-600 tokens per chunk** (roughly 150-450 words), but this varies by use case. Legal documents with dense, self-contained clauses might work at 200 tokens. Technical documentation with interconnected concepts might need 600.

**Chunking strategies:**

**Fixed-size chunking**: Split text every N tokens. Fast, but often cuts mid-sentence or mid-paragraph, breaking semantic coherence. The chunk ends with "The enterprise refund policy applies to all customers who—" and the next chunk starts "—purchased annual plans after January 2024." Neither chunk alone makes sense.

**Recursive splitting**: Start with the largest natural boundaries (section headings, double newlines), then split further at paragraph breaks, then sentence breaks, only using hard character limits as a last resort. This preserves the document's natural structure. Most production systems use this approach.

**Overlap**: Include 10-20% overlap between consecutive chunks. If Chunk 1 ends with sentences A-B-C and Chunk 2 starts with B-C-D, the overlapping sentences B and C appear in both. This prevents information loss at chunk boundaries — if the answer spans a boundary, at least one chunk will contain the complete information.

**Semantic chunking**: Use an embedding model to detect where the *meaning* shifts within a document. When consecutive sentences have high embedding similarity, they belong in the same chunk. When similarity drops sharply, that's a natural split point. More expensive to compute but produces chunks that are semantically coherent.

> **REAL-LIFE**: When we built PrabhupadaAI — a conversational AI trained on Srila Prabhupada's teachings — we processed 157,000 chunks from books, lectures, and conversations spanning decades. The chunking strategy was critical: Prabhupada's lecture transcripts wander through multiple topics in a single talk, so we couldn't use fixed-size splitting. We used recursive splitting that respected paragraph boundaries, with 15% overlap, targeting 400 tokens per chunk. Too-small chunks lost the philosophical context that makes each point meaningful. Too-large chunks mixed unrelated topics and confused retrieval.

### Step 2: Embedding — Converting Text to Vectors

Each chunk needs to be converted into a mathematical representation that captures its meaning. This is **embedding** — the process covered in depth in Chapter 12.

The key insight: an embedding model converts a chunk of text into a vector (a list of numbers, typically 768 to 3,072 dimensions). Chunks with similar meanings end up as vectors that are close together in this high-dimensional space. "Our enterprise refund policy allows full refunds within 90 days" and "What is the refund window for enterprise plans?" produce vectors that are nearby, even though they share few exact words.

The same embedding model converts both chunks (during indexing) and queries (during search) into vectors. This is what makes retrieval work — you're finding chunks whose vector representations are closest to the query's vector representation.

**Popular embedding models (March 2026):**

| Model | Dimensions | Best For | Provider |
|-------|-----------|----------|----------|
| text-embedding-3-large | 3,072 | High-accuracy retrieval | OpenAI |
| text-embedding-3-small | 1,536 | Cost-efficient retrieval | OpenAI |
| voyage-3 | 1,024 | Code and technical docs | Voyage AI |
| Cohere embed-v4 | 1,024 | Multilingual search | Cohere |
| BGE-M3 | 1,024 | Open-source, multilingual | BAAI |

The choice of embedding model affects retrieval quality more than most people expect. A poor embedding model will put "bank" (financial institution) and "bank" (river bank) close together. A good one will disambiguate based on surrounding context.

### Step 3: Storing — The Vector Database

You now have thousands (or millions) of vectors. You need somewhere to store them and — critically — search through them fast. This is the job of a **vector database** (also called a **vector store**): a database optimized for finding the nearest neighbors to a given vector.

Traditional databases excel at exact matches: "Find all users where country = 'India'." Vector databases excel at similarity matches: "Find the 10 vectors most similar to this query vector."

> **ANALOGY**: Imagine a room full of people at a party, each wearing a name tag that describes what they know about. You walk in with a question and need to find the 5 people most relevant to your question. A traditional database would require every person to have the exact keyword you're looking for — if your question says "refund" but their tag says "money-back guarantee," they're invisible. A vector database understands that "refund" and "money-back guarantee" are close in meaning and sends you to the right people.

**Popular vector stores:**

| Tool | Type | Best For | Cost |
|------|------|----------|------|
| FAISS | Library (in-memory) | Prototyping, small datasets (<1M vectors) | Free (open source) |
| Pinecone | Managed service | Production apps, zero-ops | Pay per use |
| Weaviate | Self-hosted or cloud | Complex filtering + vector search | Free tier + paid |
| Chroma | Library | Local development, quick experiments | Free (open source) |
| pgvector | PostgreSQL extension | Teams already using Postgres | Free (open source) |

For most builders starting out, **Chroma** (for experiments) or **pgvector** (if you're already on Postgres) are the right choices. Pinecone is the right choice when you need managed infrastructure and don't want to think about scaling. FAISS is what you use when you need raw speed and are willing to manage the infrastructure yourself — it was developed by Meta's AI Research team and powers similarity search at massive scale.

### Step 4: Retrieving — Finding What Matters

When a user asks a question, the system:

1. Embeds the question into a vector (using the same embedding model from Step 2)
2. Searches the vector database for the K most similar chunk vectors (typically K = 5 to 20)
3. Returns those chunks as "context" for the generation step

This is **semantic search** — finding relevant content by meaning, not keywords. The question "How do I get my money back?" retrieves the chunk about "Refund Policy: Enterprise Tier" even though the words don't overlap at all.

The most common similarity metric is **cosine similarity** — it measures the angle between two vectors. Two vectors pointing in the same direction (cosine similarity = 1) represent the same meaning. Two vectors pointing in opposite directions (cosine similarity = -1) represent opposite meanings. Two vectors at right angles (cosine similarity = 0) are unrelated.

> **INTUITION**: Why return K results instead of the single best match? Because relevance is uncertain. The best match might be a red herring — a chunk that's semantically similar to the question but doesn't contain the answer. By returning the top 5 or 10 matches, you give the model multiple pieces of evidence to work with. If 3 out of 5 chunks agree on the refund policy, the model can be more confident. If they contradict each other, the model can flag the inconsistency. Retrieval is inherently noisy, so redundancy is valuable.

### Step 5: Generating — The Answer

The final step assembles everything into a prompt for the LLM:

```
System: You are a helpful assistant that answers questions about
our company's policies. Use ONLY the provided context to answer.
If the context doesn't contain enough information, say so.

Context:
---
[Chunk 1: Enterprise Refund Policy v3.2 — Updated Jan 2026]
Enterprise customers on annual plans are eligible for prorated
refunds within the first 90 days of their contract...
---
[Chunk 2: Refund Processing FAQ]
All refund requests must be submitted through the account
manager. Processing takes 5-10 business days...
---
[Chunk 3: Enterprise Pricing Tiers]
Enterprise plans start at $50,000/year for up to 500 seats...
---

Question: What is our refund policy for enterprise customers?
```

The model reads the retrieved chunks, synthesizes the information, and generates a grounded answer. The instruction "Use ONLY the provided context" is crucial — it tells the model to treat this as an open-book exam, not a test of its memorized knowledge.

This is where the model's reasoning ability becomes essential. The model must:
- **Identify** which chunks are relevant to the specific question
- **Synthesize** information spread across multiple chunks
- **Resolve** any contradictions between chunks (and flag them)
- **Decline** to answer if the retrieved context doesn't contain the answer
- **Cite** which chunks it used (if instructed to do so)

A common failure mode: the model ignores the retrieved context and answers from its training data instead. This happens when the prompt doesn't sufficiently emphasize the context or when the retrieved chunks are tangentially relevant but don't answer the question. The prompt engineering for RAG is a craft in itself.

## Eugene Yan's RAG Evolution Framework

Not all RAG systems are created equal. Eugene Yan, a principal engineer at Amazon who has written extensively about applied ML, proposed a framework for understanding how RAG systems evolve as teams learn what works and what doesn't. This framework has become the standard vocabulary in the field.

```
THE EVOLUTION OF RAG
═══════════════════════════════════════════════════════════════

  NAIVE RAG          ADVANCED RAG        MODULAR RAG         AGENTIC RAG
  ─────────          ────────────        ───────────         ───────────
  ┌─────────┐       ┌─────────────┐     ┌──────────────┐   ┌──────────────┐
  │ Chunk   │       │ Smart Chunk │     │ Router       │   │ Agent        │
  │ Embed   │       │ Embed       │     │   ↓          │   │   ↓          │
  │ Store   │       │ Store       │     │ Retrieve     │   │ Plan         │
  │ Retrieve│       │ Retrieve    │     │   ↓          │   │   ↓          │
  │ Generate│       │ Rerank      │     │ Rerank       │   │ Search (×N)  │
  └─────────┘       │ Generate    │     │   ↓          │   │   ↓          │
                    └─────────────┘     │ Generate     │   │ Synthesize   │
                                        │   ↓          │   │   ↓          │
                                        │ Validate     │   │ Validate     │
                                        └──────────────┘   │   ↓          │
                                                           │ Iterate?     │
                                                           └──────────────┘

  "It works!"       "It works well"     "It works for       "It works for
                                         different cases"    hard questions"
```

### Stage 1: Naive RAG — "The Prototype"

The basic pipeline described above. Chunk the documents, embed them, store them, retrieve the top K chunks, generate an answer. This is what you build first and it works surprisingly well for 60-70% of queries.

**Where it breaks:**

- **Wrong chunks retrieved**: The query "How do I reset my password?" retrieves chunks about "password policy requirements" instead of the actual reset instructions. Semantically similar, but not what the user needs.
- **No answer in top K**: The answer is in the 15th most relevant chunk, but you only retrieved 5.
- **Conflicting information**: Retrieved chunks from different document versions contradict each other, and the model doesn't know which is current.
- **Multi-hop questions**: "What was the outcome of the feature that the VP of Product proposed in Q3?" requires finding who the VP of Product is, what they proposed, and what happened — spanning multiple documents.

### Stage 2: Advanced RAG — "The Refinement"

Advanced RAG adds pre-retrieval and post-retrieval processing to improve quality:

**Pre-retrieval improvements:**
- **Query rewriting**: Transform the user's question into a better search query. "Why is the app slow?" becomes "application performance issues latency timeout errors" — expanding the semantic surface area.
- **Hypothetical Document Embedding (HyDE)**: Ask the LLM to generate a hypothetical answer, then use *that* as the search query. The reasoning: a hypothetical answer is closer in embedding space to the actual answer than the question is.
- **Query decomposition**: Break complex questions into sub-questions. "Compare our Q3 and Q4 revenue" becomes two retrieval queries: one for Q3 revenue data, one for Q4.

**Post-retrieval improvements:**
- **Reranking**: Retrieve 20 chunks, then use a specialized reranking model to score each chunk's relevance to the specific query, keeping only the top 5. (More on this below.)
- **Chunk compression**: Summarize or trim retrieved chunks to remove irrelevant sentences, keeping only the parts that matter for the query.
- **Citation tracking**: Tag each piece of information in the generated answer with its source chunk, enabling users to verify claims.

### Stage 3: Modular RAG — "The Architecture"

Modular RAG treats the pipeline not as a fixed sequence but as a set of composable modules. Different query types route through different pipelines:

- **Factual questions** ("What is the refund policy?"): Standard retrieve → generate
- **Analytical questions** ("How has churn changed over time?"): Retrieve → aggregate → chart → generate
- **Conversational questions** ("Tell me more about that"): Resolve coreferences from chat history → retrieve → generate
- **No-retrieval questions** ("What is machine learning?"): Skip retrieval entirely, answer from model knowledge

The **router** — often an LLM itself — examines each query and decides which pipeline to use. This prevents unnecessary retrieval (wasting latency and tokens on questions the model can answer directly) and enables specialized handling for different query types.

### Stage 4: Agentic RAG — "The Researcher"

> **ANALOGY**: Naive RAG is like asking a librarian to grab the five most relevant books and hand them to you. Agentic RAG is like hiring a research analyst who reads your question, formulates a research plan, searches multiple databases, reads the results, decides they need more information, searches again with refined queries, synthesizes everything into a coherent answer, and checks it for accuracy before handing it to you.

Agentic RAG gives the retrieval system **agency** — the ability to plan, execute multiple searches, reflect on results, and iterate. The system might:

1. **Plan**: "To answer this question, I need the pricing document, the contract template, and recent customer feedback"
2. **Search**: Execute three separate retrievals across different knowledge bases
3. **Evaluate**: "The pricing document is outdated — let me search for the latest version"
4. **Re-search**: Execute a refined query
5. **Synthesize**: Combine all retrieved information into a coherent answer
6. **Validate**: Check the answer against the retrieved sources for consistency

This is where RAG meets agents (Chapter 15). LlamaIndex founder Jerry Liu has been instrumental in pushing this paradigm, arguing that the future of RAG is not better retrieval algorithms but better reasoning about *when* and *how* to retrieve.

**Comparison of RAG stages:**

| Dimension | Naive RAG | Advanced RAG | Modular RAG | Agentic RAG |
|-----------|-----------|-------------|-------------|-------------|
| **Retrieval** | Single vector search | Hybrid search + reranking | Route-dependent retrieval | Multi-step, iterative retrieval |
| **Reasoning** | None | Query rewriting | Query routing | Planning, reflection, iteration |
| **Accuracy** | 60-70% | 75-85% | 80-90% | 85-95% |
| **Latency** | 1-2s | 2-4s | 2-5s | 5-30s |
| **Cost per query** | Low | Medium | Medium-High | High |
| **Implementation effort** | Days | Weeks | Months | Months+ |
| **Best for** | Internal tools, prototypes | Customer-facing products | Multi-domain knowledge bases | Complex research, compliance |

## Hybrid Search: The Best of Both Worlds

Vector search finds semantically similar content. But it has a weakness: it can miss exact keyword matches that are important.

If a user searches for "error code E-4012," a pure vector search might return chunks about error handling in general — semantically related, but not the specific error code. The chunk that contains the exact string "E-4012" might rank lower because its overall semantic content is about a different topic.

**BM25** is a traditional keyword search algorithm that's been the backbone of search engines for decades. It ranks documents by how often the search terms appear, adjusted for document length and term rarity. BM25 excels at exact matches — it will find "E-4012" every time.

**Hybrid search** combines both approaches:

```
HYBRID SEARCH
═══════════════════════════════════════════════════════

  User Query: "error code E-4012 connection timeout"
        │
        ├──────────────────────┬──────────────────────┐
        ▼                      ▼                      │
  ┌──────────────┐     ┌──────────────┐              │
  │ Vector Search│     │ BM25 Keyword │              │
  │ (semantic)   │     │ Search       │              │
  │              │     │              │              │
  │ Finds chunks │     │ Finds chunks │              │
  │ about network│     │ containing   │              │
  │ errors,      │     │ "E-4012"     │              │
  │ timeouts,    │     │ exactly      │              │
  │ connectivity │     │              │              │
  └──────┬───────┘     └──────┬───────┘              │
         │                    │                       │
         ▼                    ▼                       │
  ┌──────────────────────────────────┐               │
  │  Reciprocal Rank Fusion (RRF)    │               │
  │                                  │               │
  │  Combine rankings:               │               │
  │  • Chunk A: rank 3 (vector)      │               │
  │           + rank 1 (BM25) = top  │               │
  │  • Chunk B: rank 1 (vector)      │               │
  │           + rank 8 (BM25) = mid  │               │
  │  • Chunk C: rank 2 (vector)      │               │
  │           + rank 2 (BM25) = top  │               │
  └──────────────┬───────────────────┘               │
                 │                                    │
                 ▼                                    │
         Top K combined results                       │
         sent to LLM for generation                   │
                                                      │
═══════════════════════════════════════════════════════
```

The combination method matters. **Reciprocal Rank Fusion (RRF)** is the most common: it assigns each result a score based on its rank in each list (1/rank), then sums the scores. A chunk that ranks high in both lists gets a high combined score. A chunk that ranks high in only one list gets a moderate score.

Anthropic's RAG cookbook explicitly recommends hybrid search as a best practice. Their guidance: use vector search as the primary retrieval method, BM25 as a secondary signal, and combine them with RRF. The improvement over pure vector search is typically 10-20% in retrieval accuracy, and the additional implementation complexity is modest.

> **INTUITION**: Why does combining two imperfect search methods produce better results than either alone? Because their failure modes are different. Vector search fails on exact matches and rare terms. BM25 fails on semantic similarity and paraphrasing. What trips up one method is handled by the other. This principle — combining diverse signals with uncorrelated errors — is foundational in machine learning. It's the same reason ensemble models (combining multiple ML models) almost always beat individual models.

## Reranking: The Quality Filter

Retrieval is inherently noisy. Out of 20 retrieved chunks, maybe 5 are genuinely useful, 10 are tangentially related, and 5 are irrelevant. Feeding all 20 to the LLM wastes tokens, increases cost, and can confuse the model.

**Reranking** is a second pass that scores each retrieved chunk against the original query using a more powerful (and more expensive) model. The initial retrieval is fast and broad — cast a wide net. Reranking is slow and precise — examine each catch carefully.

> **ANALOGY**: Imagine you're hiring. The initial resume screen (retrieval) scans 500 applications in minutes using keyword matching and basic criteria. It passes 50 candidates forward. The interview round (reranking) spends 30 minutes with each of those 50 candidates, evaluating them deeply. You wouldn't interview all 500 — too expensive. You wouldn't skip the initial screen and pick randomly — too unreliable. The two-stage process gives you both efficiency and quality.

**How reranking works:**

1. **Retrieve** the top 20 chunks using vector search (or hybrid search)
2. **Score** each chunk using a cross-encoder model — a model that takes (query, chunk) as a pair and outputs a relevance score from 0 to 1
3. **Sort** by relevance score
4. **Keep** the top 5

Cross-encoder models are more accurate than embedding similarity because they process the query and chunk *together*, allowing deep interaction between the two texts. Embedding-based retrieval encodes query and chunk separately, then compares the resulting vectors — a less nuanced comparison.

Popular reranking models include Cohere Rerank, BGE Reranker, and ColBERT. The accuracy improvement from adding reranking is typically 5-15% — a meaningful gain that often makes the difference between a "kind of useful" and "genuinely reliable" RAG system.

The tradeoff: reranking adds 100-300ms of latency per query and costs additional compute. For real-time applications, this is worth it. For batch processing, it's a no-brainer.

## Long Context vs. RAG: Is RAG Dead?

With Gemini processing 1 million tokens (roughly 1,500 pages) and context windows growing every quarter, a reasonable question emerges: why bother with the complexity of chunking, embedding, storing, and retrieving when you can feed entire document collections directly into the model?

This "long context kills RAG" argument is wrong, but it's wrong in interesting ways.

**Where long context wins:**

- **Small knowledge bases**: If your entire documentation fits in the context window (under 500 pages), RAG adds complexity without clear benefit. Stuff it all in the context and let the model find what it needs.
- **Single-document analysis**: Analyzing one long contract, one codebase, one research paper — no retrieval needed.
- **Conversational depth**: Long context lets the model maintain awareness of the entire conversation history without summarization or retrieval tricks.

**Where RAG still wins — and will continue to:**

**Scale.** Most real-world knowledge bases are far larger than any context window. A company with 10 years of documentation, thousands of support tickets, hundreds of product specs, and years of Slack history has millions of documents. Even a 10-million-token context window (which doesn't exist yet) couldn't hold all of it. RAG scales to billions of chunks.

**Cost.** Processing 1 million tokens in the context costs roughly 100x more than processing 5,000 tokens (the typical RAG context). If you're serving 10,000 queries per day, the cost difference between "search and retrieve 5 relevant chunks" and "process the entire knowledge base for every query" is the difference between a viable business and bankruptcy.

**Accuracy.** Counterintuitively, more context can *hurt* accuracy. Research from multiple teams (including work discussed in Chip Huyen's *AI Engineering*, Chapter 8) shows that models struggle to find specific information buried in very long contexts. The model's attention doesn't distribute evenly — information in the middle of long contexts receives less attention than information at the beginning or end (the "lost in the middle" phenomenon). RAG preselects the relevant information, avoiding this problem.

**Freshness.** RAG indexes can be updated in real time as new documents arrive. There's no need to re-embed the entire corpus — append the new chunks and they're immediately searchable. Long context requires reassembling the full context on every query.

**Auditability.** RAG can cite exactly which chunks contributed to an answer. "This answer was based on sections 3.2 and 4.7 of the Enterprise Policy document, version 3.1, last updated January 15, 2026." Long context provides no such traceability.

> **REAL-LIFE**: The most sophisticated AI systems use both. Perplexity, the AI-powered search engine, retrieves relevant web pages using RAG-style retrieval, then feeds those pages into a model with a large context window for synthesis. It doesn't try to fit the entire internet into the context, and it doesn't limit itself to tiny chunks. The combination — retrieval for finding relevant documents, long context for understanding them — is the emerging best practice.

The realistic answer: RAG and long context are complementary, not competing. Use long context for small, bounded knowledge tasks. Use RAG for large, dynamic, or multi-source knowledge tasks. Use both together for the best results.

## Real-World RAG in Production

### Perplexity: RAG as Product

Perplexity is perhaps the purest example of RAG as a product. When you ask Perplexity a question:

1. It decomposes your question into search queries
2. Searches the web using multiple search engines
3. Retrieves and processes the top results
4. Feeds the relevant content to an LLM
5. Generates a cited, synthesized answer

Every answer includes numbered citations linked to source pages. This isn't a nice-to-have — it's the core value proposition. Users trust Perplexity because they can verify every claim. The RAG pipeline *is* the product.

### Notion AI: RAG Over Personal Knowledge

Notion AI retrieves relevant pages from a user's workspace before generating answers. The challenge is that Notion workspaces are deeply personal and idiosyncratic — every user's structure, naming conventions, and organizational patterns are different. Notion's embedding and retrieval system must generalize across millions of wildly different knowledge bases.

### GitHub Copilot: RAG Over Code

When GitHub Copilot suggests code completions, it doesn't rely solely on its training data. It uses RAG-style retrieval to find relevant code from the current repository — recent files you've edited, similar functions elsewhere in the codebase, project-specific patterns. This is why Copilot's suggestions get better the longer you work in a codebase: it has more context to retrieve from.

### PrabhupadaAI: RAG Over Spiritual Literature

This project — a conversational AI that answers questions based on Srila Prabhupada's teachings — processes a corpus of 157,000 chunks spanning books, lectures, conversations, and letters. The RAG pipeline uses FAISS for vector storage, recursive chunking with overlap, and a carefully crafted system prompt that instructs the model to ground all answers in Prabhupada's actual words.

Three lessons learned from building this system:

**Chunk quality is everything.** We spent more time on chunking strategy than on any other component. A lecture transcript where Prabhupada shifts from discussing karma to discussing devotion needs to be split at the topic boundary, not at an arbitrary token count. Getting this wrong meant the retrieval would return chunks that started on one topic and ended on another — confusing both the retrieval model and the generation model.

**Metadata is the secret weapon.** Each chunk carries metadata: source book or lecture, date, location, topic tags. This enables filtered retrieval — "What does Prabhupada say about karma *in the Bhagavad Gita*?" retrieves only chunks from that specific text, not from every source. Without metadata filtering, a query about a Gita verse might retrieve a casual conversation transcript that mentions the same verse in passing.

**Evaluation is hard and necessary.** How do you measure whether the AI's answer is faithful to Prabhupada's teachings? We built a test set of 200 question-answer pairs validated by scholars. The RAG system's answers were compared against these ground truths. This evaluation pipeline — building it, running it, iterating on it — consumed 30% of the total development effort. Skip evaluation and you ship a system that *feels* right but might be wrong in ways you can't detect.

## Building Your First RAG System

This exercise walks you through building a working RAG pipeline over a PDF document using Claude and Python. By the end, you'll have a system that answers questions about any PDF you feed it.

<div class="exercise">
<div class="exercise-title">Exercise: Build a RAG System Over a PDF</div>

**What you'll build**: A Python script that takes a PDF, chunks it, embeds the chunks, stores them, and answers questions using retrieval + Claude.

**Prerequisites**: Python 3.10+, a Claude API key (from console.anthropic.com)

**Step 1: Set up the project**

Open Claude Code and type:

```
Create a new Python project called "my-first-rag" with a virtual
environment. Install these packages: anthropic, PyPDF2, chromadb,
rich (for pretty printing).
```

**Step 2: Ingest a PDF**

Place any PDF in the project folder. A company policy document, a research paper, a product spec — anything with substantial text.

```
In my-first-rag, write a script called ingest.py that:
1. Reads a PDF file using PyPDF2
2. Splits the text into chunks of ~400 tokens with 15% overlap
3. Uses the Anthropic API to generate embeddings for each chunk
   (or use an open-source embedding model via chromadb's default)
4. Stores the chunks and embeddings in a local ChromaDB collection
5. Prints how many chunks were created
```

**Step 3: Query the system**

```
Write a script called query.py that:
1. Takes a question as a command-line argument
2. Embeds the question
3. Retrieves the 5 most similar chunks from ChromaDB
4. Sends the chunks + question to Claude with a system prompt
   that says "Answer based only on the provided context"
5. Prints the answer with source citations
```

**Step 4: Test it**

Run: `python query.py "What is the main topic of this document?"`

Then try progressively harder questions:
- A factual question with an explicit answer in the text
- A question that requires synthesizing information from multiple sections
- A question the document doesn't answer (the system should say so)

**Step 5: Evaluate and improve**

```
Enhance the system:
1. Add hybrid search (ChromaDB supports this)
2. Add a reranking step that uses Claude to score each chunk's
   relevance before generating the final answer
3. Add metadata (page numbers) so answers cite specific pages
```

**Reflection questions**: Which questions did the system answer well? Which did it struggle with? Were the retrieved chunks the right ones? When the answer was wrong, was the problem in retrieval (wrong chunks) or generation (right chunks, wrong answer)?

</div>

## The Practitioner's Checklist

If you're a product manager evaluating or specifying a RAG system, these are the questions that matter:

**On chunking**: What is the chunk size? How were boundaries determined? Is there overlap? Were different strategies tested? Chunking decisions made early constrain everything downstream.

**On retrieval**: Is the system using pure vector search, pure keyword search, or hybrid? What is the top-K value? Has retrieval accuracy been measured independently from generation accuracy? A system can generate beautiful answers from the wrong chunks.

**On evaluation**: What is the test set? Who created it? How are answers scored? Is the team measuring retrieval accuracy (are the right chunks being found?) separately from end-to-end accuracy (are the final answers correct?)? Without separate measurement, you can't diagnose whether problems are in retrieval or generation.

**On freshness**: How are new documents added to the index? How are outdated documents removed? What happens when a document is updated — is the old version's chunks replaced? Stale knowledge bases erode trust.

**On cost**: What is the cost per query? How does it break down between embedding, retrieval, and generation? Can the system be optimized (smaller chunks = fewer tokens in the generation step = lower cost)?

---

**Chapter endnotes**

[1] Patrick Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (2020) introduced the RAG framework and demonstrated its effectiveness on multiple benchmarks. The paper showed that combining retrieval with generation outperformed both pure retrieval and pure generation approaches across diverse knowledge-intensive tasks.

[2] Eugene Yan's writing on RAG patterns, particularly his posts on applied ML at eugeneyan.com, has become the de facto vocabulary for discussing RAG system evolution. His framework of Naive → Advanced → Modular → Agentic RAG is widely cited by practitioners and framework developers alike.

[3] Anthropic's RAG cookbook (docs.anthropic.com) provides production-grade guidance on hybrid search, chunk sizing, and prompt construction for RAG systems. Their explicit recommendation of combining BM25 with vector search, using Reciprocal Rank Fusion, reflects lessons learned from deploying RAG at scale across customer workloads.

[4] Jerry Liu, founder of LlamaIndex, has been the most vocal advocate for Agentic RAG — the idea that retrieval should be an agent capability, not a fixed pipeline. His talks and writing (notably "The Future of RAG is Agentic") argue that rigid retrieve-then-generate pipelines fail on complex questions that require iterative reasoning about what information is needed.

[5] Chip Huyen's *AI Engineering* (O'Reilly, 2025), particularly Chapter 8 on retrieval and memory, provides the most thorough treatment of the "lost in the middle" phenomenon — the finding that LLMs struggle to use information placed in the middle of long contexts. Her analysis of when to use RAG vs. long context vs. fine-tuning remains the clearest framework for practitioners making this architectural decision.

[6] The "lost in the middle" finding was first published by Nelson F. Liu et al. (2023) in "Lost in the Middle: How Language Models Use Long Contexts," demonstrating that models perform best when relevant information appears at the very beginning or very end of the context, with significant degradation for information placed in the middle — even for models specifically designed for long-context tasks.

[7] FAISS (Facebook AI Similarity Search), developed by Meta's Fundamental AI Research team, is the most widely used library for efficient similarity search over dense vectors. It supports multiple index types with different speed/accuracy tradeoffs and scales to billions of vectors.

[8] The PrabhupadaAI system referenced in this chapter processed a corpus of Srila Prabhupada's books, lectures, conversations, and letters — spanning over four decades of teaching — into 157,000 indexed chunks using FAISS with recursive text splitting and 15% chunk overlap.
