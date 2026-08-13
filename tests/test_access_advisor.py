from pathlib import Path

from decision.access import recommend_access
from decision.domain import (
    AccessContext,
    AccessRequirement,
    AccessRoute,
    Capability,
    CloudProvider,
    Eligibility,
    Evidence,
    EvidenceStatus,
    Intensity,
    RequirementKind,
    RouteEligibilityState,
    UseMode,
    WorkloadType,
)
from decision.loader import load_access_routes, load_dataset

ROOT = Path(__file__).resolve().parents[1]
MODELS = {model.id: model for model in load_dataset(ROOT / "dataset" / "models")}
ROUTES = load_access_routes(ROOT / "dataset" / "access_routes")


def _context(**overrides):
    defaults = dict(
        use_mode=UseMode.API_INTEGRATION,
        workload_type=WorkloadType.INTERACTIVE,
        intensity=Intensity.OCCASIONAL,
        country=None,
        subscriptions=(),
        has_api_billing=None,
        cloud_accounts=(),
        program_memberships=(),
        has_gpu_infrastructure=None,
    )
    defaults.update(overrides)
    return AccessContext(**defaults)


def test_currently_eligible_when_requirement_met():
    model = MODELS["claude-opus-5"]
    recommendation = recommend_access(model, _context(has_api_billing=True), ROUTES)

    [entry] = recommendation.routes
    assert entry.state == RouteEligibilityState.CURRENTLY_ELIGIBLE
    assert entry.unmet_requirements == ()


def test_requires_onboarding_when_requirement_declared_false():
    model = MODELS["claude-opus-5"]
    recommendation = recommend_access(model, _context(has_api_billing=False), ROUTES)

    [entry] = recommendation.routes
    assert entry.state == RouteEligibilityState.REQUIRES_ONBOARDING
    assert len(entry.unmet_requirements) == 1


def test_unknown_never_counts_as_satisfied():
    """None ("unknown") must behave exactly like an explicit False -- spec Part 5.2.1."""
    model = MODELS["claude-opus-5"]
    recommendation = recommend_access(model, _context(has_api_billing=None), ROUTES)

    [entry] = recommendation.routes
    assert entry.state == RouteEligibilityState.REQUIRES_ONBOARDING


def test_consumer_subscription_matches_declared_plan():
    model = MODELS["gemini-2.5-pro"]
    recommendation = recommend_access(
        model, _context(has_api_billing=True, subscriptions=("google-ai-pro",)), ROUTES
    )

    by_surface = {entry.route.access.surface.value: entry.state for entry in recommendation.routes}
    assert by_surface["direct_api"] == RouteEligibilityState.CURRENTLY_ELIGIBLE
    assert by_surface["playground_or_studio"] == RouteEligibilityState.CURRENTLY_ELIGIBLE


def test_consumer_subscription_unmet_without_declared_plan():
    model = MODELS["gemini-2.5-pro"]
    recommendation = recommend_access(model, _context(has_api_billing=True), ROUTES)

    by_surface = {entry.route.access.surface.value: entry.state for entry in recommendation.routes}
    assert by_surface["direct_api"] == RouteEligibilityState.CURRENTLY_ELIGIBLE
    assert by_surface["playground_or_studio"] == RouteEligibilityState.REQUIRES_ONBOARDING


def test_summary_highlights_unique_confirmed_direct_api():
    model = MODELS["claude-opus-5"]
    recommendation = recommend_access(model, _context(has_api_billing=True), ROUTES)

    assert recommendation.summary.bucket_state == RouteEligibilityState.CURRENTLY_ELIGIBLE
    assert recommendation.summary.highlighted_route is not None
    assert recommendation.summary.highlighted_route.access.surface.value == "direct_api"


def test_summary_falls_back_to_requires_onboarding_bucket():
    model = MODELS["claude-opus-5"]
    recommendation = recommend_access(model, _context(has_api_billing=False), ROUTES)

    assert recommendation.summary.bucket_state == RouteEligibilityState.REQUIRES_ONBOARDING
    assert recommendation.summary.highlighted_route is not None


def test_summary_shows_neutral_count_with_two_eligible_routes_neither_uniquely_direct_api():
    model = MODELS["claude-opus-5"]
    template = next(route for route in ROUTES if route.model_id == "claude-opus-5")
    second_direct_api_route = AccessRoute(
        route_id="zz-second-direct-api",
        provider=template.provider,
        model_id=model.id,
        access=template.access.__class__(
            surface=template.access.surface,  # also direct_api -- now two compete
            access_method="second API key",
            capabilities=template.access.capabilities,
            guide_ref=template.access.guide_ref,
        ),
        eligibility=template.eligibility,
        economics=template.economics,
        evidence=template.evidence,
    )

    recommendation = recommend_access(
        model, _context(has_api_billing=True), [template, second_direct_api_route]
    )

    assert recommendation.summary.bucket_size == 2
    assert recommendation.summary.highlighted_route is None


