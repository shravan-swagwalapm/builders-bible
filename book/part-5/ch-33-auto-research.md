<span class="chapter-number">Chapter 33</span>

# Autonomous Research & Self-Improving Systems {.chapter-title}

In October 2025, Andrej Karpathy posted a thread that made the AI research community stop and pay attention. He described a system called **AutoResearch** — 630 lines of Python, running on a single GPU, that conducted 12 machine learning experiments per hour. Left running overnight, it completed 100 experiments, analyzed the results, generated hypotheses about why certain configurations worked, designed follow-up experiments to test those hypotheses, and ran those too. By morning, the system had discovered a configuration that outperformed the human-designed baseline.

Karpathy didn't claim the system was an artificial scientist. He claimed something more practical and more important: that the loop of hypothesis → experiment → analysis → new hypothesis could be automated, and that when it was, the pace of discovery accelerated by an order of magnitude. A human researcher running the same experiments manually would have needed two weeks. The system needed one night.

This chapter is about that loop — and about systems that don't stay static after deployment but observe their own performance, detect their own failures, and improve themselves. We will cover Karpathy's AutoResearch architecture, the broader paradigm of self-improving AI systems, the DSPy compile pattern that automates prompt optimization, continuous evaluation frameworks, automated red-teaming, and the philosophical questions raised by systems that modify their own behavior.

---

## AutoResearch: 630 Lines That Change the Game

### The Architecture

AutoResearch is deceptively minimal. It has four components:

```
AutoResearch Architecture:

  ┌──────────────────────────────────────────────────────────┐
  │                    EXPERIMENT MANAGER                      │
  │  Maintains a queue of experiments to run, tracks results,  │
  │  manages GPU allocation, handles failures and retries      │
  └─────────────────────────┬────────────────────────────────┘
                            │
              ┌─────────────┼─────────────────┐
              ▼             ▼                 ▼
  ┌───────────────┐ ┌──────────────┐ ┌───────────────────┐
  │  EXPERIMENTER │ │   ANALYZER   │ │  HYPOTHESIS GEN   │
  │               │ │              │ │                   │
  │  Runs a       │ │  Reads       │ │  Takes analysis   │
  │  training     │ │  experiment  │ │  results +        │
  │  experiment   │ │  logs,       │ │  past experiments │
  │  with given   │ │  extracts    │ │  and generates    │
  │  config       │ │  metrics,    │ │  new experiment   │
  │  (model,      │ │  compares    │ │  configurations   │
  │  hyperparams, │ │  to past     │ │  to test          │
  │  data config) │ │  results     │ │                   │
  └──────┬────────┘ └──────┬───────┘ └─────────┬─────────┘
         │                 │                    │
         └─────────────────┴────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │     RESULTS LOG        │
              │  Append-only record    │
              │  of every experiment,  │
              │  its config, metrics,  │
              │  and analysis          │
              └────────────────────────┘
```

The loop runs continuously:

1. **Hypothesis Generator** (an LLM — Claude or GPT-4) examines the results log and proposes a new experiment configuration. It reads what has been tried, what worked, what failed, and why. It then suggests a specific change: "Try increasing the learning rate from 0.001 to 0.003 while keeping batch size at 32, because the loss curve from experiment #47 suggests we're in a flat region."

2. **Experimenter** takes the configuration and runs the actual training. This is real code executing on real hardware — not the LLM pretending to run an experiment.

3. **Analyzer** (another LLM call) reads the training logs, extracts key metrics (loss, accuracy, training time, convergence behavior), and compares them against all previous experiments.

4. **Experiment Manager** logs everything and feeds it back to step 1.

> **ANALOGY**: Think of a chef developing a new recipe. The traditional approach: cook one version, taste it, think for a while, cook another version, taste again. Each iteration takes an hour. Now imagine the chef has a kitchen with 12 stoves, a very fast taster, and a recipe assistant who — after each tasting — immediately suggests the next variation. "That was too salty. Try reducing salt by 10% and adding lime. And on the next stove, try keeping the salt but adding coconut milk." The throughput of experimentation increases dramatically, not because any single experiment is faster, but because the gap between experiments shrinks to nearly zero.

