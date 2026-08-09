# Claude Opus 4.6

Dataset entry: [`dataset/models/claude-opus-4-6.yaml`](../../dataset/models/claude-opus-4-6.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't), and
`claude-opus-4-8.md` for why this and its sibling legacy Claude
entries were added.

---

## Identity

| Field      | Value              |
|------------|---------------------|
| `id`       | `claude-opus-4-6`   |
| `name`     | Claude Opus 4.6     |
| `provider` | Anthropic            |
| `version`  | `4.6`                |
| `license`  | `proprietary`        |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Consistent with every current-generation Claude model. |
| `audio`                | false | Not listed as supported. |
| `image_generation`     | false | Not listed as supported. |
| `tool_calling`         | true  | Confirmed via Anthropic's tool-use pricing table, which lists Claude Opus 4.6 explicitly. |
| `structured_output`    | true  | Not independently reconfirmed this pass — inherited, same gap as every Claude entry. |
| `json_mode`            | true  | Same as above — inherited. |

## Quality `[Editorial]`

| Field                    | Value  | Why |
|---------------------------|--------|-----|
| `reasoning`                | `high` | One notch below Opus 4.7/4.8: Anthropic's own table shows a meaningfully older "reliable knowledge cutoff" (May 2025 vs. Jan 2026 for 4.7/4.8) and lists extended thinking as "Yes (deprecated)" rather than the newer adaptive-thinking-only design — real, sourced signals of a bigger generational gap than between 4.7 and 4.8, not an arbitrary split. |
| `coding`                   | `high` | Same reasoning. |
| `creative_writing`         | `high` | Consistent with the rest of the Opus line except Fable 5. |
| `instruction_following`    | `high` | Same reasoning as `reasoning`. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as the rest of the Claude family (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 128,000    |

Confirmed directly against Anthropic's "Legacy models" table.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $5.00  |
| `output_per_million`        | $25.00 |

Confirmed directly against the same table — same price as Opus
4.7/4.8/5, despite being the oldest and lowest-rated of the four. The
clearest "no reason to stay here" case in the Opus line.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same availability as the rest of the Claude family. |
| `maturity`              | `stable` | Still generally available — no "legacy" value in `SCHEMA.md`'s `maturity` enum, deliberately (see `claude-opus-4-8.md`). |

---

## Access

Standard Claude API, plus Amazon Bedrock, Google Cloud Vertex AI, and
Microsoft Foundry, at (or close to) the pricing in `cost.*` above. Also
exposed inside Google Antigravity labeled "(thinking)" — see
`SCHEMA.md`'s note on why that's a parameter, not a separate model, and
`IMPLEMENTATION_NOTES.md` Iteration #6 for why Antigravity isn't a
valid pricing source.

**Free access (`access.has_free_access`):** `false`. Anthropic's own
Console docs describe only a one-time starter credit for new accounts,
not continuous free access — doesn't meet the strict bar defined in
`SCHEMA.md`'s Access section.

## Sources

- [Claude models overview, "Legacy models" section](https://platform.claude.com/docs/en/docs/about-claude/models/overview) — pricing, context window, max output, capabilities, thinking-mode status, knowledge cutoffs.

Accessed 2026-08-07, official Anthropic documentation only.

## Verification result

New dataset entry. Objective fields confirmed. `structured_output` and
`json_mode` flagged as not independently reconfirmed, same recurring
gap as every other Claude entry in this catalog.
