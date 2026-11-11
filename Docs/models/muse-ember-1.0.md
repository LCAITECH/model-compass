# Muse Ember

Dataset entry: [`dataset/models/muse-ember-1.0.yaml`](../../dataset/models/muse-ember-1.0.yaml)
Access route: [`dataset/access_routes/meta/muse-ember-1.0-direct-api.yaml`](../../dataset/access_routes/meta/muse-ember-1.0-direct-api.yaml)
Last verified: 2026-11-10

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Proposed by the catalog bot on 2026-11-10
after its daily audit found the model on Meta's pages; the owner asked
for it to be added the same day. Every value below was read on Meta's
own pages on 2026-11-10.

---

## Fit with the Meta policy (Iteration #33)

Iteration #33 keeps three kinds of Meta model out of the dataset: the
Contributor-mode ids, the older Muse Spark 1.2 and 1.1, and Muse Wonder
Full, which is subscription-only with no API id. Muse Ember is none of
these. It is its own model line with a Standard-mode API id
(`muse-ember-1.0`), and the pricing page says "Contributor mode isn't
available for Muse Wonder or Muse Ember on Model API". It is not
open-weight, so the "Self-hosted open-weights models" item on the bot
contract's owner-work list does not apply either. The curated Meta
language list of Iteration #33 is reused.

## Identity

| Field      | Value            |
|------------|------------------|
| `id`       | `muse-ember-1.0` |
| `name`     | Muse Ember       |
| `provider` | Meta             |
| `version`  | `1.0`            |
| `license`  | `proprietary`    |

Served only through Meta Model API and Muse Code; no weights are
published.

## Capabilities `[Objective]`

| Field               | Value | Notes |
|---------------------|-------|-------|
| `vision`            | true  | Muse Ember page: "Input Text, image, video, audio, and PDF"; "image understanding". |
| `audio`             | true  | Same input row. Meta's launch post: "Muse Ember supports text, image, audio and video inputs". No caveat like Muse Spark 1.3's "not fully supported" was found. |
| `image_generation`  | false | "Output Text". |
| `tool_calling`      | true  | "It works with computer use, image understanding, tool calling, structured output, and search grounding." |
| `structured_output` | true  | Same sentence. |
| `json_mode`         | true  | Meta documents JSON Schema structured output only, the same basis as the other Muse entries. |

**Correction to the bot's own audit note.** The audit summary of
2026-11-10 called Muse Ember "text only". Meta's pages say it takes
text, image, video, audio and PDF input. The entry follows Meta's
pages.

## Quality `[Editorial]`

**The bot's judgment, 2026-11-10, for owner review.** None of these is
derived from a benchmark score.

| Field                   | Value    | Why |
|-------------------------|----------|-----|
| `reasoning`             | `medium` | Meta calls it "the efficient execution model in the Muse family", "our smallest reasoning model", built for "bounded work that repeats many times", and tells developers to "pair it with Muse Spark or Muse Wonder: the larger model plans". That is a claim about efficiency, not depth. Below `muse-spark-1.3` (`high`). |
| `coding`                | `medium` | Meta names coding subtasks as a core use ("run the focused coding tasks, terminal commands, and lookups that a main agent hands out"), but also says "For hard single-shot coding problems, knowledge-heavy questions, or visual coding, use Muse Spark or Muse Wonder." A bounded-coding claim with the provider's own limit on it, so it does not reach the `high` that an unqualified coding claim gets (as for `qwen3.7-flash`). |
| `creative_writing`      | `medium` | No claim. The conservative middle tier used across the dataset. |
| `instruction_following` | `medium` | No claim specific to this dimension. |

## Languages

Meta publishes no supported-language list. Curated as in Iteration #33:
English `very_high`; Spanish, Portuguese, French, German and Italian
`high`.

## Operational `[Objective]`

| Field            | Value     | Source |
|------------------|-----------|--------|
| `context_window` | 1,048,576 | Muse Ember page: "Context window 1,048,576 tokens". |
| `max_output`     | 524,288   | Muse Ember page: "Max output 524,288 tokens". The research post agrees: "up to 512K output tokens". |

Reasoning effort goes from "minimal" to "max", and the default is "max".
Rate limits (pricing page, per team): 3,000 RPM, 4,000,000 TPM, its own
bucket.

## Cost `[Objective]`

| Field                | Value |
|----------------------|-------|
| `input_per_million`  | $0.10 |
| `output_per_million` | $0.50 |

Pricing page, Standard mode only. There are two tiers set by the
request's input tokens, cached tokens included:

| Usage        | Up to 200K input tokens | Over 200K input tokens |
|--------------|-------------------------|------------------------|
| Cached input | $0.004                  | $0.012                 |
| Input        | $0.10                   | $0.30                  |
| Output       | $0.50                   | $1.50                  |

"A request with more is billed at the long-context rates in full, not
only for the tokens past 200K." A request that continues a stored
conversation (`previous_response_id`) counts that history as input. The
entry stores the lower tier, the one a typical first request hits
(Iteration #24). Web search grounding costs $2.50 per 1,000 queries on
top.

## Ecosystem `[Editorial]`

| Field              | Value    | Why |
|--------------------|----------|-----|
| `integration_ease` | `high`   | Responses, Chat Completions and Messages endpoints. "Muse Ember accepts the same request body as Muse Spark, so switching most examples is a model ID change." |
| `maturity`         | `stable` | Listed on Meta's public models page and its own docs page, neither of which says preview. That is unlike Muse Wonder ("Muse Wonder is in preview"), which is `experimental`. |

## Lifecycle

`status: active`, `release_date: "2026-11-09"` (Meta AI Research post,
dated November 9, 2026: "Muse Ember is available today on the Meta
Model API"). No deprecation is published.

---

## Access

One route: the direct API on Meta Model API, `api_billing_linked`,
`region_scope: region_dependent` ("Model availability can vary by
country", models page). It is also in Muse Code "on pay-as-you-go and
with any subscription". That gives no subscription route, because the
catalog has no Muse Code plans. Meta's site also links a Google Cloud
Marketplace listing for `muse-ember-1-0`. It was not read, and the
catalog has no route type for a provider's model on another cloud's
marketplace, so there is no route for it.

**Free access (`access.has_free_access`):** `false`. There is no free
API tier and no free consumer plan that names the model.

## Sources

- [Muse Ember](https://dev.meta.ai/docs/muse-ember): id, modalities, context, max output, features, availability.
- [Models](https://dev.meta.ai/docs/models): listing, Standard mode only.
- [Pricing and rate limits](https://dev.meta.ai/docs/pricing-rate-limits): both price tiers, no Contributor mode, rate limits.
- [Muse Ember model page](https://dev.meta.ai/models/muse-ember): positioning.
- [Start building with Muse Ember](https://dev.meta.ai/resources/blog/build-with-muse-ember): launch post, multimodal input.
- [Introducing Muse Ember](https://research.meta.ai/blog/muse-ember): release date (November 9, 2026), output limit.

All accessed 2026-11-10.

## Verification result

New entry. Objective fields confirmed on Meta's documentation.
`json_mode` and the language list are curated and flagged as such. The
quality ratings are the bot's judgment and are flagged for owner review.
