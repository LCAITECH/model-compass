# Model Compass

> Developers don't need more information. They need better decisions.

**Status: Pre-MVP — in active development**

The core decision engine (dataset loader, evaluator, explainer) and a
first web interface are implemented and tested. The project is still
pre-1.0 and evolving — see [Getting Started](#getting-started) to run
it locally.

---

## What is Model Compass?

Model Compass is an open-source decision engine that helps developers
choose the most suitable AI model for their specific use case.

Instead of comparing benchmarks, reading scattered provider documentation,
or guessing based on popularity, developers describe their context —
use case, budget, priorities, language, expected volume — and Model
Compass returns an explainable recommendation together with the
trade-offs behind every decision.

## The Problem

Choosing an AI model today means digging through inconsistent provider
docs, benchmarks that don't reflect real use cases, and opinions scattered
across forums and social media.

Most of that effort doesn't lead to a better decision — it just costs time.

Model Compass exists to answer one question directly:

**"What model should I use for this?"**

## Why Model Compass?

Model Compass focuses on decision making rather than information retrieval.

Instead of asking an AI model for an opinion, it evaluates your requirements
against a transparent and curated knowledge base to produce deterministic,
explainable recommendations.

Every recommendation can be understood, reviewed, and reproduced.

## How it works

**Input**

```
Use case    Telegram Community Bot
Budget      Low
Priority    Lowest Cost
Language    Spanish
```

**Output**

```
────────────────────────────────
Recommended model

Gemini 2.5 Flash

Reason
✓ Lowest operational cost
✓ Excellent Spanish support
✓ Great latency
✓ Strong function calling

Trade-offs
• Not the strongest reasoning model
• Better suited for high-volume applications

Alternatives
GPT-5 Mini
Claude Sonnet
────────────────────────────────
```

*This illustrates the interaction — the exact wording and ranking logic
may differ slightly from a live run. Try it yourself locally, see
[Getting Started](#getting-started) below.*

## Getting Started

Requires Python 3.11+.

```bash
git clone https://github.com/LCAITECH/model-compass.git
cd model-compass
pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

Run the web interface locally:

```bash
uvicorn interfaces.web.app:app --reload
```

Then open `http://localhost:8000`.

## Core Principles

- **Explainability** — every recommendation comes with a reason, never
  just a model name.
- **Vendor neutrality** — no provider is favored. Recommendations depend
  on context, not on partnerships.
- **Transparency** — the dataset and the recommendation logic are public.
- **Deterministic recommendations** — results are based on explicit rules
  and curated data, not on opaque AI-generated opinions.
- **Community-driven dataset** — maintained in the open, versioned in Git,
  and improved through reviewed contributions.

## Roadmap

| Phase | Access form | Status |
|-------|-------------|--------|
| MVP   | Web app     | In progress |
| v2    | API         | Planned |
| v3    | Python SDK  | Planned |
| v4    | CLI         | Planned |

See [ROADMAP.md](./ROADMAP.md) for details.

## Contributing

Model Compass is in its early stages, and contributions — code, dataset
entries, ideas, feedback — are welcome.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to get
involved.

## License

MIT — see [LICENSE](./LICENSE) for details.

## Learn More

- [VISION.md](./VISION.md) — project mission and philosophy
- [ROADMAP.md](./ROADMAP.md) — where the project is headed
- [FEATURES.md](./FEATURES.md) — planned and existing features
- [ARCHITECTURE.md](./ARCHITECTURE.md) — technical design
- [SCHEMA.md](./SCHEMA.md) — how the dataset represents knowledge
- [CONTRIBUTING.md](./CONTRIBUTING.md) — how to contribute
