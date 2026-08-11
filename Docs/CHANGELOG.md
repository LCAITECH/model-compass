# CHANGELOG.md — Model Compass

What changed, and why — in plain language. This is not a git log and
it doesn't require reading code to follow: it's the answer to "what
happened this week and why does it matter," for anyone following the
project, not just contributors.

For the technical detail behind any entry, see the linked commits. For
*why* a decision was made the way it was (not just that it was made),
see the relevant doc — `IMPLEMENTATION_NOTES.md` for schema/dataset
friction, `DESIGN_NOTES.md` for visual decisions, `docs/models/` for
why a specific model's data looks the way it does.

Entries are dated, newest first, tagged with the project version at
the time (see `pyproject.toml`) — note the version hasn't been bumped
per entry yet, since the project is still pre-1.0 and hasn't adopted a
release-per-version discipline. That may change once there's a first
public release to version against.

---

## 2026-08-11 — v0.1.0

**Shipped the Budget redesign, corrected 5 dataset calibration errors
found by a real-evidence audit, and replaced "single winner" framing
with an honest tie indicator when the recommendation is a close call.**

- **Budget is now a fixed price band, not a moving target.** Cost tier
  (Low/Medium/High/Very High) used to be computed as relative terciles
  of whatever was currently in the dataset — a model could silently
  drift between tiers just because other models were added, and "High"
  budget didn't actually cap anything (the priciest model in the
  catalog always qualified). Tiers are now fixed $/million-token bands
  anchored to real price data, with a new top band (`Very High`) so
  "High" means something again. Confirmed live: `budget=high` +
  reasoning priority used to recommend the single most expensive model
  in the dataset; it no longer does.
- **Cost's influence on the ranking now scales with how loose the
  budget is** — full weight at Low, down to 10% at Very High — but
  only when Cost isn't the developer's own #1 priority, and never at
  all under the new **Custom Budget** mode (a real dollar figure, kept
  deliberately separate from the fixed tiers: it narrows the
  affordability estimate shown after the fact, never the ranking
  itself, since doing that honestly would require assuming a token
  volume nobody provided).
- **Lower-cost Alternative stopped suggesting worse models just because
  they were cheap.** It now only proposes a cheaper option if it stays
  within one quality tier of the recommendation on the priority that
  actually matters, and says so explicitly with a side-by-side
  comparison table instead of a single "you'd save X%" line.
- **New: when two or more models are practically tied, the page says
  so.** A four-level quality scale produces real ties more often than
  not, and until now the UI still had to pick a single "winner" to
  display — via a plain, meaningless tie-break (alphabetical model id).
  Any model within 2% of the top score **and** within one quality tier
  on every dimension is now shown as an "Also strong option" alongside
  the recommendation, not silently folded into a false single-answer
  framing. The 2% threshold wasn't picked by feel — it came out of an
  audit across the full grid of every priority combination and budget
  tier this project supports, checking exactly how often a looser or
  tighter cutoff would start calling genuinely different models
  "equivalent."
- **Dataset calibration audit, evidence-based, per model, not by
  feel.** A user-reported pattern ("one cheap model keeps winning")
  turned into a full audit: every model whose quality rating had no
  real citation behind it (8 of 26) got re-sourced against fresh
  official documentation. Five ratings changed with real evidence
  behind each one — two OpenAI/DeepSeek reasoning ratings moved up,
  one Gemini instruction-following rating moved down, one DeepSeek
  capability flag corrected, and one Mistral price fixed (a stale
  $2.00/$6.00 that should have been $0.50/$1.50 — an out-of-date
  number, not an opinion). The original "cheap model dominates" pattern
  turned out not to be a scoring bug at all — controlled testing (same
  context, only the budget tier changed) showed the ranking already
  shifts in a sensible, budget-aware way; what looked like bias was
  mostly the tie-break problem above wearing a different hat.
- **A real frontend bug, found by hand-testing, fixed:** choosing
  "I know my $ budget" and submitting the form silently did nothing.
  The hidden tier dropdown was still marked required, and the browser
  blocked the submission without being able to show an error on a
  field the visitor couldn't see. Fixed with a small script that keeps
  the two budget modes' required fields in sync.