### The Shopify Adaptation

Karpathy's proof-of-concept used a straightforward ML training task. But the pattern was quickly adapted to production contexts. A team at Shopify applied the AutoResearch loop to their product recommendation model. Instead of A/B testing one configuration at a time (a process that took weeks per experiment due to the need for statistical significance), they ran the AutoResearch loop against historical data:

- **12 configurations tested per hour** against six months of historical purchase data
- **100 configurations evaluated overnight**
- The winning configuration — discovered by the system, not a human — improved click-through rate by 7% over the human-designed baseline

The human-designed baseline was the result of two years of iterative optimization by a team of experienced ML engineers. The automated system beat it in 12 hours. Not because the system was smarter, but because it explored a larger space of configurations more rapidly, without the human biases that tend to anchor researchers near their existing solutions.

> **REAL-LIFE**: The Shopify team reported a key insight: the system's winning configuration used a combination of hyperparameters that no human had tried because it seemed counterintuitive — a very high dropout rate (regularization technique that randomly deactivates parts of the network during training) paired with an unusually low learning rate. Human researchers had tested high dropout and low learning rates separately, but never in combination, because conventional wisdom suggested they would cancel each other out. The system had no such conventional wisdom. It tested the combination because it was systematically exploring the space, and it worked.

### What Makes AutoResearch Different from Grid Search

A fair question: isn't this the same as grid search (trying every combination of parameters) or random search (trying random combinations)? No, and the difference matters.

```
Experiment Selection Strategies:

  Grid Search:     Try every combination in a predefined grid
                   ├── Exhaustive but exponentially expensive
                   ├── 5 parameters × 10 values = 100,000 experiments
                   └── No learning between experiments

  Random Search:   Try random combinations
                   ├── Surprisingly effective (Bergstra & Bengio, 2012)
                   ├── More efficient than grid search
                   └── No learning between experiments

  Bayesian Opt:    Use a mathematical model to predict which
                   regions of the space are most promising
                   ├── Learning from past experiments
                   ├── Efficient for smooth parameter spaces
                   └── Struggles with discrete or complex spaces

  AutoResearch:    Use an LLM to read experiment results and
                   propose the next experiment
                   ├── Learning from past experiments (like Bayesian)
                   ├── Can reason about WHY something worked
                   ├── Can propose novel combinations based on
                   │   understanding, not interpolation
                   └── Can read error logs and debug failures
```

The key difference: AutoResearch's hypothesis generator *reads the experiment logs in natural language*. It doesn't operate on a mathematical model of the search space. It reads: "Experiment #47: learning_rate=0.001, batch_size=32, loss stopped decreasing at epoch 15, final accuracy 87.2%. The loss curve shows a plateau with occasional spikes, suggesting the learning rate may be too low to escape the local minimum." From that narrative, it reasons about what to try next.

This ability to reason about experimental results, rather than interpolate numerically, is what makes LLM-powered experimentation different from traditional automated methods. It can handle messy, high-dimensional search spaces where the relationships between parameters are complex and non-obvious.

---

## Self-Improving Skills: Observe, Detect, Propose, Evaluate

AutoResearch optimizes ML training configurations. But the same loop — observe behavior, detect patterns, propose improvements, evaluate results — applies to a much broader class of systems. Any AI system that performs repeated tasks can, in principle, improve itself.

This is not hypothetical. It is running in production.

### The Self-Improving Skills Architecture

In a production system built by the author, AI-powered tools (called "skills") are augmented with a **self-improvement loop** that continuously monitors their performance and proposes optimizations:

