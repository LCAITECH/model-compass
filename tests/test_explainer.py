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
    # deepseek-v4-flash is the cheapest of all 8 (blended cost 0.42) but
    # is not the strongest on any quality dimension or context window --
    # true with 5 models and still true with 8, since adding more
    # competitors can only add ground it doesn't win, never remove it.
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
    # claude-opus-5 ties claude-sonnet-5, gemini-2.5-pro, and gpt-5 for
    # the best reasoning, coding, and instruction_following among all 8
    # (all very_high -- "best" via _is_best_quality tolerates ties), and
    # ties claude-sonnet-5/gpt-5/gemini-2.5-pro for creative_writing too
    # (all high, the current ceiling for that dimension -- see
    # Docs/models/gpt-5.md). claude-opus-5 wins the reasoning-priority
    # tie-break by dataset load order (see test_evaluator.py). It's
    # still neither the cheapest (claude-opus-5 is the priciest model in
    # the dataset) nor the largest context window (gemini-2.5-flash and
    # gemini-2.5-pro both have a bigger one) -- same two trade-offs as
    # when claude-sonnet-5 was the winner under 5 models.
    context = Context(
        use_case="Complex agentic workflow",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.REASONING,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert recommendation.recommended.id == "claude-opus-5"
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
    assert recommendation.recommended.id not in {alt.model.id for alt in recommendation.alternatives}


def test_alternatives_get_honest_standout_reasons_or_none(models):
    # Winner is deepseek-v4-flash (cheapest, blended 0.42). Alternatives
    # ranked by cost among the other 12: gpt-5-nano (0.45), gpt-5-mini
    # (2.25), gemini-2.5-flash (2.80, tied with gemini-3.5-flash-lite but
    # alphabetically first) -- gpt-5-nano's arrival bumped mistral-large-3
    # out of the top 3. Among all 13 qualifying models, several tie for
    # the best quality on every dimension, so gpt-5-nano and gpt-5-mini
    # have nothing left to stand out on; gemini-2.5-flash now ties three
    # other Gemini models (2.5 Pro, 3.6 Flash, 3.5 Flash-Lite) for the
    # largest context window -- a tie still counts as "largest".
    context = Context(
        use_case="Bot",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)
    by_id = {alt.model.id: alt for alt in recommendation.alternatives}

    assert any("largest context window" in reason for reason in by_id["gemini-2.5-flash"].reasons)
    assert by_id["gpt-5-nano"].reasons == ()
    assert by_id["gpt-5-mini"].reasons == ()


def test_excluded_models_carry_their_disqualification_reasons(models):
    # Only mistral-large-3 supports "ko" -- none of the other 12 models
    # list it either, since every curated language list in this dataset
    # was inherited from a same-provider sibling, none of which support
    # "ko" (see Docs/models/*.md).
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
        "gpt-5",
        "gemini-2.5-pro",
        "claude-opus-5",
        "gpt-4o",
        "gpt-5-nano",
        "claude-haiku-4-5",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite",
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
