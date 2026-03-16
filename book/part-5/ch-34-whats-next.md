<span class="chapter-number">Chapter 34</span>

# What's Next — The Builder's Horizon {.chapter-title}

Every chapter in this book has been about the present — technologies that exist, tools you can use today, patterns that are working in production right now. This final chapter is different. It looks forward. Not into the distant, speculative future, but into the near horizon — the 12-24 months ahead where trends that are currently emerging will become the default tools and paradigms of every builder.

Some of what follows will age well. Some will turn out to be wrong. That is the nature of prediction in a field that moves as fast as AI. But the underlying currents — the direction of the tide, not the specific waves — are readable. And reading them gives you a head start.

This chapter covers video AI, memory and personalization, the agentic operating system, the open-source tide, the convergence of AI with traditional developer tools, the regulatory landscape, the job market implications, and — most importantly — what to learn next after you close this book.

---

## Video AI: The Next Modality

Text is solved. Images are solved. Audio is solved (Chapter 32). Video is next — and it is arriving faster than most people expect.

### The Landscape

**OpenAI's Sora** generated the first viral AI videos in early 2024 and launched publicly in late 2024. The quality was stunning: photorealistic videos up to 60 seconds long, generated from text prompts. The limitations were equally notable — Sora struggled with physics (objects floating impossibly, hands with wrong numbers of fingers, water flowing uphill) and with temporal consistency (objects appearing and disappearing between frames).

**Runway** has been the most aggressive commercial player, with their Gen-3 Alpha model producing high-quality short clips. Their focus is on creative professionals — filmmakers, advertisers, and content creators who need footage that doesn't exist.

**Kling** (from Kuaishou, China) has matched or exceeded Sora's quality on several benchmarks while being available much earlier. **MiniMax** and **Pika** round out the competitive field.

```
Video AI Model Comparison (Early 2026):

  Model            Max Length   Quality     Physics     Cost         Access
  ──────────────   ──────────   ─────────   ─────────   ───────────  ────────
  Sora             60 sec       Excellent   Improving   ~$0.10/sec   API
  Runway Gen-3     10 sec       Excellent   Good        ~$0.05/sec   Web+API
  Kling 2.0        30 sec       Very Good   Good        ~$0.03/sec   API
  MiniMax          10 sec       Good        Fair        ~$0.02/sec   API
  Pika 2.0         10 sec       Very Good   Fair        ~$0.04/sec   Web+API

  Quality: visual fidelity, realism, resolution
  Physics: does water flow downhill? do objects have consistent shadows?
```

### What Builders Should Watch

Video AI is not yet at the "use it in production" stage for most applications. The quality is inconsistent, the cost is high for anything beyond short clips, and the physics errors make the output unsuitable for contexts where realism matters (education, documentation, product demos).

But three trends suggest this will change rapidly:

1. **Video understanding is preceding video generation.** Models like Gemini 2.5 Pro can already watch a video and answer questions about it — identifying objects, describing actions, transcribing speech, and reasoning about the content. This understanding capability is more immediately useful than generation for most builders: automatically tagging and categorizing video content, extracting key moments from long recordings, generating summaries of video meetings.

2. **Short-form video is where the quality threshold is already met.** A 5-second product animation, a 10-second social media clip, a 3-second loading animation — for these use cases, current video AI quality is sufficient. Builders who work in marketing, social media, and content creation can use these tools today.

3. **The combination of video AI with other modalities is the unlock.** A system that watches a lecture recording (video understanding), generates a transcript (audio → text), creates a summary (LLM), produces visual aids (image generation), and assembles them into a study guide (compound AI system) — this is a compound system problem, not a video generation problem. The video AI component doesn't need to be perfect. It needs to be good enough for one step in a larger pipeline.

> **INTUITION**: Video AI in 2026 is roughly where image AI was in 2022 — impressive demos, limited production use cases, rapidly improving quality, and enormous creative potential. Builders who start experimenting now, even with the limitations, will have a significant advantage when the quality crosses the production threshold in 12-18 months.

---

## Memory & Personalization: AI That Knows You

The AI systems you've used so far have amnesia. Every conversation starts from zero. The model doesn't remember that you prefer concise answers, that you work in fintech, that you asked about Kubernetes yesterday, or that your name is Priya.

This is changing.

### ChatGPT Memory

