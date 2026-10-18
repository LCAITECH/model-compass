# CHANGELOG.md — Model Compass

What changed, and why — in plain language. This is not a git log and
it doesn't require reading code to follow: it's the answer to "what
happened this week and why does it matter," for anyone following the
project, not just contributors.

For the technical detail behind any entry, see the linked commits. For
*why* a decision was made the way it was (not just that it was made),
see the relevant doc — `IMPLEMENTATION_NOTES.md` for schema/dataset
friction, `DESIGN_NOTES.md` for visual decisions, `docs/models/` for
why a specific model's data looks the way it does.

Entries are dated, newest first, tagged with the project version at
the time (see `pyproject.toml`) — note the version hasn't been bumped
per entry yet, since the project is still pre-1.0 and hasn't adopted a
release-per-version discipline. That may change once there's a first
public release to version against.

---

## 2026-10-17 — A review log, so the catalog bot stops repeating what was already checked

**Documentation only. No change to the engine, the dataset or the schema.**

- **The problem.** The bot already compared its findings with `main`, which only covers what ended up as a dataset change. News that was checked and needed no change (a price that was already right, a field the schema has no place for, a model waiting on an owner decision) left no trace, so it came back in the next digest.
- **A log of what was checked.** `Docs/CATALOG_NEWS_LOG.md` records each item with an outcome (applied, no change, not admitted, waiting for the owner, outside scope) and what was checked. Only the owner or their reviewer writes to it, after reading the provider's own page; the bot reads it and never edits it. It records outcomes, never values: nothing is copied from it into a model file.
- **The bot's rule.** `CATALOG_BOT.md` has a new section: look an item up in the last 60 days of the log before reporting it; if the provider's page still says what the entry records, don't repeat it; new evidence (a new official page, price, date or snapshot) reopens it. It also lists what isn't worth reporting: funding, policy, lawsuits, research, voice, image or video models, and hosting platforms.
- **First entries.** The 2026-10-17 review: the Argon correction below, DeepSeek-V4.1-Flash-1017 (price already right), Claude Opus 5.5 fast mode (no field in the schema), two retirement claims that match nothing in the catalog, and the open-weights and new-provider releases that wait for an owner decision.
- **Tests:** none affected; 343 pass.

---

## 2026-10-17 — Gemini 4 Argon in AI Studio is included with Google AI Pro

**Dataset correction. No change to the engine or the schema.**

- **Argon in AI Studio no longer needs Ultra.** Google updated its plans and pricing pages on 2026-10-16: Google AI Pro now lists Gemini 4 Argon, and only the free plan is excluded. We had recorded it as Ultra-only. The AI Studio route now accepts AI Pro as well as both Ultra tiers (Ultra keeps the highest limits), so a developer with AI Pro sees it as available instead of "needs onboarding".
- **What did not change:** the Gemini API route and its price ($2/$10 through 2026-11-30, then $4/$20) are as before; the plan's quota still applies only inside the AI Studio web interface and API use is billed separately. The API route's note no longer says "or with Google AI Pro".
- **Tests:** 343 pass (one new); the two tests that assumed "Ultra only" now expect AI Pro too.

---

## 2026-10-16 — "What if…" on the result page

**Interface only. No change to the engine, the dataset or the schema.**

- **Try another budget or priority order without starting over.** A panel under the winner's card lets you pick one of the four budget levels and reorder, add or remove up to three priorities. The decision graph redraws with the engine's answer for that context, the dots move between rings, and one sentence says what changed: the winner, how many models qualify, who enters or leaves the top alternatives, and whether the old and new winners are practically tied.
- **"What would change the answer?"** runs every single-step change (the other budget levels, each other priority first, swapping the top two) and lists only the ones that give a different winner, each with a click to apply it. If none does, it says the winner holds.
- **The link follows what you are looking at.** The address and "Copy link" show the scenario; "Back to my context" restores both. The winner's card on the left stays your original result, and the panel says so.
- **What it does not do:** no scores, percentages or confidence figures; a change is a different named winner. Language is not a control, and with a dollar budget (which never filters the ranking) only priorities can be explored.
- **Under the hood:** two JSON endpoints (`/whatif`, `/whatif/neighbors`) that run the same `evaluate` and `explain`; the graph's data now comes from one builder used by the page and the endpoint; `graph.js` was split into three files so the graph can be redrawn. Pages render the same elements as before (checked on seven results).
- **Tests:** 342 pass (24 new).

---

## 2026-10-15 — Docker image and deploy guide

**Tooling only. No change to the engine, the dataset or the site.**

- **A container for the public instance.** One image, one worker, no database and no background work. It is meant to sit behind a Cloudflare Tunnel that already runs on the host: no port is opened on the machine, Cloudflare provides the HTTPS, and the container is capped at 256 MB of memory and half a CPU so it does not crowd other projects (the app measured about 60 MB in use after a batch of requests).
- **A step-by-step guide** in `deploy/README.md`: first deploy, publishing the hostname, updating, and rolling back. Updating prices, models or retirements ships the same way as the code: the dataset is read when the app starts, so a rebuild picks it up.
- **Docker is new tooling here**, used only for deploying; development still runs with `pip install -e ".[dev]"` and `uvicorn`.
- **Not built yet.** It was checked by running the app from a tree holding only what the image copies, with a fresh Python 3.13 environment of just the runtime dependencies (FastAPI 0.143, Starlette 1.8): the landing, a static file, the comparator, the plans page, a recommendation and a 404 all answered correctly. The first real build happens on the server.

---

## 2026-10-15 — Results have their own link

**Interface only. No change to the engine or the dataset.**

- **Why:** a recommendation could not be sent to anyone, bookmarked or reopened: it only existed as the answer to the form.
- **What changes:** the form now puts the context in the address (empty fields left out), so every result has a URL that rebuilds it. A "Copy link to this result" button sits with the result's other links. Because the engine is deterministic, the link shows the same recommendation, run on the catalog of the day it is opened: if a price or a model changed in between, so can the result, and the button's note says so.
- **Kept working:** results sent by the old form still render and get their link in the address bar; an address with no context goes back to the form, and one with an incomplete context shows the form with what is missing.
- **Tests:** 318 pass (5 new).

---

## 2026-10-15 — Full audit: dead CSS out, light theme readable, access notes rewritten

**Interface, dataset and documentation. The ranking is unchanged.**

- **What was checked:** every code file against the 400-line limit (none over), unused code and files, repeated code, broken links and references, every page and link of the running site, text contrast in both themes, and the dataset against what the site shows.
- **Light theme:** cyan text was barely readable on white (2.3:1, the minimum is 4.5:1) in "Stop guessing.", the catalog radar labels and the comparator's "new" dates; it uses a darker cyan in the light theme now, and the grey for secondary text is a little darker. The dark theme, the default, didn't change and already passed.
- **Cleaner styles, same look:** an old block of landing-page styles nobody used anymore is gone, and every dark-theme color is defined once instead of twice. Every element on five pages was compared before and after, in both themes: identical.
- **Access notes written for people:** the notes under each access route (billing, requirements, region) had internal audit wording in them ("primary evidence.source_url", "read directly on…"), and two were out of date. They are plain sentences now; the audit history stays in each model's notes.
- **Mistral Large 3:** its maximum output was a copy of its context window and had never been checked against a source. Mistral publishes no maximum, so the catalog says so now.
- **Documentation:** two links that broke on GitHub (a lowercase folder name) are fixed, and 24 files no longer point to research documents that were never published.
- **Smaller:** the comparator's search box shows the same focus ring as the other inputs; two repeated form fields and two pill styles share their code.
- **Tests:** 313 pass.

---

## 2026-10-15 — Gemini 3.1 Pro Preview is in the Gemini app

**Access catalog only. Rankings unchanged.**

- **Why it was missing:** Google's plan pages offer "Gemini 3.1 Pro" in the Gemini app, and the catalog's entry is called "Gemini 3.1 Pro Preview", so the rule that a plan must name the exact model kept it out.
- **What settled it:** Google's own list of Gemini API models gives the name "Gemini 3.1 Pro" to `gemini-3.1-pro-preview`, its only 3.1 Pro model. The project owner decided that a name the provider itself gives a model id counts as naming it.
- **What changes:** the model now shows the Gemini app route (Google AI Pro and both Ultra tiers) in the access section and on "Subscription or API?". As with every app route, Google doesn't say the app runs the same version as the API. The free Gemini app doesn't include it.
- **Tests:** 313 pass (99 access routes).

---

## 2026-10-15 — Error pages, a header that fits on phones, a readable decision graph, new screenshots

**Interface only. No change to the engine or the dataset.**

- **Error pages:** an address that doesn't exist, or a result page opened again from its link, used to show a raw line of JSON. Both now show the site's own page; opening a result without its form takes you back to the form. A server error gets the same kind of page, without technical details.
- **Phones:** on a 375 px screen the header squeezed the site name into a narrow column and pushed the theme button off the edge. The buttons now sit beside the name and the two links get their own line. Every page was checked at 340, 375 and 768 px in an emulated browser; no real phone, Firefox or Safari yet.
- **The decision graph can be read:** its rings spin, so a dot's details vanished within a second or two of hovering it. Clicking or tapping any dot, excluded ones included, now opens a card that stays open until you close it, with all of that model's reasons and a link to compare it with the winner; the rings stop while it is open. That link also had been going to the wrong page since the "Subscription or API?" link was added; it goes to the comparator again.
- **Access requirements read correctly:** "an AWS account", "an Azure account", "a Google Cloud account" instead of "a AWS account".
- **The background animation was measured:** about 0.2 ms of work per frame on the landing page, far below what a frame allows. It already stops when the tab is hidden or effects are off.
- **README:** its screenshots predated the redesign; all four were retaken, and the comparator and "Subscription or API?" got their own.
- **Tests:** 313 pass (new: error pages, the three cloud-account labels).

