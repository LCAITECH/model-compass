"""compare_plans: "should I pay for this model with a subscription or the API?"

Part of the Access Advisor's question ("how do I reach this model"), never
"which model should I use": the model is an input, and this module never
imports decision/evaluator/ or decision/explainer/, so nothing here can
change which model wins (ARCHITECTURE.md; FEATURES.md, "Subscription vs.
API Comparator").

Everything is read from attributes: a plan includes a model when a route
for that model names the plan in a consumer_subscription requirement and
bills against the plan's quota; included API credits count for a model
when the plan's provider is the model's provider and the model has a route
on the surface the credits are spent on. No model or provider name appears
in this file.

The only arithmetic is exact: the API cost of a usage the developer typed
in, at the model's current list prices. A plan's usage limit is never
turned into tokens, because no provider publishes it that way; when the
API costs more than the plan, the verdict says the plan *may* be cheaper,
only if its unpublished limit covers that usage.
"""

from decision.domain.access_context import UseMode
from decision.domain.access_route import AccessRoute, BillingScheme, RequirementKind
from decision.domain.ai_model import AIModel
from decision.domain.plan_comparison import MonthlyUsage, PlanComparison, PlanOption, Verdict
from decision.domain.subscription import SubscriptionPlan

# Building something that calls the model: a plan's quota is never usable that way.
_INTEGRATION_MODES = (UseMode.API_INTEGRATION, UseMode.AUTOMATION)


def api_cost(model: AIModel, usage: MonthlyUsage) -> float:
    """Exact monthly cost of `usage` at the model's current list prices."""
    return (
        usage.input_tokens / 1_000_000 * model.cost.input_per_million
        + usage.output_tokens / 1_000_000 * model.cost.output_per_million
    )


def _plan_routes(model: AIModel, routes: list[AccessRoute]) -> dict[str, list[AccessRoute]]:
    """plan_id -> the model's routes that bill against that plan's quota."""
    by_plan: dict[str, list[AccessRoute]] = {}
    for route in routes:
        if route.model_id != model.id or route.economics.billing_scheme != BillingScheme.SUBSCRIPTION_QUOTA:
            continue
        for requirement in route.eligibility.requirements:
            if requirement.kind == RequirementKind.CONSUMER_SUBSCRIPTION:
                for plan_id in requirement.value:
                    by_plan.setdefault(plan_id, []).append(route)
    return by_plan


def _usable_credits(plan: SubscriptionPlan, model: AIModel, model_routes: list[AccessRoute]) -> float | None:
    credits = plan.api_credits
    if not credits or plan.provider != model.provider:
        return None
    if not any(route.access.surface == credits.surface for route in model_routes):
        return None
    return credits.monthly_usd


def plan_options(model: AIModel, routes: list[AccessRoute], plans: list[SubscriptionPlan]) -> tuple[PlanOption, ...]:
    """Every plan that includes `model`, cheapest first."""
    by_id = {plan.plan_id: plan for plan in plans}
    model_routes = [route for route in routes if route.model_id == model.id]
    options = []
    for plan_id, plan_routes in _plan_routes(model, routes).items():
        plan = by_id.get(plan_id)
        if plan is None:
            continue  # validate_subscription_references already guarantees this never happens
        base = by_id.get(plan.usage_multiplier.relative_to) if plan.usage_multiplier else None
        options.append(
            PlanOption(
                plan=plan,
                routes=tuple(plan_routes),
                credits_usd=_usable_credits(plan, model, model_routes),
                base_price_usd=base.price.monthly_usd if base else None,
            )
        )
    return tuple(sorted(options, key=lambda option: (option.plan.price.monthly_usd, option.plan.plan_id)))


def compare_plans(
    model: AIModel,
    routes: list[AccessRoute],
    plans: list[SubscriptionPlan],
    use_mode: UseMode,
    *,
    plan_id: str | None = None,
    monthly_usd: float | None = None,
    usage: MonthlyUsage | None = None,
) -> PlanComparison:
    """The facts and the verdict for paying for `model` by plan or by API.

    `plan_id` picks the plan to compare (default: the cheapest that includes
    the model). `monthly_usd` overrides that plan's list price with what the
    developer actually pays (regional price, taxes). `usage` is optional and
    only ever comes from the developer.
    """
    options = plan_options(model, routes, plans)
    chosen = next((option for option in options if option.plan.plan_id == plan_id), options[0] if options else None)
    amount = monthly_usd if monthly_usd is not None else (chosen.plan.price.monthly_usd if chosen else None)
    cost = api_cost(model, usage) if usage else None
    credits_cover = bool(chosen and chosen.credits_usd and cost is not None and cost <= chosen.credits_usd)

    if use_mode in _INTEGRATION_MODES:
        verdict = Verdict.API_TO_INTEGRATE
    elif not options:
        verdict = Verdict.API_ONLY_PATH
    elif cost is None or amount is None:
        verdict = Verdict.NO_COST_VERDICT
    elif cost <= amount:
        verdict = Verdict.API_CHEAPER
    else:
        verdict = Verdict.PLAN_MAY_BE_CHEAPER

    return PlanComparison(
        model=model,
        options=options,
        chosen=chosen,
        monthly_usd=amount,
        usage=usage,
        api_cost_usd=cost,
        credits_cover_usage=credits_cover,
        verdict=verdict,
    )
