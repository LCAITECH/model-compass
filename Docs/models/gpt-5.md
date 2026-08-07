# GPT-5

Dataset entry: [`dataset/models/gpt-5.yaml`](../../dataset/models/gpt-5.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Identity

| Field      | Value          |
|------------|----------------|
| `id`       | `gpt-5`        |
| `name`     | GPT-5          |
| `provider` | OpenAI         |
| `version`  | `5`            |
| `license`  | `proprietary`  |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Input: text and images. |
| `audio`                | false | Not listed as a supported modality. |
| `image_generation`     | false | Output modality is text-only. OpenAI's docs mention "image generation... available through the Responses API," but that's a separate tool the model can call, not a native output modality of GPT-5 itself — treated as false here, same distinction Gemini's cards draw (see `gemini-2.5-flash.md`). Noted as a judgment call, not a clean-cut fact. |
| `tool_calling`         | true  | "function_calling" listed among supported features. |
| `structured_output`    | true  | "structured_outputs" listed among supported features. |
| `json_mode`            | true  | Not independently reconfirmed this pass — "structured_outputs" was confirmed, JSON mode specifically wasn't cited separately. Inherited/curated. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Flagship model of the GPT-5 line, positioned above GPT-5 Mini. |
| `coding`                   | `very_high` | Same reasoning as above; not benchmark-derived, per `SCHEMA.md`. |
| `creative_writing`         | `high`      | Strong general-purpose model; kept below `very_high` since no model in this dataset is rated `very_high` on creative writing yet — a deliberate ceiling until a model actually distinguishes itself there. |
| `instruction_following`    | `very_high` | Consistent with flagship, tool-using positioning. |

## Languages

Not independently reconfirmed this pass — OpenAI does not publish an
explicit per-model language list. Reused the same curated set as
`gpt-5-mini` (same provider family), which is itself a curated list,
not an OpenAI-published fact (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value    |
|----------------------|----------|
| `context_window`      | 400,000  |
| `max_output`           | 128,000  |

Confirmed directly against the official model card. Same nuance as
`gpt-5-mini`: a 272,000-token *input* sub-limit exists within the
400,000 total context window.

## Cost `[Objective]`

| Field                    | Value   |
|----------------------------|---------|
| `input_per_million`         | $1.25   |
| `output_per_million`        | $10.00  |

Confirmed directly against OpenAI's pricing page (standard tier).

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same API surface as GPT-5 Mini — standard REST/SDK access. |
| `maturity`              | `stable` | Generally available. |

---

## Sources

- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — cost fields.
- [GPT-5 model card](https://developers.openai.com/api/docs/models/gpt-5) — capabilities, context window, max output, knowledge cutoff (Sep 30, 2024).

Both accessed 2026-08-07, official OpenAI documentation only.

## Verification result

No drift — this is a new dataset entry, not a re-verification of an
existing one. `json_mode` and `languages`/`language_quality` are
flagged above as not independently reconfirmed, inherited/curated
rather than freshly sourced.
