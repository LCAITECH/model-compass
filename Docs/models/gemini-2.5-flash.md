# Gemini 2.5 Flash

Dataset entry: [`dataset/models/gemini-2.5-flash.yaml`](../../dataset/models/gemini-2.5-flash.yaml)
Last verified: 2026-08-07

This document is not a second dataset. The YAML file above is the only
value the Decision Engine reads — this page is its audit trail: where
each value came from, and the reasoning behind every editorial call.
See [SCHEMA.md](../SCHEMA.md) for what each field means and the
Objective/Editorial distinction used throughout.

---

## Identity

| Field      | Value                |
|------------|-----------------------|
| `id`       | `gemini-2.5-flash`    |
| `name`     | Gemini 2.5 Flash      |
| `provider` | Google                |
| `version`  | `2.5`                 |
| `license`  | `proprietary`         |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Input modalities: text, image, video, audio. |
| `audio`                | true  | Audio input supported; audio *generation* is not (see Cost note below — priced separately from text). |
| `image_generation`     | false | Explicitly listed as unsupported by the model card. |
| `tool_calling`         | true  | "Function calling" in Google's docs. |
| `structured_output`    | true  | |
| `json_mode`            | true  | Via `response_mime_type: application/json`. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `high`      | Marketed by Google as "our best price-performance model ... that require reasoning," with an explicit thinking-mode; not positioned as the top-tier reasoning model in Google's own lineup (that's Gemini 2.5 Pro), so `high` rather than `very_high`. |
| `coding`                   | `high`      | Consistent with general-purpose high-tier positioning; no coding-specific benchmark is treated as authoritative here, per `SCHEMA.md`'s rule that editorial fields aren't derived from benchmark scores. |
| `creative_writing`         | `medium`    | Flash-tier models are optimized for latency/cost over stylistic depth; judgment call, not a benchmark result. |
| `instruction_following`    | `high`      | Consistent with the model's positioning for high-volume, tool-using tasks, where reliable instruction following is a stated design goal. |

## Languages

| Field              | Value |
|----------------------|-------|
| `languages`           | `en, es, pt, fr, de, ja, zh, hi, ar, ru` |
| `language_quality`    | `en: very_high`; `es, pt, fr, de: high`; `ja, zh, hi, ar, ru: medium` |

Google does not publish an official per-model language list or
per-language quality rating (confirmed again during this verification
pass — the model page only lists documentation UI languages, not
generation languages). This list was curated from public usage and
general Gemini family documentation, same known gap logged in
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1).
Treat `language_quality` here as the project's editorial judgment, not
a value Google publishes directly.

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,048,576  |
| `max_output`           | 65,536     |

Confirmed directly against the official model card.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.30  |
| `output_per_million`        | $2.50  |

Confirmed directly against Google's pricing page (standard tier,
text/image/video input). Two nuances the schema doesn't capture, noted
here rather than worked around in the dataset:

- **Audio input is priced separately**, at $1.00 per 1M tokens, not
  $0.30. `SCHEMA.md`'s `cost.input_per_million` doesn't distinguish by
  modality, so the dataset entry uses the text rate — the dataset
  is not wrong, just less granular than Google's actual price list.
- Google also offers **batch** ($0.15 in / $1.25 out) and **priority**
  ($0.54 in / $4.50 out) tiers. The dataset value reflects the
  standard, non-batch, non-priority tier, since that's the default a
  developer hits first.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Standard REST/SDK access via the Gemini API, no waitlist, broad client library support. |
| `maturity`              | `stable` | Generally available, not marked preview/experimental on Google's own model listing. |

---

## Sources

- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields.
- [Gemini API models index](https://ai.google.dev/gemini-api/docs/models) — model listing, endpoint identifier.
- [Gemini 2.5 Flash model card](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash) — capabilities, context window, max output, knowledge cutoff.

All accessed 2026-08-07, official Google documentation only — no
third-party aggregators, per the dataset sourcing rule in `AGENTS.md`
and the drift this rule was written to avoid
([IMPLEMENTATION_NOTES.md, Iteration #2](../IMPLEMENTATION_NOTES.md#iteration-2)).

## Verification result

No drift found. Every `[Objective]` field in `dataset/models/gemini-2.5-flash.yaml`
matches the current official documentation exactly as of the date
above. `[Editorial]` fields were re-read against current positioning,
not re-scored — they remain the project's own judgment calls.
