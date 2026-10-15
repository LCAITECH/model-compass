# Access guide — Meta

Curated pointer, not a step-by-step tutorial: it says what you need
and where to start, and links to the official documentation for the
steps, which would go stale every time a provider redesigns its
console. Model Compass does not replace that documentation (`VISION.md`).

## `meta#direct-api`

Meta Model API serves the Muse models over endpoints compatible with
the OpenAI SDK and the Anthropic SDK, so most stacks need only a base
URL (`https://api.meta.ai/v1`) and a key. Availability varies by
country: check Meta's
[Geographic Use Policy](https://dev.meta.ai/legal/geographic-use-policy)
first.

1. Sign in at [dev.meta.ai](https://dev.meta.ai) and set up
   pay-as-you-go billing.
2. Create an API key in the Model API dashboard and export it as
   `MODEL_API_KEY`.
3. Pick the mode by model id: the plain id (`muse-spark-1.3`) is
   Standard mode, where Meta does not train on your content; a
   `-contributor` id is cheaper because Meta may train future models on
   your prompts and outputs.
4. Follow the official docs for your first call:
   [Quickstart](https://dev.meta.ai/docs/quickstart).

Source: [Models](https://dev.meta.ai/docs/models) and
[Pricing and rate limits](https://dev.meta.ai/docs/pricing-rate-limits),
consulted 2026-10-15.
