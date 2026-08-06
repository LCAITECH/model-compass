"""Candidate: an AIModel evaluated against a Context."""

from dataclasses import dataclass, field

from decision.domain.ai_model import AIModel, CostTier
from decision.domain.context import Priority


@dataclass(frozen=True)
class Candidate:
    model: AIModel
    score: float
    cost_tier: CostTier
    factor_scores: dict[Priority, float] = field(default_factory=dict)
    disqualified_reasons: tuple[str, ...] = ()

    @property
    def qualifies(self) -> bool:
        return not self.disqualified_reasons
