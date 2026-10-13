# Muse Wonder

Dataset entry: [`dataset/models/muse-wonder-1.0.yaml`](../../dataset/models/muse-wonder-1.0.yaml)
Access route: [`dataset/access_routes/meta/muse-wonder-1.0-direct-api.yaml`](../../dataset/access_routes/meta/muse-wonder-1.0-direct-api.yaml)
Last verified: 2026-10-13

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

**Status: preview.** Meta labels Muse Wonder as in preview
([Overview](https://dev.meta.ai/docs/overview),
[Models](https://dev.meta.ai/docs/models)). Released 2026-10-12
([announcement](https://research.meta.ai/blog/muse-wonder)). First Meta
entry in this catalog.

---

## Identity

| Field      | Value              | Source |
|------------|--------------------|--------|
| `id`       | `muse-wonder-1.0`  | API model id, https://dev.meta.ai/docs/overview |
| `name`     | Muse Wonder        | https://dev.meta.ai/docs/models |
| `provider` | Meta               | https://dev.meta.ai/docs/overview |
| `version`  | `1.0`              | From the API id `muse-wonder-1.0` |
| `license`  | `proprietary`      | Hosted-only on Meta Model API (Muse Glimmer is Meta's open-weight line, not this one), https://dev.meta.ai/docs/models |

## Capabilities `[Objective]`

| Field               | Value | Notes |
|---------------------|-------|-------|
| `vision`            | true  | Input: text, image, video, audio, PDF — https://dev.meta.ai/docs/models |
| `audio`             | true  | Audio **input** (understanding); output is text only — same convention as `gemini-3.1-pro-preview`. |
| `image_generation`  | false | Output is text only — https://dev.meta.ai/docs/models |
| `tool_calling`      | true  | Parallel and streamed tool calls — https://dev.meta.ai/docs/models |
| `structured_output` | true  | https://dev.meta.ai/docs/models |
| `json_mode`         | false | **UNCONFIRMED — conservative default.** No separate JSON-mode statement found in Meta's docs; the schema requires a boolean, so `false` is stored until confirmed. |

Also documented but not represented in the schema: search grounding,
computer use, reasoning effort levels `"minimal"`–`"max"`.

## Quality `[Editorial]`

| Field                   | Value    | Why |
|-------------------------|----------|-----|
| `reasoning`             | `high`   | **Editorial, conservative.** Meta positions it as its "most capable model" for complex software engineering and long-horizon agentic work. Only Meta's own benchmarks exist; per `SCHEMA.md` benchmarks are not a rating source, and no independent signal yet justifies `very_high`. Preview status also argues for restraint. |
| `coding`                | `high`   | Same reasoning; coding is the stated primary use case. |
| `creative_writing`      | `medium` | No provider statement about creative writing. |
| `instruction_following` | `high`   | Meta states it follows "detailed instructions closely"; kept below `very_high` for the same reason as `reasoning`. |

## Languages

**UNCONFIRMED.** Meta's docs consulted do not list officially supported
languages for Muse Wonder. The schema requires a non-empty list with a
matching `language_quality` map, so the entry stores only `[en]` with
`en: high` (editorial) — the docs and examples are in English. Spanish
and other languages are **not** claimed. Consequence: the model is
filtered out of any non-English query (e.g. `language="es"`) until
languages are confirmed.

## Operational `[Objective]`

| Field            | Value     | Source |
|------------------|-----------|--------|
| `context_window` | 1,048,576 | https://dev.meta.ai/docs/models |
| `max_output`     | 8,192     | **UNCONFIRMED — conservative placeholder.** No official max-output figure found. The loader requires a positive integer, so a deliberately low value is stored; replace once Meta publishes it. |

Rate limits (prose only, not schema fields): 3,000 RPM and 4,000,000 TPM
per team — https://dev.meta.ai/docs/pricing-rate-limits

## Cost `[Objective]`

| Field                | Value  | Source |
|----------------------|--------|--------|
| `input_per_million`  | $4.00  | https://dev.meta.ai/docs/pricing-rate-limits, https://dev.meta.ai/models/muse-wonder |
| `output_per_million` | $20.00 | same |

Standard mode, no long-context premium. Cached input is $0.20/1M — not
representable in `SCHEMA.md` (same granularity gap as
`IMPLEMENTATION_NOTES.md`, Iteration #5). Reasoning tokens are billed as
output tokens — https://dev.meta.ai/docs/reasoning. Blended $24 →
derived tier `high`.

## Ecosystem `[Editorial]`

| Field              | Value          | Why |
|--------------------|----------------|-----|
| `integration_ease` | `medium`       | API is compatible with OpenAI Chat Completions/Responses and Anthropic Messages formats (base URL `https://api.meta.ai/v1`, Bearer key — https://dev.meta.ai/docs/overview), which argues for `high`; held at `medium` because it is a brand-new platform in preview with no track record yet. |
| `maturity`         | `experimental` | Preview status — https://dev.meta.ai/docs/models. |

---

## Access

One route: Meta Model API, pay-as-you-go, Standard mode only, at the
`cost.*` above. No cloud routes (Bedrock / Vertex / Azure) are
documented or added. Availability varies by country per Meta's
Geographic Use Policy; **Argentina availability is unconfirmed**, so the
route's `region_scope` is `region_dependent`.

**Muse Wonder Full** (higher-capability variant) is **not** on the API:
it is subscription-only in Muse Code (Power Usage $50/mo, Maximum Usage
$200/mo) — https://dev.meta.ai/docs/muse-code/subscriptions,
https://dev.meta.ai/docs/models. Deliberately not added as a model
entry. Setting reasoning effort `"max"` on `muse-wonder-1.0` does not
select it.

**Free access (`access.has_free_access`):** `false` — **UNCONFIRMED,
conservative default.** No free tier or trial credit was confirmed on
the pricing page.

**Known gap:** the route uses `guide_ref: meta#direct-api`, but no
`Docs/access-guides/meta.md` exists yet (outside this change's scope).

## Sources

- https://research.meta.ai/blog/muse-wonder — release date 2026-10-12.
- https://dev.meta.ai/docs/overview — API id, base URL, auth, API format compatibility, preview status.
- https://dev.meta.ai/docs/models — modalities, context window, tool calling, structured output, search grounding, computer use, preview status, Wonder vs Wonder Full availability.
- https://dev.meta.ai/docs/pricing-rate-limits — prices, rate limits.
- https://dev.meta.ai/models/muse-wonder — prices.
- https://dev.meta.ai/docs/reasoning — reasoning tokens billed as output.
- https://dev.meta.ai/docs/muse-code/subscriptions — Muse Wonder Full plans.

All accessed 2026-10-13, official Meta pages only.

## Verification result

New entry. Objective fields confirmed as above, except the UNCONFIRMED
ones: `max_output`, `json_mode`, `access.has_free_access`,
`languages`/`language_quality`, Argentina availability. Quality and
ecosystem values are editorial.
