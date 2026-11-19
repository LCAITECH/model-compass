# Claude Fable 5.2

Dataset entry: [`dataset/models/claude-fable-5-2.yaml`](../../dataset/models/claude-fable-5-2.yaml)
Access routes: `dataset/access_routes/anthropic/claude-fable-5-2-*.yaml` (5)
Last verified: 2026-11-10

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Proposed by the catalog bot on 2026-11-10
after its daily audit found the model on Anthropic's pages; the owner
asked for it to be added the same day. Every value below was read on
Anthropic's, AWS's, Microsoft's and Google Cloud's own pages on
2026-11-10. No AI-written summary or digest was used as a source.

---

## Identity

| Field      | Value              |
|------------|--------------------|
| `id`       | `claude-fable-5-2` |
| `name`     | Claude Fable 5.2   |
| `provider` | Anthropic          |
| `version`  | `5.2`              |
| `license`  | `proprietary`      |

**Claude Mythos 5.2 is not this entry.** Anthropic offers "the same
capabilities only to organizations verified through Anthropic's
verification programs" under that name (model page). It is gated, so it
stays out, like the other Mythos models.

## Capabilities `[Objective]`

| Field               | Value | Notes |
|---------------------|-------|-------|
| `vision`            | true  | Model page: "Input → output: Text and images → text". |
| `audio`             | false | Not listed as an input. |
| `image_generation`  | false | Output is text. |
| `tool_calling`      | true  | Models overview: "All current models support text and image input, text output, multilingual capabilities, vision, and tool use." The model page adds that forced tool use (`tool_choice` `any` or `tool`) returns a 400 error. |
| `structured_output` | true  | Same basis as every other Claude entry (not itemized per model). |
| `json_mode`         | true  | Same as above. |

