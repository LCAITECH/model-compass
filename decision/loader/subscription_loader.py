"""Reads dataset/subscriptions/*/*.yaml into SubscriptionPlans.

Split out of access_loader.py (routes and plans are two catalogs with
two schemas; SCHEMA.md, "Subscription plans"). Same discipline as the
other loaders: structural validation at load time, DatasetValidationError
on any issue.

`price`, `usage_multiplier` and `api_credits` are required keys; the last
two may be null (the provider publishes no multiplier, or the plan
includes no API credits), the same "required key, null allowed" rule as
a model's lifecycle block. A multiplier's `relative_to` must name another
plan in the catalog, checked once all plans are loaded.
"""

from pathlib import Path

import yaml

from decision.domain.access_route import AccessRoute, EvidenceStatus, RequirementKind, Surface
from decision.domain.subscription import ApiCredits, PlanPrice, SubscriptionPlan, UsageMultiplier
from decision.loader._util import enum_values
from decision.loader.errors import DatasetValidationError

REQUIRED_SUBSCRIPTION_FIELDS = (
    "provider",
    "plan_name",
    "surface_entitlements",
    "documented_exclusions",
    "region_scope",
    "source_url",
    "consulted_at",
    "status",
    "price",
    "usage_multiplier",
    "api_credits",
)


def load_subscriptions(directory: Path) -> list[SubscriptionPlan]:
    """Loads and validates every subscription plan YAML file under `directory`.

    Expects the dataset/subscriptions/{provider}/{plan_id}.yaml layout.
    """
    plans = [load_subscription_file(path) for path in sorted(Path(directory).glob("*/*.yaml"))]
    known = {plan.plan_id for plan in plans}
    issues = [
        f"{plan.plan_id}: usage_multiplier.relative_to references unknown plan_id '{plan.usage_multiplier.relative_to}'"
        for plan in plans
        if plan.usage_multiplier and plan.usage_multiplier.relative_to not in known
    ]
    if issues:
        raise DatasetValidationError("subscriptions", issues)
    return plans


def load_subscription_file(path: Path) -> SubscriptionPlan:
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    issues = _validate_subscription(raw, plan_id=path.stem)
    if issues:
        raise DatasetValidationError(path, issues)

    return _to_subscription_plan(raw, plan_id=path.stem)


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


def _positive_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _text(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_subscription(raw, plan_id: str) -> list[str]:
    if not isinstance(raw, dict):
        return ["file does not contain a YAML mapping"]

    issues = [
        f"missing required field '{field}'" for field in REQUIRED_SUBSCRIPTION_FIELDS if field not in raw
    ]
    if issues:
        return issues

    if not isinstance(raw["surface_entitlements"], list):
        issues.append("surface_entitlements must be a list")
    else:
        for surface in raw["surface_entitlements"]:
            if surface not in enum_values(Surface):
                issues.append(f"invalid surface_entitlements entry '{surface}'")
    if not (
        isinstance(raw["documented_exclusions"], list)
        and all(isinstance(item, str) for item in raw["documented_exclusions"])
    ):
        issues.append("documented_exclusions must be a list of strings")
    if raw["status"] not in enum_values(EvidenceStatus):
        issues.append(f"invalid status='{raw['status']}'")

    price = raw["price"]
    if not (isinstance(price, dict) and _positive_number(price.get("monthly_usd"))):
        issues.append("price.monthly_usd must be a number greater than 0")

    multiplier = raw["usage_multiplier"]
    if multiplier is not None:
        if not isinstance(multiplier, dict):
            issues.append("usage_multiplier must be a mapping or null")
        else:
            if not _text(multiplier.get("relative_to")):
                issues.append("usage_multiplier.relative_to must be a plan_id")
            elif multiplier["relative_to"] == plan_id:
                issues.append("usage_multiplier.relative_to cannot be the plan itself")
            if not _positive_number(multiplier.get("factor")):
                issues.append("usage_multiplier.factor must be a number greater than 0")
            if not _text(multiplier.get("scope")):
                issues.append("usage_multiplier.scope must be a non-empty string")

    credits = raw["api_credits"]
    if credits is not None:
        if not isinstance(credits, dict):
            issues.append("api_credits must be a mapping or null")
        else:
            if not _positive_number(credits.get("monthly_usd")):
                issues.append("api_credits.monthly_usd must be a number greater than 0")
            if credits.get("surface") not in enum_values(Surface):
                issues.append(f"invalid api_credits.surface='{credits.get('surface')}'")
            if not _text(credits.get("conditions")):
                issues.append("api_credits.conditions must be a non-empty string")

    return issues


def _to_subscription_plan(raw: dict, plan_id: str) -> SubscriptionPlan:
    multiplier, credits = raw["usage_multiplier"], raw["api_credits"]
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
        price=PlanPrice(monthly_usd=float(raw["price"]["monthly_usd"])),
        usage_multiplier=UsageMultiplier(
            relative_to=multiplier["relative_to"],
            factor=float(multiplier["factor"]),
            scope=multiplier["scope"],
        )
        if multiplier
        else None,
        api_credits=ApiCredits(
            monthly_usd=float(credits["monthly_usd"]),
            surface=Surface(credits["surface"]),
            conditions=credits["conditions"],
        )
        if credits
        else None,
    )
