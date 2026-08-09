# Claude Sonnet 4.6

Dataset entry: [`dataset/models/claude-sonnet-4-6.yaml`](../../dataset/models/claude-sonnet-4-6.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't), and
`claude-opus-4-8.md` for why this and its sibling legacy Claude
entries were added.

---

## Identity

| Field      | Value                |
|------------|------------------------|
| `id`       | `claude-sonnet-4-6`   |
| `name`     | Claude Sonnet 4.6     |
| `provider` | Anthropic              |
| `version`  | `4.6`                  |
| `license`  | `proprietary`          |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Consistent with every current-generation Claude model. |
| `audio`                | false | Not listed as supported. |
| `image_generation`     | false | Not listed as supported. |
| `tool_calling`         | true  | Confirmed via Anthropic's tool-use pricing table, which lists Claude Sonnet 4.6 explicitly. |
| `structured_output`    | true  | Not independently reconfirmed this pass — inherited, same gap as every Claude entry. |
| `json_mode`            | true  | Same as above — inherited. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `high`   | Previous Sonnet generation — positioned below Sonnet 5's `very_high`, consistent with Anthropic's own "legacy, consider migrating" framing for this model. |
| `coding`                   | `high`   | Same reasoning. |
| `creative_writing`         | `medium` | Consistent with Sonnet 5's rating one tier down, same conservative default used across this catalog for Sonnet-class models. |
| `instruction_following`    | `high`   | Same reasoning as `reasoning`. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as the rest of the Claude family (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 128,000    |

Confirmed directly against Anthropic's "Legacy models" table. Worth
noting: this matches Sonnet 5's 1M-token window exactly, unlike Sonnet
4.5 (the generation before this one), which was capped at 200k — the
context-window jump happened at 4.6, not at 5.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $3.00  |
| `output_per_million`        | $15.00 |

Confirmed directly against the same table — identical to Sonnet 5's
**standard** (post-2026-08-31) pricing, though currently *more*
expensive than Sonnet 5's active introductory rate ($2/$10 through
2026-08-31). Worth re-checking after that date: once Sonnet 5 reverts
to standard pricing, Sonnet 4.6 will cost exactly the same as the
newer, better-rated model, making the "no reason to stay" case even
clearer than it already is.

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

- [Claude models overview, "Legacy models" section](https://platform.claude.com/docs/en/docs/about-claude/models/overview) — pricing, context window, max output, capabilities.

Accessed 2026-08-07, official Anthropic documentation only.

## Verification result

New dataset entry. Objective fields confirmed. `structured_output` and
`json_mode` flagged as not independently reconfirmed, same recurring
gap as every other Claude entry in this catalog.
