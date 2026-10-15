# DESIGN_NOTES.md — Model Compass

This document is not one of the 7 official project documents, same
status as `IMPLEMENTATION_NOTES.md`. It's a running log for UX and
visual design ideas — allowed to be informal, incomplete, and out of
date. Its only job is to keep ideas from being lost between the
functional-first phase and the dedicated design pass that follows it.

Being listed here is not a commitment to build it, and definitely not
an instruction to build it now — see the current status note below.

---

## Current status (2026-08-09)

The items flagged as open below (responsive/mobile, accessibility,
favicon/metadata) are now resolved — see the dated update at the top
of this section for detail and the reasoning behind each. Dark mode
and empty/loading states remain genuinely open. Kept the original
2026-08-06 status note below as-is, unedited, for the same reason the
"Rejected explorations" section below exists: knowing what was true
*before* a pass, and why it changed, is more useful than a silently
updated snapshot.

**Update (2026-08-09) — accessibility, responsive, and a form
redesign.** Three passes, all reviewed and approved incrementally
before implementation, all verified against the real test suite and a
live browser at each step:

1. **Accessibility + responsive audit.** Fixed two real WCAG AA
   contrast failures (a green text color, a form-input border, both
   too light), added a visible focus ring across every interactive
   element, made the three help tooltips keyboard-reachable, and
   promoted two section labels to real `<h2>` headings. Audited both
   pages down to 340px and up to 768px — no horizontal overflow
   anywhere, including the result page's densest state. Added a
   favicon and Open Graph metadata, neither of which existed before.
2. **Hierarchy and token consistency pass.** Card section titles
   (`<h2>`) now read as more important than small inline labels — they
   didn't before, both used the same small-caps muted treatment.
   Removed a hover-lift animation from cards that aren't actually
   clickable (a false affordance). Consolidated four colors that had
   drifted outside the `:root` token system back into it.
3. **The form redesign — the bigger one.** The form no longer sits in
   a white card floating on the page. It's now three numbered stages
   (`01 Use case`, `02 Priorities`, `03 Budget`) laid directly on the
   page canvas, two-column on desktop. See "Guiding principle" and the
   new subsection below for the reasoning and what was deliberately
   left out.

All three passes: zero changes to `decision/` or the dataset, 62/62
tests passing throughout.

### The form redesign, in detail

**The actual problem wasn't "the form isn't pretty enough."** It was
structural: a single stacked column of label-above-input inside a
white card is the generic shape of every SaaS signup form on the
internet, independent of how polished the CSS is. No amount of color
or shadow tuning fixes that — the fix had to be composition, not
decoration. This is now written down as a standing rule in `AGENTS.md`
("Visual polish is not always 'add more'") specifically so this
diagnosis doesn't have to be rediscovered next time.

**What changed:** the card wrapper is gone — the form sits on the page
canvas, split into three `<section>`s with real numbered headings.
Priorities moved ahead of Budget (previously Budget came first): the
priorities ranking is what actually drives the Evaluator's output
(first priority weighs most), Budget only filters candidates out, and
placing Priorities right after Use Case puts it next to the pill
buttons that already pre-fill it (`form.js`) — a relationship that
existed in the code before this pass but wasn't visible in the layout.
Desktop gets a two-column field layout (label column, control column)
using the extra width the page now has; collapses to the original
single stacked column below 640px.

**Depth without shadows.** Canvas (`--bg`) and form inputs
(`--input-bg`, new token) now sit at two distinct, deliberately close
values instead of both defaulting to white — the same recessed-fill
technique the result page's `.stat-card` already used against its
parent `.card`. Border and text contrast were recomputed against the
new values to keep the WCAG margins from the accessibility pass intact
(`--border-strong` moved from `#8f8f99` to `#87878f` specifically for
this reason — a lighter canvas would have quietly regressed the 3:1
UI-component contrast fixed one pass earlier).

