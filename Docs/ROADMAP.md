# ROADMAP.md — Model Compass

This roadmap describes how Model Compass evolves — not when. There are
no fixed dates or quarters attached to these phases.

Each phase represents a level of maturity for the project. A phase is
considered complete when its qualitative goals are met, not when a
deadline is reached. Quality takes priority over speed.

Progress is not measured by the number of models supported, lines of
code written, or number of contributors. It is measured by the level
of maturity reached at each stage.

---

## Phase 1 — Foundation

**Status: Complete.**

The base the entire project is built on: identity, documentation,
project structure, and the initial dataset.

The dataset is public from day one. Community contributions via Pull
Requests are open from the start and reviewed before merging — this is
a founding principle of the project, not a future milestone.

**Includes:**
- Project identity: name, principles, philosophy, and license
- Core documentation (VISION, README, ROADMAP, FEATURES, ARCHITECTURE,
  SCHEMA, CONTRIBUTING)
- Repository structure and contribution workflow
- Dataset schema definition
- Initial curated dataset, published and open to Pull Requests
- MIT License

**Phase complete when:**
Project identity is defined, core documentation is consolidated, the
project structure is stable, and the initial dataset is defined and
published.

---

## Phase 2 — Decision Engine

**Status: Complete.**

The core of the product: the decision logic itself, designed and
validated independently of any user interface.

**Includes:**
- Deterministic, rule-based recommendation logic
- Scoring and explainability model
- Trade-off reasoning behind every recommendation
- Validation against the project's primary use cases

**Phase complete when:**
The engine can produce deterministic, explainable, and coherent
recommendations for the project's primary defined use cases.

---

## Phase 3 — Web Platform

**Status: Functionally complete — not yet announced as MVP.** The
end-to-end experience works and is tested; whether it's ready to call
"MVP, public and announced" is the project owner's call to make, not a
technical one — see this phase's own "complete when" criterion below.

The first user-facing product: a web application that lets any
developer use the Decision Engine without installing anything.

**Includes:**
- End-to-end web experience: enter context, receive a reasoned
  recommendation
- Presentation of recommendations, reasoning, and trade-offs
- Public-facing MVP

**Phase complete when:**
A user can go through the complete experience — from entering their
context to receiving a reasoned recommendation — end to end.

---

## Phase 4 — Developer Platform

**Status: Not started.**

Expanding access beyond the browser, for developers who want to
integrate Model Compass directly into their own tools and workflows.

**Includes:**
- Public API
- Python SDK
- CLI

**Phase complete when:**
The API, SDK, and CLI offer a consistent and stable experience for
integrations.

---

## Phase 5 — Community & Governance

**Status: Not started** as a distinct phase — though note the "note on
ordering" below: community contributions have been open since Phase 1
by design, this status is about the *governance maturity* this phase
specifically tracks.

This phase is not about opening the project to the community — that
happens from Phase 1. It's about maturing how the project is governed
as it grows.

**Includes:**
- Formal contribution and review processes
- Defined maintainers
- Dataset quality standards at scale
- Criteria for accepting contributions
- A more structured governance model, if and when it becomes necessary

**Phase complete when:**
The project can sustain third-party contributions through clear,
maintainable processes — without depending exclusively on a single
person.

---

## A note on ordering

Some activities naturally continue across multiple phases.

For example, dataset curation begins in Foundation but remains an
ongoing responsibility throughout the life of the project.

The roadmap defines maturity milestones, not isolated work streams.
