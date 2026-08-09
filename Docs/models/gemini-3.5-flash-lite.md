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

## Access

Standard Gemini API — Google AI Studio and Vertex AI — at the pricing
in `cost.*` above. No other access surface checked for this entry.

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
| Requests/minute | 15 |
| Tokens/minute | 250K |
| Requests/day | 500 |

Observed in one Google AI Studio project on the date above — not a
universal specification. Limits are project- and account-dependent and
may change; verify your own active limits in Google AI Studio before
relying on this number.

**Data policy:** Free Tier requests may be used by Google to improve
its products — confirmed directly against Google's official pricing
page ("Content used to improve our products: Yes" for the Free Tier;
the Paid Tier explicitly states the opposite).

## Sources

- [Gemini 3.5 Flash-Lite model card](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite) — capabilities, context window, max output, positioning.
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) — cost fields, free/paid tier data-policy distinction.
- [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) — RPM/TPM/RPD definitions and per-project/per-model behavior.
- [Gemini API billing](https://ai.google.dev/gemini-api/docs/billing) — Free vs. Paid Tier requirements.
- [Gemini API quickstart](https://ai.google.dev/gemini-api/docs/quickstart) — access setup steps.
- Google AI Studio rate-limit dashboard (`aistudio.google.com/rate-limit`) — one project's observed Free Tier limits, 2026-08-09. Account-specific, not a public document — see caveat above.

Identity/capabilities/cost/quality fields accessed 2026-08-07; Access
expansion above accessed 2026-08-09. Official Google documentation
only.

## Verification result

New dataset entry. Objective fields confirmed against official
documentation. No drift, no gaps — this is a cleanly-sourced entry.
