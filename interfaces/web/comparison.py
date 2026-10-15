"""Model comparison: the dataset's own fields, side by side.

View logic only. Every cell is a stored field or a direct reading of one
(a language count, a route count). The "best in row" mark is just the
highest or lowest stored value among the selected models, and only when
they actually differ. Nothing here feeds decision/, and decision/ would
work identically without it (ARCHITECTURE.md).

Optionally, given a Context, the engine's own verdict for each selected
model is shown first (does it qualify, its place among the qualifying
models, the engine's reasons). That is decision/'s output passed
through unchanged: no score is shown and nothing is computed here.
"""

from decision.domain import AIModel, AccessRoute, Context, language_name
from decision.evaluator import evaluate
from decision.explainer import NoQualifyingModelsError, explain
from interfaces.web.access_labels import humanize
from interfaces.web.model_profile import capability_flags, quality_profile

MAX_COMPARED = 4
MIN_COMPARED = 2


def group_models(models: list[AIModel]) -> list[tuple[str, list[AIModel]]]:
    """Models grouped by provider, both sorted, for the picker's <optgroup>s."""
    by_provider: dict[str, list[AIModel]] = {}
    for model in models:
        by_provider.setdefault(model.provider, []).append(model)
    return [(provider, sorted(group, key=lambda m: m.name)) for provider, group in sorted(by_provider.items())]


def parse_selection(raw_ids: list[str], models: list[AIModel]) -> list[AIModel]:
    """Valid, de-duplicated models in the order given, capped at MAX_COMPARED.

    Unknown ids and blanks are dropped silently: the page is a shareable
    link, so a stale id should degrade to "fewer models", not an error.
    """
    by_id = {model.id: model for model in models}
    selected: list[AIModel] = []
    for raw in raw_ids:
        model = by_id.get(raw.strip())
        if model and model not in selected:
            selected.append(model)
    return selected[:MAX_COMPARED]


def _best_flags(values: list[float | int | None], higher_is_better: bool) -> list[bool]:
    present = [v for v in values if v is not None]
    if len(set(present)) < 2:
        return [False] * len(values)
    target = max(present) if higher_is_better else min(present)
    return [v is not None and v == target for v in values]


def _cell(text: str, **extra) -> dict:
    return {
        "text": text,
        "best": False,
        "note": None,
        "reasons": (),
        "tone": None,
        "ordinal": None,
        "max_ordinal": None,
        "flag": None,
        **extra,
    }


def _with_best(cells: list[dict], values, higher_is_better: bool) -> list[dict]:
    for cell, best in zip(cells, _best_flags(values, higher_is_better)):
        cell["best"] = best
    return cells


def _price(value: float) -> str:
    return f"${value:,.2f}"


def _cost_cell(model: AIModel, field: str) -> dict:
    value = getattr(model.cost, field)
    cell = _cell(_price(value))
    if model.cost.effective_until:
        reverted = getattr(model.cost.reverts_to, field)
        cell["note"] = f"Introductory, through {model.cost.effective_until}; then {_price(reverted)}"
    return cell


def _lifecycle_cell(model: AIModel) -> dict:
    lifecycle = model.lifecycle
    details = []
    if lifecycle.shutdown_date:
        details.append(f"Shuts down {lifecycle.shutdown_date}")
    if lifecycle.replacement:
        details.append(f"replacement: {lifecycle.replacement}")
    note = "; ".join(details) or None
    if lifecycle.deprecated:
        return _cell("Deprecated", tone="bad", note=note)
    return _cell("Active", note=note)


def context_fit(selected: list[AIModel], all_models: list[AIModel], context: Context) -> dict:
    """The engine's verdict for each selected model under `context`.

    Runs the real evaluator and explainer over the whole dataset, so the
    place shown ("#3 of 36") is the same one the main recommendation flow
    would give. `explain` raises when nothing qualifies; then every
    selected model is simply excluded, with the evaluator's own reasons.
    """
    candidates = evaluate(context, all_models)
    by_id = {candidate.model.id: candidate for candidate in candidates}
    try:
        recommendation = explain(context, candidates)
    except NoQualifyingModelsError:
        recommendation = None

    placed: dict[str, tuple[int, tuple[str, ...]]] = {}
    tied: set[str] = set()
    total = 0
    winner = None
    if recommendation:
        total = recommendation.total_qualifying
        winner = recommendation.recommended
        placed[winner.id] = (1, recommendation.reasons)
        for alt in (*recommendation.alternatives, *recommendation.also_strong_options):
            placed.setdefault(alt.model.id, (alt.rank, alt.reasons))
        for outranked in recommendation.outranked:
            placed.setdefault(outranked.model.id, (outranked.rank, outranked.reasons))
        tied = {alt.model.id for alt in recommendation.also_strong_options}

    cells = []
    for model in selected:
        candidate = by_id[model.id]
        if not candidate.qualifies:
            cells.append(_cell("Excluded", tone="bad", reasons=candidate.disqualified_reasons))
            continue
        rank, reasons = placed[model.id]
        place = f"#{rank} of {total}"
        if rank == 1:
            cells.append(_cell(f"{place} · Best match", tone="good", reasons=reasons))
        elif model.id in tied:
            cells.append(_cell(f"{place} · Practically tied with #1", tone="good", reasons=reasons))
        else:
            cells.append(_cell(place, tone="neutral", reasons=reasons))
    return {"winner": winner, "total": total, "cells": cells}


