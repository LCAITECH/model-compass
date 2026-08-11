# Mistral Large 3

Dataset entry: [`dataset/models/mistral-large-3.yaml`](../../dataset/models/mistral-large-3.yaml)
Last verified: 2026-08-11 (Cost section only — see below; everything else last touched 2026-08-07)

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Identity

| Field      | Value              |
|------------|---------------------|
| `id`       | `mistral-large-3`    |
| `name`     | Mistral Large 3      |
| `provider` | Mistral AI            |
| `version`  | `3`                    |
| `license`  | `open-weights`         |

`license: open-weights` is confirmed — Mistral's own docs state
Mistral Large 3 is Apache 2.0. One nuance: Mistral's docs label the
specific build `25.12`, while the dataset's `version` field says `3`
(matching the public model name "Large 3", not the internal build
tag). Not treated as a discrepancy — `version` follows `SCHEMA.md`'s
"as published by the provider" language, and "Large 3" is how Mistral
publicly names it; `25.12` is noted here for anyone trying to match
this entry to a specific release later.

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Not independently reconfirmed this pass — Mistral's overview page describes Large 3 as "multimodal" (implying vision) but the model card page that would confirm this explicitly returned a 404 during this pass. Inherited from original curation. |
| `audio`                | false | Not independently reconfirmed this pass — inherited. |
| `image_generation`     | false | Not independently reconfirmed this pass — inherited. |
| `tool_calling`         | true  | Not independently reconfirmed this pass — inherited. |
| `structured_output`    | true  | Not independently reconfirmed this pass — inherited. |
| `json_mode`            | true  | Not independently reconfirmed this pass — inherited. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `high`   | Positioned as Mistral's flagship general-purpose model; editorial judgment, not benchmark-derived. |
| `coding`                   | `high`   | Same reasoning as above. |
| `creative_writing`         | `medium` | No strong signal either way; default mid-tier judgment. |
| `instruction_following`    | `high`   | Consistent with flagship positioning. |

## Languages

Not independently reconfirmed this pass. `languages` and
`language_quality` in the dataset entry are curated, same known gap as
the other providers (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

**Not independently reconfirmed this pass.** `context_window`
(262,144) and `max_output` (262,144) in the dataset entry could not be
matched against an official source during this pass — Mistral's
overview page doesn't list per-model specs, and the specific model
card page (`/models/model-cards/mistral-large-3-25-12`) returned a 404
when fetched. These values are inherited from the original dataset
curation, not freshly verified. Flagging explicitly per this folder's
sourcing rule, rather than presenting a 404 lookup as confirmation.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.50  |
| `output_per_million`        | $1.50  |

**Corrected 2026-08-11 — the previous $2.00/$6.00 value was stale.**
That figure came from a generic "Mistral Large" worked example on
Mistral's pricing-page FAQ, never confirmed against this specific
model's own card, since the model-card URL 404'd during the original
2026-08-07 pass (see the dead-URL note preserved in Sources below).
That URL now resolves — Mistral's own Large 3 model card
(`docs.mistral.ai/models/model-cards/mistral-large-3-25-12`) states
**$0.50 input / $1.50 output per million tokens**, a real current-price
mismatch, not an editorial judgment call. This also moves
`cost.blended` from $8.00 to $2.00 — from `CostTier.MEDIUM` to the
`LOW`/`MEDIUM` boundary under the fixed cost-tier bands in `SCHEMA.md`.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `medium` | Open-weights means broader self-hosting options, but first-party API/tooling is less mature than OpenAI/Anthropic/Google. |
| `maturity`              | `stable` | Generally available, listed among Mistral's current (not legacy/preview) models. |

---

## Access

Standard Mistral API (La Plateforme) at the pricing in `cost.*` above.
Also downloadable as open-weights (`license: open-weights`, Apache
2.0) for self-hosting — a genuinely different access path from the
rest of this dataset's proprietary models, though not priced per-token
when self-hosted, so not reflected in `cost.*`.

**Free access (`access.has_free_access`):** `false`. Mistral's own docs
confirm La Plateforme has a free API tier generally ("designed to allow
you to try and explore their API"), but no official source found this
pass confirms Mistral Large 3 specifically is included rather than
restricted to smaller models — defaults to `false` per the strict,
no-inference rule in `SCHEMA.md`'s Access section. Revisit if Mistral
publishes a model-by-model free-tier breakdown.

## Sources

- [Mistral models overview](https://docs.mistral.ai/getting-started/models/models_overview/) — identity, license, version tag.
- [Mistral pricing](https://mistral.ai/pricing) — cost fields, 2026-08-07 pass (superseded, see below).
- [Mistral Large 3 model card](https://docs.mistral.ai/models/model-cards/mistral-large-3-25-12) — corrected cost fields, 2026-08-11 pass. Note the path changed from
  `docs.mistral.ai/getting-started/models/model-cards/...` (404 on
  2026-08-07) to `docs.mistral.ai/models/model-cards/...` (resolves as
  of 2026-08-11) — a site reorganization, not a typo in the earlier
  pass.

Accessed 2026-08-07 (identity, license, original cost estimate) and
2026-08-11 (cost correction), official Mistral documentation only.

## Verification result

License confirmed 2026-08-07. **Operational fields (context window,
max output) and all six capability flags were not independently
reconfirmed** — this remains the model with the most open sourcing
gaps in the dataset.

**2026-08-11 cost correction** (part of a catalog-wide re-audit pass):
the previously "partially confirmed" $2.00/$6.00 pricing was wrong —
the actual model card, unreachable in the original pass, gives
$0.50/$1.50. This is the only field touched this pass; quality
ratings and the remaining sourcing gaps noted above are unchanged and
still pending.
