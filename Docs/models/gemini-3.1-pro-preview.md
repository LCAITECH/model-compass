# Gemini 3.1 Pro Preview

Dataset entry: [`dataset/models/gemini-3.1-pro-preview.yaml`](../../dataset/models/gemini-3.1-pro-preview.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Correcting an earlier mistake — logged, not hidden

Earlier in this catalog's history, "Gemini 3.1 Pro" was checked
against `ai.google.dev/gemini-api/docs/models` (the general models
index) and wasn't found there, so it was treated as unconfirmed and
left out — documented at the time in `gemini-3.6-flash.md`. That was
half right: the model genuinely doesn't have a GA listing on that
index page. But it does exist, in **Preview** status, with its own
dedicated page and full official pricing, at
`ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview` — a URL
that wasn't tried in the first pass. The lesson isn't "trust the first
official-looking page and stop" — it's to check whether a preview/beta
model has its own page even when it's absent from a general index.
Corrected here rather than silently fixed, so the earlier note in
`gemini-3.6-flash.md` doesn't stand as the final word.

## Identity

| Field      | Value                        |
|------------|--------------------------------|
| `id`       | `gemini-3.1-pro-preview`      |
| `name`     | Gemini 3.1 Pro Preview        |
| `provider` | Google                          |
| `version`  | `3.1`                           |
| `license`  | `proprietary`                   |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Input modalities: text, image, video, audio, PDF. |
| `audio`                | true  | Audio input confirmed; audio generation is not supported. |
| `image_generation`     | false | Explicitly listed as unsupported (output is text-only). |
| `tool_calling`         | true  | Confirmed. |
| `structured_output`    | true  | Confirmed. |
| `json_mode`            | true  | Confirmed — same platform-wide Gemini API feature verified for `gemini-2.5-flash`. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | The first Gemini entry in this catalog rated `very_high` — this is Google's actual Pro-tier frontier model (Gemini 3.5 Pro is still delayed, see `gemini-3.6-flash.md`), unlike the Flash-tier models (2.5 Flash, 3.6 Flash, 3.5 Flash-Lite) deliberately kept at `high` to leave room for a real Pro release. |
| `coding`                   | `very_high` | Same reasoning. |
| `creative_writing`         | `high`      | Kept at the same ceiling used for other flagship-tier entries in this catalog (see `gpt-5.md`) — no Gemini model has independently earned `very_high` here yet. |
| `instruction_following`    | `very_high` | Same reasoning as `reasoning`. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as the rest of the Gemini family (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,048,576  |
| `max_output`           | 65,536     |

Confirmed directly against the official preview model card — same
ceiling as the rest of the Gemini 2.5/3.x family.

## Cost `[Objective]`

| Field                    | Value (≤200k tokens) | Value (>200k tokens) |
|----------------------------|-------------------------|--------------------------|
| `input_per_million`         | $2.00                   | $4.00                    |
| `output_per_million`        | $12.00                  | $18.00                   |

Confirmed directly against Google's pricing page — another instance of
the tiered-pricing pattern already logged in
[IMPLEMENTATION_NOTES.md, Iteration #5](../IMPLEMENTATION_NOTES.md#iteration-5)
(now five independent occurrences). The dataset uses the ≤200k tier,
same convention as `gemini-2.5-pro`. Batch, Flex, and Priority tiers
also exist at different rates, not captured here.

## Access — where this model can actually be called from

Directly relevant to the discussion that led to re-checking this
model: Gemini 3.1 Pro Preview **is** reachable through the standard,
token-priced Gemini API — Google AI Studio and Vertex AI, both listed
as official API providers on its model card, both using the pricing
above. It is *also* exposed inside Google Antigravity (see
`gemini-3.6-flash.md` and `IMPLEMENTATION_NOTES.md` Iteration #6 for
why Antigravity itself wasn't treated as a valid source) — but
Antigravity is one more surface this model happens to be available
through, not the only way to reach it. The `cost.*` values above
reflect the standard API, not Antigravity's subscription tiers.

## Ecosystem `[Editorial]`

| Field                | Value          | Why |
|------------------------|----------------|-----|
| `integration_ease`      | `high`         | Standard Gemini API surface (AI Studio + Vertex AI), same as every other Gemini entry. |
| `maturity`              | `experimental` | Explicitly labeled "Preview" by Google, with no GA model ID as of this verification date — the first entry in this catalog to use this value instead of `stable`. |

---

## Sources

- [Gemini 3.1 Pro Preview model card](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview) — capabilities, context window, max output, preview status.
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields, including the 200k-token pricing tier.

Both accessed 2026-08-07, official Google documentation only.

## Verification result

New dataset entry, added on a second pass after an initial
under-search (see the correction note above). All objective fields
confirmed against official documentation this time.
