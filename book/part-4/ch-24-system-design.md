<span class="chapter-number">Chapter 24</span>

# System Design — Thinking at Scale {.chapter-title}

Your app works. It handles 100 users, responds in under a second, and the database never breaks a sweat. Then you land on Product Hunt. Or a celebrity tweets your link. Or your marketing team's campaign actually works for once. Suddenly 100 users becomes 100,000. Requests that took 200 milliseconds now take 12 seconds. The database connection pool is exhausted. Users see error pages. Your Slack channel fills with screenshots of spinning loaders.

This is not a code quality problem. This is a **system design** problem — the discipline of structuring your infrastructure (servers, databases, networks, and the connections between them) so that your application performs reliably as usage grows from hundreds to millions.

System design is the difference between a product that handles success and a product that collapses under it.

## Lemonade Stand vs. Restaurant Chain

> **ANALOGY**: You run a lemonade stand. One table, one pitcher, one cashier — you. A customer walks up, you pour the lemonade, take the money, hand them the cup. It works beautifully because there's only one customer at a time.
>
> Now imagine your lemonade is so good that you open 200 locations across the country. You need supply chains for lemons. Hiring systems. A way to ensure the lemonade tastes the same in Chennai as it does in Chandigarh. Payment processing that doesn't fail if one location's internet goes down. A central inventory system that knows when a location is running low.
>
> The lemonade recipe didn't change. But the *system around the lemonade* had to be completely reinvented.

> **REAL-LIFE**: WhatsApp handled 100 billion messages per day in 2024 with roughly 50 engineers. Instagram reached a billion users with a monolithic Django application before refactoring. Neither team started with the architecture they ended up with. They evolved their systems as their scale demanded it — and the ability to make those evolution decisions at the right time is what system design knowledge gives you.

> **INTUITION**: System design is not about building for a billion users on day one. It's about understanding *which bottleneck will break first* as you grow, and knowing the standard solutions to each. Every system has a bottleneck. System design is the practice of identifying it before your users do.

## Load Balancing: Distributing the Weight

When your application runs on a single server, every request hits that one machine. At some point, that machine runs out of CPU, memory, or network bandwidth. The answer is to add more servers — but then you need something to decide which server handles which request.

That something is a **load balancer** (a system that sits in front of multiple servers and distributes incoming requests across them so no single server is overwhelmed).

> **ANALOGY**: Picture a grocery store during Diwali. One cash register, 200 people in line. Chaos. Now open 8 registers and hire a floor manager who directs each customer to the register with the shortest line. That floor manager is your load balancer.

```
                    ┌──────────┐
                    │  Users   │
                    └────┬─────┘
                         │
                         ▼
                ┌─────────────────┐
                │  LOAD BALANCER  │
                │  (the manager)  │
                └───┬────┬────┬───┘
                    │    │    │
              ┌─────┘    │    └─────┐
              ▼          ▼          ▼
         ┌─────────┐ ┌─────────┐ ┌─────────┐
         │Server 1 │ │Server 2 │ │Server 3 │
         │ (busy)  │ │ (idle)  │ │ (busy)  │
         └─────────┘ └─────────┘ └─────────┘
```

### Load Balancing Strategies

Not every floor manager uses the same logic. The three most common strategies:

**Round-robin**: Send Request 1 to Server A, Request 2 to Server B, Request 3 to Server C, then back to Server A. Everyone gets equal turns. This works well when all servers are identical and all requests take roughly the same time. It fails when some requests are heavy (a complex search query vs. serving a static image) — one server gets stuck processing a monster request while others sit idle.

**Least-connections**: Always send the next request to whichever server is currently handling the fewest active requests. This adapts to reality — if Server C is processing a slow database query, new requests flow to Servers A and B. More intelligent than round-robin, slightly more overhead to track connection counts.

**Weighted**: Assign servers different capacities. If Server A has 64GB of RAM and Server B has 16GB, Server A gets 4x the traffic. This reflects the real world — your fleet of servers is rarely identical, especially in cloud environments where you mix instance types.

| Strategy | Best for | Weakness |
|---|---|---|
| Round-robin | Identical servers, uniform requests | Ignores actual server load |
| Least-connections | Mixed workloads, variable request times | Slightly more overhead |
| Weighted | Mixed hardware, different server capacities | Requires manual configuration |

