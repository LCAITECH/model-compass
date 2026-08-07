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
    # Blended cost (input+output per million), ascending: deepseek-v4-flash
    # 0.42, gpt-5-mini 2.25, gemini-2.5-flash 2.80, mistral-large-3 8.00,
    # gemini-2.5-pro 11.25, gpt-5 11.25, claude-sonnet-5 12.00, gpt-4o
    # 12.50, claude-opus-5 30.00. With 9 models, tier = rank*3//9: ranks
    # 0-2 (the three cheapest) land in "low", 3-5 in "medium", 6-8 in
    # "high" -- the low tier is unchanged from the 8-model dataset,
    # since gpt-4o lands in the high tier alongside sonnet and opus.
    context = Context(
        use_case="High-volume low-cost bot",
        budget=BudgetLevel.LOW,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)
    qualifying = {c.model.id for c in candidates if c.qualifies}

    assert qualifying == {"deepseek-v4-flash", "gpt-5-mini", "gemini-2.5-flash"}


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
    # Four models now share the top reasoning rating (very_high):
    # claude-opus-5, claude-sonnet-5, gemini-2.5-pro, gpt-5. The quality
    # scale is intentionally coarse (SCHEMA.md), so ties are expected,
    # not a bug -- the Evaluator breaks them deterministically by
    # dataset load order (alphabetical by id, see loader.py), and
    # "claude-opus-5" sorts first among the tied models.
    context = Context(
        use_case="Complex agentic workflow",
        budget=BudgetLevel.HIGH,
        priorities=(Priority.REASONING,),
        language="es",
    )

    candidates = evaluate(context, models)

    assert candidates[0].model.id == "claude-opus-5"


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


def test_gpt_4o_is_dominated_by_a_newer_cheaper_model(models):
    # PoC for "legacy models, no schema change": gpt-4o was added
    # specifically to test whether the engine can surface "this is
    # outdated, consider migrating" from real data alone, with no
    # `legacy` field anywhere in SCHEMA.md. It can: gpt-5-mini costs
    # less than a fifth of gpt-4o's blended price while matching or
    # beating it on every quality dimension this schema tracks. No
    # special-casing was needed to make that comparison possible -- it
    # falls out of rating gpt-4o honestly against today's landscape
    # (see Docs/models/gpt-4o.md for the reasoning behind each rating).
    gpt_4o = next(m for m in models if m.id == "gpt-4o")
    gpt_5_mini = next(m for m in models if m.id == "gpt-5-mini")

    assert gpt_5_mini.cost.blended < gpt_4o.cost.blended
    assert gpt_5_mini.quality.reasoning.ordinal >= gpt_4o.quality.reasoning.ordinal
    assert gpt_5_mini.quality.coding.ordinal >= gpt_4o.quality.coding.ordinal
    assert gpt_5_mini.quality.creative_writing.ordinal >= gpt_4o.quality.creative_writing.ordinal
    assert gpt_5_mini.quality.instruction_following.ordinal >= gpt_4o.quality.instruction_following.ordinal
