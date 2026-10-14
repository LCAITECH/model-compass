"""The static model comparator: /compare and interfaces/web/comparison.py."""

from dataclasses import replace

import pytest

from decision.domain import BudgetLevel, BudgetMode, Context, Operational, Priority
from decision.evaluator import evaluate
from decision.explainer import explain
from decision.loader import load_access_routes
from interfaces.web.comparison import MAX_COMPARED, build_comparison, context_fit, parse_selection
from tests.conftest import ACCESS_ROUTES_DIR

ARGON = "gemini-4-argon"
HAIKU = "claude-haiku-5-5"
NANO = "gpt-5-nano"


@pytest.fixture(scope="module")
def access_routes():
    return load_access_routes(ACCESS_ROUTES_DIR)


def _row(sections, label):
    return next(row for section in sections for row in section["rows"] if row["label"] == label)


def _by_id(models, *ids):
    index = {model.id: model for model in models}
    return [index[i] for i in ids]


def test_compare_without_selection_shows_only_the_picker(client):
    response = client.get("/compare")

    assert response.status_code == 200
    assert "Compare models" in response.text
    assert "compare-table" not in response.text


def test_compare_two_models_renders_a_side_by_side_table(client):
    response = client.get("/compare", params=[("m", ARGON), ("m", HAIKU)])

    assert response.status_code == 200
    assert "compare-table" in response.text
    assert "Gemini 4 Argon" in response.text
    assert "Claude Haiku 5.5" in response.text
    assert "Price per 1M tokens" in response.text


def test_compare_one_model_asks_for_a_second(client):
    response = client.get("/compare", params=[("m", ARGON)])

    assert response.status_code == 200
    assert "compare-table" not in response.text
    assert "Pick at least 2 models" in response.text


def test_compare_ignores_unknown_ids_and_blanks(client):
    response = client.get("/compare", params=[("m", ARGON), ("m", ""), ("m", "no-such-model"), ("m", HAIKU)])

    assert response.status_code == 200
    assert "compare-table" in response.text


def test_parse_selection_dedupes_keeps_order_and_caps(models):
    ids = [m.id for m in models[:6]]

    selected = parse_selection([ids[1], ids[0], ids[1], "nope", *ids[2:]], models)

    assert [m.id for m in selected] == [ids[1], ids[0], ids[2], ids[3]]
    assert len(selected) == MAX_COMPARED


def test_best_marks_the_lowest_price_only_when_prices_differ(models, access_routes):
    sections = build_comparison(_by_id(models, ARGON, NANO), access_routes)

    inputs = _row(sections, "Input")["cells"]

    assert [cell["best"] for cell in inputs] == [False, True]  # gpt-5-nano is cheaper than Argon


def test_no_best_mark_when_values_are_identical(models, access_routes):
    twin = replace(_by_id(models, HAIKU)[0], id="haiku-twin", name="Haiku twin")

    sections = build_comparison([_by_id(models, HAIKU)[0], twin], access_routes)

    assert not any(cell["best"] for cell in _row(sections, "Input")["cells"])
    assert not any(cell["best"] for cell in _row(sections, "Context window")["cells"])


def test_unpublished_max_output_is_shown_as_such_and_never_best(models, access_routes):
    haiku, argon = _by_id(models, HAIKU, ARGON)
    unpublished = replace(argon, operational=Operational(context_window=1000, max_output=None))

    sections = build_comparison([haiku, unpublished], access_routes)

    cells = _row(sections, "Max output")["cells"]
    assert cells[1]["text"] == "Not published"
    assert cells[1]["best"] is False
    assert cells[0]["best"] is False  # a single published value is not "best" against nothing


def test_introductory_price_is_noted_on_the_cell(models, access_routes):
    sections = build_comparison(_by_id(models, ARGON, HAIKU), access_routes)

    note = _row(sections, "Input")["cells"][0]["note"]

    assert note is not None and "2026-11-30" in note and "$4.00" in note


def test_result_page_links_to_a_prefilled_comparison(client):
    response = client.post(
        "/recommend",
        data={"use_case": "Telegram community bot", "language": "es", "budget": "low", "priority_1": "cost"},
    )

    assert response.status_code == 200
    assert "/compare?m=" in response.text


def _context(budget=BudgetLevel.VERY_HIGH, priorities=(Priority.CODING, Priority.REASONING), language="en"):
    return Context(
        use_case="Coding agent",
        budget_mode=BudgetMode.TIER,
        budget=budget,
        priorities=priorities,
        language=language,
    )


def test_context_fit_matches_the_engine_ranking_exactly(models):
    context = _context()
    recommendation = explain(context, evaluate(context, models))
    expected = {recommendation.recommended.id: 1}
    for entry in (*recommendation.alternatives, *recommendation.outranked):
        expected[entry.model.id] = entry.rank

    selected = _by_id(models, ARGON, HAIKU, NANO)
    fit = context_fit(selected, models, context)

    assert fit["total"] == recommendation.total_qualifying
    for model, cell in zip(selected, fit["cells"]):
        assert cell["text"].startswith(f"#{expected[model.id]} of {fit['total']}")


def test_context_fit_flags_the_winner_and_an_over_budget_model(models):
    context = _context(budget=BudgetLevel.LOW, priorities=(Priority.COST,), language="es")
    winner = explain(context, evaluate(context, models)).recommended

    fit = context_fit(_by_id(models, winner.id, ARGON), models, context)

    assert fit["winner"].id == winner.id
    assert fit["cells"][0]["tone"] == "good" and "Best match" in fit["cells"][0]["text"]
    assert fit["cells"][1]["text"] == "Excluded"
    assert fit["cells"][1]["reasons"] == ("cost tier exceeds a 'low' budget",)


def test_context_fit_handles_a_context_nothing_qualifies_for(models):
    context = _context(language="xx")  # no model supports it

    fit = context_fit(_by_id(models, ARGON, HAIKU), models, context)

    assert fit["winner"] is None and fit["total"] == 0
    assert all(cell["text"] == "Excluded" and cell["reasons"] for cell in fit["cells"])


def test_build_comparison_puts_the_context_row_first_only_when_given(models, access_routes):
    selected = _by_id(models, ARGON, HAIKU)
    fit = context_fit(selected, models, _context())

    with_fit = build_comparison(selected, access_routes, fit)
    without = build_comparison(selected, access_routes)

    assert with_fit[0]["title"] == "For your context"
    assert without[0]["title"] == "Overview"


def test_compare_page_shows_the_engine_row_when_context_is_given(client):
    response = client.get(
        "/compare",
        params=[("m", ARGON), ("m", HAIKU), ("language", "en"), ("budget", "very_high"), ("priority_1", "coding")],
    )

    assert response.status_code == 200
    assert "Engine result" in response.text
    assert "the engine's #1 among all" in response.text


def test_compare_page_without_context_has_no_engine_row(client):
    response = client.get("/compare", params=[("m", ARGON), ("m", HAIKU)])

    assert "Engine result" not in response.text


def test_compare_page_reports_an_incomplete_context_but_keeps_the_table(client):
    response = client.get("/compare", params=[("m", ARGON), ("m", HAIKU), ("language", "en")])

    assert response.status_code == 200
    assert "Choose a budget." in response.text
    assert "compare-table" in response.text
    assert "Engine result" not in response.text


def test_result_page_comparison_link_carries_the_context(client):
    response = client.post(
        "/recommend",
        data={"use_case": "Bot", "language": "es", "budget": "low", "priority_1": "cost"},
    )

    assert "&amp;language=es" in response.text
    assert "&amp;budget=low" in response.text
    assert "&amp;priority_1=cost" in response.text
