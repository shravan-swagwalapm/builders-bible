<div class="milestone-project">
<h2>Milestone Project 3: RAG Knowledge Assistant</h2>
<p>Upload your documents, ask questions, get cited answers with source references. A complete retrieval-augmented generation system — from document ingestion to evaluation.</p>
</div>

**Companion repo:** `builders-bible/project-03-rag-chatbot`

**Time estimate:** 12-18 hours across 4-5 sessions

**What this proves you can build:** An AI system that knows things the base model doesn't, grounds its answers in evidence, and can tell you exactly where it found the information.

---

## Why This Project

The data dashboard from Project 2 was powerful but limited. Claude could only answer questions about data you fed into each prompt. What if you have 200 pages of company documentation and you want to ask: "What's our refund policy for enterprise customers?"

You can't stuff 200 pages into a prompt. The context window is finite, and even if it weren't, models get worse at finding specific information when the context is massive (the "lost in the middle" problem from Chapter 10).

RAG solves this. You split your documents into chunks, convert each chunk into an embedding (a numerical fingerprint of its meaning), store those embeddings in a vector database, and when a user asks a question, you find the most relevant chunks, inject only those into the prompt, and let the model answer based on specific evidence.

This is the architecture behind every "chat with your docs" product you've seen. After this project, you'll understand exactly how they work — and exactly where they fail.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Document Ingestion Pipeline                │
│                                                              │
│  Upload → Extract Text → Chunk → Embed → Store              │
│  (PDF,    (pdf-parse,    (recursive  (Voyage/    (Supabase   │
│   DOCX,   mammoth)        splitter)   OpenAI)     pgvector)  │
│   TXT)                                                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Query Pipeline                          │
│                                                              │
│  User Question                                               │
│       │                                                      │
│       ▼                                                      │
│  Embed Question ──→ Vector Search ──→ Top-K Chunks           │
│                     (cosine similarity)    │                  │
│                                            ▼                 │
│                                    Build Prompt              │
│                                    (system + chunks          │
│                                     + conversation           │
│                                     + question)              │
│                                            │                 │
│                                            ▼                 │
│                                    Claude API                │
│                                            │                 │
│                                            ▼                 │
│                                    Answer + Citations        │
│                                    (with source references)  │
└─────────────────────────────────────────────────────────────┘
```

**Tech stack:**
- **Framework:** Next.js 14 (App Router)
- **Vector database:** Supabase with pgvector extension
- **Embeddings:** Voyage AI (or OpenAI `text-embedding-3-small`)
- **LLM:** Claude API with structured output for citations
- **Document parsing:** `pdf-parse` for PDFs, `mammoth` for DOCX
- **Chunking:** Recursive character text splitter with overlap
- **Evaluation:** Custom eval framework (accuracy, citation quality, hallucination detection)
- **Deployment:** Vercel + Supabase

---

## What You'll Build, Step by Step

### Phase 1: Document Ingestion (Session 1)

The user uploads a PDF. Your pipeline:

1. **Extracts text** — PDF parsing is messier than you think. Tables break. Headers repeat on every page. Scanned documents yield nothing without OCR.
2. **Chunks the text** — You'll implement recursive character splitting: try to split on paragraphs, then sentences, then words. Each chunk is 500-1000 tokens with 100-token overlap so context isn't lost at boundaries.
3. **Generates embeddings** — Each chunk becomes a 1024-dimensional vector using Voyage AI. These vectors capture semantic meaning: chunks about "refund policy" will be close to chunks about "return process" in vector space, even if they share no words.
4. **Stores in Supabase** — The chunk text, its embedding, and metadata (source document, page number, chunk index) go into a pgvector-enabled table.

This phase is where Chapter 11 (embeddings) and Chapter 4 (databases) converge. You'll write SQL that uses cosine similarity to search vectors — a query type that didn't exist in traditional databases until recently.

### Phase 2: Retrieval (Session 2)

The user asks: "What are the supported payment methods?" Your system:

1. Embeds the question using the same model that embedded the chunks
2. Runs a vector similarity search: `SELECT * FROM chunks ORDER BY embedding <=> question_embedding LIMIT 5`
3. Returns the top 5 most semantically similar chunks

You'll immediately discover the first failure mode: retrieval quality. The chunks you get back might be *related* but not *relevant*. A chunk about "payment processing architecture" is semantically close to "payment methods" but doesn't answer the question.

This is where you'll implement **hybrid search** — combining vector similarity with keyword matching (BM25). The vector search captures meaning; the keyword search captures exact terms. Together, they catch what each misses alone.

### Phase 3: Generation with Citations (Session 2)

You build a prompt:

```
You are a knowledge assistant. Answer the user's question using ONLY
the provided context. If the context doesn't contain the answer, say so.

