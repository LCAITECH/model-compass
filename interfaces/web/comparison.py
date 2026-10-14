"""Static model comparison: the dataset's own fields, side by side.

View logic only -- no scoring, no verdict. Every cell is a stored field
or a direct reading of one (a language count, a route count). The only
derived thing is the "best in row" mark, which is just the highest or
lowest stored value among the selected models, and only when they
actually differ. Nothing here feeds decision/, and decision/ would work
identically without it (ARCHITECTURE.md).
"""

from decision.domain import AIModel, AccessRoute, language_name
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
    return {"text": text, "best": False, "note": None, "ordinal": None, "max_ordinal": None, "flag": None, **extra}


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


def build_comparison(selected: list[AIModel], routes: list[AccessRoute]) -> list[dict]:
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

    return [
        {
            "title": "Overview",
            "rows": [
                {"label": "Provider", "cells": [_cell(m.provider) for m in selected]},
                {"label": "License", "cells": [_cell(humanize(m.license.value.replace("-", "_"))) for m in selected]},
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
