# AGENTS.md — Model Compass

Instructions for AI coding agents (and anyone reaching for one) working
in this repository. Read this before writing any code here — it exists
so implementation sessions don't quietly drift from decisions already
made.

This file is not one of the project's 7 official documents
(`VISION.md`, `README.md`, `ROADMAP.md`, `FEATURES.md`,
`ARCHITECTURE.md`, `SCHEMA.md`, `CONTRIBUTING.md`). It doesn't replace
them — it's a pre-flight checklist that points back to them. If
anything here ever conflicts with those documents, the documents win;
raise the conflict instead of resolving it silently.

## Read before coding

1. [`Docs/ARCHITECTURE.md`](Docs/ARCHITECTURE.md) — the non-negotiable
   principles and the component boundaries.
2. [`Docs/SCHEMA.md`](Docs/SCHEMA.md) — the dataset structure and its
   Objective vs Editorial distinction.
3. [`Docs/IMPLEMENTATION_NOTES.md`](Docs/IMPLEMENTATION_NOTES.md) — the
   running log of implementation friction. Check it before assuming a
   schema or architecture gap is new.

## Hard constraints — never violate these, even if asked

These come directly from `ARCHITECTURE.md`. Code that violates one of
them is a regression, not a stylistic choice, no matter how small or
how functional it looks.

1. **`decision/` never imports from `interfaces/`.** Dependencies flow
   one way: `interfaces/` depends on `decision/`, never the reverse. If
   every interface were deleted, `decision/` and its tests must still
   work exactly the same.
2. **`decision/` never contains a model name.** No
   `if model_id == "gemini-2.5-flash"`, no `if provider == "OpenAI"`,
   anywhere in `decision/evaluator/` or `decision/explainer/`. Reason
   only about attributes (`capabilities.vision`, `quality.reasoning`,
   `cost.input_per_million`, ...), never about identity. If a use case
   seems to need a name check, the missing piece is an attribute in
   `SCHEMA.md`, not a name check in code — raise it, don't work around
   it.
3. **Rules are code, data is data.** Nothing that belongs in a model's
   YAML entry gets hardcoded into `decision/`, and nothing that's
   actually decision logic gets smuggled into the dataset as a field
   whose real purpose is to encode a rule.

## Schema and architecture discipline

`SCHEMA.md` is not modified reactively. If a model's real-world data
doesn't fit cleanly:

1. Do **not** edit `SCHEMA.md` to accommodate it.
2. Log the friction in `Docs/IMPLEMENTATION_NOTES.md`, same format as
   the existing entries (`Observation` / `Current decision` /
   `Status`).
3. Only propose an actual `SCHEMA.md` change once the same friction has
   shown up independently 2-3 times — and propose it to the user
   explicitly, don't just make the edit.

The same discipline applies to `ARCHITECTURE.md`'s "Open Implementation
Decisions": resolve one when the relevant component is actually built
(see its "Resolved" section for the pattern), not speculatively ahead
of time — and record the resolution there when you do.

## Dataset discipline

- Objective fields (`SCHEMA.md`, `[Objective]`) must be sourced from
  the provider's own official documentation — never from aggregators
  (OpenRouter, pricing trackers, etc.). Aggregators have repeatedly
  shown stale or version-mismatched numbers during this project's own
  dataset curation (see `IMPLEMENTATION_NOTES.md`, Iteration #2).
- Editorial fields (`[Editorial]`) are judgment calls, never derived
  from benchmark scores. If you're not confident making the call, say
  so instead of guessing.
- A model does not enter `dataset/models/` until every field in the
  schema is filled in. No partial entries in the main dataset.
- Run the loader's validation against any new or edited YAML before
  considering the work done — `pytest` must pass.

## Implementation order

Already agreed — don't reorder without discussing it first:

`Loader` (done) → `Evaluator` → `Explainer` → `interfaces/web/`.

Don't start `interfaces/` work while `decision/` is unfinished, and
don't add scaffolding for a future phase (API, SDK, CLI) before its
turn in `ROADMAP.md`.

## Tooling already decided

- Python 3.11+, stdlib only in `decision/` besides `pyyaml` for the
  loader. No Pydantic, no third-party validation framework — plain
  `dataclasses` + `Enum` for domain objects.
- `pytest` for tests. Tests exercise the real files in
  `dataset/models/`, not mocks of them.
- No Poetry, no uv — `pyproject.toml` + `pip install -e ".[dev]"`.
- Don't introduce a new dependency, linter, or formatter without
  flagging it first — this list is the whole toolchain on purpose.

## Tone

Minimalist, direct, technical — the project's own reference points are
"Stripe, Vercel, FastAPI, Docker." No hype emojis (🚀🔥✨) in docs, code
comments, commit messages, or error messages. Explain the *why*, not
the *what* — identifiers and structure should already say what
something does.

## When something doesn't fit this file

Say so and ask, instead of picking the closest existing pattern and
running with it. Silent judgment calls on architecture-level decisions
are exactly what this file exists to prevent.
