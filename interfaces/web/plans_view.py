"""View logic for /plans ("Subscription or API?").

Reads the form, asks decision/access/plan_compare.py for the facts and the
verdict, and turns them into what the page shows. The only numbers made
here are the tokens a dollar amount buys at a model's stored prices (the
rule affordability.py already follows) and differences between two dollar
amounts. A plan's usage limit is never shown as a number: no provider
publishes it in tokens, and the page says so instead.
"""

from urllib.parse import urlencode

from decision.access import compare_plans
from decision.domain import AIModel, MonthlyUsage, UseMode, Verdict
from interfaces.web.affordability import (
    capacity_bar_widths,
    estimated_input_capacity,
    estimated_output_capacity,
    parse_budget_usd,
)
from interfaces.web.catalog_notices import short_date
from interfaces.web.compare_cells import dollars, tokens
from interfaces.web.comparison import group_models

USE_CHOICES = (
    (UseMode.MANUAL, "I use it myself", "Chat, apps and coding tools: Claude.ai, ChatGPT, the Gemini app, Claude Code"),
    (UseMode.API_INTEGRATION, "I'm building on it", "An app, a service or an automation that calls the model"),
)


def _millions(raw: str | None) -> float | None:
    try:
        value = float(raw) if raw not in (None, "") else None
    except ValueError:
        return None
    return value if value is not None and value >= 0 else None


def parse_usage(form: dict) -> MonthlyUsage | None:
    """Monthly usage in millions of tokens, as typed; None when neither field is filled."""
    input_m, output_m = _millions(form.get("input_m")), _millions(form.get("output_m"))
    if input_m is None and output_m is None:
        return None
    return MonthlyUsage(input_tokens=round((input_m or 0) * 1_000_000), output_tokens=round((output_m or 0) * 1_000_000))


def _use_mode(form: dict) -> UseMode:
    try:
        return UseMode(form.get("use") or UseMode.MANUAL.value)
    except ValueError:
        return UseMode.MANUAL


def _capacity(usd: float, model: AIModel) -> dict:
    input_count, output_count = estimated_input_capacity(usd, model), estimated_output_capacity(usd, model)
    input_bar, output_bar = capacity_bar_widths(input_count, output_count)
    capacity = {
        "input": tokens(input_count),
        "output": tokens(output_count),
        "input_bar": input_bar,
        "output_bar": output_bar,
        "after_promo": None,
    }
    cost = model.cost
    if cost.effective_until and cost.reverts_to.input_per_million > 0 and cost.reverts_to.output_per_million > 0:
        later_in = round(usd / cost.reverts_to.input_per_million * 1_000_000)
        later_out = round(usd / cost.reverts_to.output_per_million * 1_000_000)
        capacity["after_promo"] = (
            f"Introductory price through {short_date(cost.effective_until)}; after that the same amount buys "
            f"{tokens(later_in)} of input or {tokens(later_out)} of output."
        )
    return capacity


def _option_card(option, comparison, form: dict, plan_names: dict[str, str]) -> dict:
    plan, model = option.plan, comparison.model
    multiplier = None
    if plan.usage_multiplier and option.base_price_usd:
        base_name = plan_names.get(plan.usage_multiplier.relative_to, plan.usage_multiplier.relative_to)
        ratio = plan.price.monthly_usd / option.base_price_usd
        multiplier = (
            f"{plan.usage_multiplier.factor:g}× {base_name} ({plan.usage_multiplier.scope}) "
            f"for {ratio:.1f}× its price"
        )
    credits = None
    if option.credits_usd:
        credits = {
            "amount": dollars(option.credits_usd),
            "input": tokens(estimated_input_capacity(option.credits_usd, model)),
            "output": tokens(estimated_output_capacity(option.credits_usd, model)),
            "conditions": plan.api_credits.conditions,
        }
    params = {"model": model.id, "use": form.get("use") or "", "plan": plan.plan_id}
    params.update({key: form[key] for key in ("input_m", "output_m") if form.get(key)})
    return {
        "plan": plan,
        "price": dollars(plan.price.monthly_usd),
        "multiplier": multiplier,
        "credits": credits,
        "methods": [route.access.access_method for route in option.routes],
        "production_allowed": any(route.economics.production_allowed for route in option.routes),
        "chosen": comparison.chosen is not None and comparison.chosen.plan.plan_id == plan.plan_id,
        "href": "/plans?" + urlencode({k: v for k, v in params.items() if v}),
    }


