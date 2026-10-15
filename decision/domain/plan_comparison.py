"""What the subscription-or-API comparison returns (decision/access/plan_compare.py).

A plan's usage limit never appears here as a number: providers do not
publish it in tokens. What is exact is the API side (the model's list
prices times a usage the developer typed in) and each plan's published
price, multiplier and included API credits.
"""

from dataclasses import dataclass
from enum import Enum

from decision.domain.access_route import AccessRoute
from decision.domain.ai_model import AIModel
from decision.domain.subscription import SubscriptionPlan


@dataclass(frozen=True)
class MonthlyUsage:
    """Tokens per month, as the developer states them (never estimated)."""

    input_tokens: int
    output_tokens: int


class Verdict(str, Enum):
    API_TO_INTEGRATE = "api_to_integrate"  # an app or automation needs the API
    API_ONLY_PATH = "api_only_path"  # no documented plan includes the model
    API_CHEAPER = "api_cheaper"  # the stated usage costs no more on the API
    PLAN_MAY_BE_CHEAPER = "plan_may_be_cheaper"  # only if the unpublished limit covers it
    NO_COST_VERDICT = "no_cost_verdict"  # no usage given: nothing honest to compare


@dataclass(frozen=True)
class PlanOption:
    plan: SubscriptionPlan
    routes: tuple[AccessRoute, ...]  # the documented routes naming this plan for the model
    credits_usd: float | None  # included API credits spendable on this model, if any
    base_price_usd: float | None  # price of the plan the multiplier is relative to


@dataclass(frozen=True)
class PlanComparison:
    model: AIModel
    options: tuple[PlanOption, ...]  # every plan that includes the model, cheapest first
    chosen: PlanOption | None
    monthly_usd: float | None  # the amount compared: the chosen plan's price unless overridden
    usage: MonthlyUsage | None
    api_cost_usd: float | None  # exact cost of `usage` at the model's current list prices
    credits_cover_usage: bool  # the chosen plan's API credits alone pay for `usage`
    verdict: Verdict
