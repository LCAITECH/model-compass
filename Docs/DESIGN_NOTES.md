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

**Update:** a first visual design pass landed (see git history —
"Visual design pass on interfaces/web/"): a real type scale, a 4px
spacing scale, an expanded color palette (still one neutral
violet/indigo accent, plus semantic positive/caution/danger colors,
still nothing resembling any AI provider's brand), small inline SVG
icons for reasons/trade-offs/alternatives, and card components
grouping the result page's sections. Backend was untouched throughout.

**Update 2:** a "visual identity" pass followed (gradient background,
featured/glow card treatment for the recommendation, alternatives
rebuilt as a card grid instead of a stacked list, hero badge and
decorative blobs, wider content column, richer buttons) — see git
history, "Design polish pass" and the visual-identity commit after it.
Checked at a 375px mobile viewport for the first time this session:
no horizontal overflow, all content readable, on both the form and
result pages. Not a full responsive audit (only one breakpoint
checked), but the "never tested" gap below is now partially closed.

What's still open after that pass — smaller, more polish-grade than
the first round:

- **Responsive / mobile check** — one viewport (375px) verified with
  no overflow; tablet-width and truly small phones (<360px) still
  unchecked, as is whether the grid layouts (alternatives,
  quality-row) look intentional at in-between widths, not just
  "doesn't break."
- **Dark mode** — not attempted. The current palette was designed for
  light mode only.
- **Accessibility pass** — color contrast, focus states, and screen
  reader labelling (e.g. the SVG icons are `aria-hidden`, meaning
  their meaning currently rides entirely on the adjacent text, which
  is probably fine but hasn't been deliberately checked) haven't had a
  dedicated review.
- **Empty/loading states** — no consideration yet for what the form
  looks like mid-submit, or other micro-states beyond the three main
  screens (form, result, no-match).
- **Favicon / social preview metadata** — none set.

## Guiding principle

The interface should feel like a precision instrument for making a
decision, not a marketing landing page and not a financial dashboard.
This has been the actual criterion behind several concrete rejections,
not just a vibe: no heavy glassmorphism/blur (readability risk, and
already a dated trend), no literal "neural network / connected nodes"
illustration (the most repeated visual cliché in AI products of the
last two years, and it also fights the instrument framing directly),
restrained color saturation, no decorative motion for its own sake.
When evaluating a new visual idea, this is the question to ask first:
does it make the tool feel more like an instrument, or more like every
other AI landing page?

## Rejected explorations

**Subtle glow / three-tone "aurora" background (tried and reverted).**
A version of the visual-identity pass replaced the featured
recommendation card's strong glow/gradient treatment with a smaller,
more subtle blurred circle behind the model name, added staggered
entrance animations, and swapped the page background for a three-tone
"aurora" gradient. Committed as `f53acbc`. The user tried it and said
directly that it looked *worse* than the previous version, not
better — so it was reverted with `git revert` (`96f29b0`), not
`reset --hard`, specifically to keep a record of what was tried and
why it didn't stick. **The strong-glow treatment (`647a0ba`) is the
current, confirmed-preferred version.** Don't re-propose the subtle
orb / aurora combination without knowing this was already tried and
rejected after a direct side-by-side comparison.

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
