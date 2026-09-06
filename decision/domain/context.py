"""Context: the developer's input, per FEATURES.md's "Understand" capabilities."""

from dataclasses import dataclass
from enum import Enum


class BudgetLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class BudgetMode(str, Enum):
    """Which of the two, mutually exclusive ways the developer expressed a budget.

    TIER: a fixed price-per-token band (BudgetLevel) -- a hard filter on
    qualification, and it dampens Cost's ranking weight (see
    decision/evaluator/evaluator.py).

    CUSTOM: a real dollar amount the developer has available per month.
    Never filters and never dampens Cost's weight -- doing either would
    require assuming a token volume the developer never provided (see
    interfaces/web/affordability.py's docstring). It only feeds the
    capacity calculator in interfaces/web/, which decision/ has no idea
    exists.
    """

    TIER = "tier"
    CUSTOM = "custom"


class Priority(str, Enum):
    """A factor the developer can rank as more or less important.

    Restricted to attributes that actually exist on AIModel. Latency is
    deliberately not a valid priority — SCHEMA.md excludes it as "not a
    property of the model itself".
    """

    COST = "cost"
    REASONING = "reasoning"
    CODING = "coding"
    CREATIVE_WRITING = "creative_writing"
    INSTRUCTION_FOLLOWING = "instruction_following"
    CONTEXT_WINDOW = "context_window"


# The four Priority members that map straight onto an AIModel.quality
# attribute of the same name -- COST and CONTEXT_WINDOW don't, since
# they read from Cost/Operational instead. Shared by decision/explainer/
# (phrasing a reason) and interfaces/web/affordability.py (the fair-swap
# quality-tier check), so it lives on the domain type both reference
# rather than being redefined in each.
QUALITY_DIMENSION_ATTR: dict[Priority, str] = {
    Priority.REASONING: "reasoning",
    Priority.CODING: "coding",
    Priority.CREATIVE_WRITING: "creative_writing",
    Priority.INSTRUCTION_FOLLOWING: "instruction_following",
}


@dataclass(frozen=True)
class Context:
    use_case: str
    budget_mode: BudgetMode
    budget: BudgetLevel | None
    priorities: tuple[Priority, ...]
    language: str