OpenAI's ChatGPT introduced persistent memory in 2024 — the model remembers facts about you across conversations. It learns your preferences, your context, your communication style. Over time, the model becomes personalized: it knows you're a product manager at a Series B startup, that you prefer bullet points over paragraphs, and that when you say "the usual" you mean your standard code review prompt.

The implementation is straightforward: the model extracts key facts from conversations and stores them in a user-specific memory. Before each new conversation, these facts are injected into the system prompt. The model doesn't truly "remember" — it reads its notes.

### Mem0: Memory as Infrastructure

**Mem0** (pronounced "memo") is an open-source memory layer for AI applications. It provides the infrastructure to add persistent memory to any AI system:

```
Mem0 — Memory Layer Architecture:

  User Interaction → LLM generates response
                          │
                          ├── Memory Extractor: "What facts from
                          │   this conversation should be remembered?"
                          │
                          ├── Memory Store: Vector database +
                          │   structured metadata per user
                          │
                          └── Memory Retriever: Before next conversation,
                              retrieve relevant memories and inject
                              into system prompt

  Memory Types:
  ┌────────────────────────────────────────────────────────┐
  │  FACTUAL:    "User is a PM at FinCo, based in Mumbai"  │
  │  PREFERENCE: "User prefers concise, technical answers"  │
  │  CONTEXTUAL: "User is working on a payments migration"  │
  │  RELATIONAL: "User's team uses Next.js and Supabase"    │
  └────────────────────────────────────────────────────────┘
```

For builders, Mem0 represents a pattern more than a product. The pattern: extract, store, retrieve, and inject user-specific context into every AI interaction. You can implement this with any vector database and any LLM. Mem0 provides a convenient abstraction, but the architecture is reproducible.

> **REAL-LIFE**: A healthcare AI assistant using memory can track a patient's mentioned symptoms across multiple conversations, remember their medication history, and provide context-aware follow-ups: "Last week you mentioned your headaches were improving after starting the new prescription. How are you feeling now?" Without memory, the same assistant would ask "What brings you in today?" every single time — useful for a first visit, alienating by the fifth.

### The Privacy Tension

Memory creates a fundamental tension between personalization and privacy. The more the system remembers, the more useful it becomes — and the more sensitive the stored data. A memory system that knows your medical history, financial situation, relationship status, and work context is extraordinarily useful. It is also extraordinarily dangerous if compromised.

Builders implementing memory systems must address:

| Concern | Mitigation |
|---|---|
| What is stored? | Explicit memory policy — users can view and delete any memory |
| Who has access? | Encryption at rest, access controls, audit logs |
| How long is it kept? | Retention policies with automatic expiration |
| Can it be exported? | Data portability — users can download their memory |
| Can it be erased? | True deletion, not soft delete, when requested |

> **ANALOGY**: Memory in AI systems is like a personal assistant's notebook. A good assistant keeps useful notes — "prefers window seats," "allergic to shellfish," "meeting with investors on Thursday." A good assistant also knows what not to write down, keeps the notebook secure, and shreds it when the relationship ends. Building memory into AI without building privacy controls is like giving your assistant an excellent memory and zero discretion.

---

## The Agentic Operating System

In Chapter 19, we covered Claude Code — an AI that can read files, write code, run commands, and operate within your development environment. This is the early form of something much larger: **the agentic operating system**, where AI agents are the primary interface for computer interaction.

### Claude Computer Use

Anthropic's **Computer Use** capability, released in late 2024 and refined throughout 2025, allows Claude to operate a computer the way a human does — moving the mouse, clicking buttons, typing text, reading the screen. It can fill out forms, navigate websites, use desktop applications, and complete multi-step workflows that span multiple applications.

```
Agentic OS — The Interaction Shift:

  Traditional OS:
  ┌──────────────────────────────────────────────┐
  │  Human → Mouse/Keyboard → Application → Task  │
  │                                                │
  │  "File → Export → PDF → Choose location →      │
  │   Name file → Click Save"                      │
  │                                                │
  │  Each step requires human attention and input   │
  └──────────────────────────────────────────────┘

  Agentic OS:
  ┌──────────────────────────────────────────────┐
  │  Human → Natural Language → Agent → Task       │
  │                                                │
  │  "Export this document as PDF to the            │
  │   shared drive"                                 │
  │                                                │
  │  Agent handles all GUI steps autonomously       │
  └──────────────────────────────────────────────┘
```

