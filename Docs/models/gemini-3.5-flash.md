# Gemini 3.5 Flash

Dataset entry: [`dataset/models/gemini-3.5-flash.yaml`](../../dataset/models/gemini-3.5-flash.yaml)
Last verified: 2026-08-10

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from
`Docs/CANDIDATE_RESEARCH_2026-08-10.md` (branch
`research/model-candidates`) — a distinct GA model from Gemini 3.5
Flash-Lite (already in this dataset), with its own model page and
pricing, not a variant.

---

## Identity

| Field      | Value               |
|------------|----------------------|
| `id`       | `gemini-3.5-flash`   |
| `name`     | Gemini 3.5 Flash     |
| `provider` | Google                |
| `version`  | `3.5`                  |
| `license`  | `proprietary`          |

Published May 2026 per the DeepMind model card ("the next iteration in
the Gemini 3 series").

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page: input modalities "Text, Image, Video, Audio, and PDF." |
| `audio`                | true  | Same source — audio input confirmed. Output: model page explicitly lists "Audio generation: Not supported," so audio here means input/understanding only — same convention as every other Gemini entry in this catalog. |
| `image_generation`     | false | Model page: "Image generation: Not supported." |
| `tool_calling`         | true  | Model page: "Function calling: Supported." |
| `structured_output`    | true  | Model page: "Structured outputs: Supported." |
| `json_mode`            | true  | Not independently confirmed per-model this pass — same platform-wide Gemini API feature inherited/curated as the rest of this catalog. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `high`   | Google's own positioning is stronger than 3.6 Flash's: "Most intelligent model for sustained frontier performance on agentic and coding tasks," and "combining frontier intelligence with superior search and grounding" — but `very_high` stays reserved for an actually-released, sourceable Pro-class model (the same rule `gemini-3.6-flash.md` established), and no Gemini 3.x Pro is in this dataset yet. `high` is this model's ceiling on that basis, not a downgrade. |
| `coding`                   | `high`   | Same reasoning — Google's copy explicitly calls out "coding tasks." |
| `creative_writing`         | `medium` | No stylistic-depth signal found either way; conservative default, same as `gemini-3.6-flash`. |
| `instruction_following`    | `high`   | Consistent with the agentic/tool-use-heavy positioning Google describes. |

Per `SCHEMA.md`'s evidence-based calibration principle: this rating
matches `gemini-3.6-flash`'s, but the reasoning is inverted from a
naive "same family, same tier" — Google's own copy for *this* model is
actually stronger than 3.6 Flash's, and the ceiling that keeps it at
`high` instead of `very_high` is a documented, catalog-wide rule (no
released Pro-class Gemini 3.x model exists to sourceably claim
`very_high` against), not a family assumption.

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `gemini-3.6-flash`/`gemini-2.5-flash` (same provider, same known
gap, see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,048,576  |
| `max_output`           | 65,536     |

Confirmed directly against the model page ("Input token limit:
1,048,576" / "Output token limit: 65,536"), matching the DeepMind
model card's "64K token output."

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $1.50  |
| `output_per_million`        | $9.00  |

Confirmed directly against `ai.google.dev/gemini-api/docs/pricing`,
Standard tier ("Output price (including thinking tokens)"). The page
also lists Batch/Flex ($0.75/$4.50) and Priority ($2.70/$16.20) tiers —
Standard used here, consistent with every other entry in this catalog.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same Gemini API surface as the rest of the family. |
| `maturity`              | `stable` | Generally available, not marked preview. |

---

## Access

Standard Gemini API — Google AI Studio and Vertex AI — at the pricing
in `cost.*` above.

**Free access (`access.has_free_access`):** `true`. Google's official
Gemini API pricing page lists this model's Standard tier input/output
as "Free of charge" under the Free Tier column — same continuous
free-tier pattern already used for Gemini 2.5 Flash, 3.6 Flash, and 3.5
Flash-Lite.

**Not to be confused with:** "Gemini 3.5 Live Translate," a separate
product/model listed adjacent on the pricing page (speech-to-speech
translation across ~90 languages) — different model, not this entry.

## Sources

- [Gemini 3.5 Flash model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash) — capabilities, context window, max output, positioning.
- [DeepMind model card](https://deepmind.google/models/model-cards/gemini-3-5-flash/) — license/terms, publish date.
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields, Free Tier confirmation.
- [Gemini API models index](https://ai.google.dev/gemini-api/docs/models) — comparative tiering language against 3.6 Flash and 3.5 Flash-Lite.

Accessed 2026-08-10, official Google documentation only.

## Verification result

New dataset entry. Objective fields confirmed. `license` recorded as
`proprietary` by catalog-wide convention, cross-checked against the
DeepMind model card's Gemini API Additional Terms of Service framing.
`json_mode` inherited/curated, same recurring gap as every other
Gemini entry.
