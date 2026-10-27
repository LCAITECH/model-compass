"""The comparator's newer pieces: lifecycle dates, the monthly-amount
section, price bars and ratios, access by surface, "only differences",
selection links, and the geometry of the orbit and the constellations."""

from dataclasses import replace
from datetime import date

import pytest

from decision.domain import BudgetLevel, BudgetMode, Context, Priority
from decision.evaluator import evaluate
from decision.explainer import explain
from decision.loader import load_access_routes, load_subscriptions
from interfaces.web.compare_cells import dollars, tokens
from interfaces.web.compare_visuals import constellations, orbit, podium
from interfaces.web.comparison import build_comparison, context_fit, row_counts, selection_links
from tests.conftest import ACCESS_ROUTES_DIR, SUBSCRIPTIONS_DIR

TODAY = date(2026, 10, 14)
ARGON = "gemini-4-argon"  # released 2026-10-13, introductory price through 2026-11-30
HAIKU = "claude-haiku-5-5"
NANO = "gpt-5-nano"  # deprecated, replacement gpt-5-6-luna
FABLE = "claude-fable-5-1"  # Claude subscription route on Max only


@pytest.fixture(scope="module")
def access_routes():
    return load_access_routes(ACCESS_ROUTES_DIR)


@pytest.fixture(scope="module")
def plan_names():
    return {plan.plan_id: plan.plan_name for plan in load_subscriptions(SUBSCRIPTIONS_DIR)}


def _by_id(models, *ids):
    index = {model.id: model for model in models}
    return [index[i] for i in ids]


def _row(sections, label):
    return next(row for section in sections for row in section["rows"] if row["label"] == label)


def _build(models, routes, *ids, **kwargs):
    return build_comparison(_by_id(models, *ids), routes, all_models=models, today=TODAY, **kwargs)


def _context():
    return Context(
        use_case="Coding agent",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.VERY_HIGH,
        priorities=(Priority.CODING, Priority.REASONING),
        language="en",
    )


def test_a_recent_release_is_marked_new_and_an_intro_price_counts_down(models, access_routes):
    sections = _build(models, access_routes, ARGON, NANO)

    argon, nano = _row(sections, "Released")["cells"]
    assert (argon["text"], argon["tone"], argon["note"]) == ("Oct 13, 2026", "new", "New: 1 day ago")
    assert (nano["text"], nano["tone"]) == ("Aug 7, 2025", None)

    argon, nano = _row(sections, "Price change")["cells"]
    assert argon["text"] == "Intro price until Nov 30, 2026"
    assert argon["note"] == "47 days left; then $4.00 / $20.00 from Dec 1, 2026"
    assert nano["text"] == "None scheduled"


def test_swap_in_replaces_the_deprecated_model_and_keeps_the_context(models, access_routes):
    form = {"language": "en", "budget": "high", "priority_1": "coding", "monthly_budget_usd": "20"}

    sections = _build(models, access_routes, NANO, HAIKU, form=form)

    action = _row(sections, "Replacement")["cells"][0]["action"]
    assert action["label"] == "Swap in"
    assert action["href"] == (
        "/compare?m=gpt-5-6-luna&m=claude-haiku-5-5&language=en&budget=high&priority_1=coding&monthly_budget_usd=20"
    )


def test_no_swap_when_the_successor_is_already_selected(models, access_routes):
    sections = _build(models, access_routes, NANO, "gpt-5-6-luna")

    nano = _row(sections, "Replacement")["cells"][0]
    assert nano["action"] is None
    assert nano["note"] == "Already in this comparison"


def test_monthly_amount_section_shows_both_bounds_and_the_price_to_come(models, access_routes):
    sections = _build(models, access_routes, ARGON, HAIKU, budget_usd=20)

    assert any(section["title"] == "What $20 a month buys" for section in sections)
    argon, haiku = _row(sections, "All on input")["cells"]
    assert argon["text"] == "10.0M tokens"  # $20 / $2.00 per 1M
    assert argon["note"] == "From Dec 1, 2026: 5.00M tokens"  # $20 / $4.00 per 1M
    assert haiku["text"] == "200M tokens"  # $20 / $0.10 per 1M
    assert haiku["best"] and haiku["bar"] == 100
    assert _row(sections, "All on output")["cells"][0]["text"] == "2.00M tokens"


def test_no_monthly_amount_section_without_an_amount(models, access_routes):
    sections = _build(models, access_routes, ARGON, HAIKU)

    assert not any(section["title"].startswith("What $") for section in sections)


def test_price_bars_and_ratios_compare_only_the_selected_models(models, access_routes):
    sections = _build(models, access_routes, ARGON, HAIKU)

    argon, haiku = _row(sections, "Input")["cells"]
    assert (argon["bar"], argon["ratio"]) == (100, "20×")  # $2.00 vs $0.10
    assert (haiku["bar"], haiku["ratio"], haiku["best"]) == (5, None, True)


