from pathlib import Path

import pytest

from decision.domain import (
    Access,
    AIModel,
    BudgetLevel,
    BudgetMode,
    Candidate,
    Capabilities,
    Context,
    Cost,
    CostTier,
    Ecosystem,
    IntegrationEase,
    License,
    Maturity,
    Operational,
    Priority,
    Quality,
    QualityLevel,
)
from decision.evaluator import evaluate
from decision.explainer import NoQualifyingModelsError, explain
from decision.explainer.explainer import _also_strong_options
from decision.loader import load_dataset

DATASET_DIR = Path(__file__).resolve().parents[1] / "dataset" / "models"


@pytest.fixture(scope="module")
def models():
    return load_dataset(DATASET_DIR)


def _model(id: str, quality_level: QualityLevel) -> AIModel:
    """A minimal AIModel with all four quality dimensions at the same level."""
    return AIModel(
        id=id,
        name=id,
        provider="Test",
        version="1",
        license=License.PROPRIETARY,
        capabilities=Capabilities(False, False, False, False, False, False),
        quality=Quality(quality_level, quality_level, quality_level, quality_level),
        languages=("en",),
        language_quality={"en": quality_level},
        operational=Operational(context_window=1000, max_output=1000),
        cost=Cost(input_per_million=1.0, output_per_million=1.0),
        ecosystem=Ecosystem(IntegrationEase.LOW, Maturity.STABLE),
        access=Access(has_free_access=False),
    )


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
    assert any("es" in reason and "quality" in reason for reason in recommendation.reasons)
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


def test_alternatives_are_capped(models):
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert len(recommendation.alternatives) == 3
    assert recommendation.recommended.id not in {alt.model.id for alt in recommendation.alternatives}


def test_also_strong_options_is_not_capped_at_max_alternatives(models):
    # budget=high, priority=reasoning: 9 models are within 2% of
    # claude-opus-4-7's score AND pass the quality floor -- more than
    # the 3-item cap on `alternatives`. Confirms also_strong_options
    # isn't silently truncated to that cap. gpt-5-6-sol joined this set
    # in the 2026-08-27 catalog refresh: its stale $5.00/$30.00 price
    # ($35 blended, CostTier.VERY_HIGH, excluded under a "high" budget)
    # was corrected to OpenAI's live promotional price $4.00/$20.00
    # ($24 blended, CostTier.HIGH) -- see Docs/CHANGELOG.md -- which now
    # qualifies and scores close enough to also count as also-strong.
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.REASONING,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert recommendation.recommended.id == "claude-opus-4-7"
    assert len(recommendation.alternatives) == 3
    assert len(recommendation.also_strong_options) == 9
    assert {a.model.id for a in recommendation.also_strong_options} == {
        "claude-opus-4-8",
        "claude-opus-5",
        "claude-sonnet-5",
        "deepseek-v4-pro",
        "gemini-2.5-pro",
        "gemini-3.1-pro-preview",
        "gemini-3.7-flash",
        "gpt-5",
        "gpt-5-6-sol",
    }
    assert [a.rank for a in recommendation.also_strong_options] == list(range(2, 11))  # score-sorted, contiguous


