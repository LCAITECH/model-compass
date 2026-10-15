"""Subscription plans: price, usage multiplier and included API credits
(SCHEMA.md, "Subscription plans"), against the real files and a few
broken ones."""

import pytest

from decision.domain import Surface
from decision.loader import DatasetValidationError, load_subscription_file, load_subscriptions
from tests.conftest import SUBSCRIPTIONS_DIR

_PLAN = """
provider: Anthropic
plan_name: Test Plan
surface_entitlements: [consumer_subscription]
documented_exclusions: ["no API billing"]
region_scope: account_dependent
source_url: https://example.com
consulted_at: "2026-10-14"
status: confirmed
price: PRICE
usage_multiplier: MULTIPLIER
api_credits: CREDITS
"""


def _write(tmp_path, name="test-plan", price="{monthly_usd: 20}", multiplier="null", credits="null"):
    directory = tmp_path / "subscriptions" / "anthropic"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{name}.yaml"
    text = _PLAN.replace("PRICE", price).replace("MULTIPLIER", multiplier).replace("CREDITS", credits)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture(scope="module")
def plans():
    return {plan.plan_id: plan for plan in load_subscriptions(SUBSCRIPTIONS_DIR)}


def test_every_real_plan_has_a_positive_price(plans):
    assert all(plan.price.monthly_usd > 0 for plan in plans.values())
    assert plans["claude-pro"].price.monthly_usd == 20
    assert plans["google-ai-ultra-20x"].price.monthly_usd == 199.99


def test_max_tiers_state_their_multiplier_and_api_credits(plans):
    max_5x, max_20x = plans["claude-max-5x"], plans["claude-max-20x"]

    assert (max_5x.usage_multiplier.relative_to, max_5x.usage_multiplier.factor) == ("claude-pro", 5)
    assert max_20x.usage_multiplier.factor == 20
    assert (max_5x.api_credits.monthly_usd, max_5x.api_credits.surface) == (100, Surface.DIRECT_API)
    assert max_20x.api_credits.monthly_usd == 200


def test_plans_without_published_multiplier_or_credits_store_none(plans):
    assert plans["claude-pro"].usage_multiplier is None and plans["claude-pro"].api_credits is None
    assert all(plans[f"chatgpt-pro-{tier}"].usage_multiplier is None for tier in (100, 200, 500))
    assert plans["google-ai-pro"].usage_multiplier is None
    assert plans["google-ai-pro"].api_credits.monthly_usd == 10


def test_rejects_a_missing_or_zero_price(tmp_path):
    with pytest.raises(DatasetValidationError, match="price.monthly_usd"):
        load_subscription_file(_write(tmp_path, price="{monthly_usd: 0}"))


def test_the_new_keys_are_required_even_when_null(tmp_path):
    path = _write(tmp_path)
    path.write_text(path.read_text(encoding="utf-8").replace("api_credits: null\n", ""), encoding="utf-8")

    with pytest.raises(DatasetValidationError, match="missing required field 'api_credits'"):
        load_subscription_file(path)


def test_rejects_a_multiplier_without_a_factor_or_relative_to_itself(tmp_path):
    with pytest.raises(DatasetValidationError, match="factor must be a number"):
        load_subscription_file(_write(tmp_path, multiplier="{relative_to: other, scope: per session}"))
    with pytest.raises(DatasetValidationError, match="cannot be the plan itself"):
        load_subscription_file(_write(tmp_path, multiplier="{relative_to: test-plan, factor: 5, scope: per session}"))


def test_rejects_credits_with_an_unknown_surface(tmp_path):
    credits = "{monthly_usd: 10, surface: somewhere, conditions: expires monthly}"

    with pytest.raises(DatasetValidationError, match="invalid api_credits.surface"):
        load_subscription_file(_write(tmp_path, credits=credits))


def test_multiplier_must_point_at_a_plan_in_the_catalog(tmp_path):
    _write(tmp_path, name="base")
    _write(tmp_path, name="bigger", multiplier="{relative_to: missing-plan, factor: 5, scope: per session}")

    with pytest.raises(DatasetValidationError, match="unknown plan_id 'missing-plan'"):
        load_subscriptions(tmp_path / "subscriptions")
