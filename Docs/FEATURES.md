# FEATURES.md — Model Compass

This document describes what Model Compass is capable of — not how it
is built, and not what it looks like. Interface details belong to the
product itself; architectural details belong to
[ARCHITECTURE.md](./ARCHITECTURE.md).

Capabilities are organized around the natural flow of a
recommendation: the system must first **understand** the developer's
context, then **recommend** a model, **explain** why, and give the
developer reasons to **trust** the result. The final section,
**grow**, describes how the product itself will evolve.

Capabilities are split into two groups:

- **Core Capabilities** — define the identity of Model Compass and are
  part of the MVP.
- **Planned Capabilities** — part of the project's natural evolution,
  to be introduced in later phases.

---

## Core Capabilities

### Understand

What the system understands about the developer's problem before it
recommends anything.

- **Use Case Analysis** — interprets the type of application the
  developer is building (chatbot, content generation, code assistant,
  data extraction, etc.) as a core input to the recommendation.
- **Context Analysis** — considers the developer's real constraints:
  budget, expected volume, latency needs, and language requirements.
- **Requirement Prioritization** — lets the developer indicate what
  matters most for their case (e.g. cost over reasoning power, or
  speed over context length), rather than treating every variable
  equally.

### Recommend

The core of the product: turning context into a decision.

- **Model Recommendation** — returns the single most suitable model
  for the developer's context, based on the current dataset and
  recommendation rules.
- **Alternative Recommendations** — never presents a single option in
  isolation. Every recommendation is shown alongside credible
  alternatives, so the developer can compare rather than just accept.
- **Trade-off Analysis** — makes explicit what is being given up by
  choosing the recommended model over another (e.g. lower cost in
  exchange for weaker reasoning), instead of presenting a decision as
  strictly "best."

### Explain

Why the system recommended what it recommended.

- **Explainable Recommendations** — every recommendation includes the
  reasoning behind it. A model name is never returned on its own.
- **Decision Transparency** — the developer can see how their inputs
  (budget, priorities, use case) connect to the outcome.
- **Decision Factors** — surfaces the specific factors that were
  weighed to reach a recommendation, for example:

  ```
  Decision factors

  Cost
  Language
  Latency
  Reasoning
  Tool Calling
  Context Window
  ```

### Trust

Why the developer should believe the recommendation in the first
place.

- **Dataset Transparency** — the data behind every recommendation is
  public and versioned; nothing about a model's specs or pricing is
  hidden or assumed.
- **Vendor Neutrality** — no provider is favored. The same provider
  can be recommended in one scenario and excluded in another, based
  strictly on context.
- **Deterministic Results** — the same input always produces the same
  reasoning and the same recommendation. Results come from explicit
  rules and curated data, not from an AI model's opinion.

---

## Planned Capabilities

Capabilities that extend the product's reach and depth in later
phases of the [Roadmap](./ROADMAP.md).

### Grow

- **API** — programmatic access to the Decision Engine for
  integration into other tools. *(Developer Platform phase)*
- **Python SDK** — direct use of Model Compass from Python code.
  *(Developer Platform phase)*
- **CLI** — terminal-based access for developers who prefer working
  from the shell. *(Developer Platform phase)*
- **Community Dataset Contributions at Scale** — a mature, well
  documented contribution process as the dataset and contributor base
  grow. *(Community & Governance phase)*
- **Custom Recommendation Profiles** — lets teams define their own
  weighting of priorities (e.g. always favor cost, or always favor
  reasoning) as a reusable profile instead of specifying it every time.
- **Recommendation Confidence** — as the dataset grows, some
  recommendations will be clear-cut while others will be closer
  calls. This capability would surface that distinction, for example:

  ```
  Confidence

  92%
  ```

  Not part of the MVP — noted here as a direction worth exploring
  once the dataset and engine are mature enough to support it
  meaningfully.
- **Recommendation History** — the ability to see how a recommendation
  for a given use case has changed over time, as models, pricing, and
  the dataset evolve. A long-term direction, not a near-term
  commitment.
- **Multi-Model Cost Strategies** — instead of a single recommended
  model, suggest splitting a workload across two or more models by
  task (e.g. a cheaper model for simple requests, a stronger one for
  complex ones) to reduce total spend. A genuinely different question
  from "what's the best single model for this context" — it needs its
  own domain concept for a workload made of distinct sub-tasks, and a
  defensible way to score the quality of a *blend* of models rather
  than one model's own editorial ratings. Explicitly not part of the
  MVP: doing this honestly means never presenting an estimated usage
  volume (e.g. "≈450 conversations/month") as if it were sourced data
  — a token budget only translates to real-world usage once the user
  supplies their own volume or spend numbers, not from an invented
  usage category.
- **Subscription vs. API Comparator** — help a developer decide
  between a flat-rate subscription (e.g. ChatGPT Plus, Claude Pro) and
  pay-per-token API access. A standalone tool, deliberately kept
  separate from the model recommender — it answers "how should I pay
  for this" rather than "which model should I use", and the two
  questions shouldn't be mixed into one flow. Meaningfully harder than
  anything else on this list: subscriptions don't have per-token
  pricing at all, only usage caps that providers rarely publish as a
  fixed, stable, token-denominated number — a genuinely different kind
  of objective data than anything `SCHEMA.md` currently sources, likely
  requiring its own schema extension before this could be built
  honestly. Any version of this must be explicit about what's
  verifiable (subscription price, API price) versus estimated
  (token-equivalent usage), and must not claim a precise equivalence
  like "$20 of Plus = X million tokens" — that's the same fabricated-
  precision problem Multi-Model Cost Strategies runs into, above.
- **Specialized / Domain-Specific Models** — a separate category for
  models fine-tuned or purpose-built for a narrow domain (e.g. Gemini
  3.5 Flash Cyber, tuned for cybersecurity vulnerability work) rather
  than general-purpose use. Noted 2026-08-07 when Gemini 3.5 Flash
  Cyber came up during a dataset-expansion pass and was deliberately
  left out of the general-purpose catalog instead of shoehorned in.
  The reason it's a separate capability, not just "another row in
  `dataset/models/`": `SCHEMA.md`'s quality dimensions
  (`reasoning`/`coding`/`creative_writing`/`instruction_following`) and
  cost-tier ranking assume models are being compared for the same kind
  of general work — rating a cybersecurity-specialized model on
  "creative writing" would be meaningless, and ranking it against
  general-purpose models on blended cost would misrepresent what it's
  actually for. Needs its own comparison axis (or its own section of
  the dataset) before the first specialized model is added, not an
  attempt to squeeze it into the existing schema and hope the
  dimensions happen to still make sense.
- **Total Cost of Task (a.k.a. "Effective Cost")** — a cheaper model
  that needs several corrective re-prompts to get a complex task right
  can end up costing more, in tokens and time, than a pricier model
  that succeeds on the first try. Real phenomenon, real product
  insight — and explicitly not buildable today: it would require a
  per-model, per-task-type expected iteration count, which does not
  exist anywhere as sourceable data. Estimating it would mean
  inventing a multiplier and presenting it as fact, the same mistake
  already avoided for Multi-Model Cost Strategies. Only build this if
  it can be grounded in actual evidence — repeatable benchmarks, the
  project's own structured evaluations, or opt-in user telemetry — not
  a model's or a contributor's guess. A "Cost Efficiency" star rating
  without that evidence behind it is exactly the kind of fabricated-
  confidence badge this project has declined every time it's come up;
  don't add one just because the underlying idea is good.