def test_also_strong_options_excludes_close_score_but_unfair_quality_gap(models):
    # priority_1=context_window: gpt-5-6-sol and gemini-2.5-flash-lite
    # land within 0.15% of each other in score (context_window
    # dominates the weighting), but are very_high/very_high/high/very_high
    # vs. medium/medium/low/medium -- an 8-tier cumulative quality gap.
    # This is the concrete case that motivated the quality floor: score
    # closeness alone would call this "practically tied"; it isn't.
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.VERY_HIGH,
        priorities=(Priority.CONTEXT_WINDOW,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert recommendation.recommended.id == "gpt-5-6-sol"
    assert "gemini-2.5-flash-lite" not in {a.model.id for a in recommendation.also_strong_options}


def test_also_strong_options_includes_a_close_score_similar_quality_model(models):
    # priority_1=cost: gpt-5-nano now wins (its stale-but-still-cheapest
    # deepseek-v4-flash rival was corrected to a $1.76 blended price in
    # the 2026-08-27 catalog refresh -- see Docs/CHANGELOG.md -- pushing
    # it well outside the 2% score-closeness window). gpt-5-nano is
    # itself the weakest quality profile in the qualifying pool
    # (low/low/low/medium), so the only model close enough in
    # cost-driven score to even reach the quality-floor check is
    # gemini-2.5-flash-lite (medium/medium/low/medium) -- one tier up on
    # three dimensions, tied on the fourth, so it passes the floor and
    # qualifies. The exclusion side of this mechanism (close score, but
    # more than one tier down on quality) is covered separately by
    # test_also_strong_options_excludes_close_score_but_unfair_quality_gap.
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.MEDIUM,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    also_strong_ids = {a.model.id for a in recommendation.also_strong_options}
    assert recommendation.recommended.id == "gpt-5-nano"
    assert "gemini-2.5-flash-lite" in also_strong_ids


def test_also_strong_options_is_empty_when_the_runner_up_fails_both_conditions():
    # Direct unit test of _also_strong_options with synthetic models --
    # more reliable than hunting the real 26-model dataset for an empty
    # case, and pins down the exact boundary behavior. The runner-up
    # here is both >2% behind on score AND >1 tier down on every
    # quality dimension, so it must fail on the score check before the
    # quality floor is even consulted.
    winner_model = _model("winner", QualityLevel.VERY_HIGH)
    loser_model = _model("loser", QualityLevel.LOW)
    winner = Candidate(model=winner_model, score=1.0, cost_tier=CostTier.LOW)
    loser = Candidate(model=loser_model, score=0.5, cost_tier=CostTier.LOW)

    result = _also_strong_options(winner, [loser], [winner_model, loser_model])

    assert result == ()


def test_also_strong_options_score_gap_boundary_is_inclusive():
    # Exactly 2% below the winner's score, same quality profile --
    # should still qualify (the docstring says "within 2%", i.e. <=,
    # not a strict <).
    winner_model = _model("winner", QualityLevel.HIGH)
    at_boundary_model = _model("at-boundary", QualityLevel.HIGH)
    just_over_model = _model("just-over", QualityLevel.HIGH)
    winner = Candidate(model=winner_model, score=1.0, cost_tier=CostTier.LOW)
    at_boundary = Candidate(model=at_boundary_model, score=0.98, cost_tier=CostTier.LOW)  # exactly 2% gap
    just_over = Candidate(model=just_over_model, score=0.9799, cost_tier=CostTier.LOW)  # just past 2%

    result = _also_strong_options(winner, [at_boundary, just_over], [winner_model, at_boundary_model, just_over_model])

    assert {a.model.id for a in result} == {"at-boundary"}


def test_alternatives_get_honest_standout_reasons_or_none(models):
    # Winner is gpt-5-nano ($0.45 blended, cheapest in the dataset since
    # the 2026-08-27 catalog refresh corrected deepseek-v4-flash's stale
    # price -- see Docs/CHANGELOG.md -- which also pushed deepseek-v4-flash
    # itself down into the alternatives, and pushed the previous
    # deepseek-v4-pro/gpt-5-nano standouts out of this budget=MEDIUM
    # context entirely). Alternatives ranked by cost among the rest:
    # gemini-2.5-flash-lite (0.50), gemini-3.1-flash-lite (1.75),
    # deepseek-v4-flash (1.76) -- all three genuinely stand out on a
    # dimension the winner doesn't: the two Flash-Lite models tie for
    # the largest context window in this qualifying pool, and
    # deepseek-v4-flash is the only one rated above `low` on creative
    # writing.
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.MEDIUM,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)
    by_id = {alt.model.id: alt for alt in recommendation.alternatives}

    assert any("context window" in reason for reason in by_id["gemini-2.5-flash-lite"].reasons)
    assert any("context window" in reason for reason in by_id["gemini-3.1-flash-lite"].reasons)
    assert any("creative writing" in reason for reason in by_id["deepseek-v4-flash"].reasons)


