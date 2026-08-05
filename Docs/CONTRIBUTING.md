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
   incomplete and open a discussion than to guess.
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

Model Compass doesn't have an implementation yet — the project is
currently documentation-first, and the architecture is defined in
[ARCHITECTURE.md](./ARCHITECTURE.md).

Code contributions will open once the MVP implementation begins.
Guidelines for setting up the project, running it locally, and
submitting code will be added at that point.

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
