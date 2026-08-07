# Gemini 2.5 Pro

Dataset entry: [`dataset/models/gemini-2.5-pro.yaml`](../../dataset/models/gemini-2.5-pro.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Identity

| Field      | Value              |
|------------|--------------------|
| `id`       | `gemini-2.5-pro`   |
| `name`     | Gemini 2.5 Pro     |
| `provider` | Google             |
| `version`  | `2.5`              |
| `license`  | `proprietary`      |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Input modalities: audio, images, video, text, PDF. |
| `audio`                | true  | Audio input confirmed; audio generation is not supported (output is text-only). |
| `image_generation`     | false | Explicitly listed as unsupported. |
| `tool_calling`         | true  | Confirmed. |
| `structured_output`    | true  | Confirmed. |
| `json_mode`            | true  | Confirmed — same platform-wide Gemini API feature (`response_mime_type: application/json`) verified for `gemini-2.5-flash`, not model-specific. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Google's own flagship reasoning model in the 2.5 generation, positioned above 2.5 Flash. |
| `coding`                   | `very_high` | Same reasoning; not benchmark-derived, per `SCHEMA.md`. |
| `creative_writing`         | `high`      | Same ceiling reasoning as `gpt-5.md` — no model in this dataset is yet rated `very_high` here. |
| `instruction_following`    | `very_high` | Consistent with flagship, tool-using positioning. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `gemini-2.5-flash` (same provider, same known gap — Google doesn't
publish a per-model language list, see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,048,576  |
| `max_output`           | 65,536     |

Confirmed directly against the official model card.

## Cost `[Objective]`

| Field                    | Value (≤200k tokens) | Value (>200k tokens) |
|----------------------------|-------------------------|--------------------------|
| `input_per_million`         | $1.25                   | $2.50                    |
| `output_per_million`        | $10.00                  | $15.00                   |

Confirmed directly against Google's pricing page. **This is a real
schema friction, not just a footnote**: `SCHEMA.md`'s `cost.*` fields
assume one price per model, but Gemini 2.5 Pro genuinely has two,
switching at the 200k-token prompt threshold. The dataset entry uses
the ≤200k tier since that's what a typical request hits first — logged
formally in
[IMPLEMENTATION_NOTES.md, Iteration #5](../IMPLEMENTATION_NOTES.md#iteration-5),
since this is the second or third time a single-price-per-model
assumption hasn't matched a provider's actual pricing (see also the
audio-pricing note on `gemini-2.5-flash.md` and the cache-pricing note
on `claude-sonnet-5.md`).

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same Gemini API surface as 2.5 Flash. |
| `maturity`              | `stable` | Generally available. |

---

## Access

Standard Gemini API — Google AI Studio and Vertex AI — at the pricing
in `cost.*` above. No other access surface checked for this entry.

## Sources

- [Gemini 2.5 Pro model card](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro) — capabilities, context window, max output, knowledge cutoff (January 2025).
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields, including the 200k-token pricing tier.

Both accessed 2026-08-07, official Google documentation only.

## Verification result

New dataset entry, not a re-verification. All objective fields
confirmed against official documentation. One real schema gap
surfaced and logged (tiered pricing) rather than worked around
silently.
