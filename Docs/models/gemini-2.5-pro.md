# Gemini 2.5 Pro

Dataset entry: [`dataset/models/gemini-2.5-pro.yaml`](../../dataset/models/gemini-2.5-pro.yaml)
Last verified: 2026-08-11 (Quality section re-audited; everything else last touched 2026-08-07)

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
| `reasoning`                | `very_high` | **Re-evaluated 2026-08-11**, replacing the prior purely-positional justification (this was the weakest-sourced entry in the catalog). Google's own technical report: *"Gemini 2.5 Pro is our most capable model yet, achieving SoTA performance on frontier coding and reasoning benchmarks"* ([Gemini 2.5 technical report](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf), p.1); also *"our most intelligent thinking model, exhibiting strong reasoning and code capabilities"* ([model card](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro)). Value unchanged, now properly sourced. |
| `coding`                   | `very_high` | Same technical report: *"excels at producing interactive web applications, is capable of codebase-level understanding."* Also Google Cloud's Vertex AI blog: *"now among the world's best models for coding"* ([source](https://cloud.google.com/blog/products/ai-machine-learning/gemini-2-5-pro-flash-on-vertex-ai)). Value unchanged, now properly sourced. |
| `creative_writing`         | `high`      | Technical report, p.18: *"Gemini 2.5 Pro is not just a useful coding and writing assistant, but excels at a wide range of complex tasks, ranging from those relevant for education to creative expression."* Model-specific but a secondary mention among many capabilities, not a best-in-class writing claim — consistent with `high`, not `very_high`. Value unchanged, now properly sourced. |
| `instruction_following`    | `high`      | **Changed 2026-08-11**, was `very_high`. No official Google source (ai.google.dev, blog.google, cloud.google.com, deepmind.google) makes an explicit best-in-class/flagship-tier instruction-following claim for this model specifically. The closest lead — *"we have focused on improving helpfulness / instruction following (IF)"* (technical report, p.21) — describes a generation-wide refusal-reduction effort (2.5 Pro and Flash together), not a superiority claim, and doesn't meet the bar the other three dimensions above do. |

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

**Free access (`access.has_free_access`):** `false`. Google's own
Gemini API pricing page marks this model's free-tier rows "Not
available" — "Free of charge" is listed only for the Priority tier
input, not standard usage — confirmed directly against
`ai.google.dev/gemini-api/docs/pricing`, 2026-08-09.

## Sources

- [Gemini 2.5 Pro model card](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro) — capabilities, context window, max output, knowledge cutoff (January 2025).
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields, including the 200k-token pricing tier.
- [Gemini 2.5 technical report (PDF)](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf) — quality dimension evidence, 2026-08-11 pass.
- [Vertex AI: Gemini 2.5 Pro/Flash blog post](https://cloud.google.com/blog/products/ai-machine-learning/gemini-2-5-pro-flash-on-vertex-ai) — coding-positioning quote, 2026-08-11 pass.

Objective fields accessed 2026-08-07; Quality section re-accessed
2026-08-11, official Google documentation only in both passes.

## Verification result

New dataset entry (2026-08-07), not a re-verification at that time.
All objective fields confirmed against official documentation. One
real schema gap surfaced and logged (tiered pricing) rather than
worked around silently.

**2026-08-11 re-audit** (this was flagged as the weakest-sourced
Quality section in the entire 26-model catalog — every dimension's
justification was purely positional, with no actual Google quote):
`reasoning`, `coding`, and `creative_writing` all held up under fresh
research and now carry real citations, values unchanged.
`instruction_following` did not — no first-party source supports
`very_high` specifically for this model, so it moved to `high`.
