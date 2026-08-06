# DESIGN_NOTES.md — Model Compass

This document is not one of the 7 official project documents, same
status as `IMPLEMENTATION_NOTES.md`. It's a running log for UX and
visual design ideas — allowed to be informal, incomplete, and out of
date. Its only job is to keep ideas from being lost between the
functional-first phase and the dedicated design pass that follows it.

Being listed here is not a commitment to build it, and definitely not
an instruction to build it now — see the current status note below.

---

## Current status (2026-08-06)

The functional-first phase is essentially done: the full flow (form →
recommendation, including edge cases like no qualifying model) works,
is tested, and has already absorbed several rounds of real usage
feedback — see the git history from today for what that included
(readable language names, predefined use cases, honest pricing and
affordability figures, narrative reasons, per-alternative "choose this
if" reasoning, content reordering).

What's genuinely still open, not yet started, and is real visual
design work (not content/logic):

- **Typography** — currently system font stack only, no real type
  scale decisions made.
- **Spacing / layout rhythm** — currently ad hoc per-element margins,
  no consistent spacing scale.
- **Color palette** — currently one placeholder neutral accent
  (violet/indigo), chosen only to avoid resembling any AI provider's
  brand color. Not a considered palette yet.
- **Iconography** — none in use today beyond a plain "ⓘ" tooltip
  glyph.
- **Card / component treatments** — result sections are plain
  `<div>`/`<ul>` blocks with minimal borders; no considered visual
  hierarchy beyond heading levels.

## Explicitly out of scope for this document

Ideas that sound like design but are actually product/architecture
decisions belong in `FEATURES.md` (if parked) or a real discussion (if
being built), not here:

- **Recommendation History** — requires a persistence layer that
  doesn't exist anywhere in the current architecture (the whole system
  is stateless today), plus an unresolved reproducibility question
  (does a shared link re-evaluate against the current dataset, or
  snapshot the dataset version at share time?). Already tracked in
  `FEATURES.md` as a long-term direction, explicitly not near-term —
  don't let it get swept into a "quick UX pass" because it sounds
  simple. It isn't.
- **Subscription vs. API Comparator** — tracked in `FEATURES.md`. Needs
  its own schema/domain work before any UI exists for it.