Documented but not in the schema: adaptive thinking is always on and
cannot be turned off (default effort `high`); `temperature`, `top_p` and
`top_k` must be omitted; fast mode ($16/$80 per million tokens); the
model "requires 30-day data retention and isn't available under zero
data retention unless expressly authorized by Anthropic"; queries
flagged by its cybersecurity and biology safeguards are answered by
Opus models instead (Anthropic's Fable page).

## Quality `[Editorial]`

**The bot's judgment, 2026-11-10, for owner review.** None of these is
derived from a benchmark score.

| Field                   | Value       | Why |
|-------------------------|-------------|-----|
| `reasoning`             | `very_high` | Anthropic's Models overview recommends it "for demanding reasoning and long-horizon agentic work", above Opus 5.5; the Fable page calls it "our most capable generally available model for technical fields". The scale has no tier above `very_high`. |
| `coding`                | `very_high` | Fable page: "our most capable model for ambitious software engineering". |
| `creative_writing`      | `high`      | No creative-writing claim on any page read. Anthropic positions the model for technical work and recommends Opus 5.5 "for most everyday coding and knowledge work". `high` is Opus 5.5's value here. Fable 5.1 holds `very_high`, a value inherited from Fable 5, not from its own evidence (see `claude-fable-5-1.md`), so it was not copied. |
| `instruction_following` | `very_high` | Flagship positioning on the overview and model pages, and no counter-evidence. |

## Languages

The curated Claude set (Iteration #1), the same list and values as the
other Claude entries. Anthropic's multilingual support page lists Claude
Fable 5.2 with Global-MMLU scores of 99.2% to 99.8% of its English score
in Spanish, Portuguese, Italian, French, German, Arabic, Chinese,
Korean, Japanese and Hindi. That table is a benchmark, so it was not
used to raise any value. It also gives no reason to lower one.

## Operational `[Objective]`

| Field            | Value     | Source |
|------------------|-----------|--------|
| `context_window` | 1,000,000 | Model page: "Context window: 1M tokens". |
| `max_output`     | 128,000   | Model page: "Max output: 128K tokens" (synchronous Messages API limit). |

Rate limits: the model has its own limits on the Claude API. The schema
has no field for them.

## Cost `[Objective]`

| Field                | Value  |
|----------------------|--------|
| `input_per_million`  | $8.00  |
| `output_per_million` | $40.00 |

Pricing page: "Claude Fable 5.2 | $8 / MTok | $10 / MTok | $16 / MTok |
$0.20 / MTok | $40 / MTok" (base input, 5-minute cache write, 1-hour
cache write, cache hits, output). That is down from $10/$50 on Fable 5.1
(Fable page: "down from $10 and $50 for Fable 5.1"). Not in the schema:
cache reads at 0.025x the base input price, Batch API $4/$20, fast mode
$16/$80, US-only inference at 1.1x. No long-context premium: the full
1M window is at the standard price.

## Ecosystem `[Editorial]`

| Field              | Value    | Why |
|--------------------|----------|-----|
| `integration_ease` | `high`   | Claude API, plus Bedrock, Foundry and Vertex AI confirmed on their own pages (Access below). |
| `maturity`         | `stable` | Listed in Anthropic's Models overview compare table (the public model catalog) and "Active" on the deprecations page. |

## Lifecycle

`status: active`, `release_date: "2026-11-09"` (model page: "Released
November 9, 2026"). The deprecations page says "claude-fable-5-2 |
Active | N/A | Not sooner than November 9, 2027". That is a floor, not a
shutdown date, so `shutdown_date` is `null`.

**Claude Fable 5.1 is unchanged.** It no longer appears in the
overview's compare table, which now lists it under "Legacy models (still
available)", and it is still on the pricing page at $10/$50. The
deprecations page still says "claude-fable-5-1 | Active | N/A | Not
sooner than September 1, 2027". No deprecation and no successor are
published, so its lifecycle stays as it is.

---

## Access

Five routes, each read on its own provider's page on 2026-11-10:

- **Claude API** (`-direct-api`): model id `claude-fable-5-2` (overview,
  model page, and the Fable page: "use claude-fable-5-2 via the Claude
  API").
- **Claude subscription** (`-claude-subscription`): Anthropic's Fable by
  plan article says that on "Max plans, Ultra plans, premium seats on
  Team plans, and premium seats on legacy seat-based Enterprise plans",
  all three Fable models "are a standard part of your plan", up to 50%
  of the weekly limit. On Pro and Team standard seats they "run on
  pay-as-you-go usage credits". The route lists `claude-max-5x` and
  `claude-ultra`. The article also mentions limited-time launch offers
  with extra Fable usage. They have no end date on that page, so they are
  only in the caveat. In Claude Code, Fable 5.2 "requires version
  2.1.321 or later".
- **Amazon Bedrock** (`-aws-bedrock`): AWS's model cards page lists
  "Claude Fable 5.2" under Anthropic's Claude 5.x models. Anthropic gives
  the Bedrock id `anthropic.claude-fable-5-2`.
- **Microsoft Foundry** (`-azure-foundry`): Microsoft's Claude models
  page lists `claude-fable-5-2` as "Hosted on Anthropic infrastructure:
  Preview", 1M / 128K, with no Azure-hosted option.
- **Google Cloud Vertex AI** (`-gcp-vertex`): Google's model page for
  Fable 5.2 says "Model ID claude-fable-5-2", "Launch stage GA", release
  November 9, 2026, US and Europe multi-regions and the global endpoint,
  with the Advanced AI Safety Addendum required.

**Free access (`access.has_free_access`):** `false`. There is no free
API tier ("New users receive a small amount of free credits", a one-time
credit), and the Fable article says Fable models "aren't available on
the Free plan".

## Sources

- [Model page](https://platform.claude.com/docs/en/models/fable-5-2/overview): release date, id, limits, prices, modalities, availability, retirement floor, Mythos 5.2.
- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview): compare table, platform ids, legacy list (Fable 5.1).
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing): prices, cache, batch and fast-mode rates.
- [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations): status and retirement floors of Fable 5.2 and 5.1.
- [Claude Fable](https://www.anthropic.com/claude/fable): positioning, availability, safeguards, data retention.
- [Multilingual support](https://platform.claude.com/docs/en/build-with-claude/multilingual-support): language table (not used for values).
- [Claude Fable models on your plan](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan): plans that include it.
- [Amazon Bedrock model cards](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html), [Claude models in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/claude-models), [Claude Fable 5.2 on Google Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/fable-5-2): cloud routes.

All accessed 2026-11-10.

## Verification result

New entry. Objective fields confirmed on Anthropic's and the clouds' own
pages. `structured_output`, `json_mode` and the language list follow the
existing Claude conventions. The quality ratings are the bot's judgment
and are flagged for owner review.
