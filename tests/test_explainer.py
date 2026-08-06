from pathlib import Path

import pytest

from decision.domain import BudgetLevel, Context, CostTier, Priority
from decision.evaluator import evaluate
from decision.explainer import NoQualifyingModelsError, explain
from decision.loader import load_dataset

DATASET_DIR = Path(__file__).resolve().parents[1] / "dataset" / "models"


@pytest.fixture(scope="module")
def models():
    return load_dataset(DATASET_DIR)


def test_cost_priority_explains_the_cheapest_model_and_its_weaknesses(models):
    # deepseek-v4-flash is the cheapest of all 5 (blended cost 0.42) but
    # is not the strongest on any quality dimension or context window.
    context = Context(
        use_case="High-volume low-cost bot",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert recommendation.recommended.id == "deepseek-v4-flash"
    assert recommendation.cost_tier == CostTier.LOW
    assert "your use case is High-volume low-cost bot" in recommendation.reasons[0]
    assert any("Lowest cost" in reason for reason in recommendation.reasons)
    assert any("es" in reason and "quality" in reason for reason in recommendation.reasons)
    assert len(recommendation.trade_offs) == 5  # every other factor, none of which it wins


def test_reasoning_priority_explains_a_model_that_dominates_most_factors(models):
    # claude-sonnet-5 has the best reasoning, coding, creative_writing
    # and instruction_following among all 5 — but is neither the
    # cheapest nor the largest context window (gemini-2.5-flash is).
    context = Context(
        use_case="Complex agentic workflow",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.REASONING,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert recommendation.recommended.id == "claude-sonnet-5"
    assert recommendation.cost_tier == CostTier.HIGH
    assert "your use case is Complex agentic workflow" in recommendation.reasons[0]
    assert any("Strongest reasoning" in reason for reason in recommendation.reasons)
    assert recommendation.trade_offs == (
        "Not the cheapest option among the qualifying alternatives",
        "Not the largest context window among the qualifying alternatives",
    )


def test_alternatives_are_capped(models):
    context = Context(
        use_case="Bot",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert len(recommendation.alternatives) == 3
    assert recommendation.recommended not in recommendation.alternatives


def test_excluded_models_carry_their_disqualification_reasons(models):
    # Only mistral-large-3 supports "ko".
    context = Context(
        use_case="Korean support assistant",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="ko",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert recommendation.recommended.id == "mistral-large-3"
    assert recommendation.alternatives == ()
    assert {excl.model.id for excl in recommendation.excluded} == {
        "gemini-2.5-flash",
        "gpt-5-mini",
        "claude-sonnet-5",
        "deepseek-v4-flash",
    }
    assert all(
        any("language" in reason for reason in excl.reasons)
        for excl in recommendation.excluded
    )


def test_no_opening_reason_when_use_case_is_blank(models):
    context = Context(
        use_case="",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert not recommendation.reasons[0].startswith("Because your use case")
    assert all("use case" not in reason for reason in recommendation.reasons)


def test_raises_when_no_model_qualifies(models):
    # No model in the dataset lists this made-up language code.
    context = Context(
        use_case="Bot",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="xx",
    )
    candidates = evaluate(context, models)

    with pytest.raises(NoQualifyingModelsError):
        explain(context, candidates)