The implications extend beyond convenience:

- **Accessibility**: People who cannot use a mouse or keyboard can operate any application through voice or text.
- **Automation**: Any workflow that can be demonstrated can be automated. Show the agent how to do it once; it repeats the process.
- **Legacy system integration**: AI agents can interact with old software that has no API — filling forms, clicking buttons, reading screens — bridging the gap between modern AI and legacy interfaces.

### Apple + Claude in Xcode

In 2025, Apple announced the integration of Claude into Xcode, Apple's development environment for iOS and macOS applications. This represents the first time a major platform vendor has embedded a frontier AI model directly into their primary developer tool.

The integration goes beyond autocomplete. Claude in Xcode can:

- Read the entire project structure and understand the app's architecture
- Generate new SwiftUI views based on natural language descriptions
- Debug crashes by reading stack traces and suggesting fixes
- Refactor code across multiple files while maintaining consistency
- Explain Apple-specific APIs and design patterns

For builders, this signals a broader trend: AI is becoming a native part of the development environment, not a separate tool you switch to. The future is not "use your IDE, then switch to Claude." The future is "Claude is in your IDE."

---

## The Open Source Tide

The history of technology follows a pattern: proprietary innovation leads, open source follows, and eventually open source becomes the default infrastructure. It happened with operating systems (Unix → Linux). It happened with web servers (proprietary → Apache/Nginx). It happened with databases (Oracle → PostgreSQL/MySQL). It is happening with AI.

```
The Open Source AI Timeline:

  2023: Llama 2 (Meta) — first competitive open-source LLM
  2024: Mistral, Mixtral — European open-source challenger
  2024: DeepSeek V2/V3 — Chinese open-source, competitive pricing
  2025: DeepSeek R1 — open-source reasoning, matches o3
  2025: Llama 3.1 405B — open-source approaches frontier
  2025: Qwen 2.5 — Alibaba's open-source family
  2026: Multiple open-source models within ~5% of frontier
        on most benchmarks

  The gap between best open-source and best proprietary
  has narrowed from ~30% (2023) to ~5-10% (2026) on
  standard benchmarks.
```

What this means for builders:

1. **Cost floor is dropping**: Running open-source models on your own infrastructure (or through cheap API providers like Together AI, Fireworks, and Groq) costs a fraction of frontier API pricing. For high-volume applications, this can reduce AI costs by 80-95%.

2. **Data sovereignty**: Open-source models can run on your infrastructure, in your region, under your control. No data leaves your systems. For regulated industries (healthcare, finance, government), this is often a requirement, not a preference.

3. **Customizability**: You can fine-tune open-source models on your data, modify their behavior, and deploy custom variants. You cannot do this with proprietary APIs (beyond prompt engineering).

4. **Vendor independence**: If your product depends entirely on one provider's API, you have a single point of failure — price increases, service outages, capability changes, or policy changes can break your product overnight. Open-source models eliminate this dependency.

> **INTUITION**: The question is no longer "should I use open-source AI?" but "for which components should I use open-source, and for which should I use proprietary?" The compound systems architecture from Chapter 30 provides the answer: use proprietary frontier models for the hardest tasks (complex reasoning, creative generation) and open-source models for everything else (classification, extraction, summarization, embedding). This gives you the best quality where it matters and the lowest cost everywhere else.

---

## The Regulatory Horizon

AI regulation is arriving. It will affect what you can build, how you build it, and who you can build it for.

### The Current Landscape

| Region | Regulation | Status | Key Requirement |
|---|---|---|---|
| **EU** | AI Act | Enforceable from Feb 2025 | Risk-based classification; high-risk AI (healthcare, hiring, law enforcement) requires conformity assessments, documentation, and human oversight |
| **US** | Executive Order on AI (Biden, 2023) + state-level laws | Fragmented | No comprehensive federal law; Colorado, California, Illinois have specific AI laws |
| **India** | Digital India Act (proposed) | In progress | Likely to require disclosure when AI is used in decision-making |
| **China** | Multiple regulations (deepfakes, generative AI, algorithms) | Active enforcement | Requires government approval for public-facing AI services |

### What Builders Need to Know

1. **Disclosure**: Increasingly, you must tell users when they're interacting with AI. An AI customer support bot that pretends to be human is already illegal in several jurisdictions.

