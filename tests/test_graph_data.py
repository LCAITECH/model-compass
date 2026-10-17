"""The decision graph's data: one dot per catalog model, with its real ring."""

import re
from datetime import date

from decision.domain import BudgetLevel, BudgetMode, Context, Priority
from decision.evaluator import evaluate
from decision.explainer import explain
from interfaces.web.catalog_notices import Badges, badges_for
from interfaces.web.graph_data import graph_items, ring_counts

_NO_BADGES = Badges(None, None, None)


def _recommendation(models):
    context = Context("Agent", BudgetMode.TIER, BudgetLevel.HIGH, (Priority.REASONING, Priority.COST), "es")
    return explain(context, evaluate(context, models))


def _items(models):
    return graph_items(_recommendation(models), lambda model: _NO_BADGES)


def test_every_catalog_model_is_a_dot_exactly_once_with_the_winner_first(models):
    items = _items(models)

    assert [item["id"] for item in items].count(items[0]["id"]) == 1
    assert {item["id"] for item in items} == {model.id for model in models}
    assert len(items) == len(models)
    assert items[0]["ring"] == "center" and items[0]["id"] == _recommendation(models).recommended.id


def test_rings_follow_the_engines_own_standing(models):
    recommendation = _recommendation(models)
    items = _items(models)
    tied_ids = {option.model.id for option in recommendation.also_strong_options}
    by_ring = {ring: [item for item in items if item["ring"] == ring] for ring in ("alt", "tied", "out", "ex")}

    assert [item["id"] for item in by_ring["alt"]] == [alt.model.id for alt in recommendation.alternatives]
    assert [item["rank"] for item in by_ring["alt"]] == [2, 3, 4]
    assert {item["id"] for item in by_ring["tied"]} <= tied_ids
    assert not any(item["id"] in tied_ids for item in by_ring["out"])
    assert {item["id"] for item in by_ring["ex"]} == {e.model.id for e in recommendation.excluded}
    ranks = [item["rank"] for item in by_ring["tied"] + by_ring["out"]]
    assert ranks == sorted(ranks)  # ring by ring, best first within the qualifying ones


def test_a_dot_carries_only_what_its_ring_can_say(models):
    center, *others = _items(models)

    assert "reasons" not in center and "input" not in center  # the winner's reasons live in the hero card
    excluded = next(item for item in others if item["ring"] == "ex")
    assert excluded["rank"] is None and excluded["reasons"]
    assert all(item["input"] and item["output"] for item in others)


def test_ring_counts_add_up_to_everything_but_the_winner(models):
    counts = ring_counts(_items(models))

    assert sum(counts.values()) == len(models) - 1


def test_dated_facts_become_marks_on_the_dot(models):
    today = date(2026, 10, 14)
    by_id = {model.id: model for model in models}
    mark = lambda model_id: next(  # noqa: E731
        item for item in graph_items(_recommendation(models), lambda m: badges_for(m, models, today))
        if item["id"] == model_id
    )

    assert mark("gemini-3.8-flash")["promo"] == "Dec 31, 2026"
    assert mark("gpt-5")["retiring"] == "Dec 11, 2026" and mark("gpt-5")["deprecated"]
    assert mark("gemini-3.5-flash")["retiring"] == "routed"
    assert by_id["gemini-4-argon"].id in {item["id"] for item in graph_items(_recommendation(models), lambda m: badges_for(m, models, today)) if item["is_new"]}


def test_the_result_page_lists_the_same_dots_and_legend_numbers(client, models):
    response = client.get("/recommend", params={"language": "es", "budget": "high", "priority_1": "reasoning", "priority_2": "cost"})
    html = response.text

    listed = re.findall(r'<li data-ring="(\w+)" data-id="([^"]+)"', html)
    expected = [(item["ring"], item["id"]) for item in _items(models)]
    legend = {ring: int(count) for ring, count in re.findall(r'data-ring-count="(\w+)">(\d+)<', html)}

    assert listed == expected
    assert legend == ring_counts(_items(models))
