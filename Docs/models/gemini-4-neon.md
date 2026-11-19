# Gemini 4 Neon

Dataset entry: [`dataset/models/gemini-4-neon.yaml`](../../dataset/models/gemini-4-neon.yaml)
Access routes: `dataset/access_routes/google/gemini-4-neon-*.yaml` (5)
Last verified: 2026-11-19

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Proposed by the catalog bot on 2026-11-19,
the day after Google made the model generally available; the owner asked
for it to be added that day. Every value below was read on Google's own
pages on 2026-11-19. The Gemini API docs live at `ai.google.dev` and
`aistudio.google.com/docs`.

---

## Identity

| Field      | Value            |
|------------|------------------|
| `id`       | `gemini-4-neon`  |
| `name`     | Gemini 4 Neon    |
| `provider` | Google           |
| `version`  | `4`              |
| `license`  | `proprietary`    |

## Capabilities `[Objective]`

Source for all rows: https://ai.google.dev/gemini-api/docs/models/gemini-4-neon

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
supported"), Batch, Flex and Priority inference. No Live API. The
2026-11-18 release notes also add Microsoft Office and OpenDocument
file input (Word, PowerPoint, Excel and OpenDocument), which the model
page's input list does not yet itemize.

## Quality `[Editorial]`

**The bot's judgment, 2026-11-19, for owner review.** None of these is
derived from a benchmark score, and none is copied from a sibling. The
same criterion used for Gemini 4 Hydrogen applies: rate from Google's
own positioning of the model.

| Field                   | Value       | Why |
|-------------------------|-------------|-----|
| `reasoning`             | `very_high` | The model page describes "frontier-level intelligence with fast end-to-end task completion across complex software engineering, knowledge work, and science workflows". The official introduction places Neon between Carbon (the hardest long-horizon work) and Hydrogen (fast everyday execution) and calls out "frontier-level reasoning". That is ceiling language on this scale, which stops at `very_high`. Hydrogen stayed at `high` because its published role was everyday work, not frontier reasoning. |
| `coding`                | `very_high` | The same model-page sentence leads with "complex software engineering". The official introduction frames Neon as "Built for production-ready code" and "Engineered for long-running agent workflows". That is the wording reserved for the ceiling, unlike Hydrogen's "everyday coding". |
| `creative_writing`      | `medium`    | No dedicated creative-writing positioning. The introduction's consumer section says Neon "writes clearly, with well-structured responses and a natural, direct tone" in the Gemini app; that is not enough to raise the conservative default used for the other Gemini 4 entries. |
| `instruction_following` | `high`      | The official introduction says Neon "excels at multi-step instruction following". That supports a strong rating. The ceiling is still reserved; Carbon and Argon also sit at `high` on this dimension. |

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
Rate limits were not read this pass. In Google Antigravity the published
context window is up to 512K tokens, recorded on that route's caveat.

## Cost `[Objective]`

Paid Tier, USD per 1M tokens
(https://ai.google.dev/gemini-api/docs/pricing):

| Field                | Paid tier |
|----------------------|-----------|
| `input_per_million`  | $3.00     |
| `output_per_million` | $15.00    |

Quoted: "Input price … $3.00" and "Output price (including thinking
tokens) … $15.00". The release notes say the same: "at pricing of $3.00
per 1M input tokens and $15.00 per 1M output tokens". No end date and
no prompt-length split (>200k or otherwise) are published, so there is
no `effective_until` or `reverts_to`, and no second tier to describe.

Not in the schema: context caching $0.15, "Implicit caching only
(explicit caching is not supported)". The official introduction states
the cache rate as "$0.15 per million cached input tokens, a 95%
discount". Grounding with Google Search is 5,000 free requests a month
shared across Gemini 3 and newer, then $14 per 1,000, subject to a
daily cap of 1,500 requests per day.

## Ecosystem `[Editorial]`

| Field              | Value    | Why |
|--------------------|----------|-----|
| `integration_ease` | `high`   | The same Gemini API surface as the rest of the family (GenerateContent and the Interactions API). Also in AI Studio, the Gemini app, Antigravity and Vertex AI / Agent Platform. |
| `maturity`         | `stable` | Model page: "Stable: gemini-4-neon". On the public models page under Gemini 4, and GA in the release notes. |

