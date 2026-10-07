# GPT-6 Luna

Dataset entry: [`dataset/models/gpt-6-luna.yaml`](../../dataset/models/gpt-6-luna.yaml)
Last verified: 2026-10-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from the 2026-10-06/07 daily
provider audits — every objective field re-confirmed on OpenAI's own
pages (see Sources).

## Naming note

Official API id is `gpt-6-luna` (no version dot to convert). "Luna" is
OpenAI's durable efficient/high-volume capability tier (Sol / Terra /
Luna framing from the GPT-5.6 generation onward).

---

## Identity

| Field      | Value         |
|------------|---------------|
| `id`       | `gpt-6-luna`  |
| `name`     | GPT-6 Luna    |
| `provider` | OpenAI        |
| `version`  | `6`           |
| `license`  | `proprietary` |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Modalities: "Image Input only". |
| `audio`                | false | "Audio Not supported". |
| `image_generation`     | false | Text-only native output; image generation is a tool, not a native modality. |
| `tool_calling`         | true  | Function calling Supported; Responses API tools listed. |
| `structured_output`    | true  | Structured outputs Supported. |
| `json_mode`            | true  | Inherited/curated, same basis as other OpenAI entries. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `medium` | Official framing: "our most efficient model for focused, high-volume tasks" — not flagship/Sol positioning. Rated above `gpt-5-nano` / `gpt-5-6-luna` (`low`) because GPT-6 Luna is the current efficient tier of a generation OpenAI describes as leading the cost–intelligence curve, but not raised to Sol/`high` without a dimension-specific claim. |
| `coding`                   | `medium` | Same efficient-tier framing. |
| `creative_writing`         | `low`    | No positive stylistic claim; kept at the lightweight default. |
| `instruction_following`    | `medium` | Tool-using efficient tier; kept aligned with reasoning/coding. |

## Languages

Curated set reused from `gpt-6-astra` / `gpt-5-6-sol` (Iteration #1).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,050,000  |
| `max_output`           | 128,000    |

Confirmed on the model page.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.10  |
| `output_per_million`        | $0.50  |

Standard short-context Flagship rate on the pricing page and model
page. Matches the 50% reduction vs GPT-5.6 Luna promotional rates
described in OpenAI's GPT-6 Sol and Luna announcement.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same API surface as the rest of the GPT-6 family. |
| `maturity`              | `stable` | On the live Flagship pricing table with standard usage tiers. |

## Access

Standard OpenAI API at the pricing in `cost.*` above.

**Free access (`access.has_free_access`):** `false`. Model page: Free
tier "Not supported" for API. (ChatGPT Free/Go desktop access to Luna
is a different surface, not continuous free API access per
`SCHEMA.md`.)

## Sources

- [GPT-6 Luna model page](https://developers.openai.com/api/docs/models/gpt-6-luna)
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- [Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/)

Accessed 2026-10-07, official OpenAI documentation only.

## Verification result

New dataset entry. Objective fields confirmed. Editorial ratings
evidence-based against OpenAI's efficient-tier framing, not
family-inherited from Sol/Astra.
