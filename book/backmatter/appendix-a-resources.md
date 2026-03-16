<span class="chapter-number">Appendix A</span>

# The Builder's Resource Vault {.chapter-title}

This is not a link dump. Every resource here was chosen because it changed how we think about building with AI. They're ordered within each category from "start here" to "go deeper." Bookmark this appendix. Return to it as your skills evolve — the resources that seem too advanced today will be exactly what you need in three months.

A note on longevity: the AI field moves fast, and links break. We've prioritized resources from authors and institutions with track records of maintaining their content. Where possible, we've included the author's name and year so you can find the resource even if the URL changes. For the most up-to-date links, check the companion repository.

---

## Must-Read Articles

These fifteen pieces represent the best writing on applied AI and software engineering. Read them in order if you're starting fresh; cherry-pick if you already have context.

**1. "Building LLM Applications for Production" — Chip Huyen (2023)**
The single best overview of what goes wrong when you move from prototype to production. Covers evaluation, prompt management, cost optimization, and the gap between demo and deployment. Read this before you ship anything. *Pairs with: Chapters 10-11, Project 2*

**2. "Patterns for Building LLM-based Systems & Products" — Eugene Yan (2023)**
A taxonomy of patterns: RAG, agents, structured output, evaluation. Eugene's gift is naming things precisely. After reading this, you'll have vocabulary for architectural decisions you were making intuitively. *Pairs with: Chapters 13, 15*

**3. "Building Effective Agents" — Anthropic (2024)**
Anthropic's internal guide to agent design. Covers tool use, reasoning loops, error recovery, and when *not* to use agents. The section on when a simple prompt chain outperforms an agent loop is worth the entire read. *Pairs with: Chapter 15, Project 4*

**4. "What We Learned from a Year of Building with LLMs" — Eugene Yan et al. (2024)**
Six practitioners share hard-won lessons. The tactical advice on caching, evaluations, and prompt versioning is immediately applicable. The strategic advice on when to fine-tune vs. prompt-engineer will save you weeks. *Pairs with: Chapters 11, 14*

**5. "The Illustrated Transformer" — Jay Alammar (2018)**
Still the best visual explanation of the transformer architecture. You don't need to implement one, but understanding attention mechanisms — what the model is actually doing when it generates a token — makes you a better prompt engineer. *Pairs with: Chapter 10*

**6. "A Survey on Retrieval-Augmented Generation" — Lilian Weng (2024)**
Lilian's surveys are graduate-level education compressed into blog posts. This one covers every RAG variant: naive, advanced, modular, self-reflective. Pair it with Project 3 for maximum impact. *Pairs with: Chapter 13, Project 3*

**7. "What Are Embeddings" — Vicki Boykis (2023)**
The clearest explanation of embeddings written for practitioners. Starts from first principles (word2vec) and builds to modern embedding models. After reading this, Chapter 12 will make twice as much sense. *Pairs with: Chapter 12*

**8. "Prompt Engineering" — Lilian Weng (2023)**
A comprehensive survey of prompting techniques: few-shot, chain-of-thought, tree-of-thought, self-consistency. Academic rigor with practical examples. Bookmark and revisit as your prompting skills develop. *Pairs with: Chapter 11*

**9. "Large Language Models" — Simon Willison (ongoing blog)**
Simon blogs about LLMs with the curiosity of an explorer and the rigor of an engineer. His posts on local models, prompt injection, and the ethics of AI-generated content are essential reading. Follow the blog, not just individual posts. *Pairs with: Chapters 10, 28*

**10. "Software 2.0" — Andrej Karpathy (2017)**
The essay that named the paradigm shift. Software 1.0 is code you write. Software 2.0 is behavior you train. Still the best framing for understanding why AI changes everything about how we build. *Pairs with: Chapter 9*

**11. "The Bitter Lesson" — Rich Sutton (2019)**
One page that explains 70 years of AI research: general methods that leverage computation always win over clever hand-designed approaches. This is why scaling laws matter and why the models keep getting better. *Pairs with: Chapter 9*

**12. "How to Evaluate LLMs" — Hamel Husain (2024)**
Hamel's guide to building evaluation pipelines that actually work. Covers LLM-as-judge, human evaluation, automated metrics, and the meta-problem of evaluating your evaluator. Essential reading before Project 3's eval framework. *Pairs with: Projects 3, 4*

