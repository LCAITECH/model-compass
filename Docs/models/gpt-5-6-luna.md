# GPT-5.6 Luna

Dataset entry: [`dataset/models/gpt-5-6-luna.yaml`](../../dataset/models/gpt-5-6-luna.yaml)
Last verified: 2026-10-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from the 2026-10-06/07 daily
audits as the still-documented GPT-5.6 efficient tier (also named as
the recommended replacement for `gpt-5-nano-2025-08-07` on OpenAI's
deprecations page). Newer efficient tier `gpt-6-luna` is admitted
separately.

## Naming note

Official API id `gpt-5.6-luna` → catalog `gpt-5-6-luna`.

---

## Identity

| Field      | Value           |
|------------|-----------------|
| `id`       | `gpt-5-6-luna`  |
| `name`     | GPT-5.6 Luna    |
| `provider` | OpenAI          |
| `version`  | `5.6`           |
| `license`  | `proprietary`   |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Image input only. |
| `audio`                | false | Audio not supported. |
| `image_generation`     | false | Text-only native output. |
| `tool_calling`         | true  | Function calling Supported. |
| `structured_output`    | true  | Structured outputs Supported. |
| `json_mode`            | true  | Inherited/curated. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `low`    | Official: "roughly corresponds to the nano model tier used in earlier GPT-5 families" — matched to `gpt-5-nano`. |
| `coding`                   | `low`    | Same. |
| `creative_writing`         | `low`    | Same. |
| `instruction_following`    | `medium` | Same nano-tier correspondence as `gpt-5-nano`. |

## Languages

Curated set reused from `gpt-5-6-sol` (Iteration #1).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,050,000  |
| `max_output`           | 128,000    |

Confirmed on the model page.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.20  |
| `output_per_million`        | $1.20  |

Confirmed on the model page and OpenAI's 2026-07-30 announcement
(Luna reduced to this rate).

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same API surface as the GPT-5.6 family. |
| `maturity`              | `stable` | Generally available; named as a deprecation replacement target. |

## Access

Standard OpenAI API. **Free access:** `false` (Free tier Not
supported on the model page).

## Sources

- [GPT-5.6 Luna model page](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
- [Advancing the price-performance frontier with GPT-5.6](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/)
- [OpenAI deprecations](https://developers.openai.com/api/docs/deprecations)

Accessed 2026-10-07, official OpenAI documentation only.

## Verification result

New dataset entry. Objective fields confirmed. Editorial ratings
aligned to OpenAI's explicit nano-tier correspondence.
