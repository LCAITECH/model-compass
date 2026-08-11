"""AIModel: a model as read from the dataset, per SCHEMA.md."""

from dataclasses import dataclass
from enum import Enum, IntEnum


class QualityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

    @property
    def ordinal(self) -> int:
        return list(QualityLevel).index(self)


class License(str, Enum):
    PROPRIETARY = "proprietary"
    OPEN_WEIGHTS = "open-weights"
    OPEN_SOURCE = "open-source"


class IntegrationEase(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Maturity(str, Enum):
    EXPERIMENTAL = "experimental"
    STABLE = "stable"
    MATURE = "mature"


class CostTier(IntEnum):
    """Which fixed price band a model's blended cost falls into.

    Derived, not stored in the dataset — see SCHEMA.md's Cost section.
    The type lives here as shared vocabulary; the actual derivation
    (fixed $/million-token bands, anchored to Cost.blended, the same
    for every evaluation regardless of which models are being compared)
    stays in decision/evaluator/, the only place that computes it.
    """

    LOW = 0
    MEDIUM = 1
    HIGH = 2
    VERY_HIGH = 3


@dataclass(frozen=True)
class Capabilities:
    vision: bool
    audio: bool
    image_generation: bool
    tool_calling: bool
    structured_output: bool
    json_mode: bool


@dataclass(frozen=True)
class Quality:
    reasoning: QualityLevel
    coding: QualityLevel
    creative_writing: QualityLevel
    instruction_following: QualityLevel


@dataclass(frozen=True)
class Operational:
    context_window: int
    max_output: int


@dataclass(frozen=True)
class Cost:
    input_per_million: float
    output_per_million: float

    @property
    def blended(self) -> float:
        """Cost of an equal mix of input and output tokens.

        An intermediate derived figure, not stored in the dataset (see
        SCHEMA.md's Cost section) — used to rank and tier models by
        price without picking one of input/output alone.
        """
        return self.input_per_million + self.output_per_million


@dataclass(frozen=True)
class Ecosystem:
    integration_ease: IntegrationEase
    maturity: Maturity


@dataclass(frozen=True)
class Access:
    """Whether a documented, official free-access path exists today.

    Deliberately just this one boolean — see SCHEMA.md's Access section
    for the strict definition. Rate limits and other unstable detail
    stay out of the schema entirely and live in docs/models/*.md prose.
    """

    has_free_access: bool


@dataclass(frozen=True)
class AIModel:
    id: str
    name: str
    provider: str
    version: str
    license: License
    capabilities: Capabilities
    quality: Quality
    languages: tuple[str, ...]
    language_quality: dict[str, QualityLevel]
    operational: Operational
    cost: Cost
    ecosystem: Ecosystem
    access: Access
