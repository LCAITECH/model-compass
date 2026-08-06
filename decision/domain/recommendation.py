"""Recommendation: the final, explainable result of a decision.

Presentation-agnostic on purpose — see ARCHITECTURE.md: the Explainer
that builds this object "has no knowledge of how it will later be
displayed."
"""

from dataclasses import dataclass

from decision.domain.ai_model import AIModel, CostTier


@dataclass(frozen=True)
class Exclusion:
    model: AIModel
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Alternative:
    """A qualifying model other than the winner.

    `reasons` explains why you'd pick this one instead — dimensions it's
    the best qualifying option for. Empty when it isn't the strongest at
    anything relative to the rest of the qualifying set; that's an
    honest outcome, not a gap to paper over with an invented reason.
    """

    model: AIModel
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Recommendation:
    recommended: AIModel
    cost_tier: CostTier
    reasons: tuple[str, ...]
    trade_offs: tuple[str, ...]
    alternatives: tuple[Alternative, ...]
    excluded: tuple[Exclusion, ...]
