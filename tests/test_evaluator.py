from pathlib import Path

import pytest

from decision.domain import BudgetLevel, BudgetMode, Context, Priority
from decision.evaluator import evaluate
from decision.evaluator.evaluator import _dampen_cost_weight
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
        budget_mode=BudgetMode.TIER,
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
        budget_mode=BudgetMode.TIER,
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
    # CostTier is a fixed $/million-token band on cost.blended
    # (input+output per million), not a rank relative to the loaded
    # dataset -- see SCHEMA.md's Cost section for the exact bands.
    # "low" is blended <= $2. Of all 26 models, blended cost ascending:
    # deepseek-v4-flash 0.42, gpt-5-nano 0.45, gemini-2.5-flash-lite
    # 0.50, deepseek-v4-pro 1.305, gemini-3.1-flash-lite 1.75,
    # mistral-large-3 2.00 (corrected 2026-08-11 -- see
    # Docs/models/mistral-large-3.md, was a stale $2.00/$6.00 = $8.00
    # blended, actual model card gives $0.50/$1.50) -- all <= $2, so
    # all six qualify. gpt-5-mini is next at 2.25, just over the $2
    # ceiling, so it lands in "medium" and doesn't qualify here.
    context = Context(
        use_case="High-volume low-cost bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.LOW,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)
    qualifying = {c.model.id for c in candidates if c.qualifies}

    assert qualifying == {
        "deepseek-v4-flash",
        "gpt-5-nano",
        "gemini-2.5-flash-lite",
        "deepseek-v4-pro",
        "gemini-3.1-flash-lite",
        "mistral-large-3",
    }


def test_high_budget_excludes_the_very_high_cost_tier(models):
    # "high" is a hard ceiling at CostTier.HIGH (blended <= $30) -- the
    # fourth tier, "very_high" (> $30), exists precisely so that "high"
    # budget stops meaning "no cost filter at all". Only gpt-5-6-sol
    # ($35) and claude-fable-5 ($60) are priced above $30 today.
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)
    disqualified_ids = {c.model.id for c in candidates if not c.qualifies}

    assert disqualified_ids == {"gpt-5-6-sol", "claude-fable-5"}


def test_very_high_budget_admits_every_language_qualifying_model(models):
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.VERY_HIGH,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)

    assert all(c.qualifies for c in candidates)


def test_custom_budget_never_filters_by_cost(models):
    # Custom Budget's whole point (see BudgetMode's docstring, HANDOFF.md
    # "Rediseño de Budget"): it never filters, not even at the level
    # VERY_HIGH would. claude-fable-5 ($60 blended, the priciest model in
    # the dataset) qualifies here even though no BudgetLevel tier would
    # ever be loose enough to let a costlier-than-VERY_HIGH model through.
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.CUSTOM,
        budget=None,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)

    assert all(c.qualifies for c in candidates)


def test_cost_weight_dampens_by_budget_tier_unless_cost_is_first():
    # A direct test of the weighting math itself (_dampen_cost_weight),
    # rather than round-tripping through evaluate() -- going through
    # evaluate() would confound the dampening effect with the fact that
    # a looser budget also changes *which models qualify*, which shifts
    # Cost's own relative-normalization domain. Isolating the pure
    # weight function is the only way to check the dampening curve
    # itself without that second effect mixed in.
    weights = {Priority.REASONING: 2, Priority.COST: 1}

    for budget, expected_factor in (
        (BudgetLevel.LOW, 1.0),
        (BudgetLevel.MEDIUM, 0.66),
        (BudgetLevel.HIGH, 0.33),
        (BudgetLevel.VERY_HIGH, 0.10),
    ):
        context = Context(
            use_case="Bot",
            budget_mode=BudgetMode.TIER,
            budget=budget,
            priorities=(Priority.REASONING, Priority.COST),
            language="es",
        )
        dampened = _dampen_cost_weight(context, weights)

        assert dampened[Priority.COST] == pytest.approx(1 * expected_factor)
        assert dampened[Priority.REASONING] == 2  # never touched


def test_cost_weight_is_never_dampened_when_cost_is_the_top_priority():
    weights = {Priority.COST: 2, Priority.REASONING: 1}

    for budget in (BudgetLevel.LOW, BudgetLevel.MEDIUM, BudgetLevel.HIGH, BudgetLevel.VERY_HIGH):
        context = Context(
            use_case="Bot",
            budget_mode=BudgetMode.TIER,
            budget=budget,
            priorities=(Priority.COST, Priority.REASONING),
            language="es",
        )

        assert _dampen_cost_weight(context, weights) == weights