**13. "Emerging Architectures for LLM Applications" — a16z (2023)**
The venture capital perspective on AI infrastructure. Useful for understanding what the industry is building toward: embedding pipelines, vector databases, orchestration layers, and evaluation frameworks as a category. *Pairs with: Chapter 8*

**14. "Latent Space: The AI Engineer" — swyx (2023)**
The essay that defined the AI Engineer role — a developer who builds with models rather than building models. If you're reading this book, you're becoming an AI Engineer. This essay explains what that means and why the role exists. *Pairs with: all of Part II*

**15. "Chinchilla's Wild Implications" — Nostalgebraist (2022)**
A deep dive into scaling laws and what they mean for model training. Technical but approachable. Understanding scaling laws helps you predict where AI capabilities are heading — which informs what you should build today versus what you should wait for. *Pairs with: Chapter 9*

---

## Must-Watch

Ten videos that teach better than text can. Estimated viewing time in parentheses.

**1. "Let's Build GPT: from scratch, in code" — Andrej Karpathy (~2 hours)**
Karpathy builds a GPT from a blank Python file. You watch tokens, attention, and generation emerge from simple math. Even if you never train a model, this video transforms your understanding of what's happening inside the API you're calling. The most valuable two hours of AI education available for free.

**2. "But what is a neural network?" — 3Blue1Brown (series, ~1 hour total)**
The gold standard for visual math explanation. Three videos in this series cover neural networks, gradient descent, and backpropagation. No prerequisites beyond high school math. Grant Sanderson's animations make abstract concepts tangible.

**3. "Intro to Large Language Models" — Andrej Karpathy (1 hour)**
A one-hour masterclass on LLM concepts: training, inference, fine-tuning, RLHF, and emerging capabilities. Designed for a general audience. Watch this before reading Part II if you're a visual learner.

**4. "AI Engineering 101" — swyx (45 min)**
Practical overview of building with LLMs. Covers the AI engineer stack, common patterns, and mistakes to avoid. More practical than academic — the perfect complement to the theoretical videos above.

**5. "The Spelled-Out Intro to Neural Networks and Backpropagation" — Andrej Karpathy (~2.5 hours)**
Goes deeper than 3Blue1Brown. Karpathy builds a neural network from scratch, explaining every gradient calculation. Watch at 1.5x. Pause and re-derive. This video builds mathematical intuition that lasts.

**6. "State of GPT" — Andrej Karpathy at Microsoft Build (45 min)**
The training pipeline of GPT models explained: pretraining, supervised fine-tuning, RLHF. Demystifies what happens between "we scraped the internet" and "ChatGPT answers your question."

**7. "Attention in Transformers, Visually Explained" — 3Blue1Brown (25 min)**
The visual explanation of attention mechanisms the world was waiting for. Complements "The Illustrated Transformer" article perfectly. Watch after reading Chapter 10.

**8. "Building AI Applications with the Anthropic API" — Anthropic (series, ~2 hours total)**
Official tutorials covering the Anthropic SDK, tool use, streaming, and structured output. Directly applicable to every project in this book. Authoritative and up-to-date.

**9. "The Unreasonable Effectiveness of Recurrent Neural Networks" — Andrej Karpathy (talk, 45 min)**
The talk version of the famous blog post. Karpathy's enthusiasm is infectious, and seeing character-level models generate Shakespeare, LaTeX, and C code drives home what "learning patterns" really means.

**10. "How I Use AI as a Solo Developer" — Fireship (12 min)**
A fast, practical overview of AI-assisted development workflows. Useful for seeing how experienced developers actually integrate AI into daily work, not just toy demos. Good calibration for realistic expectations.

---

## Free Courses

Fifteen courses that cover everything from foundations to production AI. All free or offer free audit options.

**1. Anthropic's Prompt Engineering Course**
Official course from the company behind Claude. Covers system prompts, few-shot examples, chain-of-thought, and tool use. Start here if you're working through Part II. Updated frequently as best practices evolve.

**2. Anthropic's Tool Use Course**
Deep dive into function calling and MCP. Directly applicable to Chapter 16 and Project 4. Includes hands-on exercises with the Anthropic API.

**3. Anthropic's Building with Claude Course**
End-to-end application building with the Anthropic API. Covers streaming, structured output, conversation management, and evaluation. The closest thing to a companion course for this book.

