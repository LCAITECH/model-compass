# CATALOG_BOT.md — contract for the catalog bot

The catalog bot audits the official pages of the providers in this
catalog and, when something changed, opens one pull request with the
change applied, for the project owner to review. It never merges.

Read this file from `origin/main` at the start of every run, before
anything else. It changes in the same commit as the schema, so any
older copy (a pack, a note, your own memory of a previous run) is out
of date by definition. If your standing instructions disagree with this
file, this file wins, and the PR says where they disagreed.

`Docs/SCHEMA.md` is the full specification of every field and
`Docs/CONTRIBUTING.md` the general contribution rules. This file adds
what is specific to an automated run and what has broken bot PRs before.

## 1. Start from what is on `main`, every run

- Fetch `origin/main` fresh and branch `bot/catalog-YYYY-MM-DD` from it.
  Never start from an older bot branch, a local copy or a pack.
- Compare every finding against the file on `origin/main`, not against
  your previous report. If `main` already holds the value, drop the
  change and list it under "Already on main" in the PR body, one line
  each, so the review can see it was checked.
- A model is new only if `dataset/models/{id}.yaml` does not exist on
  `main`. Before proposing one, search `Docs/IMPLEMENTATION_NOTES.md`
  for its name: if an iteration recorded it as not admitted, propose it
  again only with new evidence that answers the reason given there, and
  quote that reason in the PR.
- A value that its YAML comment or an iteration explains as an owner
  decision is not drift (section 9). Don't change it. If the provider's
  page now contradicts it, raise it under "Owner decision needed".
- At most one open bot PR. If the previous one is still open, add the
  new work as commits on that same branch and add a dated section to its
  description. Two bot PRs that both add entries to `Docs/CHANGELOG.md`
  and `Docs/IMPLEMENTATION_NOTES.md` always conflict.
- Skip everything listed under "Owner work in progress" at the end of
  this file.

## 2. Sources

- Objective fields come only from the provider's own pages: docs,
  pricing, model pages and cards, deprecations, release notes, and its
  official blog when the docs don't carry a price. A cloud route comes
  from that cloud's own docs (AWS, Google Cloud, Microsoft).
