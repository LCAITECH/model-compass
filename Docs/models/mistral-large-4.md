# Mistral Large 4

Dataset entry: [`dataset/models/mistral-large-4.yaml`](../../dataset/models/mistral-large-4.yaml)
Last verified: 2026-11-03 (every field, on Mistral's own pages)

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Identity

| Field      | Value              |
|------------|---------------------|
| `id`       | `mistral-large-4`    |
| `name`     | Mistral Large 4      |
| `provider` | Mistral AI            |
| `version`  | `4`                    |
| `license`  | `open-weights`         |

Mistral's model card lists the API id `mistral-large-4` (the versioned
page is `mistral-large-4-0`) and the version tag `26.10`; the dataset's
`version` follows the public model name, as for Large 3.

`license: open-weights` — the Mistral Ecosystem Open-Weight License, "a
modified version of the MIT license" (its `LICENSE` file). The weights
are free to use, modify, fine-tune and commercialize, with one condition
(section 2): a licensee that operates a "Model as a Service" business
needs a separate commercial license from Mistral. The condition does
not apply to internal use, to end-user products with the model embedded
in specific features, or to use through Mistral's own products. The
schema offers `proprietary`, `open-weights` and `open-source` without
defining the last two; `open-weights` is Mistral's own term and the value
Large 3 already uses. The schema has no field for license conditions, so
the condition is written in the self-hosted route's caveat (Iteration
#42).

## Capabilities `[Objective]`

| Field                | Value | Source |
|-----------------------|-------|--------|
| `vision`               | true  | Hugging Face model card: "Multimodal input: accepts text and image input, with text output"; the docs card adds "a 1.6B vision encoder". |
| `audio`                | false | Same card: input is text and image only. |
| `image_generation`     | false | Same card: output is text only. |
| `tool_calling`         | true  | Same card: "native function calling"; the docs card lists Function Calling on `/v1/chat/completions` and `/v1/conversations`. |
| `structured_output`    | true  | Same card: "strict JSON schema enforcement"; the docs card lists Structured Outputs. |
| `json_mode`            | true  | Same card: "JSON output". |

## Quality `[Editorial]`

Proposed with Mistral's own words as evidence (not benchmark scores,
`SCHEMA.md`), on the calibration the catalog already uses: `very_high`
where a provider claims parity with the top closed models
(`deepseek-v4-pro`, `muse-wonder-1.0`), `high` below that. Approved by
the owner before the commit.

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `high`   | The Hugging Face card says Large 4 "unifies instruction following, reasoning, coding, and agentic workflows in a single set of weights", with three reasoning efforts (`low`, `medium`, `high`) set per request. Mistral positions it against open-weight models, and its card concedes the point: on the Artificial Analysis Intelligence Index v5 it is "the highest among western open-weight models. The leading open-weight models from China score higher on this aggregate index". No claim of parity with closed frontier models. |
| `coding`                   | `high`   | Mistral's announcement of 2026-10-29: "the best open-weight model for coding", "taking the lead on FrontierCode and Terminal-Bench" among open-weight models, and, in blind human-preference tests, "ranking behind only Claude Opus 5.5 among the models evaluated" (`very_high` here). Leadership among open weights plus second place behind one closed model in a test Mistral ran, not parity with the closed frontier. This is the closest call of the four: reading "best open-weight model for coding" like DeepSeek's "Open-source SOTA in Agentic Coding" (which `deepseek-v4-pro` holds as `very_high`) would give `very_high`. |
| `creative_writing`         | `medium` | No creative-writing claim on any page checked. Conservative middle tier, as for `deepseek-v4-pro`, `qwen3.8-max` and `muse-wonder-1.0`. |
| `instruction_following`    | `high`   | Hugging Face card: "strong adherence and support for system prompts". A direct but general claim, the same tier as `deepseek-v4-pro` and `muse-wonder-1.0`. |

## Languages

`languages` is curated (the known gap shared with the other providers,
[Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)). The Hugging Face
card says the model is "natively fluent in 160+ languages, including all
official languages of the European Union" and tags its supported
languages; the eleven codes of Large 3's list are all among those tags.

