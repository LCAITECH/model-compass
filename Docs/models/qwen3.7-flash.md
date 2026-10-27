# Qwen3.7-Flash

Dataset entry: [`dataset/models/qwen3.7-flash.yaml`](../../dataset/models/qwen3.7-flash.yaml)
Last verified: 2026-10-22

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Proposed on 2026-10-22 by the catalog bot
at the owner's request, for owner review. Iteration #33 had left it out
because it was "not in Model Studio's catalog"; Alibaba's own pages now
list it with a full model page, pricing and a release date (Iteration
#36). Every field below was read on Alibaba Cloud's own documentation
(see Sources), with the same scope choices as `qwen3.8-max`.

---

## Identity

| Field      | Value            |
|------------|-------------------|
| `id`       | `qwen3.7-flash`   |
| `name`     | Qwen3.7-Flash      |
| `provider` | Alibaba Cloud      |
| `version`  | `3.7`             |
| `license`  | `proprietary`      |

The hosted Model Studio model. Its one snapshot is
`qwen3.7-flash-2026-07-15` (model page, "Snapshot Versions"); the
pricing page says `qwen3.7-flash` is "Currently equivalent to
qwen3.7-flash-2026-07-15". The snapshot is not a separate entry.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page, Model Capabilities: Input Modality "Image Text Video". |
| `audio`                | false | Not an input or output modality of this model. |
| `image_generation`     | false | Output Modality "Text". |
| `tool_calling`         | true  | "Function Calling: Supported". |
| `structured_output`    | true  | "Structured Outputs: Supported". |
| `json_mode`            | true  | Not itemized separately, same basis as `qwen3.8-max`. |

The International scope also lists Web Search, Prefix Completion and
Context Caching as supported, and Batch Inference and Fine-tuning as
unsupported; none of these is a schema field.

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `medium` | Alibaba's page makes no reasoning claim for this model. It describes a "native vision-language series Flash" model whose improvements over 3.6-Flash are in "multimodal understanding and Agent execution", "object recognition", "real-world perception and spatial intelligence". It has a thinking mode (max chain-of-thought 262,144 tokens), but no stated reasoning strength, unlike `qwen3.8-flash`'s "powerful reasoning". Conservative middle tier. |
| `coding`                   | `high`   | A specific claim on the model page: "Multimodal coding capabilities are optimized, delivering a smoother vibe coding experience", and "Multimodal Agent scenarios such as Search Agent and CI Agent have seen significant upgrades, with more stable end-to-end task execution". |
| `creative_writing`         | `medium` | No creative-writing claim on any page checked. Conservative middle tier, as for the other Qwen entries. |
| `instruction_following`    | `medium` | No instruction-following claim. "More stable end-to-end task execution" in agent scenarios is the nearest statement, and it is about task completion, not following instructions. Conservative middle tier. |

Proposed by the catalog bot (2026-10-22) for owner review, as judgment.
Not derived from benchmarks or from a sibling's ratings: each row cites
the provider's own words or their absence.

## Languages

The curated Qwen list of `qwen3.8-max`, which Iteration #33 applied to
every Qwen entry: `en`/`zh` `very_high`, `es`/`fr`/`de`/`pt` `high`,
`ja`/`ko`/`ar`/`ru` `medium`. Alibaba publishes no per-model language
list; the model page mentions none. Curated, not sourced: the owner may
prefer a shorter list (the conservative choice made for Meta in the same
iteration).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 131,072    |

Model page, Context Limits: "Context Window 1000000", "Max Output Length
131072", "Max Input Length 991808". In thinking mode: max input 983,616,
max output 131,072, max chain-of-thought 262,144 (not in the schema).

## Cost `[Objective]`

| Field                    | Value   |
|----------------------------|---------|
| `input_per_million`         | $0.03  |
| `output_per_million`        | $0.13  |

Model page, Pricing, Singapore tab ("Scope: International"), tier
"Input<=32k". The schema stores one rate, so it holds the tier a typical
first request hits (Iteration #24). All International tiers:

| Input tokens per request | Input  | Output | Implicit cache |
|---------------------------|--------|--------|----------------|
| up to 32k                  | $0.03  | $0.13  | $0.006         |
| 32k to 256k                | $0.10  | $0.40  | $0.02          |
| 256k to 1M                 | $0.20  | $0.80  | $0.04          |

China (Beijing) scope, lower tier: $0.028/$0.11. The page shows "the
original pricing for model API calls, excluding any limited-time
promotions". Same International figures on Model Studio's pricing page.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | "The Qwen models on Model Studio support OpenAI compatible interfaces. You can migrate your existing OpenAI code to Model Studio by changing only the API key, base URL, and model name" (OpenAI compatible - Chat). Seven regions on the model page. |
| `maturity`              | `stable` | Listed under Model Studio's Model List, Text Generation, with a full spec, pricing and rate-limit page and a dated snapshot; no preview label. It is not on the "Recommended models" overview, which now lists `qwen3.8-flash` instead. |

---

## Access

One route: direct API through Alibaba Cloud Model Studio,
`api_billing_linked`. Rate limits (International): 15,000 RPM,
5,000,000 TPM.

**Free access (`access.has_free_access`):** `false`. The Singapore free
quota (1 million tokens, valid 90 days from activation or release) is a
one-time allowance, which the schema does not count, and no free
consumer plan naming the model was found.

## Lifecycle

`active`. Released 2026-07-21 (International), per Model Studio's
"Model lifecycle and updates" table; US deployment scope added
2026-10-08. No deprecation published.

## Sources

- [Qwen3.7-Flash model page](https://www.alibabacloud.com/help/en/model-studio/qwen3-7-flash) — description, capabilities, context limits, pricing by scope, rate limits, snapshot.
- [Model pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing) — International tiers, free quota, "Currently equivalent to".
- [Model lifecycle and updates](https://www.alibabacloud.com/help/en/model-studio/newly-released-models) — release date, US scope.
- [OpenAI compatible - Chat](https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope) — integration.
- [Recommended models](https://www.alibabacloud.com/help/en/model-studio/models) — what the overview lists.

All accessed 2026-10-22, Alibaba Cloud's own documentation only.

## Verification result

New entry, proposed for owner review. Objective fields confirmed on
Alibaba Cloud's documentation, International scope. `json_mode` and the
language list are curated, as for the other Qwen entries; the four
quality ratings are judgment, with the evidence above.
