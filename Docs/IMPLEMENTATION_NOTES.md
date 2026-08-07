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