> **REAL-LIFE**: AWS Elastic Load Balancer, Nginx, and HAProxy are the most widely used load balancers. Netflix uses a custom load balancer called Zuul that routes requests across thousands of microservice instances, factoring in server health, geographic proximity, and current load.

## Caching: The Sticky Note on the Fridge

Every time a user loads your homepage, the server queries the database, assembles the HTML, and sends it back. If 10,000 users load the homepage in the same minute, that's 10,000 identical database queries returning identical results. Your database is doing the same work 10,000 times.

**Caching** (storing the result of an expensive computation so you can reuse it instead of recomputing) eliminates this waste.

> **ANALOGY**: Your partner asks you what time the dentist appointment is. You check the calendar app, scroll through three months, find it — Tuesday at 3 PM. An hour later, they ask again. Do you re-open the calendar and scroll through three months? No. You remember: "Tuesday at 3 PM." That remembered answer is a cache.
>
> Now imagine sticking a Post-it note on the fridge: "Dentist: Tue 3 PM." Anyone in the family who needs the answer reads the Post-it instead of checking the calendar. That Post-it is **Redis** (an in-memory data store — a database that lives entirely in RAM, making reads 100x faster than disk-based databases).

```
  WITHOUT CACHE:                    WITH CACHE:

  User Request                      User Request
       │                                 │
       ▼                                 ▼
  ┌─────────┐                      ┌─────────┐
  │  Server  │                      │  Server  │
  └────┬─────┘                      └────┬─────┘
       │                                 │
       │ 50ms                            │ Check cache
       ▼                                 ▼
  ┌──────────┐                     ┌──────────┐
  │ Database │                      │  Redis   │──── HIT? Return (0.5ms)
  └──────────┘                      └────┬─────┘
                                         │ MISS?
  Total: 50ms per request                ▼
  10K requests = 10K × 50ms        ┌──────────┐
                                   │ Database │
                                   └──────────┘
                                   Store result in Redis

                                   Total: 0.5ms for 9,990 requests
                                          50ms for 10 cache misses
```

The numbers are dramatic. A typical database query takes 5-50 milliseconds. A Redis lookup takes 0.1-0.5 milliseconds. For data that doesn't change frequently — a product catalog, a user's profile, a list of trending articles — caching delivers a 100x speed improvement and removes 99% of load from your database.

### The Cache Invalidation Problem

There's a famous saying in computer science, attributed to Phil Karlton: "There are only two hard things in Computer Science: cache invalidation and naming things."

**Cache invalidation** (deciding when to throw away cached data because the original data has changed) is genuinely difficult. If a user updates their profile name and the old name is cached, how long should other users see the stale name?

Common strategies:

- **Time-to-live (TTL)**: Cache expires after a set duration. Product catalog? Cache for 1 hour. User session? Cache for 15 minutes. Stock price? Cache for 5 seconds — or not at all.
- **Write-through**: Every time data is written to the database, the cache is updated simultaneously. Always fresh, but adds latency to writes.
- **Event-driven invalidation**: When a user updates their profile, publish an event that tells the cache to delete that entry. Fresh on next read, more complex to implement.

> **INTUITION**: Caching is a tradeoff between speed and freshness. The question is never "should we cache?" — it's "how stale can this data be before users notice or care?" For a social media feed, 30 seconds stale is fine. For a bank balance, zero seconds stale is the only acceptable answer.

## CDNs: Copies Everywhere

Your servers run in a data center in Virginia. A user in Mumbai makes a request. That request travels 13,000 kilometers across undersea fiber optic cables, through multiple network hops, to Virginia — then the response travels 13,000 kilometers back. Physics imposes a floor: the speed of light in fiber is about 200,000 km/s, so the round trip takes at minimum 130 milliseconds from physics alone, plus processing time.

A **CDN** (Content Delivery Network — a globally distributed network of servers that stores copies of your content at locations close to your users) solves this by moving the content closer.

> **ANALOGY**: Amazon doesn't ship every order from one warehouse in Seattle. They have fulfillment centers in every major city. When you order in Bengaluru, the package comes from a warehouse in Bengaluru — not from the United States. CDNs do this for digital content.

When you put your images, CSS, JavaScript, and video files on a CDN like Cloudflare, AWS CloudFront, or Akamai, copies are distributed to **edge servers** (CDN servers positioned in cities worldwide — the "edges" of the network). A user in Mumbai gets served from Mumbai. A user in London gets served from London.

