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
        return f"a {requirement.value.value.upper()} account"
    return _LABELS[requirement.kind]


def guide_ref_url(guide_ref: str) -> str:
    """Builds the link for a route's `access.guide_ref` (e.g.
    "anthropic#direct-api"), pointing at the curated
    Docs/access-guides/{provider}.md section instead of raw evidence --
    see ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 3.5/5.4. Each guide's
    heading is the literal guide_ref text (e.g. `` `anthropic#direct-api` ``),
    and GitHub's anchor slugifier drops the "#" without inserting a
    separator, so the anchor is the guide_ref with "#" removed.
    """
    provider, _, anchor = guide_ref.partition("#")
    return f"{_GUIDE_BASE_URL}/{provider}.md#{provider}{anchor}"
