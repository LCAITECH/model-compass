# Claude Opus 5.5

Dataset entry: [`dataset/models/claude-opus-5-5.yaml`](../../dataset/models/claude-opus-5-5.yaml)
Last verified: 2026-10-04

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted on the project owner's report
that a new Opus had shipped; every field below was read directly from
Anthropic's own pages (and each cloud's own docs for the access routes),
never from an aggregator or from a research agent's summary alone.

## Identity

| Field      | Value            |
|------------|------------------|
| `id`       | `claude-opus-5-5`|
| `name`     | Claude Opus 5.5  |
| `provider` | Anthropic        |
| `version`  | `5.5`            |
| `license`  | `proprietary`    |

Released 2026-09-22; status "Active (latest)", retirement "not sooner
than 2027-09-22". Anthropic's models overview now says to "start with
Claude Opus 5.5 for most workloads" and to use Claude Fable 5.1 for
demanding reasoning and long-horizon agentic work.

## Capabilities `[Objective]`

Same as `claude-sonnet-5-5`: vision true ("Text and images -> text"),
audio false (not listed; inferred from the modality row), image
generation false, tool calling true (forced tool use unsupported,
`auto`/`none` only), structured output true, `json_mode` true
(inherited/curated, not itemized separately). Adaptive thinking is
always on and can't be disabled.

## Quality `[Editorial]`

Same ceiling as `claude-opus-5` (`very_high` on reasoning, coding and
instruction following; `high` on creative writing), deliberately. Anthropic's
own positioning ("for long-running agentic coding and knowledge work";
announcement: performs at the level of Fable 5.1 on most work at lower
cost than Opus 5) supports the existing top of the scale, not a rating
above it — this 4-level scale has no room above `very_high`, and
Anthropic still positions Fable 5.1 above it for the hardest reasoning.
No creative-writing-specific claim exists, so `creative_writing` stays
`high` like every Claude entry. Benchmark figures seen in search results
were not used, per project rule.

## Languages

Curated set reused from `claude-opus-5` (same family); not an
Anthropic-published list (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational / Cost `[Objective]`

`context_window` 1,000,000, `max_output` 128,000 (Batch API: 300K with a
beta header, not represented). $4.00 input / $20.00 output per million
tokens — 20% below Opus 5's list price, no introductory rate or expiry,
no long-context premium. Cache reads are $0.20/M (a different ratio than
other Claude models); cache/batch tiers are not represented in the
schema.

## Ecosystem `[Editorial]`

`integration_ease: high`, `maturity: stable`.

## Access

Four routes, each confirmed on the platform's own documentation: direct
API, AWS Bedrock, Google Vertex and Microsoft Foundry (Microsoft lists
`claude-opus-5-5` as "Hosted on Azure: GA"). No Claude-subscription
route: no plan tier is named on Anthropic's pages. `has_free_access:
false`.

## Sources

- [Claude Opus 5.5 model page](https://platform.claude.com/docs/en/models/opus-5-5/overview)
- [Models overview](https://platform.claude.com/docs/en/models/overview)
- [Model deprecations / lifecycle](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- [Amazon Bedrock models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)
- [Claude on Google Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude)
- [Claude models in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/claude-models)

Accessed 2026-10-04, official documentation only.

## Verification result

New dataset entry. Objective fields confirmed against official pages;
`audio` inferred; `json_mode` and languages inherited/curated.
Subscription route deliberately omitted (tier not confirmed).