2. **Explainability**: For high-risk applications (credit decisions, hiring, medical diagnosis), you may need to explain why the AI made a specific decision. "The model said so" is not sufficient. This has architectural implications — you need audit trails, reasoning traces, and the ability to reconstruct the decision path.

3. **Bias testing**: If your AI system makes decisions about people, you'll need to test for demographic bias. Does the system treat users differently based on gender, race, age, or location? Automated bias testing (related to the automated red-teaming in Chapter 33) will become a standard part of the deployment pipeline.

4. **Data handling**: Where does user data go? Is it used to train models? Can users opt out? GDPR (Europe), DPDP Act (India), and similar regulations worldwide impose specific requirements on how AI systems handle personal data.

> **REAL-LIFE**: In 2024, an AI hiring tool used by a major European company was found to systematically score female candidates lower for technical roles. The company faced regulatory action under the EU AI Act's high-risk provisions. The fix required not changing the model — but implementing the bias testing and human oversight procedures that the regulation mandated. The lesson: regulation doesn't prevent you from building AI. It requires you to build it carefully and prove that you've done so.

---

## Jobs, Skills, and the Builder's Advantage

"Will AI take my job?" is the wrong question. The right question is: "Which parts of my job will AI automate, and what new capabilities does this give me?"

### The Emerging Roles

```
Jobs That AI Creates or Transforms:

  ENTIRELY NEW ROLES:
  ├── AI Product Manager — defines what AI features to build and how
  ├── Prompt Engineer → AI Systems Engineer — designs compound AI systems
  ├── AI Safety Engineer — red-teams, evaluates, and secures AI systems
  ├── AI Ethics Lead — ensures AI systems are fair, transparent, and accountable
  └── AI Operations (AIOps) — monitors, maintains, and optimizes AI in production

  TRANSFORMED ROLES:
  ├── Software Engineer → 2-5x more productive with AI tools
  ├── Data Analyst → focuses on insight and strategy, AI handles data prep
  ├── Designer → AI generates variants, human curates and refines
  ├── Product Manager → AI handles research and analysis, PM focuses on strategy
  └── Customer Support → AI handles routine, humans handle complex and emotional

  AT RISK (routine, pattern-based):
  ├── Manual data entry and processing
  ├── Basic code writing without design or architecture
  ├── Template-based content creation
  ├── First-line customer support (simple queries)
  └── Manual testing of repetitive scenarios
```

The pattern across all of these: **AI handles the repetitive execution. Humans handle the judgment, creativity, and relationship.**

> **ANALOGY**: Consider what happened when spreadsheets replaced manual accounting. Accountants didn't disappear. The role transformed. The tedious work (summing columns, cross-referencing ledgers) was automated. The valuable work (interpreting financial data, advising on strategy, catching fraud) was amplified. The accountants who adapted became more valuable. The ones who defined their identity as "the person who sums the columns" struggled. AI is the spreadsheet for knowledge work — and the lesson from history is the same: adapt the role, don't resist the tool.

### The Builder's Career Advantage

You — the person who has read this book, built projects, and developed fluency in AI tools — have a specific advantage. You are not threatened by AI because you are the person who builds with AI. You are the spreadsheet creator, not the column-summer.

The skills you've developed through this book are among the most valuable in the current and near-future job market:

| Skill | From Chapter | Market Value |
|---|---|---|
| Building full-stack applications | Part 1 | High — foundation of all software |
| Prompt engineering and LLM integration | Part 2 | Very High — every company needs this |
| AI-assisted development workflow | Part 3 | High — 2-5x productivity multiplier |
| System design with AI components | Part 4 | Very High — architectural thinking is rare |
| Compound AI systems | Ch. 30 | Extremely High — the next generation of AI products |
| Evaluation and safety | Ch. 28, 33 | High and growing — regulation is driving demand |

---

## Learning Roadmap: What to Study After This Book

This book gave you a foundation. What you build on it depends on the path you choose. Here are three paths — not mutually exclusive — with specific next steps for each:

### Path 1: The Product Manager / AI PM

You want to define what AI products should exist, for whom, and why. You think in terms of user problems, market opportunities, and business models.

