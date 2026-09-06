"""Alternatives' standout reasons, excluded models, and the outranked group."""

from decision.domain import BudgetLevel, BudgetMode, Context, Priority
from decision.evaluator import evaluate
from decision.explainer import explain


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
    # Only mistral-large-3 supports "ko" -- none of the other 29 models
    # list it either, since every curated language list in this dataset
    # was inherited from a same-provider sibling, none of which support
    # "ko" (see Docs/models/*.md), including deepseek-v4-pro (inherits
    # deepseek-v4-flash's curated language list), the six candidates
    # admitted 2026-08-10 (each inherits its nearest same-provider
    # sibling's curated list), gemini-3.7-flash (admitted 2026-08-13,
    # inherits gemini-3.6-flash's curated list), claude-fable-5-1
    # (admitted 2026-09-01, inherits claude-fable-5's curated list),
    # gemini-3.8-flash (admitted 2026-09-02, inherits gemini-3.7-flash's
    # curated list), and gpt-6-astra (admitted 2026-09-04, inherits
    # gpt-5-6-sol's curated list).
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
        "gemini-3.8-flash",
        "gpt-6-astra",
    }
    assert all(
        any("language" in reason for reason in excl.reasons)
        for excl in recommendation.excluded
    )


def test_total_qualifying_and_alternative_ranks(models):
    # 29 models total, all support "es", budget=HIGH is a fixed <=$30
    # cost tier (SCHEMA.md's Cost section) -- it excludes claude-fable-5
    # and claude-fable-5-1 ($60 blended each), so 27 qualify. gpt-5-6-sol
    # used to be excluded too at its stale $35 blended price; the
    # 2026-08-27 catalog refresh corrected it to OpenAI's live
    # promotional price ($24 blended, see Docs/CHANGELOG.md), which now
    # qualifies. Alternatives are the winner's (gpt-5-nano's) immediate
    # runners-up (rank starts at 2, since the winner is implicitly rank
    # 1); neither gpt-5-6-sol's $24 blended cost nor gemini-3.8-flash's
    # $4.50 blended cost is cheap enough to displace any of the top-3
    # alternatives here.
    context = Context(
        use_case="High-volume low-cost bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )
    candidates = evaluate(context, models)

    recommendation = explain(context, candidates)

    assert recommendation.total_qualifying == 27
    assert [alt.rank for alt in recommendation.alternatives] == [2, 3, 4]


def test_outranked_models_get_ranked_and_include_priority_dimensions(models):
    # Same context as above (27 qualifying, see
    # test_total_qualifying_and_alternative_ranks). The top-3
    # alternatives (gemini-2.5-flash-lite, gemini-3.1-flash-lite,
    # deepseek-v4-flash) leave mistral-large-3 ($2.00 blended) as the
    # first model past them, into the outranked group (rank 5 of 27).
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

    assert len(recommendation.outranked) == 23  # 27 - winner - 3 alternatives
    assert [o.rank for o in recommendation.outranked] == list(range(5, 28))

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