def test_excluded_models_carry_their_disqualification_reasons(models):
    # Only mistral-large-3 supports "ko" -- none of the other 27 models
    # list it either, since every curated language list in this dataset
    # was inherited from a same-provider sibling, none of which support
    # "ko" (see Docs/models/*.md), including deepseek-v4-pro (inherits
    # deepseek-v4-flash's curated language list), the six candidates
    # admitted 2026-08-10 (each inherits its nearest same-provider
    # sibling's curated list), gemini-3.7-flash (admitted 2026-08-13,
    # inherits gemini-3.6-flash's curated list), and claude-fable-5-1
    # (admitted 2026-09-01, inherits claude-fable-5's curated list).
    context = Context(
        use_case="Korean support assistant",
        budget_mode=BudgetMode.TIER,
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
        "gemini-2.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash",
        "gpt-5-mini",
        "gpt-5-6-sol",
        "claude-sonnet-5",
        "claude-sonnet-4-5",
        "deepseek-v4-flash",
        "deepseek-v4-pro",
        "gpt-5",
        "gemini-2.5-pro",
        "claude-opus-5",
        "claude-opus-4-5",
        "gpt-4o",
        "gpt-5-nano",
        "claude-haiku-4-5",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite",
        "claude-opus-4-8",
        "claude-opus-4-7",
        "claude-opus-4-6",
        "claude-sonnet-4-6",
        "claude-fable-5",
        "claude-fable-5-1",
        "gemini-3.1-pro-preview",
        "gemini-3.7-flash",
    }
    assert all(
        any("language" in reason for reason in excl.reasons)
        for excl in recommendation.excluded
    )


def test_total_qualifying_and_alternative_ranks(models):
    # 27 models total, all support "es", budget=HIGH is a fixed <=$30
    # cost tier (SCHEMA.md's Cost section) -- it excludes claude-fable-5
    # ($60 blended), so 26 qualify. gpt-5-6-sol used to be excluded too
    # at its stale $35 blended price; the 2026-08-27 catalog refresh
    # corrected it to OpenAI's live promotional price ($24 blended, see
    # Docs/CHANGELOG.md), which now qualifies -- one more than the
    # previous 25. Alternatives are the winner's (gpt-5-nano's) immediate
    # runners-up (rank starts at 2, since the winner is implicitly rank
    # 1); gpt-5-6-sol's $24 blended cost isn't cheap enough to displace
    # any of the top-3 alternatives here.
    context = Context(
        use_case="High-volume low-cost bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert recommendation.total_qualifying == 26
    assert [alt.rank for alt in recommendation.alternatives] == [2, 3, 4]


def test_outranked_models_get_ranked_and_include_priority_dimensions(models):
    # Same context as above (26 qualifying, see
    # test_total_qualifying_and_alternative_ranks). The top-3
    # alternatives (gemini-2.5-flash-lite, gemini-3.1-flash-lite,
    # deepseek-v4-flash) leave mistral-large-3 ($2.00 blended) as the
    # first model past them, into the outranked group (rank 5 of 26).
    # Unlike the winner's trade_offs, its reasons include "Not the
    # cheapest option" even though COST is the prioritized dimension,
    # because there's no positive "reasons" line for it to contradict;
    # omitting the cost gap would hide the actual reason it lost, per
    # _dimension_gaps' docstring.
    context = Context(
        use_case="High-volume low-cost bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert len(recommendation.outranked) == 22  # 26 - winner - 3 alternatives
    assert [o.rank for o in recommendation.outranked] == list(range(5, 27))

    first = recommendation.outranked[0]
    assert first.model.id == "mistral-large-3"
    assert any("Not the cheapest" in reason for reason in first.reasons)


def test_outranked_reasons_put_the_users_actual_priority_first(models):
    # With priority=CODING instead of COST, claude-haiku-4-5 (which has
    # a real coding gap, unlike most outranked models under this
    # priority) should show "Not the strongest coding" first, not
    # buried where cost would normally sort in the canonical dimension
    # order (cost, then quality dimensions, then context window).
    context = Context(
        use_case="x",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.CODING,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)
    by_id = {o.model.id: o for o in recommendation.outranked}

    assert by_id["claude-haiku-4-5"].reasons[0] == "Not the strongest coding among the qualifying alternatives"


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
