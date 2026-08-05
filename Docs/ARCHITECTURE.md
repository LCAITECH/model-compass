# ARCHITECTURE.md — Model Compass

This document describes how Model Compass is structured internally:
its main building blocks, the boundaries between them, and the
principles that constrain how those blocks are allowed to depend on
each other.

It does not describe *what* the product does (see
[FEATURES.md](./FEATURES.md)), *why* it exists (see
[VISION.md](./VISION.md)), or *how the dataset represents knowledge*
(see [SCHEMA.md](./SCHEMA.md)). This document answers one question
only: **how do the parts of the system relate to each other?**

---

## Architectural Principles

These principles are non-negotiable constraints. Any implementation
decision that violates one of them is considered an architectural
regression, not a stylistic choice.

### 1. Interfaces depend on the Decision Engine. The Decision Engine never depends on interfaces.

The Decision Engine has no knowledge of FastAPI, HTML, JSON, a REST
API, a CLI, or an SDK. Its only responsibility is to receive a
context, apply decision logic against the dataset, and return an
explainable recommendation.

The web app is simply the first consumer of the Decision Engine. The
API, the SDK, and the CLI will later consume the exact same core,
without duplicating any business logic.

If every interface were deleted tomorrow, the Decision Engine would
continue to work exactly the same. If a new interface is added in the
future — a VS Code extension, a Telegram bot — it consumes the
existing core without modifying it.

### 2. The Decision Engine never contains knowledge about AI models.

The Decision Engine does not know what GPT, Gemini, or Claude are. It
only knows how to read data, apply rules, and return a result. All
knowledge about specific models lives in the dataset, never in code.

When a new model is released, the dataset is updated — not the
Decision Engine.

### 3. Rules are code. Data is data. The two are never mixed.

The Decision Engine reasons about **attributes and capabilities**
(`supports_spanish`, `cost_tier`, `latency_class`), never about
**names** (`"gemini"`, `"gpt"`, `"claude"`). Any logic that
special-cases a model by name violates this principle, regardless of
how small or well-intentioned the exception seems.

This is what makes Principle 2 enforceable in practice, not just in
intention.

---

## System Overview

Model Compass is organized around three clearly separated concerns:

```
dataset/        → knowledge (what models exist, and what they can do)
decision/       → logic (how a recommendation is produced)
interfaces/     → access (how a recommendation is consumed)
```

Data flows in one direction, from knowledge to logic to presentation:

```
dataset/models/*.yaml
        │
        ▼
    ┌─────────┐
    │ Loader  │   reads the dataset, produces domain objects
    └────┬────┘
         ▼
    ┌───────────┐
    │ Evaluator │   applies decision logic to a context + candidates
    └────┬──────┘
         ▼
    ┌───────────┐
    │ Explainer │   builds the reasoning behind the result
    └────┬──────┘
         ▼
    Recommendation (typed, presentation-agnostic)
         │
         ▼
    interfaces/web/   → renders HTML
    interfaces/api/*  → renders JSON        (future)
    interfaces/cli/*  → renders terminal output (future)
    interfaces/sdk/*  → returns the object as-is (future)
```

The Decision Engine's job ends at producing a `Recommendation` object.
Nothing downstream of that point is its concern.

---

## Repository Structure

```
model-compass/
│
├── dataset/
│   └── models/
│       ├── gemini-2.5-flash.yaml
│       ├── gpt-5-mini.yaml
│       └── claude-sonnet-5.yaml
│
├── decision/                    ← the core. Independent of every interface.
│   ├── domain/
│   │   ├── ai_model.py          entity: a model as read from the dataset
│   │   ├── context.py           entity: the user's input (use case, budget, priorities...)
│   │   ├── candidate.py         entity: a model evaluated against a context
│   │   └── recommendation.py    entity: the final, explainable result
│   ├── loader/                  reads dataset/, produces AIModel objects
│   ├── evaluator/                applies decision logic to Context + AIModel[] → Candidate[]
│   └── explainer/                turns Candidate[] into a Recommendation
│
├── interfaces/
│   └── web/                     the only consumer of decision/ in the MVP
│       # api/, sdk/, cli/ are added in the Developer Platform phase.
│       # Each future interface consumes decision/ and presents the
│       # resulting Recommendation in its own format.
│
├── docs/
│   ├── VISION.md
│   ├── ROADMAP.md
│   ├── FEATURES.md
│   ├── ARCHITECTURE.md
│   ├── SCHEMA.md
│   └── CONTRIBUTING.md
│
├── README.md
└── LICENSE
```

---

## Component Responsibilities

### `dataset/`

The single source of truth for knowledge about AI models. One YAML
file per model, human-readable and reviewable through Pull Requests.
The structure of an individual model file — its required and optional
attributes, types, and validation rules — is defined in
[SCHEMA.md](./SCHEMA.md), not here. This document only fixes *where*
the dataset lives and *how* it's organized at the file level.

### `decision/loader/`

Reads the dataset and converts it into `AIModel` domain objects.
Does not decide, does not explain, does not apply business rules.
Its only responsibility is to deliver structured objects to the rest
of the core.

### `decision/evaluator/`

Where the actual decision-making logic lives. Receives a `Context`
and a set of `AIModel` objects, and produces a list of `Candidate`
objects — each representing a model evaluated against that context.

Deliberately named `evaluator` rather than `scorer` or `rules`: it may
filter, weigh, discard, or rank candidates, and the specific technique
(rule-based logic today, potentially something else in the future) is
an implementation detail, not part of its name.

### `decision/explainer/`

Takes the `Candidate` objects produced by the evaluator and builds the
reasoning behind the outcome: which factors mattered, what trade-offs
exist, and which alternatives are relevant. Produces the final
`Recommendation` object. Has no knowledge of how that object will
later be displayed.

### `decision/domain/`

The shared domain model used across `loader/`, `evaluator/`, and
`explainer/`. A single, explicit definition of `AIModel`, `Context`,
`Candidate`, and `Recommendation`, so that no component defines its
own divergent version of the same concept. This mirrors, at the code
level, the same "single source of truth" principle already applied to
the dataset.

### `interfaces/`

Everything that consumes `decision/` and presents its output. Each
interface is responsible for adapting a `Recommendation` object into
its own format — HTML for the web, JSON for the API, plain text for
the CLI, the object itself for the SDK. This logic lives entirely
outside `decision/`, so the core never needs to know that any of these
interfaces exist.

Only `interfaces/web/` is part of the MVP. Other interfaces are added
according to [ROADMAP.md](./ROADMAP.md), each as its own self-contained
addition — never requiring changes to `decision/`.

---

## Open Implementation Decisions

Some decisions are intentionally left open at this stage, because
resolving them now would mean designing implementation details before
they're needed. They are noted here so they aren't forgotten, not
because they're unimportant:

- **Project tooling** — dependency management, test layout, and other
  implementation-level configuration. Deliberately not defined here.

### Resolved

- **Dataset validation** (was open, resolved when `decision/loader/`
  was implemented) — validation lives inside `loader/`, as part of
  turning a YAML file into an `AIModel`. A single component reading
  and validating the dataset was the simplest option for the set of
  rules `SCHEMA.md` currently defines; a separate validation step can
  be split out later if the rules grow enough to justify it.

---

## Why this shape

This structure exists to make one thing true, permanently: **the
Decision Engine can be reused by any future interface without being
modified, and the dataset can grow without touching a single line of
code.** Every boundary in this document exists to protect that
guarantee.
