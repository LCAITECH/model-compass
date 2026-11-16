# Qwen4-Max

Dataset entry: [`dataset/models/qwen4-max.yaml`](../../dataset/models/qwen4-max.yaml)
Last verified: 2026-11-16

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Fifth Alibaba Cloud entry, admitted
2026-11-16 as the generally available successor to the Token-Plan-only
`qwen4-max-preview` (that preview id is not this entry and is not in
the dataset). Every field below was read on Alibaba Cloud's own
documentation (see Sources), with the same International (Singapore)
scope choice as `qwen3.8-max`.

---

## Identity

| Field      | Value            |
|------------|-------------------|
| `id`       | `qwen4-max`       |
| `name`     | Qwen4-Max          |
| `provider` | Alibaba Cloud      |
| `version`  | `4`               |
| `license`  | `proprietary`      |

The hosted Model Studio model, invocation ID `qwen4-max`. Distinct
from `qwen4-max-preview`, which remains Token Plan only and is
scheduled to retire after 24:00 on 2026-11-25 (UTC+8).

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page, Model capabilities, Singapore: Input modalities "Text, image, video". |
| `audio`                | false | Not listed as an input or output modality. |
| `image_generation`     | false | Output modality "Text". |
| `tool_calling`         | true  | "Function Calling: Supported". |
| `structured_output`    | true  | "Structured output (JSON Object, JSON Schema) Supported". |
| `json_mode`            | true  | Covered by JSON Object / JSON Schema; same basis as the other Qwen entries. |

## Quality `[Editorial]`

| Field                    | Value         | Why |
|---------------------------|---------------|-----|
| `reasoning`                | `very_high`  | Alibaba's own model page and launch post call it the next-generation flagship, "the most capable model in the Qwen family to date", with deep reasoning and work aimed at complex agentic tasks and scientific discovery. That is the family's ceiling claim, not a mid-tier speed/cost pitch. |
| `coding`                   | `very_high`  | The model page names coding, frontend design and complex agentic tasks as the design targets. The rating follows that official positioning, not a leaderboard score. |
| `creative_writing`         | `medium`     | The announcement title mentions creativity, but the model page and the body of the post emphasize coding, office work, agents and research, not creative writing. |
| `instruction_following`    | `high`       | No claim specific to this dimension; one step below the ceiling. |

Proposed by the catalog bot (2026-11-16), pending the owner's review.

## Languages

The curated Qwen list of `qwen3.8-max` (Alibaba publishes no per-model
list): `en`/`zh` `very_high`, `es`/`fr`/`de`/`pt` `high`,
`ja`/`ko`/`ar`/`ru` `medium`.

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 131,072    |

Model page, Context limits: "Context length 1,000,000", "Maximum output
length (non-thinking) 131,072". Thinking is enabled by default.
"Maximum combined tokens for thinking and the final answer 262,144"
has no separate schema field and is recorded only here (same
convention as `qwen3.8-flash` and Iteration #24/#26).

## Cost `[Objective]`

| Field                    | Value   |
|----------------------------|---------|
| `input_per_million`         | $1.50  |
| `output_per_million`        | $4.50  |

Model page and the Model Studio pricing page, Singapore tab
("Deployment scope: International"), 0 < tokens ≤ 1M, "Non-Thinking
and Thinking modes", the scope reachable from a standard account, as
for `qwen3.8-max`. Other published scopes (China/Beijing, Hong Kong,
Frankfurt, Virginia, Tokyo) are $1.413 / $4.24.

Cached input has no schema field. The pricing page's Qwen4-Max cache
table for Singapore is: cache write 5-minute $1.875, 1-hour $3,
explicit/implicit cache read $0.075, all per million tokens. Beijing
cache read is $0.071.

The Singapore tab also lists a 1 million token free quota, valid for
90 days from Model Studio activation, model release, or application
approval.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Official compatibility with OpenAI Chat Completions, OpenAI Responses, Anthropic Messages and DashScope, in the same Model Studio regions as the rest of the Qwen family. |
| `maturity`              | `stable` | Generally available on 2026-11-16: on the public Model Studio release list and the pricing page as `qwen4-max`, with no preview label. The preview is a different id. |

---

## Access

One route: direct API through Alibaba Cloud Model Studio,
`api_billing_linked`. Pay-as-you-go is available; Token Plan also
lists the model as of 2026-11-16.

**Free access (`access.has_free_access`):** `false`. The 1 million
token Singapore free quota is a 90-day new-user allowance, not a
continuous free tier (`CATALOG_BOT.md` §3, Iteration #32).

## Lifecycle

`active`. Released 2026-11-16 (International), per Model Studio's
"Model releases and updates" table. No shutdown date is published.
`qwen4-max-preview` remains a separate, Token-Plan-only id with a
preview end of 24:00 on 2026-11-25 (UTC+8); it is not this entry.

## Sources

- [Qwen4-Max model page](https://www.alibabacloud.com/help/en/model-studio/qwen4-max) — capabilities, context limits, International pricing, rate limits, API protocols. Last updated 2026-11-16.
- [Model inference pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing) — Singapore $1.5 / $4.5 and the cache table; other-region prices. Last updated 2026-11-16.
- [Model releases and updates](https://www.alibabacloud.com/help/en/model-studio/newly-released-models) — release date 2026-11-16, International scope.
- [Alibaba unveils Qwen4-Max](https://www.alibabacloud.com/blog/alibaba-unveils-qwen4-max-new-ai-teammate-for-work-creativity-and-discovery_603783) — official positioning used only for editorial ratings (2026-11-16).
- [Qwen4-Max-Preview](https://www.alibabacloud.com/help/en/model-studio/qwen4-max-preview) — confirms the production id is separate, and the preview retires after 2026-11-25 24:00 UTC+8.
- [Token Plan product updates](https://www.alibabacloud.com/help/en/model-studio/token-plan-product-updates) — "2026-11-16 / Qwen4-Max available" on Personal and Team editions.

All accessed 2026-11-16, Alibaba Cloud's own documentation only.

## Verification result

New entry. Objective fields confirmed on Alibaba Cloud's documentation,
International scope. `json_mode` and the language list are curated, as
for the other Qwen entries. Editorial ratings are the bot's and await
the owner's review.
