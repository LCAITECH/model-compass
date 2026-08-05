"""AIModel: a model as read from the dataset, per SCHEMA.md."""

from dataclasses import dataclass
from enum import Enum


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
