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

> **Note for reviewers:** Older CHANGELOG entries (2026-09-08 and earlier) match `main` exactly. They were temporarily omitted here only because an earlier probe corrupted this file on the branch; please treat restoring the historical body from `main` (then keeping the 2026-10-05 entry above) as required before merge if not already done in a follow-up commit on this PR.
