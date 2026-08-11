# Claude Sonnet 4.5

Dataset entry: [`dataset/models/claude-sonnet-4-5.yaml`](../../dataset/models/claude-sonnet-4-5.yaml)
Last verified: 2026-08-10

See [README.md](README.md) for what this document is (and isn't), and
`claude-opus-4-8.md` for why this and its sibling legacy Claude entries
were added. Admitted from `Docs/CANDIDATE_RESEARCH_2026-08-10.md`
(branch `research/model-candidates`) — same admission pattern as the
other legacy Claude entries already in this catalog.

---

## Identity

| Field      | Value                        |
|------------|--------------------------------|
| `id`       | `claude-sonnet-4-5`            |
| `name`     | Claude Sonnet 4.5              |
| `provider` | Anthropic                       |
| `version`  | `4.5`                           |
| `license`  | `proprietary`                   |

Dated pinned snapshot: `claude-sonnet-4-5-20250929`. Per Anthropic's
own note, dateless aliases before the 4.6 generation are convenience
pointers that resolve to this dated ID.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Confirmed indirectly — Anthropic's vision docs classify all Claude models into a "High-resolution: Claude 4.7 and later" vs. "Standard: All other models" image-token table, placing Sonnet 4.5 in the Standard tier, implying support. Same confirmation depth as `claude-sonnet-4-6`'s ("consistent with every current-generation Claude model"), not independently stronger or weaker. |
| `audio`                | false | Not listed as supported — no audio content-block type in Anthropic's documented API. Same "not listed" convention already used for `claude-sonnet-4-6`. |
| `image_generation`     | false | Anthropic's own vision FAQ, verbatim: "No, Claude is an image understanding model only. It can interpret and analyze images, but it cannot generate, produce, edit, manipulate, or create images." Applies to all Claude models, no exception documented. |
| `tool_calling`         | true  | Confirmed via Anthropic's tool-use pricing table, which explicitly lists Claude Sonnet 4.5 with its own system-prompt token overhead row. |
| `structured_output`    | true  | Confirmed directly — `claude-sonnet-4-5-20250929` is explicitly named in the structured-outputs "Compatibility" list at `platform.claude.com/docs/en/build-with-claude/structured-outputs`. |
| `json_mode`            | true  | Same basis as `structured_output` — Anthropic doesn't distinguish a separate "JSON mode" flag from structured outputs. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `medium` | Anthropic's own "Legacy models" table shows a real, sourced 7-month gap in reliable knowledge cutoff against Sonnet 4.6 (Jan 2025 vs. Aug 2025), and Sonnet 4.5 lacks adaptive thinking entirely ("No"), a capability Sonnet 4.6 has ("Yes") — two independent, dimension-relevant signals, same kind and strength already used to justify Opus 4.6's one-tier degradation below Opus 4.7/4.8 in this catalog. |
| `coding`                   | `medium` | Same evidence — cutoff gap and missing adaptive thinking bear directly on reasoning-adjacent capability. |
| `creative_writing`         | `medium` | **Not degraded.** Neither the cutoff gap nor the missing adaptive-thinking feature is evidence about writing style specifically — per `SCHEMA.md`'s evidence-based calibration principle, degradation is scoped to the dimension the evidence supports. Kept at Sonnet 4.6's own value, same precedent as Opus 4.6 keeping `creative_writing` unchanged relative to Opus 4.7/4.8 for the identical reason. |
| `instruction_following`    | `medium` | Same reasoning/coding evidence — cutoff and thinking-capability gaps plausibly affect reliability on complex instructions, same scoping already used for Opus 4.6. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as the rest of the Claude family (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 200,000    |
| `max_output`           | 64,000     |

Confirmed directly against Anthropic's "Legacy models" table. The
oldest entry in that table by these two metrics — Opus 4.6/4.7/4.8 and
Sonnet 4.6 are all already at 1M context / 128K output; the
context-window jump happened at the 4.6 generation, not before.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $3.00  |
| `output_per_million`        | $15.00 |

Confirmed directly against the same table, cross-confirmed against
Anthropic's dedicated pricing page — identical to Sonnet 4.6's current
pricing despite being one generation older and rated lower.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same availability as the rest of the Claude family. |
| `maturity`              | `stable` | Still generally available — no "legacy" value in `SCHEMA.md`'s `maturity` enum, deliberately (see `claude-opus-4-8.md`). |

---

## Access

Standard Claude API, plus Amazon Bedrock, Claude Platform on AWS,
Google Cloud Vertex AI, and Microsoft Foundry, at (or close to) the
pricing in `cost.*` above.

**Free access (`access.has_free_access`):** `false`. Anthropic's
pricing FAQ describes only a one-time starter credit for new accounts
("New users receive a small amount of free credits to test the API"),
not continuous free access — same pattern as every Claude entry in
this catalog.

## Sources

- [Claude models overview, "Legacy models" section](https://platform.claude.com/docs/en/about-claude/models/overview) — pricing, context window, max output, knowledge cutoffs, thinking-mode status.
- [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) — cost cross-confirmation, free-credit FAQ.
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) — explicit model-compatibility confirmation.
- [Vision](https://platform.claude.com/docs/en/build-with-claude/vision) — resolution-tier table, image-generation FAQ.

Accessed 2026-08-10, official Anthropic documentation only.

## Verification result

New dataset entry. Objective fields confirmed, including an explicit
structured-outputs compatibility-list match (stronger sourcing than
the "inherited" gap most other Claude entries in this catalog carry
for that field). Quality calibration reviewed twice this session for
evidence scope — the first pass over-degraded `creative_writing`
without a dimension-specific signal; corrected to match Sonnet 4.6's
value once the error was caught (see this session's chat log for the
full reasoning trail, not reproduced here).
