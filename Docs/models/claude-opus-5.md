# Claude Opus 5

Dataset entry: [`dataset/models/claude-opus-5.yaml`](../../dataset/models/claude-opus-5.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Identity

| Field      | Value            |
|------------|-------------------|
| `id`       | `claude-opus-5`   |
| `name`     | Claude Opus 5     |
| `provider` | Anthropic         |
| `version`  | `5`               |
| `license`  | `proprietary`     |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Confirmed — all current Claude models support text and image input. |
| `audio`                | false | Not listed as a supported modality. |
| `image_generation`     | false | Not listed as a supported capability. |
| `tool_calling`         | true  | Confirmed via Anthropic's tool-use pricing tables, which list Claude Opus 5 explicitly. |
| `structured_output`    | true  | Not independently reconfirmed this pass — inherited from the same gap noted on `claude-sonnet-5.md`. |
| `json_mode`            | true  | Same as above — not independently reconfirmed, inherited. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Anthropic positions Opus 5 for "complex agentic coding and enterprise work" — its top generally-available model below the invitation-only Fable/Mythos tier. |
| `coding`                   | `very_high` | Same positioning. |
| `creative_writing`         | `high`      | Editorial judgment, consistent with `claude-sonnet-5`'s rating — the discrete scale doesn't have room to separate Opus from Sonnet here without inventing precision the project doesn't have. |
| `instruction_following`    | `very_high` | Consistent with enterprise/agentic positioning. |

**Note on Opus vs. Sonnet:** Opus 5 and Sonnet 5 end up with identical
`quality.*` ratings in this dataset. That's a real limit of a
four-level scale (`low/medium/high/very_high`), not an oversight — both
are genuinely flagship-tier models, and the meaningful difference
between them (cost, latency, depth on the hardest tasks) already shows
up in `cost` and in Anthropic's own "moderate" vs. "fast" latency
framing, not in a quality dimension this schema tracks. When two
qualifying models tie on every dimension relevant to a given priority,
the Evaluator's dataset-load order (alphabetical by `id`) breaks the
tie — for reasoning-priority queries, that means Claude Opus 5 now
wins over Claude Sonnet 5. This is expected, deterministic behavior,
not a bug — see `tests/test_evaluator.py` for where this is asserted
explicitly.

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `claude-sonnet-5` (same provider, same known gap, see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 128,000    |

Confirmed directly against Anthropic's current models comparison
table.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $5.00  |
| `output_per_million`        | $25.00 |

Confirmed directly against Anthropic's pricing page. Unlike Sonnet 5,
Opus 5 has no introductory-pricing note — this is standard, stable
pricing as of the verification date.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same first- and third-party availability as Sonnet 5 (Claude API, Bedrock, Google Cloud, Microsoft Foundry). |
| `maturity`              | `stable` | Generally available. |

---

## Access

Standard Claude API, plus Amazon Bedrock, Google Cloud Vertex AI, and
Microsoft Foundry, at (or close to) the pricing in `cost.*` above.
Consumer-subscription access is a separate question this section
deliberately doesn't answer — see `docs/models/README.md`.

## Sources

- [Claude API pricing](https://platform.claude.com/docs/en/docs/about-claude/pricing) — cost fields.
- [Claude models overview](https://platform.claude.com/docs/en/docs/about-claude/models/overview) — context window, max output, capabilities, positioning.

Both accessed 2026-08-07, official Anthropic documentation only —
reused from the same pass that verified `claude-sonnet-5.md`, since
both models are documented on the same pages.

## Verification result

New dataset entry, not a re-verification. Objective fields confirmed.
`structured_output` and `json_mode` flagged as not independently
reconfirmed, same gap as Sonnet 5.