**4. DeepLearning.AI: ChatGPT Prompt Engineering for Developers**
Andrew Ng and Isa Fulford. Short, practical, code-heavy. A good complement to Anthropic's course — different model, same principles. Completable in a weekend.

**5. DeepLearning.AI: Building Systems with the ChatGPT API**
Chains, routing, evaluation, and moderation. The patterns are model-agnostic despite the OpenAI branding. Good preparation for Project 4.

**6. DeepLearning.AI: LangChain for LLM Application Development**
Even if you don't use LangChain (and this book argues you often shouldn't), understanding its abstractions teaches you what problems orchestration frameworks are trying to solve. Know what you're choosing not to use.

**7. DeepLearning.AI: Building RAG Agents with LLMs**
Practical RAG implementation with retrieval strategies, evaluation, and deployment. Pair with Chapter 13 and Project 3 for a complete RAG education.

**8. Stanford CS229: Machine Learning (YouTube)**
Andrew Ng's legendary Stanford course. More depth than you need for this book, but invaluable if you want to understand the math behind the models. Audit the first 10 lectures for maximum return on time invested.

**9. Stanford CS224N: NLP with Deep Learning (YouTube)**
The academic foundation for everything in Part II. Transformers, attention, pretraining, fine-tuning. Watch selectively — lectures 1-5 and the transformer lectures are most relevant to this book.

**10. Fast.ai: Practical Deep Learning for Coders**
Jeremy Howard's top-down approach: start building, understand theory as you go. Philosophically aligned with this book. The lessons on learning rate, transfer learning, and data augmentation are timeless.

**11. Google AI Essentials (Coursera, free audit)**
Non-technical introduction to AI concepts. Good for complete beginners who want context before Part II. Less depth than DeepLearning.AI courses, but broader coverage.

**12. freeCodeCamp: Full Stack Web Development**
Comprehensive web development curriculum covering HTML, CSS, JavaScript, Node.js, and databases. Covers everything in Part I and more. Use it as a reference when you want deeper practice on any web topic.

**13. The Odin Project: Full Stack JavaScript**
Project-based web development education. Excellent for building the muscle memory of creating, breaking, and fixing web applications. Less lecture, more building.

**14. Harvard CS50: Introduction to Computer Science (edX)**
The best introduction to computer science ever created. David Malan's lectures are legendary for clarity and energy. Watch the first 6 weeks if Part 0 left you wanting more depth on how computers actually work.

**15. Hugging Face: NLP Course**
Hands-on NLP with transformers. More technical than this book requires, but invaluable if you're heading toward fine-tuning (Chapter 14). Free, self-paced, and backed by one of the most important companies in open-source AI.

---

## Books

Ten books that go deeper than any course or blog post. These are the ones worth owning physically — the kind you'll highlight, dog-ear, and return to across years. Ordered from most immediately practical to most foundational.

