# SCHEMA.md — Model Compass

This document defines the structure of a model entry in the Model
Compass dataset: which attributes exist, what type each one is, which
values are valid, and what a complete, valid entry looks like.

It does not explain why the dataset is organized the way it is at a
system level — see [ARCHITECTURE.md](./ARCHITECTURE.md) for that. This
document answers a narrower question: **how do we represent knowledge
about a single AI model?**

## Philosophy

> A model does not enter the dataset because it exists.
> It enters when it is fully characterized.

Model Compass does not aim to list every model on the market. It aims
to maintain a smaller set of models that are completely and reliably
documented. A dataset of 40 fully characterized models is more
valuable — and more trustworthy — than a dataset of 400 incomplete
ones.

This is why, in this version of the schema, **every field is
required**. If a model hasn't been fully evaluated yet, it simply
doesn't enter the main dataset until it has.

## Objective vs. Editorial Attributes

Every attribute in the schema belongs to one of two categories. This
distinction is the single most important thing to understand before
contributing to the dataset.

**Objective attributes** are facts that can be verified against public
provider documentation. They don't require judgment — they require
looking them up correctly. Examples: pricing, context window,
supported modalities.

**Editorial attributes** are qualitative evaluations made by the
project, based on public information, technical documentation, and
practical usage. They are not benchmark scores, and they don't claim
to be an absolute truth — they are a transparent, documented judgment
call. Examples: reasoning quality, integration ease, maturity.

Every field in this document is explicitly labeled `[Objective]` or
`[Editorial]`, so contributors always know whether they're expected to
cite a source or apply judgment.

Editorial attributes are not derived from benchmark scores. They are
based on the project's own editorial evaluation, informed by public
documentation and practical usage. Benchmarks may provide additional
context, but they are never the source of an editorial rating.

**Calibration is evidence-based, not family-based.** A model does not
inherit a lower — or higher — editorial rating simply because it is an
older generation, a smaller/cheaper tier, or shares a naming family
with an already-rated model. Every calibration must point to a
specific, sourced signal: a knowledge-cutoff gap, a stated or missing
capability (e.g. a deprecated or absent feature), an explicit provider
statement of relative positioning — never the version number by
itself. Two models one generation apart can carry identical ratings if
no such signal exists between them (e.g. Claude Opus 4.7 and Opus 4.8
in this dataset, rated identically despite being different releases,
because their sourced knowledge-cutoff dates match). Conversely, when
a signal exists but only affects part of a model's capability profile,
the degradation should be scoped to the dimension the evidence
actually supports, not applied uniformly across all four quality
dimensions.

---

## Schema

### Identity

| Field      | Type   | Category     | Description |
|------------|--------|--------------|--------------|
| `id`       | string | `[Objective]` | Unique slug for the model. Lowercase, hyphen-separated (e.g. `gemini-2.5-flash`). |
| `name`     | string | `[Objective]` | Display name of the model. |
| `provider` | string | `[Objective]` | Organization that provides the model. |
| `version`  | string | `[Objective]` | Model version, as published by the provider. |
| `license`  | string | `[Objective]` | One of: `proprietary`, `open-weights`, `open-source`. |

**A runtime mode is not a separate model.** If a provider exposes the
same underlying model with a toggle — e.g. Anthropic's
`thinking.type: "enabled"` parameter on Claude Sonnet 4.6 or Opus
4.6 — that's one dataset entry, not two. The signal to check: does the
provider's own API documentation assign it a distinct model ID? If
yes, it's a separate entry (e.g. Claude Haiku 4.5 really is a
different `id` from Sonnet 4.5). If it's a request parameter on the
same model ID, it stays one entry, and the mode itself isn't
represented in `SCHEMA.md` at all. This came up concretely with
Google Antigravity's UI, which lists "Claude Opus 4.6 (thinking)" as
if it were its own model — it isn't, per Anthropic's own API
reference, and third-party UI labeling never overrides that.

### Functional Capabilities

What the model is able to do. Binary, factual, verifiable against
provider documentation.

| Field                          | Type    | Category      |
|---------------------------------|---------|---------------|
| `capabilities.vision`           | boolean | `[Objective]` |
| `capabilities.audio`            | boolean | `[Objective]` |
| `capabilities.image_generation` | boolean | `[Objective]` |
| `capabilities.tool_calling`     | boolean | `[Objective]` |
| `capabilities.structured_output`| boolean | `[Objective]` |
| `capabilities.json_mode`        | boolean | `[Objective]` |

### Quality

How well the model performs across general capability dimensions.
Each quality dimension uses the same editorial quality scale (`low`,
`medium`, `high`, `very_high`).

| Field                             | Type | Category      |
|-------------------------------------|------|---------------|
| `quality.reasoning`                 | enum | `[Editorial]` |
| `quality.coding`                    | enum | `[Editorial]` |
| `quality.creative_writing`          | enum | `[Editorial]` |
| `quality.instruction_following`     | enum | `[Editorial]` |

This list is intentionally limited to general-purpose dimensions. It
does not include domain-specific dimensions (math, legal, medical,
etc.) in this version of the schema.

### Languages