def test_cost_weight_dampening_is_a_noop_when_cost_is_not_ranked():
    weights = {Priority.REASONING: 2, Priority.CODING: 1}
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.REASONING, Priority.CODING),
        language="es",
    )

    assert _dampen_cost_weight(context, weights) == weights


def test_cost_weight_is_never_dampened_under_custom_budget():
    # Custom Budget never dampens Cost -- dampening is defined over
    # price-per-token bands, and Custom is a $/month figure with no
    # such band (see BudgetMode's docstring). True even with Cost as
    # priority #2, where Tier mode would dampen it.
    weights = {Priority.REASONING: 2, Priority.COST: 1}
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.CUSTOM,
        budget=None,
        priorities=(Priority.REASONING, Priority.COST),
        language="es",
    )

    assert _dampen_cost_weight(context, weights) == weights


def test_deepseek_v4_pro_still_wins_on_reasoning_even_with_cost_dampened(models):
    # HANDOFF.md "Finding 1": with the tested dampening curve, this
    # extreme case (Reasoning#1, Cost#2, budget=High) still picks
    # deepseek-v4-pro -- its price gap to the competition is wide
    # enough that even a lightly-weighted Cost still tips the balance.
    # Confirmed as correct-given-the-data (see HANDOFF.md Parte C), not
    # patched around by hand-tuning the dampening numbers for this one
    # case -- this test documents and locks in that decision.
    context = Context(
        use_case="Complex agentic workflow",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.REASONING, Priority.COST),
        language="es",
    )

    candidates = evaluate(context, models)

    assert candidates[0].model.id == "deepseek-v4-pro"


def test_cost_priority_picks_the_cheapest_qualifying_model(models):
    context = Context(
        use_case="High-volume low-cost bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)

    assert candidates[0].model.id == "deepseek-v4-flash"


def test_reasoning_priority_picks_the_strongest_reasoning_model(models):
    # Seven models now share the top reasoning rating (very_high):
    # claude-fable-5, claude-opus-4-7, claude-opus-4-8, claude-opus-5,
    # claude-sonnet-5, gemini-2.5-pro, gpt-5. The quality scale is
    # intentionally coarse (SCHEMA.md), so ties are expected, not a
    # bug -- the Evaluator breaks them deterministically by dataset
    # load order (alphabetical by id, see loader.py), and
    # "claude-fable-5" sorts first among the tied models. budget=VERY_HIGH
    # (not HIGH) because claude-fable-5's $60 blended cost puts it in
    # CostTier.VERY_HIGH -- a "high" budget correctly excludes it now
    # that CostTier is a fixed price band, not a relative tercile.
    context = Context(
        use_case="Complex agentic workflow",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.VERY_HIGH,
        priorities=(Priority.REASONING,),
        language="es",
    )

    candidates = evaluate(context, models)

    assert candidates[0].model.id == "claude-fable-5"


def test_priority_order_changes_the_winner(models):
    # deepseek-v4-pro (cheap, very_high reasoning and coding) now wins
    # under budget=LOW regardless of COST/REASONING order -- it's close
    # enough to Pareto-dominant on those two dimensions that swapping
    # their priority no longer changes the winner, confirmed directly
    # against the Evaluator rather than assumed. COST vs.
    # CREATIVE_WRITING still demonstrates the thing this test actually
    # checks, since deepseek-v4-pro is only rated `medium` there:
    # budget=HIGH, cost-first still picks the cheapest model
    # (deepseek-v4-flash), creative-writing-first picks a model that
    # doesn't win on cost at all (gemini-2.5-pro).
    cost_first = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST, Priority.CREATIVE_WRITING),
        language="es",
    )
    creative_writing_first = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.CREATIVE_WRITING, Priority.COST),
        language="es",
    )

    cost_winner = evaluate(cost_first, models)[0].model.id
    creative_writing_winner = evaluate(creative_writing_first, models)[0].model.id

    assert cost_winner != creative_writing_winner


def test_disqualified_candidates_are_ranked_after_qualifying_ones(models):
    context = Context(
        use_case="Korean support assistant",
        budget_mode=BudgetMode.TIER,
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
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(),
        language="es",
    )

    with pytest.raises(ValueError):
        evaluate(context, models)


def test_tier_mode_without_a_budget_is_rejected(models):
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=None,
        priorities=(Priority.COST,),
        language="es",
    )

    with pytest.raises(ValueError):
        evaluate(context, models)


def test_no_models_returns_no_candidates():
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
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
