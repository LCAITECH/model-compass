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

## `google#gemini-app`

The Gemini app (web and mobile) under a Google AI plan. Usage draws from
the app quota, which Google does not publish in tokens; Ultra 5x and
Ultra 20x give 5x or 20x the AI Pro quota.

1. Subscribe to Google AI Pro or one of the two Ultra tiers (Google One),
   at [Google AI plans](https://one.google.com/intl/en_us/about/google-ai-plans/).
2. Open the Gemini app with that account and pick the model.
3. The app quota is not usable through the Gemini API; API use is billed
   separately (see `google#direct-api`), although the plans include
   Google Cloud credits that apply to it.

Sources: [Google AI Pro](https://support.google.com/googleone/answer/14534406?hl=en) and [Google AI plans](https://one.google.com/intl/en_us/about/google-ai-plans/), consulted 2026-10-14.

## `google#ai-studio`

Currently listed as a Google AI Pro/Ultra benefit.

1. Subscribe to Google AI Pro or one of the two Ultra tiers (Google One). Some models are Ultra-only here (for example Gemini 4 Argon).
2. Open Google AI Studio with that account.
3. If you link a paid API key inside AI Studio, its usage is billed
   separately as API usage.
4. The plan's AI Studio quota covers the AI Studio web interface only.
   AI Pro and Ultra do include monthly Google Cloud credits (USD 10 on
   Pro, 40 on Ultra 5x, 100 on Ultra 20x, through the Google Developer
   Program) that apply to Cloud services, including the Gemini API.

Sources: [Google One restrictions](https://support.google.com/googleone/answer/16105039?hl=en-en), consulted 2026-08-11; [Google AI plans and the Gemini API](https://ai.google.dev/gemini-api/docs/google-ai-plans), consulted 2026-10-14.
