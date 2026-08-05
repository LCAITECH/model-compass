"""Context: the developer's input, per FEATURES.md's "Understand" capabilities."""

from dataclasses import dataclass
from enum import Enum


class BudgetLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


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


@dataclass(frozen=True)
class Context:
    use_case: str
    budget: BudgetLevel
    priorities: tuple[Priority, ...]
    language: str
