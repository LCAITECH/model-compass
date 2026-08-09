# GPT-5 Mini

Dataset entry: [`dataset/models/gpt-5-mini.yaml`](../../dataset/models/gpt-5-mini.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Identity

| Field      | Value          |
|------------|----------------|
| `id`       | `gpt-5-mini`   |
| `name`     | GPT-5 Mini     |
| `provider` | OpenAI         |
| `version`  | `5`            |
| `license`  | `proprietary`  |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Input modalities: text, image. |
| `audio`                | false | No audio input/output confirmed. |
| `image_generation`     | false | Confirmed unsupported. |
| `tool_calling`         | true  | "Function calling" in OpenAI's docs. |
| `structured_output`    | true  | Confirmed. |
| `json_mode`            | true  | Not independently reconfirmed this pass — the model card confirms "structured outputs," which typically implies JSON mode, but no explicit JSON-mode citation was found. Treated as inherited from original curation, not freshly verified. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `medium` | Positioned as the smaller, faster sibling of GPT-5 — reasoning capability, not the frontier tier. |
| `coding`                   | `medium` | Same reasoning as above; not benchmark-derived, per `SCHEMA.md`. |
| `creative_writing`         | `medium` | Mini-tier models generally trade stylistic depth for cost/latency. |
| `instruction_following`    | `high`   | Mini-tier OpenAI models are commonly used for high-volume, structured tasks where reliable instruction following matters more than raw capability. |

## Languages

Not independently reconfirmed this pass — OpenAI does not publish an
explicit per-model language list (same known gap as Gemini, see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).
`languages` and `language_quality` in the dataset entry are curated
from general usage, not from an official OpenAI source — treat as the
project's editorial judgment, not an OpenAI-published fact.

## Operational `[Objective]`

| Field              | Value    |
|----------------------|----------|
| `context_window`      | 400,000  |
| `max_output`           | 128,000  |

Confirmed directly against the official model card. Note: OpenAI's
card separately lists a 272,000-token *input* ceiling within that
400,000 context window (the remainder is reserved for output/reasoning
tokens) — not a discrepancy with the dataset, just more granular than
what `SCHEMA.md` captures.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.25  |
| `output_per_million`        | $2.00  |

Confirmed directly against OpenAI's pricing page (standard tier).
Batch, Flex, and "fast" pricing tiers exist at different rates; the
dataset value reflects the standard tier.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Standard REST/SDK access, no waitlist, broad client library support. |
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

- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — cost fields.
- [GPT-5 Mini model card](https://developers.openai.com/api/docs/models/gpt-5-mini) — capabilities, context window, max output, knowledge cutoff (May 31, 2024).

Both accessed 2026-08-07, official OpenAI documentation only. Note:
`platform.openai.com/docs/*` now 301-redirects to `developers.openai.com/api/docs/*`
— same publisher, new host, worth knowing if a future pass hits the old URLs.

## Verification result

No drift found in objective fields. `json_mode` and `languages` /
`language_quality` are flagged above as not independently
reconfirmed — inherited from original dataset curation, not fabricated
citations for this pass.
