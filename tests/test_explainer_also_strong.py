"""The MAX_ALTERNATIVES cap and the also_strong_options tie-detection rules."""

from decision.domain import BudgetLevel, BudgetMode, Candidate, Context, CostTier, Priority, QualityLevel
from decision.evaluator import evaluate
from decision.explainer import explain
from decision.explainer.explainer import _also_strong_options


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
    # budget=high, priority=reasoning: 10 models are within 2% of
    # claude-opus-4-7's score AND pass the quality floor -- more than
    # the 3-item cap on `alternatives`. Confirms also_strong_options
    # isn't silently truncated to that cap. gpt-5-6-sol joined this set
    # in the 2026-08-27 catalog refresh: its stale $5.00/$30.00 price
    # ($35 blended, CostTier.VERY_HIGH, excluded under a "high" budget)
    # was corrected to OpenAI's live promotional price $4.00/$20.00
    # ($24 blended, CostTier.HIGH) -- see Docs/CHANGELOG.md -- which now
    # qualifies and scores close enough to also count as also-strong.
    # gemini-3.8-flash joined the same way at its 2026-09-02 admission,
    # rated very_high on reasoning like gemini-3.7-flash before it.
    # qwen3.8-max joined the same way at its 2026-09-08 admission, also
    # rated very_high on reasoning.
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
    assert len(recommendation.also_strong_options) == 11
    assert {a.model.id for a in recommendation.also_strong_options} == {
        "claude-opus-4-8",
        "claude-opus-5",
        "claude-sonnet-5",
        "deepseek-v4-pro",
        "gemini-2.5-pro",
        "gemini-3.1-pro-preview",
        "gemini-3.7-flash",
        "gemini-3.8-flash",
        "gpt-5",
        "gpt-5-6-sol",
        "qwen3.8-max",
    }
    assert [a.rank for a in recommendation.also_strong_options] == list(range(2, 13))  # score-sorted, contiguous


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


def test_also_strong_options_is_empty_when_the_runner_up_fails_both_conditions(make_model):
    # Direct unit test of _also_strong_options with synthetic models --
    # more reliable than hunting the real 26-model dataset for an empty
    # case, and pins down the exact boundary behavior. The runner-up
    # here is both >2% behind on score AND >1 tier down on every
    # quality dimension, so it must fail on the score check before the
    # quality floor is even consulted.
    winner_model = make_model("winner", quality=QualityLevel.VERY_HIGH)
    loser_model = make_model("loser", quality=QualityLevel.LOW)
    winner = Candidate(model=winner_model, score=1.0, cost_tier=CostTier.LOW)
    loser = Candidate(model=loser_model, score=0.5, cost_tier=CostTier.LOW)

    result = _also_strong_options(winner, [loser], [winner_model, loser_model])

    assert result == ()


def test_also_strong_options_score_gap_boundary_is_inclusive(make_model):
    # Exactly 2% below the winner's score, same quality profile --
    # should still qualify (the docstring says "within 2%", i.e. <=,
    # not a strict <).
    winner_model = make_model("winner", quality=QualityLevel.HIGH)
    at_boundary_model = make_model("at-boundary", quality=QualityLevel.HIGH)
    just_over_model = make_model("just-over", quality=QualityLevel.HIGH)
    winner = Candidate(model=winner_model, score=1.0, cost_tier=CostTier.LOW)
    at_boundary = Candidate(model=at_boundary_model, score=0.98, cost_tier=CostTier.LOW)  # exactly 2% gap
    just_over = Candidate(model=just_over_model, score=0.9799, cost_tier=CostTier.LOW)  # just past 2%

    result = _also_strong_options(winner, [at_boundary, just_over], [winner_model, at_boundary_model, just_over_model])

    assert {a.model.id for a in result} == {"at-boundary"}
