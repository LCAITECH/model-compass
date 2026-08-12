"""Human-readable text for RequirementKind -- interfaces/'s job, not decision/'s.

decision/access/ only knows the closed vocabulary (RequirementKind); how
to phrase "you need this" to a person is presentation, same split as
model_profile.py's best_for()/less_suited_for() for AIModel.
"""

from decision.domain import RequirementKind

_LABELS = {
    RequirementKind.API_BILLING_LINKED: "an API key with billing set up",
    RequirementKind.CLOUD_ACCOUNT: "a cloud account",
    RequirementKind.CONSUMER_SUBSCRIPTION: "one of the listed subscriptions",
    RequirementKind.PROGRAM_MEMBERSHIP: "membership in the listed developer program",
    RequirementKind.GPU_INFRASTRUCTURE: "GPU infrastructure to run it yourself",
}


def requirement_label(requirement) -> str:
    base = _LABELS[requirement.kind]
    if requirement.kind == RequirementKind.CLOUD_ACCOUNT and requirement.value:
        return f"a {requirement.value.upper()} account"
    return base
