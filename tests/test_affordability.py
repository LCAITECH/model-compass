import pytest

from decision.domain import (
    AIModel,
    Capabilities,
    Cost,
    Ecosystem,
    IntegrationEase,
    License,
    Maturity,
    Operational,
    Quality,
    QualityLevel,
)
from interfaces.web.affordability import (
    cheapest_qualifying_alternative,
    cost_savings_pct,
    estimated_input_capacity,
    estimated_output_capacity,
    parse_budget_usd,
)


def _model(input_per_million: float, output_per_million: float, id: str = "test-model") -> AIModel:
    return AIModel(
        id=id,
        name=id,
        provider="Test",
        version="1",
        license=License.PROPRIETARY,
        capabilities=Capabilities(False, False, False, False, False, False),
        quality=Quality(QualityLevel.LOW, QualityLevel.LOW, QualityLevel.LOW, QualityLevel.LOW),
        languages=("en",),
        language_quality={"en": QualityLevel.LOW},
        operational=Operational(context_window=1000, max_output=1000),
        cost=Cost(input_per_million=input_per_million, output_per_million=output_per_million),
        ecosystem=Ecosystem(IntegrationEase.LOW, Maturity.STABLE),
    )


def test_estimated_input_and_output_capacity_are_independent_bounds():
    # $10 spent entirely on input vs. entirely on output -- two separate
    # extremes, not a combined total assuming some split.
    model = _model(input_per_million=2.0, output_per_million=10.0)

    assert estimated_input_capacity(10, model) == round((10 / 2.0) * 1_000_000)
    assert estimated_output_capacity(10, model) == round((10 / 10.0) * 1_000_000)


@pytest.mark.parametrize("raw", [None, "", "0", "-5", "not-a-number"])
def test_parse_budget_usd_rejects_invalid_input(raw):
    assert parse_budget_usd(raw) is None


def test_parse_budget_usd_accepts_a_positive_number():
    assert parse_budget_usd("12.50") == 12.50


def test_cost_savings_pct_is_an_exact_price_ratio():
    expensive = _model(input_per_million=2.0, output_per_million=10.0)
    cheap = _model(input_per_million=0.5, output_per_million=1.0)

    input_pct, output_pct = cost_savings_pct(expensive, cheap)

    assert input_pct == 75.0  # (2.0 - 0.5) / 2.0 * 100
    assert output_pct == 90.0  # (10.0 - 1.0) / 10.0 * 100


def test_cost_savings_pct_handles_a_free_axis_without_dividing_by_zero():
    from_model = _model(input_per_million=0.0, output_per_million=5.0)
    to_model = _model(input_per_million=0.0, output_per_million=2.0)

    input_pct, output_pct = cost_savings_pct(from_model, to_model)

    assert input_pct == 0
    assert output_pct == 60.0


def test_cheapest_qualifying_alternative_finds_the_true_minimum():
    winner = _model(input_per_million=2.0, output_per_million=10.0, id="winner")
    mid = _model(input_per_million=1.0, output_per_million=3.0, id="mid")
    cheapest = _model(input_per_million=0.1, output_per_million=0.2, id="cheapest")

    result = cheapest_qualifying_alternative(winner, [winner, mid, cheapest])

    assert result.id == "cheapest"


def test_cheapest_qualifying_alternative_is_none_when_winner_is_already_cheapest():
    winner = _model(input_per_million=0.1, output_per_million=0.2, id="winner")
    pricier = _model(input_per_million=1.0, output_per_million=3.0, id="pricier")

    assert cheapest_qualifying_alternative(winner, [winner, pricier]) is None
