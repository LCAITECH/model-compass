# GPT-6.2 Astra

Dataset entry: [`dataset/models/gpt-6-2-astra.yaml`](../../dataset/models/gpt-6-2-astra.yaml)
Last verified: 2026-11-18

See [README.md](README.md) for what this document is (and isn't) and
the sourcing rule it follows. Proposed from the 2026-11-18 catalog
update, at the owner's request, after OpenAI released the model on
2026-11-17. Every objective field was read on OpenAI's own pages (see
Sources).

## Naming note

Official API id is `gpt-6.2-astra`; the dataset id converts the dot to a
dash (`gpt-6-2-astra`), as with `gpt-6-1-terra` and `gpt-6-1-sol`. It is
a different model from `gpt-6-astra`, which stays in the catalog: OpenAI
has not deprecated GPT-6 Astra.

---

## Identity

| Field      | Value            |
|------------|------------------|
| `id`       | `gpt-6-2-astra`  |
| `name`     | GPT-6.2 Astra    |
| `provider` | OpenAI           |
| `version`  | `6.2`            |
| `license`  | `proprietary`    |

## Capabilities `[Objective]`

| Field                | Value | Notes |
|-----------------------|-------|-------|
| `vision`               | true  | Model page: "Input modalities: text, image". |
| `audio`                | false | "Unsupported modalities: audio, video". |
| `image_generation`     | false | "Output modalities: text". Image generation appears only as a Responses API tool, not a native output. |
| `tool_calling`         | true  | `function_calling` under "Supported features". The changelog says "Tool calling requires the Responses API." |
| `structured_output`    | true  | `structured_outputs` under "Supported features". |
| `json_mode`            | true  | Same basis as the other OpenAI entries (structured outputs supported). |

The API rejects requests that set reasoning effort to `none`. That is a
request constraint, not a schema field.

## Quality `[Editorial]`

Judgment, from OpenAI's own positioning of the model on its pages. No
rating is derived from a benchmark score.

| Field                    | Value       | Why |
|---------------------------|-------------|-----|
| `reasoning`                | `very_high` | OpenAI presents it as "our most capable model for your hardest projects", "our new frontier model", and "our flagship model for complex reasoning and coding". That is the catalog ceiling. |
| `coding`                   | `very_high` | The model page says it "can build and revise software"; the changelog points to it "for demanding reasoning and coding tasks"; the announcement says it "writes cleaner code". |
| `creative_writing`         | `high`      | The announcement emphasizes professional writing (slides, spreadsheets and documents that "read less like AI", "more direct and specific, with fewer generic takeaways"). That supports a strong writing rating, not a claim that creative writing is the model's flagship use. |
| `instruction_following`    | `very_high` | The announcement says its documents "more closely follow the templates you provide and the conventions of your field". |

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
("Maximum input tokens: 922,000"). Knowledge cutoff May 18, 2026 (not in
the schema).

## Cost `[Objective]`

| Field                    | Value  |
|----------------------------|--------|
| `input_per_million`         | $8.00  |
| `output_per_million`        | $40.00 |

Standard short-context rate, on the model page and the pricing page's
Flagship table. Prompts over 272K input tokens are billed at 2x input and
cache rates and 1.5x output for the whole request ($16.00 / $60.00 on the
pricing page); that higher tier is not stored (Iteration #24). Cached
input $0.40; cache writes $10.00 (30-minute retention) or $20.00
(12-hour). Long-context cached input is $0.80; long-context 30-minute /
12-hour writes are $20.00 / $40.00.

Batch is 50% of Standard ($4.00 / $20.00 short-context). Fast is 2x
Standard ($16.00 / $80.00). Ultrafast is 3x Standard through February 28,
2027 ($24.00 / $120.00) and 6x Standard from March 1, 2027 (Pacific time;
$48.00 / $240.00). Background completion windows in the Responses API
public beta are 30% below Standard for a two-hour window and 40% below
for an eight-hour window. Regional processing adds a 10% uplift. The
model is not listed in the Flex table. None of these has a schema field.

## Ecosystem `[Editorial]`

| Field                | Value    | Why |
|------------------------|----------|-----|
| `integration_ease`      | `high`   | Same API surface as the rest of the GPT-6 family: Responses, Chat Completions and Batch. Tool calls need the Responses API. |
| `maturity`              | `stable` | Listed in OpenAI's public models index as a featured / flagship model and on the pricing page's Flagship table, with the standard usage tiers, generally available on 2026-11-17. |

## Access

Direct API only in this entry. Rate limits on the model page: Build
5,000 RPM / 1,000,000 TPM, Launch 10,000 RPM / 4,000,000 TPM, Grow
15,000 RPM / 40,000,000 TPM. No Free tier is listed.

**Free access (`access.has_free_access`):** `false`. The model page lists
no free API tier, and OpenAI's announcement makes it available "to all
Plus, Pro, Enterprise, and Edu users in ChatGPT Work and Codex": the free
ChatGPT plan is not named (Iteration #32).

**ChatGPT route: not added.** Section 5 of `CATALOG_BOT.md` needs the
plan's own page to name the model. ChatGPT's plan comparison table
(`chatgpt.com/pricing`, read 2026-11-18) lists GPT-6.1 Sol, GPT-6 Astra,
GPT-6 Sol, GPT-6 Luna and GPT-5.6 Terra, and does not name GPT-6.2 Astra.
The announcement is not a plan page. The route can be added once the plan
table is read with this exact name.

## Sources

- [GPT-6.2 Astra model page](https://developers.openai.com/api/docs/models/gpt-6.2-astra)
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)
- [OpenAI models index](https://developers.openai.com/api/docs/models)
- [OpenAI API changelog](https://developers.openai.com/api/docs/changelog): "Nov 17 ... Use GPT-6.2 Astra for demanding reasoning and coding tasks..."
- [Introducing GPT-6.2 Astra and Sol](https://openai.com/index/introducing-gpt-6-2-astra-sol/)
- [OpenAI deprecations](https://developers.openai.com/api/docs/deprecations): not listed
- [ChatGPT plans and pricing](https://chatgpt.com/pricing/): exact name not in the comparison table (read 2026-11-18)

Accessed 2026-11-18, official OpenAI pages only.

## Verification result

Proposed new dataset entry. Objective fields read on OpenAI's pages.
Editorial ratings are the bot's judgment from OpenAI's own positioning
as the current flagship, pending the owner's review.