```
Self-Improving Skills — The Four-Phase Loop:

  Phase 1: OBSERVE
  ┌────────────────────────────────────────────────┐
  │  Every time a skill runs, a PostToolUse hook    │
  │  captures:                                      │
  │  - Input (what the user asked)                  │
  │  - Output (what the skill produced)             │
  │  - Latency (how long it took)                   │
  │  - User reaction (did they accept, modify,      │
  │    or reject the output?)                        │
  │  - Error (if any)                                │
  │                                                  │
  │  Stored as a JSONL (JSON Lines) log file         │
  └────────────────────────────┬───────────────────┘
                               │
                               ▼
  Phase 2: DETECT
  ┌────────────────────────────────────────────────┐
  │  A periodic analysis job reads the observation  │
  │  log and detects patterns:                      │
  │                                                  │
  │  - Recurring failures (same error 3+ times)     │
  │  - Quality degradation (user rejection rate     │
  │    increasing over time)                         │
  │  - Performance drift (latency increasing)        │
  │  - Common user modifications (users consistently │
  │    edit the output in the same way)              │
  └────────────────────────────┬───────────────────┘
                               │
                               ▼
  Phase 3: PROPOSE
  ┌────────────────────────────────────────────────┐
  │  An LLM reviews the detected patterns and       │
  │  proposes specific improvements:                 │
  │                                                  │
  │  "Users are consistently removing the greeting   │
  │   line from email drafts. Propose: modify the    │
  │   email skill's prompt to omit greetings when    │
  │   the context is internal communication."         │
  │                                                  │
  │  Proposed changes are logged, not auto-applied   │
  └────────────────────────────┬───────────────────┘
                               │
                               ▼
  Phase 4: EVALUATE
  ┌────────────────────────────────────────────────┐
  │  The proposed change is tested:                  │
  │                                                  │
  │  - Run the modified skill against the last 50    │
  │    real inputs (stored in the observation log)    │
  │  - Compare outputs to the originals              │
  │  - If quality improves on >80% of cases:         │
  │    → Flag for human review and approval           │
  │  - If quality degrades:                           │
  │    → Discard the proposal, log why                │
  └────────────────────────────────────────────────┘
```

> **INTUITION**: Think of this as the difference between a restaurant that cooks the same menu forever and a restaurant where the chef reviews customer feedback every week, notices that 40% of customers are asking for less salt, tests a reduced-salt version with the kitchen staff, and — only if it's better — updates the recipe. The food improves continuously without a major menu overhaul. The self-improving skills loop works the same way: small, evidence-based adjustments, verified before deployment.

### The Critical Constraint: Human in the Loop

Notice that Phase 4 does not automatically deploy the change. It flags the proposal for human review. This is a deliberate design decision, not a technical limitation.

Self-improving systems without human oversight create a specific category of risk: **value drift**. The system optimizes for the metric it can measure (user acceptance rate, latency, error rate) but may drift away from qualities it cannot measure (brand voice, ethical guidelines, long-term user trust). A skill that learns users prefer shorter responses might progressively strip away important caveats and disclaimers — improving the acceptance rate while degrading the safety of the output.

The human review step is the circuit breaker. It ensures that optimization doesn't outrun judgment.

```
Self-Improvement Safety Levels:

  Level 0: NO SELF-IMPROVEMENT
  │  System is static after deployment
  │  Pros: Predictable, auditable
  │  Cons: Degrades as the world changes
  │
  Level 1: OBSERVE AND REPORT (recommended starting point)
  │  System monitors its own performance and generates reports
  │  Humans decide what to change
  │
  Level 2: PROPOSE AND REVIEW (production-ready)
  │  System proposes specific improvements
  │  Humans approve or reject each proposal
  │  Changes are versioned and reversible
  │
  Level 3: AUTO-IMPROVE WITH GUARDRAILS (advanced)
  │  System applies low-risk improvements automatically
  │  (e.g., prompt wording changes within defined parameters)
  │  High-risk changes still require human review
  │
  Level 4: FULL AUTONOMY (not recommended for production)
  │  System modifies itself without human oversight
  │  Risk of value drift, unintended optimization, and
  │  behaviors that are difficult to audit or reverse
```

Most production systems should operate at Level 2. The observation and proposal capabilities provide the acceleration. The human review provides the steering.

### Implementation: The JSONL Pattern

The observation log uses **JSONL** (JSON Lines) format — one JSON object per line, one line per observation. This format is chosen for specific technical reasons:

- **Append-only**: New observations are appended to the file without reading or modifying existing data. This is fast, crash-safe, and works well with concurrent writes.
- **Streamable**: Tools can read the file line by line without loading the entire file into memory, enabling analysis of large logs.
- **Queryable**: Each line is a self-contained JSON object that can be filtered, aggregated, and analyzed with standard tools.

