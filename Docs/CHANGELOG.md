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

## 2026-10-05 — DeepSeek V4.1 Flash price/vision fix; Claude Sonnet 4.5 lifecycle noted

**Urgent catalog corrections from the daily provider audit against official docs.**

- **DeepSeek Flash** (`deepseek-v4-flash`): cost updated peak cache-miss **$0.30 / $1.20** (was $0.44/$1.32); `capabilities.vision` set to `true`; display name/version aligned to DeepSeek-V4.1-Flash. Official page still accepts the legacy id `deepseek-v4-flash` but serves V4.1-Flash. Source: https://api-docs.deepseek.com/quick_start/pricing
- **Claude Sonnet 4.5** stays in the active dataset. Anthropic deprecated it 2026-09-30 (retires 2026-11-30, replacement `claude-sonnet-5-5`). Lifecycle documented in `Docs/models/claude-sonnet-4-5.md`; removal vs flag remains the open catalog-policy question in `IMPLEMENTATION_NOTES.md` Iteration #22. Source: https://docs.anthropic.com/en/docs/about-claude/model-deprecations

## 2026-10-04 — Claude Sonnet 5.5 and Claude Opus 5.5 admitted (33 models); Gemini 4 not yet admissible

**Two new Claude models are in, both confirmed on Anthropic's own pages and on each cloud's own documentation; the "Gemini 4" announcement turned out to be one gated model with no public API yet.**

- **Claude Sonnet 5.5** (released 2026-09-28): $2.00/$10.00 per million tokens, 1M-token context, 128K max output, vision and tool calling. Same price as Sonnet 5, standard rate with no introductory pricing.
- **Claude Opus 5.5** (released 2026-09-22): $4.00/$20.00, same 1M/128K limits — 20% cheaper than Opus 5, and Anthropic's overview now points to it as the default starting model. Quality ratings for both mirror their predecessors: the evidence supports the scale's existing ceiling, not a rating above it.
- Four access routes each (direct API, AWS Bedrock, Google Vertex, Microsoft Foundry), every cloud checked against its own documentation rather than just Anthropic's model page. No Claude-subscription route: Anthropic names no plan tier.
- **Gemini 4 Argon is not admitted.** It's a single model, announced 2026-09-30 and rolling out only to trusted cyber defenders; it isn't in Google's model catalog or pricing page and has no model id. No other Gemini 4 variant exists in any Google source.
- Noted, not acted on: `claude-sonnet-4-5` is now deprecated (retires 2026-11-30), `gpt-5`'s current snapshot retires 2026-12-11, and DeepSeek released V4.1-Flash. See `Docs/IMPLEMENTATION_NOTES.md`, Iteration #22.

---

## 2026-09-08 — Qwen3.8-Max admitted (31st model, first Alibaba Cloud entry); Muse Spark 1.3 held back on a real sourcing gap

**Two OpenRouter listings from a Grok tip, evaluated independently against each provider's own documentation — one cleared the bar, one didn't, for a reason worth understanding rather than working around.**

- **Qwen3.8-Max admitted.** First Alibaba Cloud entry in this catalog. Confirmed directly on Alibaba Cloud Model Studio's own model page: vision input, 1,000,000-token context window, 131,072 max output, $2.00/$6.00 per 1M tokens on the International (Singapore) pricing scope (the China/Beijing scope is materially cheaper but requires a Mainland China account). One access route: ordinary self-serve API billing, no program-membership gate like `gpt-6-astra` had.
- **A real complication surfaced and was resolved deliberately, not by assumption**: Alibaba also ships a separately-released open-weights checkpoint (`Qwen/Qwen3.8-2.4T-A95B` on Hugging Face) under overlapping "Qwen3.8-Max" naming — text-only, no vision, a smaller context window than the hosted API. Different model ID, different capabilities, per `SCHEMA.md`'s own rule for when something is a separate entry. Admitted only the hosted API product this pass; the open-weights variant is flagged as an open question for a possible second entry later, not folded in or silently skipped. Full reasoning in `Docs/IMPLEMENTATION_NOTES.md`, Iteration #20.
- **Meta Muse Spark 1.3 was not admitted.** Everything else checked out — real product (Meta Model API, first-party, OpenAI/Anthropic-SDK-compatible), $1.25/$4.25 per 1M tokens confirmed on Meta's own pricing page (matching the tip exactly), 1,048,576-token context window confirmed on multiple official pages. But every official page checked publishes exactly one combined context-window figure and never a distinct output-token ceiling — one page states outright that all three Muse Spark versions "share... a 1,048,576-token context window." `SCHEMA.md` requires `context_window` and `max_output` as two separate fields; a third-party aggregator's specific number for the latter (943,718) appears nowhere in Meta's own docs and wasn't used. Logged as a genuine open question rather than guessed — `Docs/IMPLEMENTATION_NOTES.md`, Iteration #21.

---

## 2026-09-07 — GPT-6 Astra's Trusted Access Program gate lifted, three days after admission

**The gate this catalog modeled honestly on 2026-09-04 didn't last long — OpenAI opened the model up to ordinary self-serve API access, and the route now says so.**