For every claim in your answer, cite the source using [Source N] format,
where N corresponds to the chunk number.

Context:
[Chunk 1 - payments.pdf, page 12]: "We support UPI, credit cards..."
[Chunk 2 - faq.pdf, page 3]: "Enterprise customers can also pay via..."

Question: What are the supported payment methods?
```

Claude's structured output returns:

```json
{
  "answer": "The supported payment methods are UPI, credit cards [Source 1], and enterprise customers also have access to wire transfer [Source 2].",
  "sources": [
    {"chunk_id": 1, "document": "payments.pdf", "page": 12, "relevance": "high"},
    {"chunk_id": 2, "document": "faq.pdf", "page": 3, "relevance": "medium"}
  ],
  "confidence": "high"
}
```

Citations are not optional. They're the difference between a useful tool and a hallucination machine. Your users need to verify every answer, and they can only do that if you show them exactly where the information came from.

### Phase 4: Conversation Memory (Session 3)

"What about for international customers?" — this follow-up only makes sense in context of the previous answer. You'll implement a conversation window that includes the last few exchanges, compressed into summaries to save tokens.

The challenge: balancing conversation context against retrieval context. Your prompt has a finite budget. Spend too much on conversation history and you have less room for retrieved chunks. Spend too little and follow-up questions break. You'll find the balance through experimentation, not theory.

### Phase 5: Evaluation Framework (Session 4)

This is the phase most tutorials skip and most production systems regret skipping.

You'll build a test suite of 20 question-answer pairs with known correct answers. For each question, your eval framework measures:

- **Retrieval quality:** Did the right chunks get retrieved? (Recall@5)
- **Answer accuracy:** Does the generated answer match the expected answer? (LLM-as-judge)
- **Citation quality:** Are citations accurate? Does each claim have a source?
- **Hallucination rate:** Did the model add information not present in any chunk?

Every time you change your chunking strategy, embedding model, prompt template, or retrieval method, you run the eval suite. Without this, you're optimizing blind.

### Phase 6: Deploy and Harden (Session 5)

Rate limiting (Claude API calls are expensive). File size limits (someone will try to upload a 500MB PDF). Auth (each user's documents are private). Error handling (what if the embedding API is down?). Cost tracking (how much does each conversation cost?).

---

## What Will Go Wrong (And What It Teaches)

- **Retrieved chunks are related but don't answer the question.** Your chunking strategy is wrong — chunks are too large or split in the wrong places. This teaches you that RAG quality is 70% retrieval quality.
- **The model ignores retrieved chunks and answers from its training data.** Your prompt isn't explicit enough about grounding. Add "Answer ONLY from the provided context" and watch the behavior change.
- **Citations point to the wrong chunks.** The model is associating claims with sources based on position, not content. Shuffle chunk order in your prompt and see if citations still hold.
- **Performance degrades as you add more documents.** Your vector index needs tuning. This teaches you that vector search at scale requires HNSW indexes, not brute-force cosine similarity.

---

## Definition of Done

Upload your company's documentation (or a textbook, or any 50+ page PDF). Ask 10 questions. Verify that every answer is grounded in actual document content, every citation points to the right source, and the system says "I don't know" when the answer isn't in the documents.

The hardest test: ask a question where the answer is *not* in your documents. A good RAG system says "I don't have enough information to answer this." A bad one makes something up confidently. Yours should be good.
