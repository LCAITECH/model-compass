# Muse Spark 1.3

Dataset entry: [`dataset/models/muse-spark-1.3.yaml`](../../dataset/models/muse-spark-1.3.yaml)
Last verified: 2026-10-15

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted on 2026-10-15 with Muse Wonder.
Iteration #21 had held Muse Spark 1.3 out for its missing `max_output`;
Iteration #26 made the field nullable, and Meta now publishes a figure
anyway (see Operational). Every field below was read on Meta's own pages.

---

## Identity

| Field      | Value             |
|------------|--------------------|
| `id`       | `muse-spark-1.3`   |
| `name`     | Muse Spark 1.3      |
| `provider` | Meta                |
| `version`  | `1.3`               |
| `license`  | `proprietary`       |

**Not separate entries:** `muse-spark-1.3-contributor` is the same model
at a lower price in exchange for letting Meta train on your content (a
pricing mode with its own id, described under Cost). Muse Spark 1.2 and
1.1 are earlier versions, still served at the same price; the owner chose
to admit only 1.3, which Meta marks "Recommended for new work".

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Models page: all Muse Spark versions "take text, image, video, audio, and PDF input". |
| `audio`                | false | Same page: "Audio understanding in Muse Spark 1.3 is currently not fully supported, and response quality for requests including audio content may be degraded. For audio, use Muse Spark 1.2". Meta's own agent configuration lists input `["text", "image", "pdf", "video"]`. Revisit when Meta drops the caveat. |
| `image_generation`     | false | Text output only. |
| `tool_calling`         | true  | Models page feature list. |
| `structured_output`    | true  | Models page feature list; JSON Schema constrained decoding (structured-output guide, whose examples use `muse-spark-1.3`). |
| `json_mode`            | true  | JSON Schema structured output only, no separate JSON mode: same basis as other entries. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `high`   | Meta's model for "agentic and coding work — multi-step tool loops, software engineering assistants, and long-context reasoning", but its own guidance sends complex, capability-first work to Muse Wonder and positions Spark for "high-volume, latency-sensitive, or cost-sensitive work". |
| `coding`                   | `high`   | Model page: "optimized for competitive coding performance ... performs competitively with frontier models across several coding evals". A claim of parity on some evals, not leadership, from the provider's volume tier: `high`, as for `claude-haiku-5-5` and `qwen3.8-flash`. |
| `creative_writing`         | `medium` | No creative-writing claim found. |
| `instruction_following`    | `high`   | Launch post: "follows complex, long-form instructions more reliably than earlier Muse Spark models ... better at preserving detailed requirements without dropping constraints". |

Proposed by Claude, approved by the project owner (2026-10-15).

## Languages

Same curated list as `muse-wonder-1.0` (Iteration #33): Meta publishes
no supported-language list. English `very_high`; Spanish, Portuguese,
French, German, Italian `high`.

## Operational `[Objective]`

| Field              | Value       |
|----------------------|-------------|
| `context_window`      | 1,048,576   |
| `max_output`           | 131,072     |

Context: "a 1,048,576-token context window" (models page). Output: Meta's
quickstart and coding-agents guide tell agents to register
`muse-spark-1.3` with "Limits: context 1048576, output 131072". It is
the only output figure Meta publishes, inside a configuration it
recommends rather than a limits table; recorded as Meta's own number
(Iteration #33). Iteration #21 found no such figure on 2026-09-08.

## Cost `[Objective]`

| Field                    | Value   |
|----------------------------|---------|
| `input_per_million`         | $1.25  |
| `output_per_million`        | $4.25  |

Pricing page, Standard mode: Meta does not use your content to train its
models. Cached input $0.15/M. Contributor mode, through
`muse-spark-1.3-contributor`: $0.10 input, $0.20 output, $0.002 cached,
"in exchange for permission to use your content ... to train future Meta
models", with lower rate limits (150 RPM). Not stored: the engine ranks
on the price that keeps your data out of training.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | OpenAI- and Anthropic-compatible endpoints; Meta's setup guides cover OpenCode, Codex and Claude Code. |
| `maturity`              | `stable` | "The latest version ... Recommended for new work" on the models page, no preview label; the line has had three versions since its launch. |

---

## Access

One route: direct API on Meta Model API, `api_billing_linked`,
`region_scope: region_dependent` (Geographic Use Policy). Rate limits per
team: 3,000 RPM, 4,000,000 TPM. Also in Muse Code.

**Free access (`access.has_free_access`):** `false`. Contributor mode is
discounted, not free, and no free consumer plan names the model.

## Lifecycle

`active`. Released 2026-09-02 ("Muse Spark 1.3 with max reasoning is now
available on Muse Code and Meta Model API", launch post). No deprecation
published.

## Sources

- [Models](https://dev.meta.ai/docs/models) — versions, modalities, audio caveat, context window.
- [Pricing and rate limits](https://dev.meta.ai/docs/pricing-rate-limits) — Standard and Contributor prices, rate limits.
- [Muse Spark 1.3 model page](https://dev.meta.ai/models/muse-spark) — positioning.
- [Introducing Muse Spark 1.3](https://research.meta.ai/blog/introducing-muse-spark-1-3) — release date, instruction following.
- [Quickstart](https://dev.meta.ai/docs/quickstart) and [coding agents guide](https://dev.meta.ai/docs/coding-agents) — output limit, input modalities.
- [Structured output](https://dev.meta.ai/docs/structured-output).

All accessed 2026-10-15, Meta's own pages only.

## Verification result

New entry. Objective fields confirmed on Meta's documentation. `audio`
is `false` on Meta's own caveat; `max_output` comes from Meta's agent
configuration, flagged as such. `json_mode` and the language list are
curated.
