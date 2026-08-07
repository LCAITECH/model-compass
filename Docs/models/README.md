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
