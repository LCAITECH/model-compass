# Claude Opus 4.5

Dataset entry: [`dataset/models/claude-opus-4-5.yaml`](../../dataset/models/claude-opus-4-5.yaml)
Last verified: 2026-08-10 (objective fields); lifecycle updated 2026-11-24

See [README.md](README.md) for what this document is (and isn't), and
`claude-opus-4-8.md` for why this and its sibling legacy Claude entries
were added. Admitted from the 2026-08-10 candidate research
(internal branch `research/model-candidates`, not published) — same admission pattern as the
other legacy Claude entries already in this catalog.

---

## Lifecycle

| Field | Value |
|-------|--------|
| API model name | `claude-opus-4-5-20251101` (the dateless alias `claude-opus-4-5` is included) |
| Status | **Deprecated** |
| Deprecated | 2026-11-23 |
| Tentative retirement (Claude API) | 2027-01-22 |
| Recommended replacement | `claude-opus-5-5` (already in this catalog) |

Source: [Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) (checked 2026-11-24). Anthropic notified developers on 2026-11-23. Its page says these dates apply to Anthropic-operated platforms: the Claude API, Claude Platform on AWS, Claude Models on Google Cloud (Anthropic managed), and Microsoft Foundry. Partner-operated platforms set their own schedules.

**2026-11-24, `lifecycle` block (Iteration #47):** the YAML records `status: deprecated`, `shutdown_date: "2027-01-22"`, `replacement: claude-opus-5-5`, re-checked on Anthropic's deprecations page the same day. The Decision Engine never recommends a `deprecated` model; this one is listed among the exclusions with its date and successor. The YAML and its access routes are removed on the shutdown date (`tests/test_catalog_dates.py` fails from that day). Cloud platforms publish different dates, recorded in each route's caveat:

- **Amazon Bedrock** (partner-operated): "Legacy stage in all Regions"; public extended access starts on February 23, 2027; "upcoming end of life of May 23, 2027". Source: [Claude Opus 4.5 model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-opus-4-5.html) (checked 2026-11-24).
- **Microsoft Foundry**, version 1 (hosted on Anthropic infrastructure): Microsoft's retirement schedule lists lifecycle **GA**, retirement date **2027-02-22**, replacement `claude-opus-5-5`. This is 31 days later than the date Anthropic says also applies to Foundry. This catalog stores Microsoft's date on the Foundry route, because a cloud route comes from that cloud's own docs. Source: [Model retirement schedule - Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule) (checked 2026-11-24).
- **Google Cloud Vertex AI** (Google managed): the model page only states "Retirement Date: Not sooner than Nov 24, 2026." That is a floor, not a specific shutdown date, so none is stored for this route. The partner-models page still lists the model as available. Sources: [Claude Opus 4.5 on Google Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/opus-4-5) and [Use Claude](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) (checked 2026-11-24).

Because the schema has a single model-level `shutdown_date`, the entry uses Anthropic's Claude API date of 2027-01-22. On that day the Bedrock and Foundry routes may still be live. That is noted in Iteration #47; it is not resolved here.

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
- [Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — 2026-11-24 lifecycle: Deprecated on 2026-11-23, retires 2027-01-22, replacement `claude-opus-5-5`.
- [Amazon Bedrock model card: Claude Opus 4.5](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-opus-4-5.html) — 2026-11-24 Bedrock EOL May 23, 2027.
- [Model retirement schedule - Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule) — 2026-11-24 Foundry version 1 retires 2027-02-22.
- [Claude Opus 4.5 on Google Cloud](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/opus-4-5) — 2026-11-24, retirement "Not sooner than Nov 24, 2026" only.

Accessed 2026-08-10, official Anthropic documentation only. Lifecycle sources accessed 2026-11-24.

## Verification result

New dataset entry. Objective fields confirmed, including an explicit
structured-outputs compatibility-list check specific to this model
(closed during this session — the first sourcing pass had left it
PENDING). Quality calibration scoped to the single sourced signal
found (missing adaptive thinking → `reasoning` only), reviewed against
the stronger two-signal case for Sonnet 4.5 to confirm the asymmetry is
evidence-driven, not an oversight.