**1. *Designing Machine Learning Systems* — Chip Huyen (O'Reilly, 2022)**
The production ML bible. Covers data engineering, feature stores, evaluation, deployment, monitoring, and maintenance. Read after completing all four projects. The chapter on data distribution shifts alone is worth the price.

**2. *AI Engineering* — Chip Huyen (O'Reilly, 2025)**
Chip's follow-up focused specifically on building AI applications. Covers evaluation, RAG, agents, fine-tuning, and production deployment. The most comprehensive single book on applied AI engineering.

**3. *Designing Data-Intensive Applications* — Martin Kleppmann (O'Reilly, 2017)**
The most important software engineering book of the decade. Covers databases, distributed systems, consistency, and replication. Dense but transformative. Read Chapter 2 (Data Models) and Chapter 3 (Storage) first. Return to the rest as your systems grow.

**4. *Build a Large Language Model (From Scratch)* — Sebastian Raschka (Manning, 2024)**
Implements a GPT-style model from raw Python. The book equivalent of Karpathy's "Let's Build GPT" video, with more depth, exercises, and explanation. For readers who want to understand the machinery, not just the interface.

**5. *System Design Interview* — Alex Xu (2020, 2022)**
Two volumes of system design problems: URL shortener, rate limiter, chat system, search autocomplete. Each solution teaches architectural patterns you'll use in your own projects. Practical and interview-relevant.

**6. *Vibe Coding: The Future of Programming* — Addy Osmani (O'Reilly, 2025)**
A practical guide to building software with AI assistance. Covers workflows, prompt strategies, and the mindset shift from "writing code" to "directing code." Directly relevant to how this book teaches building.

**7. *The Pragmatic Programmer* — David Thomas & Andrew Hunt (Addison-Wesley, 2019)**
Timeless principles of software craftsmanship. "Tracer bullets," "broken windows," and "good enough software" apply whether you're writing code or directing AI to write it. The 20th-anniversary edition is still fresh.

**8. *Refactoring UI* — Adam Wathan & Steve Schoger (2018)**
Design fundamentals for developers. Color, typography, spacing, hierarchy — everything from Chapter 21 (Design Systems) in gorgeous visual detail. More practical than any design course. Directly inspired Appendix C.

**9. *Staff Engineer* — Will Larson (2021)**
What happens after senior? Technical leadership, architecture decisions, organizational influence. Read this when you're building systems used by teams, not just by yourself.

**10. *The Missing README* — Chris Riccomini & Dmitriy Ryaboy (2021)**
Everything they don't teach you in school or bootcamps: code reviews, on-call, technical debt, working with managers. Practical, human, and surprisingly funny.

---

## Templates and Tools

Ten resources you'll use repeatedly across all projects. These aren't learning materials — they're working tools. The difference between a template and a tutorial is that a template saves you time on day one and every day after.

All templates are available in the companion repository and are designed to be forked, not copied. Make them yours.

**1. CLAUDE.md Templates (Appendix B)**
Starter, Advanced, and Team templates for configuring Claude Code. The single highest-leverage file in any AI-assisted project. Three templates covering beginner to multi-person team workflows.

**2. Design System Starter Kit (Appendix C)**
Color tokens (light/dark), typography scale, spacing system, component patterns. Fork it, customize it, use it on every project. Prevents the "every component looks different" problem.

**3. Eval Framework Template**
A starter evaluation pipeline with LLM-as-judge, rule-based checks, and metric tracking. Used in Projects 3 and 4. Available in the companion repos with example test cases.

**4. Next.js + Supabase Starter**
Pre-configured with auth, Row Level Security, dark mode, and the design system from Appendix C. The foundation for Projects 2-4. Saves 2-3 hours of boilerplate on every new project.

**5. Prompt Library Template**
Versioned prompt templates with variable injection, A/B testing support, and cost tracking. Organize your prompts like code, not like sticky notes. Includes a naming convention and changelog format.

**6. MCP Server Starter**
A minimal MCP server implementation with tool registration, error handling, and TypeScript types. Your starting point for Chapter 16 and a base for any custom tool integration.

**7. Cost Tracking Dashboard**
A Supabase-backed dashboard that logs every LLM API call with model, tokens, latency, and cost. Used in Project 4, reusable across all AI projects. Includes alerts for budget thresholds.

**8. CI/CD Pipeline Template**
GitHub Actions workflow with TypeScript checking, linting, testing, and deployment. Pre-configured for Vercel and Railway. Drop into any project repository.

**9. Security Checklist**
A markdown checklist covering auth, input sanitization, environment variables, RLS, rate limiting, and OWASP top 10. Review before every deployment. Used in Chapter 28.

**10. Production Readiness Checklist**
Error handling, monitoring, logging, backup, scaling, and incident response. The checklist that turns a project into a product. Referenced in Chapter 27.

---

---

## How to Use This Vault

**If you're just starting:** Read articles 1, 2, and 5. Watch videos 1 and 2. Take Anthropic's Prompt Engineering Course. Read *Refactoring UI* alongside Part I of this book.

**If you're building your first AI product:** Read articles 3, 4, 6, and 12. Watch videos 3 and 5. Take the DeepLearning.AI courses on prompt engineering and RAG. Use templates 1-4 from the Tools section.

**If you're going to production:** Read articles 4, 7, 8, and 12. Read *Designing Machine Learning Systems* and *Designing Data-Intensive Applications*. Use the eval framework, security checklist, and production readiness checklist.

**If you want to go deep on AI fundamentals:** Watch the full Karpathy video series. Take Stanford CS224N. Read *Build a Large Language Model from Scratch*. Read Lilian Weng's survey articles. These won't make you ship faster today, but they'll make you a fundamentally better builder for the rest of your career.

*Resources evolve faster than books. For the latest links, additions, and community contributions, visit the companion repository at `builders-bible/resources`. If you find a resource that belongs here, open a pull request — this vault is community-maintained.*
