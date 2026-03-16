<span class="chapter-number">Chapter 8</span>

# Software Architecture — How Big Systems Are Organized {.chapter-title}

You've now seen how individual pieces of software work — frontend, backend, databases, APIs, caching. Each is a tool. But when you're building something the size of Zomato or Uber, the question isn't "what tools do I use?" It's "how do I organize all these tools so that 500 engineers can work on them without stepping on each other's toes?"

That question is **software architecture** (the overall structure and organization of a software system — which parts exist, what each part does, and how they communicate).

Architecture is the decision that's hardest to change later. Pick the wrong database? You can migrate. Write bad code? You can refactor. Choose the wrong architecture? That's like realizing you should have built an apartment complex after you've finished the single-family home. The walls are wrong. The plumbing runs through the wrong floors. Everything works — but it resists every change you want to make next.

## One Kitchen or Many? The Core Tradeoff

> **ANALOGY**: Imagine a restaurant with one kitchen. Five cooks, everything in the same room. The dessert chef needs cream? She walks three steps. Coordination is effortless.
>
> Now the restaurant becomes wildly popular. Five cooks become 80. The kitchen is chaos. Someone changing the oven temperature for bread is ruining the roast. Every change requires shouting across the room.
>
> Option one: build a food court. Each cuisine gets its own stall, kitchen, and staff. The pizza stall upgrades its oven without affecting the sushi bar — but if a customer orders both, someone must coordinate between stalls.
>
> Option two: keep one building, but build walls *inside* the kitchen. Bread section, grill section, dessert section — each has its own workspace, but they share the building and the dishwasher. Clear boundaries, shared infrastructure.

These three options map directly to the three major architectural patterns in software:

1. **Monolith** — one application, one codebase, one deployment. The single-kitchen restaurant.
2. **Microservices** — many small, independent services, each doing one thing. The food court.
3. **Modular monolith** — one application with strict internal boundaries between modules. The kitchen with walls.

Let's look at each.

## The Monolith: Everything in One Place

A **monolith** (from the Greek *monolithos*, meaning "single stone") is an application where all the code lives in one place and runs as a single program. Authentication, payments, notifications, search — it all lives in the same project, gets deployed together, and shares one database.

> **REAL-LIFE**: When Instagram launched in 2010, it was a monolith. Two engineers, one codebase, one server. By 2012, when Facebook acquired it for $1 billion, it was still a monolith — one of the world's most popular apps running on a single Django codebase with 13 engineers.

Here's what makes monoliths attractive:

- **Function calls, not network calls.** If orders needs to check a user's payment method, it calls a function. Microseconds, not milliseconds. No retry logic needed.
- **One codebase to search.** Trace a bug from the API endpoint to the database query in one editor.
- **One thing to deploy.** Build, test, ship. No coordinating releases across 15 services.
- **One database to query.** A report joining users, orders, and payments? One SQL query.

> **INTUITION**: The monolith gets blamed for problems that are actually *organizational*. When a monolith becomes painful, it's usually because 40 engineers are changing code in the same repository without clear ownership. The architecture didn't fail — the team structure outgrew it.

### When Monoliths Break Down

The pain arrives when the team grows. Specifically:

- **Deploy conflicts**: Engineer A wants to ship a new feature, but Engineer B's half-finished code is in the same codebase. They have to coordinate.
- **Blast radius**: A bug in the notification module crashes the entire application — including checkout, search, and everything else.
- **Scaling mismatches**: The search feature gets 100x more traffic than the settings page, but you can only scale the entire application as one unit. You're paying for 100x capacity on code that doesn't need it.
- **Build times**: The codebase grows so large that running the test suite takes 45 minutes. Engineers start skipping tests.

These are real problems — but problems of *scale*, not of the architecture itself. A team of 8 with 50,000 users will likely never hit them.

## Microservices: The Food Court Model

**Microservices** (an architecture where an application is built as a collection of small, independent services, each running its own process and communicating over the network) emerged to solve these scaling problems. Instead of one application, you split the system into many small services. Each owns one capability, has its own codebase and database, can be deployed independently, and communicates over the network via HTTP or messaging queues.

> **REAL-LIFE**: Netflix runs over 1,000 microservices. When you press play, the request touches dozens: one finds the content, another checks your subscription, another picks the optimal video encoding for your internet speed, another logs the event for recommendations. Each is deployed by a separate team. One team can update the recommendation engine without touching the video player.

