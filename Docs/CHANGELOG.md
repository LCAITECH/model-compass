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

Entries older than the two most recent live in
[`CHANGELOG_ARCHIVE.md`](CHANGELOG_ARCHIVE.md), moved out to keep this
file under `AGENTS.md`'s 400-line ceiling — same format, same rules,
just a continuation.

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
