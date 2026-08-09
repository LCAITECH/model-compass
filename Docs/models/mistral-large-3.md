# Mistral Large 3

Dataset entry: [`dataset/models/mistral-large-3.yaml`](../../dataset/models/mistral-large-3.yaml)
Last verified: 2026-08-07

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
| `input_per_million`         | $2.00  |
| `output_per_million`        | $6.00  |

Partially confirmed: Mistral's pricing page FAQ gives "$2/M tokens in
and $6/M tokens out" as a worked example for "Mistral Large," matching
the dataset exactly. This example did not explicitly say "Large 3" by
name, so treat this as a strong match rather than a fully independent
reconfirmation — worth a direct check against the model card's own
pricing line next time that page is reachable.

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
- [Mistral pricing](https://mistral.ai/pricing) — cost fields (partial match, see note above).
- `https://docs.mistral.ai/getting-started/models/model-cards/mistral-large-3-25-12` — attempted, returned HTTP 404 as of this pass. Left here so the next verification pass doesn't waste time rediscovering that this specific URL doesn't resolve.

Accessed 2026-08-07, official Mistral documentation only.

## Verification result

License and pricing reasonably confirmed. **Operational fields
(context window, max output) and all six capability flags were not
independently reconfirmed this pass** — this is the model with the
most open sourcing gaps of the five in the dataset right now. Nothing
in the dataset entry was changed as a result; this is logged as a
pending verification, not a correction.
