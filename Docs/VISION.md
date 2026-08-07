# VISION.md — Model Compass

> "Developers don't need more information.
> They need better decisions."

## Mission

Help developers choose the most suitable AI model for their use case
through a transparent and explainable recommendation engine.

## The problem

Choosing an AI model today means digging through scattered provider
documentation, comparing benchmarks that don't reflect the actual use
case, and relying on loose opinions from forums or social media.

This costs developers hours when all they need is a simple answer:
**what model should I use for this?**

Model Compass exists to answer that question with judgment, speed,
and transparency.

## Users

**Primary user:** the software developer (individual or part of a
small team) who needs to integrate an AI model into an application
and wants to decide without spending hours on research.

**Secondary users:** startups, CTOs, and companies evaluating which
provider/model to adopt at an organizational level.

The developer is the hero of this product. Every product decision
starts from that perspective.

## Philosophy

Model Compass does not try to answer which model is the best.

It tries to answer which model is the most suitable for a specific
context.

The right choice depends on the problem, not on the model. That's why
the project focuses on understanding the user's needs first, and then
recommending the most appropriate option through a transparent and
explainable system.

## What Model Compass is

A recommendation engine that:

- Takes the user's context as input (use case, budget, priorities,
  language, volume, etc.).
- Cross-references that context against a curated, versioned dataset
  of AI models available on the market.
- Returns an **explained** recommendation, not just a model name.

It recommends models.
It explains why.
It exposes the trade-offs behind every recommendation.

## What it is NOT / does NOT do

- Does not run its own benchmarks.
- Does not execute models or call inference APIs.
- Does not replace official provider documentation.
- Does not measure quality through automated testing.
- Does not do prompting or compare model outputs.
- Does not rank by popularity alone.
- Does not make the final decision for the user — it informs it.
- Does not show a number or claim that looks like real data when it's
  actually an invented assumption. Usage-volume estimates, decorative
  confidence scores, and quality scoring for a mix of models are only
  ever shown when the engine can actually derive them — never guessed
  to fill a visual gap.

## What a recommendation looks like

Explainability is a non-negotiable requirement. The system never
responds with just a model name:

> ❌ "Recommended model: Gemini"

It responds with the reasoning behind it:

> ✅
> **Gemini 2.5 Flash**
>
> Because:
> - Your priority was cost
> - You need Spanish language support
> - You don't need advanced reasoning
> - You have 3,000 users
> - Your budget is low

## Vendor neutrality

Model Compass does not promote or favor any provider.

Every recommendation is based on the user's context and the project's
recommendation rules. The same provider may be recommended for one
scenario and not recommended for another.

The project's commitment is to the developer's success, not to any
AI vendor.

## Source of truth

The project maintains its own **dataset, versioned in Git**, based
on publicly available provider information and manually curated.

The community can contribute via Pull Requests, but every change is
reviewed before being merged into the main dataset.

The recommendation logic is deterministic. Recommendations are based
on explicit rules and curated data — not on opaque AI-generated
opinions.

This guarantees the data and the logic are:

- **Reproducible** — anyone can see exactly what data and rules were
  used in a recommendation, and when they changed.
- **Transparent** — the dataset and the rules are public, not a
  black box.
- **Auditable** — every change is tracked in Git history.

## Product access evolution

| Phase | Access form | Why in this order |
|-------|-------------|--------------------|
| MVP   | Web app     | Accessible to anyone, no installation friction |
| v2    | API         | Enables integrating recommendations into other tools |
| v3    | Python SDK  | Direct use from code, for developers automating workflows |
| v4    | CLI         | Terminal-first usage, for developers who live in the shell |

The web maximizes initial reach. The API, SDK, and CLI expand the
surface of use once the recommendation engine and dataset are mature
and validated.

## Tone and identity

The project should feel like Stripe, Vercel, FastAPI, or Docker:
minimalist, but well explained. Developer-first.

The official tone is direct, clear, and technical — avoiding
unnecessary corporate language and emoji-heavy marketing speak. The
priority is explaining decisions simply and transparently, not
sounding like a sales pitch.

## What success looks like

Success is not measured by the number of models supported or the
volume of users. It's measured by the confidence developers place in
the tool when making technical decisions.

Community adoption is a consequence. Developer trust is the goal.

A successful project is one that lets a developer confidently answer:

> "What model should I use for this case?"

in under a minute, while understanding *why* that recommendation was
made.

In the long term, success also means becoming an open, trustworthy
reference for the community — with a transparently maintained
dataset and high-quality contributions.
