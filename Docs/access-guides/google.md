# Access guide — Google

Curated pointer, not a step-by-step tutorial — see
`Docs/ACCESS_ADVISOR_AUDIT_2026-08-11.md`, Part 5.4, for why.

## `google#direct-api`

Requires a Google Cloud project with Cloud Billing linked for paid
tiers.

1. Create/use a Google Cloud project.
2. Link a Cloud Billing account (a small prepay may be required).
3. Generate an API key via Google AI Studio or the Cloud Console.
4. Follow the official docs for your first call: [Gemini API docs](https://ai.google.dev/gemini-api/docs?hl=es-419).

Source: [Billing](https://ai.google.dev/gemini-api/docs/billing?hl=es-419), consulted 2026-08-11.

## `google#ai-studio`

Currently listed as a Google AI Pro/Ultra benefit.

1. Subscribe to Google AI Pro or Ultra (Google One).
2. Open Google AI Studio with that account.
3. If you link a paid API key inside AI Studio, its usage is billed
   separately as API usage.
4. The plan's AI Studio quota covers the AI Studio web interface only.
   AI Pro and Ultra do include monthly Google Cloud credits (USD 10 on
   Pro, 40 on Ultra 5x, 100 on Ultra 20x, through the Google Developer
   Program) that apply to Cloud services, including the Gemini API.

Sources: [Google One restrictions](https://support.google.com/googleone/answer/16105039?hl=en-en), consulted 2026-08-11; [Google AI plans and the Gemini API](https://ai.google.dev/gemini-api/docs/google-ai-plans), consulted 2026-10-14.