def build_comparison(
    selected: list[AIModel], routes: list[AccessRoute], fit: dict | None = None
) -> list[dict]:
    """Sections of rows; every row has one cell per selected model, in order."""
    profiles = [quality_profile(model) for model in selected]
    quality_rows = []
    for index, dim in enumerate(profiles[0]):
        ordinals = [profile[index]["ordinal"] for profile in profiles]
        cells = [
            _cell(profile[index]["level"].capitalize(), ordinal=profile[index]["ordinal"], max_ordinal=profile[index]["max_ordinal"])
            for profile in profiles
        ]
        quality_rows.append({"label": dim["label"], "segments": True, "cells": _with_best(cells, ordinals, True)})

    flags = [dict(capability_flags(model)) for model in selected]
    capability_rows = [
        {"label": label, "cells": [_cell("Yes" if f[label] else "No", flag=f[label]) for f in flags]}
        for label in flags[0]
    ]

    inputs = [m.cost.input_per_million for m in selected]
    outputs = [m.cost.output_per_million for m in selected]
    contexts = [m.operational.context_window for m in selected]
    max_outputs = [m.operational.max_output for m in selected]

    def routes_for(model: AIModel) -> list[str]:
        return [r.access.access_method for r in routes if r.model_id == model.id]

    fit_section = (
        [{"title": "For your context", "rows": [{"label": "Engine result", "cells": fit["cells"]}]}] if fit else []
    )
    return fit_section + [
        {
            "title": "Overview",
            "rows": [
                {"label": "Provider", "cells": [_cell(m.provider) for m in selected]},
                {"label": "License", "cells": [_cell(humanize(m.license.value.replace("-", "_"))) for m in selected]},
                {"label": "Lifecycle", "cells": [_lifecycle_cell(m) for m in selected]},
                {"label": "Maturity", "cells": [_cell(humanize(m.ecosystem.maturity.value)) for m in selected]},
                {"label": "Integration ease", "cells": [_cell(humanize(m.ecosystem.integration_ease.value)) for m in selected]},
            ],
        },
        {"title": "Quality (editorial ratings)", "rows": quality_rows},
        {
            "title": "Price per 1M tokens",
            "rows": [
                {"label": "Input", "cells": _with_best([_cost_cell(m, "input_per_million") for m in selected], inputs, False)},
                {"label": "Output", "cells": _with_best([_cost_cell(m, "output_per_million") for m in selected], outputs, False)},
            ],
        },
        {
            "title": "Limits",
            "rows": [
                {"label": "Context window", "cells": _with_best([_cell(f"{v:,} tokens") for v in contexts], contexts, True)},
                {
                    "label": "Max output",
                    "cells": _with_best(
                        [_cell("Not published" if v is None else f"{v:,} tokens") for v in max_outputs], max_outputs, True
                    ),
                },
            ],
        },
        {"title": "Capabilities", "rows": capability_rows},
        {
            "title": "Languages and access",
            "rows": [
                {
                    "label": "Languages",
                    "cells": [
                        _cell(f"{len(m.languages)}", note=", ".join(language_name(code) for code in m.languages))
                        for m in selected
                    ],
                },
                {
                    "label": "Free access",
                    "cells": [_cell("Yes" if m.access.has_free_access else "No", flag=m.access.has_free_access) for m in selected],
                },
                {
                    "label": "Documented access routes",
                    "cells": [
                        _cell(str(len(routes_for(m))), note="; ".join(routes_for(m)) or "None documented yet")
                        for m in selected
                    ],
                },
            ],
        },
    ]
