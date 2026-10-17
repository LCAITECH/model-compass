"""What-if: the same engine on another context, and what changed.

Expected values come from real runs of the engine on the real dataset (the
same discipline as the rest of the suite), never from guesses.
"""

import re

from decision.domain import BudgetLevel, BudgetMode, Context, Priority
from interfaces.web.whatif import headline, neighbors, options, run

AGENT = "/recommend?language=es&budget=high&priority_1=reasoning&priority_2=cost"
CHEAP_BOT = "/recommend?language=en&budget=low&priority_1=cost"


def _scenario(client, origin, **fields):
    return client.get("/whatif", params={**fields, "from": origin})


def _agent_low(client):
    return _scenario(client, AGENT, language="es", budget="low", priority_1="reasoning", priority_2="cost").json()


def test_the_scenario_is_the_same_result_the_normal_page_would_show(client):
    data = _agent_low(client)
    page = client.get("/recommend", params={"language": "es", "budget": "low", "priority_1": "reasoning", "priority_2": "cost"}).text

    listed = re.findall(r'<li data-ring="(\w+)" data-id="([^"]+)"', page)

    assert [(item["ring"], item["id"]) for item in data["items"]] == listed
    assert data["winner"]["id"] == listed[0][1]


def test_headline_when_the_winner_changes_and_the_top_reshuffles(client):
    data = _agent_low(client)

    assert data["headline"] == (
        "Winner: Gemini 3.8 Flash → Claude Haiku 5.5. 8 models qualify instead of 30. "
        "DeepSeek V4.1 Flash, GPT-6 Luna and Qwen3.8-Flash move into the top alternatives. "
        "Claude Sonnet 5.5, DeepSeek V4 Pro and Qwen3.8-Max drop out of the top alternatives."
    )
    assert data["diff"]["qualifying"] == {"from": 30, "to": 8}
    assert not data["diff"]["practically_tied"]


def test_headline_when_nothing_changes(client):
    data = _scenario(client, AGENT, language="es", budget="high", priority_1="reasoning", priority_2="cost").json()

    assert data["headline"] == "Gemini 3.8 Flash stays the winner."
    assert not data["diff"]["winner_changed"]


def test_a_new_winner_that_was_practically_tied_says_so(client):
    data = _scenario(client, CHEAP_BOT, language="en", budget="low", priority_1="context_window", priority_2="cost").json()

    assert data["headline"] == "Winner: Claude Haiku 5.5 → GPT-6 Luna (practically tied)."
    assert data["diff"]["practically_tied"]


def test_a_scenario_nothing_qualifies_for_says_so_and_has_no_dots(client):
    response = _scenario(client, AGENT, language="xx", budget="low", priority_1="cost")
    data = response.json()

    assert response.status_code == 200
    assert data["winner"] is None and data["items"] == []
    assert data["headline"] == "No model qualifies for this scenario."


def test_the_scenario_link_is_the_canonical_query_without_empty_fields(client):
    data = _scenario(client, CHEAP_BOT, language="en", budget="low", priority_1="context_window", priority_2="cost", priority_3="").json()

    assert data["query"] == "/recommend?language=en&budget=low&priority_1=context_window&priority_2=cost"


def test_bad_requests_are_refused_with_the_forms_own_messages(client):
    assert client.get("/whatif").status_code == 400
    assert client.get("/whatif", params={"language": "es", "budget": "low", "priority_1": "cost"}).status_code == 400
    bad_priority = _scenario(client, AGENT, language="es", budget="low", priority_1="nope")
    bad_origin = _scenario(client, "/recommend?language=es", language="es", budget="low", priority_1="cost")

    assert (bad_priority.status_code, bad_priority.json()["error"]) == (422, "Choose valid priorities.")
    assert bad_origin.status_code == 422


def test_nearby_changes_that_give_a_different_winner(client):
    data = client.get("/whatif/neighbors", params={"language": "es", "budget": "medium", "priority_1": "cost"}).json()

    assert data["tested"] == 8
    assert [(c["label"], c["winner"]["name"]) for c in data["changes"]] == [
        ("Reasoning as your first priority", "Gemini 3.8 Flash"),
        ("Coding as your first priority", "Gemini 3.8 Flash"),
        ("Context window as your first priority", "GPT-6 Luna"),
    ]
    assert data["changes"][0]["set"] == {"priority_1": "reasoning", "priority_2": "cost", "priority_3": ""}


