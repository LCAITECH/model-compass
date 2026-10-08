# Claude Haiku 5.5

Dataset entry: [`dataset/models/claude-haiku-5-5.yaml`](../../dataset/models/claude-haiku-5-5.yaml)
Last verified: 2026-10-08

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from the 2026-10-08 catalog
audit; every objective field below was re-read directly on Anthropic's
own pages (and each cloud's own docs for the access routes), never
from an aggregator or from the audit summary alone.

## Identity

| Field      | Value              |
|------------|--------------------|
| `id`       | `claude-haiku-5-5` |
| `name`     | Claude Haiku 5.5   |
| `provider` | Anthropic          |
| `version`  | `5.5`              |
| `license`  | `proprietary`      |

Released 2026-10-07; status "Active (latest)" on the model page, and
the models overview now lists it as the current Haiku (Claude Haiku 4.5
moved to "Legacy models (still available)").

## Capabilities `[Objective]`

| Field               | Value | Notes |
|----------------------|-------|-------|
| `vision`              | true  | Model page: "Text and images -> text"; overview: all current models support vision. |
| `audio`               | false | Input/output row is text and images only; audio is not listed anywhere. Inferred from that row, not an explicit "unsupported" statement. |
| `image_generation`    | false | Output is text only. |
| `tool_calling`        | true  | Overview: all current models support tool use. Pricing page's tool-use table lists Haiku 5.5 for both `auto`/`none` (286 tokens) and `any`/`tool` (406 tokens), so forced tool use is supported, unlike Sonnet/Opus 5.5. |
| `structured_output`   | true  | Anthropic documents structured outputs (JSON outputs + strict tool use) as a GA API feature with no per-model exclusion listed. Same basis as every other Claude entry. |
| `json_mode`           | true  | Not itemized as a separate feature; same basis as every other Claude entry (structured output confirmed). Inherited/curated. |

## Quality `[Editorial]`

Identical to `claude-haiku-4-5` (`reasoning`/`coding`/`instruction_following`
`high`, `creative_writing` `medium`). Anthropic's own positioning for 5.5
is "for high-volume, latency-sensitive tasks such as classification,
extraction, and routing" (plus subagent tasks), with "Fastest"
comparative latency — a speed/cost positioning, not a provider
statement that it reaches the `very_high` tier held by Sonnet 5.5 /
Opus 5.5. The one sourced signal of improvement over Haiku 4.5 (reliable
knowledge cutoff Jun 2026, same as Sonnet/Opus 5.5) and adaptive
thinking with the effort parameter keep it at `high`, not lower; no
signal supports raising any dimension. `creative_writing` stays
`medium` — no creative-writing claim for any Haiku.

## Languages

Not independently reconfirmed — Anthropic publishes no per-model
language list ("multilingual capabilities" for all current models
only). Reused the curated Claude set (same as `claude-haiku-4-5` /
`claude-sonnet-5-5`), itself a curated list, not an Anthropic-published
fact (see [IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

`context_window` 1,000,000, `max_output` 128,000 (synchronous Messages
API; the Batch API allows 300K with the `output-300k-2026-03-24` beta
header, not represented in this schema). Both from the model page and
the models overview table.

## Cost `[Objective]`

**Two tiers by prompt length** — the first Claude model priced this
way ("Claude 4.6 and later models (except Claude Haiku 5.5) include
the full 1M token context window at standard pricing"):

| Prompt length        | Input / MTok | Output / MTok | 5m cache write | 1h cache write | Cache read |
|----------------------|--------------|---------------|----------------|----------------|------------|
| up to 100,000 tokens | $0.10        | $0.50         | $0.125         | $0.20          | $0.01      |
| over 100,000 tokens  | $0.50        | $2.50         | $0.625         | $1.00          | $0.05      |

`cost.*` stores the **≤100k tier ($0.10 / $0.50)**, the rate a typical
first request hits, since the schema holds a single rate (same
convention as Gemini 2.5 Pro's >200k tier — `IMPLEMENTATION_NOTES.md`
Iteration #5, now Iteration #24). Consequence worth knowing: the engine
ranks this model at $0.60 blended (`low` tier); a workload that
routinely sends >100k-token prompts pays 5x that ($3.00 blended,
`medium` band). Batch API: 50% off both tiers ($0.05/$0.25 and
$0.25/$1.25). No introductory rate or expiry.

## Ecosystem `[Editorial]`

`integration_ease: high`, `maturity: stable` — GA, "Active" in
Anthropic's lifecycle table, available on five platforms; same call as
`claude-sonnet-5-5` / `claude-opus-5-5` at their admission.

## Access

Four routes, each confirmed on the platform's own documentation:
direct API (Anthropic model page), AWS Bedrock (AWS's models-at-a-glance
page lists Claude Haiku 5.5 under Claude 5.x), Google Vertex (Google
Cloud's own Claude Haiku 5.5 page: model id `claude-haiku-5-5`, launch
stage GA), Microsoft Foundry (Microsoft's Claude-models page lists
`claude-haiku-5-5` as "Hosted on Azure: GA"). **No Claude-subscription
route:** Anthropic's pages name no plan tier, so none was added rather
than guessed. `has_free_access: false` — Anthropic's pricing FAQ
describes only a small one-time credit for new users, not continuous
free access.

**Rate limits (prose only, per Iteration #8):** Anthropic's rate-limits
page lists Claude Haiku 5.5 at the Start tier (entry-level standard
tier) with 1,000 RPM, 2,000,000 ITPM, 400,000 OTPM; Build tier 5,000 /
5,000,000 / 1,000,000; Scale tier 10,000 / 10,000,000 / 2,000,000.
Cached reads don't count toward ITPM. New organizations may start in a
lower Evaluation tier.

## Lifecycle (informational — not a schema field)

`claude-haiku-5-5`: Active, Deprecated N/A, tentative retirement "Not
sooner than October 7, 2027" (Anthropic's model deprecations page and
models overview; applies to Anthropic-operated platforms). Google
Cloud's page states the same floor for Vertex.

## Sources

- [Claude Haiku 5.5 model page](https://platform.claude.com/docs/en/models/haiku-5-5/overview) — id, release, status, context/output, modalities, platforms, pricing tiers.
- [Models overview](https://platform.claude.com/docs/en/models/overview) — current lineup, API/cloud ids, retirement floor, capabilities shared by all current models.
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) — both price tiers, batch, long-context note, tool-use token table.
- [Rate limits](https://platform.claude.com/docs/en/api/rate-limits) — Start/Build/Scale limits.
- [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — lifecycle.
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Amazon Bedrock models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)
- [Claude Haiku 5.5 on Google Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/haiku-5-5)
- [Claude models in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/claude-models)

Accessed 2026-10-08, official documentation only.

## Verification result

New dataset entry. Objective fields confirmed against official pages;
`audio` inferred from the modality row; `json_mode` and languages
inherited/curated as for every Claude entry. `cost.*` deliberately
holds the ≤100k tier only. Subscription route omitted (tier not
confirmed).
