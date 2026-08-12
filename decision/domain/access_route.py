"""AccessRoute: one documented way to reach a specific model, per SCHEMA.md's
counterpart for access -- ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 3.2.

Access, Eligibility, and Economics are kept as three explicit, separate
blocks on purpose -- they are independent axes (does the route exist /
who qualifies / what does it cost), and collapsing them back into a flat
list of fields is the exact regression the spec's design review caught
and corrected. See the spec doc, Part 3.1.
"""

from dataclasses import dataclass
from enum import Enum


class Surface(str, Enum):
    DIRECT_API = "direct_api"
    PLAYGROUND_OR_STUDIO = "playground_or_studio"
    CONSUMER_SUBSCRIPTION = "consumer_subscription"
    CLOUD_HOSTED = "cloud_hosted"
    ENTERPRISE = "enterprise"
    SELF_HOSTED = "self_hosted"


class Capability(str, Enum):
    PROTOTYPE = "prototype"
    BUILD = "build"
    DEPLOY = "deploy"
    MANAGED_AGENT = "managed_agent"
    ENTERPRISE_GOVERNANCE = "enterprise_governance"
    AUTOMATION = "automation"


class RequirementKind(str, Enum):
    """Closed vocabulary -- see spec Part 5.2.1. Each kind pairs with an
    optional `value` whose shape depends on the kind (see AccessRequirement).
    """

    API_BILLING_LINKED = "api_billing_linked"
    CLOUD_ACCOUNT = "cloud_account"  # value: CloudProvider
    CONSUMER_SUBSCRIPTION = "consumer_subscription"  # value: tuple[plan_id, ...]
    PROGRAM_MEMBERSHIP = "program_membership"  # value: str
    GPU_INFRASTRUCTURE = "gpu_infrastructure"


class RegionScope(str, Enum):
    ACCOUNT_DEPENDENT = "account_dependent"
    REGION_DEPENDENT = "region_dependent"
    GLOBAL = "global"
    NOT_DETERMINED = "not_determined"


class BillingScheme(str, Enum):
    SUBSCRIPTION_QUOTA = "subscription_quota"
    API_TOKEN = "api_token"
    MEDIA_UNIT = "media_unit"
    CLOUD_PAYGO = "cloud_paygo"
    GPU_LICENSE = "gpu_license"
    PROVISIONED = "provisioned"


class QuotaScope(str, Enum):
    PRODUCT = "product"
    PROJECT = "project"
    ORGANIZATION = "organization"
    BILLING_ACCOUNT = "billing_account"
    REGION = "region"
    ACCOUNT = "account"


class EvidenceStatus(str, Enum):
    CONFIRMED = "confirmed"
    NOT_DETERMINED = "not_determined"
    ACCOUNT_DEPENDENT = "account_dependent"
    REGION_DEPENDENT = "region_dependent"
    DEPRECATED = "deprecated"


@dataclass(frozen=True)
class AccessRequirement:
    kind: RequirementKind
    value: object | None = None  # shape depends on kind, see RequirementKind


@dataclass(frozen=True)
class Access:
    surface: Surface
    access_method: str
    capabilities: tuple[Capability, ...]
    guide_ref: str  # section id in docs/access-guides/{provider}.md


@dataclass(frozen=True)
class Eligibility:
    requirements: tuple[AccessRequirement, ...]
    region_scope: RegionScope


@dataclass(frozen=True)
class Economics:
    billing_owner: str
    billing_scheme: BillingScheme
    quota_scope: QuotaScope
    production_allowed: bool | None  # None = not_determined


@dataclass(frozen=True)
class Evidence:
    source_url: str
    consulted_at: str  # ISO date, kept as string -- displayed as-is, never
    # interpreted into a freshness score (spec Part 5.4.3)
    status: EvidenceStatus
    caveat: str


@dataclass(frozen=True)
class AccessRoute:
    route_id: str
    provider: str
    model_id: str  # exact dataset/models/ id -- never a family, see spec 5.1
    access: Access
    eligibility: Eligibility
    economics: Economics
    evidence: Evidence
