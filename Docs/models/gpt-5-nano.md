# GPT-5 Nano

Dataset entry: [`dataset/models/gpt-5-nano.yaml`](../../dataset/models/gpt-5-nano.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Identity

| Field      | Value          |
|------------|----------------|
| `id`       | `gpt-5-nano`   |
| `name`     | GPT-5 Nano     |
| `provider` | OpenAI         |
| `version`  | `5`            |
| `license`  | `proprietary`  |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Input: text and images. |
| `audio`                | false | Not listed as supported. |
| `image_generation`     | false | Output is text-only. |
| `tool_calling`         | true  | Function calling confirmed, plus Responses API tools (web search, file search, code interpreter, MCP). |
| `structured_output`    | true  | "structured_outputs" listed among supported features. |
| `json_mode`            | true  | Not independently reconfirmed this pass — same gap as `gpt-5`/`gpt-5-mini`. Inherited. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `low`    | Smallest, fastest, cheapest tier of the GPT-5 line — positioned below GPT-5 Mini (`medium`), not above it. |
| `coding`                   | `low`    | Same reasoning. |
| `creative_writing`         | `low`    | Same reasoning. |
| `instruction_following`    | `medium` | Nano-tier OpenAI models are commonly deployed for narrow, high-volume, structured tasks (classification, extraction, routing) where reliable instruction following matters more than depth — kept a notch above the other three dimensions for that reason, not because of a specific benchmark. |

## Languages

Not independently reconfirmed this pass — reused the same curated set
as `gpt-5`/`gpt-5-mini` (same provider, same known gap, see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value    |
|----------------------|----------|
| `context_window`      | 400,000  |
| `max_output`           | 128,000  |

Confirmed directly against the official model card — identical ceiling
to GPT-5 and GPT-5 Mini (the context/output limits appear to be
shared across the GPT-5 family, only pricing and quality differ by
tier).

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.05  |
| `output_per_million`        | $0.40  |

Confirmed directly against OpenAI's pricing page — the cheapest entry
in the dataset by a wide margin (blended $0.45, next cheapest is
DeepSeek V4 Flash at $0.42, essentially tied).

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same API surface as the rest of the GPT-5 line. |
| `maturity`              | `stable` | Generally available. |

---

## Access

Standard OpenAI API at the pricing in `cost.*` above. No other access
surface checked for this entry.

**Free access (`access.has_free_access`):** `false`. OpenAI's official
API pricing page lists no free tier for any language model — the only
free entries there are the moderation endpoint and storage allowances,
unrelated to this model.

## Sources

- [GPT-5 Nano model card](https://developers.openai.com/api/docs/models/gpt-5-nano) — capabilities, context window, max output, knowledge cutoff (May 31, 2024).
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — cost fields.

Both accessed 2026-08-07, official OpenAI documentation only.

## Verification result

New dataset entry. Objective fields confirmed. `json_mode` and
`languages`/`language_quality` flagged as not independently
reconfirmed, same gap as the rest of the GPT-5 family.
