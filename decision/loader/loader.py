"""Reads dataset/models/*.yaml and produces AIModel domain objects.

Validates each entry against the rules in SCHEMA.md's "Validation
Rules" section. Validation lives here, as part of turning a YAML file
into a domain object, rather than as a separate component — the
simplest option for the set of rules this dataset currently has. This
resolves the open question noted in ARCHITECTURE.md ("Dataset
validation ... To be resolved when loader/ is implemented").
"""

from pathlib import Path

import yaml

from decision.domain.ai_model import (
    AIModel,
    Capabilities,
    Cost,
    Ecosystem,
    IntegrationEase,
    License,
    Maturity,
    Operational,
    Quality,
    QualityLevel,
)
from decision.loader.errors import DatasetValidationError

REQUIRED_TOP_LEVEL_FIELDS = (
    "id",
    "name",
    "provider",
    "version",
    "license",
    "capabilities",
    "quality",
    "languages",
    "language_quality",
    "operational",
    "cost",
    "ecosystem",
)

REQUIRED_CAPABILITIES = (
    "vision",
    "audio",
    "image_generation",
    "tool_calling",
    "structured_output",
    "json_mode",
)

REQUIRED_QUALITY_DIMENSIONS = (
    "reasoning",
    "coding",
    "creative_writing",
    "instruction_following",
)


def load_dataset(directory: Path) -> list[AIModel]:
    """Loads and validates every model YAML file in `directory`."""
    return [load_model_file(path) for path in sorted(Path(directory).glob("*.yaml"))]


def load_model_file(path: Path) -> AIModel:
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    issues = _validate(raw, path)
    if issues:
        raise DatasetValidationError(path, issues)

    return _to_ai_model(raw)


def _validate(raw, path: Path) -> list[str]:
    if not isinstance(raw, dict):
        return ["file does not contain a YAML mapping"]

    issues = [
        f"missing required field '{field}'"
        for field in REQUIRED_TOP_LEVEL_FIELDS
        if field not in raw
    ]
    if issues:
        # Every other check assumes the top-level fields exist.
        return issues

    if raw["id"] != path.stem:
        issues.append(f"id '{raw['id']}' does not match filename '{path.stem}'")

    if raw["license"] not in _values(License):
        issues.append(f"invalid license '{raw['license']}'")

    capabilities = raw["capabilities"]
    for field in REQUIRED_CAPABILITIES:
        if field not in capabilities:
            issues.append(f"missing capabilities.{field}")
        elif not isinstance(capabilities[field], bool):
            issues.append(f"capabilities.{field} must be a boolean")

    quality = raw["quality"]
    for field in REQUIRED_QUALITY_DIMENSIONS:
        if field not in quality:
            issues.append(f"missing quality.{field}")
        elif quality[field] not in _values(QualityLevel):
            issues.append(f"invalid quality.{field}='{quality[field]}'")

    languages = set(raw["languages"])
    language_quality = raw["language_quality"]
    lq_keys = set(language_quality.keys())
    if languages != lq_keys:
        missing = languages - lq_keys
        extra = lq_keys - languages
        if missing:
            issues.append(f"language_quality missing entries for: {sorted(missing)}")
        if extra:
            issues.append(f"language_quality has entries not in languages: {sorted(extra)}")
    for lang, level in language_quality.items():
        if level not in _values(QualityLevel):
            issues.append(f"invalid language_quality.{lang}='{level}'")

    operational = raw["operational"]
    if not _is_positive_int(operational.get("context_window")):
        issues.append("operational.context_window must be a positive integer")
    if not _is_positive_int(operational.get("max_output")):
        issues.append("operational.max_output must be a positive integer")

    cost = raw["cost"]
    if not _is_non_negative_number(cost.get("input_per_million")):
        issues.append("cost.input_per_million must be a non-negative number")
    if not _is_non_negative_number(cost.get("output_per_million")):
        issues.append("cost.output_per_million must be a non-negative number")

    ecosystem = raw["ecosystem"]
    if ecosystem.get("integration_ease") not in _values(IntegrationEase):
        issues.append(f"invalid ecosystem.integration_ease='{ecosystem.get('integration_ease')}'")
    if ecosystem.get("maturity") not in _values(Maturity):
        issues.append(f"invalid ecosystem.maturity='{ecosystem.get('maturity')}'")

    return issues


def _values(enum_cls):
    return {member.value for member in enum_cls}


def _is_positive_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _is_non_negative_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def _to_ai_model(raw: dict) -> AIModel:
    quality = raw["quality"]
    ecosystem = raw["ecosystem"]

    return AIModel(
        id=raw["id"],
        name=raw["name"],
        provider=raw["provider"],
        version=str(raw["version"]),
        license=License(raw["license"]),
        capabilities=Capabilities(**raw["capabilities"]),
        quality=Quality(
            reasoning=QualityLevel(quality["reasoning"]),
            coding=QualityLevel(quality["coding"]),
            creative_writing=QualityLevel(quality["creative_writing"]),
            instruction_following=QualityLevel(quality["instruction_following"]),
        ),
        languages=tuple(raw["languages"]),
        language_quality={
            lang: QualityLevel(level) for lang, level in raw["language_quality"].items()
        },
        operational=Operational(**raw["operational"]),
        cost=Cost(**raw["cost"]),
        ecosystem=Ecosystem(
            integration_ease=IntegrationEase(ecosystem["integration_ease"]),
            maturity=Maturity(ecosystem["maturity"]),
        ),
    )
