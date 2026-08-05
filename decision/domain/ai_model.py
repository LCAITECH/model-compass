"""AIModel: a model as read from the dataset, per SCHEMA.md."""

from dataclasses import dataclass
from enum import Enum


class QualityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


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
