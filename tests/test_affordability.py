import pytest

from decision.domain import Priority, QualityLevel
from interfaces.web.affordability import (
    cheapest_qualifying_alternative,
    cost_savings_pct,
    estimated_input_capacity,
    estimated_output_capacity,
    parse_budget_usd,
)


def test_estimated_input_and_output_capacity_are_independent_bounds(make_model):
    # $10 spent entirely on input vs. entirely on output -- two separate
    # extremes, not a combined total assuming some split.
    model = make_model(input_per_million=2.0, output_per_million=10.0)

    assert estimated_input_capacity(10, model) == round((10 / 2.0) * 1_000_000)
    assert estimated_output_capacity(10, model) == round((10 / 10.0) * 1_000_000)


@pytest.mark.parametrize("raw", [None, "", "0", "-5", "not-a-number"])
def test_parse_budget_usd_rejects_invalid_input(raw):
    assert parse_budget_usd(raw) is None


def test_parse_budget_usd_accepts_a_positive_number():
    assert parse_budget_usd("12.50") == 12.50


def test_cost_savings_pct_is_an_exact_price_ratio(make_model):
    expensive = make_model(input_per_million=2.0, output_per_million=10.0)
    cheap = make_model(input_per_million=0.5, output_per_million=1.0)

    input_pct, output_pct = cost_savings_pct(expensive, cheap)

    assert input_pct == 75.0  # (2.0 - 0.5) / 2.0 * 100
    assert output_pct == 90.0  # (10.0 - 1.0) / 10.0 * 100


def test_cost_savings_pct_handles_a_free_axis_without_dividing_by_zero(make_model):
    from_model = make_model(input_per_million=0.0, output_per_million=5.0)
    to_model = make_model(input_per_million=0.0, output_per_million=2.0)

    input_pct, output_pct = cost_savings_pct(from_model, to_model)

    assert input_pct == 0
    assert output_pct == 60.0


def test_cheapest_qualifying_alternative_finds_the_true_minimum(make_model):
    winner = make_model(input_per_million=2.0, output_per_million=10.0, id="winner")
    mid = make_model(input_per_million=1.0, output_per_million=3.0, id="mid")
    cheapest = make_model(input_per_million=0.1, output_per_million=0.2, id="cheapest")

    result = cheapest_qualifying_alternative(winner, [winner, mid, cheapest])

    assert result.id == "cheapest"


def test_cheapest_qualifying_alternative_is_none_when_winner_is_already_cheapest(make_model):
    winner = make_model(input_per_million=0.1, output_per_million=0.2, id="winner")
    pricier = make_model(input_per_million=1.0, output_per_million=3.0, id="pricier")

    assert cheapest_qualifying_alternative(winner, [winner, pricier]) is None


def test_quality_floor_admits_an_alternative_within_one_tier(make_model):
    # winner is very_high (ordinal 3) on reasoning; an alternative rated
    # high (ordinal 2) is only one tier below -- a fair swap.
    winner = make_model(input_per_million=5.0, output_per_million=25.0, id="winner", reasoning=QualityLevel.VERY_HIGH)
    fair = make_model(input_per_million=0.5, output_per_million=1.0, id="fair", reasoning=QualityLevel.HIGH)

    result = cheapest_qualifying_alternative(winner, [winner, fair], priority_1=Priority.REASONING)

    assert result.id == "fair"


def test_quality_floor_rejects_an_alternative_more_than_one_tier_below(make_model):
    # winner is very_high (ordinal 3); the only cheaper model is low
    # (ordinal 0) -- more than one tier below, not a fair swap, so no
    # alternative should be surfaced even though it's much cheaper.
    winner = make_model(input_per_million=5.0, output_per_million=25.0, id="winner", reasoning=QualityLevel.VERY_HIGH)
    unfair = make_model(input_per_million=0.1, output_per_million=0.2, id="unfair", reasoning=QualityLevel.LOW)

    assert cheapest_qualifying_alternative(winner, [winner, unfair], priority_1=Priority.REASONING) is None


def test_quality_floor_picks_the_cheapest_among_multiple_fair_options(make_model):
    winner = make_model(input_per_million=5.0, output_per_million=25.0, id="winner", reasoning=QualityLevel.VERY_HIGH)
    fair_cheap = make_model(input_per_million=0.5, output_per_million=1.0, id="fair-cheap", reasoning=QualityLevel.HIGH)
    fair_pricier = make_model(input_per_million=1.0, output_per_million=2.0, id="fair-pricier", reasoning=QualityLevel.HIGH)
    unfair_cheapest = make_model(input_per_million=0.1, output_per_million=0.2, id="unfair-cheapest", reasoning=QualityLevel.LOW)

    result = cheapest_qualifying_alternative(
        winner, [winner, fair_cheap, fair_pricier, unfair_cheapest], priority_1=Priority.REASONING
    )

    assert result.id == "fair-cheap"  # cheapest of the two fair options, not the unfair cheapest overall


def test_quality_floor_is_a_noop_when_priority_1_is_cost_or_unset(make_model):
    # COST and CONTEXT_WINDOW aren't quality dimensions -- there's no
    # tier to protect, so the search falls back to the true cheapest,
    # same as before this rule existed.
    winner = make_model(input_per_million=5.0, output_per_million=25.0, id="winner", reasoning=QualityLevel.VERY_HIGH)
    cheapest_but_unfair = make_model(input_per_million=0.1, output_per_million=0.2, id="cheapest", reasoning=QualityLevel.LOW)

    assert (
        cheapest_qualifying_alternative(winner, [winner, cheapest_but_unfair], priority_1=Priority.COST).id
        == "cheapest"
    )
    assert (
        cheapest_qualifying_alternative(winner, [winner, cheapest_but_unfair], priority_1=None).id == "cheapest"
    )
