# Claude Fable 5

Dataset entry: [`dataset/models/claude-fable-5.yaml`](../../dataset/models/claude-fable-5.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Access

This is the model that motivated the user's "how do I actually get
access to this" question, so it gets documented here in full even
though there's no dedicated schema field for it (see the open
discussion in `HANDOFF.md` about whether to add one). As of this
verification date, Fable 5 access works differently depending on how
you're paying for Claude at all:

- **Claude Max / Team Premium subscribers**: Fable 5 is included as a
  permanent part of the plan, at 50% of the account's standard weekly
  usage limit.
- **Claude Pro / Team Standard subscribers**: no standing access — a
  one-time $100 usage credit is granted, and once that's used up,
  continuing to use Fable 5 means paying direct API rates.
- **Direct API access** (no consumer subscription at all): standard
  per-token pricing, same as every other model in this dataset — this
  is the number recorded in `cost.*` below, for consistency with how
  every other entry in this catalog is priced.

This access story is genuinely volatile — it changed at least three
times in the month before this verification (see the search results
behind this entry: a "June 23 billing shift," a "July 7 pricing
switch," and a "July 18" resolution to "permanent for Max, credits-only
for Pro"). That volatility is itself a reason this belongs in prose
here rather than a rigid schema field for now — a field that goes
stale every few weeks needs a different design than "one enum value
per model."

**Free access (`access.has_free_access`):** `false`. None of the three
paths above is continuous, unconditional free access — the Pro/Team
Standard credit is explicitly one-time, and Max/Team Premium requires
an existing paid subscription. Doesn't meet the strict bar defined in
`SCHEMA.md`'s Access section (the open discussion referenced above is
now resolved — this is that field).

## Identity

| Field      | Value              |
|------------|---------------------|
| `id`       | `claude-fable-5`    |
| `name`     | Claude Fable 5      |
| `provider` | Anthropic            |
| `version`  | `5`                  |
| `license`  | `proprietary`        |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Consistent with every current-generation Claude model. |
| `audio`                | false | Not listed as supported. |
| `image_generation`     | false | Not listed as supported. |
| `tool_calling`         | true  | Not found in Anthropic's tool-use pricing table specifically (unlike every other Claude entry in this catalog, which is explicitly listed there) — inferred from Fable 5's own positioning ("next-generation intelligence for long-running agents," which is meaningless without tool use). Flagged as an inference, not a direct citation, per this folder's sourcing rule. |
| `structured_output`    | true  | Not independently reconfirmed this pass — inherited, same gap as every Claude entry. |
| `json_mode`            | true  | Same as above — inherited. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Anthropic's own description: "Anthropic's most capable widely released model." The only model in this dataset explicitly described that way by its own provider. |
| `coding`                   | `very_high` | Same reasoning. |
| `creative_writing`         | `very_high` | The **only** model in this entire catalog rated `very_high` here — every other model (including Claude Opus 5) was deliberately capped at `high`, to leave room for a model that actually earns the top rating. At 2x Opus 5's price and explicitly positioned above it, Fable 5 is that model. |
| `instruction_following`    | `very_high` | Same reasoning as `reasoning`. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as the rest of the Claude family (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 128,000    |

Confirmed directly against Anthropic's current models comparison
table — same ceiling as Opus 5/Sonnet 5, despite the much higher
price; the differentiation is in quality and latency, not context
size.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $10.00 |
| `output_per_million`        | $50.00 |

Confirmed directly against Anthropic's pricing page — this is the
**direct API rate**, double Opus 5's. See the Access section above for
why this number doesn't tell the whole story for a Claude subscriber.
Anthropic's own latency framing for Fable 5 is "Slower" (vs. Opus 5's
"Moderate"), consistent with it being the deepest, most expensive
tier.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Standard Claude API/Bedrock/Google Cloud/Microsoft Foundry access, same surface as the rest of the family — the *access model* is unusually complex (see above), but the *integration* itself isn't. |
| `maturity`              | `stable` | Generally available since 2026-06-09, not a limited/invitation-only release (unlike its sibling Claude Mythos 5, deliberately not added to this dataset — invitation-only with no self-serve access at all, which fails this catalog's admission criteria even harder than the Fable 5 access story does). |

---

## Sources

- [Claude models overview](https://platform.claude.com/docs/en/docs/about-claude/models/overview) — identity, capabilities, context window, max output, positioning, GA date.
- [Claude API pricing](https://platform.claude.com/docs/en/docs/about-claude/pricing) — direct API cost fields.
- Web search results (TechTimes, PCWorld, MindStudio, and others, all dated June-July 2026) — the subscription/credits access story. **Not treated as sourcing for any `[Objective]` schema field** — used only for the prose Access section above, which isn't part of the YAML the Decision Engine reads. If this ever becomes a real schema field, it needs a direct Anthropic source, not aggregated news coverage.

Accessed 2026-08-07.

## Verification result

New dataset entry. Objective fields (identity, context, max output,
API pricing) confirmed against official Anthropic documentation.
`tool_calling` is an inference, flagged as such. `structured_output`
and `json_mode` flagged as not independently reconfirmed. The access
story is documented in full but deliberately kept out of the schema
for now — see the Access section above and `HANDOFF.md` for the open
design question.