def test_nearby_changes_flag_a_practically_tied_winner(client):
    data = client.get("/whatif/neighbors", params={"language": "en", "budget": "low", "priority_1": "cost"}).json()

    assert [(c["winner"]["name"], c["practically_tied"]) for c in data["changes"]] == [("GPT-6 Luna", True)]


def test_a_winner_that_holds_under_every_single_step_change_is_reported_as_such(client):
    data = client.get("/whatif/neighbors", params={"language": "en", "budget": "low", "priority_1": "cost", "priority_2": "creative_writing"}).json()

    # 3 budgets + 4 other priorities first; "creative writing first" is the same scenario as the swap.
    assert data == {"tested": 8, "changes": []}


def test_a_custom_dollar_budget_never_offers_budget_changes(client):
    data = client.get(
        "/whatif/neighbors", params={"language": "es", "budget_mode": "custom", "monthly_budget_usd": "30", "priority_1": "cost"}
    ).json()

    assert data["tested"] == 5
    assert not any("Budget" in change["label"] for change in data["changes"])


def test_each_priority_order_is_offered_once(models):
    # Moving the second priority to the front and swapping the top two are
    # the same scenario; it must not appear twice.
    context = Context("x", BudgetMode.TIER, BudgetLevel.MEDIUM, (Priority.REASONING, Priority.COST, Priority.CODING), "es")

    changes = neighbors(context, models)["changes"]
    sets = [tuple(sorted(change["set"].items())) for change in changes]

    assert len(sets) == len(set(sets))
    assert [c["label"] for c in changes] == ["Budget → Low", "Cost as your first priority"]


def test_neighbors_agree_with_running_the_engine_by_hand(models):
    context = Context("x", BudgetMode.TIER, BudgetLevel.HIGH, (Priority.REASONING, Priority.COST), "es")
    base = run(context, models).recommended.id

    by_hand = []
    for level in BudgetLevel:
        if level != context.budget:
            nearby = Context("x", BudgetMode.TIER, level, context.priorities, "es")
            result = run(nearby, models)
            if result is None or result.recommended.id != base:
                by_hand.append(f"Budget → {level.value.replace('_', ' ').capitalize()}")

    assert [c["label"] for c in neighbors(context, models)["changes"] if c["label"].startswith("Budget")] == by_hand


def test_the_result_page_carries_the_panel_with_the_visitors_own_context(client):
    page = client.get("/recommend", params={"language": "es", "budget": "high", "priority_1": "reasoning", "priority_2": "cost"}).text

    assert "data-whatif" in page and 'data-budget="high"' in page
    assert """data-priorities='["reasoning", "cost"]'""" in page
    assert 'data-base-query="/recommend?language=es&amp;budget=high&amp;priority_1=reasoning&amp;priority_2=cost"' in page
    assert "Your monthly budget in dollars" not in page


def test_with_a_dollar_budget_the_panel_only_offers_priorities(client):
    page = client.get(
        "/recommend", params={"language": "es", "budget_mode": "custom", "monthly_budget_usd": "30", "priority_1": "cost"}
    ).text

    assert 'data-budget=""' in page
    assert "Your monthly budget in dollars never filters or weighs the ranking" in page
    assert 'aria-label="Budget"' not in page


def test_a_page_with_no_recommendation_has_no_panel(client):
    page = client.get("/recommend", params={"language": "xx", "budget": "low", "priority_1": "cost"}).text

    assert "data-whatif" not in page


def test_headline_wording_for_small_counts():
    one_model = {
        "no_match": False, "winner_changed": False, "from": {"name": "A"}, "to": {"name": "A"},
        "practically_tied": False, "qualifying": {"from": 3, "to": 1},
        "entered_top": ["B"], "left_top": ["C", "D"],
    }

    assert headline(one_model) == (
        "A stays the winner. 1 model qualifies instead of 3. B moves into the top alternatives. "
        "C and D drop out of the top alternatives."
    )


def test_the_panels_options_come_from_the_engines_enums():
    offered = options()

    assert [b["value"] for b in offered["budgets"]] == [level.value for level in BudgetLevel]
    assert [p["value"] for p in offered["priorities"]] == [p.value for p in Priority]
    assert offered["priorities"][3] == {"value": "creative_writing", "label": "Creative writing"}
    assert offered["max_priorities"] == 3
