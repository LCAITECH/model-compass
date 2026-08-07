# GPT-4o

Dataset entry: [`dataset/models/gpt-4o.yaml`](../../dataset/models/gpt-4o.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Why this model — a PoC, not a routine addition

This is the project's first "previous-generation, still in production"
model, added deliberately as a proof of concept: can the Decision
Engine surface "this is outdated, consider migrating" **using only
real data**, with no `legacy` field, no special-casing, nothing added
to `SCHEMA.md`? See `tests/test_evaluator.py::test_gpt_4o_is_dominated_by_a_newer_cheaper_model`
for the answer, verified against this dataset entry directly: GPT-4o
costs more than GPT-5 Mini while matching or losing on every quality
dimension the schema tracks. No schema change was needed to make that
visible — the numbers already say it. If a future model needs
something this approach genuinely can't express, that's a real reason
to revisit `SCHEMA.md`; this PoC alone isn't that reason.

## Identity

| Field      | Value          |
|------------|----------------|
| `id`       | `gpt-4o`       |
| `name`     | GPT-4o         |
| `provider` | OpenAI         |
| `version`  | `4o`           |
| `license`  | `proprietary`  |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Input: text and images. |
| `audio`                | false | Not supported (this dataset entry is text/image GPT-4o, not the separate real-time voice product). |
| `image_generation`     | false | Output is text-only, including structured outputs. |
| `tool_calling`         | true  | Confirmed. |
| `structured_output`    | true  | Confirmed. |
| `json_mode`            | true  | Confirmed explicitly — OpenAI's own model card states "Structured outputs: Yes, including JSON mode." Unlike GPT-5/GPT-5 Mini, this one didn't need to be marked pending. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `medium` | A 2024-era general-purpose model; OpenAI's reasoning-focused work since then (the o-series, then GPT-5) has moved the frontier well past it. Rated on today's landscape, not on how it compared at release. |
| `coding`                   | `medium` | Same reasoning as above. |
| `creative_writing`         | `medium` | No standout signal either way. |
| `instruction_following`    | `high`   | GPT-4o was and remains well-regarded specifically for reliable instruction following — this held up better over time than raw reasoning/coding did. |

**This is the editorial core of the PoC.** These ratings put GPT-4o at
or below GPT-5 Mini on every dimension, while GPT-4o costs roughly 5-10x
more (see Cost below). That gap is the whole "should I migrate?" signal
— it comes from rating the model honestly against 2026's landscape, not
from a special flag.

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `gpt-5`/`gpt-5-mini` (same provider, same known gap, see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value    |
|----------------------|----------|
| `context_window`      | 128,000  |
| `max_output`           | 16,384   |

Confirmed directly against the official model card. Notably smaller
than GPT-5/GPT-5 Mini's 400,000-token window — another real,
non-editorial data point in the same direction as the quality ratings.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $2.50  |
| `output_per_million`        | $10.00 |

Confirmed directly against OpenAI's pricing page (standard tier; a
$1.25/M cached-input rate also exists, not captured by the schema,
same kind of nuance logged for other models in
[IMPLEMENTATION_NOTES.md, Iteration #5](../IMPLEMENTATION_NOTES.md#iteration-5)).
For comparison: GPT-5 Mini costs $0.25/$2.00 — GPT-4o's blended cost
($12.50) is roughly 5.5x GPT-5 Mini's ($2.25) for equal-or-worse
quality on this dataset's dimensions.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same OpenAI API surface as the GPT-5 line. |
| `maturity`              | `stable` | OpenAI's own docs describe it as **not deprecated**, still generally available. Worth flagging as a slightly odd signal: the same page also calls it "our most capable model outside of our o-series models" and "recommended as the best option for most general tasks" — language that reads as stale relative to GPT-5's existence, not something this project treats as current guidance. `maturity: stable` reflects availability, not a claim that OpenAI's marketing copy is still accurate. |

---

## Sources

- [GPT-4o model card](https://developers.openai.com/api/docs/models/gpt-4o) — capabilities, context window, max output, knowledge cutoff (Oct 1, 2023), availability status.
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — cost fields.

Both accessed 2026-08-07, official OpenAI documentation only.

## Verification result

New dataset entry, not a re-verification. All objective fields
confirmed, including `json_mode` (unusually, explicitly — most other
entries in this catalog have it flagged as inherited/pending). This is
the cleanest-sourced entry in the dataset so far.
