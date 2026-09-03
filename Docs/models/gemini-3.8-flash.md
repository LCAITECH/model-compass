# Gemini 3.8 Flash

Dataset entry: [`dataset/models/gemini-3.8-flash.yaml`](../../dataset/models/gemini-3.8-flash.yaml)
Last verified: 2026-09-02

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from a tip in a third-party
AI-generated audit (Grok) about Google's 2026-09-02 GA announcement —
the tip itself was not used as a source for any field below; every
fact was independently re-confirmed by reading Google's own pages
directly (see Sources), same discipline already applied to every prior
Grok tip this project has received (`IMPLEMENTATION_NOTES.md`,
Iterations #14 and #16).

---

## Naming note

The tip also flagged **Gemini 3.8 Flash Cyber**, a cybersecurity-
specialized variant available only through Google's invite-only
"Fairwind Program" (trusted government/critical-infrastructure/software-
maintainer defenders). Confirmed directly on Google's announcement
blog: no public `$`/MTok price is stated anywhere for it, and it
doesn't appear on the Gemini Developer API pricing page. **Not added
to this catalog** — same admission bar every other invite-only,
unpriced model in this dataset has failed to clear (Claude Mythos
5/5.1, Gemini 3.5 Flash Cyber — see `FEATURES.md`'s "Specialized /
Domain-Specific Models" entry for the latter). Revisit if Google
publishes a public price and general availability.

## Identity

| Field      | Value               |
|------------|----------------------|
| `id`       | `gemini-3.8-flash`   |
| `name`     | Gemini 3.8 Flash     |
| `provider` | Google                |
| `version`  | `3.8`                 |
| `license`  | `proprietary`         |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page: "Supported data types — Inputs: Text, Image, Video, Audio, and PDF." |
| `audio`                | true  | Same Inputs statement; output is text-only ("Audio generation: Not supported"). |
| `image_generation`     | false | Model page: "Image generation: Not supported." |
| `tool_calling`         | true  | Model page: "Function calling: Supported." |
| `structured_output`    | true  | Model page: "Structured outputs: Supported." |
| `json_mode`            | true  | Not itemized separately from `structured_output` on the model page — same basis already used for the rest of the Gemini 3 family (`response_format`/schema-constrained output is this feature under a different name). |

## Quality `[Editorial]`

| Field                    | Value    | Why |
|---------------------------|----------|-----|
| `reasoning`                | `very_high` | Google's announcement blog: "our best reasoning & coding model yet," achieves 54.9% on HLE-Verified (up from 3.7 Flash's 53.6%), described as "often approaching the performance of higher-cost frontier models." Kept at the same ceiling as `gemini-3.7-flash` (already `very_high`) rather than treated as newly exceptional — per `SCHEMA.md`'s evidence-based calibration principle, real improvement over the prior version doesn't get a rating this 4-level scale has no room above. |
| `coding`                   | `very_high` | Same source: "significant improvements from 3.7 Flash across software engineering," outperforms "most larger frontier models" on DeepSWE v1.1 (long-horizon software engineering). Same ceiling reasoning as `reasoning`. |
| `creative_writing`         | `medium`    | No creative-writing-specific claim found anywhere checked (blog, model card, model page). Kept identical to `gemini-3.7-flash`'s conservative default rather than guessed independently. |
| `instruction_following`    | `high`      | Google's own internal safety-eval comparison to 3.7 Flash: "performs similarly... across both safety and tone, with low unjustified refusals," plus an explicit prompt-injection robustness improvement (Gray Swan). Positive signal, but not a claim specific enough to justify a scale bump beyond 3.7 Flash's own `high` — kept identical, same "don't move a rating without dimension-specific evidence" discipline as `creative_writing` above. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `gemini-3.7-flash`/`gemini-3.6-flash` (same provider, same known
gap, see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,048,576  |
| `max_output`           | 65,536     |

Confirmed directly against the model's own official model page ("Input
token limit: 1,048,576," "Output token limit: 65,536") and independently
cross-checked against its model card ("a token context window of up to
1M," "Text, with a 64K token output") — same ceiling as the rest of the
Gemini 3 Flash family.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $0.75  |
| `output_per_million`        | $3.75  |

**Introductory price, with a confirmed expiration date** — same
pattern and same exact footnote text as `gemini-3.6-flash`/`gemini-3.7-flash`.
Quoted directly from Google's own announcement blog post: "It is
available at the same introductory price¹ as 3.7 Flash at $0.75 per
million input tokens and $3.75 per million output tokens," with
footnote 1 reading, verbatim: *"Introductory price expires on December
31, 2026. Starting January 1, 2027, $1.50/1M input tokens and $7.50/1M
output tokens will apply."*

Notably, **this price does not appear on the Gemini Developer API
pricing page** (`ai.google.dev/gemini-api/docs/pricing`) as of this
verification — checked directly against the page's raw HTML, not just
its rendered text, and `gemini-3.8-flash` isn't present anywhere in it.
The blog post's own footnote is used as the source instead, the same
first-party-but-not-the-generic-pricing-page pattern already
established for `gemini-3.7-flash` (whose price came from its model
card, not this same pricing page either).

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same Gemini API surface as the rest of the Gemini 3 Flash family — confirmed distribution via Gemini app, Gemini Enterprise Agent Platform, Google AI Studio, Gemini API, Google AI Mode, and Google Antigravity (model card, Distribution section). |
| `maturity`              | `experimental` | Same principle applied to `gemini-3.7-flash` at its own admission: maturity requires evidence of stability in the platform's public model catalog, not just a model card and announcement. As of this verification date, `ai.google.dev/gemini-api/docs/models` (the page that labels each Gemini model's stability) does not list `gemini-3.8-flash` — and, checked in the same pass, still doesn't list `gemini-3.7-flash` either, three weeks after that model's own admission. Revisit once the model appears in that catalog with an explicit stability label. |

---

## Access

Standard Gemini API — Google AI Studio — at the pricing in `cost.*`
above, same single `direct_api` route pattern as `gemini-3.6-flash`/
`gemini-3.7-flash`. Also distributed via Gemini app, Gemini Enterprise
Agent Platform, Google AI Mode, and Google Antigravity per the model
card's Distribution section, and available to Google AI Pro/Ultra
subscribers per the announcement blog — neither modeled as a separate
schema access route yet, consistent with how this catalog has treated
every other Gemini model's non-API surfaces so far.

**Free access (`access.has_free_access`):** `false`. Unlike
`gemini-3.6-flash`/`gemini-3.7-flash` (confirmed `true` via the Gemini
Developer API pricing page's free-tier column and the rate-limits
page's tiered-system listing), neither of those pages mentions
`gemini-3.8-flash` at all as of this verification — checked directly
against both pages' raw HTML, not inferred. No public source
confirms continuous free access for this specific model yet, so this
defaults to `false` per this catalog's strict bar (same default used
whenever explicit confirmation is absent, e.g. `claude-haiku-4-5`).
Revisit once either page is updated.

## Sources

- [Gemini 3.8 Flash model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) — identity, capabilities, context window, max output, distribution surfaces.
- [Gemini 3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/) — description, positioning, knowledge cutoff, safety-evaluation comparison to 3.7 Flash, distribution.
- [Introducing Gemini 3.8 Flash and 3.8 Flash Cyber](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) — GA announcement, pricing (including the footnote expiration date), benchmark claims, Cyber variant's limited-availability terms, consumer/enterprise/developer access surfaces.
- [Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing) — checked directly (raw HTML), confirms this model is **not yet listed**; basis for not using this page as the cost source and for the `has_free_access: false` call.
- [Gemini API models](https://ai.google.dev/gemini-api/docs/models) — checked directly, does not yet list this model (or `gemini-3.7-flash`); basis for the `maturity: experimental` call.

All read directly in-browser, 2026-09-02, not via summarization
tooling. No third-party AI-generated audit content used as a source
for any field above.

## Verification result

New dataset entry. All `[Objective]` fields confirmed against primary
official Google documentation. `[Editorial]` fields kept identical to
`gemini-3.7-flash` where no dimension-specific counter-evidence was
found, per `SCHEMA.md`'s evidence-based calibration principle. Two
fields defaulted conservatively for lack of public confirmation as of
this date, both explicitly flagged rather than guessed: `maturity`
(`experimental`, pending catalog listing) and `access.has_free_access`
(`false`, pending pricing/rate-limits page listing).