The impact:

| Without CDN | With CDN |
|---|---|
| Every asset from Virginia | Assets from nearest edge server |
| 200-500ms latency for distant users | 10-50ms latency |
| Your server handles all traffic | CDN handles 70-90% of traffic |
| Single point of failure | 200+ points of presence |

> **REAL-LIFE**: Netflix stores its content library across a CDN called Open Connect, with servers physically installed inside ISPs (internet service providers) worldwide. When you stream a movie in India, the video data comes from a Netflix box sitting inside your ISP's data center — not from a Netflix server in the US. This is why Netflix can serve 250 million subscribers with consistent quality.

## Message Queues: The Kitchen Ticket System

A user clicks "Place Order" on a food delivery app. The system must: validate the order, charge the payment, notify the restaurant, assign a delivery partner, send a confirmation email, update analytics, and deduct loyalty points. If every step happens sequentially and synchronously (the user waits for each step to finish), the response takes 3-4 seconds. If the payment gateway is slow, it takes 10 seconds. If the email service is down, the entire order fails.

**Message queues** (systems that let one part of your application send a message to another part without waiting for it to be processed immediately) decouple these steps.

> **ANALOGY**: In a busy restaurant, the waiter doesn't walk into the kitchen and stand there watching the chef cook your meal. The waiter writes your order on a ticket, pins it to the queue rail above the kitchen counter, and goes back to take the next table's order. The kitchen works through tickets at its own pace. If 50 orders come in during a rush, the ticket rail absorbs the spike — the kitchen doesn't need to cook 50 meals simultaneously.
>
> The ticket rail is a message queue. The waiter is the **producer** (the part that creates messages). The kitchen is the **consumer** (the part that processes messages).

```
   ┌────────────┐     ┌─────────────────────┐     ┌──────────────┐
   │  Producer   │────▶│    MESSAGE QUEUE     │────▶│   Consumer   │
   │ (Order API) │     │                     │     │ (Email Svc)  │
   └────────────┘     │  ┌───┐ ┌───┐ ┌───┐  │     └──────────────┘
                       │  │ 3 │ │ 2 │ │ 1 │  │
                       │  └───┘ └───┘ └───┘  │     ┌──────────────┐
                       │                     │────▶│   Consumer   │
                       │  Messages waiting   │     │ (Analytics)  │
                       └─────────────────────┘     └──────────────┘
```

The two dominant message queue systems:

**RabbitMQ**: A traditional message broker (a system that receives messages from producers and routes them to consumers). Messages are delivered to consumers and then deleted. Good for task distribution — "process this payment," "send this email." Think of it as a postal service: each letter is delivered to one recipient.

**Apache Kafka**: A distributed event streaming platform where messages are persisted in an ordered log. Multiple consumers can read the same messages independently. Good for event-driven architectures where many systems care about the same event. Think of it as a newspaper: the article is published once, and anyone who wants to read it can, at any time. LinkedIn, where Kafka was created, processes over 7 trillion messages per day through it.

| Feature | RabbitMQ | Kafka |
|---|---|---|
| Model | Message broker (deliver and delete) | Event log (persist and replay) |
| Throughput | Thousands/second | Millions/second |
| Best for | Task queues, request-response | Event streaming, analytics pipelines |
| Complexity | Moderate | High |
| Used by | Robinhood, Reddit | LinkedIn, Uber, Netflix |

> **INTUITION**: The fundamental insight of message queues is that not everything needs to happen right now. The user needs to know their order was placed — but they don't need to wait for the confirmation email to be sent, the analytics to be logged, or the loyalty points to be calculated. Queues let you respond to the user immediately and handle the rest asynchronously (happening in the background, not blocking the user).

## Database Scaling: When One Database Isn't Enough

Your application's single PostgreSQL database handles 1,000 queries per second beautifully. Then growth pushes it to 10,000. Then 50,000. The database is doing two kinds of work: **reads** (SELECT queries — looking up data) and **writes** (INSERT, UPDATE, DELETE — changing data). In most applications, reads outnumber writes by 10:1 or more. People browse products far more than they buy them.

### Read Replicas

The first scaling technique: create copies of your database that handle read traffic.

