"""Evaluates AIModel candidates against a Context.

Where the actual decision-making logic lives, per ARCHITECTURE.md:
receives a Context and a set of AIModel objects, and produces a list
of Candidate objects — one per input model, disqualified or not, so
the Explainer can later account for alternatives and exclusions, not
only the winner.

Two things this module deliberately never does, per ARCHITECTURE.md's
non-negotiable principles: it never branches on a model's id, name, or
provider, and it never reads a stored cost_tier — cost_tier is derived
here, from each model's raw pricing, relative to the other models it's
being evaluated against (SCHEMA.md: "cost_tier is not stored... it's a
derived value").
"""

from decision.domain.ai_model import AIModel, CostTier, QualityLevel
from decision.domain.candidate import Candidate
from decision.domain.context import BudgetLevel, Context, Priority

_MAX_QUALITY_ORDINAL = QualityLevel.VERY_HIGH.ordinal

_BUDGET_CEILING = {
    BudgetLevel.LOW: CostTier.LOW,
    BudgetLevel.MEDIUM: CostTier.MEDIUM,
    BudgetLevel.HIGH: CostTier.HIGH,
}


def evaluate(context: Context, models: list[AIModel]) -> list[Candidate]:
    """Evaluates every model in `models` against `context`.

    Returns one Candidate per model, best-qualifying-candidate first,
    disqualified candidates last. Every model is represented, so the
    caller can explain both the winner and why any given alternative
    didn't make it.
    """
    if not context.priorities:
        raise ValueError("Context.priorities must not be empty")
    if not models:
        return []

    cost_tiers = _derive_cost_tiers(models)
    qualifying, disqualified = _split_by_hard_filters(context, models, cost_tiers)

    candidates = [_score(context, model, qualifying, cost_tiers) for model in qualifying]
    candidates += [
        Candidate(model=model, score=0.0, cost_tier=cost_tiers[model.id], disqualified_reasons=reasons)
        for model, reasons in disqualified
    ]

    return sorted(candidates, key=lambda candidate: (not candidate.qualifies, -candidate.score))


def _derive_cost_tiers(models: list[AIModel]) -> dict[str, CostTier]:
    ranked_by_cost = sorted(models, key=lambda model: model.cost.blended)
    total = len(ranked_by_cost)
    return {
        model.id: CostTier(min(rank * 3 // total, CostTier.HIGH))
        for rank, model in enumerate(ranked_by_cost)
    }


def _split_by_hard_filters(context: Context, models: list[AIModel], cost_tiers: dict[str, CostTier]):
    budget_ceiling = _BUDGET_CEILING[context.budget]
    qualifying = []
    disqualified = []

    for model in models:
        reasons = []
        if context.language not in model.languages:
            reasons.append(f"does not support language '{context.language}'")
        if cost_tiers[model.id] > budget_ceiling:
            reasons.append(f"cost tier exceeds a '{context.budget.value}' budget")

        if reasons:
            disqualified.append((model, tuple(reasons)))
        else:
            qualifying.append(model)

    return qualifying, disqualified


def _score(context: Context, model: AIModel, qualifying: list[AIModel], cost_tiers: dict[str, CostTier]) -> Candidate:
    weights = {
        priority: len(context.priorities) - index
        for index, priority in enumerate(context.priorities)
    }
    total_weight = sum(weights.values())

    factor_scores = {
        priority: _normalized_factor(priority, model, qualifying)
        for priority in context.priorities
    }
    score = sum(weights[p] * factor_scores[p] for p in context.priorities) / total_weight

    return Candidate(model=model, score=score, cost_tier=cost_tiers[model.id], factor_scores=factor_scores)


def _normalized_factor(priority: Priority, model: AIModel, qualifying: list[AIModel]) -> float:
    if priority == Priority.COST:
        return _normalize_relative(
            value=model.cost.blended,
            values=[m.cost.blended for m in qualifying],
            lower_is_better=True,
        )
    if priority == Priority.CONTEXT_WINDOW:
        return _normalize_relative(
            value=model.operational.context_window,
            values=[m.operational.context_window for m in qualifying],
            lower_is_better=False,
        )

    # Quality dimensions use SCHEMA.md's fixed low/medium/high/very_high
    # scale directly, rather than normalizing relative to the candidate
    # set — "high reasoning" means the same thing regardless of who
    # else happens to qualify.
    quality_by_priority = {
        Priority.REASONING: model.quality.reasoning,
        Priority.CODING: model.quality.coding,
        Priority.CREATIVE_WRITING: model.quality.creative_writing,
        Priority.INSTRUCTION_FOLLOWING: model.quality.instruction_following,
    }
    return quality_by_priority[priority].ordinal / _MAX_QUALITY_ORDINAL


def _normalize_relative(value: float, values: list[float], lower_is_better: bool) -> float:
    low, high = min(values), max(values)
    if low == high:
        return 1.0

    normalized = (value - low) / (high - low)
    return 1.0 - normalized if lower_is_better else normalized
