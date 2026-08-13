# Access guide — Mistral

Curated pointer, not a step-by-step tutorial — see
`Docs/ACCESS_ADVISOR_AUDIT_2026-08-11.md`, Part 5.4, for why. Links to
official documentation for the actual steps; Model Compass does not
replace it.

## `mistral#direct-api`

La Plateforme is Mistral's API console; billing is managed there,
separate from the Le Chat consumer app.

1. Create/use a Mistral account at [console.mistral.ai](https://console.mistral.ai).
2. Add billing under the console's workspace settings.
3. Generate an API key from the console.
4. Follow the official docs for your first call: [Mistral API reference](https://docs.mistral.ai/api/).

Source: [Mistral pricing](https://mistral.ai/pricing), consulted 2026-08-13.

## `mistral#self-hosted`

Mistral Large 3 is released under Apache 2.0 as open weights -- no
Mistral account or billing needed, but you provide and pay for your
own compute.

1. Download the weights from [Hugging Face](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512).
2. Provision GPU infrastructure: a single node with 8xH200 GPUs (FP8)
   or 8xH100/A100 GPUs (NVFP4) is the vendor-documented minimum for
   this 675B-parameter (41B active) mixture-of-experts model.
3. Serve it with an inference engine such as vLLM, using tensor
   parallelism across the 8 GPUs.

Source: [Mistral Large 3 model repository, Hugging Face](https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512), consulted 2026-08-13.
