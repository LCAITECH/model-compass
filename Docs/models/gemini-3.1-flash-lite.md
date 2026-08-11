# Gemini 3.1 Flash-Lite

Dataset entry: [`dataset/models/gemini-3.1-flash-lite.yaml`](../../dataset/models/gemini-3.1-flash-lite.yaml)
Last verified: 2026-08-10

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from
`Docs/CANDIDATE_RESEARCH_2026-08-10.md` (branch
`research/model-candidates`) — GA successor to
`gemini-3.1-flash-lite-preview`, which Google's own docs say is
"deprecated and has been shut down."

---

## Identity

| Field      | Value                       |
|------------|-------------------------------|
| `id`       | `gemini-3.1-flash-lite`      |
| `name`     | Gemini 3.1 Flash-Lite        |
| `provider` | Google                        |
| `version`  | `3.1`                          |
| `license`  | `proprietary`                  |

**Distinct from `gemini-3.1-pro-preview` (already in this dataset):**
different model IDs, an order-of-magnitude pricing gap ($0.25/$1.50 vs.
$2–4/$12–18), and different free-tier treatment (this model has one,
Pro Preview does not) — confirmed independent models, not two labels
for the same underlying model.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page: "Input formats: Text, Image, Video, Audio, and PDF." |
| `audio`                | true  | Same source — audio input has its own price line ($0.50/M vs. $0.25/M text/image/video), confirming it as a real supported modality. Output is text-only. |
| `image_generation`     | false | Model page: "Image generation: Not supported." Output format is text only. |
| `tool_calling`         | true  | Model page: "Function calling: Supported." |
| `structured_output`    | true  | Model page: "Structured outputs: Supported." |
| `json_mode`            | true  | Not independently confirmed per-model this pass — same platform-wide Gemini API feature inherited/curated as the rest of this catalog's Gemini entries. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `medium` | Google's own model page: "a low-latency, cost-effective multimodal model optimized for high-frequency, lightweight tasks," for "high-volume agentic workflows, simple data extraction, and applications where latency and API cost are the primary constraints" — never claims superiority over Gemini 3.1 Pro Preview. |
| `coding`                   | `medium` | Same reasoning. |
| `creative_writing`         | `low`    | No positive signal for stylistic depth; same lightweight-tier framing as above. |
| `instruction_following`    | `medium` | Kept in line with the other dimensions. |

Per `SCHEMA.md`'s evidence-based calibration principle: this matches
`gemini-3.5-flash-lite`'s rating, but there is no official signal
differentiating this model's capability from that one (the ~17-40%
price gap between them comes with no accompanying capability
statement) — absence of a differentiating signal means no
differentiation, same logic already used for Claude Opus 4.7/4.8 in
this catalog.

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `gemini-3.1-pro-preview` (same provider, same generation, same
known gap, see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,048,576  |
| `max_output`           | 65,536     |

Confirmed directly against the official model page ("Input token
limit: 1,048,576" / "Output token limit: 65,536").

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.25  |
| `output_per_million`        | $1.50  |

Confirmed directly against `ai.google.dev/gemini-api/docs/pricing`,
Paid Tier, text/image/video input rate ($0.50/M for audio input, not
represented — same known schema limitation as every other multimodal
Gemini entry, see `IMPLEMENTATION_NOTES.md` Iteration #5).

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same Gemini API surface as the rest of the family. |
| `maturity`              | `stable` | Generally available, not marked preview — successor to the now-shut-down `gemini-3.1-flash-lite-preview`. |

---

## Access

Standard Gemini API — Google AI Studio and Vertex AI — at the pricing
in `cost.*` above.

**Free access (`access.has_free_access`):** `true`. Google's official
Gemini API pricing page lists both Standard and Batch tiers as "Free of
charge" for this model's input/output under the Free Tier column — same
continuous free-tier pattern already used for Gemini 2.5 Flash, 3.6
Flash, and 3.5 Flash-Lite. By contrast, the sibling `gemini-3.1-pro-preview`
entry has no such free tier — confirming the two are priced and
positioned as genuinely different tiers, not the same model twice.

## Sources

- [Gemini 3.1 Flash-Lite model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite) — capabilities, context window, max output, positioning.
- [Gemini 3.1 Flash-Lite Preview model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-preview) — deprecation/shutdown confirmation for the predecessor.
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields, Free Tier confirmation, contrast with Gemini 3.1 Pro Preview pricing.

Accessed 2026-08-10, official Google documentation only.

## Verification result

New dataset entry. Objective fields confirmed. `license` recorded as
`proprietary` by catalog-wide convention (no explicit per-model
statement found). `json_mode` inherited/curated, same recurring gap as
every other Gemini entry.
