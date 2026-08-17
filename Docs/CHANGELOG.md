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

## 2026-08-17 — Use case detection (keyword-based, not AI)

**The free-text "use case" field now actually does something — without
ever calling an AI model to read it.**

- Previously, typing a use case (e.g. "customer support chatbot") did
  nothing beyond being echoed back in the explanation text — it never
  affected which priorities got weighed. Closing that gap with an LLM
  was considered and rejected: it would make the recommendation
  non-deterministic (same input could produce different results) and
  add real, unbounded API cost per request. Silent keyword matching
  that fed straight into the ranking was rejected too — that would be
  guessing at intent and presenting it as understood fact, the same
  fabricated-confidence problem this project has declined everywhere
  else.
- Instead: a plain-rules keyword matcher (15 categories, expanded from
  the 8 existing use-case shortcuts) scans the free text as you type
  and, when there's a single clear match, suggests the priorities that
  category usually needs — shown openly ("Detected: Customer support →
  prioritize instruction following and cost") with a button to accept
  it, never applied automatically. If two categories tie, it says so
  instead of guessing which one you meant. `decision/` is untouched —
  this lives entirely in the web interface, same tier as the existing
  preset pills.
- **Crypto / trading bot** added as its own 15th category (`Cost` +
  `Reasoning`) after live testing turned up a real gap: "trading
  community with a bot" correctly produced no suggestion (by design —
  the bare word "bot" was deliberately excluded as too generic), but
  the underlying use case genuinely wasn't covered. Kept separate from
  "Telegram / WhatsApp bot" rather than folding in its keywords, since
  the two categories weigh different priorities and merging them would
  have meant guessing which one actually applies.
- **Dictionary widened** (~50 phrases across all 15 categories) after
  the user asked for the detection to get "smarter" — scoped down to
  hand-curated plurals and verb-form variants (`chatbot`/`chatbots`,
  `refactor`/`refactoring`) rather than automatic stemming, and stayed
  English-only. Same reasoning as the LLM rejection above: a stemming
  rule is less auditable at a glance than an explicit phrase list, and
  this project favors the latter every time.
- See `IMPLEMENTATION_NOTES.md`, Iteration #15 for the full rejected-
  alternatives reasoning and why this is deliberately scoped as a
  first step, not the whole feature `FEATURES.md` describes.

---

## 2026-08-13 — Gemini 3.7 Flash admitted + Gemini 3.6 Flash pricing correction

**Added the newest Google Gemini model to the dataset, and fixed a real
pricing bug found on an already-shipped one while researching it.**

- **`gemini-3.6-flash.yaml` had a stale price.** Its `cost.*` was
  $1.50/$7.50 — correct when it was loaded (2026-08-07), but Google
  quietly moved it to an introductory rate ($0.75/$3.75, reverting to
  $1.50/$7.50 on 2027-01-01) at some point before 2026-08-13. Caught
  incidentally while researching Gemini 3.7 Flash's own model card,
  which discloses 3.6 Flash's current price in its comparison
  benchmark table. Corrected; the expiration date and future value are
  documented in prose in `docs/models/gemini-3.6-flash.md` (no
  `SCHEMA.md` field exists for a time-limited price — see
  `IMPLEMENTATION_NOTES.md`, Iteration #13).
- **Gemini 3.7 Flash added** (26→27 models) — Google's newest Flash
  model, published the same day as this entry (2026-08-13), based on
  Gemini 3.6 Flash with algorithmic reasoning improvements. Same
  introductory-pricing pattern as 3.6 Flash. All `[Objective]` fields
  sourced directly against the model's official model card and the
  Gemini API's function-calling/structured-output reference docs
  (neither of which state capability flags directly on the card
  itself). `[Editorial]` fields (`quality.*`, `ecosystem.maturity`)
  set by the project, not inherited from any benchmark score or
  third-party audit — see `docs/models/gemini-3.7-flash.md` for the
  full reasoning per field. `ecosystem.maturity: experimental`,
  specifically, because the model doesn't appear yet in Google's
  public Gemini API models catalog as a labeled stable/preview entry —
  a new editorial principle (maturity requires public documentation
  evidence, not just technical availability) applied here for the
  first time.
- Added its `direct_api` access route (Google AI Studio / Gemini API),
  same pattern as the rest of the Gemini family — 60→61 routes,
  27/27 models with at least one confirmed route. `evidence.source_url`
  points to the model's own model card (model-specific confirmation of
  Gemini API distribution), not the generic Gemini API billing page —
  the billing page covers eligibility/economics mechanics only, noted
  in the route's `evidence.caveat` instead.
