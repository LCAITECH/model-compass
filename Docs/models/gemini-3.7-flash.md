# Gemini 3.7 Flash

Dataset entry: [`dataset/models/gemini-3.7-flash.yaml`](../../dataset/models/gemini-3.7-flash.yaml)
Last verified: 2026-08-13

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows.

---

## Naming note

Gemini 3.7 Flash's official model card
(`deepmind.google/models/model-cards/gemini-3-7-flash/`) was published
2026-08-13 — the same day this entry was researched. Confirmed real,
not a placeholder or leak, via two independent direct reads of the
page (not a summarization tool) plus cross-check against the model
cards index (`deepmind.google/models/model-cards/`), which lists it as
the most recently updated entry in the entire Gemini family, above
Gemini 3.6 Flash (2026-07-21). As of this same date, the Gemini API
models listing (`ai.google.dev/gemini-api/docs/models`, page dated
2026-08-04) does not yet list it — read as ordinary documentation lag
(the API page predates the model card by 9 days), not evidence against
the model's existence. See `ecosystem.maturity` below for how this
timing gap is handled editorially.

Several third-party AI-generated "audits" of this and related model
cards were also reviewed during this research pass, but none were used
as a source for any field below — see `IMPLEMENTATION_NOTES.md`,
Iteration #14, for why (a concrete cross-check found one such audit
claiming a 2M-token context window for Gemini 3.1 Pro, contradicted by
this project's own already-sourced `gemini-3.1-pro-preview.yaml`,
which has 1,048,576). Every fact below traces to a primary Google
source, read directly.

## Identity

| Field      | Value               |
|------------|----------------------|
| `id`       | `gemini-3.7-flash`   |
| `name`     | Gemini 3.7 Flash     |
| `provider` | Google                |
| `version`  | `3.7`                 |
| `license`  | `proprietary`         |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model card, Inputs: "Text strings..., images, audio, and video files." |
| `audio`                | true  | Same Inputs statement; output is text-only (see below). |
| `image_generation`     | false | Model card, Outputs: "Text, with a 64K token output." No image output modality stated. |
| `tool_calling`         | true  | Not stated directly on the model card. Confirmed via `ai.google.dev/gemini-api/docs/function-calling`, which scopes reasoning-enhanced function calling, parallel/compositional calls, and multimodal function responses to "Gemini 3 series models" generically, no exclusions listed. Gemini 3.7 Flash is explicitly "the next iteration in the Gemini 3 model family" per its own model card. |
| `structured_output`    | true  | Confirmed via `ai.google.dev/gemini-api/docs/structured-output`: JSON-schema-constrained output ("Puedes configurar los modelos de Gemini para que generen respuestas que cumplan con un esquema JSON") stated generically for Gemini models; the enhanced structured-output-plus-tools mode is explicitly scoped to "los modelos de la serie Gemini 3." |
| `json_mode`            | true  | Same source as `structured_output` — `response_format` with `mime_type: application/json` is this feature under a different name. |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `very_high` | Consistent improvement over Gemini 3.6 Flash across the model card's own benchmark table: Artificial Analysis Intelligence Index 56 vs. 52, HLE-Verified 53.6% vs. 51.2%, GDM-MRCR v2 (long context) 97.0% vs. 91.8%. Comparison is against 3.6 Flash specifically (same card, same methodology), not a claim of standing versus the rest of the dataset. |
| `coding`                   | `very_high` | Strongest, most consistent delta in the whole benchmark table: FrontierCode 1.1 43.6% vs. 34.4%, DeepSWE v1.1 65.3% vs. 48.6%, Terminal-bench 2.1 85.8% vs. 78.0%, Code Arena (Elo) 1588 vs. 1538. |
| `creative_writing`         | `medium` | No creative-writing-specific benchmark or claim anywhere on the model card. Kept at the same conservative default as Gemini 3.6 Flash rather than inferring from unrelated benchmarks. |
| `instruction_following`    | `high`   | No dedicated instruction-following benchmark. The internal safety-eval table shows a mixed signal versus 3.6 Flash (Tone -0.47pp is worse, Unjustified-refusals +0.84pp is worse, Text-to-Text Safety +1.17pp is better) — not a clear enough signal to justify moving above 3.6 Flash's own `high`. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `gemini-3.6-flash`/`gemini-2.5-flash` (same provider, same known
gap — see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,048,576  |
| `max_output`           | 65,536     |

Confirmed directly against the model card: "a token context window of
up to 1M" (input), "64K token output." Same ceiling as Gemini 3.6
Flash and the rest of the Gemini 3 family.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.75  |
| `output_per_million`        | $3.75  |

