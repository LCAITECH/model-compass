import re
from pathlib import Path

import pytest

from decision.domain import AccessRoute, RequirementKind, SubscriptionPlan
from decision.loader import (
    DatasetValidationError,
    load_access_route_file,
    load_access_routes,
    load_dataset,
    load_subscription_file,
    load_subscriptions,
    validate_route_references,
    validate_subscription_references,
)

ROOT = Path(__file__).resolve().parents[1]
ACCESS_ROUTES_DIR = ROOT / "dataset" / "access_routes"
SUBSCRIPTIONS_DIR = ROOT / "dataset" / "subscriptions"
MODELS_DIR = ROOT / "dataset" / "models"


def test_loads_all_real_access_routes():
    routes = load_access_routes(ACCESS_ROUTES_DIR)

    assert len(routes) == 4
    assert all(isinstance(route, AccessRoute) for route in routes)
    assert {route.route_id for route in routes} == {
        "claude-opus-5-direct-api",
        "gpt-5-direct-api",
        "gemini-2.5-pro-direct-api",
        "gemini-2.5-pro-ai-studio",
    }


def test_loads_all_real_subscriptions():
    plans = load_subscriptions(SUBSCRIPTIONS_DIR)

    assert len(plans) == 2
    assert all(isinstance(plan, SubscriptionPlan) for plan in plans)
    assert {plan.plan_id for plan in plans} == {"google-ai-pro", "google-ai-ultra"}


def test_real_route_references_are_valid():
    routes = load_access_routes(ACCESS_ROUTES_DIR)
    models = load_dataset(MODELS_DIR)

    validate_route_references(routes, models)  # must not raise


def test_real_subscription_references_are_valid():
    routes = load_access_routes(ACCESS_ROUTES_DIR)
    subscriptions = load_subscriptions(SUBSCRIPTIONS_DIR)

    validate_subscription_references(routes, subscriptions)  # must not raise


def test_free_text_fields_stay_in_english():
    # Model Compass has no i18n system -- every other dataset field
    # (dataset/models/*.yaml) is English-only, and the web UI is
    # English-only, so free-text fields here (evidence.caveat,
    # documented_exclusions) must never ship in Spanish/Spanglish
    # either. Regression for the ai-studio route's caveat, which
    # originally shipped as "Restricciones de Google One indican...".
    spanish_markers = re.compile(
        r"\b(que|el|la|los|las|una|esta|está|cuenta|requiere|indican|vinculada|"
        r"salvedad|facturado|cuotas|creditos|créditos|proyecto)\b",
        re.IGNORECASE,
    )

    routes = load_access_routes(ACCESS_ROUTES_DIR)
    for route in routes:
        assert not spanish_markers.search(route.evidence.caveat), (route.route_id, route.evidence.caveat)

    plans = load_subscriptions(SUBSCRIPTIONS_DIR)
    for plan in plans:
        for exclusion in plan.documented_exclusions:
            assert not spanish_markers.search(exclusion), (plan.plan_id, exclusion)


def test_gemini_ai_studio_route_requires_consumer_subscription():
    route = load_access_route_file(ACCESS_ROUTES_DIR / "google" / "gemini-2.5-pro-ai-studio.yaml")

    [requirement] = route.eligibility.requirements
    assert requirement.kind == RequirementKind.CONSUMER_SUBSCRIPTION
    assert requirement.value == ("google-ai-pro", "google-ai-ultra")


def test_rejects_unknown_model_id(tmp_path):
    routes_dir = tmp_path / "access_routes" / "anthropic"
    routes_dir.mkdir(parents=True)
    (routes_dir / "fake-route.yaml").write_text(_MINIMAL_ROUTE.replace("REPLACE_ME", "not-a-real-model"), encoding="utf-8")

    routes = load_access_routes(tmp_path / "access_routes")
    models = load_dataset(MODELS_DIR)

    with pytest.raises(DatasetValidationError) as exc_info:
        validate_route_references(routes, models)

    assert "does not exist in dataset/models/" in str(exc_info.value)


