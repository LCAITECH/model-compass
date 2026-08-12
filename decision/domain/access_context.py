"""AccessContext: the developer's access-related input, per Access Advisor spec.

Separate from Context (decision/domain/context.py) -- quality/budget
priorities and access circumstances are independent questions, per
ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 3.3.
"""

from dataclasses import dataclass
from enum import Enum


class UseMode(str, Enum):
    MANUAL = "manual"
    PROTOTYPE = "prototype"
    API_INTEGRATION = "api_integration"
    AUTOMATION = "automation"


class WorkloadType(str, Enum):
    EXPLORATORY = "exploratory"
    INTERACTIVE = "interactive"
    BATCH = "batch"
    AGENTIC = "agentic"


class Intensity(str, Enum):
    OCCASIONAL = "occasional"
    FREQUENT = "frequent"
    INTENSIVE = "intensive"


class CloudProvider(str, Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


@dataclass(frozen=True)
class AccessContext:
    """`bool | None` fields use None for "unknown" -- never treated as False,
    and per the spec's closed rule, never treated as True either: an
    unconfirmable requirement leaves a route in REQUIRES_ONBOARDING (see
    decision/access/advisor.py).
    """

    use_mode: UseMode
    workload_type: WorkloadType
    intensity: Intensity
    country: str | None  # ISO 3166-1 alpha-2, None = unknown; informational
    # only in v1 -- never gates a route (no stable per-country match data,
    # see spec Part 5.1).
    subscriptions: tuple[str, ...]  # plan_id values from subscriptions/*.yaml
    has_api_billing: bool | None
    cloud_accounts: tuple[CloudProvider, ...]
    program_memberships: tuple[str, ...]
    has_gpu_infrastructure: bool | None
