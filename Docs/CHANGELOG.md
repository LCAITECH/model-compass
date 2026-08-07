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