**Introductory price, with a confirmed expiration date** — same
pattern as Gemini 3.6 Flash (see that model's own entry, corrected in
this same session). Quoted directly from the model card's benchmark
pricing table footnote: *"For 3.6 and 3.7 Flash, introductory price
expires on December 31, 2026. Starting January 1, 2027, $1.50/1M input
tokens and $7.50/1M output tokens will apply."* This entry's `cost.*`
will need the same follow-up correction on 2027-01-01 that
`gemini-3.6-flash.yaml` now needs a re-check for.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same Gemini API surface as Gemini 3.6 Flash — identical distribution channel list, and the function-calling/structured-output docs scope their features to "Gemini 3 series models" without carving out exceptions for this specific model. |
| `maturity`              | `experimental` | New editorial principle established this session, applied here for the first time: **maturity is not derived from technical availability alone — it requires evidence of stability in public, provider-maintained documentation.** As of this entry's research date, `ai.google.dev/gemini-api/docs/models` (the page that labels each Gemini model "Estable"/"Vista previa"/experimental) does not list Gemini 3.7 Flash at all yet, only Gemini 3.6 Flash as the newest stable entry. The model card's existence and GA-sounding language aren't treated as equivalent to that catalog listing. Revisit once the model appears in that catalog with an explicit stability label. |

---

## Access

Standard Gemini API — Google AI Studio and (unconfirmed for this
specific model) Vertex AI — at the pricing in `cost.*` above. Also
listed in the model card's Distribution section under: Gemini App
(Spark), Gemini Enterprise App, Gemini Enterprise Agent Platform,
Google AI Studio, Gemini API, Google Antigravity (Antigravity isn't
itself a valid pricing source — see `IMPLEMENTATION_NOTES.md`,
Iteration #6).

**Free access (`access.has_free_access`):** `true`, with a caveat.
`ai.google.dev/gemini-api/docs/rate-limits` confirms Gemini 3.7 Flash
is listed among the models covered by Google's tiered rate-limit
system (which includes a Free tier reachable with just a Google
account, no billing) — but, per that same page, Google does not
publish a static public table of the actual limits; it explicitly
states limits "depend on a variety of factors... can be viewed in
Google AI Studio." The project owner's own AI Studio project dashboard
(`aistudio.google.com/u/4/rate-limit`, 2026-08-13) shows Gemini 3.7
Flash at 0/5 RPM, 0/250K TPM, 0/20 RPD — identical shape to Gemini 3.6
Flash's own free-tier quota. Per the same discipline already applied
to Gemini 3.6 Flash and NVIDIA NIM (Iteration #8), this dashboard
reading is real but account-specific, not a citable public document —
included here for context only, not as the basis for the boolean
above. The boolean itself rests on the public rate-limits page listing
the model under the tiered system that includes an unbilled Free tier,
the same reasoning already applied to every other Gemini model in this
dataset.

**How to access:**

1. Sign in with a Google account.
2. Open [Google AI Studio](https://aistudio.google.com/) — a project
   and API key are created automatically for new users.
3. Accept the Gemini API Terms of Service.
4. Copy the API key, or generate one manually at
   `aistudio.google.com/apikey`.
5. Install a Gemini SDK (e.g. `pip install -U google-genai`) and set
   the key as an environment variable to start making calls.

**Billing and subscription:** no billing account and no credit card
required for the Free Tier, same terms as every other Gemini model in
this dataset — see `gemini-3.6-flash.md`'s Access section for the
verbatim Google billing-docs quote, not repeated here.

### Rate limits

Same situation as every other Gemini model in this dataset: Google
defines RPM/TPM/RPD per project, varying by model and usage tier, with
no fixed public table — only viewable per-account in Google AI Studio.
Source: `ai.google.dev/gemini-api/docs/rate-limits`. The observed
dashboard numbers above (0/5, 0/250K, 0/20) are one project's snapshot
on one date, not a specification.

## Sources

- [Gemini 3.7 Flash model card](https://deepmind.google/models/model-cards/gemini-3-7-flash/) — description, model dependencies, inputs/outputs, distribution, pricing table, benchmark results, safety evaluation. Read directly in-browser, two independent passes, 2026-08-13.
- [Gemini 3.6 Flash model card](https://deepmind.google/models/model-cards/gemini-3-6-flash/) — cross-check for the shared introductory-pricing pattern and "based on" lineage claim.
- [Model cards index](https://deepmind.google/models/model-cards/) — confirmed publish date (2026-08-13) and that this is the most recently updated entry in the Gemini family, read directly in-browser.
- [Gemini API — Function calling](https://ai.google.dev/gemini-api/docs/function-calling) — `tool_calling` scoped to "Gemini 3 series models."
- [Gemini API — Structured output](https://ai.google.dev/gemini-api/docs/structured-output) — `structured_output`/`json_mode` scoped generically to Gemini models, enhanced mode scoped to "Gemini 3 series."
- [Gemini API — Models](https://ai.google.dev/gemini-api/docs/models) — checked directly, page dated 2026-08-04, does not yet list this model; basis for the `maturity: experimental` call.
- [Gemini API — Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) — free-tier/paid-tier structure, no static table.
- Google AI Studio rate-limit dashboard (`aistudio.google.com/u/4/rate-limit`) — one project's observed Free Tier limits, 2026-08-13. Account-specific, not a public document — see caveat above.

All fields accessed and cross-checked 2026-08-13. Official Google
documentation only — third-party AI-generated audits of these same
pages were reviewed but explicitly excluded as sources (see Naming
note above and `IMPLEMENTATION_NOTES.md`, Iteration #14).

## Verification result

New dataset entry. All `[Objective]` fields confirmed against primary
official documentation, read directly (not via summarization tooling)
on a second pass to guard against extraction errors. `[Editorial]`
fields are this project's own judgment, informed by but not derived
from the model card's benchmark table, per `SCHEMA.md`.
