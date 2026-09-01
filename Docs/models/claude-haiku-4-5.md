# Claude Haiku 4.5

Dataset entry: [`dataset/models/claude-haiku-4-5.yaml`](../../dataset/models/claude-haiku-4-5.yaml)
Last verified: 2026-08-07 (see also the 2026-08-27 retirement-lifecycle
note below — no dataset field changed, `SCHEMA.md` has no lifecycle
field)

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Identity

| Field      | Value               |
|------------|----------------------|
| `id`       | `claude-haiku-4-5`   |
| `name`     | Claude Haiku 4.5     |
| `provider` | Anthropic             |
| `version`  | `4.5`                 |
| `license`  | `proprietary`         |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Confirmed — all current Claude models support text and image input. |
| `audio`                | false | Not listed as a supported modality. |
| `image_generation`     | false | Not listed as a supported capability. |
| `tool_calling`         | true  | Confirmed via Anthropic's tool-use pricing tables, which list Claude Haiku 4.5 explicitly. |
| `structured_output`    | true  | Not independently reconfirmed this pass — same gap as the other Claude entries. Inherited. |
| `json_mode`            | true  | Same as above — inherited. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `high`   | Anthropic's own positioning: "the fastest model with near-frontier intelligence" — notably, Haiku 4.5 is the only current-generation Claude model with **extended thinking** support (the others use always-on adaptive thinking instead), which is real signal of deliberate reasoning capability, not just speed. Kept at `high` rather than `very_high` since it's still the cheapest, fastest tier by design. |
| `coding`                   | `high`   | Same reasoning as above. |
| `creative_writing`         | `medium` | No strong signal either way; conservative default. |
| `instruction_following`    | `high`   | Consistent with Anthropic's general reputation and the model's positioning for fast, reliable agentic use. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `claude-sonnet-5`/`claude-opus-5` (same provider, same known gap,
see [IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 200,000    |
| `max_output`           | 64,000     |

Confirmed directly against Anthropic's current models comparison
table — notably smaller than Sonnet 5/Opus 5's 1M-token window, the
one clear objective trade-off for the price.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $1.00  |
| `output_per_million`        | $5.00  |

Confirmed directly against Anthropic's pricing page. No
introductory-pricing note, unlike Sonnet 5 — this is standard, stable
pricing as of the verification date.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same first- and third-party availability as Sonnet 5/Opus 5. |
| `maturity`              | `stable` | Generally available. |

---

## Access

Standard Claude API, plus Amazon Bedrock, Google Cloud Vertex AI, and
Microsoft Foundry, at (or close to) the pricing in `cost.*` above.
Consumer-subscription access is a separate question this section
deliberately doesn't answer — see `docs/models/README.md`.

**Free access (`access.has_free_access`):** `false`. Anthropic's own
Console docs describe only a one-time starter credit for new accounts,
not continuous free access — doesn't meet the strict bar defined in
`SCHEMA.md`'s Access section.

## Lifecycle (informational — not a schema field)

`claude-haiku-4-5-20251001` is listed `Active` on Anthropic's model
deprecations page, with a tentative retirement date of "Not sooner
than October 15, 2026" — confirmed directly, 2026-08-27, against
`platform.claude.com/docs/en/about-claude/model-deprecations`. No
deprecation has been announced. `SCHEMA.md` has no lifecycle/retirement
field, so this is recorded here in prose only, same convention as
every other fact that doesn't map to a schema field.

## Sources

- [Claude models overview](https://platform.claude.com/docs/en/docs/about-claude/models/overview) — pricing, context window, max output, capabilities, thinking-mode positioning, knowledge cutoff (reliable: Feb 2025; training: Jul 2025).
- [Claude model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — lifecycle status and tentative retirement date (accessed 2026-08-27).

Accessed 2026-08-07, official Anthropic documentation only — same page
already used for `claude-sonnet-5.md`/`claude-opus-5.md`, since all
current Claude models are documented on one comparison table.

## Verification result

New dataset entry. Objective fields confirmed. `structured_output` and
`json_mode` flagged as not independently reconfirmed, same gap as the
other Claude entries in this catalog.

**2026-08-27 re-audit (lifecycle only):** confirmed `Active`, no
retirement scheduled before October 15, 2026 at the earliest. No
dataset field affected.
