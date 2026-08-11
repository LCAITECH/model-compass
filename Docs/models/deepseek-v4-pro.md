# DeepSeek V4 Pro

Dataset entry: [`dataset/models/deepseek-v4-pro.yaml`](../../dataset/models/deepseek-v4-pro.yaml)
Last verified: 2026-08-10

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Identity

| Field      | Value              |
|------------|---------------------|
| `id`       | `deepseek-v4-pro`   |
| `name`     | DeepSeek V4 Pro      |
| `provider` | DeepSeek              |
| `version`  | `V4`                  |
| `license`  | `open-weights`        |

`open-weights` confirmed directly against the official model repository
(`huggingface.co/deepseek-ai/DeepSeek-V4-Pro`, DeepSeek's own org, MIT
license). This is a stronger confirmation than DeepSeek V4 Flash's
entry currently has (see that file — license there is flagged
"not independently reconfirmed").

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | false | Confirmed with unusually strong evidence — see [IMPLEMENTATION_NOTES.md, Iteration #11](../IMPLEMENTATION_NOTES.md#iteration-11). Four independent official sources (Chat Completions API reference, full docs navigation index, official Hugging Face model card, Responses API guide) all confirm no image/vision support, contradicting several third-party sites that claimed otherwise. The Responses API guide is explicit: *"Image and file inputs are not supported (`input_image` parts do not cause an error, but are replaced with a placeholder text)."* |
| `audio`                | false | No mention in any official source checked. |
| `image_generation`     | false | No mention in any official source checked. |
| `tool_calling`         | true  | API reference: `tools` parameter, function calling supported. |
| `structured_output`    | false | DeepSeek's own JSON mode guide (`guides/json_mode`) describes example-guided JSON output, not enforced JSON Schema — doesn't meet the bar for `structured_output`. Note: `deepseek-v4-flash`'s entry currently has this field as `true`, unreconfirmed — worth revisiting there separately. |
| `json_mode`            | true  | Confirmed: `response_format: {"type": "json_object"}`. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Re-evaluated 2026-08-10 against `SCHEMA.md`'s evidence-based calibration principle — the original justification here was family/parameter-count-based ("flagship of the V4 line"), exactly what that principle now rules out, so it was replaced rather than reused. Official evidence found on a re-read of the release announcement (previously listed as a source but explicitly *not* used as a basis): under the heading **"World-Class Reasoning,"** DeepSeek states *"Beats all current open models in Math/STEM/Coding, rivaling top closed-source models."* This is first-party positioning language, not a benchmark score — the actual benchmark figures on that page are only in chart images, never quoted or used here, consistent with `SCHEMA.md`'s ban on benchmark-derived ratings. "Rivaling" (not "beats") the closed-source frontier is read as supporting a shared `very_high` ceiling alongside the dataset's other frontier models, not a claim of outright superiority. |
| `coding`                   | `very_high` | Same source, same re-evaluation: *"Beats all current open models in Math/STEM/Coding, rivaling top closed-source models"* plus a separate claim, *"Open-source SOTA in Agentic Coding benchmarks."* Same treatment as `reasoning` — the prose positioning is used, the chart-only benchmark figures are not. |
| `creative_writing`         | `medium`    | No signal in either direction; consistent with V4 Flash's own rating — this is a reasoning/coding-focused family, not a rating downgrade specific to Pro. |
| `instruction_following`    | `high`      | Stepped up one level from V4 Flash's `medium`, same flagship-tier calibration logic as `reasoning` and `coding` — a general capability judgment, not sourced from any specific claim. |

## Languages

Not independently sourced — DeepSeek doesn't publish an official
per-model language list or language-quality breakdown, same known gap
as every other provider in this dataset (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).
Curated consistent with `deepseek-v4-flash`'s existing language list,
with per-language quality stepped up one tier for the top five
non-English languages to reflect the Pro tier's larger capacity —
an editorial judgment, not a sourced fact.

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 384,000    |

Confirmed directly against DeepSeek's official Models & Pricing page
("Context Length: 1M", "MAXIMUM: 384K") — same page, same date, as the
cost fields below.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.435 |
| `output_per_million`        | $0.87  |

Confirmed directly against DeepSeek's official Models & Pricing page
(cache-miss rate — the price a typical first request hits). A
cache-hit input rate of $0.003625/M also exists but isn't captured by
`SCHEMA.md`, same known granularity gap as
[IMPLEMENTATION_NOTES.md, Iteration #5](../IMPLEMENTATION_NOTES.md#iteration-5).

DeepSeek's own pricing page states a general price increase is planned
"in the near future" without a firm date, same open warning already
noted on `deepseek-v4-flash`'s entry — worth re-checking sooner than
most models next time this file is revisited.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `medium` | Same OpenAI-compatible API surface as V4 Flash, same ecosystem/tooling maturity gap relative to OpenAI/Anthropic/Google's first-party surface — no reason to rate differently from Flash on this dimension. |
| `maturity`              | `stable` | Initially announced as "DeepSeek V4 Preview Release" (2026-04-24), but current official docs (pricing page, model listing) show no preview/beta flag four months later — treated as generally available, consistent with V4 Flash's rating. |

---

## Access

Standard DeepSeek API at the pricing in `cost.*` above. No other
access surface checked for this entry.

**Free access (`access.has_free_access`):** `false`. DeepSeek's
official pricing page makes no mention of any free tier or trial
credit — confirmed directly, 2026-08-10.

## Sources

- [DeepSeek Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing) — model ID, cost fields, context window, max output, price-increase warning.
- [DeepSeek Chat Completions API reference](https://api-docs.deepseek.com/api/create-chat-completion/) — `content` schema (text-only), `tools`, `response_format` parameters.
- [DeepSeek JSON Output guide](https://api-docs.deepseek.com/guides/json_mode) — confirms example-guided JSON mode, not strict schema.
- [DeepSeek Responses API guide](https://api-docs.deepseek.com/guides/responses_api) — explicit confirmation that image/file inputs are unsupported.
- [DeepSeek V4 Preview Release announcement](https://api-docs.deepseek.com/news/news260424/) — release date, parameter counts, and (as of the 2026-08-10 re-evaluation) the "World-Class Reasoning" / coding positioning quotes now used as the basis for `quality.reasoning` and `quality.coding` above. Chart-only benchmark figures on the same page were not used, per `SCHEMA.md`'s ban on benchmark-derived ratings.
- [DeepSeek-V4-Pro model card, Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) — license (MIT), no vision/multimodal mention.
- Full navigation index of `api-docs.deepseek.com` — confirmed no vision/image/audio guide exists anywhere in the docs.

All accessed 2026-08-10, official DeepSeek documentation and DeepSeek's
own Hugging Face model repository only — no third-party aggregators,
per `AGENTS.md`.

## Verification result

New entry — no prior dataset version to compare against. Every
`[Objective]` field independently confirmed against official sources
listed above, including `vision` and `structured_output`, both
resolved with direct evidence rather than left as pending (see
Iteration #11 for the `vision` sourcing story specifically).

**2026-08-10 addendum:** `quality.reasoning` and `quality.coding`
re-evaluated against `SCHEMA.md`'s evidence-based calibration
principle, prompted by a product audit of why this model kept
outranking pricier flagships once `cost` entered the ranking. The
original justification was family/parameter-count-based, which the
principle now rules out — replaced with the official positioning
language quoted above. **Both values stay `very_high`, unchanged** —
the re-evaluation found the rating adequately supported by evidence
that was already cited as a source but not previously used as the
basis, not a case of an inflated rating. Same pass flagged
`gemini-2.5-pro.md`'s `quality.*` justification as comparatively weak
under this same principle — noted for a future session, not addressed
here.
