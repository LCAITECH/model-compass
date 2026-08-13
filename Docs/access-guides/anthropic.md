# Access guide — Anthropic

Curated pointer, not a step-by-step tutorial — see
`Docs/ACCESS_ADVISOR_AUDIT_2026-08-11.md`, Part 5.4, for why. Links to
official documentation for the actual steps; Model Compass does not
replace it.

## `anthropic#direct-api`

Requires an API key, billed and managed separately from any Claude
consumer plan.

1. Create/use an Anthropic account.
2. Set up billing in the Console.
3. Generate an API key.
4. Follow the official docs for your first call: [Claude Platform home](https://platform.claude.com/docs/en/home).

This same API key also works with [Claude Code](https://code.claude.com/docs/en/overview)
(the terminal/IDE/desktop coding tool) -- Claude Code isn't a separate
billing path, it's a client that authenticates with either this API
key or a Claude subscription (see `anthropic#claude-subscription`
below).

Source: [Pricing](https://platform.claude.com/docs/en/about-claude/pricing), consulted 2026-08-11.

## `anthropic#claude-subscription`

Claude.ai and Claude Code can both be used under a paid Claude
subscription instead of an API key -- usage draws from the plan's
shared weekly limit ("usage credits"), not per-token billing.

1. Subscribe to Claude Pro or Claude Max at [claude.com/pricing](https://claude.com/pricing).
2. Sign in to [Claude.ai](https://claude.ai/) or [Claude Code](https://code.claude.com/docs/en/overview) with that account -- no separate API key needed for this path.
3. Model availability and the exact usage-credit split per model change over time; check the pricing page's comparison table for current terms.

Source: [Pricing](https://claude.com/pricing), consulted 2026-08-13.

## `anthropic#aws-bedrock`

Claude models on Amazon Bedrock are billed through AWS, not Anthropic
directly.

1. Create/use an AWS account with billing set up.
2. In the Bedrock console, request access to the specific Claude model.
3. Use the Bedrock Converse or InvokeModel API with your AWS
   credentials -- no separate Anthropic API key needed.
4. Follow the official docs for your first call: [Supported foundation models in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html).

Source: [Amazon Bedrock model cards](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html), consulted 2026-08-13.

## `anthropic#gcp-vertex`

Claude models on Google Cloud Vertex AI are billed through Google
Cloud, not Anthropic directly.

1. Create/use a Google Cloud project with Cloud Billing enabled.
2. Enable the specific Claude model in Vertex AI's Model Garden
   (Partner Models).
3. Call the model through Vertex AI's standard prediction API, using
   Google Cloud authentication (API key or Application Default
   Credentials).
4. Follow the official docs for your first call: [Anthropic Claude models on Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude).

Source: [Anthropic Claude models on Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude), consulted 2026-08-13.

## `anthropic#azure-foundry`

Claude models in Microsoft Foundry are billed through Azure
Marketplace, not Anthropic directly.

1. Have a paid Azure subscription with an active pay-as-you-go billing
   method, in a supported billing region (some subscription types --
   student, free-trial, sponsored-credit-only -- aren't eligible).
2. Create a Microsoft Foundry project.
3. Deploy the Claude model from the Foundry model catalog, accepting
   the Azure Marketplace terms.
4. Call it via the Claude Messages API using either an API key or
   Microsoft Entra ID, following the official docs: [Deploy and use Claude models in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/how-to/use-foundry-models-claude).

Source: [Deploy and use Claude models in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/how-to/use-foundry-models-claude), consulted 2026-08-13.