def _verdict_copy(comparison) -> dict:
    verdict, chosen = comparison.verdict, comparison.chosen
    name = chosen.plan.plan_name if chosen else ""
    amount = dollars(comparison.monthly_usd) if comparison.monthly_usd is not None else ""
    cost = dollars(comparison.api_cost_usd) if comparison.api_cost_usd is not None else ""
    if verdict == Verdict.API_TO_INTEGRATE:
        detail = "An app or automation needs the API: no plan's usage limit can be used through it."
        if any(option.credits_usd for option in comparison.options):
            detail += " Some plans that include this model also come with monthly API credits for it (below)."
        return {"tone": "api", "headline": "Use the API", "detail": detail}
    if verdict == Verdict.API_ONLY_PATH:
        return {"tone": "api", "headline": "The API is the way in", "detail": f"No plan in this catalog names {comparison.model.name}."}
    if verdict == Verdict.NO_COST_VERDICT:
        return {
            "tone": "open",
            "headline": "Add your monthly usage to compare costs",
            "detail": f"Without it, the honest comparison is what {amount} buys on the API, next to a plan whose limit is not published in tokens.",
        }
    gap = dollars(abs(comparison.monthly_usd - comparison.api_cost_usd))
    if verdict == Verdict.API_CHEAPER:
        detail = f"Your usage costs {cost} a month on the API, {gap} less than {name} at {amount}."
        if comparison.credits_cover_usage:
            detail += f" {name}'s included API credits would also cover it."
        return {"tone": "api", "headline": "The API costs less for your usage", "detail": detail}
    return {
        "tone": "plan",
        "headline": "The plan may cost less, if its limit covers you",
        "detail": (
            f"Your usage costs {cost} a month on the API, {gap} more than {name} at {amount}. "
            f"{chosen.plan.provider} does not publish the plan's limit in tokens, so whether it covers that usage cannot be known from here."
        ),
    }


def plans_context(form: dict, models: list[AIModel], routes, plans) -> dict:
    """Everything plans.html needs, for a form that may be empty or partial."""
    by_id = {model.id: model for model in models}
    model = by_id.get((form.get("model") or "").strip())
    context = {
        "form": form,
        "model_groups": group_models(models),
        "use_choices": USE_CHOICES,
        "model": model,
        "comparison": None,
        "plan_count": len(plans),
    }
    if not model:
        return context

    use_mode = _use_mode(form)
    plan_id = form.get("plan") or None
    # The amount only counts for the plan it was filled in for; switching plans
    # without JavaScript would otherwise carry the old plan's price along.
    amount = parse_budget_usd(form.get("monthly_usd")) if (form.get("amount_for") or None) == plan_id else None
    usage = parse_usage(form)
    comparison = compare_plans(model, routes, plans, use_mode, plan_id=plan_id, monthly_usd=amount, usage=usage)
    plan_names = {plan.plan_id: plan.plan_name for plan in plans}
    cards = [_option_card(option, comparison, form, plan_names) for option in comparison.options]
    context.update(
        {
            "use_mode": use_mode,
            "comparison": comparison,
            "verdict": _verdict_copy(comparison),
            "cards": cards,
            "chosen_card": next((card for card in cards if card["chosen"]), None),
            "capacity": _capacity(comparison.monthly_usd, model) if comparison.monthly_usd else None,
            "amount": dollars(comparison.monthly_usd) if comparison.monthly_usd is not None else None,
            "api_cost": dollars(comparison.api_cost_usd) if comparison.api_cost_usd is not None else None,
        }
    )
    return context