**Explicitly considered and rejected, again:** glow, gradients beyond
what already existed, glassmorphism, drop shadows, decorative
animation. Not because they were untried — because the "instrument,
not a landing page" framing (see Guiding principle below) already
answers whether they belong, and the answer is still no. A technical
micro-label pattern ("`INPUT`", "`CONTEXT`", "`CONSTRAINT`" next to
every field) was proposed and scoped down to exactly one instance (a
"Rank" label next to the Priorities badges, where it explains a real
1/2/3 sequence) instead of applied broadly — the risk flagged at the
time was that scattering that vocabulary everywhere starts reading as
a backend admin panel, not a developer tool.

## Original status note (2026-08-06)

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

## Catalog notices (2026-10-14)

Badges, a floating dock on the result page and a "catalog radar" on the
landing page, in the immersive language of Phase 17 (glass panels,
sweeping gradient borders, motion only with the effects switch on).

- **Three tones, one per kind of fact**, used everywhere the fact
  appears: cyan/violet for a new release, gold for an introductory
  price, rose for a model leaving the catalog (`badges.css` holds the
  tokens; `notices.css` and `radar.css` reuse them).
- **Numbers are day counts only.** No progress ring or bar: a bar needs
  a total (how long the promo lasted, when the deprecation was
  announced) that providers don't publish consistently.
- **The dock never keeps covering the result.** It enters after the
  reveal, folds into a handle after ~9 s (or at once on phones), and
  stays open while the pointer is on it. A first version that stayed
  open sat on top of the decision graph's centre, the one thing the
  page is about.
- **Badges wrap on phones** instead of widening the page (a long "Intro
  price" badge pushed a 375 px viewport to 393 px before that).

## Model comparator, rebuilt (2026-10-14)

The owner picked every improvement on a list grounded in the old page
(a plain four-select table, about 3,700 px tall, a third of its rows
identical across models).

- **One color per picked model** (`--series-1..4` in `compare.css`,
  indigo, cyan, pink, orange; darker in light theme), the same on its
  chip, column, card, constellation and orbit node, so a model reads as
  one thread down the page. Amber and green were avoided: they already
  mean "promo" and "good".
- **Columns as cards, header pinned.** A real `<table>` with
  `border-spacing` gaps and per-column tints. The old wrapper with
  `overflow-x: auto` silently broke `position: sticky`; on wide screens
  the table now fits, and below 760 px it is replaced by one swipeable
  card per model built from the same data.
- **Orbit, not podium heights.** The engine's verdict uses the decision
  graph's rings (every catalog model on its ring, the picks lit and
  numbered), plus the picks listed in the engine's order. Step heights
  proportional to rank were rejected: they would draw a continuous scale
  the engine doesn't have.
- **Constellations are discrete.** Four axes, four fixed rings; a vertex
  always sits on a ring. Small multiples (one per model, the others as
  dashed outlines), not one overlaid chart, because identical profiles
  would hide each other. The caption says the shape is not a score.
- **Bars only relative to the picked models,** never to a maximum, plus
  an exact price ratio ("20×").
- **Learned the hard way:** every stylesheet loads on every page, so a
  generic class collides. `graph.css` reverses animations on `.ring-out`;
  the podium steps that reused that class finished invisible. The
  comparator's ring classes are `on-*` and its keyframes `cmp-*`; grep
  `static/*.css` before naming a new class.

## Subscription or API page (2026-10-15)

- **Two paths and a node.** The API on the left, measured (two token
  bounds as bars whose lengths are their real ratio, an animated stream
  inside them); the plan on the right, in fog. The fog is the data: no
  provider publishes a plan's limit in tokens, so the page draws that
  absence instead of a number. Only what the provider does publish sits
  on top of it (price, its own "5x Pro" wording, included API credits).
- **Solid beam on the API side, dashed on the plan side,** meeting at the
  verdict orb, whose color follows the verdict (cyan for the API,
  violet for the plan, accent when there is no cost verdict).
- **Included credits are green** (`--positive`), the one place a plan
  carries a number of tokens: what its API credits buy at list prices,
  which is exact.
