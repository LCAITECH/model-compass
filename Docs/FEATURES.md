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
  **Partially addressed 2026-08-17** by a deterministic keyword matcher
  over the free-text field (`interfaces/web/use_case_matcher.py`, 14
  categories) that suggests priorities the developer must explicitly
  accept — never an automatic, always-on input to the ranking itself,
  since that would require either an LLM in the loop (breaks
  determinism) or silent keyword-to-ranking inference (fabricates
  confidence the plain-text input doesn't support). See
  `IMPLEMENTATION_NOTES.md`, Iteration #15.
- **Context Analysis** — considers the developer's real constraints:
  budget, expected volume, latency needs, and language requirements.
  Budget can be expressed either as a fixed price tier (Low/Medium/High/
  Very High, anchored to real $/million-token bands) or as a real
  monthly dollar figure — the two are mutually exclusive: a dollar
  figure narrows the affordability estimate shown alongside the
  recommendation, never the ranking itself, since doing that honestly
  would require assuming a token volume nobody provided.
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
- **Tie Detection ("Also Strong Options")** — a coarse, four-level
  quality scale produces real ties more often than not; when another
  qualifying model scores within 2% of the recommendation *and* stays
  within one quality tier of it on every dimension (not just the
  ranked priority), it's shown as a practically-tied "also strong"
  option instead of being silently outranked by an arbitrary
  tie-break. Honest about when the "winner" isn't a clear one.
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

### Access

A recommendation is only useful if the developer can actually reach
the model. Access Advisor answers a distinct question from
Recommend/Explain above — not "which model", but "how do I actually
get it, given my situation" — and never influences the ranking
itself.

- **Access Advisor** — after a recommendation, shows every officially
  documented way to reach that specific model (direct API, a cloud
  platform like Bedrock/Vertex/Azure Foundry, a consumer subscription,
  a playground, self-hosting), grouped by eligibility state rather
  than ranked against each other: `currently_eligible` (usable now
  given what the developer declared), `requires_onboarding` (needs an
  API key, cloud account, or subscription — never hidden, just marked
  as a gap), or excluded entirely (enterprise-only routes, until an
  explicit opt-in is designed). Declaring "no AWS account" never
  removes Bedrock from the list, it just says what's missing.
- **Documented-route discipline** — "can be done in practice" isn't
  the bar; a route only enters the catalog with an official source URL,
  a confirmed status, and the exact dataset model id (never a family
  or sibling standing in). MCP-based or third-party-integration access
  is deliberately excluded until it clears the same bar — this
  distinction (verifiable vs. merely possible) is what keeps the
  advisor trustworthy as the catalog grows.
- **26/26 model coverage** — every model in the dataset has at least
  one documented access route (60 routes total as of 2026-08-13, up
  from 4 at launch), reached through 10 reusable access-pattern
  templates rather than 60 independent research efforts. Claude Fable
  5 is the catalog's most complex case: 5 real routes across 3
  distinct surfaces (direct API, three cloud platforms, a consumer
  subscription), each with its own eligibility and economics — proof
  the advisor models "how you'd actually get this" rather than a
  simple yes/no per model.

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
  meaningfully. **Partially addressed 2026-08-11** by Tie Detection
  ("Also Strong Options," under Recommend, above) — a categorical
  signal ("practically tied" vs. not), not a percentage. A numeric
  score was considered and rejected for the same reason a "92%
  confidence" badge would be: the underlying quality scale is only
  four levels, and inventing a smooth number on top of a coarse
  scale would be exactly the fabricated-precision problem this
  project avoids elsewhere (see the ranking-transparency decision in
  `HANDOFF.md`). This capability stays open for a genuinely different
  kind of confidence signal, not superseded by Tie Detection.
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
- **Self-Hosted / Infrastructure Cost** — for models distributed as
  open weights and served through an inference platform like NVIDIA
  NIM, the real question often isn't "what's the per-token price" (many
  have none, or none NVIDIA itself publishes) but "what does it cost to
  operate this." NVIDIA's own docs separate this cleanly from token
  pricing: NIM Day 0 (free, unofficial rate limits, no compliance SLA)
  vs. NIM Certified (requires NVIDIA AI Enterprise, priced per-GPU —
  $4,500/GPU/year or ~$1/GPU/hour — flat regardless of model or GPU
  size), plus an official per-model GPU support matrix (verified GPU
  SKUs and tensor-parallelism profiles, e.g. Llama 3.1 70B on
  A100-SXM4-40GB/H100-80GB). That's a genuinely different data shape
  than `cost.input_per_million`/`output_per_million` — model to GPU
  requirement to GPU-hour price to operational cost — and forcing it
  into the existing token-cost fields would misrepresent a flat
  infrastructure license as if it were a per-token API price. First
  noted 2026-08-09 during the free-access research pass, confirmed
  against official NVIDIA docs 2026-08-10 (see
  `IMPLEMENTATION_NOTES.md`, Iteration #10); not started, not scoped,
  and explicitly not part of the `has_free_access` proposal from the
  free-access research pass — this needs its own schema extension, decided
  separately, once (or if) it's worth pursuing.
