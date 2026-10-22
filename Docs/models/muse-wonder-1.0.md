# Muse Wonder

Dataset entry: [`dataset/models/muse-wonder-1.0.yaml`](../../dataset/models/muse-wonder-1.0.yaml)
Last verified: 2026-10-15

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. First Meta entry in this catalog, admitted
on 2026-10-15 at the owner's request once Iteration #26 (`max_output`
may be `null`) removed the blocker that closed the bot's PR #5. Every
field below was read on Meta's own pages (see Sources).

---

## Identity

| Field      | Value             |
|------------|--------------------|
| `id`       | `muse-wonder-1.0`  |
| `name`     | Muse Wonder         |
| `provider` | Meta                |
| `version`  | `1.0`               |
| `license`  | `proprietary`       |

Served only through Meta Model API and Muse Code; no weights are
published (Meta's open-weight model is a different line, Muse Glimmer).

**Muse Wonder Full is not this entry.** Meta's higher-capability
variant is "available only in Muse Code with a subscription" (Power
Usage and Maximum Usage plans), has no API id and no per-token price,
so it cannot be a dataset entry. Setting reasoning effort to "max" on
`muse-wonder-1.0` does not select it.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Models page: "takes text, image, video, audio, and PDF input". |
| `audio`                | true  | Same sentence, and "video and audio understanding" in its feature list. Meta's launch post adds that "audio-dependent use cases require confirmation of audio support on the release surface"; the API docs, the surface this entry describes, list it. |
| `image_generation`     | false | "returns text". Image generation is a separate model (Muse Image). |
| `tool_calling`         | true  | Models page feature list: "tool calling". |
| `structured_output`    | true  | Models page feature list; the structured-output guide constrains decoding to a JSON Schema. |
| `json_mode`            | true  | Meta documents JSON Schema structured output only, no separate JSON mode: same basis as other entries where JSON mode isn't itemized. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Models page: "Meta's most capable model, built for complex software engineering and long-horizon agentic work"; it "plans, delegates to sub-agents, calls tools in parallel, and recovers from errors across many steps". Meta positions it against Claude Fable 5.1, GPT-6 Astra and Claude Opus 5.5, all `very_high` here. |
| `coding`                   | `very_high` | Same page: "makes and verifies changes across many files in real repositories". The launch post: Muse Wonder "brings comparable performance to Muse Wonder Full", which Meta says tops independent coding leaderboards. |
| `creative_writing`         | `medium`    | No creative-writing claim on any page checked. Conservative middle tier, as for `qwen3.8-max` and `deepseek-v4-pro`. |
| `instruction_following`    | `high`      | Models page: "following detailed instructions closely". A direct but general claim, one step below the `very_high` given where a provider published specific evidence (`gpt-6-astra`'s system card). |

Proposed by Claude, approved by the project owner (2026-10-15).

## Languages

Meta publishes no supported-language list for the Muse models (the
model card is a PDF download, not read this pass). Curated
conservatively, Iteration #33: English at `very_high`, and Spanish,
Portuguese, French, German and Italian at `high`. A shorter list keeps
the model out of contexts it may serve well, which is the safer error:
a developer asking for Japanese is never told Muse Wonder handles it on
a guess.

## Operational `[Objective]`

| Field              | Value       |
|----------------------|-------------|
| `context_window`      | 1,048,576   |
| `max_output`           | `null`      |

Context: "a 1,048,576-token context window" (models page). Meta
publishes no output ceiling for Muse Wonder; `null` per Iteration #26.
(For `muse-spark-1.3` Meta's agent-setup guides do give one; nothing
equivalent exists for Wonder.)

## Cost `[Objective]`

| Field                    | Value    |
|----------------------------|----------|
| `input_per_million`         | $4.00   |
| `output_per_million`        | $20.00  |

Pricing page, Standard mode. Cached input $0.20/M. "No long-context
premium". Web search grounding is $2.50 per 1,000 queries on top.
Contributor mode (cheaper, Meta trains on your content) "isn't available
for Muse Wonder on Model API".

## Ecosystem `[Editorial]`

| Field                | Value          | Why |
|------------------------|----------------|-----|
| `integration_ease`      | `high`         | Responses, Chat Completions and Anthropic Messages endpoints: "most stacks work with a base-URL and key change" (quickstart). |
| `maturity`              | `experimental` | "Muse Wonder is in preview" (models page). |

---

## Access

One route: direct API on Meta Model API, `api_billing_linked`,
`region_scope: region_dependent` ("Model availability can vary by
country", Geographic Use Policy). Rate limits are per team: 3,000 RPM,
4,000,000 TPM. Also in Muse Code, pay-as-you-go or any plan; no
subscription route, since this catalog has no Muse Code plans.

**South Korea (2026-10-22):** Meta's models page now names one country:
"Muse Wonder and Muse Wonder Full aren't currently available in South
Korea, on Model API or in Muse Code." The route's caveat says so; its
`region_scope` was already `region_dependent`, so no field changed.

**Free access (`access.has_free_access`):** `false`. No free API tier
and no free consumer plan names the model.

## Lifecycle

`active`. Released 2026-10-12 ("Today we're excited to launch Muse
Wonder on Muse Code and Meta Model API", launch post). Preview, no
deprecation or shutdown published.

## Sources

- [Models](https://dev.meta.ai/docs/models) — id, modalities, features, context window, preview status, variants.
- [Pricing and rate limits](https://dev.meta.ai/docs/pricing-rate-limits) — cost, modes, rate limits.
- [Muse Wonder model page](https://dev.meta.ai/models/muse-wonder) — positioning, Muse Wonder Full.
- [Put your ideas to work with Muse Wonder and Muse Wonder Full](https://dev.meta.ai/resources/blog/build-with-muse-wonder) — release date, audio note.
- [Structured output](https://dev.meta.ai/docs/structured-output) and [Quickstart](https://dev.meta.ai/docs/quickstart).

All accessed 2026-10-15, Meta's own pages only; the models page re-read
on 2026-10-22 for the South Korea note.

## Verification result

New entry, first Meta model in the catalog. Objective fields confirmed
on Meta's documentation; `max_output` is `null` because Meta publishes
none. `json_mode` and the language list are curated, flagged as such.
