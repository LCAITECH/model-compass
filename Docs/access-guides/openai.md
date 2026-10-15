# Access guide — OpenAI

Curated pointer, not a step-by-step tutorial: it says what you need
and where to start, and links to the official documentation for the
steps, which would go stale every time a provider redesigns its
console. Model Compass does not replace that documentation (`VISION.md`).

## `openai#direct-api`

The API is billed and managed separately from any ChatGPT subscription.

1. Create/use an OpenAI platform account.
2. Add a payment method under API billing settings.
3. Generate an API key.
4. Follow the official docs for your first call: [OpenAI API docs](https://developers.openai.com/api/docs).

Source: [Is API usage included in ChatGPT subscriptions?](https://help.openai.com/en/articles/8156019-is-api-usage-included-in-chatgpt-subscriptions-even-if-i-have-a-paid-chatgpt-account), consulted 2026-08-11.

## `openai#chatgpt-subscription`

ChatGPT's own apps (web, desktop, mobile) under a paid ChatGPT plan, with
no API key. Usage draws from the plan's limits, which OpenAI does not
publish in tokens.

1. Subscribe to ChatGPT Plus (USD 20 a month) or one of the three Pro
   tiers (USD 100, 200 or 500 a month) at [chatgpt.com/pricing](https://chatgpt.com/pricing/).
2. Pick the model in ChatGPT; the plan comparison table on the pricing
   page shows which models each plan includes.
3. API usage is not included in any ChatGPT plan and is billed to a
   separate API account (see `openai#direct-api`).

Sources: [ChatGPT pricing](https://chatgpt.com/pricing/), [What is ChatGPT Plus?](https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus) and [ChatGPT Pro tiers](https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers), consulted 2026-10-14.