def test_access_rows_group_routes_by_surface_and_name_the_plans(models, access_routes, plan_names):
    sections = _build(models, access_routes, FABLE, ARGON, plan_names=plan_names)

    fable, argon = _row(sections, "Subscription apps")["cells"]
    assert [chip["detail"] for chip in fable["chips"]] == ["Claude Max 5x or Claude Max 20x"]  # Pro pays Fable at API rates
    # Antigravity joined the Gemini app on 2026-10-27; both sit on the same three plans.
    plans_text = "Google AI Pro or Google AI Ultra 5x or Google AI Ultra 20x"
    assert [(chip["label"], chip["detail"]) for chip in argon["chips"]] == [
        ("Google Antigravity", plans_text),
        ("Gemini app", plans_text),
    ]
    fable_studio, argon_studio = _row(sections, "Studio")["cells"]
    assert (fable_studio["chips"], fable_studio["text"], fable_studio["tone"]) == ((), "Not documented", "muted")
    assert [chip["detail"] for chip in argon_studio["chips"]] == [
        "Google AI Pro or Google AI Ultra 5x or Google AI Ultra 20x"
    ]
    fable_api, argon_api = _row(sections, "Direct API")["cells"]
    assert [chip["label"] for chip in argon_api["chips"]] == ["Google API"]
    assert fable_api["chips"][0]["href"].endswith("anthropic.md#anthropicdirect-api")


def test_rows_that_read_the_same_are_flagged_and_counted(models, access_routes):
    haiku = _by_id(models, HAIKU)[0]
    twin = replace(haiku, id="haiku-twin", name="Haiku twin")

    sections = build_comparison([haiku, twin], access_routes, all_models=models, today=TODAY)

    assert _row(sections, "Input")["same"] and _row(sections, "Coding")["same"]
    counts = row_counts(sections)
    assert counts["differ"] < counts["total"]


def test_the_engine_row_is_never_hidden_as_same(models, access_routes):
    selected = _by_id(models, ARGON, HAIKU)
    fit = context_fit(selected, models, _context())

    sections = build_comparison(selected, access_routes, fit, all_models=models, today=TODAY)

    assert _row(sections, "Engine result")["same"] is False
    assert row_counts(sections)["total"] == sum(len(s["rows"]) for s in sections) - 1


def test_selection_links_remove_one_model_and_offer_the_engines_winner(models):
    context = _context()
    winner = explain(context, evaluate(context, models)).recommended
    others = [m for m in models if m.id != winner.id][:2]
    fit = context_fit(others, models, context)
    form = {"language": "en", "budget": "very_high", "priority_1": "coding"}

    links = selection_links(others, form, fit)

    assert links["remove"][others[0].id] == f"/compare?m={others[1].id}&language=en&budget=very_high&priority_1=coding"
    assert links["add_winner"].startswith(f"/compare?m={others[0].id}&m={others[1].id}&m={winner.id}&")


def test_context_fit_places_every_catalog_model_on_one_ring(models):
    selected = _by_id(models, ARGON, NANO)

    fit = context_fit(selected, models, _context())

    placed = [model.id for ring in fit["rings"].values() for model in ring]
    assert sorted(placed) == sorted(model.id for model in models)
    assert len(fit["rings"]["center"]) == 1
    nano = fit["cells"][1]
    assert (nano["ring"], nano["category"], nano["rank"]) == ("ex", "Excluded", None)


def test_orbit_lights_exactly_the_selected_models(models):
    selected = _by_id(models, ARGON, NANO, HAIKU)
    fit = context_fit(selected, models, _context())

    drawing = orbit(fit, selected)

    assert len(drawing["nodes"]) == len(models)
    lit = {node["name"]: node for node in drawing["nodes"] if node["series"]}
    assert set(lit) == {model.name for model in selected}
    assert lit["GPT-5 Nano"]["mark"] == "×"
    assert [entry["model"].id for entry in podium(fit, selected)][-1] == NANO  # excluded last


def test_constellation_vertices_sit_on_the_fixed_rings(models):
    shapes = constellations(_by_id(models, ARGON, HAIKU))

    for shape in shapes:
        for vertex in shape["vertices"]:
            radius = abs(vertex["x"] - 120) + abs(vertex["y"] - 120)  # on an axis: one offset is 0
            assert radius in (22, 44, 66, 88)
        assert len(shape["ghosts"]) == 1


def test_token_and_dollar_formatting():
    assert tokens(12_500_000) == "12.5M tokens"
    assert tokens(2_000_000) == "2.00M tokens"
    assert tokens(400_000) == "400K tokens"
    assert tokens(950) == "950 tokens"
    assert dollars(20) == "$20" and dollars(12.5) == "$12.50"


def test_compare_page_renders_the_new_pieces(client):
    response = client.get(
        "/compare",
        params=[("m", ARGON), ("m", HAIKU), ("monthly_budget_usd", "20")],
    )

    assert response.status_code == 200
    for fragment in ("What $20 a month buys", "only-diff", "Constellations", "picker-chip", "compare-cards"):
        assert fragment in response.text
    assert "orbit-svg" not in response.text  # no context, no engine verdict
    assert 'aria-label="Remove Gemini 4 Argon"' in response.text


def test_compare_page_with_context_draws_the_orbit_and_podium(client):
    response = client.get(
        "/compare",
        params=[("m", ARGON), ("m", HAIKU), ("language", "en"), ("budget", "very_high"), ("priority_1", "coding")],
    )

    assert "orbit-svg" in response.text
    assert "podium-step" in response.text
