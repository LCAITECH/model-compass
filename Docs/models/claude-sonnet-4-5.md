# Claude Sonnet 4.5

Dataset entry: [`dataset/models/claude-sonnet-4-5.yaml`](../../dataset/models/claude-sonnet-4-5.yaml)
Last verified: 2026-08-10 (objective fields); lifecycle updated 2026-10-05

See [README.md](README.md) for what this document is (and isn't), and
`claude-opus-4-8.md` for why this and its sibling legacy Claude entries
were added.

---

## Lifecycle

| Field | Value |
|-------|--------|
| API model name | `claude-sonnet-4-5-20250929` |
| Status | **Deprecated** |
| Deprecated | 2026-09-30 |
| Tentative retirement | 2026-11-30 |
| Recommended replacement | `claude-sonnet-5-5` (already in this catalog) |

Source: [Anthropic model deprecations](https://docs.anthropic.com/en/docs/about-claude/model-deprecations) (fetched 2026-10-05).

Anthropic's Deprecated state means the model is still functional but no
longer recommended. Per `IMPLEMENTATION_NOTES.md` Iteration #22, whether
to remove deprecated entries from `dataset/models/` is a catalog-policy
decision not yet closed — this entry stays in the active dataset until
retirement or an explicit remove decision, with lifecycle recorded here
(same pattern as other provider deprecation notes in `Docs/models/`).
`ecosystem.maturity` remains `stable` because `SCHEMA.md` has no
`legacy`/`deprecated` enum value.

---

## Identity

| Field      | Value                        |
|------------|--------------------------------|
| `id`       | `claude-sonnet-4-5`            |
| `name`     | Claude Sonnet 4.5              |
| `provider` | Anthropic                       |
| `version`  | `4.5`                           |
| `license`  | `proprietary`                   |

Dated pinned snapshot: `claude-sonnet-4-5-20250929`.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Confirmed via Anthropic vision docs Standard tier for pre-4.7 models. |
| `audio`                | false | No audio content-block type in Anthropic's documented API. |
| `image_generation`     | false | Anthropic vision FAQ: image understanding only. |
| `tool_calling`         | true  | Explicit in tool-use pricing table. |
| `structured_output`    | true  | Named in structured-outputs Compatibility list. |
| `json_mode`            | true  | Same basis as structured_output. |

## Quality `[Editorial]`

| Field                    | Value    |
|---------------------------|----------|
| `reasoning`                | `medium` |
| `coding`                   | `medium` |
| `creative_writing`         | `medium` |
| `instruction_following`    | `medium` |

Evidence and calibration notes from the 2026-08-10 admission pass remain
in git history; not re-litigated on the 2026-10-05 lifecycle update.

## Languages

Curated Claude-family set (see IMPLEMENTATION_NOTES Iteration #1).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 200,000    |
| `max_output`           | 64,000     |

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $3.00  |
| `output_per_million`        | $15.00 |

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same availability as the rest of the Claude family. |
| `maturity`              | `stable` | Still generally available; no `legacy` value in `SCHEMA.md`. |

## Access

Standard Claude API plus Bedrock, Vertex, Foundry. `has_free_access: false`.

## Sources

- [Model deprecations](https://docs.anthropic.com/en/docs/about-claude/model-deprecations) — lifecycle (2026-10-05).
- [Claude models overview / pricing / structured outputs / vision](https://platform.claude.com/docs/) — objective fields (2026-08-10 admission).