## Lifecycle

`status: active`, `release_date: "2026-11-18"` (release notes, November
18, 2026: "Gemini 4 Neon (`gemini-4-neon`) generally available (GA)").
Deprecations page: "gemini-4-neon | November 18, 2026 | No shutdown date
announced". `shutdown_date` and `replacement` are `null`.

---

## Access

Five routes, all read on Google's own pages on 2026-11-19:

- **Gemini API** (`-direct-api`), with a billing-linked project. The
  pricing page lists Free Tier input and output as "Not available", and
  the release notes place it "on the paid tier", so
  **`access.has_free_access` is `false`**.
- **Google AI Studio** (`-ai-studio`), on AI Pro and both Ultra tiers.
  The plans page: "Gemini 4 Argon and Gemini 4 Neon are available on AI
  Pro and AI Ultra (not available on the Free plan)."
- **Gemini app** (`-gemini-app`), on Google AI Pro and both Ultra
  tiers. The Google One plans page: Pro "Gemini app with access to
  Gemini 4 Neon"; Ultra "Gemini app with higher access to Gemini 4
  Carbon and Gemini 4 Neon". Plus names Hydrogen, not Neon. The name
  matches the API id through Google's model page (Iteration #34).
- **Google Antigravity** (`-antigravity`), on Google AI Pro (a paid
  plan, or a trial on eligible premium devices) and both Ultra tiers.
  Antigravity's models page, "Reasoning model" table: Gemini 4 Neon
  "❌" on Free & Google AI Plus, "✅" on Google AI Pro (dagger note),
  Google AI Ultra and Enterprise. The same page sets the Antigravity
  context window at up to 512K tokens. Enterprise is documented in the
  caveat, not as a `consumer_subscription` id.
- **Google Cloud Vertex AI** (`-gcp-vertex`), on Vertex AI / Model
  Garden (Gemini Enterprise Agent Platform). The Agent Platform
  pricing page lists Gemini 4 Neon at $3.00 / $15.00 per million
  tokens on the Global endpoint (non-global $3.30 / $16.50; Global
  cache read $0.15). The model page uses the id `gemini-4-neon`,
  locations `global`, `us`, or `eu`, and says Neon "is available to
  verified enterprise customers in select regions". Billing is through
  Google Cloud, not the Gemini API key path.

The Google AI Ultra plans in the catalog are `google-ai-ultra-5x` and
`google-ai-ultra-20x`. Google's pages say "AI Ultra" without separating
the tiers, so both are listed.

The official introduction also mentions "Gemini 4 Neon for cyber"
rolling out to Fairwind Program members. That is not a separate model
id on the Gemini API models or pricing pages, so no extra route was
added.

## Sources

- https://ai.google.dev/gemini-api/docs/models/gemini-4-neon: id, modalities, token limits, capabilities, stability.
- https://ai.google.dev/gemini-api/docs/pricing: paid prices, no free tier, implicit cache price, no prompt-length split.
- https://ai.google.dev/gemini-api/docs/deprecations: release date, no shutdown date.
- https://ai.google.dev/gemini-api/docs/changelog: GA on 2026-11-18, paid price, thinking levels, long decode, Office/OpenDocument input.
- https://aistudio.google.com/docs/google-ai-plans: AI Studio on AI Pro and AI Ultra, not Free.
- https://one.google.com/intl/en_us/about/google-ai-plans/: Gemini app, AI Studio and Antigravity on Pro and Ultra.
- https://antigravity.google/docs/models: Antigravity availability by plan, 512K context, thinking levels.
- https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/: official positioning, cache discount wording, app and Antigravity rollout (2026-11-18).
- https://cloud.google.com/model-garden/pricing: Vertex / Agent Platform Standard Global $3.00 / $15.00, non-global $3.30 / $16.50, cache read $0.15.
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-neon: model id `gemini-4-neon`, locations `global`, `us`, `eu`, GA date, enterprise-availability note.

All accessed 2026-11-19.

## Verification result

New entry. Objective fields confirmed on Google's own pages, except
`languages` (not published, so the curated set is used) and `json_mode`
(not itemized). The quality ratings are the bot's judgment and are
flagged for owner review.