| Languages | `language_quality` | Why |
|-----------|--------------------|-----|
| English | `very_high` | The top tier every other entry in the catalog gives English; Mistral makes no language-specific claim. |
| Spanish, Portuguese, French, German, Italian, Dutch | `high` | Official EU languages, which Mistral names as native. |
| Chinese, Japanese, Korean, Arabic | `medium` | Listed among supported languages; no claim about their level. |

## Operational `[Objective]`

| Field              | Value       |
|----------------------|-------------|
| `context_window`      | 1,048,576   |
| `max_output`           | `null`      |

The docs card says context "1M"; the exact figure is `max_position_embeddings`
1048576 in `config.json` of Mistral's own Hugging Face repository (the
docs card has no token count). No maximum output is published, so
`max_output` is `null` (Iteration #26). The repository notes that
`max_completion_tokens` includes reasoning tokens.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.70  |
| `output_per_million`        | $2.10  |

Cached input is $0.07 per million; the schema has no field for it.
Blended $2.80, the `medium` cost tier.

History: Mistral's changelog of 2026-10-06 said "Launch pricing: 50% off
for 2 weeks", and the admissions pass of 2026-10-15 (Iteration #33) read
the card's price as a temporary sale ($0.68/$2.09 against a list of
$1.36/$4.18) with no end date, so the model was held back. Mistral's
announcement of 2026-10-29 states: "Starting today, Mistral Large 4 is
priced at $0.70 input / M, $0.07 cached input / M, and $2.10 output / M
tokens", and the docs card shows those figures with no sale marker. They
are stored as the price in force; there is no `effective_until`.

## Ecosystem `[Editorial]`

| Field                | Value          | Why |
|------------------------|----------------|-----|
| `integration_ease`      | `medium`       | Same call as `mistral-large-3`: open weights with support in vLLM, SGLang and transformers (the repository), and available through the Mistral API, Microsoft Foundry, NVIDIA-hosted endpoints and OpenRouter (the announcement), but first-party API tooling is less mature than OpenAI, Anthropic or Google. |
| `maturity`              | `experimental` | The docs card is dated October 6, 2026 and still labels the model "Public Preview", and the 2026-10-29 announcement calls the open weights "this improved Mistral Large 4", a later checkpoint than the preview. Against it: the models overview lists Large 4 in its public catalog and names it the alternative to the deprecated Large 3. `maturity` only shows in the comparison table; the engine does not use it. |

---

## Access

Mistral API (La Plateforme), model id `mistral-large-4`, at the price in
`cost.*`; and open weights for self-hosting
([`Docs/access-guides/mistral.md`](../access-guides/mistral.md),
`mistral#self-hosted-large-4`), under the license condition above.

**Free access (`access.has_free_access`):** `false`. No official page
names Mistral Large 4 as part of a free API tier or of the free consumer
plan (Iteration #32), and the docs card's price block marks it as not
free.

**Not routes in the dataset:** the announcement also lists Microsoft
Foundry (a cloud route comes from Microsoft's own docs, which were not
read), NVIDIA-hosted endpoints and OpenRouter (a hosting platform, the
owner's call).

**Related:** Mistral's models overview lists Mistral Large 3
(`mistral-large-2512`) under "Deprecated & retired models" with
deprecation 10/31/2026, retirement 4/30/2027 and Mistral Large 4 as the
alternative. `mistral-large-3` is not changed by this entry; see
Iteration #42.

## Sources

- [Mistral Large 4 model card](https://docs.mistral.ai/models/mistral-large-4) — identity, license label, status, context, price, free flag.
- [Mistral Large 4 on Hugging Face](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) — README (capabilities, languages, reasoning efforts, serving), `config.json` (context), `LICENSE` (terms).
- [Mistral announcement, 2026-10-29](https://mistral.ai/news/mistral-large-4-oss/) — weights release, price, positioning, availability.
- [Mistral changelog](https://docs.mistral.ai/getting-started/changelog/) — Public Preview on October 6, launch pricing.
- [Mistral models overview](https://docs.mistral.ai/getting-started/models/models_overview/) — public catalog listing, Large 3 deprecation table.

Accessed 2026-11-03, Mistral's own pages only (no aggregator).

## Verification result

Every `[Objective]` field is sourced to Mistral's pages. Two things rest
on the model's own repository rather than the docs card: the exact
context size (the card says "1M") and the capability flags (the card
lists API features, the repository states the modalities). The
`[Editorial]` fields are judgment, labeled above.
