# Claude Sonnet 5

Dataset entry: [`dataset/models/claude-sonnet-5.yaml`](../../dataset/models/claude-sonnet-5.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## ⚠ Pricing changes in 3 weeks

The dataset's `cost` values are Anthropic's **introductory pricing**,
valid only **through August 31, 2026**. Standard pricing of $3 / $15
per million input/output tokens takes effect **September 1, 2026** —
confirmed directly on Anthropic's own pricing page, not a guess. This
was already flagged as a comment in the YAML file itself, but it's
worth restating here loudly: this is not a hypothetical future drift,
it's a known, dated, already-scheduled one. Whoever picks up this
project next should update the dataset entry on or shortly after
2026-09-01.

## Identity

| Field      | Value            |
|------------|-------------------|
| `id`       | `claude-sonnet-5` |
| `name`     | Claude Sonnet 5   |
| `provider` | Anthropic         |
| `version`  | `5`               |
| `license`  | `proprietary`     |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Confirmed — all current Claude models support text and image input. |
| `audio`                | false | Not listed as a supported input/output modality. |
| `image_generation`     | false | Not listed as a supported capability. |
| `tool_calling`         | true  | Confirmed via Anthropic's tool-use pricing tables, which list Claude Sonnet 5 explicitly. |
| `structured_output`    | true  | Not independently reconfirmed this pass — no explicit citation found; inherited from original curation. |
| `json_mode`            | true  | Same as above — not independently reconfirmed this pass, inherited. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Anthropic's own comparison table describes Sonnet 5 as "the best combination of speed and intelligence" among current models, with adaptive thinking enabled; positioned just below the top-tier Fable/Opus line. |
| `coding`                   | `very_high` | Consistent with Anthropic's general positioning of the Claude line for coding/agentic work; not benchmark-derived, per `SCHEMA.md`. |
| `creative_writing`         | `high`      | Editorial judgment — strong but not rated `very_high` to leave room above it for models specifically positioned on long-form/creative strength. |
| `instruction_following`    | `very_high` | Consistent with Claude's general reputation and Anthropic's own positioning for reliable agentic use. |

## Languages

Not independently reconfirmed this pass — Anthropic does not publish
an explicit per-model language list with per-language quality ratings.
`languages` and `language_quality` in the dataset entry are curated,
same known gap as the other providers (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 128,000    |

Confirmed directly against Anthropic's current models comparison
table.

## Cost `[Objective]`

| Field                    | Value (through 2026-08-31) | Value (from 2026-09-01) |
|----------------------------|------------------------------|----------------------------|
| `input_per_million`         | $2.00                        | $3.00                       |
| `output_per_million`        | $10.00                       | $15.00                      |

Confirmed directly against Anthropic's pricing page. The dataset
currently holds the introductory-pricing values — see the warning at
the top of this document.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Claude API, Bedrock, Google Cloud, Microsoft Foundry — broad first- and third-party availability. |
| `maturity`              | `stable` | Generally available, not a limited/invitation-only release (unlike e.g. Claude Mythos). |

---

## Access

Standard Claude API, plus Amazon Bedrock, Google Cloud Vertex AI, and
Microsoft Foundry, at (or close to) the pricing in `cost.*` above —
cloud-platform pricing can differ slightly, see Anthropic's pricing
page. Consumer-subscription access (Claude Pro/Max) is a separate
question this section deliberately doesn't answer — see
`docs/models/README.md`.

## Sources

- [Claude API pricing](https://platform.claude.com/docs/en/docs/about-claude/pricing) — cost fields, introductory pricing expiration date.
- [Claude models overview](https://platform.claude.com/docs/en/docs/about-claude/models/overview) — context window, max output, capabilities, positioning.

Both accessed 2026-08-07, official Anthropic documentation only. Note:
`docs.anthropic.com/*` now 301-redirects to `platform.claude.com/docs/*`
— same publisher, new host.

## Verification result

No drift found in objective fields that are currently in effect
(introductory pricing, context window, max output). One drift is
already scheduled and known: pricing changes 2026-09-01 (see warning
above). `structured_output` and `json_mode` are flagged as not
independently reconfirmed this pass.
