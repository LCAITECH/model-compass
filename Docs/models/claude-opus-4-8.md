# Claude Opus 4.8

Dataset entry: [`dataset/models/claude-opus-4-8.yaml`](../../dataset/models/claude-opus-4-8.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Why this model — Anthropic says it directly

Second entry in this catalog's "previous generation, still in
production" line, after `gpt-4o`. This one has a stronger source than
that PoC did: Anthropic's own models page lists Opus 4.8 (and 4.7,
4.6, and Sonnet 4.6 — see their own files) under a section titled
**"Legacy models"**, with the sentence: *"The following models are
still available. Consider migrating to current models for improved
performance."* No inference needed here — the provider itself uses
the word "legacy" and recommends migration, in an official doc. That's
a stronger signal than GPT-4o's entry, where OpenAI's own copy still
called it "recommended... for most general tasks."

## Identity

| Field      | Value              |
|------------|---------------------|
| `id`       | `claude-opus-4-8`   |
| `name`     | Claude Opus 4.8     |
| `provider` | Anthropic            |
| `version`  | `4.8`                |
| `license`  | `proprietary`        |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Consistent with every current-generation Claude model; not restated per-model on Anthropic's legacy table but not contradicted either. |
| `audio`                | false | Not listed as supported for any Claude model in this catalog. |
| `image_generation`     | false | Not listed as supported. |
| `tool_calling`         | true  | Confirmed via Anthropic's tool-use pricing table, which lists Claude Opus 4.8 explicitly. |
| `structured_output`    | true  | Not independently reconfirmed this pass — same gap as every other Claude entry in this catalog. Inherited. |
| `json_mode`            | true  | Same as above — inherited. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Same Opus-tier positioning as Opus 5 — this is the immediately-prior Opus release, not a materially weaker model, just superseded. Anthropic's own "reliable knowledge cutoff" for 4.8 is Jan 2026, close to Opus 5's May 2026. |
| `coding`                   | `very_high` | Same reasoning. |
| `creative_writing`         | `high`      | Kept consistent with Opus 5's rating on this dimension, not with Fable 5's (the one model in this dataset rated `very_high` here — see `claude-fable-5.md`). |
| `instruction_following`    | `very_high` | Same reasoning. |

**On why this still counts as "legacy" despite near-identical
ratings**: the quality scale is coarse by design (see
`gpt-4o.md`/`claude-opus-5.md` for the same point). What actually
signals "migrate" here isn't a lower quality score — it's Anthropic's
own explicit "legacy... consider migrating" language, plus this model
having **identical pricing to Opus 5** ($5/$25 both) while Opus 5 is
the actively maintained, currently-recommended option. Same price,
provider-recommended downgrade — there's no honest angle where staying
on 4.8 makes sense once 5 is available at the same cost, and the
provider says so outright.

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `claude-sonnet-5`/`claude-opus-5` (same provider, same known gap,
see [IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 128,000    |

Confirmed directly against Anthropic's "Legacy models" comparison
table — identical to Opus 5's operational limits.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $5.00  |
| `output_per_million`        | $25.00 |

Confirmed directly against the same table. Identical to Opus 5's
current pricing — see the note above on why that matters for the
"legacy" story.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same Claude API/Bedrock/Google Cloud/Microsoft Foundry availability as every other Claude entry. |
| `maturity`              | `stable` | Still generally available — `SCHEMA.md`'s `maturity` enum (`experimental`/`stable`/`mature`) has no "legacy" option, deliberately not added for this (see `IMPLEMENTATION_NOTES.md` and the `gpt-4o` PoC — the "consider migrating" signal comes from cost/quality comparison, not a status flag). |

---

## Access

Standard Claude API, plus Amazon Bedrock, Google Cloud Vertex AI, and
Microsoft Foundry, at (or close to) the pricing in `cost.*` above —
same access surface as Opus 5, unsurprisingly, since it's the model
being recommended as the migration target.

**Free access (`access.has_free_access`):** `false`. Anthropic's own
Console docs describe only a one-time starter credit for new accounts,
not continuous free access — doesn't meet the strict bar defined in
`SCHEMA.md`'s Access section.

## Sources

- [Claude models overview, "Legacy models" section](https://platform.claude.com/docs/en/docs/about-claude/models/overview) — pricing, context window, max output, capabilities, explicit "consider migrating" language.

Accessed 2026-08-07, official Anthropic documentation only — same page
already used for every other Claude entry in this catalog.

## Verification result

New dataset entry. Objective fields confirmed, including the
provider's own explicit legacy/migration language — the cleanest
possible confirmation of this model's status. `structured_output` and
`json_mode` flagged as not independently reconfirmed, same recurring
gap as every other Claude entry.