```
AI Product Manager Learning Path:

  NEXT 3 MONTHS:
  ├── Build 2-3 AI features end-to-end (from user need to deployed product)
  ├── Study token economics deeply — cost per query, margins, unit economics
  ├── Read "Inspired" by Marty Cagan (product discovery)
  ├── Read "AI Product Management" by Marily Nika
  └── Practice: write PRDs for AI features with evaluation criteria

  NEXT 6 MONTHS:
  ├── Learn to design AI evaluation frameworks (Ch. 33 patterns)
  ├── Study A/B testing and experimentation platforms
  ├── Understand model selection tradeoffs (when to use what)
  └── Practice: ship an AI product to real users, measure retention

  NEXT 12 MONTHS:
  ├── Develop expertise in one AI vertical (healthcare, fintech, education)
  ├── Build a portfolio of shipped AI products with measurable outcomes
  └── Study AI regulation relevant to your vertical
```

### Path 2: The Engineer / AI Engineer

You want to build the systems. You think in terms of architecture, latency, reliability, and scale.

```
AI Engineer Learning Path:

  NEXT 3 MONTHS:
  ├── Master one LLM framework deeply (LangChain or LlamaIndex)
  ├── Build a production RAG system with evaluation
  ├── Learn vector databases (Pinecone, Weaviate, or pgvector)
  ├── Study DSPy for prompt optimization
  └── Practice: deploy a compound AI system handling 1000+ queries/day

  NEXT 6 MONTHS:
  ├── Learn fine-tuning (LoRA, QLoRA) for domain-specific models
  ├── Build an agent system with tool use and planning
  ├── Study inference optimization (quantization, batching, caching)
  └── Practice: reduce the cost of your deployed system by 50%+

  NEXT 12 MONTHS:
  ├── Contribute to an open-source AI project
  ├── Build expertise in one specialized area (voice AI, vision,
  │   multimodal, or reasoning systems)
  ├── Study distributed systems for AI inference at scale
  └── Practice: build a system that handles 100K+ queries/day reliably
```

### Path 3: The Founder / Builder

You want to create something new. You think in terms of problems worth solving, markets worth entering, and teams worth building.

```
Founder / Builder Learning Path:

  NEXT 3 MONTHS:
  ├── Identify a problem where AI creates 10x improvement (not 10%)
  ├── Build an MVP in 2-4 weeks using the tools from this book
  ├── Get 10 users. Not 10,000. Ten. Talk to each one.
  ├── Read "The Mom Test" by Rob Fitzpatrick (customer interviews)
  └── Practice: ship something, get feedback, iterate weekly

  NEXT 6 MONTHS:
  ├── Find product-market fit (users coming back without being asked)
  ├── Build the compound AI system that makes your product defensible
  ├── Study unit economics — can this be a business at scale?
  └── Practice: reach 100 active users with positive unit economics

  NEXT 12 MONTHS:
  ├── Scale what's working. Cut what's not.
  ├── Build a team (or decide to stay solo)
  ├── Study fundraising if needed (or profitability if bootstrapping)
  └── Practice: reach 1,000 active users or $10K MRR
```

---

## The Builder's Mindset

Technology changes. Tools change. Models change. Frameworks come and go. But the mindset that makes someone a successful builder — the disposition toward action, the comfort with uncertainty, the habit of learning by doing — is durable.

Here are the principles that will remain true regardless of what the next 12 months bring:

**Build first, optimize later.** A working prototype that's messy teaches you more than a perfect architecture diagram that was never implemented. Ship the rough version. Learn from real usage. Then improve.

**Learn the layer below.** Using an LLM API is a skill. Understanding how the model works (Chapter 10) is a deeper skill. When something breaks — and it will — the person who understands the layer below the abstraction is the person who can diagnose and fix it. You don't need to understand every layer. But always understand one layer below where you operate.

**Compound your knowledge.** Every project you build, every bug you fix, every paper you read, every tool you evaluate — these accumulate. A person who has built 10 projects understands software differently from a person who has built 1. The knowledge from Project 3 informs Project 7 in ways you cannot predict at Project 3. Keep building. The returns compound.

**Stay close to the problem.** Technology is a means, not an end. The best AI product in the world is worthless if it doesn't solve a real problem for a real person. Talk to users. Watch them struggle. Build for their struggle, not for the elegance of the technology.

**Embrace the uncomfortable.** Every new technology feels uncomfortable at first. The terminal was uncomfortable. Git was uncomfortable. Docker was uncomfortable. AI tools are uncomfortable. The discomfort is the learning. It's the feeling of your mental model expanding to accommodate something new. People who run from the discomfort stop growing. People who lean into it become the builders who shape the next wave.

