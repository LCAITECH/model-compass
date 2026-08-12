"""recommend_access: answers "how can I access this model", never "which
model should I use" -- that question belongs to decision/evaluator/ and
decision/explainer/, which this module never imports from. See
ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 5.0/5.3 for the import boundary
and Part 5.2.1 for the three-state eligibility model this implements.

KNOWN SPEC GAP, deliberately not resolved here (see AGENTS.md: raise it,
don't invent a workaround): the spec repeatedly says enterprise routes
"are shown only if the user explicitly asks to see them," but no
AccessContext field for that opt-in was ever closed. Until that's
decided, every route with Capability.ENTERPRISE_GOVERNANCE is
unconditionally treated as NOT_AVAILABLE (excluded) -- the one behavior
the spec unambiguously supports today.

DEVIATION FROM THE SPEC'S LITERAL SIGNATURE, documented rather than
silent: Part 5.3 closed `recommend_access(model, context, routes,
subscriptions)`. In practice `subscriptions` (the SubscriptionPlan
catalog) has no legitimate use inside this function -- consumer_
subscription eligibility only needs `context.subscriptions` (what the
user declared) against `requirement.value` (the plan_ids already
denormalized onto the route by the loader); resolving those plan_ids to
human-readable names is presentation, which belongs in interfaces/, not
here (see interfaces/web/access_labels.py); and re-validating that a
plan_id is real would duplicate validate_subscription_references(),
contradicting 5.3's explicit rule that the advisor stays "dumb" and
never re-checks what the loader already guaranteed. Keeping an
always-unused parameter is worse than a small, justified signature
correction -- so it was dropped. Flagged here instead of buried in a
commit message.
"""

from decision.domain.access_context import AccessContext
from decision.domain.access_recommendation import (
    AccessRecommendation,
    AccessSummary,
    RouteEligibilityState,
    RouteEntry,
)
from decision.domain.access_route import (
    AccessRequirement,
    AccessRoute,
    Capability,
    EvidenceStatus,
    RequirementKind,
    Surface,
)
from decision.domain.ai_model import AIModel


def recommend_access(
    model: AIModel,
    context: AccessContext,
    routes: list[AccessRoute],
) -> AccessRecommendation:
    model_routes = [route for route in routes if route.model_id == model.id]

    entries = []
    for route in model_routes:
        if Capability.ENTERPRISE_GOVERNANCE in route.access.capabilities:
            continue  # NOT_AVAILABLE -- never reaches a RouteEntry, see 5.2.1

        unmet = tuple(
            requirement
            for requirement in route.eligibility.requirements
            if not _is_satisfied(requirement, context)
        )
        state = (
            RouteEligibilityState.REQUIRES_ONBOARDING
            if unmet
            else RouteEligibilityState.CURRENTLY_ELIGIBLE
        )
        entries.append(RouteEntry(route=route, state=state, unmet_requirements=unmet))

    entries.sort(key=lambda entry: (entry.state != RouteEligibilityState.CURRENTLY_ELIGIBLE, entry.route.route_id))

    return AccessRecommendation(
        model=model,
        routes=tuple(entries),
        summary=_build_summary(entries),
    )


def _is_satisfied(requirement: AccessRequirement, context: AccessContext) -> bool:
    """None ("unknown") never counts as satisfied -- see spec Part 5.2.1's
    closed rule: an unconfirmable requirement leaves the route in
    REQUIRES_ONBOARDING, same as an explicit "I don't have this."
    """
    if requirement.kind == RequirementKind.API_BILLING_LINKED:
        return context.has_api_billing is True
    if requirement.kind == RequirementKind.CLOUD_ACCOUNT:
        return requirement.value in context.cloud_accounts
    if requirement.kind == RequirementKind.CONSUMER_SUBSCRIPTION:
        return any(plan_id in context.subscriptions for plan_id in requirement.value)
    if requirement.kind == RequirementKind.PROGRAM_MEMBERSHIP:
        return requirement.value in context.program_memberships
    if requirement.kind == RequirementKind.GPU_INFRASTRUCTURE:
        return context.has_gpu_infrastructure is True
    raise AssertionError(f"unhandled RequirementKind: {requirement.kind}")  # pragma: no cover


def _build_summary(entries: list[RouteEntry]) -> AccessSummary:
    for state in (RouteEligibilityState.CURRENTLY_ELIGIBLE, RouteEligibilityState.REQUIRES_ONBOARDING):
        bucket = [entry for entry in entries if entry.state == state]
        if not bucket:
            continue

        direct_api_confirmed = [
            entry.route
            for entry in bucket
            if entry.route.access.surface == Surface.DIRECT_API
            and entry.route.evidence.status == EvidenceStatus.CONFIRMED
        ]
        highlighted = direct_api_confirmed[0] if len(direct_api_confirmed) == 1 else None

        return AccessSummary(highlighted_route=highlighted, bucket_state=state, bucket_size=len(bucket))

    return AccessSummary(highlighted_route=None, bucket_state=None, bucket_size=0)
