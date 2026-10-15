import pytest

from decision.domain import BudgetLevel, BudgetMode, Context, LifecycleStatus, Priority
from decision.evaluator import evaluate


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
    # Only mistral-large-3 and the Qwen entries (qwen3.8-max, admitted
    # 2026-09-08; qwen3.8-flash and qwen3.7-plus, 2026-10-15, same curated
    # Qwen list) have "ko" among their supported languages.
    context = Context(
        use_case="Korean support assistant",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="ko",
    )

    candidates = evaluate(context, models)
    qualifying = [c for c in candidates if c.qualifies]

    assert {c.model.id for c in qualifying} == {"mistral-large-3", "qwen3.8-max", "qwen3.8-flash", "qwen3.7-plus"}
    other = by_id(candidates, "gemini-2.5-flash")
    assert not other.qualifies
    assert any("language" in reason for reason in other.disqualified_reasons)


def test_low_budget_only_admits_the_cheapest_cost_tier(models):
    # CostTier is a fixed $/million-token band on cost.blended
    # (input+output per million), not a rank relative to the loaded
    # dataset -- see SCHEMA.md's Cost section for the exact bands.
    # "low" is blended <= $2. Blended cost ascending among low-tier:
    # gpt-5-nano 0.45, gemini-2.5-flash-lite 0.50, gpt-6-luna 0.60,
    # claude-haiku-5-5 0.60 (<=100k-token tier, admitted 2026-10-08),
    # gpt-5-6-luna 1.40, gemini-3.1-flash-lite 1.75, deepseek-v4-flash
    # 1.50, mistral-large-3 2.00 -- all <= $2. gpt-5-mini is next at
    # 2.25, just over the $2 ceiling. gpt-5-nano is in the band but
    # deprecated (shuts down 2026-12-11), so it never qualifies.
    # deepseek-v4-pro moved out of this tier in the 2026-08-27 catalog
    # refresh: its stale $0.435/$0.87 ($1.305 blended) was corrected to
    # the official peak rate $1.32/$3.96 ($5.28 blended), landing it in
    # "medium" instead -- see Docs/CHANGELOG.md, 2026-08-27.
    # gemini-2.5-flash-lite ($0.50) is in the band too, but restricted
    # since 2026-10-15 (Google limits it to developers who already used
    # it), so it never qualifies either. qwen3.8-flash (0.62) and
    # qwen3.7-plus (2.00, <=256k-token tier) joined the band on 2026-10-15.
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
        "gpt-6-luna",
        "claude-haiku-5-5",
        "gpt-5-6-luna",
        "gemini-3.1-flash-lite",
        "deepseek-v4-flash",
        "mistral-large-3",
        "qwen3.8-flash",
        "qwen3.7-plus",
    }


def test_high_budget_excludes_the_very_high_cost_tier(models):
    # "high" is a hard ceiling at CostTier.HIGH (blended <= $30) -- the
    # fourth tier, "very_high" (> $30), exists precisely so that "high"
    # budget stops meaning "no cost filter at all". claude-fable-5,
    # claude-fable-5-1, and gpt-6-astra ($60 blended each) are priced
    # above $30 today -- 5.1 was admitted 2026-09-01 at the same
    # headline price as 5, and gpt-6-astra (2026-09-04) landed at the
    # same $10/$50 blended cost independently. gpt-5-6-sol used to be
    # excluded too at its stale $5.00/$30.00 ($35 blended), but the
    # 2026-08-27 catalog refresh corrected it to OpenAI's live
    # promotional price $4.00/$20.00 ($24 blended, in effect at least
    # through 2026-11-21) -- see Docs/CHANGELOG.md, 2026-08-27 -- which
    # now qualifies under this $30 ceiling. Deprecated and restricted
    # models are disqualified too, for that reason alone, never for cost.
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.HIGH,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)
    over_budget = {c.model.id for c in candidates if not c.qualifies and c.model.lifecycle.status == LifecycleStatus.ACTIVE}

    assert over_budget == {"claude-fable-5", "claude-fable-5-1", "gpt-6-astra"}


def test_very_high_budget_admits_every_language_qualifying_model(models):
    context = Context(
        use_case="Bot",
        budget_mode=BudgetMode.TIER,
        budget=BudgetLevel.VERY_HIGH,
        priorities=(Priority.COST,),
        language="es",
    )

    candidates = evaluate(context, models)

    assert all(c.qualifies for c in candidates if c.model.lifecycle.status == LifecycleStatus.ACTIVE)


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

    assert all(c.qualifies for c in candidates if c.model.lifecycle.status == LifecycleStatus.ACTIVE)


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
