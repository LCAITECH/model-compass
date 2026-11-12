# Gemini Decision

Dataset entry: [`dataset/models/gemini-decision-1.yaml`](../../dataset/models/gemini-decision-1.yaml)
Access routes: `dataset/access_routes/google/gemini-decision-1-direct-api.yaml` (1)
Last verified: 2026-11-12

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Proposed by the catalog bot on 2026-11-12,
the day after Google released the model. **This entry is an exception to
the catalog's text-and-code scope (`VISION.md`), made by the owner on
2026-11-12 ("Sumalo al catálogo")**: Gemini Decision reads text and media
but generates no text or code. It returns calibrated probabilities for
yes/no, choice and score questions through its own API, the Decisions
API. See `IMPLEMENTATION_NOTES.md`, Iteration #44. Every value below was
read on Google's own pages on 2026-11-12.

---

## Identity

| Field      | Value               |
|------------|---------------------|
| `id`       | `gemini-decision-1` |
| `name`     | Gemini Decision     |
| `provider` | Google              |
| `version`  | `1`                 |
| `license`  | `proprietary`       |

The name is the models page's "Gemini Decision"; the model code is
`gemini-decision-1`. The Decisions API guide also calls it "Gemini
Decision 1".

## What the model does

Model page: "a specialized multimodal model built for the Decisions API.
It evaluates typed questions over text, images, video, audio, and PDFs
in a single prefill pass and returns calibrated outcome probabilities
with zero output tokens." One request carries up to 1,000 independent
questions over shared input, each of one type:

- **Yes/no** (`noul`): a probability from 0.01 to 0.99 and a confidence.
- **Choice**: 2 to 255 options; the top option, per-option probabilities
  and a confidence.
- **Score**: 2 to 255 ordered rubric levels; the probability-weighted
  expected level, per-level probabilities and a confidence.

The Decisions API guide sends developers elsewhere for "Generated text,
summaries, or explanations", "Tool calls with arguments" and "Multi-step
reasoning" ("Use the Interactions API when you need ...").

## Capabilities `[Objective]`

Source for all rows: https://aistudio.google.com/docs/models/gemini-decision-1

| Field               | Value | Notes |
|---------------------|-------|-------|
| `vision`            | true  | "Inputs Text, Image, Video, Audio, and PDF". |
| `audio`             | true  | Audio **input**. "Audio generation Not supported". |
| `image_generation`  | false | "Image generation Not supported". |
| `tool_calling`      | false | "Function calling Not supported". |
| `structured_output` | false | "Structured outputs Not supported". |
| `json_mode`         | false | Not itemized. The model emits no text ("Text generation Not supported"), so there is no JSON mode. The typed JSON answer is the Decisions API's response format, not model output. |

Documented but not in the schema: output is "Calibrated probabilities
(yes/no, choice, and score, with 0 output tokens)". Also "Not supported":
text generation, thinking, Batch API, caching, code execution, computer
use, file search, Flex and Priority inference, Google Search and Maps
grounding, Live API, URL context. The Decisions API takes no YouTube
URLs or `gs://` URIs, and question instructions are text only.

**The schema has no way to say "this model does not generate text".**
The closest representation is the set of `false` capabilities above,
`max_output: null`, `output_per_million: 0` and the low quality ratings
below, with this note and the route's caveat.

## Quality `[Editorial]`

**The bot's judgment, 2026-11-12, for owner review.** Deliberately
conservative: the quality scale describes a model that writes answers,
and this one does not. None of these is derived from a benchmark score.

| Field                   | Value    | Why |
|-------------------------|----------|-----|
| `reasoning`             | `low`    | "Thinking Not supported", one prefill pass, and Google's own guide says to use the Interactions API for "Multi-step reasoning". It judges single, narrow questions ("Ask narrow, single-purpose questions"); it cannot work through a problem. |
| `coding`                | `low`    | It cannot write code: "Text generation Not supported", "Code execution Not supported". |
| `creative_writing`      | `low`    | It writes nothing. |
| `instruction_following` | `medium` | It does follow per-question instructions and criteria, which is its whole job, but only within the three fixed answer types. No claim on any page rates it above that. |

## Languages

