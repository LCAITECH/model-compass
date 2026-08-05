from pathlib import Path

import pytest

from decision.domain import BudgetLevel, Context, Priority
from decision.evaluator import evaluate
from decision.loader import load_dataset

DATASET_DIR = Path(__file__).resolve().parents[1] / "dataset" / "models"


@pytest.fixture(scope="module")
def models():
    return load_dataset(DATASET_DIR)


def by_id(candidates, model_id):
    return next(c for c in candidates if c.model.id == model_id)


def test_every_model_gets_a_candidate(models):
    context = Context(
        use_case="Telegram community bot",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)

    assert len(candidates) == len(models)
    assert {c.model.id for c in candidates} == {m.id for m in models}


def test_disqualifies_models_that_dont_support_the_language(models):
    # Only mistral-large-3 lists "ko" among its supported languages.
    context = Context(
        use_case="Korean support assistant",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="ko",
    )

    candidates = evaluate(context, models)
    qualifying = [c for c in candidates if c.qualifies]

    assert [c.model.id for c in qualifying] == ["mistral-large-3"]
    other = by_id(candidates, "gemini-2.5-flash")
    assert not other.qualifies
    assert any("language" in reason for reason in other.disqualified_reasons)


def test_low_budget_only_admits_the_cheapest_cost_tier(models):
    # Blended cost (input+output per million): deepseek-v4-flash 0.42,
    # gpt-5-mini 2.25, gemini-2.5-flash 2.80, mistral-large-3 8.00,
    # claude-sonnet-5 12.00. With 5 models split into thirds, the two
    # cheapest land in the "low" cost tier.
    context = Context(
        use_case="High-volume low-cost bot",
        budget=BudgetLevel.LOW,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)
    qualifying = {c.model.id for c in candidates if c.qualifies}

    assert qualifying == {"deepseek-v4-flash", "gpt-5-mini"}


def test_cost_priority_picks_the_cheapest_qualifying_model(models):
    context = Context(
        use_case="High-volume low-cost bot",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)

    assert candidates[0].model.id == "deepseek-v4-flash"


def test_reasoning_priority_picks_the_strongest_reasoning_model(models):
    context = Context(
        use_case="Complex agentic workflow",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.REASONING,),
        language="es",
    )

    candidates = evaluate(context, models)

    assert candidates[0].model.id == "claude-sonnet-5"


def test_priority_order_changes_the_winner(models):
    cost_first = Context(
        use_case="Bot",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST, Priority.REASONING),
        language="es",
    )
    reasoning_first = Context(
        use_case="Bot",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.REASONING, Priority.COST),
        language="es",
    )

    cost_winner = evaluate(cost_first, models)[0].model.id
    reasoning_winner = evaluate(reasoning_first, models)[0].model.id

    assert cost_winner != reasoning_winner


def test_disqualified_candidates_are_ranked_after_qualifying_ones(models):
    context = Context(
        use_case="Korean support assistant",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="ko",
    )

    candidates = evaluate(context, models)

    qualifies_flags = [c.qualifies for c in candidates]
    assert qualifies_flags == sorted(qualifies_flags, reverse=True)


def test_empty_priorities_is_rejected(models):
    context = Context(
        use_case="Bot",
        budget=BudgetLevel.HIGH,
        priorities=(),
        language="es",
    )

    with pytest.raises(ValueError):
        evaluate(context, models)


def test_no_models_returns_no_candidates():
    context = Context(
        use_case="Bot",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )

    assert evaluate(context, []) == []
