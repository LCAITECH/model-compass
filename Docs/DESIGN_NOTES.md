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

**Update 3:** third design-only pass — toned down the featured-card
glow (the first version, card gradient + strong colored shadow + badge
+ giant title, read as "too much" per direct feedback: "más que eso
puede empezar a parecer publicidad"), replaced it with a single small
blurred orb behind the recommended model's name instead. Added a third
background gradient tone (aurora-style, still restrained), staggered
the page-section fade-in instead of animating the whole page as one
block, animated the quality-profile segments filling in on load,
alternating background bands inside the form card, and bigger (22px)
directional icons on the pricing stat cards. Adopted a guiding design
principle from this round worth remembering for future passes: the
interface should feel like a precision instrument for a decision
("radar de decisión"), not a marketing landing page or a financial
dashboard — favor short, functional motion and restraint over density
of effects.

**A v2 idea, explicitly not for this version** — a background accent
tint that shifts based on which model gets recommended (e.g. a
different subtle color pairing for a Gemini vs. a Claude vs. a
DeepSeek result), with no logos or provider branding, just a
color-only "this result feels different" cue. Interesting and
low-risk architecturally (interfaces/web/ reading which model won and
picking a tint is presentation-only, decision/ still never touches a
name) — but real work: needs a considered color mapping across the
whole dataset, not just the 5 models on hand today, so it wasn't
started now.

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
