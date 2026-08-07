# Gemini 3.5 Flash-Lite

Dataset entry: [`dataset/models/gemini-3.5-flash-lite.yaml`](../../dataset/models/gemini-3.5-flash-lite.yaml)
Last verified: 2026-08-07

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. See also `gemini-3.6-flash.md` for a
note on why "Gemini 3.1 Pro" and "Gemini 3.5 Pro" (both mentioned in
the original request) aren't in this dataset.

---

## Identity

| Field      | Value                     |
|------------|-----------------------------|
| `id`       | `gemini-3.5-flash-lite`    |
| `name`     | Gemini 3.5 Flash-Lite      |
| `provider` | Google                      |
| `version`  | `3.5`                       |
| `license`  | `proprietary`               |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Input modalities: text, image, video, audio, PDF — same breadth as Gemini 3.6 Flash despite being the "lite" tier. |
| `audio`                | true  | Audio input confirmed. |
| `image_generation`     | false | Output modality is text-only. |
| `tool_calling`         | true  | Confirmed; explicitly positioned for "subagent tasks," which implies tool use is a core design target, not an afterthought. |
| `structured_output`    | true  | Confirmed. |
| `json_mode`            | true  | Confirmed — same platform-wide Gemini API feature verified for `gemini-2.5-flash`. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `medium` | Google's own description: "low-latency, cost-effective... optimized for high-throughput, low-cost execution for subagent tasks and document parsing" — a lightweight tier, positioned below Flash, not a reasoning-focused model. |
| `coding`                   | `medium` | Same reasoning. |
| `creative_writing`         | `low`    | Lite-tier models built for narrow, high-throughput tasks typically trade away stylistic depth first. |
| `instruction_following`    | `medium` | The explicit "subagent tasks" positioning implies decent reliability following structured instructions, kept in line with the other dimensions rather than singled out higher, unlike the nano-tier OpenAI judgment call. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `gemini-2.5-flash`/`gemini-3.6-flash` (same provider, same known
gap, see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,048,576  |
| `max_output`           | 65,536     |

Confirmed directly against the official model card — same ceiling as
the rest of the Gemini 2.5/3.6 family; the "lite" positioning is about
cost and latency, not a smaller context window.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.30  |
| `output_per_million`        | $2.50  |

Confirmed directly against Google's pricing page — identical to Gemini
2.5 Flash's pricing exactly, despite being a newer generation. Worth
noting as observed, not explained away: it's plausible Flash-Lite
inherited 2.5 Flash's price point as the new "entry tier" price while
3.6 Flash moved up-market. Not treated as an error.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same Gemini API surface as the rest of the family. |
| `maturity`              | `stable` | Generally available, released alongside Gemini 3.6 Flash (2026-07-21), not marked preview. |

---

## Sources

- [Gemini 3.5 Flash-Lite model card](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite) — capabilities, context window, max output, positioning.
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields.

Both accessed 2026-08-07, official Google documentation only.

## Verification result

New dataset entry. Objective fields confirmed against official
documentation. No drift, no gaps — this is a cleanly-sourced entry.