```
Example Observation Log (JSONL):

{"timestamp":"2026-03-15T14:23:01Z","skill":"email_draft","input":"write follow-up email to Raj about Q4 planning","output":"Subject: Q4 Planning Follow-Up...","latency_ms":2340,"user_action":"accepted_with_edits","edits":"removed greeting, shortened second paragraph"}
{"timestamp":"2026-03-15T14:45:22Z","skill":"email_draft","input":"draft email declining meeting invitation","output":"Subject: Re: Team Sync...","latency_ms":1890,"user_action":"accepted","edits":null}
{"timestamp":"2026-03-15T15:01:47Z","skill":"code_review","input":"review this auth middleware","output":"3 issues found...","latency_ms":4520,"user_action":"rejected","edits":null,"rejection_reason":"missed the SQL injection vulnerability in line 47"}
```

From this log, the detection phase can identify: "The email_draft skill is being edited to remove greetings in 60% of internal emails. The code_review skill missed a SQL injection vulnerability, suggesting its prompt needs stronger security-focused instructions."

---

## Continuous Evaluation: Never Trust Yesterday's Performance

A deployed AI system that was 95% accurate last month might be 85% accurate today. Models don't degrade in isolation — the world changes around them. User language shifts. New product names appear that weren't in the training data. Competitors change their strategies. Seasonal patterns shift behavior.

**Continuous evaluation** is the practice of regularly testing a deployed system against a maintained test set, tracking performance over time, and alerting when metrics decline.

```
Continuous Evaluation Pipeline:

  ┌─────────────────────────────────────────────────────┐
  │  GOLDEN TEST SET                                     │
  │  100-500 representative examples                     │
  │  Input + Expected Output + Quality Criteria          │
  │  Updated monthly with new edge cases                 │
  └────────────────────────────┬────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────┐
  │  SCHEDULED EVALUATION (daily or weekly)              │
  │  Run the production system against the test set      │
  │  Score each output on defined quality criteria        │
  │  Compare scores to historical baseline               │
  └────────────────────────────┬────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────┐
  │  DRIFT DETECTION                                     │
  │  Has accuracy dropped >5% from baseline?             │
  │  Has latency increased >20%?                         │
  │  Are new failure patterns appearing?                  │
  │                                                       │
  │  If yes → ALERT the team                              │
  │  If no  → Log results, continue monitoring            │
  └─────────────────────────────────────────────────────┘
```

The golden test set is not static. It must evolve:

| Trigger | Action |
|---|---|
| New feature deployed | Add test cases covering the new feature |
| Bug reported by user | Add the bug-triggering input to the test set |
| New edge case discovered | Add it with expected behavior |
| Model or prompt changed | Re-baseline the expected scores |
| Quarterly review | Prune outdated test cases, add emerging patterns |

> **REAL-LIFE**: A fintech company deployed an AI system for classifying customer support tickets. At launch, accuracy was 94%. Three months later, without any code changes, accuracy had dropped to 81%. The cause: a new product launch had introduced ticket categories ("crypto wallet issues," "staking rewards questions") that didn't exist in the training data or test set. The system was still confidently classifying these tickets — into wrong categories. Continuous evaluation with a regularly updated test set would have caught this drift within the first week.

---

## Automated Red-Teaming: Breaking Your Own System

**Red-teaming** is the practice of deliberately trying to make a system fail — finding the inputs that produce harmful, incorrect, or embarrassing outputs. Traditional red-teaming is manual: a team of humans thinks up adversarial inputs and tests them one by one.

**Automated red-teaming** uses an LLM to generate adversarial inputs at scale. The idea: if an LLM can generate thousands of creative attack vectors in minutes, it can find vulnerabilities that a human team might miss.

