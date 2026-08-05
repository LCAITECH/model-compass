"""Recommendation: the final, explainable result of a decision.

Presentation-agnostic on purpose — see ARCHITECTURE.md: the Explainer
that builds this object "has no knowledge of how it will later be
displayed."
"""

from dataclasses import dataclass

from decision.domain.ai_model import AIModel


@dataclass(frozen=True)
class Exclusion:
    model: AIModel
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Recommendation:
    recommended: AIModel
    reasons: tuple[str, ...]
    trade_offs: tuple[str, ...]
    alternatives: tuple[AIModel, ...]
    excluded: tuple[Exclusion, ...]
