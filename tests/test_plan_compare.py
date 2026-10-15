"""decision/access/plan_compare.py on the real dataset: which plans include
a model, the credits that count for it, and every branch of the verdict."""

import inspect

import pytest

import decision.access.plan_compare as plan_compare_module
from decision.access import api_cost, compare_plans
from decision.domain import MonthlyUsage, UseMode, Verdict
from decision.loader import load_access_routes, load_subscriptions
from tests.conftest import ACCESS_ROUTES_DIR, SUBSCRIPTIONS_DIR

OPUS = "claude-opus-5-5"  # $4 / $20 per 1M; on Claude Pro, Max 5x, Max 20x
ARGON = "gemini-4-argon"  # Gemini app on AI Pro and Ultra, AI Studio on Ultra only
NO_PLAN = "deepseek-v4-pro"  # no documented subscription route


@pytest.fixture(scope="module")
def routes():
    return load_access_routes(ACCESS_ROUTES_DIR)


@pytest.fixture(scope="module")
def plans():
    return load_subscriptions(SUBSCRIPTIONS_DIR)


@pytest.fixture(scope="module")
def by_id(models):
    return {model.id: model for model in models}


def _compare(by_id, routes, plans, model_id, use_mode=UseMode.MANUAL, **kwargs):
    return compare_plans(by_id[model_id], routes, plans, use_mode, **kwargs)


def test_lists_the_plans_that_name_the_model_cheapest_first(by_id, routes, plans):
    comparison = _compare(by_id, routes, plans, OPUS)

    assert [option.plan.plan_id for option in comparison.options] == ["claude-pro", "claude-max-5x", "claude-max-20x"]
    assert comparison.chosen.plan.plan_id == "claude-pro"
    assert comparison.monthly_usd == 20


def test_credits_count_only_where_the_plan_includes_them(by_id, routes, plans):
    options = {option.plan.plan_id: option for option in _compare(by_id, routes, plans, OPUS).options}

    assert options["claude-pro"].credits_usd is None
    assert (options["claude-max-5x"].credits_usd, options["claude-max-20x"].credits_usd) == (100, 200)
    # The multiplier's base plan, for "10x the price for 20x the usage".
    assert options["claude-max-20x"].base_price_usd == 20


def test_a_plan_route_on_one_surface_only_still_counts(by_id, routes, plans):
    options = {option.plan.plan_id: option for option in _compare(by_id, routes, plans, ARGON).options}

    assert len(options["google-ai-pro"].routes) == 1  # Gemini app only; AI Studio is Ultra-only
    assert len(options["google-ai-ultra-5x"].routes) == 2
    assert options["google-ai-pro"].credits_usd == 10


def test_building_an_app_always_points_to_the_api(by_id, routes, plans):
    for mode in (UseMode.API_INTEGRATION, UseMode.AUTOMATION):
        assert _compare(by_id, routes, plans, OPUS, mode).verdict == Verdict.API_TO_INTEGRATE


def test_a_model_no_plan_names_has_the_api_as_its_only_path(by_id, routes, plans):
    comparison = _compare(by_id, routes, plans, NO_PLAN)

    assert comparison.verdict == Verdict.API_ONLY_PATH
    assert comparison.options == () and comparison.chosen is None and comparison.monthly_usd is None


def test_without_usage_there_is_no_cost_verdict(by_id, routes, plans):
    comparison = _compare(by_id, routes, plans, OPUS)

    assert comparison.verdict == Verdict.NO_COST_VERDICT
    assert comparison.api_cost_usd is None


def test_api_cost_is_exact_at_list_prices(by_id):
    assert api_cost(by_id[OPUS], MonthlyUsage(input_tokens=1_000_000, output_tokens=500_000)) == pytest.approx(14)


def test_small_usage_is_cheaper_on_the_api(by_id, routes, plans):
    comparison = _compare(by_id, routes, plans, OPUS, usage=MonthlyUsage(1_000_000, 500_000))  # $14 vs $20

    assert comparison.verdict == Verdict.API_CHEAPER
    assert comparison.credits_cover_usage is False  # Claude Pro includes no API credits


def test_large_usage_says_the_plan_may_be_cheaper(by_id, routes, plans):
    comparison = _compare(by_id, routes, plans, OPUS, usage=MonthlyUsage(10_000_000, 5_000_000))  # $140 vs $20

    assert comparison.verdict == Verdict.PLAN_MAY_BE_CHEAPER


def test_max_credits_cover_usage_that_costs_less_than_them(by_id, routes, plans):
    usage = MonthlyUsage(5_000_000, 2_500_000)  # $70 on the API

    comparison = _compare(by_id, routes, plans, OPUS, plan_id="claude-max-5x", usage=usage)

    assert (comparison.monthly_usd, comparison.verdict) == (100, Verdict.API_CHEAPER)
    assert comparison.credits_cover_usage is True


def test_the_developer_can_override_the_list_price(by_id, routes, plans):
    comparison = _compare(by_id, routes, plans, OPUS, monthly_usd=25.0, usage=MonthlyUsage(1_000_000, 500_000))

    assert comparison.monthly_usd == 25
    assert comparison.verdict == Verdict.API_CHEAPER


def test_an_unknown_plan_falls_back_to_the_cheapest(by_id, routes, plans):
    assert _compare(by_id, routes, plans, OPUS, plan_id="no-such-plan").chosen.plan.plan_id == "claude-pro"


def test_the_module_never_reaches_the_ranking():
    source = inspect.getsource(plan_compare_module)

    assert "decision.evaluator" not in source and "decision.explainer" not in source
