# GPT-6 Astra

Dataset entry: [`dataset/models/gpt-6-astra.yaml`](../../dataset/models/gpt-6-astra.yaml)
Last verified: 2026-09-07 (access route only — see "Access note" below;
all other fields last verified 2026-09-04, unchanged since)

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from a tip in a third-party
AI-generated audit (Grok) about OpenAI's 2026-09-04 announcement — the
tip itself was not used as a source for any field below; every fact
was independently re-confirmed by reading OpenAI's own pages directly
(see Sources), same discipline already applied to every prior Grok tip
this project has received (`IMPLEMENTATION_NOTES.md`, Iterations #14,
#16, #17).

---

## Access note — Trusted Access Program gate lifted (2026-09-07)

**Update, 2026-09-07:** the gate described below no longer applies.
Re-verified against `developers.openai.com/api/docs/pricing`, this
model's own page, and the models index (all three, live): the Trusted
Access Program rollout paragraph is gone from every one of them, GPT-6
Astra is now presented as the default flagship model with no access
caveat, and its rate-limits table lists standard usage tiers (Tier
1-5) identical in shape to every other self-serve model — no
program-membership tier anywhere. `dataset/access_routes/openai/gpt-6-astra-direct-api.yaml`
now uses `RequirementKind.API_BILLING_LINKED`, the same requirement as
`gpt-5-6-sol`'s own direct-api route, not `PROGRAM_MEMBERSHIP` anymore.
Verified directly with `recommend_access()`: `has_api_billing=True`
now resolves to `CURRENTLY_ELIGIBLE` regardless of
`program_memberships`; holding the Trusted Access Program membership
without billing info still correctly resolves to
`REQUIRES_ONBOARDING` — the checkbox has no effect on this route
anymore. See `IMPLEMENTATION_NOTES.md`, Iteration #19.

Per Iteration #18's own closing note ("add a second route [for
Plus/Pro/Business/Enterprise], don't upgrade this one in place"): that
guidance was about a *future, separate* consumer-subscription surface
possibly appearing later, not about the direct-API route's own gate
being lifted. This is the second case, not the first — the same
`surface: direct_api` route just no longer requires program
membership, so it was edited in place rather than left stale next to
a new one.

The rest of this section is kept as written on 2026-09-04, for the
historical record of what the gate actually looked like and why it
was modeled the way it was:

GPT-6 Astra's price is public and it sits on OpenAI's standard
Flagship pricing table, not a separate limited-access tier — but its
own model page stated plainly: *"GPT-6 Astra is rolling out today for
enterprises in our Trusted Access Program, with access through API and
our Plus, Pro, Business and Enterprise plans coming in the coming
days."* This didn't match either of this catalog's two prior
patterns cleanly: it wasn't a permanently invite-only research program
(Claude Mythos 5/5.1, Gemini 3.8 Flash Cyber — never admitted at all),
and it wasn't ordinary self-serve API access either (every other model
in this dataset).

**Decision (explicit, asked of the project owner rather than assumed):**
admit the model, and model the real gate honestly instead of pretending
it doesn't exist — the route used `RequirementKind.PROGRAM_MEMBERSHIP`
(`SCHEMA.md`/`decision/domain/access_route.py`), the first access
route in this catalog to actually use that requirement kind since it
was added to the closed vocabulary (Fase 7). For a developer without
Trusted Access Program membership, Access Advisor correctly reported
this route as `REQUIRES_ONBOARDING`, never `CURRENTLY_ELIGIBLE`.

A checkbox ("OpenAI Trusted Access Program") was added to the web
form's "Developer programs you're a member of" section
(`interfaces/web/templates/index.html`), alongside the existing NVIDIA
Developer Program one, so the route was actually reachable/testable.
That checkbox now has no route behind it — same open question as the
NVIDIA one (see `IMPLEMENTATION_NOTES.md`, Iteration #19, for the
disposition decided).

## Identity

| Field      | Value          |
|------------|----------------|
| `id`       | `gpt-6-astra`  |
| `name`     | GPT-6 Astra    |
| `provider` | OpenAI         |
| `version`  | `6`            |
| `license`  | `proprietary`  |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page, Modalities: "Image — Input only." |
| `audio`                | false | Model page, Modalities: "Audio — Not supported." |
| `image_generation`     | false | Native output is text-only (Modalities table lists no image output). Image generation is reachable only as a separate Responses API tool ("Image generation: Supported" under Tools) — same distinction already drawn for `gpt-5`/`gpt-5-6-sol`, not a native output modality. |
| `tool_calling`         | true  | Model page, Features: "Function calling: Supported." |
| `structured_output`    | true  | Model page, Features: "Structured outputs: Supported." |
| `json_mode`            | true  | Not itemized separately by OpenAI — same basis already used for the rest of the GPT-5.x/6 family (structured output confirmed, JSON mode not itemized as a distinct feature). Inherited/curated. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | OpenAI's own system card (`deploymentsafety.openai.com`, first-party domain): "the most capable model we have ever broadly deployed." Model page: built "for the hardest end-to-end work," covering "complex reasoning, coding, computer use, research, and document creation." Kept at the same ceiling as `gpt-5-6-sol` (already `very_high`) rather than treated as automatically superior — per `SCHEMA.md`'s evidence-based calibration principle, a newer flagship doesn't get a rating this 4-level scale has no room above just for being newer. |
| `coding`                   | `very_high` | Same system-card framing plus model page's explicit "coding" use case. Same ceiling reasoning as `reasoning`. |
| `creative_writing`         | `high`      | No creative-writing-specific claim found on either page checked. Kept at the same catalog-wide ceiling already applied to `gpt-5`/`gpt-5-6-sol` ("no OpenAI model in this dataset is rated `very_high` on creative writing yet") — not bumped just because other dimensions were. |
| `instruction_following`    | `very_high` | System card: "better aligned than GPT-5.6 Sol... stronger at respecting safety and security boundaries and staying within its authorized scope," roughly half as many higher-severity misalignment flags as Sol across 54,000+ internal Codex tasks. Direct, dimension-specific evidence — stronger sourcing than the flagship-positioning inference used for `gpt-5-6-sol`'s own rating on this dimension. |

