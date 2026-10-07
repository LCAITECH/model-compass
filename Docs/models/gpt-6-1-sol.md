# GPT-6.1 Sol

Dataset entry: [`dataset/models/gpt-6-1-sol.yaml`](../../dataset/models/gpt-6-1-sol.yaml)
Last verified: 2026-10-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from the 2026-10-06/07 daily
provider audits — every objective field re-confirmed on OpenAI's own
pages (see Sources).

## Naming note

OpenAI's API model id is `gpt-6.1-sol` (confirmed on
`developers.openai.com/api/docs/models/gpt-6.1-sol` and the Flagship
pricing table). Dataset `id` follows the established convention that
converts version dots to hyphens: `gpt-6-1-sol` (same pattern as
`gpt-5-6-sol`). An older Sol alias, `gpt-6-sol`, still has its own
model page pointing users to GPT-6.1 Sol as the newer Sol; this
admission covers **6.1 Sol** only (the Flagship-table current Sol).

---

## Identity

| Field      | Value           |
|------------|-----------------|
| `id`       | `gpt-6-1-sol`   |
| `name`     | GPT-6.1 Sol     |
| `provider` | OpenAI          |
| `version`  | `6.1`           |
| `license`  | `proprietary`   |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page Modalities: "Image Input only". |
| `audio`                | false | Model page: "Audio Not supported". |
| `image_generation`     | false | Native output is text-only; image generation is a Responses API tool, not a native output modality (same distinction as `gpt-5-6-sol` / `gpt-6-astra`). |
| `tool_calling`         | true  | Features: "Function calling Supported"; Responses API tools listed. |
| `structured_output`    | true  | Features: "Structured outputs Supported". |
| `json_mode`            | true  | Not itemized separately — same inherited basis as other OpenAI entries when structured outputs are confirmed. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Official framing: "delivers near-Astra performance at a lower cost for complex coding, computer use, and professional work." Astra is already at the scale ceiling; near-Astra stays at that ceiling. |
| `coding`                   | `very_high` | Same "complex coding" positioning. |
| `creative_writing`         | `high`      | No creative-writing-specific claim; kept at the catalog-wide ceiling already used for Sol/Astra siblings. |
| `instruction_following`    | `very_high` | Consistent with near-flagship, tool-using positioning. |

## Languages

Not independently reconfirmed — OpenAI does not publish an explicit
per-model language list. Reused the curated set from `gpt-6-astra` /
`gpt-5-6-sol` (Iteration #1).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,050,000  |
| `max_output`           | 128,000    |

Confirmed on the model page ("1,050,000 context window", "128,000 max
output tokens").

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $2.00  |
| `output_per_million`        | $10.00 |

Standard short-context Flagship rate on
`developers.openai.com/api/docs/pricing` (row `gpt-6.1-sol`) and the
model page. Long-context / Batch / Flex / Fast tiers exist but are
not represented in `SCHEMA.md` (Iteration #5) — short-context Standard
used, consistent with every other OpenAI entry.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same Responses / Chat Completions API surface as the rest of the GPT-6 family. |
| `maturity`              | `stable` | Listed on the live Flagship pricing table with standard usage tiers; generally available. |

## Access

Standard OpenAI API at the pricing in `cost.*` above.

**Free access (`access.has_free_access`):** `false`. Model page rate
limits: Free tier "Not supported".

## Sources

- [GPT-6.1 Sol model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- [Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/) (points to GPT-6.1 Sol update)

Accessed 2026-10-07, official OpenAI documentation only.

## Verification result

New dataset entry. Objective fields confirmed against official docs.
`json_mode` and `languages`/`language_quality` inherited/curated, same
recurring OpenAI gap. `id` naming: official `gpt-6.1-sol` → catalog
`gpt-6-1-sol`.