- Re-verified against `developers.openai.com/api/docs/pricing`, GPT-6 Astra's own model page, and the models index — all three, live, on a Grok tip. The Trusted Access Program rollout paragraph present three days ago is gone from every one of them; the model is now presented as the default recommended flagship with no access caveat, and its rate-limits table lists standard usage tiers identical in shape to every other self-serve OpenAI model. Prices unchanged.
- `dataset/access_routes/openai/gpt-6-astra-direct-api.yaml` updated in place: `RequirementKind.PROGRAM_MEMBERSHIP` → `RequirementKind.API_BILLING_LINKED`, the same requirement as `gpt-5-6-sol`'s own direct-api route. Verified both directions with `recommend_access()`: billing info alone now resolves to `CURRENTLY_ELIGIBLE`; holding the Trusted Access Program membership without billing info still correctly resolves to `REQUIRES_ONBOARDING` — the membership genuinely no longer matters to this route.
- This isn't the "Plus/Pro/Business/Enterprise access ships" scenario the admission entry anticipated (see 2026-09-04 below) — there's no subscription-plan angle here. The direct API route's own gate was lifted; edited in place rather than adding a parallel route, since it's the same surface with one changed requirement, not a second access method. Full reasoning in `Docs/IMPLEMENTATION_NOTES.md`, Iteration #19.
- The "OpenAI Trusted Access Program" checkbox has no access route behind it again — `RequirementKind.PROGRAM_MEMBERSHIP` is back to zero real usages, same as before this model's admission. Kept, not removed: same reasoning as the NVIDIA Developer Program checkbox (OpenAI could gate a future model the same way again), and unlike NVIDIA, this program did have one real, working route for three days — that's signal, not dead weight.

---

## 2026-09-06 — Full codebase audit: two display bugs fixed, silent priority duplication closed, dead-line-limit cleanup

**A full functional/visual audit of the web form (every priority combination, every budget mode, the access checkboxes) surfaced two real display bugs and a UX gap that unit tests alone hadn't caught — all three are fixed, alongside a round of pure code deduplication that changed no behavior.**

- **Fixed:** the Cost tier card showed "Very_high" instead of "Very high" for the top budget tier — `result.html` was missing the `replace('_', ' ')` step the rest of the templates already used before `capitalize`. Now handled by a shared Jinja `humanize` filter, also applied to the three other templates that had the same pattern inlined.
- **Fixed:** the "why this model" reasoning showed the raw ISO code ("Supports en with...") instead of the language's name ("Supports English with..."). `language_name()` moved from `interfaces/web/languages.py` into `decision/domain/languages.py` so `decision/explainer/` can use it directly, without `decision/` importing from `interfaces/`.
- **Fixed:** picking the same priority at two different ranks (e.g. Cost at #1 and #2) used to be silently deduplicated with zero feedback. The web form now disables an already-picked priority in the other two dropdowns as soon as it's chosen, so the ambiguous state can't be created from the UI at all. The silent-dedup fallback in `context_form.py` stays for a no-JS submission.
- **Confirmed, not changed:** GPT-6 Astra's `program_membership` access gate (see 2026-09-04 below) works correctly end-to-end — verified this time with real clicks in the browser, not just a direct function call. But under its current quality ratings it can never actually become the #1 recommendation, so a real user has no path in the live UI to ever see that access requirement rendered. Documented as a known, honest limitation of the current dataset, not a bug to fix.
- **Refactor, no behavior change:** a triplicated `_values()` helper (renamed `enum_values`) consolidated into `decision/loader/_util.py`; the `Priority -> quality attribute` mapping that `decision/explainer/` and `interfaces/web/affordability.py` each redefined separately is now one `QUALITY_DIMENSION_ATTR` constant on `decision/domain/context.py`; `tests/conftest.py` centralizes the `models`/`make_model`/`client`/`candidate_factory` fixtures and path constants that were duplicated or inlined across 8 test files.
- **Fixed the 400-line ceiling violation** (`AGENTS.md`) in the two files that had crossed it: `tests/test_web.py` (489 lines) split into `test_web_core.py` / `test_web_budget.py` / `test_web_savings.py` / `test_web_alternatives.py`; `tests/test_explainer.py` (460 lines) split into `test_explainer_reasons.py` / `test_explainer_also_strong.py` / `test_explainer_alternatives_outranked.py`. Same 170 tests, same coverage, regrouped by responsibility.
- **Left alone, deliberately:** the CSS icon-size duplication across 8 selectors in 3 stylesheets — fixing it properly means touching every icon macro plus ~14 template call sites for a purely cosmetic, zero-bug-risk cleanup, not worth the blast radius; the NVIDIA Developer Program checkbox, kept in case NVIDIA NIM gets admitted to the dataset someday.

---

## 2026-09-04 — GPT-6 Astra admitted (30th model), with an honest access gate

**OpenAI's new flagship is public-priced but not yet self-serve —
instead of excluding it or pretending the gate doesn't exist, this
release models it directly for the first time.**

- New dataset entry `gpt-6-astra`: OpenAI's own system card calls it
  "the most capable model we have ever broadly deployed." Quality
  ratings kept identical to `gpt-5-6-sol` on reasoning/coding (already
  at this dataset's ceiling), with stronger direct evidence this time
  for `instruction_following` (roughly half the alignment-flag rate of
  its predecessor across 54,000+ internal tasks).
- **Access is the real story.** OpenAI's own model page: "rolling out
  today for enterprises in our Trusted Access Program, with access
  through API and our Plus, Pro, Business and Enterprise plans coming
  in the coming days." That's neither "excluded, invite-only" (this
