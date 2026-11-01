"""Human-readable text for RequirementKind, plus a general snake_case->label helper.

decision/access/ only knows the closed vocabulary (RequirementKind); how
to phrase "you need this" to a person is presentation, same split as
model_profile.py's best_for()/less_suited_for() for AIModel.
"""

from decision.domain import CloudProvider, RequirementKind

# Spelled out per provider: the article follows the name ("an AWS", "a
# Google Cloud"), which uppercasing the enum value got wrong.
_CLOUD_ACCOUNTS = {
    CloudProvider.AWS: "an AWS account",
    CloudProvider.AZURE: "an Azure account",
    CloudProvider.GCP: "a Google Cloud account",
}

_LABELS = {
    RequirementKind.API_BILLING_LINKED: "an API key with billing set up",
    RequirementKind.CLOUD_ACCOUNT: "a cloud account",
    RequirementKind.CONSUMER_SUBSCRIPTION: "one of the listed subscriptions",
    RequirementKind.PROGRAM_MEMBERSHIP: "membership in the listed developer program",
    RequirementKind.GPU_INFRASTRUCTURE: "GPU infrastructure to run it yourself",
}

_GUIDE_BASE_URL = "https://github.com/LCAITECH/model-compass/blob/main/Docs/access-guides"


def requirement_label(requirement, plan_names: dict[str, str] | None = None) -> str:
    """`plan_names` maps subscriptions/*.yaml plan_id -> plan_name, so a
    consumer_subscription requirement can name the actual plans ("Google AI
    Pro or Google AI Ultra") instead of the generic fallback -- built once
    in app.py from the SubscriptionPlan catalog already loaded there.
    """
    if requirement.kind == RequirementKind.CONSUMER_SUBSCRIPTION and plan_names:
        names = [plan_names.get(plan_id, plan_id) for plan_id in requirement.value]
        return " or ".join(names)
    if requirement.kind == RequirementKind.CLOUD_ACCOUNT and requirement.value:
        return _CLOUD_ACCOUNTS[requirement.value]
    return _LABELS[requirement.kind]


_ACRONYMS = {"api": "API"}


def humanize(value: str) -> str:
    """Turns a snake_case enum value into a readable label ("very_high" -> "Very high",
    "api_integration" -> "API integration")."""
    words = value.replace("_", " ").capitalize().split(" ")
    return " ".join(_ACRONYMS.get(word.lower(), word) for word in words)


def guide_ref_url(guide_ref: str) -> str:
    """Builds the link for a route's `access.guide_ref` (e.g.
    "anthropic#direct-api"), pointing at the curated
    Docs/access-guides/{provider}.md section instead of raw evidence.
    Each guide's heading is the literal guide_ref text (e.g.
    `` `anthropic#direct-api` ``), and GitHub's anchor slugifier drops
    the "#" without inserting a separator, so the anchor is the guide_ref
    with "#" removed.
    """
    provider, _, anchor = guide_ref.partition("#")
    return f"{_GUIDE_BASE_URL}/{provider}.md#{provider}{anchor}"


# Each RouteNote phrased for the visitor. "fits" marks the one positive note,
# so the template can style it apart from the cautions.
ROUTE_NOTES = {
    "not_for_production": ("You're building on it, and this route doesn't allow production use.", False),
    "for_personal_use": ("Fits using it yourself: the provider's own apps, signed in with your plan.", True),
    "no_automation": ("This route doesn't document automated use, which batch and agent workloads rely on.", False),
    "quota_not_in_tokens": ("At frequent or intensive use, mind the plan's limit: its provider doesn't publish it in tokens.", False),
}


def route_note(note) -> tuple[str, bool]:
    """(text, fits) for a decision.domain.RouteNote."""
    return ROUTE_NOTES[note.value]
