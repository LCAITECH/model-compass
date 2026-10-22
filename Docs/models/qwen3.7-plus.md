# Qwen3.7-Plus

Dataset entry: [`dataset/models/qwen3.7-plus.yaml`](../../dataset/models/qwen3.7-plus.yaml)
Last verified: 2026-10-15

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted on 2026-10-15 with
`qwen3.8-flash`, from the candidate list left open since Phase 14. Every
field below was read on Alibaba Cloud's own documentation. Qwen3.7-Flash,
on the same candidate list, does not appear in Model Studio's catalog
and was not admitted.

---

## Identity

| Field      | Value            |
|------------|-------------------|
| `id`       | `qwen3.7-plus`    |
| `name`     | Qwen3.7-Plus       |
| `provider` | Alibaba Cloud      |
| `version`  | `3.7`             |
| `license`  | `proprietary`      |

The model page says `qwen3.7-plus` "is functionally equivalent to the
snapshot model qwen3.7-plus-2026-05-26"; the snapshot is not a separate
entry.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page, Model Capabilities: Input Modality "Image Text Video". |
| `audio`                | false | Not an input or output modality. |
| `image_generation`     | false | Output Modality "Text". |
| `tool_calling`         | true  | "Function Calling: Supported". |
| `structured_output`    | true  | "Structured Outputs: Supported". |
| `json_mode`            | true  | Not itemized separately, same basis as `qwen3.8-max`. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `high`   | Model page: "builds on its robust text capabilities ... preserving its full-stack agent-level intelligence". The "cost-effective" model of the 3.7 series, not its flagship. |
| `coding`                   | `high`   | "full-stack agent-level intelligence for coding, tool use, and productivity workflows", and it can "generate code based on visual references". |
| `creative_writing`         | `medium` | No creative-writing claim. |
| `instruction_following`    | `high`   | No specific claim; same conservative call as the other Qwen entries. |

Not lowered for being an older generation than `qwen3.8-flash`: the
calibration is evidence-based, and both pages make the same kind of
claims. Proposed by Claude, approved by the project owner (2026-10-15).

## Languages

The curated Qwen list of `qwen3.8-max`: `en`/`zh` `very_high`,
`es`/`fr`/`de`/`pt` `high`, `ja`/`ko`/`ar`/`ru` `medium`.

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 131,072    |

Model page, Context Limits: "Context Window 1000000", "Max Output Length
131072".

## Cost `[Objective]`

| Field                    | Value   |
|----------------------------|---------|
| `input_per_million`         | $0.40  |
| `output_per_million`        | $1.60  |

Model page, Pricing, Singapore tab ("Scope: International"), tier
"Input<=256k". Inputs from 256k to 1M tokens are billed $1.20/$4.80. The
schema stores one rate, so it holds the tier a typical request hits, as
for `claude-haiku-5-5` (Iteration #24). Cached input $0.08/M on the lower
tier.

**Limited-time discount, noted 2026-10-22 (owner request).** Model
Studio's pricing page shows `qwen3.7-plus` (International) as "List price
$0.4 (Limited-time 20% off)" for input and "List price $1.6
(Limited-time 20% off)" for output on the lower tier (and the same label
on $1.20/$4.80 above 256k), with no end date. The snapshot
`qwen3.7-plus-2026-05-26` is listed at $0.4/$1.6 with no discount label,
and the model page shows "the original pricing ... excluding any
limited-time promotions". The dataset keeps the list price: a
temporary price can only be stored with `cost.effective_until` and
`cost.reverts_to`, and those need a date the provider publishes
(`SCHEMA.md`, Cost; Iteration #13), which Alibaba does not. The same
rule kept Mistral Large 4's undated sale price out (Iteration #33). If
Alibaba publishes an end date, the discounted price can be stored with
it. Source: https://www.alibabacloud.com/help/en/model-studio/model-pricing,
read 2026-10-22.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | DashScope-native and OpenAI-compatible endpoints, six regions. |
| `maturity`              | `stable` | On Model Studio's model list with a full spec, pricing and rate-limit page; released in June 2026. |

---

## Access

One route: direct API through Alibaba Cloud Model Studio,
`api_billing_linked`. International scope rate limits: 15,000 RPM,
5,000,000 TPM.

**Free access (`access.has_free_access`):** `false`, for the same reasons
as `qwen3.8-flash`.

## Lifecycle

`active`. Released 2026-06-01 (International), per Model Studio's "Model
lifecycle and updates" table; the 2026-05-26 in the snapshot's id is not
the release date.

## Sources

- [Qwen3.7-Plus model page](https://www.alibabacloud.com/help/en/model-studio/qwen3-7-plus) — capabilities, context limits, both price tiers, rate limits.
- [Supported models overview](https://www.alibabacloud.com/help/en/model-studio/models) — current, not deprecated.
- [Model lifecycle and updates](https://www.alibabacloud.com/help/en/model-studio/newly-released-models) — release date.

All accessed 2026-10-15, Alibaba Cloud's own documentation only.

## Verification result

New entry. Objective fields confirmed on Alibaba Cloud's documentation,
International scope, lower price tier. `json_mode` and the language list
are curated.
