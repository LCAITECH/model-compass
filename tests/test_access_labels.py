from decision.domain import AccessRequirement, CloudProvider, RequirementKind
from interfaces.web.access_labels import requirement_label


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
