# docs/models/ — Model Catalog

One file per model in `dataset/models/`, same `id`, same filename
(`{id}.md`). This is not a second dataset — `dataset/models/*.yaml` is
the only thing the Decision Engine reads. This folder is the audit
trail: where every value came from, and the reasoning behind every
editorial call. See [SCHEMA.md](../SCHEMA.md) for field definitions
and the Objective/Editorial distinction these files follow.

## Format

Each file mirrors `SCHEMA.md`'s categories (Identity, Capabilities,
Quality, Languages, Operational, Cost, Ecosystem), plus two sections
the YAML can't hold:

- **Sources** — official documentation URLs used, and the date they
  were accessed.
- **Verification result** — whether the dataset entry still matches
  the official docs as of that date, or what drifted.

See [`gemini-2.5-flash.md`](gemini-2.5-flash.md) for the reference
example.

Every entry also includes an **Access** section: which official,
token-priced API(s) actually serve this exact model. For the common
case — one provider, one API, matching the `cost.*` fields already in
the entry — a single sentence is enough; don't inflate it into a
section it doesn't need. It earns more space when the access story is
genuinely more complex than "call the API" — see
[`claude-fable-5.md`](claude-fable-5.md) (subscription tiers, one-time
credits, and direct API access are three different things for the
same model) or [`gemini-3.1-pro-preview.md`](gemini-3.1-pro-preview.md)
(available both through the standard API and through a separate
product, Google Antigravity, that isn't itself a valid data source —
see `IMPLEMENTATION_NOTES.md`, Iteration #6).

**This is deliberately scoped narrower than "how do I pay for this
model."** Consumer subscription equivalence (does my ChatGPT Plus or
Claude Pro plan already include this, and for how much usage) is a
separate, harder problem — tracked as "Subscription vs. API
Comparator" in `FEATURES.md`, explicitly parked because subscriptions
don't have stable per-token pricing to source honestly. The Access
section here only answers "which API can I call," not "what does my
existing subscription get me."

Since 2026-08-09, the Access section also states this model's
`access.has_free_access` value and its source — see `SCHEMA.md`'s
Access section for the strict definition. That field only says whether
a documented free path exists; the unstable detail (exact limits,
conditions) stays here in prose, never as a structured field.

## Sourcing rule

If a field has no clear official source, it is **not** written up as
confirmed data. It gets marked explicitly as pending / inherited —
e.g. "not independently reconfirmed, no official source found as of
this date" — rather than citing a source that doesn't actually say
that. This applies even when the YAML already has a value for that
field (the dataset entry isn't touched over this alone; see
`AGENTS.md`'s schema discipline — a sourcing gap is logged, not
reactively fixed). This is the same principle as "never fabricate
precision," applied to citations specifically: an invented source is
worse than an honest "pending," because it looks verified when it
isn't.

Third-party aggregators (OpenRouter, pricing trackers, etc.) are never
an acceptable source here, same rule as the dataset itself — see
[IMPLEMENTATION_NOTES.md, Iteration #2](../IMPLEMENTATION_NOTES.md#iteration-2).
