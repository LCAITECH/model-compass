"""What-if: the same engine on another context, and what changed.

Everything here is decision/'s own output run again (evaluate + explain) on a
context that differs from the visitor's in one or two inputs, then compared:
which model wins, how many qualify, who enters or leaves the top. Nothing is
scored, estimated or given a confidence; a "change" is a different winner,
named. The sentences are built here, in Python, so tests pin them.

Only presentation-level comparison lives here (interfaces/): the engine is
not touched and never learns it is being asked a hypothetical.
"""

from collections.abc import Callable

from decision.domain import AIModel, BudgetLevel, BudgetMode, Context, Priority, Recommendation
from decision.evaluator import evaluate
from decision.explainer import NoQualifyingModelsError, explain
from interfaces.web.access_labels import humanize
from interfaces.web.catalog_notices import Badges
from interfaces.web.graph_data import graph_items

MAX_PRIORITIES = 3


def options() -> dict:
    """What the panel offers, read from the engine's own enums (never retyped)."""
    return {
        "budgets": [{"value": level.value, "label": humanize(level.value)} for level in BudgetLevel],
        "priorities": [{"value": p.value, "label": humanize(p.value)} for p in Priority],
        "max_priorities": MAX_PRIORITIES,
    }


def run(context: Context, models: list[AIModel]) -> Recommendation | None:
    """The engine's recommendation for `context`, or None when nothing qualifies."""
    try:
        return explain(context, evaluate(context, models))
    except NoQualifyingModelsError:
        return None


def _top_ids(recommendation: Recommendation) -> set[str]:
    return {recommendation.recommended.id} | {alt.model.id for alt in recommendation.alternatives}


def _names(ids: set[str], by_id: dict[str, AIModel]) -> list[str]:
    return sorted(by_id[model_id].name for model_id in ids if model_id in by_id)


def _join(names: list[str]) -> str:
    if len(names) <= 2:
        return " and ".join(names)
    return f"{', '.join(names[:-1])} and {names[-1]}"


def diff(base: Recommendation | None, scenario: Recommendation | None, models: list[AIModel]) -> dict:
    """What differs between the visitor's result and the scenario's."""
    by_id = {model.id: model for model in models}
    if scenario is None:
        return {"no_match": True, "winner_changed": base is not None}
    if base is None:
        return {"no_match": False, "winner_changed": True, "from": None, "to": _brief(scenario.recommended),
                "practically_tied": False, "qualifying": {"from": 0, "to": scenario.total_qualifying},
                "entered_top": [], "left_top": []}

    old_win, new_win = base.recommended, scenario.recommended
    scenario_tied = {option.model.id for option in scenario.also_strong_options}
    base_tied = {option.model.id for option in base.also_strong_options}
    changed = old_win.id != new_win.id
    # "Practically tied" in either direction: the old winner is one of the
    # scenario's also-strong options, or the new winner was one of the
    # visitor's. Both are the engine's own tie rule (explainer.py).
    tied = changed and (old_win.id in scenario_tied or new_win.id in base_tied)
    entered = _top_ids(scenario) - _top_ids(base) - {new_win.id}
    left = _top_ids(base) - _top_ids(scenario) - {old_win.id}
    return {
        "no_match": False,
        "winner_changed": changed,
        "from": _brief(old_win),
        "to": _brief(new_win),
        "practically_tied": tied,
        "qualifying": {"from": base.total_qualifying, "to": scenario.total_qualifying},
        "entered_top": _names(entered, by_id),
        "left_top": _names(left, by_id),
    }


def _brief(model: AIModel) -> dict:
    return {"id": model.id, "name": model.name}


