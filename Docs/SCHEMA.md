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
| `operational.max_output`     | integer or `null` | `[Objective]` | Maximum output length, in tokens. `null` means the provider publishes no output ceiling; the key must still be present. Never a placeholder. When a provider documents a default and a higher maximum, store the default and record the maximum in the model's `Docs/models/` page. |

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
| `cost.effective_until`       | date (ISO 8601 string), optional | `[Objective]` | Last day the current price above is guaranteed to hold, when the provider has published a known expiration for an introductory rate. Absent for a model with an ordinary, non-time-limited price. |
| `cost.reverts_to.input_per_million` | number, optional | `[Objective]` | USD/million input tokens the price reverts to once `effective_until` passes. Required together with `effective_until` — never one without the other. |
| `cost.reverts_to.output_per_million` | number, optional | `[Objective]` | USD/million output tokens the price reverts to once `effective_until` passes. |

`cost.effective_until`/`cost.reverts_to` are **display-only** — the
Decision Engine always ranks and tiers on the current
`input_per_million`/`output_per_million` above, never on the future
reverted price. First added 2026-08-17 (`gemini-3.6-flash`,
`gemini-3.7-flash`) after both models' current price turned out to be
a temporary introductory rate with a provider-published expiration
date; see `Docs/IMPLEMENTATION_NOTES.md`, Iteration #13. Nothing in
this project re-checks these fields automatically once
`effective_until` passes — updating `cost.*` back to the reverted
price on that date is still a manual dataset edit; since 2026-10-14
`tests/test_catalog_dates.py` fails the suite from the day after
`effective_until` until it is done (see Lifecycle below).

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
documented way to use this specific model without paying — even if
rate-limited, quota-capped, or otherwise restricted. Two paths count: a
free tier of the provider's API (Google's Gemini API free tier, for
several Gemini models), or the provider's free consumer plan when the
provider's own page names that exact model (Claude.ai's Free plan for
Claude Haiku 5.5). `false` by default. Only becomes `true` when a specific
model has demonstrable official free access from the provider's own
documentation — never `true` by inference or by family name, never based
on a one-time trial credit (that's temporary, not continuous free
access), and never for a paid plan, however cheap. The consumer path was
added on 2026-10-15 (owner decision, `Docs/IMPLEMENTATION_NOTES.md`,
Iteration #32); before that the field counted only free API tiers.

The boolean says whether a documented path exists — not how generous it
is, nor which of the two it is: a model's Access section in
`docs/models/{id}.md` says which, because a free chat app is not a way to
build an application on the model.
Exact limits, conditions, and expiry are not objective facts stable enough to
put in this schema (see `Docs/IMPLEMENTATION_NOTES.md`, Iteration #8: most
providers' rate limits are dynamic per-account dashboards or simply
undocumented, only one of six providers checked publishes a stable official
table). That detail stays in prose, in that model's `docs/models/{id}.md`
Access section, the same place other access nuance (subscription tiers,
multi-surface access) already lives.

### Lifecycle

| Field                       | Type | Category      | Allowed values |
|-------------------------------|------|---------------|-----------------|
| `lifecycle.status`          | enum | `[Objective]` | `active`, `deprecated`, `restricted` |
| `lifecycle.release_date`    | date (ISO 8601 string) or `null` | `[Objective]` | The day the provider first made the model available through its API. |
| `lifecycle.shutdown_date`   | date (ISO 8601 string) or `null` | `[Objective]` | The specific date the provider publishes for turning the model off. |
| `lifecycle.replacement`     | model id or `null` | `[Objective]` | The successor the provider names, when it is a model in this dataset. |

Sourced from the provider's own deprecations or lifecycle page, never
from an aggregator. Every key is required, `null` included, the same
rule as `operational.max_output`: "the provider publishes no date" has
to be written down, so a missing key can't pass for a checked one.

- **`status`** is `deprecated` once the provider has announced the
  model is going away, or already serves its requests with a successor
  (Google's "the endpoint ... automatically routes API requests to"
  wording). Providers use different words for the same thing (Anthropic
  "Deprecated", OpenAI "deprecated"/"shut down", Google a shutdown date
  plus a recommended replacement); the provider's page decides, and the
  entry's YAML comment cites it. `restricted` is a model the provider
  still serves and says is *not* deprecated, but has closed to new
  developers (Google's "limited to users who have actively used them in
  the past", for Gemini 2.5). `active` is everything else, including
  Anthropic's "Legacy".
- **`shutdown_date`** is a specific date, never a "not sooner than"
  floor: Anthropic gives every active model one ("not sooner than
  2027-09-28") and it promises nothing. An `active` model can carry a
  `shutdown_date` when the provider publishes one without announcing a
  deprecation (`gemini-3.1-flash-lite`, 2027-05-07): it is shown, not
  filtered.
- **`release_date`** is the provider's own date for the model's first
  API availability: Anthropic's per-model "Released" field, the release
  date column of Google's deprecations page, OpenAI's API changelog,
  DeepSeek's and Alibaba's release notes, Mistral's model card. For a
  preview that later went GA it is the first public API date (DeepSeek
  V4 Pro: 2026-04-24, GA 2026-08-13). Never a snapshot date read off a
  model id, and never a blog date for a model that was not yet callable.
  Display-only: it drives the "New" badge (released in the last 30 days,
  `interfaces/web/catalog_notices.py`), never the ranking. Added
  2026-10-14, Iteration #30.
- **`replacement`** must be the id of another model in this dataset;
  the loader checks it across files. If the provider's successor isn't
  in the catalog, it is `null` and the successor is named in that
  model's `Docs/models/{id}.md`. For a `restricted` model whose provider
  only gives general advice ("use 3.5 Flash-Lite or 3.8 Flash"), the
  per-model pick is the project owner's and its YAML comment says so.

Unlike `ecosystem.maturity` (an editorial call about stability), this
block decides something: **the Decision Engine never recommends a
`deprecated` model.** It is a hard filter, like language and budget:
the model is listed among the exclusions with the provider's date and
successor, so the user sees why. Recommending it for new work would be
advice the provider itself contradicts. First added 2026-10-14; see
`Docs/IMPLEMENTATION_NOTES.md`, Iteration #28. A `restricted` model is
excluded the same way, with a reason saying the provider limits it to
developers who already used it: a new project cannot start on it. Added
2026-10-15 (owner decision), Iteration #29.

Nothing in `decision/` reads the calendar: on the shutdown date the
engine behaves exactly as the day before. Removing the model (its YAML
and its access routes) on that date is a manual dataset edit, enforced
by `tests/test_catalog_dates.py`, which fails from the first day a
`shutdown_date` or a `cost.effective_until` has passed and warns during
the 30 days before.

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

lifecycle:
  status: active
  release_date: "2025-06-17"
  shutdown_date: null
  replacement: null
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
- `operational.context_window` must be a positive integer.
  `operational.max_output` must be a positive integer, or `null` when
  the provider publishes no output ceiling (the key may not be omitted).
- `access.has_free_access` must be a boolean.
- `lifecycle.status`, `lifecycle.release_date`,
  `lifecycle.shutdown_date` and `lifecycle.replacement` must all be
  present. Both dates are quoted ISO date strings or `null`, and a
  `release_date` must come before a `shutdown_date`; `replacement` is
  `null` or the id of another model in the dataset, never the model
  itself.
- No dated fact may be in the past: a `cost.effective_until` or
  `lifecycle.shutdown_date` that has passed fails the test suite
  (`tests/test_catalog_dates.py`) until the entry is updated.

## Subscription plans

Consumer plans live in `dataset/subscriptions/{provider}/{plan_id}.yaml`,
a separate catalog from the models. A plan never lists the models it
includes: an access route (`dataset/access_routes/`) names the plan in
its `consumer_subscription` requirement, and only where the provider's
own page names that exact model (never a family). Every field is
`[Objective]` and sourced from the provider's own pages, with the URLs
in a YAML comment, the same rule as `lifecycle`.

| Field                           | Type | Allowed values |
|---------------------------------|------|----------------|
| `provider`, `plan_name`         | string | As the provider writes them. |
| `surface_entitlements`          | list of surfaces | Where the plan applies (display only). |
| `documented_exclusions`         | list of strings | What the plan does not cover, in English. |
| `region_scope`                  | string | Usually `account_dependent`. |
| `source_url`, `consulted_at`, `status` | string, ISO date, evidence status | The plan's main source. |
| `price.monthly_usd`             | number > 0 | US list price, monthly billing, before tax. |
| `usage_multiplier`              | mapping or `null` | `relative_to` (another plan_id), `factor` (> 0), `scope` (what is multiplied, in the provider's words). |
| `api_credits`                   | mapping or `null` | `monthly_usd` (> 0), `surface` (where they are spent), `conditions` (expiry, separate account, exclusions). |

- **No plan limit is stored as a number.** No provider publishes a
  plan's usage limit in tokens, so nothing here pretends to: the
  multiplier is the provider's own "5x Pro" statement, kept as a factor
  and a scope, and it is never converted into tokens.
- **`price.monthly_usd`** is the US list price. Regional prices and
  taxes differ, which is why the site prefills it and lets the visitor
  change it. A plan with several tiers at different prices is several
  plans (`claude-max-5x`, `claude-max-20x`).
- **`usage_multiplier`** is `null` when the provider publishes no
  number, or only one against a tier that is not a plan in this catalog
  (Free). `relative_to` must name another plan in the catalog; the
  loader checks it across files.
- **`api_credits`** is `null` when the plan includes none. When it
  does, it states the monthly amount and where it can be spent; a page
  may translate that amount into the tokens it buys at a model's list
  prices, which is exact, never into plan usage.
- `price`, `usage_multiplier` and `api_credits` are required keys,
  `null` allowed for the last two. Approved by the owner on 2026-10-14,
  added 2026-10-15;
  see `Docs/IMPLEMENTATION_NOTES.md`, Iteration #31.

Plans are read by the Access Advisor (`decision/access/`) and never by
the evaluator: nothing about a plan changes which model is recommended.

## Contributing a New Model

Adding a model to the dataset means creating one new YAML file under
`dataset/models/`, following this schema exactly, with every field
completed — objective fields sourced from official documentation,
editorial fields evaluated according to the criteria above.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full contribution
process.
