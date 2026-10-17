"""The decision graph's data: one dot per model, with the ring it sits on.

Built once from the explainer's Recommendation and used twice: the result
page renders it into a hidden list that graph-draw.js reads, and the what-if
endpoint returns the same items as JSON. Sharing one builder is what keeps
the first paint and every later redraw from disagreeing.

Nothing here ranks or scores anything: the ring is the engine's own
standing (top alternative, practically tied, also qualifies, excluded) and
the marks are dated facts the catalog already carries
(interfaces/web/catalog_notices.py).
"""

from collections.abc import Callable

from decision.domain import AIModel, Recommendation
from interfaces.web.catalog_notices import Badges, short_date


def _marks(badges: Badges) -> dict:
    retiring = ""
    if badges.retiring:
        retiring = short_date(badges.retiring.shutdown_date) if badges.retiring.shutdown_date else "routed"
    return {
        "is_new": bool(badges.new),
        "promo": short_date(badges.promo.ends) if badges.promo else "",
        "retiring": retiring,
        "deprecated": bool(badges.retiring and badges.retiring.deprecated),
    }


def _item(ring: str, model: AIModel, badges_of: Callable[[AIModel], Badges], *, rank=None, tied=False, reasons=()) -> dict:
    item = {"ring": ring, "id": model.id, "name": model.name, "rank": rank, "tied": tied}
    if ring != "center":
        item["input"] = f"{model.cost.input_per_million:.2f}"
        item["output"] = f"{model.cost.output_per_million:.2f}"
        item["reasons"] = list(reasons)
    item.update(_marks(badges_of(model)))
    return item


def graph_items(recommendation: Recommendation, badges_of: Callable[[AIModel], Badges]) -> list[dict]:
    """Every catalog model as a dot: the winner first, then ring by ring."""
    tied_ids = {option.model.id for option in recommendation.also_strong_options}
    items = [_item("center", recommendation.recommended, badges_of, rank=1)]
    items += [
        _item("alt", alt.model, badges_of, rank=alt.rank, tied=alt.model.id in tied_ids, reasons=alt.reasons)
        for alt in recommendation.alternatives
    ]
    items += [
        _item("tied" if o.model.id in tied_ids else "out", o.model, badges_of, rank=o.rank, reasons=o.reasons)
        for o in recommendation.outranked
    ]
    items += [_item("ex", e.model, badges_of, reasons=e.reasons) for e in recommendation.excluded]
    return items


def ring_counts(items: list[dict]) -> dict[str, int]:
    """How many dots sit on each ring (the legend's numbers)."""
    counts = {"alt": 0, "tied": 0, "out": 0, "ex": 0}
    for item in items:
        if item["ring"] in counts:
            counts[item["ring"]] += 1
    return counts
