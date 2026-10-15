"""The comparator's sections, one builder per section.

Each returns {"title", "rows", "note"}; every row has one cell per
selected model, in order. View logic only (see comparison.py): a cell
shows a stored field, a calendar difference against today's date (the
rule catalog_notices.py already follows), or what a typed-in dollar
amount buys at stored prices (the rule affordability.py already follows).
"""

from collections.abc import Callable
from datetime import date, timedelta

from decision.domain import AccessRoute, AIModel, RequirementKind, Surface, language_name
from interfaces.web.access_labels import guide_ref_url, humanize
from interfaces.web.affordability import estimated_input_capacity, estimated_output_capacity
from interfaces.web.catalog_notices import NEW_WINDOW_DAYS, short_date
from interfaces.web.compare_cells import cell, dollars, price, tokens, with_bars, with_best, with_ratios
from interfaces.web.model_profile import capability_flags, quality_profile

_PRICE_FIELDS = (("Input", "input_per_million"), ("Output", "output_per_million"))

_SURFACE_ROWS = (
    (Surface.DIRECT_API, "Direct API"),
    (Surface.CLOUD_HOSTED, "Cloud platforms"),
    (Surface.CONSUMER_SUBSCRIPTION, "Subscription apps"),
    (Surface.PLAYGROUND_OR_STUDIO, "Studio"),
    (Surface.SELF_HOSTED, "Self-hosted"),
    (Surface.ENTERPRISE, "Enterprise"),
)


def _days(n: int) -> str:
    return "1 day" if n == 1 else f"{n} days"


def _day_after(iso: str) -> str:
    return (date.fromisoformat(iso) + timedelta(days=1)).isoformat()


def overview_section(selected: list[AIModel]) -> dict:
    return {
        "title": "Overview",
        "rows": [
            {"label": "Provider", "cells": [cell(m.provider) for m in selected]},
            {"label": "License", "cells": [cell(humanize(m.license.value.replace("-", "_"))) for m in selected]},
            {
                "label": "Languages",
                "cells": [
                    cell(str(len(m.languages)), note=", ".join(language_name(code) for code in m.languages))
                    for m in selected
                ],
            },
            {"label": "Maturity", "cells": [cell(humanize(m.ecosystem.maturity.value)) for m in selected]},
            {"label": "Integration ease", "cells": [cell(humanize(m.ecosystem.integration_ease.value)) for m in selected]},
        ],
    }


def _status_cell(model: AIModel) -> dict:
    if model.lifecycle.deprecated:
        return cell("Deprecated", tone="bad")
    if model.lifecycle.restricted:
        return cell("Existing users only", tone="bad", note="Its provider limits it to developers who already used it")
    if model.lifecycle.shutdown_date:
        return cell("Active", tone="caution", note="Its provider has published a shutdown date")
    return cell("Active")


def _released_cell(model: AIModel, today: date) -> dict:
    released = model.lifecycle.release_date
    if not released:
        return cell("Not published")
    days_ago = (today - date.fromisoformat(released)).days
    if 0 <= days_ago <= NEW_WINDOW_DAYS and not (model.lifecycle.deprecated or model.lifecycle.restricted):
        when = "released today" if days_ago == 0 else f"{_days(days_ago)} ago"
        return cell(short_date(released), tone="new", note=f"New: {when}")
    return cell(short_date(released))


def _shutdown_cell(model: AIModel, today: date) -> dict:
    lifecycle = model.lifecycle
    tone = "bad" if lifecycle.deprecated else "caution"
    if lifecycle.shutdown_date:
        left = (date.fromisoformat(lifecycle.shutdown_date) - today).days
        when = "today" if left == 0 else "date has passed" if left < 0 else f"in {_days(left)}"
        return cell(short_date(lifecycle.shutdown_date), tone=tone, note=when)
    if lifecycle.deprecated:
        return cell("No date", tone=tone, note="Requests already go to its successor")
    return cell("None announced")


def _price_change_cell(model: AIModel, today: date) -> dict:
    cost = model.cost
    if not cost.effective_until:
        return cell("None scheduled")
    left = (date.fromisoformat(cost.effective_until) - today).days
    then = (
        f"then {price(cost.reverts_to.input_per_million)} / {price(cost.reverts_to.output_per_million)}"
        f" from {short_date(_day_after(cost.effective_until))}"
    )
    if left < 0:
        return cell(f"Intro price ended {short_date(cost.effective_until)}", tone="bad", note=then)
    remaining = "last day" if left == 0 else f"{_days(left)} left"
    return cell(f"Intro price until {short_date(cost.effective_until)}", tone="caution", note=f"{remaining}; {then}")


def _replacement_cell(model: AIModel, by_id: dict[str, AIModel], selected_ids: set[str], swap_href) -> dict:
    successor_id = model.lifecycle.replacement
    if not successor_id:
        return cell("None named")
    successor = by_id.get(successor_id)
    name = successor.name if successor else successor_id
    if successor_id in selected_ids or not successor:
        return cell(name, note="Already in this comparison" if successor_id in selected_ids else None)
    return cell(name, action={"label": "Swap in", "href": swap_href(model.id, successor_id)})


def lifecycle_section(
    selected: list[AIModel],
    all_models: list[AIModel],
    today: date,
    swap_href: Callable[[str, str], str],
) -> dict:
    by_id = {m.id: m for m in all_models}
    selected_ids = {m.id for m in selected}
    return {
        "title": "Lifecycle",
        "rows": [
            {"label": "Status", "cells": [_status_cell(m) for m in selected]},
            {"label": "Released", "cells": [_released_cell(m, today) for m in selected]},
            {"label": "Shutdown", "cells": [_shutdown_cell(m, today) for m in selected]},
            {"label": "Price change", "cells": [_price_change_cell(m, today) for m in selected]},
            {
                "label": "Replacement",
                "cells": [_replacement_cell(m, by_id, selected_ids, swap_href) for m in selected],
            },
        ],
        "note": "Provider dates; days counted from today.",
    }


