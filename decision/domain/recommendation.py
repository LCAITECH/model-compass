"""Recommendation: the final, explainable result of a decision.

Presentation-agnostic on purpose — see ARCHITECTURE.md: the Explainer
that builds this object "has no knowledge of how it will later be
displayed."
"""

from dataclasses import dataclass

from decision.domain.ai_model import AIModel, CostTier


@dataclass(frozen=True)
class Exclusion:
    """A model that never entered the ranking.

    Disqualified by a hard filter (unsupported language, cost tier
    over budget) before any scoring happened — it never competed, so
    it has no `rank`. Distinct from `Outranked`, which did compete.
    """

    model: AIModel
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Alternative:
    """One of the top qualifying models other than the winner.

    `rank` is this model's position among every qualifying model for
    this context (the winner is always rank 1). `reasons` explains why
    you'd pick this one instead — dimensions it's the best qualifying
    option for. Empty when it isn't the strongest at anything relative
    to the rest of the qualifying set; that's an honest outcome, not a
    gap to paper over with an invented reason.
    """

    model: AIModel
    rank: int
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Outranked:
    """A qualifying model that competed but didn't make the top alternatives.

    It was scored and ranked like every other qualifying model — it
    just didn't rank high enough to be shown as an `Alternative`.
    `reasons` lists every dimension it isn't the best qualifying option
    on, including ones the user prioritized (unlike the winner's
    `trade_offs`, there's no positive "reasons" line here to avoid
    contradicting).
    """

    model: AIModel
    rank: int
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Recommendation:
    recommended: AIModel
    cost_tier: CostTier
    reasons: tuple[str, ...]
    trade_offs: tuple[str, ...]
    total_qualifying: int
    alternatives: tuple[Alternative, ...]
    outranked: tuple[Outranked, ...]
    excluded: tuple[Exclusion, ...]