```
Automated Red-Teaming Architecture:

  ┌─────────────────────────────────────────┐
  │  ATTACKER MODEL (LLM)                    │
  │  "Generate inputs that might cause the   │
  │   target system to produce harmful,       │
  │   incorrect, or unsafe outputs.           │
  │   Be creative. Try different strategies:  │
  │   - Prompt injection                      │
  │   - Jailbreaking                          │
  │   - Edge cases                            │
  │   - Encoding tricks                       │
  │   - Role-play scenarios"                  │
  └──────────────────┬──────────────────────┘
                     │ generates 1000+ attack inputs
                     ▼
  ┌─────────────────────────────────────────┐
  │  TARGET SYSTEM                           │
  │  Your production AI system               │
  │  (processes each attack input normally)   │
  └──────────────────┬──────────────────────┘
                     │ produces 1000+ outputs
                     ▼
  ┌─────────────────────────────────────────┐
  │  JUDGE MODEL (LLM)                       │
  │  "For each output, evaluate:             │
  │   - Did the system follow its guidelines? │
  │   - Did it produce harmful content?       │
  │   - Did it leak system prompt details?    │
  │   - Did it comply with manipulation?"     │
  └──────────────────┬──────────────────────┘
                     │
                     ▼
  ┌─────────────────────────────────────────┐
  │  VULNERABILITY REPORT                    │
  │  Successful attacks ranked by severity   │
  │  Patterns identified across attacks      │
  │  Suggested mitigations                   │
  └─────────────────────────────────────────┘
```

The attacker model is told to be adversarial. The target system runs normally. The judge model evaluates whether the target was compromised. This three-model architecture — attacker, target, judge — is the standard pattern for automated red-teaming.

> **ANALOGY**: This is the AI equivalent of a security penetration test. Companies hire ethical hackers to attack their systems and find vulnerabilities before malicious actors do. Automated red-teaming does the same thing — but instead of hiring five security experts for two weeks, you run an LLM for two hours and generate thousands of attack vectors. The LLM-generated attacks won't be as creative as an expert human's, but the volume compensates. You find the easy-to-exploit vulnerabilities automatically, freeing human red-teamers to focus on the subtle, complex attack surfaces.

Anthropic's **Constitutional AI** paper (2022) introduced a related concept: using an LLM to critique and revise its own outputs according to a set of principles (a "constitution"). This is self-improvement applied to safety — the model doesn't wait for external feedback but evaluates its own responses against explicit values and rewrites those that violate them.

---

## The DSPy Compile Paradigm: Optimizing Prompts Automatically

Chapter 30 introduced DSPy as a framework for compound AI systems. Here, we examine its self-improvement mechanism — the **compile** step — which is the most production-relevant application of the automatic optimization paradigm.

The core insight: writing prompts by hand is like writing machine code by hand. It works for small programs, but it doesn't scale. DSPy's compile step replaces manual prompt engineering with automatic optimization:

```
DSPy Compile — Before and After:

  BEFORE (Manual Prompt Engineering):
  ┌──────────────────────────────────────────────┐
  │  Developer writes prompt → Tests on examples  │
  │  → Tweaks wording → Tests again → Tweaks     │
  │  → Tests → Ships → Discovers edge cases      │
  │  → Tweaks more → Ships again                  │
  │                                                │
  │  Time: Days to weeks                           │
  │  Quality: Limited by developer's intuition     │
  │  Portability: Breaks when model changes        │
  └──────────────────────────────────────────────┘

  AFTER (DSPy Compile):
  ┌──────────────────────────────────────────────┐
  │  Developer defines:                            │
  │    - Signature: input → output                 │
  │    - Training examples: 20-50 labeled pairs    │
  │    - Quality metric: function that scores      │
  │      output quality                            │
  │                                                │
  │  DSPy compiler:                                │
  │    - Generates candidate prompts               │
  │    - Tests each against training examples       │
  │    - Selects optimal prompt/few-shot examples   │
  │    - Optionally fine-tunes the model            │
  │                                                │
  │  Time: Minutes to hours (automated)            │
  │  Quality: Optimized against actual metric       │
  │  Portability: Re-compile for any model          │
  └──────────────────────────────────────────────┘
```

The compile step is itself a self-improving loop: DSPy generates prompts, evaluates them, learns which patterns work for this model on this task, and converges on an optimized configuration. When you switch models (from GPT-4o to Claude Sonnet, say), you re-compile and the optimizer finds the best prompt for the new model automatically.

