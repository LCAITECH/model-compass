# Gemini 4 Argon

Dataset entry: [`dataset/models/gemini-4-argon.yaml`](../../dataset/models/gemini-4-argon.yaml)
Access route: [`dataset/access_routes/google/gemini-4-argon-direct-api.yaml`](../../dataset/access_routes/google/gemini-4-argon-direct-api.yaml)
Last verified: 2026-10-14 (access routes re-read 2026-10-17)

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from the bot's PR #6 note
(Iteration #25) about Google's 2026-10-13 general availability; that
note and a third-party AI-generated news digest were not used as
sources for any field below. Every value was read from Google's own
pages (raw HTML, not a summarizer): the model page, the pricing page
and the models index.

---

## Naming note

Google also ran an earlier invite-only preview of Argon under the
"Fairwind Program" for cyber defenders (announcement blog, 2026-09-30).
This entry is the generally available `gemini-4-argon` on the Gemini
API; nothing about the invite-only program is modeled.

## Identity

| Field      | Value             |
|------------|-------------------|
| `id`       | `gemini-4-argon`  |
| `name`     | Gemini 4 Argon    |
| `provider` | Google            |
| `version`  | `4`               |
| `license`  | `proprietary`     |

## Capabilities `[Objective]`

Source for all rows: https://ai.google.dev/gemini-api/docs/models/gemini-4-argon

| Field               | Value | Notes |
|---------------------|-------|-------|
| `vision`            | true  | "Inputs: Text, Image, Video, Audio, and PDF." |
| `audio`             | true  | Audio **input**; output is text only ("Audio generation: Not supported"). |
| `image_generation`  | false | "Image generation: Not supported." |
| `tool_calling`      | true  | "Function calling: Supported." |
| `structured_output` | true  | "Structured outputs: Supported." |
| `json_mode`         | true  | Not itemized separately on the model page; same basis as `gemini-3.8-flash` (schema-constrained output is this feature under another name). |

Documented but not represented in the schema: code execution, search
grounding, Google Maps grounding, URL context, file search, computer
use (Preview), thinking levels low/medium/high, implicit caching only
(explicit caching "not supported"), Batch/Flex/Priority inference.

## Quality `[Editorial]`

**Judgment calls, proposed for owner review.** None derive from
benchmark scores.

| Field                   | Value       | Why |
|-------------------------|-------------|-----|
| `reasoning`             | `very_high` | Google's own description: "our flagship reasoning model, built for complex software engineering, deep mathematical and scientific problem solving, autonomous multi-step agents." The scale has no tier above `very_high`, so a flagship claim lands at the ceiling, same as `gemini-3.8-flash` and `gemini-3.1-pro-preview`. |
| `coding`                | `very_high` | Same source: "complex software engineering" is the first stated purpose. |
| `creative_writing`      | `medium`    | No creative-writing claim in anything read. Kept at the conservative default used for `gemini-3.8-flash`. |
| `instruction_following` | `high`      | No dimension-specific claim found; kept at the `gemini-3.8-flash` value rather than guessed upward. A flagship could justify `very_high` (as `gemini-3.1-pro-preview` has); needs a source or an owner call. |

## Languages

**Not stated** on the model page. Reused the curated Gemini set
(`gemini-3.8-flash` / `gemini-3.7-flash`), the same known gap as the rest
of the Gemini family
([IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field            | Value     | Source |
|------------------|-----------|--------|
| `context_window` | 1,048,576 | Model page: "Context window (unified input and output token limit): 1,048,576". |
| `max_output`     | 65,536    | Model page: "65,536 (default synchronous) / up to 1,048,576 (with long decode)". |

`max_output` stores the **default** limit. The higher maximum of
1,048,576 tokens applies with long decode and is documented here only,
same convention as a second price tier (Iteration #24, #26). Note the
context window is described as a unified input-plus-output budget.

Rate limits: the rate-limits page lists no RPM/TPM/RPD for this model
(it points to AI Studio); batch enqueued-token limits are 5,000,000
(Tier 1), 500,000,000 (Tier 2), 1,000,000,000 (Tier 3).

## Cost `[Objective]`

Paid Tier, Standard, USD per 1M tokens
(https://ai.google.dev/gemini-api/docs/pricing):

| Field                | Through 2026-11-30 | From 2026-12-01 |
|----------------------|--------------------|-----------------|
| `input_per_million`  | $2.00              | $4.00           |
| `output_per_million` | $10.00             | $20.00          |

Output includes thinking tokens. The dataset stores the current
introductory price with `effective_until: "2026-11-30"` and
`reverts_to` $4.00 / $20.00. **Reminder with a date: nothing in the
engine flips this automatically; from 2026-12-01 the displayed price is
stale until the entry is updated** (same class of reminder as
`gpt-5-6-sol`).

Not represented in the schema: context caching $0.10 → $0.20, Batch
$1.00/$5.00 → $2.00/$10.00, Flex the same as Batch, Priority
$3.60/$18.00 → $7.20/$36.00. No long-context tier is listed. Search
grounding is 5,000 free requests per month (shared across Gemini 3 and
newer), then $14 per 1,000.

## Ecosystem `[Editorial]`

| Field              | Value    | Why |
|--------------------|----------|-----|
| `integration_ease` | `high`   | Same Gemini API surface as the rest of the family; also on AI Studio. |
| `maturity`         | `stable` | The Gemini API models index (https://ai.google.dev/gemini-api/docs/models) lists Gemini 4 Argon under "Stable" and the model page lists "Stable: gemini-4-argon". This is the explicit stability label the `gemini-3.8-flash` entry was waiting for; it applies from day one. Computer use is separately marked Preview. |

---

## Access

Three routes (`dataset/access_routes/google/gemini-4-argon-*.yaml`):

- **Gemini API**, with a billing-linked project, at the `cost.*` above.
  The pricing page says "Gemini 4 Argon is not available on the Free
  tier", so **`access.has_free_access` is `false`**.
- **Gemini app**, on Google AI Pro and both Ultra tiers (Google's AI Pro
  page lists the "Gemini app with Gemini 4 Argon").
- **Google AI Studio**, on Google AI Pro and both Ultra tiers. The plans
  page lists "premium models like Gemini 4 Argon" under AI Pro and
  "advanced frontier models like Gemini 4 Argon" with the highest limits
  under AI Ultra, and says the model "is not available on the Free
  plan". The plan's quota applies only in the AI Studio web interface;
  API use is billed separately.

**Correction, 2026-10-17.** The AI Studio route was first recorded as
Ultra-only, from a plans page that said Argon was not available on the
Free or Google AI Pro plans (the pricing page said the same). Google
updated both pages (the plans page reads "Last updated 2026-10-16 UTC"):
AI Pro now lists Argon, and both pages name only the Free plan/tier as
excluded. The AI Studio unlock dialog ("needs a Google AI plan or a
Gemini API key") agrees, without naming a tier. That dialog is a UI
screen, not a source; the plans page is. Vertex / Gemini Enterprise Agent
Platform availability was not verified, so no cloud route is added.

**Antigravity route, proposed 2026-10-22 (owner request, Iteration #37).**
Google now names the model in Antigravity on two of its own pages. The
Google One plans page: "Expanded access to Gemini 4 Argon in Google
Antigravity and Google AI Studio" (AI Pro) and "Higher access to Gemini 4
Argon in Google Antigravity and Google AI Studio" (AI Ultra).
Antigravity's models page, "Reasoning model" table: Argon is not
available on "Free & Google AI Plus", available on Google AI Pro
("non-trial subscriptions only") and on Google AI Ultra, and "Not
available in Antigravity IDE. Available in the Antigravity App,
Antigravity CLI, and IDE extensions." The route
`gemini-4-argon-antigravity` uses the same shape as the Gemini app route
(a `consumer_subscription` surface on the three plans, not for
production). Antigravity's quota is refreshed every five hours with a
weekly cap, not published in tokens (Antigravity plans page).

## Sources

- https://ai.google.dev/gemini-api/docs/models/gemini-4-argon — identity, modalities, token limits, capabilities, stability (page updated 2026-10-13 UTC).
- https://ai.google.dev/gemini-api/docs/pricing — prices, caching, free-tier exclusion (re-read 2026-10-17: prices unchanged, "AI Pro" no longer named as excluded).
- https://ai.google.dev/gemini-api/docs/google-ai-plans — which plans include the model in AI Studio (read 2026-10-17, page updated 2026-10-16 UTC).
- https://support.google.com/googleone/answer/14534406 — Gemini app on AI Pro.
- https://ai.google.dev/gemini-api/docs/models — "Stable" label.
- https://ai.google.dev/gemini-api/docs/rate-limits — batch limits.
- https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/ — positioning, Ultra mention, Fairwind context (dated 2026-09-30).
- https://antigravity.google/docs/models and https://antigravity.google/docs/plans — Antigravity availability by plan and quotas (read 2026-10-22).
- https://one.google.com/intl/en_us/about/google-ai-plans/ — Argon in Antigravity on AI Pro and Ultra (read 2026-10-22).

All accessed 2026-10-14.

## Verification result

New entry. Objective fields confirmed against Google's own pages,
except `languages` (not published, curated set reused) and `json_mode`
(not itemized, inferred from structured outputs). Quality ratings are
editorial and flagged for owner review.