def test_no_routes_for_a_model_returns_explicit_empty_state():
    # Every real model now has at least one route (26/26 coverage), so
    # exclude gpt-5-mini's own routes from the catalog handed to the
    # advisor -- still proves the empty-state path with real route data
    # for other models present, not just an empty list.
    model = MODELS["gpt-5-mini"]
    other_routes = [route for route in ROUTES if route.model_id != model.id]
    recommendation = recommend_access(model, _context(), other_routes)

    assert recommendation.routes == ()
    assert recommendation.summary.bucket_state is None
    assert recommendation.summary.highlighted_route is None


def test_enterprise_governance_routes_are_never_shown():
    model = MODELS["claude-opus-5"]
    enterprise_route = _make_enterprise_route(model.id)

    recommendation = recommend_access(model, _context(has_api_billing=True), [enterprise_route])

    assert recommendation.routes == ()


def test_cloud_account_requires_onboarding_without_declared_account():
    """No cloud_hosted route exists in the sample dataset yet (spec 5.1 --
    Bedrock/Vertex/Foundry were left out pending per-model_id evidence), so
    this exercises the CLOUD_ACCOUNT branch with a synthetic route --
    same pattern as _make_enterprise_route below.
    """
    model = MODELS["claude-opus-5"]
    route = _make_cloud_hosted_route(model.id, provider_value="aws")

    without_account = recommend_access(model, _context(), [route])
    [entry] = without_account.routes
    assert entry.state == RouteEligibilityState.REQUIRES_ONBOARDING
    assert entry.unmet_requirements[0].value == CloudProvider.AWS

    with_account = recommend_access(model, _context(cloud_accounts=(CloudProvider.AWS,)), [route])
    [entry] = with_account.routes
    assert entry.state == RouteEligibilityState.CURRENTLY_ELIGIBLE

    with_wrong_account = recommend_access(model, _context(cloud_accounts=(CloudProvider.GCP,)), [route])
    [entry] = with_wrong_account.routes
    assert entry.state == RouteEligibilityState.REQUIRES_ONBOARDING


def test_currently_eligible_routes_sort_before_requires_onboarding():
    model = MODELS["gemini-2.5-pro"]
    recommendation = recommend_access(model, _context(has_api_billing=True), ROUTES)

    states = [entry.state for entry in recommendation.routes]
    assert states == sorted(states, key=lambda s: s != RouteEligibilityState.CURRENTLY_ELIGIBLE)


def _make_cloud_hosted_route(model_id: str, provider_value: str) -> AccessRoute:
    template = next(route for route in ROUTES if route.model_id == "claude-opus-5")
    return AccessRoute(
        route_id="fake-cloud-hosted-route",
        provider="AWS",
        model_id=model_id,
        access=template.access.__class__(
            surface=template.access.surface,
            access_method="AWS Bedrock InvokeModel/Converse",
            capabilities=(Capability.DEPLOY,),
            guide_ref="aws-bedrock#claude",
        ),
        eligibility=Eligibility(
            requirements=(
                AccessRequirement(kind=RequirementKind.CLOUD_ACCOUNT, value=CloudProvider(provider_value)),
            ),
            region_scope=template.eligibility.region_scope,
        ),
        economics=template.economics,
        evidence=Evidence(
            source_url="https://example.com",
            consulted_at="2026-08-11",
            status=EvidenceStatus.CONFIRMED,
            caveat="test fixture",
        ),
    )


def _make_enterprise_route(model_id: str) -> AccessRoute:
    template = next(route for route in ROUTES if route.model_id == "claude-opus-5")
    return AccessRoute(
        route_id="fake-enterprise-route",
        provider=template.provider,
        model_id=model_id,
        access=template.access.__class__(
            surface=template.access.surface,
            access_method=template.access.access_method,
            capabilities=(Capability.ENTERPRISE_GOVERNANCE,),
            guide_ref=template.access.guide_ref,
        ),
        eligibility=Eligibility(requirements=(), region_scope=template.eligibility.region_scope),
        economics=template.economics,
        evidence=Evidence(
            source_url="https://example.com",
            consulted_at="2026-08-11",
            status=EvidenceStatus.CONFIRMED,
            caveat="test fixture",
        ),
    )
