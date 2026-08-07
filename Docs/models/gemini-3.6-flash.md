# Gemini 3.6 Flash

Dataset entry: [`dataset/models/gemini-3.6-flash.yaml`](../../dataset/models/gemini-3.6-flash.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Naming note

The user's initial ask mentioned "Gemini 3.1 Pro" and "Gemini 3.5
Flash" specifically. Neither matched anything findable in official
Google documentation as of this pass: no "3.1 Pro" exists, and "3.5
Pro" was teased but is delayed (reported internally behind on
performance goals, not yet released). What *is* real and current:
**Gemini 3.6 Flash** (this entry) and **Gemini 3.5 Flash-Lite** (see
its own file). Confirmed with the user before researching either.

## Identity

| Field      | Value               |
|------------|----------------------|
| `id`       | `gemini-3.6-flash`   |
| `name`     | Gemini 3.6 Flash     |
| `provider` | Google                |
| `version`  | `3.6`                 |
| `license`  | `proprietary`         |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Input modalities: text, image, video, audio, PDF. |
| `audio`                | true  | Audio input confirmed; output is text-only. |
| `image_generation`     | false | Output modality is text-only. |
| `tool_calling`         | true  | Confirmed. |
| `structured_output`    | true  | Confirmed. |
| `json_mode`            | true  | Confirmed — same platform-wide Gemini API feature verified for `gemini-2.5-flash`. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `high`   | Google's own materials position it as an agentic-focused Flash-tier model, not the (still-delayed) Pro tier — `high`, not `very_high`, reserved for a Pro-class model once one is actually released and sourceable. |
| `coding`                   | `high`   | Explicitly called out as excelling at "code generation" — one of the more directly-sourced editorial calls in this catalog, not a generic tier guess. |
| `creative_writing`         | `medium` | No strong signal either way; conservative default. |
| `instruction_following`    | `high`   | Consistent with an agentic-focused positioning, where reliable instruction/tool-use matters most. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `gemini-2.5-flash`/`gemini-2.5-pro` (same provider, same known gap,
see [IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,048,576  |
| `max_output`           | 65,536     |

Confirmed directly against the official model card — same ceiling as
Gemini 2.5 Flash/Pro.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $1.50  |
| `output_per_million`        | $7.50  |

Confirmed directly against Google's pricing page. Notably cheaper than
Gemini 2.5 Flash's blended cost ($2.80 vs. $9.00) despite being a
newer generation — worth double-checking on a future pass in case this
reflects an early-release promotional rate rather than durable
pricing; nothing in the source page flagged it as introductory, but
that's exactly the kind of thing Claude Sonnet 5's entry shows can
happen without obvious warning on the page itself.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same Gemini API surface as the 2.5 generation. |
| `maturity`              | `stable` | Generally available (released 2026-07-21), not marked preview. |

---

## Sources

- [Gemini 3.6 Flash model card](https://ai.google.dev/gemini-api/docs/models/gemini-3.6-flash) — capabilities, context window, max output.
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields.

Both accessed 2026-08-07, official Google documentation only. Note:
the model card page did not state an explicit knowledge-cutoff date at
the time of this pass (only a "last updated" page date of
2026-07-30) — flagged rather than guessed.

## Verification result

New dataset entry. Objective fields confirmed against official
documentation. Knowledge cutoff date not found/not applicable to the
schema (schema doesn't track it), noted for completeness only.
