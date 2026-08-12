"""SubscriptionPlan: a consumer/developer plan documented in subscriptions/*.yaml.

Deliberately never references a model or a route -- the relationship is
one-directional. An AccessRoute's `consumer_subscription` requirement
points at a plan_id (see access_route.py); a plan never declares what it
satisfies. See ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 5.4.1 for why the
earlier two-directional design (`satisfies_requirements` on both sides)
was dropped as redundant.
"""

from dataclasses import dataclass

from decision.domain.access_route import EvidenceStatus, Surface


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
