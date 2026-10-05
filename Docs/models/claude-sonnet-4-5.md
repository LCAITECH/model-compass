# Claude Sonnet 4.5 — removed from active catalog

Dataset entry: **removed** (was [`dataset/models/claude-sonnet-4-5.yaml`](../../dataset/models/claude-sonnet-4-5.yaml))
Last catalog action: 2026-10-05

---

## Lifecycle

| Field | Value |
|-------|--------|
| API model name | `claude-sonnet-4-5-20250929` |
| Status | **Deprecated** |
| Deprecated | 2026-09-30 |
| Tentative retirement | 2026-11-30 |
| Recommended replacement | `claude-sonnet-5-5` (still in this catalog) |

Source: [Anthropic model deprecations](https://docs.anthropic.com/en/docs/about-claude/model-deprecations) (fetched 2026-10-05).

Anthropic defines Deprecated as still functional but **no longer recommended**. Model Compass only recommends models that belong in the active dataset, so this entry and its four access routes were removed rather than left as a silent recommendation path. The audit-trail doc is kept so the retirement decision stays reproducible.

## Why not a `maturity: legacy` flag

`SCHEMA.md`'s `ecosystem.maturity` enum is only `experimental` / `stable` / `mature` — there is no deprecated/legacy value (deliberately; see earlier Claude legacy admissions). Catalog policy for deprecated Anthropic models was left open in `IMPLEMENTATION_NOTES.md` Iteration #22; this removal is the first explicit decision: drop from `dataset/models/` when the provider marks Deprecated and names a replacement already in the catalog.

## Sources

- [Model deprecations](https://docs.anthropic.com/en/docs/about-claude/model-deprecations) — status, dates, replacement.
- Prior admission audit (2026-08-10) retained in git history for objective fields while the model was Active/Legacy.
