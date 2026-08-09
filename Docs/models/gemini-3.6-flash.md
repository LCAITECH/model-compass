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

## Access

Standard Gemini API — Google AI Studio and Vertex AI — at the pricing
in `cost.*` above. Also exposed inside Google Antigravity, which
isn't itself a valid pricing source — see
`IMPLEMENTATION_NOTES.md`, Iteration #6.

**Free access (`access.has_free_access`):** `true`. Google's own Gemini
API pricing page lists this model's standard input/output as "Free of
charge" under the free tier — confirmed directly against
`ai.google.dev/gemini-api/docs/pricing`, 2026-08-09.

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
required for the Free Tier — confirmed directly against Google's
official billing docs: *"New accounts begin on the Free Tier, which
allows access to certain models in the Gemini API and AI Studio, up to
the models' free tier rate limits."* Upgrading to a Paid Tier requires
linking a billing account and a minimum $10 prepayment; not required to
use this model on the Free Tier.

### Rate limits

**Documented (Google, official):** Google defines rate limits along
three dimensions — RPM (requests/minute), TPM (tokens/minute), RPD
(requests/day) — applied per project (not per API key), varying by
model and usage tier. Google does not publish a fixed public table of
these values; active limits are only viewable per-account in Google AI
Studio. Source: `ai.google.dev/gemini-api/docs/rate-limits`.

**Observed — Free Tier, one Google AI Studio project, 2026-08-09:**

| Limit | Value |
|---|---|
| Requests/minute | 5 |
| Tokens/minute | 250K |
| Requests/day | 20 |

Observed in one Google AI Studio project on the date above — not a
universal specification. Limits are project- and account-dependent and
may change; verify your own active limits in Google AI Studio before
relying on this number.

**Data policy:** Free Tier requests may be used by Google to improve
its products — confirmed directly against Google's official pricing
page ("Content used to improve our products: Yes" for the Free Tier;
the Paid Tier explicitly states the opposite).

## Sources

- [Gemini 3.6 Flash model card](https://ai.google.dev/gemini-api/docs/models/gemini-3.6-flash) — capabilities, context window, max output.
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields, free/paid tier data-policy distinction.
- [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) — RPM/TPM/RPD definitions and per-project/per-model behavior.
- [Gemini API billing](https://ai.google.dev/gemini-api/docs/billing) — Free vs. Paid Tier requirements.
- [Gemini API quickstart](https://ai.google.dev/gemini-api/docs/quickstart) — access setup steps.
- Google AI Studio rate-limit dashboard (`aistudio.google.com/rate-limit`) — one project's observed Free Tier limits, 2026-08-09. Account-specific, not a public document — see caveat above.

Identity/capabilities/cost/quality fields accessed 2026-08-07; Access
expansion above accessed 2026-08-09. Official Google documentation
only. Note:
the model card page did not state an explicit knowledge-cutoff date at
the time of this pass (only a "last updated" page date of
2026-07-30) — flagged rather than guessed.

## Verification result

New dataset entry. Objective fields confirmed against official
documentation. Knowledge cutoff date not found/not applicable to the
schema (schema doesn't track it), noted for completeness only.