- Never a source: aggregators (OpenRouter, pricing trackers), AI-written
  summaries or audits (yours included), forums. They are tips to go and
  check, nothing more (Iterations #2, #14, #16).
- Every changed value cites the URL it was read from, in the YAML
  comment and in the PR's table. A lifecycle status or date quotes the
  provider's exact words.
- A field with no official source keeps the model out. Never fill a gap
  with a guess, a sibling model's value or a placeholder.

## 3. A new model entry

Every key in `SCHEMA.md`, nothing extra. These are the ones that have
broken PRs before:

- **`lifecycle`**, all four keys, `null` allowed, dates quoted:
  `status` (`active`, `deprecated` or `restricted`), `release_date` (the
  provider's date of first API availability, never a snapshot date read
  off the id), `shutdown_date` (a specific published date, never a "not
  sooner than" floor), `replacement` (the id of a model in the dataset,
  or `null`). A missing key fails the loader.
- **`operational.max_output`**: an integer, or `null` when the provider
  publishes no output ceiling. Never the context window, never an
  invented number (Iteration #26).
- **`cost.*`** is the current price. An introductory price with a
  published end date also gets `cost.effective_until` and
  `cost.reverts_to`, both or neither. With prices by prompt length,
  store the tier a typical first request hits and describe the other in
  `Docs/models/{id}.md` (Iteration #24).
- **`access.has_free_access`** is `true` only with an official,
  continuous way to use that exact model without paying for API usage
  (`SCHEMA.md`, Access). A one-time credit is not one.
- **Editorial fields** (`quality`, `language_quality`, `ecosystem`) are
  judgment: evidence-based, never copied from a sibling or derived from
  a benchmark, and labeled as judgment in the PR. `maturity: stable`
  needs the model in the provider's public model catalog, not only a
  model card (Iterations #16, #17). If you can't support a rating, the
  model doesn't enter: list it under "Not included" with the reason.
- Alongside the YAML: at least one access route in
  `dataset/access_routes/{provider}/` with the exact `model_id`,
  `Docs/models/{id}.md` with a source per field, and a
  `Docs/CHANGELOG.md` entry.
- **Scope:** text and code LLMs only (`VISION.md`). No video, music or
  image-generation models.
- **Providers:** Anthropic, DeepSeek, Google, Mistral AI, OpenAI and
  Alibaba Cloud. A new provider, or a hosting platform (OpenRouter,
  Groq), is the owner's call: report it under "Owner decision needed",
  don't add it.

## 4. Lifecycle and dated facts

- The provider announces a deprecation, or already routes the model's
  requests to a successor: `status: deprecated`, with `shutdown_date`
  and `replacement` from its deprecations page. The engine stops
  recommending it; the YAML stays until the shutdown date.
- The provider still serves the model, says it is not deprecated, but
  closes it to new developers: `restricted` (Iteration #29). When the
  provider names no successor for that model, leave `replacement`
  alone and ask: the pick is the owner's.
- `tests/test_catalog_dates.py` failing is the alarm working, not a bug.
  Fix the dataset, never the test, and never move a date to make the
  suite pass:
  - **Introductory price ended:** re-check the pricing page, set
    `cost.*` to the price now in force, and remove `effective_until`
    and `reverts_to` (or update them if the provider extended the
    offer).
  - **Shutdown date reached:** remove the model's YAML and every one of
    its access routes, update the counts (section 6) and leave
    `Docs/models/{id}.md` in place. If another entry's `replacement`
    names the removed model, the loader fails: report it, don't pick a
    new successor yourself.

## 5. Subscription plans

- `dataset/subscriptions/{provider}/{plan_id}.yaml`. Every field is
  objective, with its URLs in a YAML comment.
- `price.monthly_usd` is the US list price. `usage_multiplier` and
  `api_credits` are required keys, `null` allowed. A plan's usage limit
  is never stored as a number or turned into tokens. A tier with its own
  price is its own plan (Iteration #31).
- A subscription access route exists only where the plan's own page
  names that exact model. A family name is not enough, and a different
  name is a different model ("Gemini 3.1 Pro" in the app is not
  `gemini-3.1-pro-preview` until the owner decides it is).
- Plan prices have no date alarm. Re-check price, multiplier and
  credits of every plan in each run.

## 6. Tests

- Run the full `pytest` before opening or updating the PR and paste its
  summary line.
- The only test edits allowed are the catalog counts:
  - `tests/test_loader.py`: `len(models) == N` and `EXPECTED_IDS`.
  - `tests/test_access_loader.py`: the route count, the direct-API model
    count and the plan count.
- Any other failing test stays exactly as it is: don't change its
  priorities, its expected winner, its scenario or its numbers. Open the
  PR anyway with `[tests red]` in the title and paste each failing test
  with its assertion message. A ranking change caused by real data is
  information for the owner, not something to hide.

## 7. Files

**May edit:** `dataset/models/`, `dataset/access_routes/`,
`dataset/subscriptions/`, `Docs/models/{id}.md`, existing
`Docs/access-guides/*.md`, `Docs/CHANGELOG.md`,
`Docs/IMPLEMENTATION_NOTES.md`, and the two test files above (counts
only).

**Never edit:** `decision/`, `interfaces/`, any other file in `tests/`,
`Docs/SCHEMA.md`, `Docs/ARCHITECTURE.md`, `Docs/VISION.md`,
`Docs/ROADMAP.md`, `Docs/FEATURES.md`, `Docs/CONTRIBUTING.md`,
`Docs/DESIGN_NOTES.md`, `README.md`, `pyproject.toml`, this file.

- **`Docs/models/{id}.md`:** add or update the section that changed.
  The rest stays as it is: the "Why" columns, per-field notes and
  sources are never compressed or rewritten.
- **`Docs/CHANGELOG.md`:** a new dated entry at the top, in the
  existing voice. Nothing older is removed or edited.
- **`Docs/IMPLEMENTATION_NOTES.md`:** a new iteration at the end, with
  the next number and the same format (Observation / Current decision /
  Status). Older iterations are never renumbered or edited.
- **400 lines** is a limit for code and tests, not for `Docs/*.md`.
  Never split or truncate a document to fit it. If a count edit would
  take a test file past 400 lines, stop and report it.

## 8. Git and the pull request

- Never push to `main`, merge, force-push, delete a branch, rewrite
  history or close a PR.
- Commit only the real change. No probe, size-test or delete-and-restore
  commits. If the GitHub API rejects a payload, split the change into
  smaller commits of whole files; never commit a truncated file.
- Title: `catalog(YYYY-MM-DD): <summary> — DO NOT MERGE (bot)`, with
  `[tests red]` in front when section 6 applies.
- Body, in this order: files touched; objective fields (model, field,
  old → new, source URL); editorial fields, as judgment, with the
  reasoning; already on main; not included, and why; owner decision
  needed; `pytest` summary.
- Nothing changed: no PR.

## 9. Settled decisions

Don't reopen these; raise new evidence under "Owner decision needed".

| Decision | Where |
|---|---|
| DeepSeek `cost.*` stores the peak-hours rate | YAML comments of the DeepSeek entries |
| Prices by prompt length store the lower tier | Iteration #24 |
| `max_output: null` when the provider publishes no ceiling | Iteration #26 |
| The quality scale stops at `very_high`; ties are broken by price | Iteration #27 |
| `deprecated` and `restricted` models are never recommended | Iterations #28, #29 |
| Gemini 2.5 is `restricted`, successors picked by the owner | Iteration #29 |
| `release_date` sourcing | Iteration #30 |
| Plans: list price, multiplier in the provider's words, no token limits | Iteration #31 |
| Text and code LLMs only | `VISION.md` |

## Owner work in progress

The owner is working on these right now. Don't open PRs about them; if
you find something new, mention it under "Owner decision needed". Items
leave this list when they land on `main`.

- `access.has_free_access` of `claude-haiku-5-5`, `claude-sonnet-5-5`
  and `gpt-6-luna`.
- Admissions: Mistral Large 4; Meta (Muse Wonder, Muse Spark 1.x);
  Qwen3.8-Flash, Qwen3.7-Plus, Qwen3.7-Flash; self-hosted open-weights
  models (Liquid AI LFM2.5).
- The `lifecycle` block of `claude-haiku-4-5`.
- A subscription route for "Gemini 3.1 Pro" in the Gemini app.
