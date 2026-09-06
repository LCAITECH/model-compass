"""The winner's reasons/trade-offs, and the two edge cases around them."""

import pytest

from decision.domain import BudgetLevel, BudgetMode, Context, CostTier, Priority
from decision.evaluator import evaluate
from decision.explainer import NoQualifyingModelsError, explain


def test_cost_priority_explains_the_cheapest_model_and_its_weaknesses(models):
    # gpt-5-nano ($0.45 blended) is the cheapest model in the dataset and
    # is not the strongest on any quality dimension or context window.
    # Previously deepseek-v4-flash held this spot at a stale $0.42
    # blended; the 2026-08-27 catalog refresh corrected it to the
    # official peak rate ($1.76 blended, see Docs/CHANGELOG.md),
    # handing the win to gpt-5-nano.
    context = Context(
        use_case="High-volume low-cost bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert recommendation.recommended.id == "gpt-5-nano"
    assert recommendation.cost_tier == CostTier.LOW
    assert "your use case is High-volume low-cost bot" in recommendation.reasons[0]
    assert any("Lowest cost" in reason for reason in recommendation.reasons)
    assert any("Supports Spanish" in reason and "quality" in reason for reason in recommendation.reasons)
    assert len(recommendation.trade_offs) == 5  # every other factor, none of which it wins


def test_reasoning_priority_explains_a_model_that_dominates_most_factors(models):
    # claude-fable-5 and claude-fable-5-1 are the only models in the
    # dataset rated very_high on creative_writing (see
    # Docs/models/claude-fable-5.md / claude-fable-5-1.md), so whichever
    # of the two wins the tie-break "wins" that dimension outright, not
    # just by tie -- and both tie several other flagship models
    # (claude-opus-4-7/4-8/5, claude-sonnet-5, gemini-2.5-pro, gpt-5) on
    # reasoning/coding/instruction_following (all very_high).
    # claude-fable-5-1 wins the reasoning-priority tie-break by dataset
    # load order (see test_evaluator.py). Still neither the cheapest
    # (tied priciest in the dataset with claude-fable-5, at $10/$50
    # direct API pricing) nor the largest context window (several
    # Gemini models have a bigger one) -- same two trade-offs as every
    # prior winner of this test. budget=VERY_HIGH (not HIGH) because
    # claude-fable-5-1's $60 blended cost puts it in CostTier.VERY_HIGH
    # -- a "high" budget correctly excludes it now that CostTier is a
    # fixed price band, not a relative tercile.
    context = Context(
        use_case="Complex agentic workflow",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.VERY_HIGH,
        priorities=(Priority.REASONING,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert recommendation.recommended.id == "claude-fable-5-1"
    assert recommendation.cost_tier == CostTier.VERY_HIGH
    assert "your use case is Complex agentic workflow" in recommendation.reasons[0]
    assert any("Strongest reasoning" in reason for reason in recommendation.reasons)
    assert recommendation.trade_offs == (
        "Not the cheapest option among the qualifying alternatives",
        "Not the largest context window among the qualifying alternatives",
    )


def test_no_opening_reason_when_use_case_is_blank(models):
    context = Context(
        use_case="",
        budget_mode=BudgetMode.TIER,
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
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="xx",
    )
    candidates = evaluate(context, models)

    with pytest.raises(NoQualifyingModelsError):
        explain(context, candidates)