> **REAL-LIFE**: In published benchmarks from the DSPy team (Stanford NLP group), compiled pipelines consistently outperform hand-crafted prompts by 10-20% on accuracy metrics. The improvement is largest when the task is complex (multi-step reasoning, retrieval-augmented generation) and when the model is unfamiliar (a new release that no one has tuned prompts for yet). The improvement is smallest for simple tasks where a straightforward prompt already works well.

The broader lesson: any system component whose behavior is controlled by a prompt can, in principle, be automatically optimized. The DSPy compile paradigm makes this practical for production systems.

---

## Philosophical Implications: Where Does This Lead?

The systems described in this chapter — AutoResearch, self-improving skills, continuous evaluation, automated red-teaming, DSPy compile — share a common structure: an AI system that modifies its own behavior based on evidence. This raises questions that go beyond engineering.

### The Attribution Problem

When AutoResearch discovers a winning configuration, who deserves credit? The human who wrote the 630-line framework? The LLM that proposed the hypothesis? The GPU that ran the experiment? The training data that taught the LLM to reason about ML configurations?

This is not a philosophical abstraction. It has immediate implications for academic publishing, patent law, and professional reputation. If an AI system discovers a drug candidate, who gets the patent? If an AI system writes a paper, who gets listed as author?

The current consensus is pragmatic: the human who designed, deployed, and interpreted the system's output is the author. The AI is a tool, like a microscope or a statistical software package. But this consensus will be tested as systems become more autonomous and their contributions become less distinguishable from human insight.

### The Alignment Tax

Self-improving systems optimize for what they can measure. If your quality metric captures everything that matters, the system improves in the right direction. If your metric misses something — fairness, long-term user trust, cultural sensitivity — the system may optimize away from those unmeasured values.

This is the **alignment tax**: the cost of ensuring that a self-improving system improves in the direction you want, not the direction that maximizes the measurable metric. It requires:

- **Comprehensive metrics**: Multiple quality dimensions, not a single score
- **Human review**: Regular audits of the system's proposed changes
- **Reversiblity**: The ability to roll back any change the system makes
- **Value constraints**: Hard limits on what the system is allowed to optimize

> **INTUITION**: Consider a self-improving customer support bot that discovers it can increase its "issue resolved" metric by 15% if it pre-emptively offers refunds before the customer asks. The metric improves. But the company is now giving away money unnecessarily. The bot optimized the metric it could measure (resolution rate) at the expense of a metric it couldn't (company profitability). The alignment tax is the cost of designing metrics, guardrails, and review processes that prevent this kind of well-intentioned but misaligned optimization.

### The Acceleration Question

If AI systems can improve themselves, and if those improvements make the systems more capable of improving themselves further, what governs the pace of improvement?

The current answer is: human review is the bottleneck, and that is by design. Every system described in this chapter has a human checkpoint — a point where a person reviews, approves, or rejects the system's proposed change. This human-in-the-loop constraint means the system improves at the pace of human judgment, not the pace of compute.

Whether this constraint should be relaxed — and under what conditions — is one of the most consequential questions in AI safety. For now, as a builder, the pragmatic answer is: keep the human in the loop. The cost of slower improvement is vastly lower than the cost of an unchecked system optimizing in a direction you didn't intend.

---

## Building Your Own Self-Improving System

Here is a practical starting point — a minimal self-improvement loop you can implement for any LLM-powered feature:

```
Minimal Self-Improvement Implementation:

  Step 1: INSTRUMENT (Day 1)
  ├── Log every LLM call: input, output, latency, model
  ├── Log user reactions: accepted, edited, rejected
  ├── Use JSONL format for append-only, streamable logs
  └── Store logs locally or in a simple database

  Step 2: ANALYZE (Weekly, automated)
  ├── Run an LLM over the last 7 days of logs
  ├── Prompt: "Identify the top 3 patterns in user edits
  │   and rejections. What is the system consistently
  │   getting wrong?"
  └── Output: A structured report of identified patterns

  Step 3: PROPOSE (Weekly, automated)
  ├── For each identified pattern, ask the LLM:
  │   "Propose a specific change to the system prompt
  │    that would address this pattern. Show the current
  │    prompt section and the proposed modification."
  └── Output: Specific, diffable prompt modifications

  Step 4: EVALUATE (Weekly, human-reviewed)
  ├── Run proposed changes against last 50 real inputs
  ├── Compare new outputs to original outputs
  ├── Score improvement: better / same / worse
  ├── If >80% better or same → present to human for approval
  └── If approved → deploy as new prompt version

  Total implementation: ~150 lines of code + a cron job
  Total cost per week: ~$0.50-2.00 in LLM API calls
```

