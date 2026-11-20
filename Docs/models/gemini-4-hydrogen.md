# Gemini 4 Hydrogen

Dataset entry: [`dataset/models/gemini-4-hydrogen.yaml`](../../dataset/models/gemini-4-hydrogen.yaml)
Access routes: `dataset/access_routes/google/gemini-4-hydrogen-*.yaml` (5)
Last verified: 2026-11-20

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Proposed by the catalog bot on 2026-11-13
(branch `bot/catalog-2026-11-13`, never opened as a PR), the day after
Google made the model generally available; the bot records that the
owner asked for it to be added that day. It was admitted to `main` on
2026-11-20, assembled by hand from that branch (Iteration #46). The
review log's entry of 2026-11-06 listed "Hydrogen" among items treated
as "new providers or outside text/code". That is no longer the case: on
2026-11-12 Google published Gemini 4 Hydrogen (`gemini-4-hydrogen`) as a
generally available text and code model on the Gemini API models,
pricing, deprecations and release-notes pages. Every value below was
read on Google's own pages on 2026-11-13 and read again on 2026-11-20;
where the two readings differ (Antigravity), the text says so. The
Gemini API docs live at `aistudio.google.com/docs`.

---

## Identity

| Field      | Value               |
|------------|---------------------|
| `id`       | `gemini-4-hydrogen` |
| `name`     | Gemini 4 Hydrogen   |
| `provider` | Google              |
| `version`  | `4`                 |
| `license`  | `proprietary`       |

## Capabilities `[Objective]`

Source for all rows: https://aistudio.google.com/docs/models/gemini-4-hydrogen

| Field               | Value | Notes |
|---------------------|-------|-------|
| `vision`            | true  | "Inputs Text, Image, Video, Audio, and PDF". |
| `audio`             | true  | Audio **input**; "Audio generation Not supported", output is text. |
| `image_generation`  | false | "Image generation Not supported". |
| `tool_calling`      | true  | "Function calling Supported". |
| `structured_output` | true  | "Structured outputs Supported". |
| `json_mode`         | true  | Not itemized; same basis as the other Gemini entries. |

Documented but not in the schema: code execution, computer use, file
search, Google Search and Google Maps grounding, URL context, thinking
(levels `low`, `medium`, `high` (default) and `xhigh`), agentic video
understanding, implicit context caching only ("Explicit caching is not
supported"), Batch, Flex and Priority inference. No Live API.

## Quality `[Editorial]`

**Proposed by the bot on 2026-11-13; reasoning and coding changed by the
owner's call on 2026-11-20. The rest is the bot's judgment and the owner
has not reviewed it.** None of these is derived from a benchmark score.

| Field                   | Value       | Why |
|-------------------------|-------------|-----|
| `reasoning`             | `very_high` | The bot proposed `high`: the model page and the models page describe "speed and efficiency for everyday coding and agentic workflows", not the "strongest" wording used for Gemini 4 Carbon. The catalog already rates `gemini-3.8-flash`, the model Google's migration guide moves workloads from, at `very_high`, and the "What's new" page says Hydrogen "cuts fabricated claims by more than 5x compared to Gemini 3.8 Flash". A `high` would put the newer model below the one it improves on, so the owner chose `very_high`, the same value as `gemini-3.8-flash` (the scale has no tier above it). Carbon and Argon are also `very_high`; Google's "strongest" wording is a positioning claim, not a rating the scale can express. |
| `coding`                | `very_high` | Same reasoning. The "What's new" page says it "Writes cleaner code" than Gemini 3.8 Flash and is built for "fast agentic execution"; `gemini-3.8-flash` is `very_high` on coding. |
| `creative_writing`      | `medium`    | No creative-writing claim on any page read. The conservative default used for the other Gemini entries, and the value of `gemini-3.8-flash`. |
| `instruction_following` | `high`      | No claim specific to this dimension. The value of `gemini-3.8-flash`. |

## Languages

Google does not state languages on the model page. The entry uses the
curated Gemini set (Iteration #1), the same list and values as the other
Gemini entries.

## Operational `[Objective]`

| Field            | Value     | Source |
|------------------|-----------|--------|
| `context_window` | 1,048,576 | Model page: "Context window (unified input and output token limit) 1,048,576". |
| `max_output`     | 65,536    | Model page: "Max output 65,536 (default synchronous) / up to 1,048,576 (with long decode)". |

`max_output` stores the **default** limit. The 1,048,576-token maximum
with long decode is recorded here only (the Iteration #24 and #26
convention, the same one `gemini-4-carbon` and `gemini-4-argon` use).
Rate limits were not read this pass.

## Cost `[Objective]`

Paid Tier, USD per 1M tokens
(https://aistudio.google.com/docs/pricing):

| Field                | Paid tier |
|----------------------|-----------|
| `input_per_million`  | $1.50     |
| `output_per_million` | $7.50     |

Quoted: "Input price … $1.50" and "Output price (including thinking
tokens) … $7.50". The release notes say the same: "at paid-tier pricing
of $1.50 per 1M input tokens and $7.50 per 1M output tokens". No end
date is published, so there is no `effective_until` or `reverts_to`.

Not in the schema: context caching $0.075, "Implicit caching only
(explicit caching is not supported)", and Grounding with Google Search
at 5,000 free requests a month shared across Gemini 3 and newer, then
$14 per 1,000. The "What's new" page adds that implicit caching "runs
by default on prompts of at least 4,096 tokens and discounts cached
input tokens by 95% on cache hits". The pricing page shows no
long-context tier and no introductory-price window.

## Ecosystem `[Editorial]`

| Field              | Value    | Why |
|--------------------|----------|-----|
| `integration_ease` | `high`   | The same Gemini API surface as the rest of the family (GenerateContent and the Interactions API). Also in AI Studio, the Gemini app and Antigravity. |
| `maturity`         | `stable` | Model page: "Stable: gemini-4-hydrogen". On the public models page under Gemini 4, and GA in the release notes. |

## Lifecycle

`status: active`, `release_date: "2026-11-12"` (release notes, November
12, 2026: "Gemini 4 Hydrogen (`gemini-4-hydrogen`) generally available
(GA)"). Deprecations page: "gemini-4-hydrogen | November 12, 2026 | No
shutdown date announced". `shutdown_date` and `replacement` are `null`.

---

## Access

Five routes. The first four were read on Google's own pages on
2026-11-13 and the Vertex AI route on 2026-11-16; all five were read
again on 2026-11-20:

- **Gemini API** (`-direct-api`), with a billing-linked project for the
  paid path. The pricing page lists Free Tier input and output as "Free
  of charge", and the release notes say it is "Available on the free
  tier", so **`access.has_free_access` is `true`**. The free plan of
  AI Studio also names the model, which would count on its own
  (Iteration #32).
- **Google AI Studio** (`-ai-studio`), on AI Pro and both Ultra tiers
  in the route's plan list. The plans page: "Gemini 4 Hydrogen is
  available on all plans, including the Free plan." The overview table
  on that page has rows for Free, AI Pro and AI Ultra; Plus is not a
  row there, so it is not listed on this route. There is no free-plan
  entry in `dataset/subscriptions/`, so the Free plan is documented in
  the caveat and here, not as a `consumer_subscription` id.
- **Gemini app** (`-gemini-app`), on Google AI Plus, AI Pro and both
  Ultra tiers. The Google One plans page Plus card: "Access to Gemini 4
  Hydrogen and Deep Research in Gemini"; Plus FAQ: "Gemini app with
  access to Gemini 4 Hydrogen". Pro "gives you everything in Plus";
  Ultra "gives you a higher level of access to everything in Google AI
  Pro". The name matches the API id through Google's models page
  (Iteration #34).
- **Google Antigravity** (`-antigravity`), on AI Pro and both Ultra
  tiers. Antigravity's models page, "Reasoning model" table, read
  rendered in a browser on 2026-11-20 in English and in Spanish: Gemini 4
  Hydrogen "❌" on Free & Google AI Plus, "✅" on Google AI Pro with the
  footnote "Available on Google AI Pro for non-trial subscriptions
  only", "✅" on Google AI Ultra and "✅" on Enterprise. **This differs
  from the bot's reading of 2026-11-13**, which recorded "✅" in all four
  columns and listed the free plan and Google AI Plus. The page was not
  archived, so whether it changed in between or was misread is not
  known; the route follows the page as read on 2026-11-20. The release
  notes also say it is "the default model for the Antigravity agent in
  Gemini Managed Agents".

- **Google Cloud Vertex AI** (`-gcp-vertex`), on Vertex AI / Model
  Garden (Gemini Enterprise Agent Platform). The Agent Platform
  pricing page lists Gemini 4 Hydrogen at $1.50 / $7.50 per million
  tokens on the Global endpoint (non-global $1.65 / $8.25). The
  developer's guide uses the model id `gemini-4-hydrogen` and
  locations `global`, `us`, or `eu`. Billing is through Google Cloud,
  not the Gemini API key path.

The Google AI Ultra plans in the catalog are `google-ai-ultra-5x` and
`google-ai-ultra-20x`. Google's pages say "AI Ultra" without separating
the tiers, so both are listed.

## Sources

- https://aistudio.google.com/docs/models/gemini-4-hydrogen: id, modalities, token limits, capabilities, stability.
- https://aistudio.google.com/docs/models: name, listing under Gemini 4.
- https://aistudio.google.com/docs/pricing: paid prices, free-tier inclusion, implicit cache price.
- https://aistudio.google.com/docs/deprecations: release date, no shutdown date.
- https://aistudio.google.com/docs/changelog: GA on 2026-11-12, free tier, paid price.
- https://aistudio.google.com/docs/whats-new-gemini-4-hydrogen: paid price, thinking levels, implicit caching, default 64K/65,536 output.
- https://aistudio.google.com/docs/google-ai-plans: AI Studio on all plans, including Free.
- https://one.google.com/intl/en_us/about/google-ai-plans/: Gemini app on Plus, and Pro/Ultra by inclusion.
- https://antigravity.google/docs/models: Antigravity availability by plan.

All accessed 2026-11-13 and 2026-11-20 (the Antigravity page rendered in a
browser on 2026-11-20, because its table is built with JavaScript).

- https://cloud.google.com/model-garden/pricing: Vertex / Agent Platform Standard Global $1.50 / $7.50, non-global $1.65 / $8.25, cache read $0.075. Accessed 2026-11-16 and 2026-11-20.
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/guides/gemini-4-hydrogen: model id `gemini-4-hydrogen`, locations `global`, `us`, `eu`. Accessed 2026-11-16 and 2026-11-20.

## Verification result

New entry. Objective fields confirmed on Google's own pages on
2026-11-13 and again on 2026-11-20, except `languages` (not published,
so the curated set is used) and `json_mode` (not itemized). On the
second reading every value matched, except the Antigravity plan list
(see Access). The quality ratings are the bot's judgment, except
reasoning and coding, which the owner set to `very_high` on 2026-11-20;
the rest are not yet reviewed by the owner.

The Vertex AI / Model Garden route was added 2026-11-16 from the
Agent Platform pricing page and the Hydrogen developer's guide. No
objective field on the model YAML itself changed.