> **ANALOGY**: A library has one master copy of every book. When 500 students need the same textbook, the library doesn't buy one copy and make everyone wait in line. It buys 10 copies. Any student can grab any copy — they all contain the same information. The master copy is where updates happen (a new edition arrives), and the copies get refreshed periodically.

A **read replica** (a copy of your database that stays synchronized with the primary and handles read-only queries) follows this principle. Writes go to the primary database. Reads are distributed across replicas. If you have 5 replicas, you can handle roughly 5x the read traffic.

The catch: there's a small delay — usually under a second — between a write to the primary and its appearance on the replica. This is called **replication lag**. For most applications, this is invisible. For a banking application showing your balance after a transfer, it's unacceptable.

### Sharding

Read replicas scale reads. But what about writes? If a single database can handle 5,000 writes per second and you need 50,000, replicas won't help — every write must go to the primary.

**Sharding** (splitting your database into multiple independent databases, each holding a portion of the data) distributes both reads and writes.

> **ANALOGY**: A city's voter records used to live in one filing cabinet at city hall. As the city grew to a million residents, one cabinet wasn't enough. So they split: A-F in Cabinet 1, G-L in Cabinet 2, M-R in Cabinet 3, S-Z in Cabinet 4. Each cabinet handles a quarter of the lookups and a quarter of the new registrations. That splitting strategy is a **shard key** (the rule that determines which shard holds which data).

Common shard keys:
- **User ID**: User 1-1M on Shard A, 1M-2M on Shard B. Keeps all of a user's data together.
- **Geographic region**: Indian users on Shard-India, US users on Shard-US. Reduces latency for region-specific queries.
- **Tenant** (in multi-tenant SaaS): Each customer's data lives on its own shard. Natural isolation.

Sharding is powerful but painful. Queries that span shards — "find all users who signed up last month" across 20 shards — become far more complex. Rebalancing shards when one grows too large requires careful data migration. This is why most teams exhaust every other optimization (caching, read replicas, query optimization, connection pooling) before resorting to sharding.

### Connection Pooling

Every database query requires a **connection** (a live channel between your application and the database). Creating a connection takes 20-50 milliseconds. If your server creates a new connection for every request, that's 20-50ms of pure overhead per query.

**Connection pooling** (maintaining a set of pre-established database connections that can be reused across requests) eliminates this overhead. Tools like PgBouncer for PostgreSQL keep 100 connections open and hand them to your application as needed. Request comes in, grabs a connection, runs the query, returns the connection to the pool. The next request reuses it.

This is one of those changes that costs an afternoon to implement and reduces database latency by 30-40% overnight.

## The CAP Theorem: You Can't Have Everything

In 2000, computer scientist **Eric Brewer** proposed what became known as the **CAP theorem**: in a distributed system (any system where data is stored on more than one machine), you can guarantee at most two of three properties simultaneously.

- **C — Consistency**: Every read returns the most recent write. If you deposit $100, the next read shows the updated balance — always.
- **A — Availability**: Every request receives a response, even if some servers are down.
- **P — Partition tolerance**: The system continues functioning even when network communication between servers is broken.

```
                         C
                      Consistency
                        /\
                       /  \
                      /    \
                     / CP   \
                    /  zone  \
                   /          \
                  /     CA     \
                 /    zone     \
                /   (no net     \
               /    partitions)  \
              /──────────────────\
             P                    A
         Partition            Availability
         Tolerance
              \                  /
               \    AP zone    /
                \             /
                 \           /
                  ───────────
```

> **ANALOGY**: You own three restaurants — one in Mumbai, one in Delhi, one in Bengaluru. Every restaurant must serve the same menu. When you change a dish in Mumbai, you call the other locations to update their menus.
>
> One night, a storm knocks out the phone lines between cities. Now you face a choice:
>
> - **Consistency + Partition tolerance (CP)**: You tell Delhi and Bengaluru to stop taking orders until the phone lines are restored, because they can't confirm they have the latest menu. No customers served, but you guarantee no one gets the wrong dish.
> - **Availability + Partition tolerance (AP)**: You tell all three restaurants to keep serving with whatever menu they currently have. Customers get served, but Mumbai might be selling a new dish that Delhi doesn't know about yet.
> - **Consistency + Availability (CA)**: This only works if the phone lines never go down — which you can't guarantee in the real world.