- **"Existing users only" is neutral grey,** not the rose of a model
  leaving the catalog: Google says those models are not deprecated.

## Error pages, the phone header and measured debt (2026-10-15)

A pass over the visual debt left open since August, scoped by the owner:
error and empty states, the README screenshots, the canvas cost and an
emulated phone audit.

- **Error pages in the site's language.** An unknown URL and a GET on
  `/recommend` (opening a result in a new tab, sharing its link) answered
  with FastAPI's raw JSON. Requests that accept HTML now get a page that
  reuses the "no match" block (eyebrow, heading, one line, a link back to
  the form), no new styles; `/recommend` without a form redirects to the
  form, since a result has no URL of its own. `fetch()` callers keep the
  JSON. A 500 gets the same page without the exception text.
- **The header on phones was a layout problem, not a styling one.** The
  header grid put the brand beside four actions; at 375 px the actions
  took 265 px, the brand wrapped word by word and the theme toggle sat
  off-screen (horizontal scroll). Under 640 px the two toggles now share
  the brand's row and the two links take a row of their own
  (`.header-actions` becomes `display: contents`, the links sit in a
  `<nav>`). Desktop is unchanged, checked by position.
- **Emulated audit, no device.** Landing, result, `/compare` with four
  models and a context, `/plans` with a model, and the 404 page, at 340,
  375 and 768 px: no element wider than the viewport once the entrance
  animations finish (the browser pane freezes them at time 0, which
  reads as overflow if not finished first). Not tested on a real phone,
  Firefox or Safari; the CSS nesting in `landing.css`, `reveal.css` and
  `graph.css` still needs 2023-or-newer browsers.
- **Canvas cost, measured where it can be.** The landing's field (120
  nodes, a 1600x1000 backing store at DPR 1.25) costs 0.18 ms of script
  per frame on average, 0.30 ms at p95, against a 16.7 ms frame. The
  pane was hidden, so rasterisation and real frame rate could not be
  measured, and nothing ran on a slow device. The loop already stops when
  the tab is hidden and when effects are off. No change.
- **Empty states that already worked:** `/compare` with fewer than two
  models (slots and the picker) and `/plans` without a model. The
  result's "no match" state is unreachable with today's catalog: every
  language and budget leaves at least one model.
- **README screenshots** were from 2026-08-13, before Phases 16-17.
  Retaken from the browser pane (its capture tops out near 800 px wide,
  so they are taken at a 960-1100 px viewport and cropped), plus the
  comparator and `/plans`.

- **The decision graph's dots can be read now (owner request).** The
  rings spin, so a dot slid out from under the pointer within a second or
  two and its hover tip vanished; on a phone there was no way to read a
  dot at all, and clicking left the page for `/compare`. A click, tap or
  Enter now opens a card beside the dot that stays until ×, Escape or a
  click elsewhere: what the ring means ("Practically tied with the
  winner", "Excluded for your context"), place, price, dated notices,
  every reason (the tip showed two), and "Compare with {winner}". The
  rings stop while a card is open or the pointer is over the graph, and
  the chosen dot is outlined. Excluded dots open a card too, with the
  reason they were excluded. The card is anchored to the dot (it can
  stay there because the ring is stopped) and flips below it near the
  top edge (`graph-card.css`).
- **Found while building it:** since the `/plans` link was added to the
  result (Phase 19), the graph's "click to compare" built a `/plans` URL,
  because it took the first `a.compare-link` on the page. It now picks
  the link by its destination.

Seen and left for the full audit: route caveats are written as audit
notes ("primary evidence.source_url", "see docs/models/...") and the
result shows them to users as they are; with effects on, the
"calculating" overlay holds the form for 3.3 s although the answer takes
milliseconds (a Phase 17 decision); the ChatGPT plan table served in
Spanish marks GPT-6 Luna, GPT-6.1 Sol and Astra as "Limitado" on Plus
while their routes quote "Yes" from the English page.

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
