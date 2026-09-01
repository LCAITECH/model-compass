# Claude Fable 5.1

Dataset entry: [`dataset/models/claude-fable-5-1.yaml`](../../dataset/models/claude-fable-5-1.yaml)
Last verified: 2026-09-01

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Admitted from a tip in a third-party
AI-generated audit (Grok) about Anthropic's 2026-09-01 GA
announcement — the tip itself was not used as a source for any field
below; every fact was independently re-confirmed by reading Anthropic's
own pages directly (see Sources), same discipline already applied to
every prior Grok tip this project has received (`IMPLEMENTATION_NOTES.md`,
Iteration #14).

---

## Identity

| Field      | Value                |
|------------|------------------------|
| `id`       | `claude-fable-5-1`    |
| `name`     | Claude Fable 5.1      |
| `provider` | Anthropic              |
| `version`  | `5.1`                  |
| `license`  | `proprietary`          |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | `platform.claude.com`'s Models overview: "All current models support text and image input, text output, multilingual capabilities, vision, and tool use." Also confirmed on the model's own marketing page, which describes vision use for document/diagram/chart understanding and self-checking coding output. |
| `audio`                | false | Not listed as a supported modality anywhere checked. |
| `image_generation`     | false | Not listed as a supported capability. |
| `tool_calling`         | true  | Same Models overview statement as `vision` above — a direct citation, stronger than the inference `claude-fable-5.md` had to rely on (that page's own tool-use pricing table still doesn't list Fable models by name). |
| `structured_output`    | true  | Not independently reconfirmed this pass — inherited, same known gap as every Claude entry in this catalog. |
| `json_mode`            | true  | Same as above — inherited. |

## Quality `[Editorial]`

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | Anthropic's own positioning, read directly on `anthropic.com/claude/fable`: "sets a new standard on coding, knowledge work, and long-running problem-solving tasks," recommended over Opus 5 for "demanding reasoning and long-horizon agentic work" on the Models overview compare table. Kept at the same ceiling as `claude-fable-5` (already `very_high`, the top of a 4-level scale) rather than treated as automatically superior — per `SCHEMA.md`'s evidence-based calibration principle, a newer version doesn't get bumped past an already-maximum rating just for being newer, and no dimension-specific evidence here would justify a rating this scale doesn't have room to express anyway. |
| `coding`                   | `very_high` | Same source: "our most capable model for coding and knowledge work" / "most capable model for ambitious coding projects." Same ceiling reasoning as `reasoning`. |
| `creative_writing`         | `very_high` | No creative-writing-specific claim found on either page checked. Kept identical to `claude-fable-5` (the only other model in this catalog at this ceiling) rather than guessed independently — same "no evidence to move it, so don't" logic already applied to `gpt-5-6-sol` relative to `gpt-5`. |
| `instruction_following`    | `very_high` | Same reasoning as `reasoning`/`coding` — flagship positioning, no dimension-specific counter-evidence found. |

## Languages

Not independently reconfirmed this pass. Reused the same curated set
as `claude-fable-5` (same provider, same known gap, see
[IMPLEMENTATION_NOTES.md, Iteration #1](../IMPLEMENTATION_NOTES.md#iteration-1)).

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,000,000  |
| `max_output`           | 128,000    |

Confirmed directly against `platform.claude.com`'s Models overview
compare table ("1 M tokens" / "128 k tokens") — same ceiling as Fable
5/Opus 5/Sonnet 5.

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $10.00 |
| `output_per_million`        | $50.00 |

Confirmed directly against both the Models overview compare table and
the dedicated pricing page — identical headline price to Claude Fable
5. The real change is prompt-caching cost, not represented in
`SCHEMA.md`: cache reads drop to $0.25/MTok (was $1.00/MTok for Fable
5, a 75% cut), which Anthropic's own marketing page states reduces
typical-workload cost by roughly 25% and highly agentic workloads by
up to roughly 45% — noted here in prose only, same convention as every
other cache-pricing nuance in this catalog (`IMPLEMENTATION_NOTES.md`,
Iteration #5). A "US-only inference" surcharge (1.1x input/output) also
exists and isn't represented in the schema, same treatment.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Confirmed on 3 of 4 access surfaces checked this pass (direct API, AWS Bedrock, Microsoft Foundry) — see Access below for the one gap (Google Cloud Vertex). |
| `maturity`              | `stable` | GA since 2026-09-01, confirmed `Active` (not `Legacy`/`Deprecated`) on Anthropic's own model-deprecations lifecycle page, and is the model Anthropic's own Models overview table recommends first ("start with Claude Opus 5 for most workloads. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work"). Meets this project's maturity bar (evidence of stability in public, provider-maintained documentation, not just technical availability) more cleanly than most admissions — it's already in the primary lifecycle/compare-table pages, not just a standalone announcement. |

---

## Access

Four of the five surfaces `claude-fable-5` already has were independently
re-checked for `claude-fable-5-1` this pass — **one did not confirm**:

- **Direct API**: confirmed. `claude-fable-5-1` is the API model ID on
  both the Models overview table and the marketing page ("use
  `claude-fable-5-1` via the Claude API").
- **Consumer subscription** (Claude.ai / Claude Code, Pro/Max/Team/Enterprise):
  confirmed directly on the marketing page: "available to Pro, Max,
  Team, and Enterprise users."
- **Amazon Bedrock**: confirmed. AWS's own Bedrock model-cards page
  explicitly lists "Claude Fable 5.1" under Anthropic's Claude 5.x
  lineup, alongside Claude Mythos 5.1, Opus 5, Sonnet 5, Mythos 5, and
  Fable 5.
- **Microsoft Foundry**: confirmed. Microsoft's own Claude-models-in-Foundry
  concepts page explicitly lists `claude-fable-5-1` (alongside
  `claude-mythos-5-1` and `claude-fable-5`, noting it uses a different
  watermarking scheme than the original Fable 5).
- **Google Cloud Vertex AI**: **not confirmed, not added as a route.**
  `docs.cloud.google.com`'s Claude-on-Google-Cloud partner-models page,
  re-read directly 2026-09-01, still only describes "Claude Fable 5 en
  Google Cloud" throughout — no mention of 5.1 anywhere on the page.
  Same documentation-lag pattern already established as project
  precedent for `gemini-3.7-flash`'s `maturity: experimental` call
  (Fase 9): a model can be GA everywhere else while one specific
  platform's docs haven't caught up yet. Revisit once Google's page is
  updated; not treated as "no Vertex access exists," just "not
  citable yet."

Access route YAML files added for the four confirmed surfaces only,
same pattern as `claude-fable-5`'s own five (see
`dataset/access_routes/anthropic/claude-fable-5-*.yaml` for the
templates these were built from — access method, eligibility, and
economics fields copied where the underlying terms are identical
across 5/5.1, evidence/source_url/consulted_at independently
re-verified for each, not copied).

**Free access (`access.has_free_access`):** `false`. Same reasoning as
`claude-fable-5` — no continuous, unconditional free access path found
on any surface checked.

## Sources

- [Claude Fable marketing page](https://www.anthropic.com/claude/fable) — GA announcement date, pricing, cache-read discount, availability surfaces, positioning, use cases.
- [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview) — compare-table identity, capabilities (vision/tool-use platform-wide statement), context window, max output, knowledge-cutoff, positioning recommendation.
- [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) — full pricing table cross-check (base, cache writes/reads, output).
- [Claude model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — lifecycle status (`Active`), tentative retirement date ("Not sooner than September 1, 2027").
- [Amazon Bedrock model support](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html) — Bedrock availability.
- [Claude models in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/claude-models) — Foundry availability, model ID.
- [Claude on Google Cloud](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) — checked, does **not** yet list Fable 5.1; basis for excluding the Vertex route this pass.

All read directly in-browser, 2026-09-01, not via summarization
tooling for the pages behind capability/cost/lifecycle claims. No
third-party AI-generated audit content used as a source for any field
above.

## Verification result

New dataset entry. All `[Objective]` fields confirmed against primary
official documentation from Anthropic, AWS, and Microsoft. `[Editorial]`
fields kept at the same ceiling as `claude-fable-5` where no
dimension-specific counter-evidence was found, per `SCHEMA.md`'s
evidence-based calibration principle. One access surface (Google Cloud
Vertex) explicitly excluded this pass for lack of official confirmation
— a real documentation-lag finding, not an oversight.