def headline(change: dict) -> str:
    """One readable sentence for the panel, from the diff only."""
    if change["no_match"]:
        return "No model qualifies for this scenario."
    to = change["to"]["name"]
    if change["winner_changed"] and change["from"]:
        sentence = f"Winner: {change['from']['name']} → {to}"
        sentence += " (practically tied)." if change["practically_tied"] else "."
    elif change["winner_changed"]:
        sentence = f"Winner: {to}."
    else:
        sentence = f"{to} stays the winner."
    before, after = change["qualifying"]["from"], change["qualifying"]["to"]
    if before != after:
        sentence += f" {after} models qualify instead of {before}." if after != 1 else f" 1 model qualifies instead of {before}."
    if change["entered_top"]:
        names = change["entered_top"]
        sentence += f" {_join(names)} {'moves' if len(names) == 1 else 'move'} into the top alternatives."
    if change["left_top"]:
        names = change["left_top"]
        sentence += f" {_join(names)} {'drops' if len(names) == 1 else 'drop'} out of the top alternatives."
    return sentence


def scenario_payload(
    context: Context,
    base_context: Context,
    models: list[AIModel],
    badges_of: Callable[[AIModel], Badges],
    query: str,
) -> dict:
    """The graph's items and the diff for `context`, compared with `base_context`."""
    scenario = run(context, models)
    change = diff(run(base_context, models), scenario, models)
    return {
        "query": query,
        "winner": _brief(scenario.recommended) if scenario else None,
        "total_qualifying": scenario.total_qualifying if scenario else 0,
        "items": graph_items(scenario, badges_of) if scenario else [],
        "diff": change,
        "headline": headline(change),
    }


def _with(context: Context, *, budget: BudgetLevel | None = None, priorities: tuple[Priority, ...] | None = None) -> Context:
    return Context(
        use_case=context.use_case,
        budget_mode=context.budget_mode,
        budget=budget if budget is not None else context.budget,
        priorities=priorities if priorities is not None else context.priorities,
        language=context.language,
    )


def _neighbor_changes(context: Context):
    """Each nearby context changes one thing: (label, form fields to set, Context).

    Each priority order is offered once: moving the second priority to the
    front and swapping the top two are the same scenario.
    """
    if context.budget_mode == BudgetMode.TIER:
        for level in BudgetLevel:
            if level != context.budget:
                yield f"Budget → {humanize(level.value)}", {"budget": level.value}, _with(context, budget=level)
    seen = {context.priorities}
    for priority in Priority:
        if priority == context.priorities[0]:
            continue
        rest = tuple(p for p in context.priorities if p != priority)
        order = ((priority,) + rest)[:MAX_PRIORITIES]
        if order in seen:
            continue
        seen.add(order)
        yield (
            f"{humanize(priority.value)} as your first priority",
            _priority_fields(order),
            _with(context, priorities=order),
        )
    if len(context.priorities) > 1:
        order = (context.priorities[1], context.priorities[0]) + context.priorities[2:]
        if order not in seen:
            yield "Swap your top two priorities", _priority_fields(order), _with(context, priorities=order)


def _priority_fields(order: tuple[Priority, ...]) -> dict:
    fields = {f"priority_{index}": "" for index in range(1, MAX_PRIORITIES + 1)}
    fields.update({f"priority_{index}": priority.value for index, priority in enumerate(order, start=1)})
    return fields


def neighbors(context: Context, models: list[AIModel]) -> dict:
    """The single-step changes that give a different winner, each with the
    fields to set to apply it. Empty when the winner holds under all of them."""
    base = run(context, models)
    changes = []
    tested = 0
    for label, fields, nearby in _neighbor_changes(context):
        tested += 1
        result = run(nearby, models)
        if result is not None and base is not None and result.recommended.id == base.recommended.id:
            continue
        changes.append({
            "label": label,
            "set": fields,
            "winner": _brief(result.recommended) if result else None,
            "practically_tied": bool(
                result and base and (
                    base.recommended.id in {o.model.id for o in result.also_strong_options}
                    or result.recommended.id in {o.model.id for o in base.also_strong_options}
                )
            ),
        })
    return {"tested": tested, "changes": changes}