Per `SCHEMA.md`'s evidence-based calibration principle: reasoning/coding/
instruction_following are identical to `gpt-5-6-sol`'s, deliberately —
the sourced evidence supports Astra remaining at the existing top of
the 4-level scale, not an automatic bump simply for being the newer
release.

## Languages

Not independently reconfirmed this pass — OpenAI does not publish an
explicit per-model language list. Reused the same curated set as
`gpt-5-6-sol`/`gpt-5` (same provider family), itself a curated list,
not an OpenAI-published fact (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,050,000  |
| `max_output`           | 128,000    |

Confirmed directly against the official model page: "1,050,000 context
window," "128,000 max output tokens" — identical ceiling to
`gpt-5-6-sol`. A 272,000-token input sub-limit exists within that
total (prompts above it are billed at premium long-context rates),
same style of nuance already noted for `gpt-5`/`gpt-5-mini`/`gpt-5-6-sol`.

## Cost `[Objective]`

| Field                    | Value   |
|----------------------------|---------|
| `input_per_million`         | $10.00  |
| `output_per_million`        | $50.00  |

Confirmed directly against `developers.openai.com/api/docs/pricing`
and the model's own page, standard/short-context tier. Additional
tiers not represented in the schema: cached input $1.00/M, cache
writes $12.50/M, and a premium long-context rate (2x input/1.5x
output = $20.00/$75.00) above 272K input tokens — same tiered-pricing
friction already logged in `IMPLEMENTATION_NOTES.md` Iteration #5,
standard short-context tier used here consistent with every other
entry in this catalog. Unlike `gpt-5-6-sol`, this is **not** a
time-limited introductory rate — no expiration mentioned anywhere
checked, so no `cost.effective_until`/`reverts_to` fields were added.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same API surface as the rest of the GPT-5.x/6 family — Chat Completions, Responses, Realtime, Batch, Fine-tuning, Embeddings, and the full Responses API tool set (web search, file search, code interpreter, computer use, MCP, etc.) all listed as supported on the model page. |
| `maturity`              | `stable` | Published on OpenAI's own primary model catalog and pricing pages with a full system card the same week, a stronger stability signal than this catalog's `experimental` calls for Gemini 3.7/3.8 Flash (which are still absent from Google's own model catalog page weeks after their own admissions) — see those entries' Ecosystem sections for the contrast. `maturity` here is about documentation stability, not about who can access it today; the access gate itself is modeled separately (see Access note above), not folded into this field. |

---

## Access

See the Access note at the top of this document for the full
reasoning and the 2026-09-07 update. One route: direct API,
`api_billing_linked` (ordinary self-serve, same as `gpt-5-6-sol`'s
own direct-api route) as of 2026-09-07 — was gated by
`program_membership` (Trusted Access Program) from 2026-09-04 until
then.

**Free access (`access.has_free_access`):** `false`. No free tier
mentioned anywhere checked; the model's own rate-limits table
explicitly lists "Free: Not supported."

## Sources

- [GPT-6 Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra) — capabilities, context window, max output, features, tools, rate limits; re-checked 2026-09-07, no access caveat present anymore.
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — cost fields, confirms Astra is on the standard Flagship table; re-checked 2026-09-07, the Trusted Access Program banner present on 2026-09-04 is gone.
- [OpenAI models index](https://developers.openai.com/api/docs/models) — checked 2026-09-07: GPT-6 Astra listed as the default recommended flagship, no access caveat.
- [GPT-6 Astra system card](https://deploymentsafety.openai.com/gpt-6-astra) — flagship framing ("most capable model we have ever broadly deployed"), alignment/robustness evidence used for `instruction_following`, published 2026-09-03 (first-party OpenAI subdomain).

Accessed 2026-09-04 (model admission); access route re-verified
2026-09-07. Official OpenAI documentation only, both times.

## Verification result

New dataset entry (2026-09-04). Objective fields confirmed against
official documentation. `json_mode` and `languages`/`language_quality`
flagged as inherited/curated, same recurring gap as every other OpenAI
entry. Access was initially modeled as a real gate (`program_membership`,
`REQUIRES_ONBOARDING` by default) rather than either excluding the
model outright or pretending self-serve access already existed — an
explicit decision from the project owner, not assumed. That gate was
lifted by OpenAI three days later (2026-09-07) and the route was
updated to reflect it — see the Access note above and
`IMPLEMENTATION_NOTES.md` Iteration #19.
