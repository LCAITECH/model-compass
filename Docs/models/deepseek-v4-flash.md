# DeepSeek V4 Flash

Dataset entry: [`dataset/models/deepseek-v4-flash.yaml`](../../dataset/models/deepseek-v4-flash.yaml)
Last verified: 2026-08-11 (quality.reasoning and capabilities.structured_output only — see Quality and Capabilities sections below; everything else last touched 2026-08-07)

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Identity

| Field      | Value                |
|------------|------------------------|
| `id`       | `deepseek-v4-flash`    |
| `name`     | DeepSeek V4 Flash      |
| `provider` | DeepSeek                |
| `version`  | `V4`                    |
| `license`  | `open-weights`          |

Not independently reconfirmed this pass: the exact license
classification (`open-weights` vs `open-source`). DeepSeek's own
pricing/models pages describe access and pricing but a formal license
statement wasn't found in the pages fetched this pass. Inherited from
original curation.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | false | Not independently reconfirmed this pass — inherited from original curation. |
| `audio`                | false | Same as above — inherited. |
| `image_generation`     | false | Same as above — inherited. |
| `tool_calling`         | true  | Same as above — inherited. |
| `structured_output`    | false | **Corrected 2026-08-11**, was `true`. Re-checked DeepSeek's JSON mode guide directly: it still reads "provide an example of the desired JSON format to guide the model," with no schema-enforcement language — the same gap already found for `deepseek-v4-pro` (whose `structured_output` was downgraded to `false` for the same reason), now reconfirmed for Flash with no model-specific exception found. |
| `json_mode`            | true  | Same as above — inherited. |

This pass confirmed the model's identity and pricing directly (see
below), but the specific capability flags above could not be
reconfirmed against a page that stated them explicitly — DeepSeek's
docs split pricing, model listing, and API parameters across separate
pages, and the capability details weren't found in any of them during
this pass. Flagged here rather than silently treated as freshly
verified, per this folder's sourcing rule.

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `high`   | **Changed 2026-08-11**, was `medium`. Re-evaluated against `SCHEMA.md`'s evidence-based calibration principle — the original "flash-tier positioning" justification was family-based, exactly what that principle rules out. Official evidence found in the same V4 release announcement already cited for `deepseek-v4-pro.md` (`api-docs.deepseek.com/news/news260424/`): *"Reasoning capabilities closely approach V4-Pro."* Since V4 Pro is rated `very_high`, "closely approach" supports stepping Flash up to `high`, not leaving it at `medium` nor equalizing it to `very_high`. |
| `coding`                   | `high`   | DeepSeek's models have a strong general reputation specifically for coding tasks; editorial judgment, not benchmark-derived. |
| `creative_writing`         | `medium` | No strong signal either way; default mid-tier judgment for a flash/cost-optimized model. |
| `instruction_following`    | `medium` | No first-party statement found addressing this dimension specifically (2026-08-11 re-audit). Kept at `medium` as an explicitly unsourced editorial default — not re-derived from `reasoning`'s new evidence, since that citation ("closely approach V4-Pro") is scoped to reasoning, not instruction-following. |

## Languages

Not independently reconfirmed this pass. `languages` and
`language_quality` in the dataset entry are curated, same known gap as
the other providers (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 384,000    |

Confirmed directly against DeepSeek's Models & Pricing page ("Context
Length: 1M", "Max Output: 384K").

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.14  |
| `output_per_million`        | $0.28  |

Confirmed directly against DeepSeek's Models & Pricing page (cache-miss
input rate; a cache-hit rate of $0.0028/M also exists but isn't
captured by the schema). DeepSeek's own docs state a general price
increase is planned "in the near future" without a firm date — worth
re-checking sooner than the other three models next time this file is
revisited.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `medium` | OpenAI-compatible API exists, but ecosystem/tooling maturity is behind OpenAI/Anthropic/Google's first-party surface. |
| `maturity`              | `stable` | Generally available, not a preview release. |

---

## Access

Standard DeepSeek API at the pricing in `cost.*` above. No other
access surface checked for this entry.

**Free access (`access.has_free_access`):** `false`. DeepSeek's own
pricing docs (same page cited below) make no mention of any free tier
— confirmed directly during the 2026-08-09 free-access research pass
(`IMPLEMENTATION_NOTES.md`, Iteration #8).

## Sources

- [DeepSeek Models & Pricing](https://api-docs.deepseek.com/quick_start/pricing) — cost fields, context window, max output.
- [DeepSeek List Models API](https://api-docs.deepseek.com/api/list-models) — confirmed `deepseek-v4-flash` is a currently listed model ID.

Both accessed 2026-08-07, official DeepSeek documentation only.

## Verification result

Pricing, context window, and max output confirmed with no drift
(2026-08-07 pass). License and the remaining five capability flags
were **not** independently reconfirmed — flagged above as pending
rather than presented as freshly verified.

**2026-08-11 re-audit** (part of a catalog-wide pass re-checking every
model whose `docs/models/*.md` justification was purely positional,
per `SCHEMA.md`'s evidence-based calibration principle): `reasoning`
changed from `medium` to `high` and `structured_output` changed from
`true` to `false`, both against fresh official DeepSeek sources cited
above. `coding`, `creative_writing`, and `instruction_following` were
also checked this pass — no first-party prose was found either
confirming or contradicting their current values, so they're
unchanged and explicitly flagged as unsourced editorial judgment
rather than silently left looking equally confirmed.
