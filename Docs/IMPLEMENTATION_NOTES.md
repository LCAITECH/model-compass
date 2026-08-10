# IMPLEMENTATION_NOTES.md — Model Compass

This document is not one of the 7 official project documents. It is a
running log of friction discovered while implementing against
`SCHEMA.md` and `ARCHITECTURE.md`. It is allowed to be incomplete,
informal, and out of date — its only job is to keep observations from
being lost until there's enough evidence to act on them.

An observation here does not mean the schema or architecture is wrong.
It means something was noticed. Most observations should stay
observations. A schema or architecture change is a separate, deliberate
decision made in `SCHEMA.md` / `ARCHITECTURE.md` directly, only after a
pattern repeats — not on the first, second, or even third occurrence in
isolation.

---

## Iteration #1

**Observation**
Several providers (OpenAI, Anthropic, DeepSeek) don't publish an
explicit language list. Curated a reasonable list from public docs
and practical usage in those 3 cases.

**Current decision**
No schema change. Treat as a documentation/process gap, not a
schema gap — `languages` as a field is correct; what's missing (if
anything) is guidance for contributors on this edge case.

**Status**
Observation only. Review after ~20-30 dataset entries, once we can
tell a real pattern from a coincidence of which providers we loaded
first.

---

## Iteration #2

**Observation**
Third-party pricing/spec aggregators (OpenRouter, pricepertoken,
llm-stats, etc.) frequently mix up model versions — e.g. surfacing
GPT-5.4 figures under a GPT-5 search, or Mistral Large 2 figures under
"Mistral Large". Only the provider's own docs could be trusted to
identify which version was actually being described.

**Current decision**
No schema change. This isn't a gap in what fields exist — it's a
sourcing discipline problem. `SCHEMA.md` and `CONTRIBUTING.md` already
say objective fields must come from official provider documentation;
this is a data point confirming why that rule exists, not a reason to
add a new one.

**Status**
Observation only. Worth revisiting only if it turns into a recurring
contributor mistake once external Pull Requests start landing (Phase
5, Community & Governance) — at that point it might warrant an
explicit callout in `CONTRIBUTING.md` about not trusting aggregators.

---

## Iteration #3

**Observation**
`operational.max_output` is not always documented as a distinct,
explicit number. Some providers report it plainly (OpenAI, DeepSeek);
others report a context window without separately confirming the true
output ceiling, so it had to be inferred as equal to the context
window from what the model card actually stated (e.g. Mistral Large
3).

**Current decision**
No schema change. The field definition is correct; this is a
data-collection nuance (objective fields sometimes need reasonable
inference from adjacent published facts, not always a direct lookup)
rather than evidence the field is wrong or missing something.

**Status**
Observation only. Revisit if this inference pattern becomes common
enough that `SCHEMA.md` should say explicitly how to handle it.

---

## Iteration #4

**Observation**
Two of the five example models from `HANDOFF.md` had drifted by the
time they were actually loaded: DeepSeek V3 is no longer served by
DeepSeek's API (replaced by V4), and Mistral Large is now Mistral
Large 3 — Apache 2.0 / open-weights, not proprietary as the original
example assumed.

**Current decision**
No schema or architecture change. This is catalog drift, not a schema
gap — the schema handled both substitutions (DeepSeek V4 Flash,
Mistral Large 3) without any friction. It's a preview of an ongoing
reality: `dataset/` entries and even example model choices in docs
will keep drifting out from under the project over time.

**Status**
Observation only. Confirms the value of the planned dataset-update
pipeline noted in `HANDOFF.md` ("Ideas anotadas pero explícitamente NO
comprometidas todavía") — not an argument to build it now.

---

## Iteration #5

**Observation**
`cost.input_per_million` / `cost.output_per_million` assume one price
per model, but real provider pricing is frequently more granular than
that. This has now shown up independently at least three times:
Gemini 2.5 Flash prices audio input separately from text/image/video
input ($1.00/M vs $0.30/M); Claude Sonnet 5 has distinct 5-minute and
1-hour prompt-caching write rates plus a cache-hit rate, on top of base
input/output pricing; and Gemini 2.5 Pro charges a materially different
rate above a 200k-token prompt threshold ($2.50/$15.00 vs $1.25/$10.00).
In every case, the dataset entry uses the standard/base-tier price a
typical first request would hit, and the more granular real pricing is
documented in that model's `docs/models/*.md` file, not silently
dropped.

**Current decision**
No schema change yet, per this file's own discipline (2-3 independent
occurrences before proposing one) — this is the third, so it's now
explicitly on the table rather than a coincidence. Options if this
keeps happening as more models are added (not decided, just named for
whoever picks this up): (a) keep `cost.*` as a single "typical" price
and treat the granularity gap as `docs/models/`'s job, which is what's
happening today by default; or (b) add an optional `cost.notes` free-text
field to `SCHEMA.md` for exactly this kind of nuance, so it's visible
from the YAML itself and not only from the audit-trail doc. Not
proposing (b) yet — raise it with the project owner before acting on
it, per `AGENTS.md`.