| Field               | Type            | Category      | Description |
|----------------------|-----------------|---------------|--------------|
| `languages`          | list of strings | `[Objective]` | ISO 639-1 codes for languages the model officially supports. |
| `language_quality`   | map              | `[Editorial]` | Per-language quality, using the same scale as `quality.*`. Must include an entry for every language listed in `languages`. |

### Operational Characteristics

| Field                        | Type    | Category      | Description |
|--------------------------------|---------|---------------|--------------|
| `operational.context_window` | integer | `[Objective]` | Maximum input context, in tokens. |
| `operational.max_output`     | integer | `[Objective]` | Maximum output length, in tokens. |

Latency is intentionally excluded from this version of the schema.
Unlike quality or maturity, latency is not a property of the model
itself — it depends on the provider's infrastructure, region, load,
and endpoint, and can vary independently of the model. Representing it
as a single attribute would misrepresent it as an intrinsic property
of the model, which it is not.

### Cost

| Field                        | Type   | Category      | Description |
|--------------------------------|--------|---------------|--------------|
| `cost.input_per_million`     | number | `[Objective]` | USD cost per million input tokens. |
| `cost.output_per_million`    | number | `[Objective]` | USD cost per million output tokens. |

Cost tier (e.g. "low-cost", "premium") is not stored in the dataset.
It's a derived value, computed by the Decision Engine from the raw
prices above — this avoids the dataset going stale whenever pricing
changes.

The tier is a fixed $/million-token band over `cost.blended`
(`input_per_million + output_per_million`), not a rank relative to
whichever models happen to be loaded — a model's tier shouldn't drift
just because other models were added to or removed from the catalog:

| Tier | `cost.blended` |
|---|---|
| `low` | ≤ $2 |
| `medium` | $2–10 |
| `high` | $10–30 |
| `very_high` | > $30 |

These bands were chosen against the real distribution of the dataset's
`cost.blended` values (natural gaps between clusters of models), not
arbitrary round numbers — see `HANDOFF.md`, "Rediseño de Budget", for
the data behind them. `BudgetLevel` (the developer's stated budget)
mirrors these same four tiers, and acts as a hard ceiling: a model
whose tier exceeds the chosen `BudgetLevel` doesn't qualify.

### Ecosystem

| Field                       | Type | Category      | Allowed values |
|-------------------------------|------|---------------|-----------------|
| `ecosystem.integration_ease`| enum | `[Editorial]` | `low`, `medium`, `high` |
| `ecosystem.maturity`        | enum | `[Editorial]` | `experimental`, `stable`, `mature` |

### Access

| Field                       | Type    | Category      |
|-------------------------------|---------|---------------|
| `access.has_free_access`    | boolean | `[Objective]` |

**Definition, deliberately narrow:** there currently exists an official,
documented way to use this specific model without paying for API usage —
even if rate-limited, quota-capped, or otherwise restricted. `false` by
default. Only becomes `true` when a specific model has demonstrable official
free access from the provider's own documentation — never `true` by
inference, and never based on a one-time trial credit (that's temporary, not
continuous free access).

The boolean says whether a documented path exists — not how generous it is.
Exact limits, conditions, and expiry are not objective facts stable enough to
put in this schema (see `Docs/IMPLEMENTATION_NOTES.md`, Iteration #8: most
providers' rate limits are dynamic per-account dashboards or simply
undocumented, only one of six providers checked publishes a stable official
table). That detail stays in prose, in that model's `docs/models/{id}.md`
Access section, the same place other access nuance (subscription tiers,
multi-surface access) already lives.

---

## Example — `gemini-2.5-flash.yaml`

```yaml
id: gemini-2.5-flash
name: Gemini 2.5 Flash
provider: Google
version: "2.5"
license: proprietary

capabilities:
  vision: true
  audio: true
  image_generation: false
  tool_calling: true
  structured_output: true
  json_mode: true

quality:
  reasoning: high
  coding: high
  creative_writing: medium
  instruction_following: high

languages: [en, es, pt]
language_quality:
  en: very_high
  es: high
  pt: medium

operational:
  context_window: 1000000
  max_output: 8192

cost:
  input_per_million: 0.15
  output_per_million: 0.60

ecosystem:
  integration_ease: high
  maturity: stable

access:
  has_free_access: false
```

*Values in this example are illustrative and may not reflect the
model's current real-world specifications. The dataset entry, not this
document, is the source of truth for actual values.*

---

## Validation Rules

- Every field listed in this schema is **required**. A model entry is
  not considered valid — and is not accepted into the main dataset —
  until every field is present.
- `id` must be unique across the entire dataset and match the YAML
  filename (`dataset/models/{id}.yaml`).
- Every language in `language_quality` must also appear in `languages`,
  and vice versa.
- Enum fields must use one of the exact allowed values listed above —
  no free-text substitutes.
- `cost.input_per_million` and `cost.output_per_million` must be
  non-negative numbers.
- `operational.context_window` and `operational.max_output` must be
  positive integers.
- `access.has_free_access` must be a boolean.

## Contributing a New Model

Adding a model to the dataset means creating one new YAML file under
`dataset/models/`, following this schema exactly, with every field
completed — objective fields sourced from official documentation,
editorial fields evaluated according to the criteria above.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full contribution
process.
