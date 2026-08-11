# GPT-5.6 Sol

Dataset entry: [`dataset/models/gpt-5-6-sol.yaml`](../../dataset/models/gpt-5-6-sol.yaml)
Last verified: 2026-08-10

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from
`Docs/CANDIDATE_RESEARCH_2026-08-10.md` (branch
`research/model-candidates`) — **replaced GPT-5 as OpenAI's current
flagship**, GA since 2026-07-09.

## Naming note

OpenAI's own model ID uses a dot (`gpt-5.6-sol`, confirmed on
`developers.openai.com/api/docs/models/gpt-5.6-sol`). No file in this
dataset uses a literal dot — the established convention converts
version dots to hyphens (`claude-sonnet-4-6` for "4.6"). This entry's
`id` follows that same convention: `gpt-5-6-sol`. "Sol" is a durable
capability-tier identifier (OpenAI's own framing: "the number
identifies a model's generation, while Sol, Terra, and Luna identify
durable capability tiers"), kept in `name`, not folded into a suffix
like "mini"/"nano".

---

## Identity

| Field      | Value          |
|------------|----------------|
| `id`       | `gpt-5-6-sol`  |
| `name`     | GPT-5.6 Sol    |
| `provider` | OpenAI         |
| `version`  | `5.6`          |
| `license`  | `proprietary`  |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page: "Input: Text and image"; "Vision/image input ✓". |
| `audio`                | false | Model page: "Audio input ✗", "Audio output ✗". |
| `image_generation`     | false | Native output is text-only; image generation reachable only as a separate Responses API tool, same distinction already drawn for `gpt-5` — not a native output modality. |
| `tool_calling`         | true  | Model page: "Function calling ✓", plus web_search/file_search/code_interpreter/computer_use tools listed. |
| `structured_output`    | true  | Model page: "Structured outputs ✓". |
| `json_mode`            | true  | Not independently confirmed per-model this pass — same basis already used for `gpt-5` (structured_output confirmed, JSON mode specifically not itemized separately by OpenAI). Inherited/curated. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | OpenAI's own official framing (`deploymentsafety.openai.com`, first-party domain): "our new flagship model," "sets a new standard for both intelligence and efficiency... outperforming previous and competing frontier models," "state-of-the-art results across coding, knowledge work, cybersecurity, and science." GPT-5 was already `very_high` here — this evidence supports Sol staying at that same ceiling as the new flagship, not exceeding a scale that has no higher rung. |
| `coding`                   | `very_high` | Same evidence — "state-of-the-art results across coding" explicitly named. |
| `creative_writing`         | `high`      | No official statement specifically addresses creative writing quality for this model — kept at the same catalog-wide ceiling already applied to `gpt-5` ("no model in this dataset is rated `very_high` on creative writing yet"), not bumped just because other dimensions were. |
| `instruction_following`    | `very_high` | Consistent with the flagship, tool-using, "state-of-the-art" positioning. |

Per `SCHEMA.md`'s evidence-based calibration principle: this rating is
identical to `gpt-5`'s, deliberately — the sourced evidence
("flagship," "outperforming... frontier models") supports Sol
remaining at the existing top of the 4-level scale, not an automatic
bump simply for being the newer release. A benchmark claim surfaced
during research (an "Agents' Last Exam" score allegedly beating Claude
Fable 5) was explicitly excluded here — it could not be confirmed
against a directly-fetched first-party OpenAI page, only a
WebSearch-indexed snippet, and this catalog does not use benchmark
scores as an editorial source regardless of confirmation status (see
`SCHEMA.md`'s Objective vs. Editorial section).

## Languages

Not independently reconfirmed this pass — OpenAI does not publish an
explicit per-model language list. Reused the same curated set as
`gpt-5`/`gpt-5-mini` (same provider family), itself a curated list, not
an OpenAI-published fact (see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,050,000  |
| `max_output`           | 128,000    |

Confirmed directly against the official model page ("Context window:
1.05M tokens"; a 922K-token input sub-limit exists within that total,
same style of nuance already noted for `gpt-5`/`gpt-5-mini`'s
272,000-token input sub-limit).

## Cost `[Objective]`

| Field                    | Value   |
|----------------------------|---------|
| `input_per_million`         | $5.00   |
| `output_per_million`        | $30.00  |

Confirmed directly against `developers.openai.com/api/docs/pricing`,
standard/short-context tier. Additional tiers not represented in the
schema: cached input $0.50/M, cache writes $6.25/M, batch $2.50/$15.00,
and a premium long-context rate (2x input/1.5x output) above 272K
input tokens — same tiered-pricing friction already logged in
`IMPLEMENTATION_NOTES.md` Iteration #5, standard tier used here
consistent with every other entry in this catalog.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same API surface as the rest of the GPT-5 family. |
| `maturity`              | `stable` | Generally available following a limited preview — GA rollout confirmed 2026-07-09. |

---

## Access

Standard OpenAI API at the pricing in `cost.*` above.

**Free access (`access.has_free_access`):** `false`. OpenAI's own
announcement (`openai.com`/`help.openai.com`) states free-tier ChatGPT
users are defaulted to GPT-5.6 Luna (a different, cheaper tier), not
Sol — Sol itself requires ChatGPT Plus or higher, or API billing. No
continuous free path to this specific model exists, same pattern as
every other OpenAI entry in this catalog.

**Note for the project:** with GPT-5.6 Sol confirmed GA and
explicitly framed by OpenAI as the flagship replacing GPT-5, the
existing `gpt-5.yaml` entry is now in the same "superseded, still
priced/available" position as the legacy Claude entries already in
this dataset. Flagging this as an observation for a future session —
out of scope for this admission, which only concerns the six
candidates approved this session.

## Sources

- [GPT-5.6 Sol model page](https://developers.openai.com/api/docs/models/gpt-5.6-sol) — capabilities, context window, max output, id.
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) — cost fields.
- [GPT-5.6 system card](https://deploymentsafety.openai.com/gpt-5-6-preview) — flagship framing, "state-of-the-art" language (first-party OpenAI subdomain).
- OpenAI's GPT-5.6-in-ChatGPT announcement (`help.openai.com`) — free-tier routing to Luna, not Sol.

Accessed 2026-08-10, official OpenAI documentation only. Two pages
(`openai.com/index/gpt-5-6/`, one `help.openai.com` article) returned
HTTP 403 on direct fetch during this research pass — corroborated
instead via the first-party `deploymentsafety.openai.com` system card
and WebSearch-indexed snippets of the blocked pages, never via
aggregators.

## Verification result

New dataset entry. Objective fields confirmed against official
documentation. `json_mode` and `languages`/`language_quality` flagged
as inherited/curated, same recurring gap as `gpt-5`. `id` naming
resolved by explicit project convention (dot → hyphen), documented
above.