> **REAL-LIFE**: The builders who defined the previous technology waves — the people who built early websites, early mobile apps, early cloud infrastructure — did not wait for the technology to mature. They built while it was messy, unreliable, and confusing. They figured it out by doing. They shipped imperfect versions and improved them. They made mistakes and learned from them. And by the time the technology became mainstream, they had years of hard-won expertise that no tutorial could replicate.

You are at that same inflection point with AI. The technology is messy, unreliable, and confusing. It is also the most powerful tool for building software that has ever existed. The builders who start now — who build with AI, not wait for it to be perfect — will define the next decade of technology.

This book gave you the foundation. The rest is up to you.

Build.

<div class="exercise">
<div class="exercise-title">Try It Yourself</div>

1. **Choose your path**: Based on the three learning paths (PM, Engineer, Founder), identify which resonates most with where you want to be in 12 months. Write down three specific things you will do in the next 30 days to start on that path. Put them in your calendar. Not "I'll learn about RAG." Instead: "Saturday 10am-12pm: Build a RAG system that answers questions about my company's documentation."

2. **Build your horizon scanner**: Set up a system for tracking the technologies mentioned in this chapter. Create an Obsidian note (or any note) with sections for: Video AI, Memory/Personalization, Agentic OS, Open Source Models, Regulation. Once a month, spend 30 minutes updating it with the latest developments. This is your early warning system for changes that affect what you build.

3. **The 12-month project**: Define a project that you will work on over the next 12 months. Not a weekend project — a sustained effort that will push you beyond your current skill level. The best learning happens at the edge of your competence. What would you build if you had twice the skill you have today? Start building it. The skill will come from the building.

4. **Teach one thing**: Take a concept from this book that you found particularly enlightening and explain it to someone who hasn't read the book. Write a blog post. Record a video. Give a talk at a local meetup. Explain it to a colleague over coffee. Teaching is the final level of understanding. If you can explain it clearly, you own it.

5. **The 30-day challenge**: For the next 30 days, build something with AI every day. It doesn't have to be big. A prompt experiment. A small automation. A feature prototype. A tool evaluation. The only rule: every day, you must produce something tangible — a working script, a deployed feature, a written analysis, a test result. By day 30, you will have 30 artifacts of learning and a dramatically expanded comfort zone with AI tools.

</div>

---

**Chapter endnotes**

[1] Sora, OpenAI's text-to-video model, was first demonstrated in February 2024 and launched publicly in December 2024. Quality and capability details based on public demonstrations and the technical report. Video AI capabilities are evolving rapidly — specific quality assessments reflect the state of the technology as of early 2026.

[2] Runway's Gen-3 Alpha model and subsequent versions have been the primary commercial video generation tool for creative professionals since 2024. Details from Runway's public documentation and product updates.

[3] ChatGPT Memory feature launched in early 2024, with the ability to remember user preferences and facts across conversations. Implementation details based on OpenAI's public documentation and observed behavior.

[4] Mem0 (mem0.ai) is an open-source memory layer for AI applications. The architecture described is based on their public documentation and GitHub repository.

[5] Claude Computer Use was introduced by Anthropic in October 2024 as a beta feature, with Claude able to view a computer screen, move the cursor, click, and type. By 2025, the capability had been refined for use in production automation workflows.

[6] Apple's integration of Claude into Xcode was announced at WWDC 2025. The integration represents the first time a major platform vendor embedded a frontier AI model directly into their primary developer IDE, signaling a broader trend of AI-native development environments.

[7] EU AI Act: formally adopted in March 2024, with enforcement beginning in February 2025 for prohibited practices and full enforcement of high-risk provisions by August 2026. The risk-based classification system categorizes AI applications into four risk levels with corresponding regulatory requirements.

[8] DeepSeek R1 open-source release (January 2025) and subsequent open-source model developments demonstrate the narrowing gap between open-source and proprietary AI capabilities. Model comparison data from public benchmarks and independent evaluations.

[9] The "spreadsheet analogy" for AI's impact on knowledge work draws on historical analysis of how previous automation technologies (ATMs, spreadsheets, industrial robots) transformed rather than eliminated the roles they affected. See Autor, "Why Are There Still So Many Jobs?" (Journal of Economic Perspectives, 2015).