def test_rejects_unknown_plan_id(tmp_path):
    routes_dir = tmp_path / "access_routes" / "google"
    routes_dir.mkdir(parents=True)
    (routes_dir / "fake-route.yaml").write_text(_MINIMAL_CONSUMER_SUBSCRIPTION_ROUTE, encoding="utf-8")

    routes = load_access_routes(tmp_path / "access_routes")

    with pytest.raises(DatasetValidationError) as exc_info:
        validate_subscription_references(routes, [])

    assert "unknown plan_id" in str(exc_info.value)


def test_rejects_missing_required_fields(tmp_path):
    routes_dir = tmp_path / "access_routes" / "anthropic"
    routes_dir.mkdir(parents=True)
    path = routes_dir / "incomplete.yaml"
    path.write_text("provider: Anthropic\n", encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_access_route_file(path)

    assert "missing required field" in str(exc_info.value)


def test_rejects_invalid_requirement_kind(tmp_path):
    routes_dir = tmp_path / "access_routes" / "anthropic"
    routes_dir.mkdir(parents=True)
    path = routes_dir / "broken.yaml"
    path.write_text(_MINIMAL_ROUTE.replace("REPLACE_ME", "claude-opus-5").replace("api_billing_linked", "made_up_kind"), encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_access_route_file(path)

    assert "invalid requirement kind" in str(exc_info.value)


def test_rejects_invalid_cloud_account_value(tmp_path):
    routes_dir = tmp_path / "access_routes" / "anthropic"
    routes_dir.mkdir(parents=True)
    path = routes_dir / "broken.yaml"
    path.write_text(
        _MINIMAL_ROUTE.replace("REPLACE_ME", "claude-opus-5").replace(
            "kind: api_billing_linked", "kind: cloud_account\n      value: digitalocean"
        ),
        encoding="utf-8",
    )

    with pytest.raises(DatasetValidationError) as exc_info:
        load_access_route_file(path)

    assert "invalid cloud_account value" in str(exc_info.value)


def test_rejects_subscription_missing_fields(tmp_path):
    subs_dir = tmp_path / "subscriptions" / "google"
    subs_dir.mkdir(parents=True)
    path = subs_dir / "incomplete.yaml"
    path.write_text("provider: Google\n", encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_subscription_file(path)

    assert "missing required field" in str(exc_info.value)


def test_rejects_subscription_with_non_list_documented_exclusions(tmp_path):
    subs_dir = tmp_path / "subscriptions" / "google"
    subs_dir.mkdir(parents=True)
    path = subs_dir / "broken.yaml"
    path.write_text(_MINIMAL_SUBSCRIPTION.replace("REPLACE_ME", '"no API billing"'), encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_subscription_file(path)

    assert "documented_exclusions must be a list of strings" in str(exc_info.value)


_MINIMAL_SUBSCRIPTION = """
provider: Google
plan_name: Test Plan
surface_entitlements: [playground_or_studio]
documented_exclusions: REPLACE_ME
region_scope: account_dependent
source_url: https://example.com
consulted_at: "2026-08-11"
status: confirmed
"""

_MINIMAL_ROUTE = """
provider: Anthropic
model_id: REPLACE_ME
access:
  surface: direct_api
  access_method: "API key"
  capabilities: [prototype]
  guide_ref: anthropic#direct-api
eligibility:
  requirements:
    - kind: api_billing_linked
  region_scope: account_dependent
economics:
  billing_owner: Anthropic
  billing_scheme: api_token
  quota_scope: organization
  production_allowed: true
evidence:
  source_url: https://example.com
  consulted_at: "2026-08-11"
  status: confirmed
  caveat: "test fixture"
"""

_MINIMAL_CONSUMER_SUBSCRIPTION_ROUTE = """
provider: Google
model_id: gemini-2.5-pro
access:
  surface: playground_or_studio
  access_method: "Google AI Studio"
  capabilities: [prototype]
  guide_ref: google#ai-studio
eligibility:
  requirements:
    - kind: consumer_subscription
      value: [not-a-real-plan]
  region_scope: account_dependent
economics:
  billing_owner: Google
  billing_scheme: subscription_quota
  quota_scope: account
  production_allowed: false
evidence:
  source_url: https://example.com
  consulted_at: "2026-08-11"
  status: confirmed
  caveat: "test fixture"
"""
