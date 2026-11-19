# Gemini 4 Carbon

Dataset entry: [`dataset/models/gemini-4-carbon.yaml`](../../dataset/models/gemini-4-carbon.yaml)
Access routes: `dataset/access_routes/google/gemini-4-carbon-*.yaml` (4)
Last verified: 2026-11-10

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Proposed by the catalog bot on 2026-11-10,
the day Google made the model generally available; the owner asked for
it to be added the same day. The review log's entry of 2026-10-31
records that Carbon was "still not on Google's models page". It is now:
the models page, the model page, the pricing page, the deprecations
page and the release notes all list it. Every value below was read on
Google's own pages on 2026-11-10. The Gemini API docs now live at
`aistudio.google.com/docs` (the old `ai.google.dev/gemini-api/docs`
URLs redirect there), so this entry cites the new URLs.

---

## Identity

| Field      | Value             |
|------------|-------------------|
| `id`       | `gemini-4-carbon` |
| `name`     | Gemini 4 Carbon   |
| `provider` | Google            |
| `version`  | `4`               |
| `license`  | `proprietary`     |

## Capabilities `[Objective]`

Source for all rows: https://aistudio.google.com/docs/models/gemini-4-carbon

| Field               | Value | Notes |
|---------------------|-------|-------|
| `vision`            | true  | "Inputs Text, Image, Video, Audio, and PDF". |
| `audio`             | true  | Audio **input**; "Audio generation Not supported", output is text. |
| `image_generation`  | false | "Image generation Not supported". |
| `tool_calling`      | true  | "Function calling Supported". |
| `structured_output` | true  | "Structured outputs Supported". |
| `json_mode`         | true  | Not itemized; same basis as the other Gemini entries. |

Documented but not in the schema: code execution, computer use, file
search, Google Search and Google Maps grounding, URL context, thinking,
agentic video understanding, implicit context caching only ("Explicit
caching is not supported"), Batch, Flex and Priority inference. No Live
API.

## Quality `[Editorial]`

**The bot's judgment, 2026-11-10, for owner review.** None of these is
derived from a benchmark score.

| Field                   | Value       | Why |
|-------------------------|-------------|-----|
| `reasoning`             | `very_high` | Model page: "our most capable reasoning model, built for complex software engineering, mathematical and scientific problem solving, high factual accuracy, autonomous multi-step agents". The models page calls it "Our strongest reasoning model". The scale stops at `very_high`. |
| `coding`                | `very_high` | Same sentence: "complex software engineering" comes first, and the release notes say it is "built for sustained agentic coding". |
| `creative_writing`      | `medium`    | No creative-writing claim on any page read. The conservative default used for the other Gemini entries. |
| `instruction_following` | `high`      | No claim specific to this dimension. "High factual accuracy" is about facts, not instructions. One step below the ceiling. |

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
convention, the same one `gemini-4-argon` uses). Rate limits were not
read this pass.

## Cost `[Objective]`

Paid Tier, Standard, USD per 1M tokens
(https://aistudio.google.com/docs/pricing):

| Field                | Through 2026-11-30 | From 2026-12-01 |
|----------------------|--------------------|-----------------|
| `input_per_million`  | $2.00              | $4.00           |
| `output_per_million` | $10.00             | $20.00          |

Quoted: "$2.00 through November 30, 2026. $4.00 starting December 1,
2026." and "$10.00 through November 30, 2026. $20.00 starting December
1, 2026." Output includes thinking tokens. The release notes say the
same: "available at introductory pricing of $2.00 per 1M input tokens
and $10.00 per 1M output tokens through November 30, 2026". The entry
stores the current price with `effective_until: "2026-11-30"` and
`reverts_to` $4.00 / $20.00. From 2026-12-01 `tests/test_catalog_dates.py`
will flag it (`CATALOG_BOT.md`, section 4).

Not in the schema: context caching $0.10 → $0.20 (implicit only), and
Grounding with Google Search at 5,000 free requests a month shared
across Gemini 3 and newer, then $14 per 1,000. The pricing page shows no
long-context tier.

## Ecosystem `[Editorial]`

| Field              | Value    | Why |
|--------------------|----------|-----|
| `integration_ease` | `high`   | The same Gemini API surface as the rest of the family. Also in AI Studio, the Gemini app and Antigravity. |
| `maturity`         | `stable` | Model page: "Stable: gemini-4-carbon". On the public models page under Gemini 4, and GA in the release notes. |

## Lifecycle

`status: active`, `release_date: "2026-11-10"` (release notes, November
10, 2026: "Gemini 4 Carbon (`gemini-4-carbon`) generally available
(GA)"). Deprecations page: "gemini-4-carbon | November 10, 2026 | No
shutdown date announced". `shutdown_date` and `replacement` are `null`.

---

## Access

Four routes, each read on Google's own pages on 2026-11-10:

- **Gemini API** (`-direct-api`), with a billing-linked project. The
  pricing page says "Gemini 4 Carbon is not available on the Free tier",
  so **`access.has_free_access` is `false`**.
- **Google AI Studio** (`-ai-studio`), on both Ultra tiers only. The
  plans page: "Gemini 4 Carbon requires an AI Ultra plan in AI Studio
  (not available on the Free or AI Pro plans)". The plan's quota covers
  the AI Studio web interface only.
- **Gemini app** (`-gemini-app`), on both Ultra tiers. The Google One
  plans page: "Higher access to Gemini 4 Carbon in the Gemini app",
  "Unlock our strongest model Gemini 4 Carbon. Sign up for a Google AI
  Ultra plan", "Available to Google AI Ultra subscribers in select
  countries". Hence `region_scope: region_dependent`. Google's AI Pro
  support article does not name Carbon. The name matches the API id
  through Google's models page (Iteration #34).
- **Google Antigravity** (`-antigravity`), on both Ultra tiers.
  Antigravity's models page, "Reasoning model" table: Gemini 4 Carbon
  "❌" on Free & Google AI Plus, "❌" on Google AI Pro, "✅" on Google AI
  Ultra and Enterprise. The Google One page adds "access to Gemini 4
  Carbon and Gemini 4 Argon in Google Antigravity" under AI Ultra.

The Google AI Ultra plans in the catalog are `google-ai-ultra-5x` and
`google-ai-ultra-20x`. Google's pages say "AI Ultra" without separating
the tiers, so both are listed. Vertex AI / Gemini Enterprise Agent
Platform availability was not checked, so there is no cloud route.

## Sources

- https://aistudio.google.com/docs/models/gemini-4-carbon: id, modalities, token limits, capabilities, stability.
- https://aistudio.google.com/docs/models: name, listing under Gemini 4.
- https://aistudio.google.com/docs/pricing: prices and their dates, free-tier exclusion.
- https://aistudio.google.com/docs/deprecations: release date, no shutdown date.
- https://aistudio.google.com/docs/changelog: GA on 2026-11-10, introductory price.
- https://aistudio.google.com/docs/google-ai-plans: AI Studio needs AI Ultra.
- https://one.google.com/intl/en_us/about/google-ai-plans/: Gemini app and Antigravity on AI Ultra.
- https://antigravity.google/docs/models: Antigravity availability by plan.

All accessed 2026-11-10.

## Verification result

New entry. Objective fields confirmed on Google's own pages, except
`languages` (not published, so the curated set is used) and `json_mode`
(not itemized). The quality ratings are the bot's judgment and are
flagged for owner review.
