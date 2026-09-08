# Access guide — Alibaba Cloud

Curated pointer, not a step-by-step tutorial — see
`Docs/ACCESS_ADVISOR_AUDIT_2026-08-11.md`, Part 5.4, for why. Links to
official documentation for the actual steps; Model Compass does not
replace it.

## `alibaba#direct-api`

Alibaba Cloud Model Studio is the console for Qwen and third-party
models; billing is per-region, separate from any Alibaba.com or
Taobao account.

1. Create/use an Alibaba Cloud account and activate Model Studio at
   [modelstudio.console.alibabacloud.com](https://modelstudio.console.alibabacloud.com).
2. Pick a region (International/Singapore is the one this catalog
   prices — see the model's own cost fields) and add billing under
   that region's account settings.
3. Generate an API key from the Model Studio console.
4. Call the model through the DashScope-native API or the
   OpenAI-compatible endpoint — follow the official docs for your
   first call: [Qwen3.8-Max model page](https://www.alibabacloud.com/help/en/model-studio/qwen3-8-max).

Source: [Qwen3.8-Max model page](https://www.alibabacloud.com/help/en/model-studio/qwen3-8-max), consulted 2026-09-08.