Tests: 74 → 103.

## 2026-08-10 (later same day) — v0.1.0

**Added 6 candidate models — 20 to 26 — and formalized a new rule for
how editorial quality ratings get calibrated.**

- **Six models admitted**, each fully sourced against official
  provider documentation with its own `docs/models/*.md` audit trail:
  Gemini 2.5 Flash-Lite, Gemini 3.1 Flash-Lite, Gemini 3.5 Flash,
  GPT-5.6 Sol (OpenAI's new flagship, replacing GPT-5), Claude Sonnet
  4.5, and Claude Opus 4.5. All six came out of a dedicated research
  branch (`research/model-candidates`, see
  `Docs/CANDIDATE_RESEARCH_2026-08-10.md`) done in a prior session —
  this pass was the field-by-field sourcing verification and the
  actual admission, not new candidate hunting.
- **New rule in `SCHEMA.md`/`CONTRIBUTING.md`: editorial calibration
  must be evidence-based, not family-based.** A model no longer
  inherits a lower or higher quality rating just because it's an
  older generation or a cheaper tier than a sibling already in the
  dataset — every rating needs a specific, sourced signal (a
  knowledge-cutoff gap, a stated or missing capability, explicit
  provider positioning language). Caught and corrected a real
  overreach mid-session: an early pass had degraded Claude Sonnet
  4.5's `creative_writing` rating alongside its reasoning/coding, with
  no evidence that specifically touched writing quality — fixed before
  it shipped.
- **`gpt-5-6-sol`'s id** deliberately doesn't match OpenAI's own model
  string (`gpt-5.6-sol`, with a dot) — converted to the project's
  existing hyphen convention, documented in that model's own `.md`.
- Also fixed the same day: `docs/models/deepseek-v4-pro.md`'s
  `reasoning`/`coding` justification, which had been written using
  the exact family-based reasoning the new rule now rules out. The
  rating itself (`very_high`/`very_high`) didn't change — re-checking
  against DeepSeek's own release announcement found real supporting
  evidence ("World-Class Reasoning: beats all current open models...
  rivaling top closed-source models") that the original write-up had
  explicitly declined to use. `gemini-2.5-pro.md`'s justification is
  now flagged as the weakest-sourced `very_high` rating left in the
  catalog — noted for a future pass, not touched yet.
- No changes to `decision/evaluator/`, `decision/explainer/`, or
  `interfaces/web/` — dataset and documentation only.

Tests: 68 → 74 (26-model dataset, plus new parametrized language
coverage for the 6 additions).

**Also this session, investigated but not yet implemented:** a
product audit found that `budget` (Low/Medium/High) and a
user-entered monthly dollar amount are structurally disconnected —
the dollar figure only feeds the affordability calculator, never the
recommendation itself, and budget tiers are relative to whatever's
currently in the dataset rather than fixed price bands. A redesign
(fixed price-per-token tiers, a mutually-exclusive custom-budget mode
that never assumes a token-usage volume, and a more honest "lower-cost
alternative" comparison) is designed but not built. Full detail in
`HANDOFF.md`.

## 2026-08-10 — v0.1.0

**Added DeepSeek V4 Pro to the dataset — 19 to 20 models — and closed
out two dataset-candidate investigations that had gone undocumented.**

- **DeepSeek V4 Pro.** Researched against DeepSeek's own official docs
  and its Hugging Face model repository only: 1M-token context, 384K
  max output, $0.435 / $0.87 per million tokens (input / output),
  MIT-licensed open weights. The one genuinely interesting question was
  whether it supports image input — several non-official sites claimed
  it does, but DeepSeek's own API reference, its full documentation
  index, its Hugging Face model card, and its Responses API guide (the
  most direct of the four: *"Image and file inputs are not supported...
  replaced with a placeholder text"*) all agree it doesn't. Resolved as
  a confirmed `false`, not left pending — the sourcing pattern itself
  (official docs vs. a cluster of consistent third-party claims) is
  logged as its own entry in `IMPLEMENTATION_NOTES.md`, since it's
  useful precedent for future research, independent of this model.
  Quality and ecosystem ratings were calibrated against DeepSeek V4
  Flash's existing entry (flagship vs. flash tier) — not against
  DeepSeek's own marketing language about the model, which is noted in
  the sourcing but explicitly excluded as a basis for any editorial
  rating, per this project's own rule.
- **Meta Llama and NVIDIA NIM, formally logged as closed
  non-candidates.** Both had been investigated in a prior session but
  never written down anywhere — re-verified against official sources
  before logging anything, rather than trusting the earlier informal
  conclusion. Meta retired its first-party Llama API on 2026-07-06; its
  successor product serves only its own proprietary "Muse Spark"
  models today, confirmed directly against that product's live model
  listing. NVIDIA NIM re-confirmed as a GPU-licensed hosting platform
  with no per-token pricing anywhere in its own documentation
  ($4,500/GPU/year or ~$1/GPU/hour, quoted directly from NVIDIA's own
  FAQ) — same verdict as an earlier pass, now backed by direct quotes
  instead of forum reports.
- No changes to `decision/evaluator/`, `decision/explainer/`, or
  `interfaces/web/` — this was a dataset and documentation pass only.

Tests: 67 → 68.

## 2026-08-09 — v0.1.0 (2)

**Added `has_free_access` — a strict, single-boolean answer to "can I use
this model without paying," across the whole dataset.**

- Two research passes this week (documented in `IMPLEMENTATION_NOTES.md`,
  Iteration #8) looked at whether free-access rate limits (NVIDIA NIM,
  Google's free tier, Groq, and others) could become part of the dataset.
  They can't, honestly — only one of six providers checked publishes a
  stable, official rate-limit table; the rest are dynamic per-account
  dashboards or simply undocumented. Putting raw numbers in the dataset
  would have meant presenting a Groq figure as equally solid as NVIDIA
  Developer Forum folklore.
- What survived instead: a new `access.has_free_access` field, strictly
  defined as "does an official, documented free-access path exist for this
  specific model today" — never inferred, never based on a one-time trial
  credit. Every one of the 19 dataset entries was individually checked
  against its provider's own pricing docs. Three qualify: Gemini 2.5 Flash,
  Gemini 3.6 Flash, and Gemini 3.5 Flash-Lite, all confirmed "Free of
  charge" on Google's own pricing page. Every other model — including
  Gemini's own Pro-tier releases, all Claude, OpenAI, DeepSeek, and Mistral
  entries — is `false`, most because no free path exists at all, one
  (Mistral Large 3) because a free API tier exists at the platform level but
  couldn't be confirmed for that specific model.
- Surfaced in the web interface as a secondary signal, not a headline claim:
  a small "Free access also documented" note appears next to pricing, but
  only when the developer's stated budget is Low — it never claims a model
  "is free" outright, since real-world limits still apply.
- No changes to `decision/evaluator/` or `decision/explainer/` — the field
  doesn't affect qualification or ranking, only what's displayed.

Tests: 62 → 67.

## 2026-08-09 — v0.1.0

**Accessibility, responsive, and visual design pass — no changes to the
recommendation engine or the dataset.**

- Fixed two real color-contrast failures against WCAG AA (a green text
  color and a form-input border that were both too light to reliably
  read), added a visible focus ring to every interactive element, made
  the three help tooltips reachable by keyboard, and gave two page
  sections real `<h2>` headings instead of styled paragraphs so they
  show up when navigating by heading (a common screen-reader pattern).
- Audited both pages at 340px and 768px, including the densest state
  of the result page (a budget entered, showing capacity bars and a
  savings callout) — no horizontal overflow anywhere.
- Added a favicon, a meta description, and Open Graph tags — none of
  that existed before.
- Added a "Supported models" section to the landing page, listing
  every provider currently in the dataset. The list is generated from
  the dataset itself, not hand-typed, so it grows on its own as new
  providers are added.
- A hierarchy and consistency pass on the result page: section titles
  now read as more important than small inline labels (they didn't
  before), removed a hover animation from cards that aren't actually
  clickable, and consolidated a handful of colors that had drifted
  outside the shared palette back into it.
- Rebuilt the form itself. It no longer sits inside a white card
  floating on the page — it's laid out as three numbered stages (Use
  case, Priorities, Budget) directly on the page, with a two-column
  layout on desktop instead of the previous single stacked column.
  Priorities now comes before Budget: it's the input that actually
  drives which model wins (the first priority you pick matters most),
  while Budget only filters candidates out — and moving it earlier
  puts it next to the quick-pick buttons that pre-fill it. Collapses
  back to a single column below 640px, audited the same way as above.
- None of this touched `decision/`, the dataset, or how a
  recommendation is computed — verified before and after every step
  with the full test suite and, for anything scoped as "visual only,"
  a `git status` check confirming zero Python files changed.

Tests: 62/62, unchanged in count (this pass added no new engine
behavior to test).

## 2026-08-07 — v0.1.0

**Grew the model dataset from 5 to 19 models, and made every entry
independently auditable.**

- Added `docs/models/` — one file per model in the dataset, citing
  exactly where each value came from (official provider documentation
  only, dated) and flagging anything that couldn't be independently
  confirmed as *pending* rather than presenting it as verified. Every
  one of the original 5 models was re-verified against current
  official docs in the process.
- Formalized a rule, visible in `CONTRIBUTING.md`: if a field has no
  clear official source, it doesn't enter the dataset as hard data —
  it's marked pending, and the model waits until it's fully sourced.
  Applied this literally: NVIDIA NIM, Mistral Medium 3.5, and Grok 4.5
  were all researched and none were added, because none had a
  complete official source for every required field.
- Added 14 new models across every major provider's current lineup —
  flagship, mid, and low-cost tiers — plus a deliberate test case:
  GPT-4o was added specifically to check whether the recommendation
  engine can surface "this is an older generation, consider
  migrating" using only real cost and quality data, with no special
  "legacy" flag anywhere in the system. It can — see the reasoning in
  `docs/models/gpt-4o.md`.
- Investigated models exposed through Google's Antigravity product
  (including what was initially reported as "Gemini 3.1 Pro") and
  found real problems with treating it as a source: no official
  per-token pricing, and community reports that its model labels
  don't reliably match what's actually running. None of those were
  added on that basis. Separately, Gemini 3.1 Pro *does* exist as a
  real, independently-priced model through Google's standard API —
  found on a second, more thorough pass, and added once it cleared the
  same bar as everything else.
- Every model entry now documents where it can actually be called
  from (which official API, at what price) — kept deliberately
  separate from the harder question of "does my existing subscription
  already cover this," which stays a future direction, not answered
  here.
- Cleaned up two small pieces of repeated code in the web interface
  (a repeated list-rendering pattern, one CSS rule that had ended up
  split across two files) — cosmetic only, verified in a real browser,
  nothing about how the app behaves changed.

All of the above shipped in 8 commits to `main`, all tests passing
(59/59) at every step.

**Added full ranking transparency to every recommendation.** Until
now, a qualifying model that ranked below the top 3 alternatives
simply disappeared from the result — not shown as a pick, not shown as
excluded, just gone. Every recommendation now shows:

- The recommended model's and every alternative's real rank ("#1 of
  19 qualifying models", "#2 of 19", etc.) — a true, computed position,
  not an invented confidence score. A raw match score (e.g. "80/100")
  was considered and deliberately not built: the underlying number is
  only meaningful relative to whichever models happen to qualify for
  one specific query, so the same model could score very differently
  for two different users with no change in the model itself —
  presenting that as an absolute percentage would have implied a
  precision the number doesn't have.
- Every model that qualified but didn't rank in the top 3, with a real
  rank and the actual dimensions it lost on — reordered so whatever
  the user actually prioritized shows first, not buried in a fixed
  list order. Only the top 2 reasons show by default, with the rest
  available on demand — a model can lose on five dimensions at once,
  and listing all five up front was noise, not information.
- Every model that never qualified at all, now grouped by why —
  "12 models — cost tier exceeds a 'low' budget" once, instead of the
  same sentence repeated 12 times. Distinct on purpose from the models
  above: these never entered the ranking, so they don't get a rank.

Tests: 59 → 62.
