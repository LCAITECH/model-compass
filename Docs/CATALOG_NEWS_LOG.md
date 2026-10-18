# CATALOG_NEWS_LOG.md — what has already been checked

A log of the news items and tips about the catalog's providers that the
project owner's review has already checked, each with its outcome. It
exists so the catalog bot does not report the same thing twice, and so a
reviewer can see that an item was looked at and what came of it.

- **Who writes it:** the owner, or whoever reviews for the owner, after
  reading the provider's own page. The catalog bot never edits it
  (`CATALOG_BOT.md`, sections 7 and 10), so an item cannot be marked as
  handled by the same bot that reported it.
- **How the bot uses it:** `CATALOG_BOT.md`, section 10.
- **It is not a source.** No value is copied from here into a YAML file.
  Values come from the provider's page or from `main`. An entry records
  what was checked and decided, nothing more.
- **Entries are never rewritten.** If an outcome changes (a pending
  decision is made, a page changes), add a new dated entry that points to
  the old one, the same way `INCIDENT_LOG.md` works. Newest first. The bot
  reads the last 60 days; older entries stay for the record, and what
  they led to lives in `CHANGELOG.md` and `IMPLEMENTATION_NOTES.md`.
- **Pages read through a summarizer** (a fetch tool that returns a summary,
  not the raw page) are marked as such. A summarizer's reading is a pointer
  to confirm, not a confirmation.

## Outcomes

| Outcome | Meaning |
|---|---|
| Applied | Changed the dataset or its docs; the commit is named. |
| No change | Checked against the provider's page; the dataset is already right, or the schema has no field for it. |
| Not admitted | A model or provider that stays out of the catalog, with the reason. |
| Owner decision pending | Needs a decision that is the owner's. Don't open a PR; raise it again only with new evidence. |
| Outside scope | Does not touch a catalog provider's text or code model, price, limit, plan or retirement. |

## Log

| Reviewed | Item as reported | Outcome | What was checked, and where it is recorded |
|---|---|---|---|
| 2026-10-17 | Gemini 4 Argon in Google AI Studio with Google AI Pro, not only Ultra (the owner's screenshot of the AI Studio unlock dialog: "needs a Google AI plan or a Gemini API key") | Applied | Google's plans page (`ai.google.dev/gemini-api/docs/google-ai-plans`, "Last updated 2026-10-16 UTC", read as raw HTML) lists Argon under AI Pro and excludes only the Free plan; its pricing page now says "not available on the Free tier". The dataset had recorded Ultra-only. Commit `289284b`; `Docs/models/gemini-4-argon.md` has a dated correction. |
| 2026-10-17 | DeepSeek-V4.1-Flash-1017 (released 2026-10-17): "$0.15/$0.60 unchanged", 552B parameters, MIT license, Search and Fetch APIs at $0.75 per 1,000 calls | No change | DeepSeek's pricing page (raw HTML) already lists `deepseek-flash` as DeepSeek-V4.1-Flash-1017 at $0.15/$0.60 off-peak and $0.30/$1.20 peak; the dataset stores the peak rate (`CATALOG_BOT.md`, section 9) and its context (1M) and output (384K) match. The release note (raw HTML) states no parameter count and names no license; it links the open weights on Hugging Face. The dataset's `version: "V4.1"` does not record the snapshot name; the schema has no field for it. Search and Fetch pricing has no field either. |
| 2026-10-17 | Claude Opus 5.5 fast mode out of research preview, $8/$40 per million tokens (standard $4/$20) | No change | Anthropic's pricing page lists fast mode for Opus 5.5 at $8/$40 beside standard $4/$20, which is what the dataset stores. The schema has no field for a fast or priority mode (the same as Gemini 4 Argon's Priority tier). The "out of research preview" part was not checked. |
| 2026-10-17 | Gemini 2.5 variants retiring on 2026-10-20 and OpenAI snapshots on 2026-10-23 | No change | Google's deprecations page (raw HTML, "Last updated 2026-10-12 UTC") has no 2026-10-20 date; its 2026-10-22 and 2026-10-23 shutdowns are Veo, `gemini-omni-flash-preview` and `deep-research-pro-preview-12-2025`, none in the catalog. Gemini 2.5 stays `restricted` with no shutdown date (Iteration #29). OpenAI's deprecations page (read through a summarizer) lists the 2026-10-23 shutdowns as legacy snapshots (GPT-3.5, GPT-4, GPT-4 Turbo, GPT-4.1 nano, o1, o1-pro, o3-mini, o4-mini, `gpt-4o-2024-05-13`, `gpt-image-1`); the only one in the catalog's scope is the GPT-4o snapshot, already recorded in `Docs/models/gpt-4o.md`. |
| 2026-10-17 | Meta Muse Spark Open: 816B open weights (42B active), 1M context, Muse Model License, released 2026-10-15 | Owner decision pending | Only press coverage was read; no Meta page. Open-weights models, hosted by third parties or self-hosted, have no admission policy yet (`CATALOG_BOT.md`, "Owner work in progress"). Not admitted. |
| 2026-10-17 | NVIDIA Nemotron 3.5 Super VL, Reflection AI Beam 1.0, Jais 3 (open-weights families) | Not admitted | The providers are not in the catalog, which is the owner's call (`CATALOG_BOT.md`, section 3), and open-weights models have no policy yet. None of their own pages was read. |
| 2026-10-17 | Elorian Glimpse, a visual-reasoning model from a new provider ($0.60/$3.00) | Not admitted | A new provider is the owner's call (`CATALOG_BOT.md`, section 3). No Elorian page was read, and it is a vision-first model, so it would also need a decision under the text-and-code scope (`VISION.md`). |
| 2026-10-17 | Microsoft MAI-Base-2, xAI Grok Voice 3.0, Anthropic's quantum-circuit research, China's draft export controls on AI, Modal Labs' Series D, METR's access at Anthropic, the White House task force, state lawsuits against OpenAI, Bank of America's remediation hiring | Outside scope | Not read. None is a text or code model of a catalog provider with a price, limit, plan or retirement to change; Grok Voice is a voice model (`VISION.md`). |
