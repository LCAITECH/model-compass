# Gemini 2.5 Flash-Lite

Dataset entry: [`dataset/models/gemini-2.5-flash-lite.yaml`](../../dataset/models/gemini-2.5-flash-lite.yaml)
Last verified: 2026-08-10

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from
`Docs/CANDIDATE_RESEARCH_2026-08-10.md` (branch
`research/model-candidates`) — GA since July 2025, a real gap in the
catalog (it sat in the same tier as Gemini 2.5 Flash/Pro, both already
loaded, and was simply never added).

---

## Identity

| Field      | Value                       |
|------------|-------------------------------|
| `id`       | `gemini-2.5-flash-lite`      |
| `name`     | Gemini 2.5 Flash-Lite        |
| `provider` | Google                        |
| `version`  | `2.5`                          |
| `license`  | `proprietary`                  |

**GA date note:** the official model card's "Published" date reads
September 26, 2025, but that's the card's/preview-refresh update date,
not original GA — the models listing page states GA as July 2025.
Recorded here for anyone re-verifying; doesn't affect any schema
field.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model card: "Inputs: Text strings ... images, audio, and video files, with a 1M token context window." |
| `audio`                | true  | Same quote — audio input confirmed. Output is text-only (no audio generation). |
| `image_generation`     | false | Model card: "Outputs: Text, with a 64K token output" — no image output. |
| `tool_calling`         | true  | ai.google.dev model page: "Function calling: Supported." |
| `structured_output`    | true  | ai.google.dev model page: "Structured output: Supported." |
| `json_mode`            | true  | Not independently confirmed per-model this pass — same platform-wide Gemini API feature inherited/curated as for `gemini-2.5-flash` and every other Gemini entry in this catalog. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `medium` | Google's own model card: positioned for "high-volume classification, simple data extraction, and extremely low-latency applications where budget and speed are the primary constraints," and explicitly "less capable than Gemini 2.5 Pro Preview." A stated lightweight tier, not a reasoning-focused model — same kind of direct evidence used for `gemini-3.5-flash-lite`, not inherited from it. |
| `coding`                   | `medium` | Same reasoning. |
| `creative_writing`         | `low`    | No positive signal for stylistic depth; lightweight/high-throughput-task positioning trades this away first, same evidence basis as the rest of this row. |
| `instruction_following`    | `medium` | Kept in line with the other dimensions — no signal singling it out higher or lower. |

Per `SCHEMA.md`'s evidence-based calibration principle: this rating
happens to match `gemini-3.5-flash-lite`'s, but by independent
evidence about this specific model (Google's own "less capable than
2.5 Pro Preview" / "budget and speed are the primary constraints"
language), not because it shares the "Flash-Lite" name.

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `gemini-2.5-flash`/`gemini-2.5-pro` (same provider, same known gap,
see [IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,048,576  |
| `max_output`           | 65,536     |

Confirmed directly against the official model card and ai.google.dev
model page ("Input token limit: 1,048,576" / "Output token limit:
65,536").

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.10  |
| `output_per_million`        | $0.40  |

Confirmed directly against `ai.google.dev/gemini-api/docs/pricing`,
Standard tier, text/image/video input rate. Note: audio input is
priced separately at $0.30/M on the same page — the schema has no
field for modality-specific pricing (same known friction as
`IMPLEMENTATION_NOTES.md` Iteration #5), so the text/image/video rate
is used, consistent with how every other multimodal Gemini entry in
this catalog is recorded.

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
Gemini API pricing page lists this model's Standard/Batch/Flex/Priority
tiers as "Free of charge" for both input and output under the Free
Tier column — same continuous (rate-limited, not one-time-credit)
pattern already used for Gemini 2.5 Flash, 3.6 Flash, and 3.5
Flash-Lite in this dataset.

## Sources

- [Gemini 2.5 Flash-Lite model page](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-lite) — capabilities, context window, max output, positioning.
- [Official model card (PDF)](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Flash-Lite-Model-Card.pdf) — capabilities, GA/publish dates, capability-tier framing.
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields, Free Tier confirmation.

Accessed 2026-08-10, official Google documentation only.

## Verification result

New dataset entry. Objective fields confirmed. `license` has no
explicit per-model statement on either source — recorded as
`proprietary` by the same catalog-wide convention applied to every
other closed Google API model. `json_mode` inherited/curated, same
recurring gap as every other Gemini entry.
