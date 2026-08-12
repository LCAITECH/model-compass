"""AccessRecommendation: the output of decision/access/, per
ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 5.3.

Answers "how can I access this model" -- a separate question from
Recommendation's "which model should I use". Never ranks routes against
each other (see spec Part 5.2.2 for why that was designed, then
reverted): routes are grouped by eligibility state only, in a stable
alphabetical order within each group that carries no meaning beyond
making repeated runs deterministic.
"""

from dataclasses import dataclass
from enum import Enum

from decision.domain.access_route import AccessRequirement, AccessRoute
from decision.domain.ai_model import AIModel


class RouteEligibilityState(str, Enum):
    CURRENTLY_ELIGIBLE = "currently_eligible"
    REQUIRES_ONBOARDING = "requires_onboarding"
    # NOT_AVAILABLE deliberately has no member here -- a route in that
    # state never reaches a RouteEntry, see decision/access/advisor.py.


@dataclass(frozen=True)
class RouteEntry:
    route: AccessRoute
    state: RouteEligibilityState
    unmet_requirements: tuple[AccessRequirement, ...]  # empty when CURRENTLY_ELIGIBLE


@dataclass(frozen=True)
class AccessSummary:
    """What the short "Acceso recomendado" line shows -- spec Part 3.5.

    highlighted_route is only ever set when exactly one CURRENTLY_ELIGIBLE
    (or, absent those, REQUIRES_ONBOARDING) route has surface == direct_api
    AND evidence.status == confirmed. Otherwise it's None and the caller
    shows a neutral count instead of guessing a "best" route.
    """

    highlighted_route: AccessRoute | None
    bucket_state: RouteEligibilityState | None  # which bucket the summary is
    # drawn from; None means no route at all (see RouteEntry emptiness).
    bucket_size: int


@dataclass(frozen=True)
class AccessRecommendation:
    model: AIModel
    routes: tuple[RouteEntry, ...]  # NOT_AVAILABLE already excluded; CURRENTLY_ELIGIBLE
    # entries first, then REQUIRES_ONBOARDING, alphabetical by route_id within
    # each group.
    summary: AccessSummary
