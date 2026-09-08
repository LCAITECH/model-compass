# Qwen3.8-Max

Dataset entry: [`dataset/models/qwen3.8-max.yaml`](../../dataset/models/qwen3.8-max.yaml)
Last verified: 2026-09-08

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. First Alibaba Cloud entry in this
catalog — admitted from a tip in a third-party AI-generated audit
(Grok) mentioning Qwen3.8-Max's OpenRouter listing. The tip itself was
not used as a source for any field below; every fact was independently
re-confirmed by reading Alibaba Cloud's own documentation directly
(see Sources), same discipline already applied to every prior Grok tip
this project has received.

---

## Two different things share the "Qwen3.8-Max" name — only one is this entry

Alibaba released an open-weights checkpoint,
[`Qwen/Qwen3.8-2.4T-A95B`](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)
(confirmed on Hugging Face, license field: `qwen3.8-max`, a custom
license, not Apache/MIT), separately from the hosted API product
described in this entry. Per `SCHEMA.md`'s own rule for distinguishing
entries ("does the provider's own API documentation assign it a
distinct model ID?"), these are two different model IDs with two
different capability sets:

- **This entry (`qwen3.8-max`, Alibaba Cloud Model Studio API)**:
  vision input, 1,000,000-token context window, the one actually
  priced and admitted here.
- **The open-weights checkpoint (`Qwen/Qwen3.8-2.4T-A95B`, Hugging
  Face)**: text-only (no vision), a smaller context window than the
  hosted API version. Not admitted as its own dataset entry this
  pass — would need its own `id`, its own (lower) capability set, and
  its own self-hosted access route, not a relaxed version of this
  one. Flagged for the project owner to decide whether it's worth a
  second entry later; not assumed here.

## Identity

| Field      | Value            |
|------------|-------------------|
| `id`       | `qwen3.8-max`     |
| `name`     | Qwen3.8-Max        |
| `provider` | Alibaba Cloud      |
| `version`  | `3.8`             |
| `license`  | `proprietary`      |

`proprietary` here specifically describes *this* API-hosted entry —
see the note above about the separate open-weights checkpoint, which
would be `open-weights` under its own, different dataset entry.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page, Model Capabilities: Input Modality "Image Text Video." |
| `audio`                | false | Not listed as an input/output modality for this model; Alibaba Cloud ships audio understanding/generation as separate models (`qwen-audio-3.0-*`), not part of `qwen3.8-max` itself. |
| `image_generation`     | false | Output Modality is "Text" only. Image generation is a separate model (`qwen-image-3.0-pro`) in Alibaba Cloud Model Studio's catalog. |
| `tool_calling`         | true  | Model page, Model Capabilities: "Function Calling: Supported." |
| `structured_output`    | true  | Model page, Model Capabilities: "Structured Outputs: Supported." |
| `json_mode`            | true  | Not itemized separately by Alibaba Cloud — same basis already used elsewhere in this dataset when structured output is confirmed but JSON mode isn't itemized as its own distinct feature. Inherited/curated. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Alibaba's own product description: delivers "production-grade results end-to-end in a single conversation" across "hundreds of professional tasks across law, finance, design, and more," with native visual understanding "through the entire planning, execution, and verification pipeline." Flagship-tier framing comparable to this dataset's other `very_high` entries. |
| `coding`                   | `very_high` | Same page, explicit: "a major leap in coding... able to autonomously code for over ten days to deliver complete projects." The single most emphasized capability in Alibaba's own framing. |
| `creative_writing`         | `medium`    | No creative-writing-specific claim found on the page checked. Kept at a conservative middle tier absent direct evidence, matching this dataset's `deepseek-v4-pro` (the closest comparable profile: `very_high`/`very_high`/`medium`/`high`) rather than assuming parity with the reasoning/coding claims. |
| `instruction_following`    | `high`      | No instruction-following-specific claim found either. Same conservative-absent-evidence approach as `creative_writing`, calibrated against `deepseek-v4-pro`'s profile as the nearest comparable entry. |

## Languages

Not independently confirmed against an Alibaba-published per-model
language list — no such list was found on the pages checked, the same
recurring gap already logged for every OpenAI entry in this dataset
(`IMPLEMENTATION_NOTES.md`, Iteration #1). Unlike a same-provider
sibling entry, there was nothing to inherit from — this is the first
Alibaba Cloud entry. Curated independently: `en`/`zh` at `very_high`
(Qwen's core trained/marketed languages), a set of major world
languages at `high`/`medium` consistent with the breadth this dataset
already applies to other flagship-tier entries without a published
list.

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 131,072    |

Confirmed directly against the official model page's Context Limits
table: "Context Window: 1000000," "Max Output Length: 131072." (The
page also lists thinking-mode-specific sub-limits and a max
chain-of-thought length; not represented in this schema, same
tiered-limit friction already logged for other providers,
`IMPLEMENTATION_NOTES.md` Iteration #5.)

## Cost `[Objective]`

| Field                    | Value   |
|----------------------------|---------|
| `input_per_million`         | $2.00  |
| `output_per_million`        | $6.00  |

Confirmed directly against the official model page's Pricing table,
**International (Singapore) scope**. Alibaba Cloud Model Studio prices
per region — the China (Beijing) scope is materially cheaper ($1.65/
$4.951) but requires a Mainland China account, so International scope
is used here as the one reachable from a standard account, same
approach already used for any other multi-tier provider in this
dataset. Additional pricing dimensions not represented in the schema:
cached input ($0.25/M), explicit cache creation ($2.50/M) and read
($0.17/M) — same tiered-pricing friction already logged in
`IMPLEMENTATION_NOTES.md` Iteration #5.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | DashScope-native and OpenAI-compatible endpoints, available across six regions (Beijing, Singapore, Frankfurt, Virginia, Tokyo, Hong Kong per the model page's region tabs) — broad, low-friction integration surface comparable to this dataset's other `high` entries. |
| `maturity`              | `stable` | Published on Alibaba Cloud's primary Model Studio documentation with a full spec/pricing/rate-limits page, not flagged preview/experimental/beta anywhere checked. |

---

## Access

One route: direct API via Alibaba Cloud Model Studio,
`api_billing_linked` (ordinary self-serve pay-as-you-go, no special
program gate found).

**Free access (`access.has_free_access`):** `false`. Alibaba Cloud
Model Studio does offer a free token quota for new users, but it's
explicitly restricted to the China (Beijing) region/service scope
(confirmed: "Only models in the China (Mainland) region... are
eligible for a free quota") — it does not apply to the International
scope this entry is priced and accessed through.

## Sources

- [Qwen3.8-Max model page](https://www.alibabacloud.com/help/en/model-studio/qwen3-8-max) — capabilities, context limits, pricing (both regions), snapshot versions.
- [Alibaba Cloud Model Studio — supported models overview](https://www.alibabacloud.com/help/en/model-studio/models) — confirms `qwen3.8-max` is a currently recommended/supported text-generation model, not a legacy or deprecated one.
- [Qwen Hugging Face organization](https://huggingface.co/Qwen) and [`Qwen/Qwen3.8-2.4T-A95B`](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) — confirms the separate open-weights checkpoint exists, its distinct model ID, license field, and text-only architecture tag (`qwen3_5_moe_text`).
- [Free quota for new users](https://www.alibabacloud.com/help/en/model-studio/new-free-quota) — confirms the free quota's China-region-only eligibility.

Accessed 2026-09-08, official Alibaba Cloud documentation (plus
Hugging Face for the open-weights variant's own model card) only.

## Verification result

New dataset entry, first Alibaba Cloud provider in this catalog.
Objective fields (capabilities, context window, max output, cost)
confirmed against official documentation, International/Singapore
pricing scope specifically. `json_mode` and `languages`/
`language_quality` flagged as inherited/curated, same recurring gap
as every provider without a published per-model list. The separate
open-weights checkpoint (`Qwen/Qwen3.8-2.4T-A95B`) was identified and
deliberately *not* folded into this entry or given a route here — its
different capabilities (text-only, smaller context) would misrepresent
either this entry or a self-hosted route built from it; left as an
explicit open question for the project owner instead of resolved by
assumption.
