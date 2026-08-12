"""Reads dataset/access_routes/*/*.yaml and dataset/subscriptions/*/*.yaml.

Mirrors decision/loader/loader.py's discipline (structural validation at
load time, DatasetValidationError on any issue) but stays a separate
module -- per ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 5.3, this is not an
extension of the model loader.

Cross-catalog referential integrity (does a route's model_id exist in
dataset/models/? does a consumer_subscription value exist in
subscriptions/?) is deliberately NOT checked here per-file -- it's a
separate, explicit step (validate_route_references) run once after both
catalogs are loaded, so decision/access/advisor.py never has to worry
about whether the ids it's handed are real.
"""

from pathlib import Path

import yaml

from decision.domain.access_route import (
    Access,
    AccessRequirement,
    AccessRoute,
    BillingScheme,
    Capability,
    Economics,
    Eligibility,
    Evidence,
    EvidenceStatus,
    QuotaScope,
    RegionScope,
    RequirementKind,
    Surface,
)
from decision.domain.ai_model import AIModel
from decision.domain.subscription import SubscriptionPlan
from decision.loader.errors import DatasetValidationError

REQUIRED_ROUTE_FIELDS = ("provider", "model_id", "access", "eligibility", "economics", "evidence")
REQUIRED_ACCESS_FIELDS = ("surface", "access_method", "capabilities", "guide_ref")
REQUIRED_ELIGIBILITY_FIELDS = ("requirements", "region_scope")
REQUIRED_ECONOMICS_FIELDS = ("billing_owner", "billing_scheme", "quota_scope", "production_allowed")
REQUIRED_EVIDENCE_FIELDS = ("source_url", "consulted_at", "status", "caveat")

REQUIRED_SUBSCRIPTION_FIELDS = (
    "provider",
    "plan_name",
    "surface_entitlements",
    "documented_exclusions",
    "region_scope",
    "source_url",
    "consulted_at",
    "status",
)

# Which kinds carry a value, and what shape it must be.
_KIND_VALUE_SHAPE = {
    RequirementKind.API_BILLING_LINKED: None,
    RequirementKind.CLOUD_ACCOUNT: "single_string",
    RequirementKind.CONSUMER_SUBSCRIPTION: "string_list",
    RequirementKind.PROGRAM_MEMBERSHIP: "single_string",
    RequirementKind.GPU_INFRASTRUCTURE: None,
}


def load_access_routes(directory: Path) -> list[AccessRoute]:
    """Loads and validates every access route YAML file under `directory`.

    Expects the dataset/access_routes/{provider}/{route_id}.yaml layout.
    """
    return [load_access_route_file(path) for path in sorted(Path(directory).glob("*/*.yaml"))]


def load_access_route_file(path: Path) -> AccessRoute:
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    issues = _validate_route(raw)
    if issues:
        raise DatasetValidationError(path, issues)

    return _to_access_route(raw, route_id=path.stem)


def load_subscriptions(directory: Path) -> list[SubscriptionPlan]:
    """Loads and validates every subscription plan YAML file under `directory`.

    Expects the dataset/subscriptions/{provider}/{plan_id}.yaml layout.
    """
    return [load_subscription_file(path) for path in sorted(Path(directory).glob("*/*.yaml"))]


def load_subscription_file(path: Path) -> SubscriptionPlan:
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    issues = _validate_subscription(raw)
    if issues:
        raise DatasetValidationError(path, issues)

    return _to_subscription_plan(raw, plan_id=path.stem)


def validate_route_references(routes: list[AccessRoute], models: list[AIModel]) -> None:
    """Cross-catalog check: every route.model_id must be a real dataset/models/ id.

    Separate from load_access_routes on purpose -- see module docstring.
    """
    known_ids = {model.id for model in models}
    issues_by_route = {
        route.route_id: f"model_id '{route.model_id}' does not exist in dataset/models/"
        for route in routes
        if route.model_id not in known_ids
    }
    if issues_by_route:
        raise DatasetValidationError(
            "access_routes", [f"{route_id}: {issue}" for route_id, issue in issues_by_route.items()]
        )


def validate_subscription_references(
    routes: list[AccessRoute], subscriptions: list[SubscriptionPlan]
) -> None:
    """Cross-catalog check: every consumer_subscription value must be a real plan_id."""
    known_plan_ids = {plan.plan_id for plan in subscriptions}
    issues = []
    for route in routes:
        for requirement in route.eligibility.requirements:
            if requirement.kind != RequirementKind.CONSUMER_SUBSCRIPTION:
                continue
            for plan_id in requirement.value:
                if plan_id not in known_plan_ids:
                    issues.append(
                        f"{route.route_id}: consumer_subscription references unknown plan_id '{plan_id}'"
                    )
    if issues:
        raise DatasetValidationError("access_routes", issues)


