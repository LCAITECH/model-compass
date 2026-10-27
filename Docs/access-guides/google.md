# Access guide — Google

Curated pointer, not a step-by-step tutorial: it says what you need
and where to start, and links to the official documentation for the
steps, which would go stale every time a provider redesigns its
console. Model Compass does not replace that documentation (`VISION.md`).

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
   Google AI Plus (US $4.99 a month) also includes the Gemini app, with
   Gemini 3.6 Flash but not Gemini 4 Argon.
2. Open the Gemini app with that account and pick the model.
3. The app quota is not usable through the Gemini API; API use is billed
   separately (see `google#direct-api`), although the plans include
   Google Cloud credits that apply to it.

Sources: [Google AI Pro](https://support.google.com/googleone/answer/14534406?hl=en) and [Google AI plans](https://one.google.com/intl/en_us/about/google-ai-plans/), consulted 2026-10-14; Google AI Plus from the same plans page and [Google AI Plus](https://support.google.com/googleone/answer/16548195), consulted 2026-10-22.

## `google#ai-studio`

Currently listed as a Google AI Pro/Ultra benefit.

1. Subscribe to Google AI Pro or one of the two Ultra tiers (Google One). Ultra has the highest limits for the newest models (for example Gemini 4 Argon); the free plan does not include them.
2. Open Google AI Studio with that account.
3. If you link a paid API key inside AI Studio, its usage is billed
   separately as API usage.
4. The plan's AI Studio quota covers the AI Studio web interface only.
   AI Pro and Ultra do include monthly Google Cloud credits (USD 10 on
   Pro, 40 on Ultra 5x, 100 on Ultra 20x, through the Google Developer
   Program) that apply to Cloud services, including the Gemini API.

Sources: [Google One restrictions](https://support.google.com/googleone/answer/16105039?hl=en-en), consulted 2026-08-11; [Google AI plans and the Gemini API](https://ai.google.dev/gemini-api/docs/google-ai-plans), consulted 2026-10-17.

## `google#antigravity`

Google Antigravity, Google's agentic development platform (app, CLI, IDE
and IDE extensions), signed in with a Google AI plan. Which models you
can pick depends on the plan; usage draws from a quota refreshed every
five hours and capped weekly, not published in tokens.

1. Subscribe to Google AI Pro or one of the two Ultra tiers for models
   such as Gemini 4 Argon; the free plan and Google AI Plus get a smaller
   model set. On Pro, Google lists Argon for paid plans, or on trial with
   eligible premium devices.
2. Install Antigravity and sign in with that account
   ([Quickstart](https://antigravity.google/docs)).
3. Pick the model in the model selector.
4. On Pro and Ultra, usage beyond the quota can draw on purchased AI
   credits. Antigravity offers no bring-your-own-key option, and its quota
   is not usable through the Gemini API.

Sources: [Antigravity models](https://antigravity.google/docs/models) and [Antigravity plans](https://antigravity.google/docs/plans), consulted 2026-10-22 and 2026-10-27.