def quality_section(selected: list[AIModel]) -> dict:
    profiles = [quality_profile(model) for model in selected]
    rows = []
    for index, dim in enumerate(profiles[0]):
        ordinals = [profile[index]["ordinal"] for profile in profiles]
        cells = [
            cell(
                profile[index]["level"].capitalize(),
                ordinal=profile[index]["ordinal"],
                max_ordinal=profile[index]["max_ordinal"],
            )
            for profile in profiles
        ]
        rows.append({"label": dim["label"], "segments": True, "cells": with_best(cells, ordinals, True)})
    return {"title": "Quality (editorial ratings)", "rows": rows}


def _cost_cell(model: AIModel, field: str) -> dict:
    item = cell(price(getattr(model.cost, field)))
    if model.cost.effective_until:
        reverted = getattr(model.cost.reverts_to, field)
        item["note"] = f"Introductory, through {model.cost.effective_until}; then {price(reverted)}"
    return item


def price_section(selected: list[AIModel]) -> dict:
    rows = []
    for label, field in _PRICE_FIELDS:
        values = [getattr(m.cost, field) for m in selected]
        cells = with_best([_cost_cell(m, field) for m in selected], values, False)
        rows.append({"label": label, "cells": with_ratios(with_bars(cells, values), values)})
    return {
        "title": "Price per 1M tokens",
        "rows": rows,
        "note": "Bars and ratios compare your picks only.",
    }


def _capacity_cell(model: AIModel, field: str, count: int | None, usd: float) -> dict:
    if count is None:
        return cell("No per-token charge listed")
    item = cell(tokens(count))
    if model.cost.effective_until:
        later = getattr(model.cost.reverts_to, field)
        if later > 0:
            item["note"] = f"From {short_date(_day_after(model.cost.effective_until))}: {tokens(round(usd / later * 1_000_000))}"
    return item


def budget_section(selected: list[AIModel], usd: float) -> dict:
    """What a typed-in monthly amount buys: two bounds, never a usage estimate."""
    capacity = {"input_per_million": estimated_input_capacity, "output_per_million": estimated_output_capacity}
    rows = []
    for label, field in _PRICE_FIELDS:
        counts = [capacity[field](usd, m) if getattr(m.cost, field) > 0 else None for m in selected]
        cells = [_capacity_cell(m, field, count, usd) for m, count in zip(selected, counts)]
        rows.append({"label": f"All on {label.lower()}", "cells": with_bars(with_best(cells, counts, True), counts)})
    return {
        "title": f"What {dollars(usd)} a month buys",
        "rows": rows,
        "note": "Two bounds, not an estimate: real use mixes input and output and lands in between. "
        "List prices, no discounts.",
    }


def limits_section(selected: list[AIModel]) -> dict:
    contexts = [m.operational.context_window for m in selected]
    outputs = [m.operational.max_output for m in selected]
    context_cells = with_best([cell(f"{v:,} tokens") for v in contexts], contexts, True)
    output_cells = with_best([cell("Not published" if v is None else f"{v:,} tokens") for v in outputs], outputs, True)
    return {
        "title": "Limits",
        "rows": [
            {"label": "Context window", "cells": with_bars(context_cells, contexts)},
            {"label": "Max output", "cells": with_bars(output_cells, outputs)},
        ],
    }


def capabilities_section(selected: list[AIModel]) -> dict:
    flags = [dict(capability_flags(model)) for model in selected]
    rows = [
        {"label": label, "cells": [cell("Yes" if f[label] else "No", flag=f[label]) for f in flags]}
        for label in flags[0]
    ]
    return {"title": "Capabilities", "rows": rows}


def _chip(route: AccessRoute, plan_names: dict[str, str]) -> dict:
    method = route.access.access_method
    if route.access.surface == Surface.DIRECT_API:
        label = f"{route.provider} API"
    else:
        # access_method reads "Product (detail)" or "Product, detail"; the chip keeps the product.
        label = method.split(" (")[0].split(",")[0]
    plans = [
        plan_names.get(plan_id, plan_id)
        for requirement in route.eligibility.requirements
        if requirement.kind == RequirementKind.CONSUMER_SUBSCRIPTION
        for plan_id in requirement.value
    ]
    return {
        "label": label,
        "detail": " or ".join(plans) or None,
        "title": method,
        "href": guide_ref_url(route.access.guide_ref),
    }


def access_section(selected: list[AIModel], routes: list[AccessRoute], plan_names: dict[str, str]) -> dict:
    rows = [
        {
            "label": "Free access",
            "cells": [cell("Yes" if m.access.has_free_access else "No", flag=m.access.has_free_access) for m in selected],
        }
    ]
    for surface, label in _SURFACE_ROWS:
        found = [[r for r in routes if r.model_id == m.id and r.access.surface == surface] for m in selected]
        if not any(found):
            continue
        cells = []
        for model_routes in found:
            chips = tuple(_chip(route, plan_names) for route in model_routes)
            text = "; ".join(f"{c['label']} {c['detail'] or ''}".strip() for c in chips) or "Not documented"
            cells.append(cell(text, chips=chips, tone=None if chips else "muted"))
        rows.append({"label": label, "cells": cells})
    return {
        "title": "Access",
        "rows": rows,
        "note": "Each chip links to its guide. Not documented is not the same as unavailable.",
    }
