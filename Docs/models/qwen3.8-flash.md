# Qwen3.8-Flash

Dataset entry: [`dataset/models/qwen3.8-flash.yaml`](../../dataset/models/qwen3.8-flash.yaml)
Last verified: 2026-10-15

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Second Alibaba Cloud entry, admitted on
2026-10-15 from the candidate list left open since Phase 14. Every field
below was read on Alibaba Cloud's own documentation (see Sources), with
the same scope choices as `qwen3.8-max`.

---

## Identity

| Field      | Value            |
|------------|-------------------|
| `id`       | `qwen3.8-flash`   |
| `name`     | Qwen3.8-Flash      |
| `provider` | Alibaba Cloud      |
| `version`  | `3.8`             |
| `license`  | `proprietary`      |

The hosted Model Studio model. Not to be confused with
`qwen3.8-omni-flash`, a separate omni-modal model (audio in and out) that
this text/code catalog does not cover.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page, Model Capabilities: Input Modality "Image Text Video". |
| `audio`                | false | Not an input or output modality of this model. |
| `image_generation`     | false | Output Modality "Text". |
| `tool_calling`         | true  | "Function Calling: Supported". |
| `structured_output`    | true  | "Structured Outputs: Supported". |
| `json_mode`            | true  | Not itemized separately, same basis as `qwen3.8-max`. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `high`   | Model page: "combining powerful reasoning and generation with remarkable speed". Alibaba's speed-and-cost tier below `qwen3.8-max` (`very_high`), whose page carries the flagship claims. |
| `coding`                   | `high`   | "It shines in coding assistance, agentic workflows, and visual understanding — whether it's fixing code autonomously, operating desktop applications". |
| `creative_writing`         | `medium` | No creative-writing claim; same call as `qwen3.8-max`. |
| `instruction_following`    | `high`   | No specific claim; same conservative call as `qwen3.8-max`. |

Proposed by Claude, approved by the project owner (2026-10-15).

## Languages

The curated Qwen list of `qwen3.8-max` (Alibaba publishes no per-model
list): `en`/`zh` `very_high`, `es`/`fr`/`de`/`pt` `high`,
`ja`/`ko`/`ar`/`ru` `medium`.

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 131,072    |

Model page, Context Limits: "Context Window 1000000", "Max Output Length
131072" (same in thinking mode; max chain-of-thought 262,144, not in the
schema).

## Cost `[Objective]`

| Field                    | Value   |
|----------------------------|---------|
| `input_per_million`         | $0.15  |
| `output_per_million`        | $0.47  |

Model page, Pricing, Singapore tab ("Scope: International"), the scope
reachable from a standard account, as for `qwen3.8-max`. China (Beijing)
scope: $0.113/$0.382. Cached input $0.016/M. The page shows "original
pricing ... excluding any limited-time promotions".

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | "Fully compatible with both OpenAI and Anthropic API protocols", six regions. |
| `maturity`              | `stable` | On Model Studio's model list with a full spec, pricing and rate-limit page; no preview label. |

---

## Access

One route: direct API through Alibaba Cloud Model Studio,
`api_billing_linked`.

**Free access (`access.has_free_access`):** `false`. Model Studio's
new-user free quota applies to the China (Beijing) scope only, and no
free consumer plan naming the model was found.

## Lifecycle

`active`. Released 2026-08-26 (International), per Model Studio's
"Model lifecycle and updates" table.

## Sources

- [Qwen3.8-Flash model page](https://www.alibabacloud.com/help/en/model-studio/qwen3-8-flash) — capabilities, context limits, pricing by scope.
- [Supported models overview](https://www.alibabacloud.com/help/en/model-studio/models) — current, not deprecated.
- [Model lifecycle and updates](https://www.alibabacloud.com/help/en/model-studio/newly-released-models) — release date.

All accessed 2026-10-15, Alibaba Cloud's own documentation only.

## Verification result

New entry. Objective fields confirmed on Alibaba Cloud's documentation,
International scope. `json_mode` and the language list are curated, as
for `qwen3.8-max`.