**Status**
Observation, now with three independent occurrences. Worth an explicit
decision (not necessarily a schema change) next time schema/architecture
gets a deliberate look, rather than staying an open-ended "watch this."

---

## Iteration #6

**Observation**
Models surfaced through Google Antigravity (an IDE/agent product, not
the public Gemini API) — specifically "Gemini 3.1 Pro" and
Claude Sonnet 4.6 / Opus 4.6 "(thinking)" — don't cleanly meet the
model admission criteria in `CONTRIBUTING.md`. Two separate problems,
not one: (1) Antigravity's own docs (`antigravity.google/docs/models`)
don't publish per-token pricing at all, only subscription-tier rate
limits (Free/Plus/Pro/Ultra/Enterprise) — there's no objective number
to put in `cost.*`. (2) A thread on Google's own AI Developers forum
claims Antigravity's model labels don't reliably match what's actually
deployed (e.g. a labeled "Gemini 3 Pro" allegedly actually being
"Gemini 2.0 Flash" under the hood) — unverified, but exactly the kind
of reliability problem the "official docs only, no aggregators" rule
exists to guard against, even though Antigravity is Google's own
product. Separately: "(thinking)" isn't a distinct model on Anthropic's
own API — it's the `thinking.type: "enabled"` request parameter,
confirmed against Anthropic's official models table. Sonnet 4.6 and
Opus 4.6 *do* qualify on their own (see the dataset additions in this
same pass), just not as "-thinking" variants.

**Current decision**
No schema change. Not a schema gap — it's a sourcing gap, same
category as Iteration #2 (aggregators). These stay out of the
dataset until Google publishes real per-token pricing for
Antigravity-exposed models through an official channel, or until the
labeling-accuracy concern is resolved by a source better than one
forum thread.

**Status**
Observation only. Revisit if Google ever ships Antigravity models
through the standard token-priced Gemini API, which would make this
moot.

---

## Iteration #7

**Observation**
Two more models researched this pass didn't clear the admission bar,
plus one non-model that shouldn't be researched as one:

- **NVIDIA NIM** isn't a model at all — it's an inference-serving
  platform (like Bedrock, Vertex AI, or Antigravity) that re-hosts
  other providers' models (Llama, Mistral Large, and ~140 others) as
  hosted endpoints or self-hosted containers. Confirmed via NVIDIA's
  own developer docs. Nothing to add under this name; if a specific
  model NIM happens to host isn't already in the dataset, that model
  (e.g. a Llama release) is the right thing to research, not "NIM."
- **Mistral Medium 3.5** is real (confirmed via `docs.mistral.ai` and
  `mistral.ai/news`), but every pricing number findable for it came
  from third-party aggregators (OpenRouter, artificialanalysis.ai,
  pricepertoken.com, others) — explicitly disallowed as a source for
  `[Objective]` fields. Mistral's own model-card URL for it
  (`/models/model-cards/mistral-medium-3-5`) 404s, and the official
  pricing page only gives a worked example for Mistral Large, not
  Medium 3.5 specifically.
