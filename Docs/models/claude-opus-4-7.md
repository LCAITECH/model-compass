# Claude Opus 4.7

Dataset entry: [`dataset/models/claude-opus-4-7.yaml`](../../dataset/models/claude-opus-4-7.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't), the
sourcing rule it follows, and `claude-opus-4-8.md` for why this and
its sibling legacy Claude entries were added — Anthropic's own docs
label them "Legacy models" and say "consider migrating," so this
catalog treats that as the strongest possible source for the
"previous generation" story, stronger than the `gpt-4o` PoC that
started it.

---

## Identity

| Field      | Value              |
|------------|---------------------|
| `id`       | `claude-opus-4-7`   |
| `name`     | Claude Opus 4.7     |
| `provider` | Anthropic            |
| `version`  | `4.7`                |
| `license`  | `proprietary`        |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Consistent with every current-generation Claude model. |
| `audio`                | false | Not listed as supported. |
| `image_generation`     | false | Not listed as supported. |
| `tool_calling`         | true  | Confirmed via Anthropic's tool-use pricing table, which lists Claude Opus 4.7 explicitly. |
| `structured_output`    | true  | Not independently reconfirmed this pass — inherited, same gap as every Claude entry. |
| `json_mode`            | true  | Same as above — inherited. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Same Opus-tier positioning as Opus 4.8/Opus 5 — Anthropic's own table shows an identical "reliable knowledge cutoff" (Jan 2026) to Opus 4.8, suggesting these two are close siblings rather than a large generational gap. |
| `coding`                   | `very_high` | Same reasoning. |
| `creative_writing`         | `high`      | Consistent with the rest of the Opus line except Fable 5 (the dataset's one `very_high` on this dimension). |
| `instruction_following`    | `very_high` | Same reasoning. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as the rest of the Claude family (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 128,000    |

Confirmed directly against Anthropic's "Legacy models" table —
identical to Opus 4.8 and Opus 5.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $5.00  |
| `output_per_million`        | $25.00 |

Confirmed directly against the same table. Identical to Opus 4.8 and
current Opus 5 pricing.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same availability as the rest of the Claude family. |
| `maturity`              | `stable` | Still generally available — no "legacy" value in `SCHEMA.md`'s `maturity` enum, deliberately (see `claude-opus-4-8.md`). |

---

## Access

Standard Claude API, plus Amazon Bedrock, Google Cloud Vertex AI, and
Microsoft Foundry, at (or close to) the pricing in `cost.*` above.

**Free access (`access.has_free_access`):** `false`. Anthropic's own
Console docs describe only a one-time starter credit for new accounts,
not continuous free access — doesn't meet the strict bar defined in
`SCHEMA.md`'s Access section.

## Sources

- [Claude models overview, "Legacy models" section](https://platform.claude.com/docs/en/docs/about-claude/models/overview) — pricing, context window, max output, capabilities.

Accessed 2026-08-07, official Anthropic documentation only.

## Verification result

New dataset entry. Objective fields confirmed. `structured_output` and
`json_mode` flagged as not independently reconfirmed, same recurring
gap as every other Claude entry in this catalog.
