"""Reads dataset/models/*.yaml and produces AIModel domain objects.

Validates each entry against the rules in SCHEMA.md's "Validation
Rules" section. Validation lives here, as part of turning a YAML file
into a domain object, rather than as a separate component — the
simplest option for the set of rules this dataset currently has. This
resolves the open question noted in ARCHITECTURE.md ("Dataset
validation ... To be resolved when loader/ is implemented").
"""

from datetime import date
from pathlib import Path

import yaml

from decision.domain.ai_model import (
    Access,
    AIModel,
    Capabilities,
    Cost,
    CostReversion,
    Ecosystem,
    IntegrationEase,
    License,
    Lifecycle,
    LifecycleStatus,
    Maturity,
    Operational,
    Quality,
    QualityLevel,
)
from decision.loader._util import enum_values
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
    "access",
    "lifecycle",
)

REQUIRED_LIFECYCLE_FIELDS = ("status", "release_date", "shutdown_date", "replacement")

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
    """Loads and validates every model YAML file in `directory`.

    One check spans files: a `lifecycle.replacement` must name a model
    that is itself in the dataset, so a successor shown to the user is
    always one the engine can actually recommend or compare.
    """
    paths = sorted(Path(directory).glob("*.yaml"))
    models = [load_model_file(path) for path in paths]
    ids = {model.id for model in models}
    for path, model in zip(paths, models):
        replacement = model.lifecycle.replacement
        if replacement is not None and replacement not in ids:
            raise DatasetValidationError(
                path, [f"lifecycle.replacement '{replacement}' is not a model in the dataset"]
            )
    return models


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

    if raw["license"] not in enum_values(License):
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
        elif quality[field] not in enum_values(QualityLevel):
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
        if level not in enum_values(QualityLevel):
            issues.append(f"invalid language_quality.{lang}='{level}'")

    operational = raw["operational"]
    if not _is_positive_int(operational.get("context_window")):
        issues.append("operational.context_window must be a positive integer")
    if "max_output" not in operational:
        issues.append("operational.max_output must be present (null if the provider publishes none)")
    elif operational["max_output"] is not None and not _is_positive_int(operational["max_output"]):
        issues.append("operational.max_output must be a positive integer or null")

    cost = raw["cost"]
    if not _is_non_negative_number(cost.get("input_per_million")):
        issues.append("cost.input_per_million must be a non-negative number")
    if not _is_non_negative_number(cost.get("output_per_million")):
        issues.append("cost.output_per_million must be a non-negative number")

    has_effective_until = "effective_until" in cost
    has_reverts_to = "reverts_to" in cost
    if has_effective_until != has_reverts_to:
        issues.append("cost.effective_until and cost.reverts_to must both be present or both absent")
    elif has_effective_until:
        if not _is_iso_date(cost["effective_until"]):
            issues.append("cost.effective_until must be an ISO date string (YYYY-MM-DD)")
        reverts_to = cost["reverts_to"]
        if not isinstance(reverts_to, dict) or not _is_non_negative_number(
            reverts_to.get("input_per_million")
        ):
            issues.append("cost.reverts_to.input_per_million must be a non-negative number")
        if not isinstance(reverts_to, dict) or not _is_non_negative_number(
            reverts_to.get("output_per_million")
        ):
            issues.append("cost.reverts_to.output_per_million must be a non-negative number")

    ecosystem = raw["ecosystem"]
    if ecosystem.get("integration_ease") not in enum_values(IntegrationEase):
        issues.append(f"invalid ecosystem.integration_ease='{ecosystem.get('integration_ease')}'")
    if ecosystem.get("maturity") not in enum_values(Maturity):
        issues.append(f"invalid ecosystem.maturity='{ecosystem.get('maturity')}'")

    access = raw["access"]
    if not isinstance(access.get("has_free_access"), bool):
        issues.append("access.has_free_access must be a boolean")

    issues.extend(_lifecycle_issues(raw["lifecycle"], raw["id"]))
    return issues


def _lifecycle_issues(lifecycle, model_id) -> list[str]:
    # Every key is required, null included -- same rule as
    # operational.max_output: "no date published" has to be written down,
    # not left out, so a missing key can't pass for a checked one.
    if not isinstance(lifecycle, dict):
        return ["lifecycle must be a mapping"]
    issues = [
        f"lifecycle.{field} must be present (null if the provider publishes none)"
        for field in REQUIRED_LIFECYCLE_FIELDS
        if field not in lifecycle
    ]
    if issues:
        return issues

    if lifecycle["status"] not in enum_values(LifecycleStatus):
        issues.append(f"invalid lifecycle.status='{lifecycle['status']}'")
    dates_valid = True
    for field in ("release_date", "shutdown_date"):
        value = lifecycle[field]
        if value is not None and not _is_iso_date(value):
            issues.append(f"lifecycle.{field} must be an ISO date string (YYYY-MM-DD) or null")
            dates_valid = False
    release_date, shutdown_date = lifecycle["release_date"], lifecycle["shutdown_date"]
    if dates_valid and release_date and shutdown_date and release_date >= shutdown_date:
        issues.append("lifecycle.release_date must be before lifecycle.shutdown_date")
    replacement = lifecycle["replacement"]
    if replacement is not None and (not isinstance(replacement, str) or not replacement):
        issues.append("lifecycle.replacement must be a model id or null")
    elif replacement == model_id:
        issues.append("lifecycle.replacement cannot be the model itself")
    return issues


def _is_positive_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _is_non_negative_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def _is_iso_date(value) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def _to_ai_model(raw: dict) -> AIModel:
    quality = raw["quality"]
    ecosystem = raw["ecosystem"]
    cost = raw["cost"]
    reverts_to = cost.get("reverts_to")

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
        cost=Cost(
            input_per_million=cost["input_per_million"],
            output_per_million=cost["output_per_million"],
            effective_until=cost.get("effective_until"),
            reverts_to=CostReversion(**reverts_to) if reverts_to else None,
        ),
        ecosystem=Ecosystem(
            integration_ease=IntegrationEase(ecosystem["integration_ease"]),
            maturity=Maturity(ecosystem["maturity"]),
        ),
        access=Access(**raw["access"]),
        lifecycle=Lifecycle(
            status=LifecycleStatus(raw["lifecycle"]["status"]),
            shutdown_date=raw["lifecycle"]["shutdown_date"],
            replacement=raw["lifecycle"]["replacement"],
            release_date=raw["lifecycle"]["release_date"],
        ),
    )
