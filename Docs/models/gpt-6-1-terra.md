# GPT-6.1 Terra

Dataset entry: [`dataset/models/gpt-6-1-terra.yaml`](../../dataset/models/gpt-6-1-terra.yaml)
Last verified: 2026-10-27

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Proposed from the 2026-10-27 daily
provider audit: OpenAI's models index, pricing page, model page and
changelog listed it for the first time that day. Every objective field
was read on OpenAI's own pages (see Sources).

## Naming note

Official API id is `gpt-6.1-terra`; the dataset id converts the dot to a
dash (`gpt-6-1-terra`), as with `gpt-6-1-sol`. "Terra" is OpenAI's middle
tier between Sol and Luna. It is a different model from `gpt-5-6-terra`,
which stays in the catalog: OpenAI has not deprecated GPT-5.6 Terra.

---

## Identity

| Field      | Value           |
|------------|-----------------|
| `id`       | `gpt-6-1-terra` |
| `name`     | GPT-6.1 Terra   |
| `provider` | OpenAI          |
| `version`  | `6.1`           |
| `license`  | `proprietary`   |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page: "Input modalities: text, image". |
| `audio`                | false | "Unsupported modalities: audio, video". |
| `image_generation`     | false | "Output modalities: text". Image generation appears only as a Responses API tool, not a native output. |
| `tool_calling`         | true  | `function_calling` under "Supported features". "Tool calling requires the Responses API." |
| `structured_output`    | true  | `structured_outputs` under "Supported features". |
| `json_mode`            | true  | Same basis as the other OpenAI entries (structured outputs supported). |

## Quality `[Editorial]`

Judgment, from OpenAI's own positioning of the model on its pages. No
rating is derived from a benchmark score.

| Field                    | Value  | Why |
|---------------------------|--------|-----|
| `reasoning`                | `high` | OpenAI presents it as "a significant step up from GPT-5.6 Terra" (rated `high`) and as its fast, efficient tier below GPT-6.1 Sol and GPT-6 Astra (`very_high`). Not raised to `very_high` because OpenAI itself points to Sol and Astra for "in-depth research or complex coding". |
| `coding`                   | `high` | The announcement calls it "a substantial improvement over GPT-5.6 Terra for software engineering" (rated `medium`), and adds "For the most complex coding tasks, GPT-6.1 Sol and GPT-6 Astra remain the better choice". One step above GPT-5.6 Terra, one below Sol. |
| `creative_writing`         | `high` | One of the three uses OpenAI names on the model page and in the GPT-6 guide: "clear, natural writing", "draft and revise text". The same rating as GPT-6.1 Sol; no claim that it writes better than Sol. |
| `instruction_following`    | `high` | The announcement says it is "more likely to stay within scope and honestly disclose limitations" than GPT-5.6 Terra (rated `high`). No claim that puts it with Sol or Astra. |

## Languages

Curated set reused from the other GPT-6 entries (Iteration #1). OpenAI's
models index says "All latest OpenAI models support ... multilingual
capabilities" and publishes no per-language results for this model.

## Operational `[Objective]`

| Field              | Value      |
|----------------------|------------|
| `context_window`      | 1,050,000  |
| `max_output`           | 128,000    |

Model page: "1,050,000 context window", "128,000 max output tokens"
("Maximum input tokens: 922,000"). Knowledge cutoff Jun 01, 2026 (not in
the schema).

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $1.00  |
| `output_per_million`        | $5.00  |

Standard short-context rate, on the model page and the pricing page's
Flagship table. Prompts over 272K input tokens are billed at 2x input and
cache rates and 1.5x output for the whole request ($2.00 / $7.50 on the
pricing page); that higher tier is not stored (Iteration #24). Cached
input $0.05; cache writes $1.25 (30-minute retention) or $2.50 (12-hour).
Batch and Flex are 50% lower, regional processing adds 10%, and Fast mode
is 2x Standard. None of these has a schema field.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same API surface as the rest of the GPT-6 family: Responses, Chat Completions and Batch. Tool calls need the Responses API. |
| `maturity`              | `stable` | Listed in OpenAI's public models index under Flagship models and on the pricing page's Flagship table, with the standard usage tiers. |

## Access

Direct API only in this entry. Rate limits on the model page: Build
5,000 RPM / 1,000,000 TPM, Launch 10,000 RPM / 4,000,000 TPM, Grow
15,000 RPM / 40,000,000 TPM.

**Free access (`access.has_free_access`):** `false`. The model page lists
no free API tier, and OpenAI's announcement makes it available "to all
Plus, Pro, Enterprise, and Edu users in ChatGPT Work and Codex": the free
ChatGPT plan is not named (Iteration #32).

**ChatGPT route: not added.** Section 5 of `CATALOG_BOT.md` needs the
plan's own page to name the model. ChatGPT's plan page
(`chatgpt.com/pricing`) could not be read from the audit's network on
2026-10-27 (HTTP 403), and the announcement is not a plan page. The
route can be added once the plan table is read.

## Sources

- [GPT-6.1 Terra model page](https://developers.openai.com/api/docs/models/gpt-6.1-terra)
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- [OpenAI models index](https://developers.openai.com/api/docs/models)
- [OpenAI API changelog](https://developers.openai.com/api/docs/changelog): "Oct 26 ... Released GPT-6.1 Terra"
- [GPT-6 guide](https://developers.openai.com/api/docs/guides/latest-model)
- [Introducing GPT-6.1 Terra](https://openai.com/index/introducing-gpt-6-1-terra)
- [OpenAI deprecations](https://developers.openai.com/api/docs/deprecations): not listed

Accessed 2026-10-27, official OpenAI pages only.

## Verification result

Proposed new dataset entry. Objective fields read on OpenAI's pages.
Editorial ratings are the bot's judgment from OpenAI's own positioning
against GPT-5.6 Terra and GPT-6.1 Sol, pending the owner's review.