> **INTUITION**: Network partitions *will* happen. Hardware fails. Cables get cut. Cloud regions have outages. Since you can't avoid partitions, the real choice is between consistency (stop serving until you're sure everything is in sync) and availability (keep serving, accept that some data might be temporarily outdated).

In practice:

| System type | CAP choice | Why |
|---|---|---|
| Banks, financial systems | CP — Consistency | Showing the wrong balance is unacceptable. Better to be temporarily unavailable. |
| Social media feeds | AP — Availability | Seeing a post 2 seconds late is fine. A 503 error is not. |
| E-commerce inventory | Depends | Product listings: AP. Payment processing: CP. Different parts of the same system make different tradeoffs. |

> **REAL-LIFE**: Amazon's DynamoDB is an AP system — it prioritizes availability and accepts eventual consistency. Google's Spanner is a CP system — it uses atomic clocks to maintain global consistency, accepting the occasional availability dip. When you see a company's database choice, you're seeing their CAP tradeoff made concrete.

## Rate Limiting: The Velvet Rope

Your API is public. Without protection, a single misbehaving client — or an attacker — can send 100,000 requests per second and overwhelm your system. Every other user suffers.

**Rate limiting** (restricting the number of requests a client can make within a given time window) is the solution.

> **ANALOGY**: A nightclub has a velvet rope and a bouncer. The bouncer lets in 5 people per minute. If you've already entered three times tonight and the limit is two, the bouncer says, "Sorry, come back tomorrow." This protects the club's capacity for everyone — not a punishment for you specifically.

Common implementations:

- **Fixed window**: 100 requests per minute per user. Resets every minute on the clock. Weakness: a user can send 100 requests at 11:59:59 and another 100 at 12:00:01 — 200 in 2 seconds.
- **Sliding window**: 100 requests in any rolling 60-second period. Smoother, but more expensive to compute.
- **Token bucket**: Each user has a bucket that fills at a steady rate (say, 10 tokens per second). Each request costs one token. If the bucket is empty, the request is rejected. Allows short bursts while enforcing average limits.