> **INTUITION**: Microservices didn't emerge from a whiteboard. They emerged from organizational reality. Amazon discovered in the early 2000s that their monolith was slowing them down — not technically, but *humanly*. Jeff Bezos mandated that every team must communicate through APIs (the "API Mandate"), and that no team should be larger than what two pizzas could feed. The architecture followed the team structure. This observation has a name: **Conway's Law** — organizations design systems that mirror their own communication structure.

### The Hidden Costs of Microservices

Microservices solve the scaling problem, but they create an entirely different category of problems:

- **Network calls replace function calls.** A 1-microsecond function call becomes a 5-millisecond network request — 5,000x slower. Network calls can *fail*. You need retry logic, timeouts, and circuit breakers for every interaction.
- **Distributed debugging.** Checkout is slow — is the problem in the API gateway, cart service, inventory service, or payment service? Tracing one request across 8 services requires specialized **distributed tracing** tools like Jaeger or Zipkin.
- **Data consistency.** In a monolith, a database transaction deducts inventory *and* charges payment atomically — if either fails, both roll back. Across microservices with separate databases, you need **eventual consistency** (where different parts may briefly show different data, converging over time).
- **Operational overhead.** Instead of deploying one application, you're deploying 50. Each needs health checks, logging, CI/CD, and on-call rotation.

Sam Newman, in *Building Microservices*, puts it directly: "Microservices buy you options. Options have a cost." If your team is 6 engineers, they're now spending 40% of their time on infrastructure instead of features.

