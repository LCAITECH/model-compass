# Claude Sonnet 5.5

Dataset entry: [`dataset/models/claude-sonnet-5-5.yaml`](../../dataset/models/claude-sonnet-5-5.yaml)
Last verified: 2026-10-04

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted on the project owner's report
that a new Sonnet had shipped; every field below was read directly from
Anthropic's own pages (and each cloud's own docs for the access routes),
never from an aggregator or from a research agent's summary alone.

## Identity

| Field      | Value               |
|------------|---------------------|
| `id`       | `claude-sonnet-5-5` |
| `name`     | Claude Sonnet 5.5   |
| `provider` | Anthropic           |
| `version`  | `5.5`               |
| `license`  | `proprietary`       |

Released 2026-09-28; status "Active (latest)", retirement "not sooner
than 2027-09-28" (Anthropic's model page and lifecycle table).

## Capabilities `[Objective]`

| Field               | Value | Notes |
|----------------------|-------|-------|
| `vision`              | true  | Model page: "Text and images -> text"; overview: all current models support vision. |
| `audio`               | false | Input/output row is text and images only; audio is not listed anywhere. Inferred from that row, not an explicit "unsupported" statement. |
| `image_generation`    | false | Output is text only. |
| `tool_calling`        | true  | Server-side and client-side tools supported. Forced tool use (`tool_choice` `any`/`tool`) returns an error; `auto`/`none` work. |
| `structured_output`   | true  | Anthropic documents structured outputs / strict tool use as supported features. |
| `json_mode`           | true  | Not itemized as a separate feature; same basis as every other Claude entry (structured output confirmed). Inherited/curated. |

## Quality `[Editorial]`

Identical to `claude-sonnet-5` on purpose — that entry is already at
this scale's ceiling on reasoning/coding/instruction following, and
Anthropic's positioning for 5.5 ("the best combination of speed and
intelligence"; stronger at everyday tasks, bug fixing and polished
documents; faster and cheaper per task than Sonnet 5 at the same price)
is a speed/cost improvement claim, not evidence of a higher tier on any
dimension. Anthropic itself positions it below Opus 5.5 for complex,
open-ended work, which is already reflected by Opus 5.5 sharing the same
ceiling at a higher price rather than by lowering this entry.
`creative_writing` stays `high`, same as every Claude entry (no
creative-writing-specific claim exists for any of them).

## Languages

Not independently reconfirmed — Anthropic publishes no per-model
language list. Reused the curated set from `claude-sonnet-5` (same
family), itself a curated list, not an Anthropic-published fact
(see [IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational / Cost `[Objective]`

`context_window` 1,000,000, `max_output` 128,000 (synchronous API; the
Batch API allows 300K with a beta header, not represented in this
schema). $2.00 input / $10.00 output per million tokens — standard
Anthropic pricing, no introductory rate or expiry, no long-context
premium (the full 1M window is billed at the standard rate).
Cache/batch tiers are not represented in the schema (same friction as
`IMPLEMENTATION_NOTES.md` Iteration #5).

## Ecosystem `[Editorial]`

`integration_ease: high`, `maturity: stable` — "Active" in Anthropic's
lifecycle table, available on five platforms.

## Access

Four routes, each confirmed on the platform's own documentation:
direct API (Anthropic model page), AWS Bedrock (AWS's models-at-a-glance
page lists it under Claude 5.x), Google Vertex (Google Cloud's Claude
partner-models page lists it), Microsoft Foundry (Microsoft's
Claude-models page lists `claude-sonnet-5-5` as "Hosted on Azure: GA").
**No Claude-subscription route:** Anthropic's pages mention the Claude
apps but name no plan tier (Pro/Max), so none was added rather than
guessed. `has_free_access: false`.

## Sources

- [Claude Sonnet 5.5 model page](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)
- [Models overview](https://platform.claude.com/docs/en/models/overview)
- [Model deprecations / lifecycle](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- [Amazon Bedrock models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)
- [Claude on Google Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude)
- [Claude models in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/claude-models)

Accessed 2026-10-04, official documentation only.

## Verification result

New dataset entry. Objective fields confirmed against official pages;
`audio` inferred from the modality row; `json_mode` and languages
inherited/curated as for every Claude entry. Subscription route
deliberately omitted (tier not confirmed).