Rate limiting protects against:
- **DDoS attacks** (Distributed Denial of Service — flooding a system with requests to make it unavailable)
- **Scraping** (automated extraction of data from your website)
- **Runaway clients** (a bug in a partner's code that accidentally sends millions of requests)
- **Cost control** (especially for AI APIs where each request costs money)

> **REAL-LIFE**: OpenAI's API enforces rate limits per pricing tier: free tier gets 3 requests per minute on GPT-4. Tier 5 customers get 10,000 requests per minute. Stripe limits API calls to 100 reads/second in live mode. Twitter's API controversially dropped from 1,500 tweets/15 minutes to 1 read/day for free tier in 2023 — a rate limit change that killed thousands of third-party applications.

## Putting It All Together: A Real System

Let's walk through what happens when you open Swiggy and order food, from a system design perspective.

1. **CDN** serves the app's JavaScript, CSS, and images from an edge server in your city. Load time: ~50ms.
2. **Load balancer** receives your API request ("show restaurants near me") and routes it to one of dozens of application servers.
3. **Cache (Redis)** checks if restaurant listings for your location were computed recently. Cache hit? Return in 0.5ms. Miss? Query the database.
4. **Database (read replica)** handles the read query across a sharded restaurant database. Your location determines which shard.
5. You tap "Order." The **primary database** processes the write: create order, deduct payment.
6. **Message queue (Kafka)** receives the order event. Multiple consumers act independently:
   - Restaurant notification service alerts the kitchen.
   - Delivery assignment service finds the nearest rider.
   - Analytics service logs the order for dashboards.
   - Loyalty service calculates cashback.
7. **Rate limiter** ensures a misbehaving client can't spam the order endpoint.
8. The entire round trip from tap to "Order Confirmed" screen: under 2 seconds.

> **REAL-LIFE**: Swiggy's engineering team has published that their system handles 5,000+ predictions per second for delivery time estimation at a P99 latency (the response time that 99% of requests are faster than — meaning only 1 in 100 requests takes longer) of 71 milliseconds. Their ML models run inference at this scale using a combination of Redis caching, model serving infrastructure, and aggressive batching.

> **REAL-LIFE**: PhonePe processes over 750 million UPI transactions per month across India. Their infrastructure must handle payment spikes during IPL matches, festive sales, and month-end salary days — all while maintaining the consistency guarantees that financial systems demand. They run on a CP-oriented architecture where a failed transaction is always preferable to an incorrect one.

## Netflix: A Case Study in Scale

Netflix serves 250 million subscribers across 190 countries. Their system design decisions are instructive:

- **Microservices**: Over 1,000 independent services. The play button triggers calls to dozens of them.
- **CDN (Open Connect)**: Custom hardware installed inside ISPs globally. Video data never crosses the public internet.
- **Chaos engineering**: Netflix invented **Chaos Monkey** — a tool that randomly kills production servers during business hours to ensure the system can tolerate failure. If your architecture can't survive a server dying, better to find out at 2 PM on a Tuesday than 2 AM on New Year's Eve.
- **Regional failover**: Netflix can redirect all traffic from one AWS region to another in minutes if a region goes down.
- **Caching**: Heavily layered — application cache, CDN cache, device-level cache. A restarted show often resumes without hitting Netflix's servers at all.

The lesson is not "build like Netflix." The lesson is that every architectural decision they've made solves a specific scaling problem they actually experienced. They didn't start with 1,000 microservices. They started as a monolith that shipped DVDs.

## System Design Cheat Sheet

Here's a reference table mapping common problems to their standard solutions:

| Problem | Solution | Key technology |
|---|---|---|
| One server can't handle all traffic | Load balancing | Nginx, HAProxy, AWS ALB |
| Same data computed repeatedly | Caching | Redis, Memcached |
| Users far from servers experience high latency | CDN | Cloudflare, CloudFront, Akamai |
| Synchronous operations slow down response | Message queues | Kafka, RabbitMQ, AWS SQS |
| Database can't handle read volume | Read replicas | PostgreSQL streaming replication |
| Database can't handle write volume | Sharding | Vitess, CockroachDB, Citus |
| Database connection overhead | Connection pooling | PgBouncer, Supavisor |
| Malicious or excessive traffic | Rate limiting | Redis-based, Cloudflare WAF |
| Need global consistency in distributed DB | CP architecture | Google Spanner, CockroachDB |
| Need high availability over consistency | AP architecture | DynamoDB, Cassandra |

<div class="exercise">

### Exercise: Design a URL Shortener

Design a system (like bit.ly) that handles 100 million URLs and 10,000 redirects per second. Think through:

1. **Storage**: How do you generate unique short codes? How do you store the mapping from short code to full URL?
2. **Read path**: A user clicks a short link. What's the fastest way to look up the full URL and redirect? (Hint: 99% of URLs are read far more often than they're written.)
3. **Write path**: A user creates a new short link. How do you ensure the short code is unique? What happens if two users submit at the same microsecond?
4. **Scaling**: Draw a diagram showing where you'd place load balancers, caches, and databases. Which caching strategy would you use for URL lookups?
5. **Tradeoff**: Would you choose a CP or AP approach? What happens if a user creates a short link and it takes 2 seconds to appear on a read replica?

There is no single correct answer. The value is in identifying tradeoffs and defending your choices. Practice explaining your design aloud — this is exactly what system design interviews test.

</div>

**Chapter Endnotes**

The foundational text for distributed systems is Martin Kleppmann's *Designing Data-Intensive Applications* (O'Reilly, 2017) — widely considered the best book on the subject for practitioners. It covers replication, partitioning, consistency, and transactions with remarkable clarity.

For interview-style system design, Alex Xu's *System Design Interview* volumes 1 and 2 (2020, 2022) provide structured walkthroughs of designing systems like rate limiters, chat systems, and notification services.

The *Google SRE Book* (*Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly, 2016) — available free online — covers load balancing, distributed consensus, and managing systems at Google scale. It's written by the engineers who keep Google Search, Gmail, and YouTube running.

Eric Brewer formalized the CAP theorem in his 2000 keynote at the ACM Symposium on Principles of Distributed Computing. His 2012 follow-up paper, "CAP Twelve Years Later: How the 'Rules' Have Changed," clarifies common misconceptions — including the fact that CAP is about the behavior *during* a partition, not a permanent architectural choice.

The Swiggy engineering blog (bytes.swiggy.com) and PhonePe tech blog provide detailed technical writeups on scaling infrastructure for Indian-scale products.