def _validate_route(raw) -> list[str]:
    if not isinstance(raw, dict):
        return ["file does not contain a YAML mapping"]

    issues = [f"missing required field '{field}'" for field in REQUIRED_ROUTE_FIELDS if field not in raw]
    if issues:
        return issues

    access, eligibility, economics, evidence = (
        raw["access"],
        raw["eligibility"],
        raw["economics"],
        raw["evidence"],
    )

    issues += [f"missing access.{f}" for f in REQUIRED_ACCESS_FIELDS if f not in access]
    issues += [f"missing eligibility.{f}" for f in REQUIRED_ELIGIBILITY_FIELDS if f not in eligibility]
    issues += [f"missing economics.{f}" for f in REQUIRED_ECONOMICS_FIELDS if f not in economics]
    issues += [f"missing evidence.{f}" for f in REQUIRED_EVIDENCE_FIELDS if f not in evidence]
    if issues:
        return issues

    if access["surface"] not in _values(Surface):
        issues.append(f"invalid access.surface='{access['surface']}'")
    for capability in access["capabilities"]:
        if capability not in _values(Capability):
            issues.append(f"invalid access.capabilities entry '{capability}'")

    issues += _validate_requirements(eligibility["requirements"])
    if eligibility["region_scope"] not in _values(RegionScope):
        issues.append(f"invalid eligibility.region_scope='{eligibility['region_scope']}'")

    if economics["billing_scheme"] not in _values(BillingScheme):
        issues.append(f"invalid economics.billing_scheme='{economics['billing_scheme']}'")
    if economics["quota_scope"] not in _values(QuotaScope):
        issues.append(f"invalid economics.quota_scope='{economics['quota_scope']}'")
    production_allowed = economics["production_allowed"]
    if not (isinstance(production_allowed, bool) or production_allowed == "not_determined"):
        issues.append("economics.production_allowed must be a boolean or 'not_determined'")

    if evidence["status"] not in _values(EvidenceStatus):
        issues.append(f"invalid evidence.status='{evidence['status']}'")

    return issues


def _validate_requirements(requirements) -> list[str]:
    if not isinstance(requirements, list):
        return ["eligibility.requirements must be a list"]

    issues = []
    for entry in requirements:
        if not isinstance(entry, dict) or "kind" not in entry:
            issues.append(f"invalid requirement entry: {entry}")
            continue
        kind = entry["kind"]
        if kind not in _values(RequirementKind):
            issues.append(f"invalid requirement kind '{kind}'")
            continue

        shape = _KIND_VALUE_SHAPE[RequirementKind(kind)]
        value = entry.get("value")
        if shape is None and value is not None:
            issues.append(f"requirement kind '{kind}' must not have a value")
        elif shape == "single_string" and not isinstance(value, str):
            issues.append(f"requirement kind '{kind}' requires a string value")
        elif shape == "string_list" and not (
            isinstance(value, list) and value and all(isinstance(v, str) for v in value)
        ):
            issues.append(f"requirement kind '{kind}' requires a non-empty list of strings")

    return issues


def _validate_subscription(raw) -> list[str]:
    if not isinstance(raw, dict):
        return ["file does not contain a YAML mapping"]

    issues = [
        f"missing required field '{field}'" for field in REQUIRED_SUBSCRIPTION_FIELDS if field not in raw
    ]
    if issues:
        return issues

    for surface in raw["surface_entitlements"]:
        if surface not in _values(Surface):
            issues.append(f"invalid surface_entitlements entry '{surface}'")
    if raw["status"] not in _values(EvidenceStatus):
        issues.append(f"invalid status='{raw['status']}'")

    return issues


def _values(enum_cls):
    return {member.value for member in enum_cls}


def _to_access_route(raw: dict, route_id: str) -> AccessRoute:
    access, eligibility, economics, evidence = (
        raw["access"],
        raw["eligibility"],
        raw["economics"],
        raw["evidence"],
    )
    production_allowed = economics["production_allowed"]

    return AccessRoute(
        route_id=route_id,
        provider=raw["provider"],
        model_id=raw["model_id"],
        access=Access(
            surface=Surface(access["surface"]),
            access_method=access["access_method"],
            capabilities=tuple(Capability(c) for c in access["capabilities"]),
            guide_ref=access["guide_ref"],
        ),
        eligibility=Eligibility(
            requirements=tuple(
                AccessRequirement(
                    kind=RequirementKind(entry["kind"]),
                    value=(
                        tuple(entry["value"])
                        if RequirementKind(entry["kind"]) == RequirementKind.CONSUMER_SUBSCRIPTION
                        else entry.get("value")
                    ),
                )
                for entry in eligibility["requirements"]
            ),
            region_scope=RegionScope(eligibility["region_scope"]),
        ),
        economics=Economics(
            billing_owner=economics["billing_owner"],
            billing_scheme=BillingScheme(economics["billing_scheme"]),
            quota_scope=QuotaScope(economics["quota_scope"]),
            production_allowed=None if production_allowed == "not_determined" else production_allowed,
        ),
        evidence=Evidence(
            source_url=evidence["source_url"],
            consulted_at=str(evidence["consulted_at"]),
            status=EvidenceStatus(evidence["status"]),
            caveat=evidence["caveat"],
        ),
    )


def _to_subscription_plan(raw: dict, plan_id: str) -> SubscriptionPlan:
    return SubscriptionPlan(
        plan_id=plan_id,
        provider=raw["provider"],
        plan_name=raw["plan_name"],
        surface_entitlements=tuple(Surface(s) for s in raw["surface_entitlements"]),
        documented_exclusions=tuple(raw["documented_exclusions"]),
        region_scope=raw["region_scope"],
        source_url=raw["source_url"],
        consulted_at=str(raw["consulted_at"]),
        status=EvidenceStatus(raw["status"]),
    )