Google does not state languages on the model page, the Decisions API
guide or the pricing page. The entry uses the curated Gemini language
list (Iteration #1). The `language_quality` values are the bot's
judgment and are **not** copied from the other Gemini entries: all are
`medium`, because the output is a probability in every language and no
page says how accuracy varies by language.

## Operational `[Objective]`

| Field            | Value   | Source |
|------------------|---------|--------|
| `context_window` | 262,144 | Model page: "Input token limit 262,144". The guide's limits table: "Context window 262,144 tokens across shared input and all questions". |
| `max_output`     | `null`  | Model page: "Output token limit 0 (up to 1,000 questions per request)". |

`max_output` must be a positive integer or `null` (`SCHEMA.md`), so the
published 0 cannot be stored. `null` is the closest valid value: there
is no output to limit. It does **not** mean that Google publishes no
figure here; Google publishes 0. Rate limits (rate-limits page, standard
interactive): Free 200 RPM / 50,000 TPM / 10,000 RPD; Tier 1 1,500 /
1,000,000 / 50,000; Tier 2 5,000 / 4,000,000 / unlimited; Tier 3 15,000 /
10,000,000 / unlimited.

## Cost `[Objective]`

Source: https://aistudio.google.com/docs/pricing#gemini-decision

| Field                | Value | Quote |
|----------------------|-------|-------|
| `input_per_million`  | $0.10 | "Input price (text, image, video, audio, PDF)", Paid Tier: "$0.10". |
| `output_per_million` | $0.00 | "Output price: Not applicable (0 output tokens)". |

No output token is ever produced or billed, so `0.00` states the real
cost of output; it is not a free offer. The pricing page adds: "Each
request bills shared input tokens once, regardless of question count.
Each question adds tokens for its own instructions, criteria, and
formatting". Context caching: "Not available". No introductory price,
no long-context tier.

Consequence for the engine: the blended cost is $0.10, the lowest in the
catalog, so cost-first recommendations now pick this model. See
Iteration #44.

## Ecosystem `[Editorial]`

| Field              | Value    | Why |
|--------------------|----------|-----|
| `integration_ease` | `medium` | Its own endpoint (`client.decisions.create`, REST `v1beta/decisions`), not `generateContent`, and it needs SDK 3.2 or later. "Available on the Gemini Developer API (v1beta) with Gemini Decision 1 only." No Batch API or caching. Simple to call, but not a drop-in for any other model. |
| `maturity`         | `stable` | On the public models page under "Specialized task models". The id has no `-preview` or `-exp` suffix, which Google's version-name patterns call a stable model ("Points to a specific stable model"). Released the day before this check, and its API is v1beta; the owner may prefer `experimental`. |

## Lifecycle

`status: active`, `release_date: "2026-11-11"` (release notes, November
11, 2026: "Released Gemini Decision (`gemini-decision-1`) and the
Decisions API"). Deprecations page, "Gemini Decision models": "gemini-decision-1
| November 11, 2026 | No shutdown date announced". `shutdown_date` and
`replacement` are `null`.

---

## Access

One route:

- **Gemini API** (`-direct-api`), through the Decisions API only. The
  paid tier needs a billing-linked project. The pricing page's Free Tier
  column says input is "Free of charge" and the rate-limits page gives
  the Free tier 200 RPM, 50,000 TPM and 10,000 RPD, so
  **`access.has_free_access` is `true`, through the free API tier**. On
  the free tier, content is "Used to improve our products"; on the paid
  tier it is not.

The release notes link three sample apps in Google AI Studio
(Decisions Playground and two others). No plan page names this model,
so there is no subscription route. Vertex AI / Gemini Enterprise Agent
Platform: the guide says the API is "Available on the Gemini Developer
API (v1beta) ... only", so there is no cloud route.

## Sources

- https://aistudio.google.com/docs/models/gemini-decision-1: id, modalities, token limits, capabilities.
- https://aistudio.google.com/docs/decisions-api: question types, limits, limitations, SDK requirement, when not to use it.
- https://aistudio.google.com/docs/models: name, listing under "Specialized task models", version-name patterns.
- https://aistudio.google.com/docs/pricing#gemini-decision: prices, free tier.
- https://aistudio.google.com/docs/rate-limits#gemini-decision: rate limits by tier.
- https://aistudio.google.com/docs/deprecations: release date, no shutdown date.
- https://aistudio.google.com/docs/changelog: released 2026-11-11.

All accessed 2026-11-12.

## Verification result

New entry, outside the usual scope on the owner's decision. Objective
fields confirmed on Google's own pages, except `languages` (not
published, so the curated list is used) and `json_mode` (not itemized).
Two values are the closest valid representation, not the published
figure: `max_output: null` for "Output token limit 0", and
`output_per_million: 0.00` for "Not applicable (0 output tokens)". The
quality, language and ecosystem ratings are the bot's judgment and are
flagged for owner review.