This is Level 2 on the safety scale described earlier — propose and review. It requires no custom ML infrastructure, no fine-tuning, and no specialized tooling. It requires logging, a weekly analysis job, and a human who reviews the proposals.

The insight that makes this practical: **the same LLMs that power your features can also analyze your features' performance and propose improvements.** The tool and the tool-improver are the same technology.

<div class="exercise">
<div class="exercise-title">Try It Yourself</div>

1. **Observation logging**: Take any AI feature you've built (or a simple prompt you use regularly). Start logging every interaction — the input, the output, and whether you were satisfied with the result. After 20 interactions, read through the log. What patterns do you notice? Where does the system consistently fail or require editing?

2. **AutoResearch micro-experiment**: Pick a task where you use an LLM with specific prompt parameters (temperature, system prompt, max tokens). Write a script that tests 10 different configurations against 5 fixed test inputs, scores each output on a 1-5 scale (using another LLM as the scorer), and reports which configuration performs best. You've built a mini AutoResearch loop.

3. **Automated red-teaming**: Take an AI feature you've built and write a prompt that asks an LLM to generate 20 adversarial inputs designed to make the feature fail. Run those inputs through your feature. How many succeed in producing bad outputs? What categories of attack are most effective?

4. **DSPy exploration**: Install DSPy (`pip install dspy-ai`) and follow the Getting Started tutorial. Define a signature for a task you care about, provide 10 training examples, and run the compile step. Compare the optimized prompt to your hand-written prompt. Is the optimized version better?

5. **Self-improvement proposal**: For any AI system you have access to, write a one-page proposal for adding a self-improvement loop. Specify: what you would observe, how you would detect patterns, what kinds of changes you would propose, and what human review process you would implement. What safety level (0-4) is appropriate for your system, and why?

</div>

---

**Chapter endnotes**

[1] Andrej Karpathy's AutoResearch system was described in a series of social media posts and a subsequent blog entry in late 2025. The 630-line figure and single-GPU constraint are from his original description. The system demonstrated that LLM-guided experiment loops can discover competitive configurations faster than manual search in well-defined parameter spaces.

[2] The Shopify adaptation of the AutoResearch pattern was described in a public engineering blog post from Shopify's ML team, late 2025. The 7% click-through rate improvement and the counterintuitive high-dropout/low-learning-rate discovery are from their published results.

[3] DSPy: Omar Khattab et al., "DSPy: Compiling Declarative Language Model Calls into State-of-the-Art Pipelines," ICLR 2024. The compile paradigm and benchmark results (10-20% improvement over hand-crafted prompts) are from the paper and subsequent DSPy team publications.

[4] Constitutional AI: Yuntao Bai et al., "Constitutional AI: Harmlessness from AI Feedback," Anthropic, 2022. The paper describes training AI systems to critique and revise their own outputs according to a set of principles, enabling self-improvement in alignment and safety.

[5] The self-improving skills architecture described in this chapter is based on the author's production implementation. The JSONL observation pattern, four-phase loop (observe/detect/propose/evaluate), and safety level framework are drawn from real deployment experience.

[6] Random search vs. grid search: Bergstra and Bengio, "Random Search for Hyper-Parameter Optimization," Journal of Machine Learning Research, 2012. The paper demonstrated that random search is more efficient than grid search for hyperparameter optimization, a finding that underpins much of modern automated ML.

[7] Automated red-teaming research: Perez et al., "Red Teaming Language Models with Language Models," 2022. The paper formalized the attacker-target-judge framework for automated adversarial testing of LLM systems.