## The Visual Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                         MONOLITH                                │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │   Auth   │ │  Orders  │ │  Search  │ │ Payments │          │
│  │  Module  │ │  Module  │ │  Module  │ │  Module  │          │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘          │
│       │             │            │             │                 │
│       └─────────────┴────────────┴─────────────┘                │
│                         │                                       │
│                ┌────────┴────────┐                              │
│                │  ONE DATABASE   │                              │
│                └─────────────────┘                              │
│                                                                 │
│  Deploy: Everything together    Scale: Everything together      │
│  Debug: One codebase            Team: Shared ownership          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       MICROSERVICES                             │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   Auth   │  │  Orders  │  │  Search  │  │ Payments │       │
│  │ Service  │  │ Service  │  │ Service  │  │ Service  │       │
│  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤       │
│  │  Own DB  │  │  Own DB  │  │  Own DB  │  │  Own DB  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │              │             │              │              │
│       └──── Network Calls (HTTP / Message Queue) ┘              │
│                                                                 │
│  Deploy: Each independently     Scale: Each independently       │
│  Debug: Distributed tracing     Team: Owned by separate teams   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     MODULAR MONOLITH                            │
│                                                                 │
│  ┌─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐    │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │    │
│  │ │   Auth   │ │  Orders  │ │  Search  │ │ Payments │  │    │
│  │ │  Module  │ │  Module  │ │  Module  │ │  Module  │  │    │
│  │ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │    │
│  │      ▲             ▲            ▲            ▲        │    │
│  │      │    Public APIs only (no direct DB access)      │    │
│  │      ▼             ▼            ▼            ▼        │    │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │    │
│  │ │ Own      │ │ Own      │ │ Own      │ │ Own      │  │    │
│  │ │ Schema   │ │ Schema   │ │ Schema   │ │ Schema   │  │    │
│  │ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │    │
│  └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘    │
│                         │                                       │
│                ┌────────┴────────┐                              │
│                │  ONE DATABASE   │                              │
│                │ (shared, but    │                              │
│                │  schema-per-    │                              │
│                │  module)        │                              │
│                └─────────────────┘                              │
│                                                                 │
│  Deploy: Together (simpler)     Scale: Together (for now)       │
│  Debug: One codebase            Team: Clear module ownership    │
│  Boundaries enforced at code level, not network level           │
└─────────────────────────────────────────────────────────────────┘
```

The key difference: the modular monolith has the *boundaries* of microservices but the *simplicity* of a monolith. Modules communicate through defined interfaces, not by reaching into each other's code — but they share a database, a deployment, and a process. Walls inside the kitchen, not between separate buildings.

## The Modular Monolith: Shopify's Middle Ground

This is the pattern that deserves more attention than it gets.

> **ANALOGY**: Microservices says: put accounting, marketing, and engineering in separate buildings — they communicate by email. Monolith says: everyone in one open-plan room. Modular monolith says: one building, each department gets its own floor with a receptionist. Want something from accounting? Go to the 3rd floor and make a request. You don't walk in and rifle through their filing cabinets.

**Shopify** is the most prominent example — one of the largest e-commerce platforms in the world, processing billions in transactions, running on a single Ruby on Rails monolith.

But not a *messy* monolith. Starting around 2019, Shopify restructured into **components** — self-contained modules with explicit boundaries. Each component:

- Defines a public interface (a set of functions that other modules can call)
- Hides its internal implementation (other modules cannot access its database tables or internal classes)
- Is owned by a specific team
- Can be tested in isolation

The result? Team-ownership benefits without the network-call tax, distributed debugging, or operational overhead.

> **REAL-LIFE**: DHH (creator of Ruby on Rails, CTO of 37signals) wrote "The Majestic Monolith" in 2016, arguing that even successful companies with millions of users are better served by a well-structured monolith. 37signals runs Basecamp and HEY as monoliths. His 2024 follow-up, "The Majestic Monolith Can Become The Citadel," introduced pulling out a few critical services while keeping the core intact. Not a food court — a castle with a few outposts.

The modular monolith answers a question the monolith-vs-microservices debate ignores: **what does a team of 15-50 engineers actually need?** Clear ownership. The ability to work on their module without coordinating deploys. Confidence that changing payment code won't break search. The modular monolith delivers all three — without the tax.

## Event-Driven Architecture: The Newspaper Model

So far, we've assumed services communicate by *calling* each other directly — **synchronous communication**, where one service asks another to do something and waits for the answer. There's another way.

> **ANALOGY**: A village with no telephones. To share news, you walk to someone's house and knock. Works with 5 houses. But what if 100 people need to know the wheat price changed? Do you knock on 100 doors?
>
> The alternative: a newspaper. Publish once, everyone who cares subscribes. The farmer publishes "wheat price: ₹2,400/quintal." The baker, distributor, and restaurant each read it and decide what to do. The farmer doesn't need to know who reads it. He published. His job is done.

This is **event-driven architecture** (a design pattern where parts of a system communicate by publishing and reacting to events — records of something that happened — rather than calling each other directly).

In technical terms: a service *publishes* an **event** (a record of something that happened: "Order #4821 was placed"). The event goes to a **message broker** (a system like Kafka or RabbitMQ that receives, stores, and delivers events) — the printing press. Other services *subscribe* to events they care about and react accordingly.

When an order is placed on Amazon, the order service publishes one event: "Order Placed." The warehouse subscribes and starts picking. The email service subscribes and sends confirmation. The analytics service subscribes and updates dashboards. None of them know about each other.

> **INTUITION**: Event-driven architecture creates **loose coupling** — parts of the system don't need to know about each other. Adding a new subscriber (say, fraud detection) requires zero changes to the order service.

The tradeoff? Debugging. In a synchronous system, you follow the chain: A called B called C, C failed. In an event-driven system, the event was published, five services consumed it, and the failure could be in any of them. The flow is harder to trace.

## Technical Debt: The Credit Card of Engineering

Before we get to the decision framework, there's one architecture concept that every PM encounters weekly: **technical debt**.

> **ANALOGY**: Technical debt works like credit card debt. When you use a credit card, you get something now and pay later — with interest. When an engineer takes a shortcut (hardcodes a value instead of making it configurable, copies-and-pastes code instead of creating a reusable function, skips writing tests), they ship faster now but pay later. The "interest" is the extra time every future change takes because of the shortcut. And like credit card debt, if you keep borrowing without paying it down, the interest payments eventually consume your entire budget.

The term was coined by **Ward Cunningham** (who also invented the wiki) in 1992, deliberately as a financial metaphor so business stakeholders could understand why engineers sometimes need to stop building features and fix old code.

Technical debt is not inherently bad. A startup racing to find product-market fit *should* take shortcuts — the building might get torn down anyway. But the debt needs to be *conscious*. The danger isn't taking on debt; it's taking it on by accident, or pretending it doesn't exist.

Three types: **Deliberate, prudent** — "This won't scale past 10,000 users, but we have 200 and need to ship this week." A legitimate business decision. **Deliberate, reckless** — "We don't have time for tests." Compounds aggressively. **Accidental** — "We didn't know there was a better approach." Inevitable; the fix is regular refactoring.

> **REAL-LIFE**: In 2020, the UK's HMRC (tax authority) estimated they were spending over 1 billion pounds per year maintaining legacy systems weighed down by technical debt. The interest payments had exceeded the cost of building new systems.

As a PM, your role is to ensure technical debt has a line item — not to eliminate it, but to make it visible. Every sprint should allocate *some* capacity to paying down debt.

## The Decision Framework

The table you'll reference in planning meetings:

```
              MONOLITH          MODULAR MONOLITH     MICROSERVICES
