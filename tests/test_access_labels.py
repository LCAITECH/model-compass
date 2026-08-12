from decision.domain import AccessRequirement, CloudProvider, RequirementKind
from interfaces.web.access_labels import guide_ref_url, requirement_label


def test_consumer_subscription_names_actual_plans_when_known():
    requirement = AccessRequirement(
        kind=RequirementKind.CONSUMER_SUBSCRIPTION, value=("google-ai-pro", "google-ai-ultra")
    )
    plan_names = {"google-ai-pro": "Google AI Pro", "google-ai-ultra": "Google AI Ultra"}

    assert requirement_label(requirement, plan_names) == "Google AI Pro or Google AI Ultra"


def test_consumer_subscription_falls_back_to_plan_id_for_unknown_plan():
    requirement = AccessRequirement(kind=RequirementKind.CONSUMER_SUBSCRIPTION, value=("mystery-plan",))
    plan_names = {"google-ai-pro": "Google AI Pro"}  # doesn't include "mystery-plan"

    assert requirement_label(requirement, plan_names) == "mystery-plan"


def test_consumer_subscription_uses_generic_text_without_plan_names():
    requirement = AccessRequirement(kind=RequirementKind.CONSUMER_SUBSCRIPTION, value=("google-ai-pro",))

    assert requirement_label(requirement) == "one of the listed subscriptions"


def test_cloud_account_names_the_specific_provider():
    requirement = AccessRequirement(kind=RequirementKind.CLOUD_ACCOUNT, value=CloudProvider.AWS)

    assert requirement_label(requirement) == "a AWS account"


def test_api_billing_linked_uses_fixed_label():
    requirement = AccessRequirement(kind=RequirementKind.API_BILLING_LINKED, value=None)

    assert requirement_label(requirement) == "an API key with billing set up"


def test_guide_ref_url_points_at_the_curated_guide_section():
    url = guide_ref_url("anthropic#direct-api")

    assert url == (
        "https://github.com/LCAITECH/model-compass/blob/main/"
        "Docs/access-guides/anthropic.md#anthropicdirect-api"
    )


def test_guide_ref_url_matches_every_real_guide_ref():
    """Every guide_ref in the dataset must resolve to a heading that
    actually exists in its Docs/access-guides/{provider}.md file --
    verified against GitHub's anchor-slug rule (drop non-alphanumeric
    characters, no separator inserted for the removed '#')."""
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    real_guide_refs = [
        "anthropic#direct-api",
        "openai#direct-api",
        "google#direct-api",
        "google#ai-studio",
    ]
    for guide_ref in real_guide_refs:
        provider, _, anchor = guide_ref.partition("#")
        guide_text = (root / "Docs" / "access-guides" / f"{provider}.md").read_text(encoding="utf-8")
        assert re.search(rf"^## `{re.escape(guide_ref)}`$", guide_text, re.MULTILINE), guide_ref
        assert guide_ref_url(guide_ref).endswith(f"{provider}.md#{provider}{anchor}")
