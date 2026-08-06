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
from interfaces.web.affordability import estimated_token_capacity, parse_budget_usd


def _model(input_per_million: float, output_per_million: float) -> AIModel:
    return AIModel(
        id="test-model",
        name="Test Model",
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


def test_estimated_token_capacity_is_budget_over_blended_price():
    model = _model(input_per_million=2.0, output_per_million=10.0)  # blended = 12.0

    assert estimated_token_capacity(10, model) == round((10 / 12.0) * 1_000_000)


@pytest.mark.parametrize("raw", [None, "", "0", "-5", "not-a-number"])
def test_parse_budget_usd_rejects_invalid_input(raw):
    assert parse_budget_usd(raw) is None


def test_parse_budget_usd_accepts_a_positive_number():
    assert parse_budget_usd("12.50") == 12.50