- **Grok 4.5** (xAI) has an official, sourced context window (500,000
  tokens) and pricing (tiered above/below 200k tokens — a fourth
  independent instance of the Iteration #5 friction), but **no
  official source states `max_output`**, checked across both the
  model-specific page and the general models listing. `SCHEMA.md`
  requires every operational field, so this one field being unsourced
  blocks the whole entry, even though everything else about it is
  confirmed. Also noted, not fully resolved: the model's own docs page
  referred to the provider as "SpaceXAI" rather than the commonly known
  "xAI" — possible rebrand, possible page error, not chased down
  further this pass.

**Current decision**
No schema change — this is the admission-criteria policy from
`CONTRIBUTING.md` working exactly as designed. Neither model enters
`dataset/models/` until the missing objective field has an official
source.

**Status**
Pending. Revisit Mistral Medium 3.5 if Mistral publishes its own
pricing page entry. Revisit Grok 4.5 if xAI publishes a max-output
value, and resolve the "SpaceXAI" naming question at that point too.

---

## Iteration #8

**Observation**
A dedicated research pass (2026-08-09, prompted by the NVIDIA NIM
investigation in Iteration #7) looked at free/no-cost access paths
across six providers — NVIDIA NIM, Google Gemini, Anthropic, OpenAI,
DeepSeek, Groq — to see whether "free access" could be represented as
an objective schema field (e.g. `rpm`/`tpm`/`rpd` limits). It can't, at
least not as raw numbers, and the reason itself is the useful finding:

- **Groq** publishes a real, stable, per-model rate-limit table on its
  own docs (`console.groq.com/docs/rate-limits`) — the one case where a
  citable official number actually exists.
- **Google** explicitly does *not* publish a fixed table for the
  interactive API — its own rate-limits page states limits "depend on
  a variety of factors... can be viewed in Google AI Studio" and
  points to a dashboard, not a static doc. Any "5 RPM for Pro" figure
  in circulation comes from aggregators re-describing that dashboard,
  not from Google.
- **NVIDIA NIM** never publishes a rate-limit number anywhere in its
  own docs (`docs.api.nvidia.com/nim/docs/product` — checked directly,
  no mention at all). The "~40 RPM" figure that circulates is NVIDIA
  Developer Forum folklore, informally acknowledged by NVIDIA staff as
  "dependent on model, use-case, and current traffic" rather than a
  fixed guarantee. Confirmed independently by the project owner's own
  account dashboard, which does show "Up to 40 rpm" — real, but a
  per-account, logged-in view, not a public documented fact the way
  `SCHEMA.md`'s `[Objective]` fields require (sourced from public
  provider documentation, reproducible by anyone).
- **Anthropic** confirms in its own docs that new accounts get "a small
  amount of free credits" but deliberately never states the figure
  (commonly reported as $5 by third parties). No continuous free tier,
  trial only.
- **OpenAI**'s current docs mention a "Free" tier at "$100/month" for
  users in allowed geographies, which contradicts older third-party
  reports of a one-time $5 credit — ambiguous enough that it wasn't
  chased further this pass.
- **DeepSeek** confirms no free tier at all, anywhere in its official
  pricing docs.

Knowledge-cutoff dates came up in the same discussion: Llama 3.1 (Dec
2023) and GPT-OSS-120B (Jun 2024) — both official model cards — are
genuinely older, but that's a property of *those specific* open-weight
models being older, not a property of "NIM" or "free access" as a
category. DeepSeek V4 Pro, also hosted on NIM, has an April 2026
cutoff. Free/cheap access and stale cutoff correlate for older
commodity open-weight releases, but it isn't a rule of the hosting
platform.

**Current decision**
No schema change. Putting raw `rpm`/`tpm`/`rpd` numbers into `SCHEMA.md`
would violate the project's "never fabricate precision" principle for
5 of the 6 providers checked — citing a Groq number next to a NVIDIA
forum number next to a Google dashboard snapshot would misrepresent
all three as equally solid facts, when they aren't.

What was proposed instead, for the project owner to decide on
explicitly (not applied yet, per this file's own discipline of raising
before editing): a single boolean, `has_free_access`, with a
deliberately narrow definition — *"there currently exists an official,
documented way to use this specific model without paying for API
usage, even if rate-limited or otherwise restricted."* `true` only
when a specific model has demonstrable official free access (Groq's
documented free-tier models, Google AI Studio's free-tier models);
`false` by default, including for Anthropic (one-time trial credit
isn't continuous free access) and for any model where free access is
suspected but not officially confirmed — never `true` by inference.
This is a "does a documented path exist" fact, not a "how generous is
it" fact — the unstable part (exact limits, how long they last, what
conditions apply) stays out of the schema entirely and continues to
live in `docs/models/*.md`'s existing "Access" section, in prose, the
same place subscription-vs-API nuance already lives.

Proposed downstream use, also not implemented: `has_free_access` as a
*secondary* signal for `budget=LOW`, not a replacement for `cost_tier`
— e.g. surfacing "also has documented free access" alongside a
qualifying cheap model, never claiming a model "is free" outright
(which would misrepresent rate-limited access as if it were
unconditional).

Separately, NVIDIA NIM raised a genuinely different question that
doesn't fit this proposal at all: self-hosted / infrastructure-based
cost (GPU requirements → GPU-hour pricing → operational cost), which is
a different shape of data than token pricing entirely. Logged as its
own future direction in `FEATURES.md` ("Planned Capabilities") instead
of folded into this one, since mixing the two would force an API-shaped
cost model onto something that isn't priced per token at all.

**Status**
Proposal documented, not decided. Needs the project owner's explicit
go-ahead before touching `SCHEMA.md`, any YAML, or `decision/` — this
file's job is to keep the reasoning from being lost until that
decision happens, not to make it.

---

## Iteration #9

**Observation**
Meta Llama was researched as a dataset candidate (2026-08-10). Meta's
official developer docs (`llama.developer.meta.com/docs/llama-api-deprecation`
— confirmed via search-engine indexing, quoting the page directly:
*"Meta is winding down Llama API on July 6, 2026, which has remained in
public preview since launch. On that date the service shuts down and
API requests will return a sunset response with redirect guidance."*)
state the first-party Llama API was retired on **2026-07-06**.

Direct confirmation of the current state: Meta's docs domain was
restructured into "Meta Model API" (`ai.developer.meta.com`), the
successor product. Its live Models page
(`ai.developer.meta.com/docs/models`, fetched directly 2026-08-10)
lists exactly three models — `muse-spark-1.1`, `muse-spark-1.2`,
`muse-spark-1.2-contributor` — all from Meta's proprietary "Muse Spark"
family. The page shows only Muse models and does not list any Llama
model. Llama weights remain downloadable, and are servable only
through third-party hosts (AWS Bedrock, Google Cloud Vertex AI, Azure
AI, Groq, Together AI, Fireworks AI) — which fall under the same "no
aggregators/third-party rehosts" rule that already blocks other
candidates (Iteration #2).

**Current decision**
No schema change. This isn't the usual "no official source found yet"
gap — Meta operated a first-party API, discontinued it, and replaced
it with a product that serves a different, proprietary model family
instead. Llama doesn't enter `dataset/models/` on this basis.

**Status**
Closed unless Meta reintroduces first-party, token-priced Llama
access. If revisited, re-check `ai.developer.meta.com/docs/models`
directly — this is a fast-moving product surface (it already changed
URL structure and model lineup once during this research).

---

## Iteration #10

**Observation**
NVIDIA NIM was re-investigated (2026-08-10) against its own official
docs, fetched directly:

- **Day 0** (`docs.nvidia.com/nim/large-language-models/2.0.3/about-nim-llm/nim-offerings.html`):
  *"NIMs that are validated to be functional on a small set of NVIDIA
  GPUs and published within about 72 hours"* of a model's release.
  Free, aimed at experimenting with newly released models.
- **Certified** (same page): *"supports broad compatibility across the
  NVIDIA hardware installed base, documented refresh cadence, CVE
  handling"* — requires an NVIDIA AI Enterprise license. Aimed at
  production/regulated use.
- **Pricing**, quoted verbatim from NVIDIA's own FAQ
  (`docs.api.nvidia.com/nim/docs/faq`, fetched directly): *"NIM is
  available through a license of NVIDIA AI Enterprise for $4500 per
  GPU per year or $1 per GPU per hour in the cloud."*
- **No per-token pricing exists anywhere in NVIDIA's own docs**,
  confirmed explicitly by the same FAQ: *"Pricing is based on the
  number of GPUs, not the number of NIMs."* Checked specifically for
  the hosted `build.nvidia.com` endpoints too — NVIDIA's own docs
  describe only free access via the NVIDIA Developer Program for
  prototyping, no token-priced tier.

**Current decision**
No schema change — confirms the same verdict as Iterations #7 and #8,
now backed by direct quotes from NVIDIA's own docs rather than forum
reports. NIM is a GPU-licensed infrastructure platform, not a model
with a price per token — a fundamentally different data shape than
`cost.input_per_million`/`output_per_million`. Already logged as its
own future direction in `FEATURES.md` ("Self-Hosted / Infrastructure
Cost," Planned Capabilities).

**Status**
Closed as a dataset candidate under this name. Note for whoever reads
`FEATURES.md`: its "Self-Hosted / Infrastructure Cost" entry currently
cites this investigation as "Iteration #8" — that's the Free Access
iteration, not this one. That cross-reference is stale and should
point here instead (not corrected in this change — flagged for a
separate, explicitly-approved edit to `FEATURES.md`).
