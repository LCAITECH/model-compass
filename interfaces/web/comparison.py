"""Model comparison: the dataset's own fields, side by side.

View logic only. Every cell is a stored field or a direct reading of one
(a language count, a price ratio, a day count, what a typed-in amount
buys at a stored price). The "best in row" mark is just the highest or
lowest stored value among the selected models, and only when they
actually differ. Nothing here feeds decision/, and decision/ would work
identically without it (ARCHITECTURE.md).

Optionally, given a Context, the engine's own verdict for each selected
model is shown first (does it qualify, its place among the qualifying
models, the engine's reasons). That is decision/'s output passed
through unchanged: no score is shown and nothing is computed here.

The section builders live in compare_sections.py, cell helpers in
compare_cells.py, and the drawings' geometry in compare_visuals.py.
"""

from datetime import date
from urllib.parse import urlencode

from decision.domain import AIModel, AccessRoute, Context
from decision.evaluator import evaluate
from decision.explainer import NoQualifyingModelsError, explain
from interfaces.web.compare_cells import cell
from interfaces.web.compare_sections import (
    access_section,
    budget_section,
    capabilities_section,
    lifecycle_section,
    limits_section,
    overview_section,
    price_section,
    quality_section,
)

MAX_COMPARED = 4
MIN_COMPARED = 2

# Query fields a selection change keeps, so removing or swapping a model
# never drops the context or the typed-in amount.
CARRIED_FIELDS = ("language", "budget", "priority_1", "priority_2", "priority_3", "monthly_budget_usd")

_CATEGORY = {
    "center": "Best match",
    "tied": "Practically tied with #1",
    "alt": "Top alternative",
    "out": "Also qualifies",
    "ex": "Excluded",
}


def group_models(models: list[AIModel]) -> list[tuple[str, list[AIModel]]]:
    """Models grouped by provider, both sorted, for the picker."""
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


def compare_href(ids: list[str], form: dict | None = None) -> str:
    """A /compare link for `ids`, carrying the context and amount from `form`."""
    form = form or {}
    params = [("m", model_id) for model_id in ids]
    params += [(field, form[field]) for field in CARRIED_FIELDS if form.get(field)]
    return "/compare?" + urlencode(params)


def selection_links(selected: list[AIModel], form: dict, fit: dict | None) -> dict:
    """Links that change the selection: remove one model, or add the engine's #1."""
    ids = [model.id for model in selected]
    links = {"remove": {i: compare_href([other for other in ids if other != i], form) for i in ids}, "add_winner": None}
    winner = fit["winner"] if fit else None
    if winner and winner.id not in ids and len(ids) < MAX_COMPARED:
        links["add_winner"] = compare_href([*ids, winner.id], form)
    return links


def context_fit(selected: list[AIModel], all_models: list[AIModel], context: Context) -> dict:
    """The engine's verdict for each selected model under `context`.

    Runs the real evaluator and explainer over the whole dataset, so the
    place shown ("#3 of 36") is the same one the main recommendation flow
    would give. `explain` raises when nothing qualifies; then every
    selected model is simply excluded, with the evaluator's own reasons.

    `rings` places every catalog model the way the result page's decision
    graph does (centre, top alternatives, practically tied, also qualify,
    excluded), for the orbit drawing.
    """
    candidates = evaluate(context, all_models)
    by_id = {candidate.model.id: candidate for candidate in candidates}
    try:
        recommendation = explain(context, candidates)
    except NoQualifyingModelsError:
        recommendation = None

    placed: dict[str, tuple[int, tuple[str, ...], str]] = {}
    tied: set[str] = set()
    total = 0
    winner = None
    if recommendation:
        total = recommendation.total_qualifying
        winner = recommendation.recommended
        tied = {alt.model.id for alt in recommendation.also_strong_options}
        placed[winner.id] = (1, recommendation.reasons, "center")
        for alt in recommendation.alternatives:
            placed.setdefault(alt.model.id, (alt.rank, alt.reasons, "alt"))
        for entry in (*recommendation.also_strong_options, *recommendation.outranked):
            placed.setdefault(entry.model.id, (entry.rank, entry.reasons, "tied" if entry.model.id in tied else "out"))

    rings: dict[str, list[AIModel]] = {ring: [] for ring in _CATEGORY}
    for candidate in candidates:
        ring = placed[candidate.model.id][2] if candidate.qualifies else "ex"
        rings[ring].append(candidate.model)

    cells = []
    for model in selected:
        candidate = by_id[model.id]
        if not candidate.qualifies:
            cells.append(
                cell("Excluded", tone="bad", reasons=candidate.disqualified_reasons, rank=None, ring="ex", category=_CATEGORY["ex"])
            )
            continue
        rank, reasons, ring = placed[model.id]
        place = f"#{rank} of {total}"
        category = _CATEGORY["tied"] if model.id in tied and rank != 1 else _CATEGORY[ring]
        extra = {"reasons": reasons, "rank": rank, "ring": ring, "category": category}
        if rank == 1:
            cells.append(cell(f"{place} · Best match", tone="good", **extra))
        elif model.id in tied:
            cells.append(cell(f"{place} · Practically tied with #1", tone="good", **extra))
        else:
            cells.append(cell(place, tone="neutral", **extra))
    return {"winner": winner, "total": total, "cells": cells, "rings": rings}


def _mark_same(sections: list[dict]) -> None:
    """Flags rows whose cells all read the same, for the "only differences" view."""
    for section in sections:
        for row in section["rows"]:
            keys = {
                (c["text"], c["note"], c["ordinal"], tuple((chip["label"], chip["detail"]) for chip in c["chips"]))
                for c in row["cells"]
            }
            row["same"] = len(keys) == 1 and not row.get("pinned")
        section["all_same"] = all(row["same"] for row in section["rows"])


def build_comparison(
    selected: list[AIModel],
    routes: list[AccessRoute],
    fit: dict | None = None,
    *,
    all_models: list[AIModel] | None = None,
    plan_names: dict[str, str] | None = None,
    today: date | None = None,
    budget_usd: float | None = None,
    form: dict | None = None,
) -> list[dict]:
    """Sections of rows; every row has one cell per selected model, in order."""
    ids = [model.id for model in selected]

    def swap_href(old: str, new: str) -> str:
        return compare_href([new if model_id == old else model_id for model_id in ids], form)

    sections = []
    if fit:
        sections.append(
            {"title": "For your context", "rows": [{"label": "Engine result", "cells": fit["cells"], "pinned": True}]}
        )
    sections += [
        overview_section(selected),
        lifecycle_section(selected, all_models or selected, today or date.today(), swap_href),
        quality_section(selected),
        price_section(selected),
    ]
    if budget_usd:
        sections.append(budget_section(selected, budget_usd))
    sections += [
        limits_section(selected),
        capabilities_section(selected),
        access_section(selected, routes, plan_names or {}),
    ]
    _mark_same(sections)
    return sections


def row_counts(sections: list[dict]) -> dict:
    """How many rows there are, and how many differ between the selected models."""
    rows = [row for section in sections for row in section["rows"] if not row.get("pinned")]
    return {"total": len(rows), "differ": sum(1 for row in rows if not row["same"])}
