# Claude Opus 4.5

Dataset entry: [`dataset/models/claude-opus-4-5.yaml`](../../dataset/models/claude-opus-4-5.yaml)
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
| `id`       | `claude-opus-4-5`              |
| `name`     | Claude Opus 4.5                |
| `provider` | Anthropic                       |
| `version`  | `4.5`                           |
| `license`  | `proprietary`                   |

Dated pinned snapshot: `claude-opus-4-5-20251101`.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Same confirmation depth as every other legacy Claude entry — consistent with the family, not independently reconfirmed per-model on the Legacy table. |
| `audio`                | false | Not listed as supported — no audio content-block type in Anthropic's documented API. |
| `image_generation`     | false | Anthropic's own vision FAQ, verbatim: "No, Claude is an image understanding model only... it cannot generate, produce, edit, manipulate, or create images." Applies to all Claude models. |
| `tool_calling`         | true  | Confirmed via Anthropic's tool-use pricing table, which explicitly lists Claude Opus 4.5 with its own system-prompt token overhead row (496/588 tokens). |
| `structured_output`    | true  | Confirmed directly — `claude-opus-4-5-20251101` is explicitly named in the structured-outputs "Compatibility" list at `platform.claude.com/docs/en/build-with-claude/structured-outputs`, checked specifically for this entry. |
| `json_mode`            | true  | Same basis as `structured_output`. |

## Quality `[Editorial]`

| Field                    | Value  | Why |
|---------------------------|--------|-----|
| `reasoning`                | `medium` | The only sourced, dimension-relevant signal found: Opus 4.5 lacks adaptive thinking entirely ("No"), a capability Opus 4.6 has ("Yes"). Anthropic's "Legacy models" table shows **no** knowledge-cutoff gap between them (both May 2025 reliable / Aug 2025 training, identical) — unlike Sonnet 4.5 vs. 4.6, which has a real 7-month cutoff gap on top of the same thinking-mode difference. Adaptive thinking is a reasoning/compute capability, mapping most directly to this dimension. |
| `coding`                   | `high`   | **Not degraded below Opus 4.6.** No sourced signal (cutoff or otherwise) distinguishes coding capability between 4.5 and 4.6 specifically — per `SCHEMA.md`'s evidence-based calibration principle, a single reasoning-scoped signal (missing adaptive thinking) doesn't automatically extend to every dimension. |
| `creative_writing`         | `high`   | Same reasoning — no signal targets this dimension; kept at Opus 4.6's value. |
| `instruction_following`    | `high`   | Same reasoning — no signal targets this dimension; kept at Opus 4.6's value. |

This is a deliberately asymmetric calibration relative to Sonnet 4.5
(degraded on reasoning/coding/instruction_following, unchanged on
creative_writing) — the two candidates carry different evidence.
Sonnet 4.5 has two signals (cutoff gap + missing adaptive thinking)
covering the reasoning-adjacent dimensions; Opus 4.5 has only one
(missing adaptive thinking, no cutoff gap), scoped here to the single
dimension it most directly bears on. Mechanically copying Sonnet 4.5's
pattern onto Opus 4.5 was considered and rejected during this
session's review specifically because the evidence didn't support it.

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `claude-opus-4-6`/`claude-opus-5` (same provider, same known gap,
see [IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 200,000    |
| `max_output`           | 64,000     |

Confirmed directly against Anthropic's "Legacy models" table —
noticeably smaller than Opus 4.6/4.7/4.8's 1M/128K. This is the real,
sourced operational difference between Opus 4.5 and its siblings; per
`SCHEMA.md`, it lives in `operational.*`, not as justification for a
`quality.*` degradation.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $5.00  |
| `output_per_million`        | $25.00 |

Confirmed directly against the same table — identical to Opus
4.6/4.7/4.8/5's pricing despite the smaller context window and older
design.

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
official promotional-credit terms describe only one-time,
subscription-tied promotional/referral credit (not API/Console,
expiring, forfeited on downgrade/cancellation) — not a continuous free
path, and not scoped to this model specifically. Same pattern as every
Claude entry in this catalog.

## Sources

- [Claude models overview, "Legacy models" section](https://platform.claude.com/docs/en/about-claude/models/overview) — pricing, context window, max output, knowledge cutoffs, thinking-mode status.
- [Claude API tool use pricing](https://platform.claude.com/docs/en/build-with-claude/tool-use/overview) — explicit per-model tool-use token overhead confirmation.
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) — explicit model-compatibility confirmation for `claude-opus-4-5-20251101`.
- [Vision](https://platform.claude.com/docs/en/build-with-claude/vision) — image-generation FAQ.
- [Promotion & credit terms](https://www.anthropic.com/legal/promotion-credit-terms) — free-access confirmation.

Accessed 2026-08-10, official Anthropic documentation only.

## Verification result

New dataset entry. Objective fields confirmed, including an explicit
structured-outputs compatibility-list check specific to this model
(closed during this session — the first sourcing pass had left it
PENDING). Quality calibration scoped to the single sourced signal
found (missing adaptive thinking → `reasoning` only), reviewed against
the stronger two-signal case for Sonnet 4.5 to confirm the asymmetry is
evidence-driven, not an oversight.
