"""SubscriptionPlan: a consumer/developer plan documented in subscriptions/*.yaml.

Deliberately never references a model or a route -- the relationship is
one-directional. An AccessRoute's `consumer_subscription` requirement
points at a plan_id (see access_route.py); a plan never declares what it
satisfies. See ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 5.4.1 for why the
earlier two-directional design (`satisfies_requirements` on both sides)
was dropped as redundant.

Price, usage multiplier and included API credits are objective facts
from the provider's own pages (SCHEMA.md, "Subscription plans"). None of
them is a token count: providers do not publish plan limits in tokens,
and nothing here pretends they do.
"""

from dataclasses import dataclass

from decision.domain.access_route import EvidenceStatus, Surface


@dataclass(frozen=True)
class PlanPrice:
    monthly_usd: float  # US list price, monthly billing, before tax


@dataclass(frozen=True)
class UsageMultiplier:
    """The provider's own "N times plan X" statement, never converted to tokens."""

    relative_to: str  # plan_id in this catalog (checked by the loader)
    factor: float
    scope: str  # what is multiplied, in the provider's words


@dataclass(frozen=True)
class ApiCredits:
    """API spend included with the plan, usable on the plan provider's API."""

    monthly_usd: float
    surface: Surface  # where the credits are spent
    conditions: str  # expiry, separate account, exclusions, in plain words


@dataclass(frozen=True)
class SubscriptionPlan:
    plan_id: str
    provider: str
    plan_name: str
    surface_entitlements: tuple[Surface, ...]  # informational only -- never
    # consulted for eligibility matching, only for "what this plan gets you"
    # display text.
    documented_exclusions: tuple[str, ...]  # informational, e.g. "no API billing"
    region_scope: str
    source_url: str
    consulted_at: str
    status: EvidenceStatus
    price: PlanPrice
    usage_multiplier: UsageMultiplier | None = None
    api_credits: ApiCredits | None = None