---

## 2026-10-15 — Four new models: Meta's Muse Wonder and Muse Spark 1.3, Qwen3.8-Flash, Qwen3.7-Plus

**Dataset and access catalog. Rankings change.**

- **Meta, a new provider:** Muse Wonder ($4/$20, in preview, Meta's most capable model for long agentic and coding work) and Muse Spark 1.3 ($1.25/$4.25, Meta's model for volume work), both through Meta Model API with a new access guide. Meta publishes no language list, so both carry a short, curated one (English, Spanish, Portuguese, French, German, Italian) that keeps them out of languages nobody has confirmed. Muse Spark 1.3 is marked without audio, as Meta itself says audio isn't fully supported in that version. Its cheaper "Contributor" option, where Meta trains on your content, is described in its notes and not used for ranking.
- **Alibaba Cloud:** Qwen3.8-Flash ($0.15/$0.47) and Qwen3.7-Plus ($0.40/$1.60 for inputs up to 256k), International pricing, like Qwen3.8-Max.
- **What changes in results:** Qwen3.8-Flash is now an alternative in cost-first contexts (Claude Haiku 5.5 still wins at $0.60 against $0.62) and wins Korean-language contexts; Muse Wonder joins the "also strong" group for reasoning-first contexts. Under a high budget 30 models qualify.
- **Not added yet:** Mistral Large 4, whose license is "Coming soon" and whose weights are due at the end of October, with a sale price that has no end date. Re-checked after 2026-10-31. Qwen3.7-Flash is not in Alibaba's catalog.
- **Ratings:** the editorial ratings of the four models were proposed with the providers' own words as evidence and approved by the project owner.
- **Tests:** 307 pass. Catalog counts and the expectations that list catalog members were updated from real engine runs; one web scenario whose winner became a tie was replaced with a real one that still has an outright winner.

---

## 2026-10-15 — Free access now counts the providers' free apps

**Schema definition (owner decision) and dataset. The ranking is unchanged.**