- Reviewed and explicitly rejected third-party AI-generated "audits" of
  official model cards as a data source, including a concrete
  counter-example: one such audit claimed a ~2M context window for
  Gemini 3.1 Pro, contradicted by that model's own official model card
  (re-fetched directly, 2026-08-13: "up to 1M"), matching this
  project's already-sourced entry — see `IMPLEMENTATION_NOTES.md`,
  Iteration #14.
- Test fixtures depending on dataset size/composition updated to match
  (`test_loader.py`, `test_explainer.py`, `test_access_loader.py`) —
  142/142 tests passing.

---

## 2026-08-13 — v0.1.0 (feature/access-catalog-expansion)

**Grew the Access Advisor catalog from 3/26 to 26/26 model coverage,
52 route files, and then found and corrected a real gap in it before
merge — 60 routes total.**

- **Closed a research + implementation-contract pass from the
  previous session** (`research/access-catalog-coverage-2026-08-12`,
  not merged, research-only per this project's convention) into
  actual dataset files, in two deliberate stages with a full test run
  and browser QA between them:
  - **23 base-pattern routes** — one `direct_api` route per model the
    v1 catalog didn't cover yet, extending the exact template v1 had
    already proven three times (Anthropic/Google/OpenAI) to the two
    providers it hadn't reached (DeepSeek, Mistral). This alone closed
    **26/26 models with at least one documented route** — a
    shippable checkpoint on its own, confirmed with the user before
    continuing.
  - **29 secondary-pattern routes** — Amazon Bedrock, Google Cloud
    Vertex AI, and Microsoft Azure AI Foundry for 9 Claude models,
    a Google AI Studio subscription route for `gemini-3.1-pro-preview`,
    and Mistral Large 3 self-hosted (open-weights, Apache 2.0, sourced
    to its real Hugging Face repository, including actual GPU
    requirements for its 675B-parameter mixture-of-experts
    architecture — the first real use of the `self_hosted` surface
    and `gpu_infrastructure` requirement kind, both already in the
    schema since Access Advisor v1 but unused until now).
  - Two new provider guide docs (DeepSeek, Mistral) and three new
    Anthropic cloud-platform sections, all sourced against live
    official documentation (AWS, Google Cloud, Microsoft Learn,
    Hugging Face) rather than this project's own `docs/models/*.md`
    prose, which only named the platforms in passing.
- **Found and corrected a real gap the closed contract's own research
  had gotten wrong, before merge — not a design change, new
  evidence.** The contract had excluded Claude Fable 5 from the
  Bedrock/Vertex/Foundry patterns as "not documented." Checking AWS's
  and Microsoft's own docs while sourcing the other 9 Claude models
  turned up Fable 5 listed on both; Anthropic's own Transparency Hub
  (`anthropic.com/transparency`) independently confirmed it across
  every surface — Claude.ai, Claude Code, the Anthropic API, Bedrock,
  Vertex AI, and Azure Foundry. Flagged to the user rather than
  silently expanded; once confirmed, added the 4 missing Fable 5
  routes plus a new `consumer_subscription` route (Claude Pro/Max,
  sourced to `claude.com/pricing`'s own comparison table — not the
  news-aggregator sourcing an earlier session's `docs/models/`
  prose had relied on, which doesn't meet this project's bar for a
  route's evidence). **Claude Code itself isn't modeled as a separate
  route** — Anthropic's own docs describe it as a client that
  authenticates via either an API key or a Claude subscription, not a
  third billing path. **MCP/Antigravity access to Claude models was
  deliberately left out** for the same reason the contract already
  excludes unconfirmed surfaces: "can be done in practice" isn't the
  bar this catalog holds itself to — "an officially documented,
  verifiable access route" is.
- Fable 5 is now the catalog's most complex access case: 5 real
  routes across 3 distinct surfaces (`direct_api`, `cloud_hosted` ×3,
  `consumer_subscription`), each with independent eligibility and
  economics — the strongest demonstration yet that Access Advisor
  answers "how do I actually reach this model, given my situation,"
  not just "does a route exist."
- New coverage-shape test (`test_access_catalog_coverage.py`) asserts
  every dataset model has at least one `confirmed` route, so future
  sessions get a loud failure instead of silently losing coverage.
- Verified two ways, not just `pytest`: directly through
  `recommend_access()` for spot-checked models across every provider
  (including the full 5-route Fable 5 breakdown), and in the real web
  UI (server restarted mid-session to pick up the new dataset) —
  Claude Fable 5, DeepSeek V4 Flash/Pro, and Gemini 3.1 Pro Preview,
  all previously "no documented access route yet," now show real
  access options end to end. The subscriptions checklist in the web
  form updated on its own (it's data-driven from the catalog) to
  include the two new Claude plans.

Tests: 141/141 (30 from Access Advisor v1 + 8 new this session).
Routes: 4 → 60. Subscription plans: 2 → 4.

## 2026-08-11 — v0.1.0 (feature/access-advisor-v1)

**Shipped Access Advisor v1 — after a recommendation, a separate "How
can you access this model?" section shows the real, documented ways to
reach it, without ranking them against each other.**

- **New subsystem, `decision/access/`, that never touches the
  recommendation.** `evaluate()`/`explain()` are unchanged; Access
  Advisor runs after them, in `interfaces/web/app.py`, and only reads
  `AIModel` — it can't import `decision/evaluator/` even by mistake,
  by design (see `Docs/ACCESS_ADVISOR_AUDIT_2026-08-11.md`).
- **Three access states, not a pass/fail gate:** a route is
  `currently_eligible` (usable now), `requires_onboarding` (needs an
  API key, a cloud account, a subscription, etc. — never hidden for
  that), or excluded entirely only when it's an enterprise-only route.
  Declaring "no AWS account" never removes Bedrock from the list — it
  just says what's needed and links to how to get it.
- **No ranking between equally-valid routes.** If a model has three
  ways to reach it (its own API, AWS Bedrock, Google Cloud), Access
  Advisor shows all of them grouped by state, never picks a "best
  cloud" — that would be inventing a preference the evidence doesn't
  support. The one exception: if exactly one *confirmed* direct API
  route exists, it's named in a short "Recommended access" summary;
  otherwise it's a neutral count with the full list one click away.
- **New dataset catalogs**, separate from `dataset/models/`:
  `dataset/access_routes/{provider}/{route_id}.yaml` and
  `dataset/subscriptions/{provider}/{plan_id}.yaml`, each entry sourced
  the same way as a model (URL, date, status) — started with 4 routes
  (Anthropic, Google ×2, OpenAI) and 2 Google subscription plans as a
  working sample, not a full catalog yet.
- **New `docs/access-guides/`** — short, curated pointers to official
  provider docs for each access method, deliberately not step-by-step
  tutorials (`VISION.md`: "does not replace official provider
  documentation").
- Access-related questions (how you'd use the model, whether you have
  billing/cloud accounts/subscriptions already) are optional fields
  added to the form — skipping all of them still gets a full
  recommendation, just without the access detail.

Full design history — including a route-ranking mechanism that was
built, discussed, and deliberately reverted before implementation —
was written up in `ACCESS_ADVISOR_AUDIT_2026-08-11.md`, an internal
research document that lives on its own research branch, not in this
tree (same policy as this project's other research docs) — the
code's own docstrings still cite it by Part number for context.

**Post-review fixes, same session, before merge to `main`:** a second
code-review pass found and fixed 4 real bugs missed by the first —
access-route rows linked to raw evidence instead of the curated
`docs/access-guides/` entry, a route's "not for production use" status
was loaded but never shown, and two dataset fields (`cloud_account`,
`documented_exclusions`) weren't validated against their expected
shape, so bad data could corrupt silently or crash the app at boot
instead of failing with a clear error. Manual QA also caught 6
dataset fields (4 route caveats, 2 subscription exclusions) that had
shipped in Spanish while the rest of the app is English-only — fixed,
with a new test guarding against it recurring. Full test suite:
139/139. **Known, deliberate gap, not a blocker:** only 3 of the 26
models in the dataset have a documented access route today (Claude
Opus 5, GPT-5, Gemini 2.5 Pro) — every other recommended model
correctly shows "no documented access route yet" rather than a wrong
answer. Widening that catalog is real, separate follow-up work, not
part of this release.

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
