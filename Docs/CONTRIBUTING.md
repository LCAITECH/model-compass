# CONTRIBUTING.md — Model Compass

Thank you for considering contributing to Model Compass.

The project is in its early stages. Right now, the main way to
contribute is through the dataset — the curated collection of AI
model entries that powers every recommendation.

## Before opening a Pull Request

Please read:

- [VISION.md](./VISION.md)
- [SCHEMA.md](./SCHEMA.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)

Understanding the philosophy of the project is more important than
submitting code quickly. Model Compass has a small number of
principles — vendor neutrality, the separation between objective and
editorial data, deterministic recommendations — that every
contribution needs to respect. A technically correct Pull Request can
still work against these principles, so understanding them first will
save you time and help your contribution get merged smoothly.

## Contributing to the dataset

This is the primary way to contribute today.

### Model admission criteria

This is the general rule for whether a model enters `dataset/models/`
at all — it governs every contribution below, not just how to fill out
a YAML file:

> **If a field has no clear official source, it is not added as hard
> data.** It gets marked as pending instead, and the model does not
> enter the main dataset until every required field has one.

This follows directly from `SCHEMA.md`'s own philosophy — "a model
does not enter the dataset because it exists, it enters when it is
fully characterized" — made explicit as a standing admission
criterion, not just a per-field guideline. A model with 11 of 12
required fields cleanly sourced and one guessed is not a 92%-complete
contribution. It's not ready. Open a discussion or a draft PR flagging
the missing field instead of filling it with a best guess — a
half-verified entry is worse than an honest gap, because it looks the
same as a fully verified one to anyone using the tool downstream.

The same standard applies to `docs/models/{id}.md`, the audit-trail
companion to each dataset entry (see
[`docs/models/README.md`](../docs/models/README.md)): every field
either cites where it came from, or is explicitly marked as not
independently confirmed. Third-party aggregators (OpenRouter, pricing
trackers, etc.) are never an acceptable source for objective fields —
see [IMPLEMENTATION_NOTES.md, Iteration #2](./IMPLEMENTATION_NOTES.md#iteration-2)
for why.

### Adding a new model

1. Create a new file at `dataset/models/{model-id}.yaml`.
2. Follow the structure defined in [SCHEMA.md](./SCHEMA.md) exactly —
   every field is required.
3. Fill in **objective fields** using official, publicly available
   provider documentation. Where a value isn't obvious, prefer the
   provider's own docs over third-party sources.
4. Fill in **editorial fields** using your own informed judgment,
   based on public documentation and practical usage — not on
   benchmark scores. If you're not confident evaluating an editorial
   field for a given model, it's better to leave the contribution
   incomplete and open a discussion than to guess. Calibration must be
   evidence-based, not family-based — don't downgrade (or upgrade) a
   rating just because a model is an older generation or a
   smaller/cheaper tier than a sibling already in the dataset; point to
   a specific sourced signal instead. See
   [SCHEMA.md](./SCHEMA.md#objective-vs-editorial-attributes) for the
   full principle and a worked example.
5. Open a Pull Request with a clear description of the model being
   added.

### Updating an existing model

Provider pricing, capabilities, and specs change over time. If you
notice a model entry is outdated:

1. Update only the fields that changed.
2. Explain what changed and, where possible, link to the source that
   confirms it (for objective fields).
3. Open a Pull Request.

### What makes a good dataset contribution

- Objective fields are accurate and verifiable.
- Editorial fields are thoughtful, not guessed.
- The entry respects the schema exactly — no extra fields, no
  shortcuts, no renamed keys.
- The model doesn't reintroduce attributes that were deliberately
  excluded from the schema (e.g. `cost_tier`, `latency_class`) — see
  [SCHEMA.md](./SCHEMA.md) for why.

## Contributing code

Model Compass is implemented and functional end-to-end — the decision
engine (`decision/loader` → `evaluator` → `explainer`) and the web
interface (`interfaces/web/`) both exist and are tested. The
architecture is defined in [ARCHITECTURE.md](./ARCHITECTURE.md); read
it before touching `decision/` — its three non-negotiable principles
(one-way dependency from `interfaces/` to `decision/`, no model names
in decision logic, rules-as-code/data-as-data) apply to every code
contribution, not just the maintainer's own work.

To run the project locally: `pip install -e ".[dev]"`, then `pytest`
for the test suite or `uvicorn interfaces.web.app:app --reload` for the
web interface. See [README.md](../README.md#getting-started) for
details.

## Review process

Every contribution — to the dataset or, later, to the code — is
reviewed by the project maintainer before being merged. There is no
formal governance process yet; as the project grows, this may evolve,
as described in [ROADMAP.md](./ROADMAP.md).

## Vendor neutrality

Model Compass does not favor any AI provider. Contributions that
introduce bias toward or against a specific provider — in the dataset,
in code, or in documentation — will not be accepted, regardless of
intent.

## A note on principles

Some contributions may be technically valid but conflict with the
project's core principles — for example, hardcoding logic around a
specific model name, storing a value that should be derived instead
of stored, or introducing a qualitative field disguised as an
objective one.

These will be declined with an explanation, not out of rigidity, but
because the principles behind Model Compass are as much a part of the
project as the code and the data themselves.
