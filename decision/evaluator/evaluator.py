"""Evaluates AIModel candidates against a Context.

Where the actual decision-making logic lives, per ARCHITECTURE.md:
receives a Context and a set of AIModel objects, and produces a list
of Candidate objects — one per input model, disqualified or not, so
the Explainer can later account for alternatives and exclusions, not
only the winner.

Two things this module deliberately never does, per ARCHITECTURE.md's
non-negotiable principles: it never branches on a model's id, name, or
provider, and it never reads a stored cost_tier — cost_tier is derived
here, from each model's raw pricing, against fixed $/million-token
bands (SCHEMA.md: "cost_tier is not stored... it's a derived value").
The bands are fixed rather than relative to the loaded dataset, so a
model's tier doesn't drift just because other models were added to or
removed from the catalog.
"""

from decision.domain.ai_model import AIModel, CostTier, QualityLevel
from decision.domain.candidate import Candidate
from decision.domain.context import BudgetLevel, BudgetMode, Context, Priority

_MAX_QUALITY_ORDINAL = QualityLevel.VERY_HIGH.ordinal

_BUDGET_CEILING = {
    BudgetLevel.LOW: CostTier.LOW,
    BudgetLevel.MEDIUM: CostTier.MEDIUM,
    BudgetLevel.HIGH: CostTier.HIGH,
    BudgetLevel.VERY_HIGH: CostTier.VERY_HIGH,
}

# Fixed $/million-token ceilings for Cost.blended (input + output per
# million tokens), checked in order. Anything above the last ceiling
# falls into CostTier.VERY_HIGH. Chosen against the real distribution
# of the dataset's Cost.blended values, not arbitrary round numbers —
# see Docs/HANDOFF.md, "Rediseño de Budget", for the data behind them.
_COST_TIER_CEILINGS: list[tuple[float, CostTier]] = [
    (2.0, CostTier.LOW),
    (10.0, CostTier.MEDIUM),
    (30.0, CostTier.HIGH),
]

# How much a budget tier dampens Cost's positional weight in the
# ranking, when Cost isn't the user's #1 priority. A looser budget
# tier means the user signaled cost matters less to them, so it should
# influence the ranking less -- unless they explicitly ranked it #1,
# which is never dampened (see _dampen_cost_weight). Deliberately
# keyed to price-per-token bands, never to the user's stated monthly
# budget in dollars -- that would require assuming a token volume the
# user never provided, which this project has already rejected once
# (see interfaces/web/affordability.py's docstring).
_COST_DAMPENING = {
    BudgetLevel.LOW: 1.0,
    BudgetLevel.MEDIUM: 0.66,
    BudgetLevel.HIGH: 0.33,
    BudgetLevel.VERY_HIGH: 0.10,
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
    if context.budget_mode == BudgetMode.TIER and context.budget is None:
        raise ValueError("Context.budget must be set when budget_mode is TIER")
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
    return {model.id: _cost_tier_for(model.cost.blended) for model in models}


def _cost_tier_for(blended: float) -> CostTier:
    for ceiling, tier in _COST_TIER_CEILINGS:
        if blended <= ceiling:
            return tier
    return CostTier.VERY_HIGH


def _split_by_hard_filters(context: Context, models: list[AIModel], cost_tiers: dict[str, CostTier]):
    # Custom Budget never filters -- see BudgetMode's docstring. A
    # ceiling of None below means "every cost tier qualifies", not "use
    # the highest tier's ceiling", since even VERY_HIGH is still a real
    # filter (it excludes nothing today, but would exclude a future,
    # even-pricier model).
    budget_ceiling = _BUDGET_CEILING[context.budget] if context.budget_mode == BudgetMode.TIER else None
    qualifying = []
    disqualified = []

    for model in models:
        reasons = []
        if context.language not in model.languages:
            reasons.append(f"does not support language '{context.language}'")
        if budget_ceiling is not None and cost_tiers[model.id] > budget_ceiling:
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
    weights = _dampen_cost_weight(context, weights)
    total_weight = sum(weights.values())

    factor_scores = {
        priority: _normalized_factor(priority, model, qualifying)
        for priority in context.priorities
    }
    score = sum(weights[p] * factor_scores[p] for p in context.priorities) / total_weight

    return Candidate(model=model, score=score, cost_tier=cost_tiers[model.id], factor_scores=factor_scores)


def _dampen_cost_weight(context: Context, weights: dict[Priority, float]) -> dict[Priority, float]:
    """Scales down Cost's positional weight per the budget tier's dampening factor.

    Never touches any priority the user didn't rank, never touches Cost
    if the user ranked it #1 -- an explicit top priority is never
    second-guessed by an implicit signal (their choice of budget) --
    and never touches it under Custom Budget either: dampening is
    defined over price-per-token bands, and Custom Budget is a
    dollar-per-month figure with no such band (see BudgetMode's
    docstring).
    """
    if Priority.COST not in weights or context.priorities[0] == Priority.COST:
        return weights
    if context.budget_mode == BudgetMode.CUSTOM:
        return weights

    dampened = dict(weights)
    dampened[Priority.COST] *= _COST_DAMPENING[context.budget]
    return dampened


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
