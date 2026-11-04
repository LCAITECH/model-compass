# Access guide — Mistral

Curated pointer, not a step-by-step tutorial: it says what you need
and where to start, and links to the official documentation for the
steps, which would go stale every time a provider redesigns its
console. Model Compass does not replace that documentation (`VISION.md`).

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

## `mistral#self-hosted-large-4`

Mistral Large 4 is released as open weights under the Mistral Ecosystem
Open-Weight License, a modified MIT license: free to use, modify and
commercialize, except that a business that operates a Model-as-a-Service
offering needs a separate commercial license from Mistral. No Mistral
account or billing needed, but you provide and pay for your own compute.

1. Download the weights from [Hugging Face](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B).
   An NVFP4 checkpoint for Blackwell GPUs is a separate repository,
   [Mistral-Large-4-1T-A52B-NVFP4](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B-NVFP4).
2. Provision GPU infrastructure for a mixture-of-experts model of about
   1 trillion parameters (52B active). Mistral's serving examples use a
   node of 8 GPUs; they are examples, not a stated minimum.
3. Serve it with vLLM or SGLang, which Mistral's repository documents,
   using tensor parallelism across the GPUs.

Source: [Mistral Large 4 model repository, Hugging Face](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B), consulted 2026-11-03.