- **Why:** Claude Haiku 5.5 and Claude Sonnet 5.5 can be used on Claude.ai's Free plan and GPT-6 Luna on ChatGPT's Free plan, and the catalog said none of them had free access. It wasn't a data error: the field had only ever counted free API tiers, like the one Google offers for several Gemini models.
- **New definition:** "free access" means the exact model can be used without paying, either through a free API tier (even a heavily rate-limited one) or through the provider's free app plan when the provider's own page names that model. A paid plan never counts, however cheap. Each model's audit doc says which of the two it is, because a free chat app is not a way to build an application on the model.
- **What changes:** the three models now have free access, and so does DeepSeek V4 Pro, which DeepSeek's free app offers in "Expert Mode". Under a low budget, Claude Haiku 5.5 is the cost-first winner and its result now carries the "Free access also documented" chip, linking to notes that say it is the Claude.ai app, not the API.
- **Not counted:** GPT-5.6 Terra, which ChatGPT Free offers only inside Work and Codex in the desktop app (owner's call); Mistral Large 3, Qwen3.8-Max and Gemini 4 Argon, which no free plan page names.
- **Tests:** 303 pass; the one test that asserted the old fact on the real page now asserts the new one, same scenario.

---

## 2026-10-15 — Gemini 2.5 stops being recommended

**Schema (owner-approved: a `restricted` lifecycle status), dataset and Decision Engine. Rankings change.**

- **Why:** Google still serves Gemini 2.5 Pro, Flash and Flash-Lite and says they are not deprecated, but limits them "to users who have actively used them in the past" and points new projects to Gemini 3.5 Flash-Lite or 3.8 Flash. Gemini 2.5 Flash-Lite was the engine's #1 for cost-first contexts, for developers who most likely cannot use it.
- **New status `restricted`:** set on the three models. The engine excludes them the same way it excludes deprecated ones, with the reason "limited by its provider to developers who already used it" and, where set, the model to use for new projects (3.5 Flash-Lite for 2.5 Flash-Lite, 3.8 Flash for 2.5 Flash; that pairing is the project owner's, since Google gives one piece of advice for all three).
- **On the site:** in the result they appear among the excluded models with the reason (also in the decision graph's tooltip); in the comparator they carry an "Existing users only" badge and status, with a "Swap in" for the successor. They are not listed as leaving the catalog, because they are not.
- **Removed:** the Gemini 2.5 Pro route through AI Studio, which no plan page supports.
- **What changes in results:** Claude Haiku 5.5 now wins cost-first contexts (tied with GPT-6 Luna at $0.60 per 1M input plus output, first by dataset order). Under a high budget 26 models qualify instead of 29.
- **Tests:** 303 pass. Changed expectations were re-derived from real engine runs; two tests that no longer tested what they claimed were replaced with real cases.

---

## 2026-10-15 — Subscription or API?

**Schema (owner-approved: plan prices, multipliers and API credits), dataset, Access Advisor and interface. The ranking is unchanged: nothing about a plan affects which model is recommended.**

- **A new page, `/plans`:** pick a model and see two paths. On one side, what a monthly amount buys on the API, measured at list prices. On the other, the plan, drawn in fog because no provider publishes its limit in tokens; the page shows only what the provider does publish (price, its own "5x Pro" multiplier, included API credits and what they buy of that model). The verdict sits where the paths meet: use the API to build an app or automation; the API is the only way in when no plan names the model; with your own monthly usage, its exact API cost against the plan; without usage, no cost verdict at all. The result page links to it with the recommended model prefilled.
- **Plans now carry facts you can compute with:** US list price (editable on the page, since regional prices differ), the provider's own usage multiplier, and included API credits. Claude Max and Google AI Ultra split into their 5x and 20x tiers, and ChatGPT Plus and the three Pro tiers were added: 10 plans.
- **Ten new access routes**, only where a plan page names the exact model: Claude Opus 5.5 and Haiku 5.5 on Claude plans, Gemini 4 Argon in the Gemini app and (Ultra only) in AI Studio, and six GPT models in ChatGPT. Gemini 3.1 Pro Preview gets no Gemini app route: the plan pages say "Gemini 3.1 Pro", which is not the catalog's name. 95 routes.
- **The Access Advisor gained `compare_plans`**, which reads plans and routes by their attributes and never imports the ranking.
- **Tests:** 295 pass (+32).

---

## 2026-10-14 — Subscription facts corrected

**Dataset and docs only, no schema change. Found while researching the upcoming "subscription or API" section.**

- **Claude Max now includes API credits:** USD 100 a month on Max 5x and USD 200 on Max 20x since 2026-10-07, in a separate Console balance that does not roll over and does not cover Claude Code. The catalog said the plan had none.
- **Google AI Pro and Ultra include Google Cloud credits** usable on the Gemini API (USD 10, 40 or 100 a month). The catalog said they had none.
- **Fable 5 and 5.1 are included in Claude Max, not Pro.** On Pro they are billed at API rates through usage credits, so the Access Advisor no longer lists Claude Pro as a way to reach them.
- **Gemini 2.5 Pro in AI Studio is now marked unconfirmed:** no current plan page names it, and Google limits Gemini 2.5 to developers who already used it.
- Details and sources: `IMPLEMENTATION_NOTES.md`, Iteration #31. Tests: 263 pass (two updated for the corrected text).

---

## 2026-10-14 — The model comparator, rebuilt

**Interface only: `decision/`, the dataset and the schema are unchanged. The improvements are the set the project owner picked from a list grounded in the old page.**

- **Picker:** the selected models are chips, each with its own color and a remove button; "Add a model" is a searchable list where deprecated models are marked. The context folds away unless it is filled in. It is still a plain form, so it works without JavaScript.
- **The engine's verdict, drawn:** with a context, every model in the catalog appears as a dot on the ring the engine put it in (the same rings as the result page's decision graph), the selected models are lit and numbered with their place, and a podium lists them in the engine's order with its reasons. If the engine's #1 is not in the selection, it can be added with one click.
- **Quality constellations:** one per model, four axes (one per editorial rating) and four fixed rings for low to very high. A point always sits on a ring, so the drawing stays as discrete as the scale; the page says the shape is not a score.
- **"Only differences":** a switch hides the rows where every selected model reads the same (often a third of them).
- **Lifecycle:** release date (with "New" for the last 30 days), days left to a shutdown or to the end of an introductory price, and a "Swap in" button that replaces a model with its named successor while keeping the context.
- **What a monthly amount buys:** type an amount and each model shows how many tokens it buys if spent all on input or all on output, plus the figure at the price that applies after a promotion. Two bounds, never a usage estimate.
- **Prices and limits as bars**, relative to the selected models only (never to an assumed maximum), with the exact ratio against the cheapest ("20×").
- **Access by surface:** direct API, cloud platforms, subscription apps and studios each get their own row, with chips linking to the access guide and naming the plans. Where no route is documented the page says "Not documented", not "No".
- **Layout:** model columns read as cards with a header that stays pinned while scrolling; on phones each model is a swipeable card. Light and dark themes.
- **Housekeeping:** the view logic is split into four modules to stay under the 400-line limit. **Tests:** 263 pass (+16).

---

## 2026-10-14 — Catalog radar: new releases, introductory prices and retirements on the site

**Schema (owner-approved: `lifecycle.release_date`) and interface. The Decision Engine is unchanged: none of this affects rankings.**

- **Release dates for all 39 models** (`lifecycle.release_date`), read from each provider's own pages, so the site can say what is new without guessing.
- **Badges on every model card, in the comparator header and in the decision graph:** "New" (released in the last 30 days), "Intro price" (with its end date and days left) and "Deprecated"/"Retiring" (with the shutdown date). In the graph they are rings around the dots, with a legend entry only for what appears.
- **Floating notices on the result page:** when the recommended model is on an introductory price, the ranking says it used today's price and what it costs afterwards; when it has a shutdown date or is a fresh release, the visitor is told; and a "Leaving the catalog" notice lists every model on its way out, with its date and successor. The notices fold away by themselves after a few seconds so they never cover the result.
- **Catalog radar on the landing page:** a ticker in the hero and three panels (new releases, introductory prices, leaving the catalog) with day counts. Every number is days between a published date and today; nothing is estimated.
- **Housekeeping:** `result.html` (429 lines, over the project's 400-line limit since the immersive redesign) was split into six partials with byte-identical output in seven scenarios.
- **Tests:** 247 pass, including the notices with today's date pinned.

---

## 2026-10-14 — Deprecated models stop being recommended

**Touches the schema, the dataset and the Decision Engine (owner-approved schema change).**

- **New `lifecycle` block in every model** (`SCHEMA.md`, Lifecycle): `status` (`active` or `deprecated`), `shutdown_date` and `replacement`, taken from each provider's own deprecations page. All 39 models were re-checked against those pages on 2026-10-14.
- **The engine no longer recommends deprecated models.** Until now a model its provider is shutting down could still win: `gpt-5-nano` (off on 2026-12-11) was the top pick for cost-first contexts. Seven models are now excluded for that reason alone, and the result, the decision graph and the comparator say when each one shuts down and which model replaces it: Claude Sonnet 4.5 (2026-11-30, use Sonnet 5.5), GPT-5, GPT-5 Mini and GPT-5 Nano (2026-12-11, use the GPT-5.6 tiers), GPT-4o (2027-01-14, use GPT-6 Luna), and Gemini 3.5/3.7 Flash (Google already routes them to 3.6/3.8 Flash).
- **A date alarm for the dataset.** Introductory prices and shutdown dates used to be reminders in a notes file. The test suite now fails from the first day one has passed and warns during the 30 days before. The engine itself never looks at the calendar, so the same input still gives the same answer on any day.
- **Comparator:** a new "Lifecycle" row (active or deprecated, shutdown date, successor).
- **Found along the way:** Google now limits Gemini 2.5 Pro, Flash and Flash-Lite to developers who already used them. Recorded in their model notes, not modeled yet (`IMPLEMENTATION_NOTES.md`, Iteration #29). It matters because Gemini 2.5 Flash-Lite is now the cheapest model the engine recommends.
- **Tests:** expected rankings that changed were re-derived from real engine runs (29 models qualify under a high budget instead of 36). 233 tests pass.

---

## 2026-10-14 — Immersive web redesign

**Interface only: `decision/`, the dataset, the schema and every `.py` file are unchanged. The first redesign layered effects over the same layout; this one changes the composition.**

- **Neural field:** a fixed canvas behind every page with depth, pointer parallax, pulses of light travelling along the links and a shock wave on click; calmer on pages other than the landing.
- **Landing:** a full-viewport hero with a very large headline and a start button; the decision form became a four-step wizard in a glass panel (use case, priorities, budget, optional access) with a progress bar and transitions. Without JS every stage is visible and the form behaves as before.
- **Calculating transition:** a full-screen seven-layer network lights up left to right, pulses ride its connections, and it folds into one node that flashes into the result. No percentages, counts or ETA; captions name the engine's real steps.
- **Result as a decision graph:** the recommended model sits at the centre and every other model in the catalog is a dot whose ring is its real standing for the visitor's context (top alternatives, practically tied, also qualify, excluded). Hover shows price and the engine's reasons; click opens the comparison with the winner. Angle within a ring carries no meaning, and the legend says so. `result.html` lists the engine's own output in a hidden `.graph-data` list and `graph.js` only draws it.
- **Effects are on by default and deliberately ignore `prefers-reduced-motion`** (owner decision); a header switch turns them off and the choice is kept in the browser (`mc-effects`). Dark is the default theme.
- **Test change, for review:** `test_web_alternatives` now counts a model's name in the visible page, excluding the hidden `.graph-data` list that repeats every name on purpose. The scenario is unchanged. 206 tests pass.

---

## 2026-10-14 — Web redesign and model comparator

**Interface only: `decision/`, the dataset and the schema are unchanged.**

- **Redesign:** light and dark themes (system preference plus a saved toggle, no flash on load); a "calculating" transition with a small neural network that lights up left to right and folds into one node (no percentages or counts, captions name the engine's real steps); a landing hero with a network that reacts to the pointer; the recommended model's name decrypts in place and the cards below enter in a cascade. Everything honors `prefers-reduced-motion`: with it, the form submits at once and the page is static.
- **Model comparator** at `/compare` (`FEATURES.md`, "Static Model Comparator"): 2-4 models side by side from stored fields, with a "best in row" mark only where values differ. With an optional context it also shows the engine's own result per model (qualifies or why not, place among qualifying models, reasons), unchanged and without a score. The result page links to it with the context prefilled.
- Tests: 206 pass (+18: comparator, context fit, link carrying the context).

---

## 2026-10-14 — Gemini 4 Argon admitted (39 models)

**Google's new flagship, with every objective field re-read from raw official HTML.**

- **Gemini 4 Argon** (`gemini-4-argon`, "Stable" on the models index, page updated 2026-10-13): 1,048,576-token context, `max_output` 65,536 (default; up to 1,048,576 with long decode, recorded in the model doc), text/image/video/audio/PDF in, text out, function calling, structured outputs.
- **Price:** introductory $2.00 / $10.00 per 1M through 2026-11-30, then $4.00 / $20.00. Stored with `effective_until: "2026-11-30"`; **nothing flips it automatically, so the entry goes stale on 2026-12-01.** Source: https://ai.google.dev/gemini-api/docs/pricing
- **Access:** one route, the Gemini API with billing linked. The pricing page says it is not available on the Free tier or on Google AI Pro, so `has_free_access: false` and no subscription route.
- **Editorial, proposed for owner review:** reasoning and coding `very_high`; creative writing `medium`; instruction following `high` (no source for a higher call). Languages not published; the curated Gemini set is reused.
- Catalog grows 38 → 39 models, 84 → 85 routes. Tests updated only where the new model legitimately changes counts and rankings (`test_loader`, `test_access_loader`, `test_explainer_also_strong`, `test_explainer_alternatives_outranked`); 188 pass.

See `Docs/models/gemini-4-argon.md`.

---

## 2026-10-14 — GPT-4o fully deprecated; Gemini 3.7/3.5 Flash lifecycle wording refreshed

**Daily audit (2026-10-14), official provider docs only. Docs only, YAML kept (Iteration #22 remove-vs-flag still open).**

- **`gpt-4o`:** OpenAI announced on 2026-10-14 the deprecation of the remaining GPT-4o snapshots (`gpt-4o-2024-08-06`, `gpt-4o-2024-11-20`), shutting down **2027-01-14**, replacement `gpt-6-luna`. With `gpt-4o-2024-05-13` already shutting down 2026-10-23, every GPT-4o text snapshot is now deprecated and the model page labels GPT-4o "Deprecated". Lifecycle table updated in `Docs/models/gpt-4o.md`; price unchanged ($2.50/$10.00). Sources: https://developers.openai.com/api/docs/deprecations and https://developers.openai.com/api/docs/models/gpt-4o
- **`gemini-3.7-flash` / `gemini-3.5-flash`:** Google's deprecations page (updated 2026-10-12) now shows shutdown **N/A** and says the endpoints are **not shutting down** and keep auto-routing to `gemini-3.8-flash` / `gemini-3.6-flash` (not selectable in AI Studio). Lifecycle notes refreshed from the 2026-10-10 "no shutdown date announced" wording. Source: https://ai.google.dev/gemini-api/docs/deprecations
- **Not admitted this pass:** Gemini 4 Argon (`gemini-4-argon`, GA 2026-10-13) is now in Google's public catalog and pricing. Admission needs owner decisions first (see `Docs/IMPLEMENTATION_NOTES.md`, Iteration #25).

---

## 2026-10-14 — `max_output` may be null (schema)

**Providers that publish no output ceiling no longer force a made-up number.**

- `operational.max_output` is now `integer | null`; the key stays required. Dataset unchanged: every existing model still has a real value.
- Why: Muse Spark, Muse Wonder and Gemini 4 Argon all failed to fit a single sourced integer (Iteration #26). The engine never read the field.
- Code: `decision/domain/ai_model.py`, `decision/loader/loader.py`. Docs: `Docs/SCHEMA.md`. Tests: `tests/test_loader_max_output.py` (+8, 187 total).

---

## 2026-10-10 — Gemini 3.7 Flash and 3.5 Flash now auto-routed to successors

**Daily audit (2026-10-10), official provider docs only. Docs only, YAML kept (Iteration #22 remove-vs-flag still open).**

- **`gemini-3.7-flash`:** Google now routes requests to `gemini-3.8-flash`; removed from the models, pricing and rate-limits pages; no shutdown date announced. Lifecycle note added to `Docs/models/gemini-3.7-flash.md`.
- **`gemini-3.5-flash`:** Google now routes requests to `gemini-3.6-flash`; same page removals; no shutdown date announced. Lifecycle note added to `Docs/models/gemini-3.5-flash.md`.
- Source: https://ai.google.dev/gemini-api/docs/deprecations

---

## 2026-10-08 — Claude Haiku 5.5 admitted (38 models)

**The new current Haiku is in, with every objective field re-read on Anthropic's own pages and each cloud's own docs.**

- **Claude Haiku 5.5** (`claude-haiku-5-5`, released 2026-10-07, GA, "Active (latest)"): 1M-token context, 128K max output, text and image input, tool calling. Retirement not sooner than 2027-10-07.
- **Two-tier pricing by prompt length**, a first for Claude: $0.10 / $0.50 per million tokens for prompts up to 100k tokens, $0.50 / $2.50 above. The dataset stores the ≤100k tier (the schema holds one rate), so the engine sees $0.60 blended (`low` tier); the >100k tier is documented in `Docs/models/claude-haiku-5-5.md`. Sources: https://platform.claude.com/docs/en/about-claude/pricing and https://platform.claude.com/docs/en/models/overview
- Quality ratings and maturity mirror `claude-haiku-4-5` (editorial; Anthropic positions it for high-volume, latency-sensitive work, not as a higher capability tier).
- Four access routes (direct API, AWS Bedrock, Google Vertex, Microsoft Foundry), each cloud confirmed on its own documentation. No Claude-subscription route (no plan tier named). Catalog grows 37 → 38 models, 80 → 84 routes.
- Tests updated only where the new low-tier model legitimately changes counts and rankings (owner-authorized for this admission).

See `Docs/IMPLEMENTATION_NOTES.md`, Iteration #24.

## 2026-10-07 — Gemini 3.8 Flash free tier; four OpenAI models admitted; lifecycle docs

**Daily audit follow-through (2026-10-06 and 2026-10-07) against official provider docs only.**

- **`gemini-3.8-flash`:** `access.has_free_access` flipped to `true`. Google's Gemini Developer API pricing page now lists Free Tier "Free of charge" for this model id (input/output/caching). Source: https://ai.google.dev/gemini-api/docs/pricing
- **Admitted (4):** `gpt-6-1-sol` ($2/$10, API id `gpt-6.1-sol`), `gpt-6-luna` ($0.10/$0.50), `gpt-5-6-terra` ($2/$12), `gpt-5-6-luna` ($0.20/$1.20). Specs from each model's official page + Flagship/pricing tables; one direct-API route each. Catalog grows 33 → 37 models.
- **Lifecycle (docs only, YAML kept — Iteration #22 remove-vs-flag still open):**
  - `gemini-3.1-flash-lite`: shutdown 2027-05-07, replacement `gemini-3.5-flash-lite` (Google deprecations).
  - `gpt-5` / `gpt-5-mini` / `gpt-5-nano` snapshots shut down 2026-12-11; `gpt-4o-2024-05-13` shuts 2026-10-23 (OpenAI deprecations).
  - `claude-haiku-4-5`: still Active; retirement floor "not sooner than 2026-10-15", no formal deprecation (Anthropic deprecations).
- Not admitted this pass: older alias `gpt-6-sol` (page defers to 6.1 Sol; Flagship table lists `gpt-6.1-sol`).

See `Docs/IMPLEMENTATION_NOTES.md`, Iteration #22 / #23.

## 2026-10-05 — DeepSeek V4.1 Flash price/vision fix; Claude Sonnet 4.5 lifecycle noted

**Urgent catalog corrections from the daily provider audit against official docs.**

- **DeepSeek Flash** (`deepseek-v4-flash`): cost updated peak cache-miss **$0.30 / $1.20** (was $0.44/$1.32); `capabilities.vision` set to `true`; display name/version aligned to DeepSeek-V4.1-Flash. Official page still accepts the legacy id `deepseek-v4-flash` but serves V4.1-Flash. Source: https://api-docs.deepseek.com/quick_start/pricing
- **Claude Sonnet 4.5** stays in the active dataset. Anthropic deprecated it 2026-09-30 (retires 2026-11-30, replacement `claude-sonnet-5-5`). Lifecycle documented in `Docs/models/claude-sonnet-4-5.md`; removal vs flag remains the open catalog-policy question in `IMPLEMENTATION_NOTES.md` Iteration #22. Source: https://docs.anthropic.com/en/docs/about-claude/model-deprecations

## 2026-10-04 — Claude Sonnet 5.5 and Claude Opus 5.5 admitted (33 models); Gemini 4 not yet admissible

**Two new Claude models are in, both confirmed on Anthropic's own pages and on each cloud's own documentation; the "Gemini 4" announcement turned out to be one gated model with no public API yet.**

- **Claude Sonnet 5.5** (released 2026-09-28): $2.00/$10.00 per million tokens, 1M-token context, 128K max output, vision and tool calling. Same price as Sonnet 5, standard rate with no introductory pricing.
- **Claude Opus 5.5** (released 2026-09-22): $4.00/$20.00, same 1M/128K limits — 20% cheaper than Opus 5, and Anthropic's overview now points to it as the default starting model. Quality ratings for both mirror their predecessors: the evidence supports the scale's existing ceiling, not a rating above it.
- Four access routes each (direct API, AWS Bedrock, Google Vertex, Microsoft Foundry), every cloud checked against its own documentation rather than just Anthropic's model page. No Claude-subscription route: Anthropic names no plan tier.
- **Gemini 4 Argon is not admitted.** It's a single model, announced 2026-09-30 and rolling out only to trusted cyber defenders; it isn't in Google's model catalog or pricing page and has no model id. No other Gemini 4 variant exists in any Google source.
- Noted, not acted on: `claude-sonnet-4-5` is now deprecated (retires 2026-11-30), `gpt-5`'s current snapshot retires 2026-12-11, and DeepSeek released V4.1-Flash. See `Docs/IMPLEMENTATION_NOTES.md`, Iteration #22.

---

## 2026-09-08 — Qwen3.8-Max admitted (31st model, first Alibaba Cloud entry); Muse Spark 1.3 held back on a real sourcing gap

**Two OpenRouter listings from a Grok tip, evaluated independently against each provider's own documentation — one cleared the bar, one didn't, for a reason worth understanding rather than working around.**

- **Qwen3.8-Max admitted.** First Alibaba Cloud entry in this catalog. Confirmed directly on Alibaba Cloud Model Studio's own model page: vision input, 1,000,000-token context window, 131,072 max output, $2.00/$6.00 per 1M tokens on the International (Singapore) pricing scope (the China/Beijing scope is materially cheaper but requires a Mainland China account). One access route: ordinary self-serve API billing, no program-membership gate like `gpt-6-astra` had.
- **A real complication surfaced and was resolved deliberately, not by assumption**: Alibaba also ships a separately-released open-weights checkpoint (`Qwen/Qwen3.8-2.4T-A95B` on Hugging Face) under overlapping "Qwen3.8-Max" naming — text-only, no vision, a smaller context window than the hosted API. Different model ID, different capabilities, per `SCHEMA.md`'s own rule for when something is a separate entry. Admitted only the hosted API product this pass; the open-weights variant is flagged as an open question for a possible second entry later, not folded in or silently skipped. Full reasoning in `Docs/IMPLEMENTATION_NOTES.md`, Iteration #20.
- **Meta Muse Spark 1.3 was not admitted.** Everything else checked out — real product (Meta Model API, first-party, OpenAI/Anthropic-SDK-compatible), $1.25/$4.25 per 1M tokens confirmed on Meta's own pricing page (matching the tip exactly), 1,048,576-token context window confirmed on multiple official pages. But every official page checked publishes exactly one combined context-window figure and never a distinct output-token ceiling — one page states outright that all three Muse Spark versions "share... a 1,048,576-token context window." `SCHEMA.md` requires `context_window` and `max_output` as two separate fields; a third-party aggregator's specific number for the latter (943,718) appears nowhere in Meta's own docs and wasn't used. Logged as a genuine open question rather than guessed — `Docs/IMPLEMENTATION_NOTES.md`, Iteration #21.

---

## 2026-09-07 — GPT-6 Astra's Trusted Access Program gate lifted, three days after admission

**The gate this catalog modeled honestly on 2026-09-04 didn't last long — OpenAI opened the model up to ordinary self-serve API access, and the route now says so.**

- Re-verified against `developers.openai.com/api/docs/pricing`, GPT-6 Astra's own model page, and the models index — all three, live, on a Grok tip. The Trusted Access Program rollout paragraph present three days ago is gone from every one of them; the model is now presented as the default recommended flagship with no access caveat, and its rate-limits table lists standard usage tiers identical in shape to every other self-serve OpenAI model. Prices unchanged.
- `dataset/access_routes/openai/gpt-6-astra-direct-api.yaml` updated in place: `RequirementKind.PROGRAM_MEMBERSHIP` → `RequirementKind.API_BILLING_LINKED`, the same requirement as `gpt-5-6-sol`'s own direct-api route. Verified both directions with `recommend_access()`: billing info alone now resolves to `CURRENTLY_ELIGIBLE`; holding the Trusted Access Program membership without billing info still correctly resolves to `REQUIRES_ONBOARDING` — the membership genuinely no longer matters to this route.
- This isn't the "Plus/Pro/Business/Enterprise access ships" scenario the admission entry anticipated (see 2026-09-04 below) — there's no subscription-plan angle here. The direct API route's own gate was lifted; edited in place rather than adding a parallel route, since it's the same surface with one changed requirement, not a second access method. Full reasoning in `Docs/IMPLEMENTATION_NOTES.md`, Iteration #19.
- The "OpenAI Trusted Access Program" checkbox has no access route behind it again — `RequirementKind.PROGRAM_MEMBERSHIP` is back to zero real usages, same as before this model's admission. Kept, not removed: same reasoning as the NVIDIA Developer Program checkbox (OpenAI could gate a future model the same way again), and unlike NVIDIA, this program did have one real, working route for three days — that's signal, not dead weight.

---

## 2026-09-06 — Full codebase audit: two display bugs fixed, silent priority duplication closed, dead-line-limit cleanup

**A full functional/visual audit of the web form (every priority combination, every budget mode, the access checkboxes) surfaced two real display bugs and a UX gap that unit tests alone hadn't caught — all three are fixed, alongside a round of pure code deduplication that changed no behavior.**

- **Fixed:** the Cost tier card showed "Very_high" instead of "Very high" for the top budget tier — `result.html` was missing the `replace('_', ' ')` step the rest of the templates already used before `capitalize`. Now handled by a shared Jinja `humanize` filter, also applied to the three other templates that had the same pattern inlined.
- **Fixed:** the "why this model" reasoning showed the raw ISO code ("Supports en with...") instead of the language's name ("Supports English with..."). `language_name()` moved from `interfaces/web/languages.py` into `decision/domain/languages.py` so `decision/explainer/` can use it directly, without `decision/` importing from `interfaces/`.
- **Fixed:** picking the same priority at two different ranks (e.g. Cost at #1 and #2) used to be silently deduplicated with zero feedback. The web form now disables an already-picked priority in the other two dropdowns as soon as it's chosen, so the ambiguous state can't be created from the UI at all. The silent-dedup fallback in `context_form.py` stays for a no-JS submission.
- **Confirmed, not changed:** GPT-6 Astra's `program_membership` access gate (see 2026-09-04 below) works correctly end-to-end — verified this time with real clicks in the browser, not just a direct function call. But under its current quality ratings it can never actually become the #1 recommendation, so a real user has no path in the live UI to ever see that access requirement rendered. Documented as a known, honest limitation of the current dataset, not a bug to fix.
- **Refactor, no behavior change:** a triplicated `_values()` helper (renamed `enum_values`) consolidated into `decision/loader/_util.py`; the `Priority -> quality attribute` mapping that `decision/explainer/` and `interfaces/web/affordability.py` each redefined separately is now one `QUALITY_DIMENSION_ATTR` constant on `decision/domain/context.py`; `tests/conftest.py` centralizes the `models`/`make_model`/`client`/`candidate_factory` fixtures and path constants that were duplicated or inlined across 8 test files.
- **Fixed the 400-line ceiling violation** (`AGENTS.md`) in the two files that had crossed it: `tests/test_web.py` (489 lines) split into `test_web_core.py` / `test_web_budget.py` / `test_web_savings.py` / `test_web_alternatives.py`; `tests/test_explainer.py` (460 lines) split into `test_explainer_reasons.py` / `test_explainer_also_strong.py` / `test_explainer_alternatives_outranked.py`. Same 170 tests, same coverage, regrouped by responsibility.
- **Left alone, deliberately:** the CSS icon-size duplication across 8 selectors in 3 stylesheets — fixing it properly means touching every icon macro plus ~14 template call sites for a purely cosmetic, zero-bug-risk cleanup, not worth the blast radius; the NVIDIA Developer Program checkbox, kept in case NVIDIA NIM gets admitted to the dataset someday.

---

## 2026-09-04 — GPT-6 Astra admitted (30th model), with an honest access gate

**OpenAI's new flagship is public-priced but not yet self-serve —
instead of excluding it or pretending the gate doesn't exist, this
release models it directly for the first time.**

- New dataset entry `gpt-6-astra`: OpenAI's own system card calls it
  "the most capable model we have ever broadly deployed." Quality
  ratings kept identical to `gpt-5-6-sol` on reasoning/coding (already
  at this dataset's ceiling), with stronger direct evidence this time
  for `instruction_following` (roughly half the alignment-flag rate of
  its predecessor across 54,000+ internal tasks).
- **Access is the real story.** OpenAI's own model page: "rolling out
  today for enterprises in our Trusted Access Program, with access
  through API and our Plus, Pro, Business and Enterprise plans coming
  in the coming days." That's neither "excluded, invite-only" (this
  catalog's existing rule for Claude Mythos 5/5.1 and Gemini 3.8 Flash
  Cyber) nor ordinary self-serve access. Asked directly rather than
  assumed: admit the model, and model the gate honestly using
  `RequirementKind.PROGRAM_MEMBERSHIP` — a piece of the schema that's
  existed since Fase 7 but had never actually been used by a route
  until now. A developer without Trusted Access Program membership
  sees this route as "requires onboarding," never "currently
  eligible" or hidden entirely.
- Added a matching "OpenAI Trusted Access Program" checkbox to the web
  form (`interfaces/web/templates/index.html`), next to the existing
  (also previously unused) NVIDIA Developer Program one, so the new
  route is actually reachable, not just theoretically valid YAML.
- No route added yet for the announced Plus/Pro/Business/Enterprise
  access — that's a promise, not documentation of something live.
  Revisit once OpenAI's own pages confirm it shipped.
- Sourced from a Grok tip, same discipline as every prior one: every
  field independently re-confirmed against OpenAI's own model page,
  pricing page, and system card before anything was added.

---

## 2026-09-02 — Gemini 3.8 Flash admitted (29th model)

**Google's third Flash release in six weeks, admitted the same day it
shipped — with its maturity rating and free-access field both
defaulted conservatively for lack of public confirmation, not
guessed.**

- New dataset entry `gemini-3.8-flash`: same introductory price as
  Gemini 3.7 Flash ($0.75/$3.75 per million input/output tokens,
  expiring 2026-12-31, reverting to $1.50/$7.50), sourced from Google's
  own announcement blog post — the model card that normally carries
  this pricing table doesn't have one this time, and the generic
  pricing page doesn't list the model yet either.
- `maturity: experimental` and `access.has_free_access: false`, both
  because the model isn't yet listed on the pages that would confirm
  otherwise (`ai.google.dev/gemini-api/docs/models` for maturity,
  the pricing/rate-limits pages for free access). Notably,
  `gemini-3.7-flash` — admitted three weeks ago under the same
  `experimental` reasoning — still isn't listed there either,
  confirming this isn't a one-off call (`Docs/IMPLEMENTATION_NOTES.md`,
  Iteration #17).
- **Gemini 3.8 Flash Cyber, the cybersecurity-specialized sibling
  announced the same day, was not admitted** — invite-only access
  (Google's "Fairwind Program"), no public price anywhere. Same bar
  every other invite-only, unpriced model in this catalog has already
  failed to clear.
- Sourced from a Grok tip, same discipline as every prior one this
  project has received: the tip pointed at the right announcement, but
  every field was independently re-confirmed against Google's own
  documentation before anything was added.

---

## 2026-09-01 — Claude Fable 5.1 admitted (28th model)

**Anthropic shipped Claude Fable 5.1 today, replacing Claude Fable 5
as the recommended top-tier model — admitted the same day, with one
access route deliberately left out.**

- New dataset entry `claude-fable-5-1`: same headline price as Fable 5
  ($10/$50 per million input/output tokens), but a 75% cheaper
  prompt-cache read rate ($0.25/MTok vs. $1.00/MTok) — Anthropic's own
  numbers put that at roughly 25% cheaper for typical workloads, up to
  roughly 45% for highly agentic ones. Quality ratings kept identical
  to Fable 5 (already at this dataset's ceiling on every dimension) —
  no evidence found to justify treating 5.1 as strictly better on any
  specific axis, so none was fabricated.
- Four access routes confirmed and added (direct API, Claude
  subscription, AWS Bedrock, Microsoft Foundry). **Google Cloud Vertex
  was not added** — Google's own Claude-on-Vertex documentation still
  only mentions Fable 5, not 5.1, as of today. Same kind of
  documentation lag already seen with Gemini 3.7 Flash's launch; the
  route will be added once Google's own page confirms it, not before.
- Claude Fable 5 stays in the catalog, unchanged, confirmed `Active`
  (not `Legacy`) on Anthropic's own lifecycle page — a third-party tip
  that suggested otherwise didn't hold up under direct verification
  (`Docs/IMPLEMENTATION_NOTES.md`, Iteration #16).
- Sourced from a Grok tip, same as the 2026-08-27 refresh below — the
  tip pointed at the right announcement, but every field was
  independently re-confirmed against Anthropic's, AWS's, and
  Microsoft's own documentation before anything was added, and one of
  the tip's specific claims (Fable 5 going "legacy") turned out to be
  wrong on direct verification.

---

## 2026-08-27 — Catalog pricing refresh (GPT-5.6 Sol, Claude Sonnet 5, DeepSeek V4)

**Four pricing facts had drifted since their last verification — all
re-checked directly against each provider's live docs before touching
the dataset.**

- **GPT-5.6 Sol** dropped to promotional pricing on 2026-08-21: $4.00
  input / $20.00 output per million tokens, guaranteed at least through
  2026-11-21, then reverting to the standard $5.00/$30.00. Uses the
  `cost.effective_until`/`cost.reverts_to` fields (`SCHEMA.md`) for the
  first time on a non-Google model.
- **Claude Sonnet 5**'s scheduled 2026-09-01 price hike to $3.00/$15.00
  has been cancelled by Anthropic — $2.00/$10.00 is now the permanent
  standard price, not introductory. No dataset value changed, only the
  stale "hike coming" note in `docs/models/claude-sonnet-5.md`.
- **DeepSeek V4 Flash and V4 Pro**'s dataset prices ($0.14/$0.28 and
  $0.435/$0.87) were stale — DeepSeek has since split every rate into
  peak and off-peak tiers, and the old numbers matched neither. Updated
  to the peak rate ($0.44/$1.32 and $1.32/$3.96), the conservative
  choice between the two; off-peak is documented in
  `docs/models/deepseek-v4-flash.md` / `deepseek-v4-pro.md`.
- **Claude Haiku 4.5**'s retirement status re-checked: still `Active`,
  no retirement sooner than 2026-10-15. No dataset change — recorded in
  `docs/models/claude-haiku-4-5.md` only, `SCHEMA.md` has no lifecycle
  field.
- Also re-verified: `dataset/subscriptions/google/google-ai-ultra.yaml`
  (no change — plan terms and quota multipliers still match).

A third-party AI-generated audit (Grok) proposed most of these same
corrections with cited URLs. Per this project's standing rule against
using third-party AI audits as a data source (`IMPLEMENTATION_NOTES.md`,
Iteration #14), none of its output was copied — every field above was
independently re-confirmed by reading the cited page directly before
any dataset edit.

---

## 2026-08-17 — Introductory-price expiration shown on the Pricing card

**If a model's current price is temporary, the recommendation page
now says so — instead of that fact living only in internal docs.**

- `gemini-3.6-flash` and `gemini-3.7-flash` both currently price at
  $0.75/$3.75 per million tokens (input/output), an introductory rate
  that reverts to $1.50/$7.50 on 2027-01-01, per Google's own pricing
  table (see `IMPLEMENTATION_NOTES.md`, Iteration #13). That fact
  existed only as prose in `docs/models/*.md` until now — the web
  interface never surfaced it.
- Added two new optional dataset fields, `cost.effective_until` and
  `cost.reverts_to.{input,output}_per_million` (documented in
  `SCHEMA.md`), required together and validated by the loader.
  **Display-only**: the Decision Engine's ranking and cost-tier logic
  keep using the current price exactly as before — a future price
  change is never something the engine reacts to today.
- The recommendation's Pricing card now shows, only for models that
  have it: "Introductory price, in effect until 2026-12-31 — reverts
  to $1.50 input / $7.50 output per 1M tokens afterward."
- Nothing automates the eventual correction — on 2027-01-01, both
  YAML files still need a manual edit to move the reverted price into
  `input_per_million`/`output_per_million` and clear the two new
  fields. This change makes the fact visible, not self-updating.

---

## 2026-08-17 — Use case detection (keyword-based, not AI)

**The free-text "use case" field now actually does something — without
ever calling an AI model to read it.**

- Previously, typing a use case (e.g. "customer support chatbot") did
  nothing beyond being echoed back in the explanation text — it never
  affected which priorities got weighed. Closing that gap with an LLM
  was considered and rejected: it would make the recommendation
  non-deterministic (same input could produce different results) and
  add real, unbounded API cost per request. Silent keyword matching
  that fed straight into the ranking was rejected too — that would be
  guessing at intent and presenting it as understood fact, the same
  fabricated-confidence problem this project has declined everywhere
  else.
- Instead: a plain-rules keyword matcher (15 categories, expanded from
  the 8 existing use-case shortcuts) scans the free text as you type
  and, when there's a single clear match, suggests the priorities that
  category usually needs — shown openly ("Detected: Customer support →
  prioritize instruction following and cost") with a button to accept
  it, never applied automatically. If two categories tie, it says so
  instead of guessing which one you meant. `decision/` is untouched —
  this lives entirely in the web interface, same tier as the existing
  preset pills.
- **Crypto / trading bot** added as its own 15th category (`Cost` +
  `Reasoning`) after live testing turned up a real gap: "trading
  community with a bot" correctly produced no suggestion (by design —
  the bare word "bot" was deliberately excluded as too generic), but
  the underlying use case genuinely wasn't covered. Kept separate from
  "Telegram / WhatsApp bot" rather than folding in its keywords, since
  the two categories weigh different priorities and merging them would
  have meant guessing which one actually applies.
- **Dictionary widened** (~50 phrases across all 15 categories) after
  the user asked for the detection to get "smarter" — scoped down to
  hand-curated plurals and verb-form variants (`chatbot`/`chatbots`,
  `refactor`/`refactoring`) rather than automatic stemming, and stayed
  English-only. Same reasoning as the LLM rejection above: a stemming
  rule is less auditable at a glance than an explicit phrase list, and
  this project favors the latter every time.
- See `IMPLEMENTATION_NOTES.md`, Iteration #15 for the full rejected-
  alternatives reasoning and why this is deliberately scoped as a
  first step, not the whole feature `FEATURES.md` describes.

---

## 2026-08-13 — Gemini 3.7 Flash admitted + Gemini 3.6 Flash pricing correction

**Added the newest Google Gemini model to the dataset, and fixed a real
pricing bug found on an already-shipped one while researching it.**

- **`gemini-3.6-flash.yaml` had a stale price.** Its `cost.*` was
  $1.50/$7.50 — correct when it was loaded (2026-08-07), but Google
  quietly moved it to an introductory rate ($0.75/$3.75, reverting to
  $1.50/$7.50 on 2027-01-01) at some point before 2026-08-13. Caught
  incidentally while researching Gemini 3.7 Flash's own model card,
  which discloses 3.6 Flash's current price in its comparison
  benchmark table. Corrected; the expiration date and future value are
  documented in prose in `docs/models/gemini-3.6-flash.md` (no
  `SCHEMA.md` field exists for a time-limited price — see
  `IMPLEMENTATION_NOTES.md`, Iteration #13).
- **Gemini 3.7 Flash added** (26→27 models) — Google's newest Flash
  model, published the same day as this entry (2026-08-13), based on
  Gemini 3.6 Flash with algorithmic reasoning improvements. Same
  introductory-pricing pattern as 3.6 Flash. All `[Objective]` fields
  sourced directly against the model's official model card and the
  Gemini API's function-calling/structured-output reference docs
  (neither of which state capability flags directly on the card
  itself). `[Editorial]` fields (`quality.*`, `ecosystem.maturity`)
  set by the project, not inherited from any benchmark score or
  third-party audit — see `docs/models/gemini-3.7-flash.md` for the
  full reasoning per field. `ecosystem.maturity: experimental`,
  specifically, because the model doesn't appear yet in Google's
  public Gemini API models catalog as a labeled stable/preview entry —
  a new editorial principle (maturity requires public documentation
  evidence, not just technical availability) applied here for the
  first time.
- Added its `direct_api` access route (Google AI Studio / Gemini API),
  same pattern as the rest of the Gemini family — 60→61 routes,
  27/27 models with at least one confirmed route. `evidence.source_url`
  points to the model's own model card (model-specific confirmation of
  Gemini API distribution), not the generic Gemini API billing page —
  the billing page covers eligibility/economics mechanics only, noted
  in the route's `evidence.caveat` instead.
- Reviewed and explicitly rejected third-party AI-generated "audits" of
  official model cards as a data source, including a concrete
  counter-example: one such audit claimed a ~2M context window for
  Gemini 3.1 Pro, contradicted by that model's own official model card
  (re-fetched directly, 2026-08-13: "up to 1M"), matching this
  project's already-sourced entry — see `IMPLEMENTATION_NOTES.md`,
  Iteration #14.
- Test fixtures depending on dataset size/composition updated to match
  (`test_loader.py`, `test_explainer.py`, `test_access_loader.py`) —
  142/142 tests passing.

---

## 2026-08-13 — v0.1.0 (feature/access-catalog-expansion)

**Grew the Access Advisor catalog from 3/26 to 26/26 model coverage,
52 route files, and then found and corrected a real gap in it before
merge — 60 routes total.**

- **Closed a research + implementation-contract pass from the
  previous session** (`research/access-catalog-coverage-2026-08-12`,
  not merged, research-only per this project's convention) into
  actual dataset files, in two deliberate stages with a full test run
  and browser QA between them:
  - **23 base-pattern routes** — one `direct_api` route per model the
    v1 catalog didn't cover yet, extending the exact template v1 had
    already proven three times (Anthropic/Google/OpenAI) to the two
    providers it hadn't reached (DeepSeek, Mistral). This alone closed
    **26/26 models with at least one documented route** — a
    shippable checkpoint on its own, confirmed with the user before
    continuing.
  - **29 secondary-pattern routes** — Amazon Bedrock, Google Cloud
    Vertex AI, and Microsoft Azure AI Foundry for 9 Claude models,
    a Google AI Studio subscription route for `gemini-3.1-pro-preview`,
    and Mistral Large 3 self-hosted (open-weights, Apache 2.0, sourced
    to its real Hugging Face repository, including actual GPU
    requirements for its 675B-parameter mixture-of-experts
    architecture — the first real use of the `self_hosted` surface
    and `gpu_infrastructure` requirement kind, both already in the
    schema since Access Advisor v1 but unused until now).
  - Two new provider guide docs (DeepSeek, Mistral) and three new
    Anthropic cloud-platform sections, all sourced against live
    official documentation (AWS, Google Cloud, Microsoft Learn,
    Hugging Face) rather than this project's own `docs/models/*.md`
    prose, which only named the platforms in passing.
- **Found and corrected a real gap the closed contract's own research
  had gotten wrong, before merge — not a design change, new
  evidence.** The contract had excluded Claude Fable 5 from the
  Bedrock/Vertex/Foundry patterns as "not documented." Checking AWS's
  and Microsoft's own docs while sourcing the other 9 Claude models
  turned up Fable 5 listed on both; Anthropic's own Transparency Hub
  (`anthropic.com/transparency`) independently confirmed it across
  every surface — Claude.ai, Claude Code, the Anthropic API, Bedrock,
  Vertex AI, and Azure Foundry. Flagged to the user rather than
  silently expanded; once confirmed, added the 4 missing Fable 5
  routes plus a new `consumer_subscription` route (Claude Pro/Max,
  sourced to `claude.com/pricing`'s own comparison table — not the
  news-aggregator sourcing an earlier session's `docs/models/`
  prose had relied on, which doesn't meet this project's bar for a
  route's evidence). **Claude Code itself isn't modeled as a separate
  route** — Anthropic's own docs describe it as a client that
  authenticates via either an API key or a Claude subscription, not a
  third billing path. **MCP/Antigravity access to Claude models was
  deliberately left out** for the same reason the contract already
  excludes unconfirmed surfaces: "can be done in practice" isn't the
  bar this catalog holds itself to — "an officially documented,
  verifiable access route" is.
- Fable 5 is now the catalog's most complex access case: 5 real
  routes across 3 distinct surfaces (`direct_api`, `cloud_hosted` ×3,
  `consumer_subscription`), each with independent eligibility and
  economics — the strongest demonstration yet that Access Advisor
  answers "how do I actually reach this model, given my situation,"
  not just "does a route exist."
- New coverage-shape test (`test_access_catalog_coverage.py`) asserts
  every dataset model has at least one `confirmed` route, so future
  sessions get a loud failure instead of silently losing coverage.
- Verified two ways, not just `pytest`: directly through
  `recommend_access()` for spot-checked models across every provider
  (including the full 5-route Fable 5 breakdown), and in the real web
  UI (server restarted mid-session to pick up the new dataset) —
  Claude Fable 5, DeepSeek V4 Flash/Pro, and Gemini 3.1 Pro Preview,
  all previously "no documented access route yet," now show real
  access options end to end. The subscriptions checklist in the web
  form updated on its own (it's data-driven from the catalog) to
  include the two new Claude plans.

Tests: 141/141 (30 from Access Advisor v1 + 8 new this session).
Routes: 4 → 60. Subscription plans: 2 → 4.

## 2026-08-11 — v0.1.0 (feature/access-advisor-v1)

**Shipped Access Advisor v1 — after a recommendation, a separate "How
can you access this model?" section shows the real, documented ways to
reach it, without ranking them against each other.**

- **New subsystem, `decision/access/`, that never touches the
  recommendation.** `evaluate()`/`explain()` are unchanged; Access
  Advisor runs after them, in `interfaces/web/app.py`, and only reads
  `AIModel` — it can't import `decision/evaluator/` even by mistake,
  by design (internal 2026-08-11 Access Advisor research, not published).
- **Three access states, not a pass/fail gate:** a route is
  `currently_eligible` (usable now), `requires_onboarding` (needs an
  API key, a cloud account, a subscription, etc. — never hidden for
  that), or excluded entirely only when it's an enterprise-only route.
  Declaring "no AWS account" never removes Bedrock from the list — it
  just says what's needed and links to how to get it.
- **No ranking between equally-valid routes.** If a model has three
  ways to reach it (its own API, AWS Bedrock, Google Cloud), Access
  Advisor shows all of them grouped by state, never picks a "best
  cloud" — that would be inventing a preference the evidence doesn't
  support. The one exception: if exactly one *confirmed* direct API
  route exists, it's named in a short "Recommended access" summary;
  otherwise it's a neutral count with the full list one click away.
- **New dataset catalogs**, separate from `dataset/models/`:
  `dataset/access_routes/{provider}/{route_id}.yaml` and
  `dataset/subscriptions/{provider}/{plan_id}.yaml`, each entry sourced
  the same way as a model (URL, date, status) — started with 4 routes
  (Anthropic, Google ×2, OpenAI) and 2 Google subscription plans as a
  working sample, not a full catalog yet.
- **New `docs/access-guides/`** — short, curated pointers to official
  provider docs for each access method, deliberately not step-by-step
  tutorials (`VISION.md`: "does not replace official provider
  documentation").
- Access-related questions (how you'd use the model, whether you have
  billing/cloud accounts/subscriptions already) are optional fields
  added to the form — skipping all of them still gets a full
  recommendation, just without the access detail.

Full design history — including a route-ranking mechanism that was
built, discussed, and deliberately reverted before implementation —
was written up in `ACCESS_ADVISOR_AUDIT_2026-08-11.md`, an internal
research document that lives on its own research branch, not in this
tree (same policy as this project's other research docs) — the
code's own docstrings still cite it by Part number for context.

**Post-review fixes, same session, before merge to `main`:** a second
code-review pass found and fixed 4 real bugs missed by the first —
access-route rows linked to raw evidence instead of the curated
`docs/access-guides/` entry, a route's "not for production use" status
was loaded but never shown, and two dataset fields (`cloud_account`,
`documented_exclusions`) weren't validated against their expected
shape, so bad data could corrupt silently or crash the app at boot
instead of failing with a clear error. Manual QA also caught 6
dataset fields (4 route caveats, 2 subscription exclusions) that had
shipped in Spanish while the rest of the app is English-only — fixed,
with a new test guarding against it recurring. Full test suite:
139/139. **Known, deliberate gap, not a blocker:** only 3 of the 26
models in the dataset have a documented access route today (Claude
Opus 5, GPT-5, Gemini 2.5 Pro) — every other recommended model
correctly shows "no documented access route yet" rather than a wrong
answer. Widening that catalog is real, separate follow-up work, not
part of this release.

---

## 2026-08-11 — v0.1.0

**Shipped the Budget redesign, corrected 5 dataset calibration errors
found by a real-evidence audit, and replaced "single winner" framing
with an honest tie indicator when the recommendation is a close call.**

- **Budget is now a fixed price band, not a moving target.** Cost tier
  (Low/Medium/High/Very High) used to be computed as relative terciles
  of whatever was currently in the dataset — a model could silently
  drift between tiers just because other models were added, and "High"
  budget didn't actually cap anything (the priciest model in the
  catalog always qualified). Tiers are now fixed $/million-token bands
  anchored to real price data, with a new top band (`Very High`) so
  "High" means something again. Confirmed live: `budget=high` +
  reasoning priority used to recommend the single most expensive model
  in the dataset; it no longer does.
- **Cost's influence on the ranking now scales with how loose the
  budget is** — full weight at Low, down to 10% at Very High — but
  only when Cost isn't the developer's own #1 priority, and never at
  all under the new **Custom Budget** mode (a real dollar figure, kept
  deliberately separate from the fixed tiers: it narrows the
  affordability estimate shown after the fact, never the ranking
  itself, since doing that honestly would require assuming a token
  volume nobody provided).
- **Lower-cost Alternative stopped suggesting worse models just because
  they were cheap.** It now only proposes a cheaper option if it stays
  within one quality tier of the recommendation on the priority that
  actually matters, and says so explicitly with a side-by-side
  comparison table instead of a single "you'd save X%" line.
- **New: when two or more models are practically tied, the page says
  so.** A four-level quality scale produces real ties more often than
  not, and until now the UI still had to pick a single "winner" to
  display — via a plain, meaningless tie-break (alphabetical model id).
  Any model within 2% of the top score **and** within one quality tier
  on every dimension is now shown as an "Also strong option" alongside
  the recommendation, not silently folded into a false single-answer
  framing. The 2% threshold wasn't picked by feel — it came out of an
  audit across the full grid of every priority combination and budget
  tier this project supports, checking exactly how often a looser or
  tighter cutoff would start calling genuinely different models
  "equivalent."
- **Dataset calibration audit, evidence-based, per model, not by
  feel.** A user-reported pattern ("one cheap model keeps winning")
  turned into a full audit: every model whose quality rating had no
  real citation behind it (8 of 26) got re-sourced against fresh
  official documentation. Five ratings changed with real evidence
  behind each one — two OpenAI/DeepSeek reasoning ratings moved up,
  one Gemini instruction-following rating moved down, one DeepSeek
  capability flag corrected, and one Mistral price fixed (a stale
  $2.00/$6.00 that should have been $0.50/$1.50 — an out-of-date
  number, not an opinion). The original "cheap model dominates" pattern
  turned out not to be a scoring bug at all — controlled testing (same
  context, only the budget tier changed) showed the ranking already
  shifts in a sensible, budget-aware way; what looked like bias was
  mostly the tie-break problem above wearing a different hat.
- **A real frontend bug, found by hand-testing, fixed:** choosing
  "I know my $ budget" and submitting the form silently did nothing.
  The hidden tier dropdown was still marked required, and the browser
  blocked the submission without being able to show an error on a
  field the visitor couldn't see. Fixed with a small script that keeps
  the two budget modes' required fields in sync.

Tests: 74 → 103.

## 2026-08-10 (later same day) — v0.1.0

**Added 6 candidate models — 20 to 26 — and formalized a new rule for
how editorial quality ratings get calibrated.**

- **Six models admitted**, each fully sourced against official
  provider documentation with its own `docs/models/*.md` audit trail:
  Gemini 2.5 Flash-Lite, Gemini 3.1 Flash-Lite, Gemini 3.5 Flash,
  GPT-5.6 Sol (OpenAI's new flagship, replacing GPT-5), Claude Sonnet
  4.5, and Claude Opus 4.5. All six came out of a dedicated research
  branch (`research/model-candidates`, internal and not published)
  done in a prior session —
  this pass was the field-by-field sourcing verification and the
  actual admission, not new candidate hunting.
- **New rule in `SCHEMA.md`/`CONTRIBUTING.md`: editorial calibration
  must be evidence-based, not family-based.** A model no longer
  inherits a lower or higher quality rating just because it's an
  older generation or a cheaper tier than a sibling already in the
  dataset — every rating needs a specific, sourced signal (a
  knowledge-cutoff gap, a stated or missing capability, explicit
  provider positioning language). Caught and corrected a real
  overreach mid-session: an early pass had degraded Claude Sonnet
  4.5's `creative_writing` rating alongside its reasoning/coding, with
  no evidence that specifically touched writing quality — fixed before
  it shipped.
- **`gpt-5-6-sol`'s id** deliberately doesn't match OpenAI's own model
  string (`gpt-5.6-sol`, with a dot) — converted to the project's
  existing hyphen convention, documented in that model's own `.md`.
- Also fixed the same day: `docs/models/deepseek-v4-pro.md`'s
  `reasoning`/`coding` justification, which had been written using
  the exact family-based reasoning the new rule now rules out. The
  rating itself (`very_high`/`very_high`) didn't change — re-checking
  against DeepSeek's own release announcement found real supporting
  evidence ("World-Class Reasoning: beats all current open models...
  rivaling top closed-source models") that the original write-up had
  explicitly declined to use. `gemini-2.5-pro.md`'s justification is
  now flagged as the weakest-sourced `very_high` rating left in the
  catalog — noted for a future pass, not touched yet.
- No changes to `decision/evaluator/`, `decision/explainer/`, or
  `interfaces/web/` — dataset and documentation only.

Tests: 68 → 74 (26-model dataset, plus new parametrized language
coverage for the 6 additions).

**Also this session, investigated but not yet implemented:** a
product audit found that `budget` (Low/Medium/High) and a
user-entered monthly dollar amount are structurally disconnected —
the dollar figure only feeds the affordability calculator, never the
recommendation itself, and budget tiers are relative to whatever's
currently in the dataset rather than fixed price bands. A redesign
(fixed price-per-token tiers, a mutually-exclusive custom-budget mode
that never assumes a token-usage volume, and a more honest "lower-cost
alternative" comparison) is designed but not built. Full detail in
`HANDOFF.md`.

## 2026-08-10 — v0.1.0

**Added DeepSeek V4 Pro to the dataset — 19 to 20 models — and closed
out two dataset-candidate investigations that had gone undocumented.**

- **DeepSeek V4 Pro.** Researched against DeepSeek's own official docs
  and its Hugging Face model repository only: 1M-token context, 384K
  max output, $0.435 / $0.87 per million tokens (input / output),
  MIT-licensed open weights. The one genuinely interesting question was
  whether it supports image input — several non-official sites claimed
  it does, but DeepSeek's own API reference, its full documentation
  index, its Hugging Face model card, and its Responses API guide (the
  most direct of the four: *"Image and file inputs are not supported...
  replaced with a placeholder text"*) all agree it doesn't. Resolved as
  a confirmed `false`, not left pending — the sourcing pattern itself
  (official docs vs. a cluster of consistent third-party claims) is
  logged as its own entry in `IMPLEMENTATION_NOTES.md`, since it's
  useful precedent for future research, independent of this model.
  Quality and ecosystem ratings were calibrated against DeepSeek V4
  Flash's existing entry (flagship vs. flash tier) — not against
  DeepSeek's own marketing language about the model, which is noted in
  the sourcing but explicitly excluded as a basis for any editorial
  rating, per this project's own rule.
- **Meta Llama and NVIDIA NIM, formally logged as closed
  non-candidates.** Both had been investigated in a prior session but
  never written down anywhere — re-verified against official sources
  before logging anything, rather than trusting the earlier informal
  conclusion. Meta retired its first-party Llama API on 2026-07-06; its
  successor product serves only its own proprietary "Muse Spark"
  models today, confirmed directly against that product's live model
  listing. NVIDIA NIM re-confirmed as a GPU-licensed hosting platform
  with no per-token pricing anywhere in its own documentation
  ($4,500/GPU/year or ~$1/GPU/hour, quoted directly from NVIDIA's own
  FAQ) — same verdict as an earlier pass, now backed by direct quotes
  instead of forum reports.
- No changes to `decision/evaluator/`, `decision/explainer/`, or
  `interfaces/web/` — this was a dataset and documentation pass only.

Tests: 67 → 68.

## 2026-08-09 — v0.1.0 (2)

**Added `has_free_access` — a strict, single-boolean answer to "can I use
this model without paying," across the whole dataset.**

- Two research passes this week (documented in `IMPLEMENTATION_NOTES.md`,
  Iteration #8) looked at whether free-access rate limits (NVIDIA NIM,
  Google's free tier, Groq, and others) could become part of the dataset.
  They can't, honestly — only one of six providers checked publishes a
  stable, official rate-limit table; the rest are dynamic per-account
  dashboards or simply undocumented. Putting raw numbers in the dataset
  would have meant presenting a Groq figure as equally solid as NVIDIA
  Developer Forum folklore.
- What survived instead: a new `access.has_free_access` field, strictly
  defined as "does an official, documented free-access path exist for this
  specific model today" — never inferred, never based on a one-time trial
  credit. Every one of the 19 dataset entries was individually checked
  against its provider's own pricing docs. Three qualify: Gemini 2.5 Flash,
  Gemini 3.6 Flash, and Gemini 3.5 Flash-Lite, all confirmed "Free of
  charge" on Google's own pricing page. Every other model — including
  Gemini's own Pro-tier releases, all Claude, OpenAI, DeepSeek, and Mistral
  entries — is `false`, most because no free path exists at all, one
  (Mistral Large 3) because a free API tier exists at the platform level but
  couldn't be confirmed for that specific model.
- Surfaced in the web interface as a secondary signal, not a headline claim:
  a small "Free access also documented" note appears next to pricing, but
  only when the developer's stated budget is Low — it never claims a model
  "is free" outright, since real-world limits still apply.
- No changes to `decision/evaluator/` or `decision/explainer/` — the field
  doesn't affect qualification or ranking, only what's displayed.

Tests: 62 → 67.

## 2026-08-09 — v0.1.0

**Accessibility, responsive, and visual design pass — no changes to the
recommendation engine or the dataset.**

- Fixed two real color-contrast failures against WCAG AA (a green text
  color and a form-input border that were both too light to reliably
  read), added a visible focus ring to every interactive element, made
  the three help tooltips reachable by keyboard, and gave two page
  sections real `<h2>` headings instead of styled paragraphs so they
  show up when navigating by heading (a common screen-reader pattern).
- Audited both pages at 340px and 768px, including the densest state
  of the result page (a budget entered, showing capacity bars and a
  savings callout) — no horizontal overflow anywhere.
- Added a favicon, a meta description, and Open Graph tags — none of
  that existed before.
- Added a "Supported models" section to the landing page, listing
  every provider currently in the dataset. The list is generated from
  the dataset itself, not hand-typed, so it grows on its own as new
  providers are added.
- A hierarchy and consistency pass on the result page: section titles
  now read as more important than small inline labels (they didn't
  before), removed a hover animation from cards that aren't actually
  clickable, and consolidated a handful of colors that had drifted
  outside the shared palette back into it.
- Rebuilt the form itself. It no longer sits inside a white card
  floating on the page — it's laid out as three numbered stages (Use
  case, Priorities, Budget) directly on the page, with a two-column
  layout on desktop instead of the previous single stacked column.
  Priorities now comes before Budget: it's the input that actually
  drives which model wins (the first priority you pick matters most),
  while Budget only filters candidates out — and moving it earlier
  puts it next to the quick-pick buttons that pre-fill it. Collapses
  back to a single column below 640px, audited the same way as above.
- None of this touched `decision/`, the dataset, or how a
  recommendation is computed — verified before and after every step
  with the full test suite and, for anything scoped as "visual only,"
  a `git status` check confirming zero Python files changed.

Tests: 62/62, unchanged in count (this pass added no new engine
behavior to test).

## 2026-08-07 — v0.1.0

**Grew the model dataset from 5 to 19 models, and made every entry
independently auditable.**

- Added `docs/models/` — one file per model in the dataset, citing
  exactly where each value came from (official provider documentation
  only, dated) and flagging anything that couldn't be independently
  confirmed as *pending* rather than presenting it as verified. Every
  one of the original 5 models was re-verified against current
  official docs in the process.
- Formalized a rule, visible in `CONTRIBUTING.md`: if a field has no
  clear official source, it doesn't enter the dataset as hard data —
  it's marked pending, and the model waits until it's fully sourced.
  Applied this literally: NVIDIA NIM, Mistral Medium 3.5, and Grok 4.5
  were all researched and none were added, because none had a
  complete official source for every required field.
- Added 14 new models across every major provider's current lineup —
  flagship, mid, and low-cost tiers — plus a deliberate test case:
  GPT-4o was added specifically to check whether the recommendation
  engine can surface "this is an older generation, consider
  migrating" using only real cost and quality data, with no special
  "legacy" flag anywhere in the system. It can — see the reasoning in
  `docs/models/gpt-4o.md`.
- Investigated models exposed through Google's Antigravity product
  (including what was initially reported as "Gemini 3.1 Pro") and
  found real problems with treating it as a source: no official
  per-token pricing, and community reports that its model labels
  don't reliably match what's actually running. None of those were
  added on that basis. Separately, Gemini 3.1 Pro *does* exist as a
  real, independently-priced model through Google's standard API —
  found on a second, more thorough pass, and added once it cleared the
  same bar as everything else.
- Every model entry now documents where it can actually be called
  from (which official API, at what price) — kept deliberately
  separate from the harder question of "does my existing subscription
  already cover this," which stays a future direction, not answered
  here.
- Cleaned up two small pieces of repeated code in the web interface
  (a repeated list-rendering pattern, one CSS rule that had ended up
  split across two files) — cosmetic only, verified in a real browser,
  nothing about how the app behaves changed.

All of the above shipped in 8 commits to `main`, all tests passing
(59/59) at every step.

**Added full ranking transparency to every recommendation.** Until
now, a qualifying model that ranked below the top 3 alternatives
simply disappeared from the result — not shown as a pick, not shown as
excluded, just gone. Every recommendation now shows:

- The recommended model's and every alternative's real rank ("#1 of
  19 qualifying models", "#2 of 19", etc.) — a true, computed position,
  not an invented confidence score. A raw match score (e.g. "80/100")
  was considered and deliberately not built: the underlying number is
  only meaningful relative to whichever models happen to qualify for
  one specific query, so the same model could score very differently
  for two different users with no change in the model itself —
  presenting that as an absolute percentage would have implied a
  precision the number doesn't have.
- Every model that qualified but didn't rank in the top 3, with a real
  rank and the actual dimensions it lost on — reordered so whatever
  the user actually prioritized shows first, not buried in a fixed
  list order. Only the top 2 reasons show by default, with the rest
  available on demand — a model can lose on five dimensions at once,
  and listing all five up front was noise, not information.
- Every model that never qualified at all, now grouped by why —
  "12 models — cost tier exceeds a 'low' budget" once, instead of the
  same sentence repeated 12 times. Distinct on purpose from the models
  above: these never entered the ranking, so they don't get a rank.

Tests: 59 → 62.