─────────────────────────────────────────────────────────────────────
Team size     1–15              10–80                40+
Stage         Pre-PMF           Scaling, post-PMF    Large-scale org
Deploy        Fast (one unit)   Fast (one unit)      Per-service fast
Scaling       Vertical          Vertical             Horizontal
Debugging     Easy              Easy                 Hard (tracing)
Data joins    Trivial           Possible             Expensive
Blast radius  Full app          Module scope         One service
Infra cost    Low               Low                  High
Best for      MVPs, startups    Growing companies    Netflix-scale
Examples      Basecamp, HEY     Shopify, Gusto       Netflix, Uber
```

**The rule of thumb**: Start monolith. When pain arrives, evolve to modular monolith. Only move to microservices when you have the team size and operational maturity to pay the tax. Martin Fowler calls this **MonolithFirst**: "Almost all the successful microservice stories have started with a monolith that got too big and was broken up."

Three questions to test your choice:

1. **Can one team hold the system in their head?** → Monolith.
2. **Do different parts change at different speeds, owned by different teams?** → Modular monolith.
3. **Do parts need to scale independently and deploy on different schedules?** → Microservices.

Most startups answering "yes" to question 3 are wrong. They're solving a problem they don't have yet.

## What This Means for Product Managers

You will not choose your company's architecture. But you will live with its consequences daily:

- **Sprint planning**: In a monolith, features touch shared code — more coordination. In microservices, team A ships without waiting for team B.
- **Incident response**: Monolith — one bad deploy breaks everything. Microservices — one bad deploy breaks one service, but finding *which* service is harder.
- **Feature scoping**: In a modular monolith, features crossing module boundaries require negotiation between module owners.
- **Technical debt**: When engineers say "we need to refactor," they often mean "the architecture is resisting where the product is going." Your job: quantify the cost of *not* refactoring.

The best architects understand the product roadmap. The best PMs understand the architecture. This chapter gives you the vocabulary for that conversation.

<div class="exercise">
<div class="exercise-title">Try It Yourself</div>

Pick a product you use daily — Spotify, Notion, Swiggy, anything. Answer three questions:

1. **What are the major domains?** (e.g., Spotify: catalog, playback, recommendations, social, payments)
2. **Which domains change at different speeds?** (Payments: rarely. Recommendations: weekly.)
3. **What architecture would you recommend from scratch today?** What about at their current scale?

Write your answers down. Compare with a technical friend or your AI tool. The exercise isn't about getting it "right" — it's about building the muscle of thinking in systems.

Bonus: Ask Claude Code: "If I were building a Spotify competitor with a team of 8, what architecture would you recommend and why?" Compare its answer with this chapter's framework.

</div>

---

**Chapter endnotes**

[1] Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2nd Edition (O'Reilly, 2021). The definitive reference. Chapters 1 and 3 are most relevant to the patterns here.

[2] David Heinemeier Hansson, "The Majestic Monolith" (Signal v. Noise, 2016) and "The Majestic Monolith Can Become The Citadel" (2024). The most influential counterargument to microservices-by-default thinking.

[3] Martin Fowler, "MonolithFirst" (martinfowler.com, 2015). Start with a monolith and extract services only when you understand domain boundaries — getting service boundaries wrong is far costlier than getting module boundaries wrong.

[4] Ward Cunningham coined "technical debt" in a 1992 OOPSLA report. His original framing was more nuanced than common usage — he meant the gap between your understanding of the problem and the code's representation of it, not shortcuts due to laziness.

[5] Shopify's modular monolith journey is documented in Kirsten Westeinde's "Deconstructing the Monolith" talk (ShopifyEngineering, 2019). They use a Ruby gem called `packwerk` to enforce module boundaries at development time.

[6] Conway's Law was articulated by Melvin Conway in 1967. The "Inverse Conway Maneuver," popularized by ThoughtWorks, suggests structuring teams to produce the architecture you want.

[7] Amazon's "two-pizza teams" and the Bezos API Mandate (circa 2002) are described in Steve Yegge's "Google Platforms Rant" (2011). The mandate required all teams to expose functionality through service interfaces — laying groundwork for Amazon's microservices and, eventually, AWS.
