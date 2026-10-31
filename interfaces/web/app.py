"""FastAPI app: the web interface, and the only consumer of decision/ in the MVP.

Loads the dataset once at startup, turns a form submission into a
Context, and renders whatever decision/ returns. Has no decision logic
of its own — per ARCHITECTURE.md, decision/ would work identically if
this whole package were deleted.
"""

import math
from datetime import date
from pathlib import Path
from urllib.parse import urlencode

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from decision.access import recommend_access
from decision.domain import BudgetLevel, CloudProvider, Intensity, Priority, UseMode, WorkloadType, language_name
from decision.evaluator import evaluate
from decision.explainer import NoQualifyingModelsError, explain
from decision.loader import (
    load_access_routes,
    load_dataset,
    load_subscriptions,
    validate_route_references,
    validate_subscription_references,
)
from interfaces.web.access_context_form import access_context_from_form
from interfaces.web.access_labels import guide_ref_url, humanize, requirement_label
from interfaces.web.catalog_notices import badges_for, catalog_notices, short_date
from interfaces.web.graph_data import graph_items, ring_counts
from interfaces.web.affordability import (
    capacity_bar_widths,
    cheapest_qualifying_alternative,
    cost_savings_pct,
    estimated_input_capacity,
    estimated_output_capacity,
    parse_budget_usd,
)
from interfaces.web.compare_visuals import constellation_frame, constellations, orbit, podium
from interfaces.web.comparison import (
    MAX_COMPARED,
    MIN_COMPARED,
    build_comparison,
    context_fit,
    group_models,
    parse_selection,
    row_counts,
    selection_links,
)
from interfaces.web.context_form import InvalidFormError, context_from_form
from interfaces.web.error_pages import install_error_pages
from interfaces.web.model_profile import best_for, less_suited_for, quality_profile
from interfaces.web.plans_view import plans_context
from interfaces.web.use_case_matcher import match_use_case
from interfaces.web.use_cases import USE_CASES
from interfaces.web.whatif import options as whatif_options
from interfaces.web.whatif_routes import make_router

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR.parent.parent / "dataset" / "models"
ACCESS_ROUTES_DIR = BASE_DIR.parent.parent / "dataset" / "access_routes"
SUBSCRIPTIONS_DIR = BASE_DIR.parent.parent / "dataset" / "subscriptions"

app = FastAPI(title="Model Compass")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.filters["language_name"] = language_name
templates.env.filters["requirement_label"] = requirement_label
templates.env.filters["guide_ref_url"] = guide_ref_url
templates.env.filters["humanize"] = humanize
templates.env.filters["short_date"] = short_date
install_error_pages(app, templates)

models = load_dataset(DATASET_DIR)
languages = sorted({language for model in models for language in model.languages})
providers = sorted({model.provider for model in models})

use_case_priorities = {label: priorities for label, priorities in USE_CASES}

access_routes = load_access_routes(ACCESS_ROUTES_DIR)
subscriptions = load_subscriptions(SUBSCRIPTIONS_DIR)
validate_route_references(access_routes, models)
validate_subscription_references(access_routes, subscriptions)
subscription_plan_names = {plan.plan_id: plan.plan_name for plan in subscriptions}

# Dated notices are computed per render, so a server left running across
# midnight still counts days from the real "today".
templates.env.globals["badges_for"] = lambda model: badges_for(model, models, date.today())
templates.env.globals["catalog_notices"] = lambda: catalog_notices(models, date.today())
templates.env.globals["graph_items"] = lambda recommendation: graph_items(
    recommendation, lambda model: badges_for(model, models, date.today())
)
templates.env.globals["ring_counts"] = ring_counts
templates.env.globals["whatif_options"] = whatif_options()
app.include_router(make_router(models, lambda model: badges_for(model, models, date.today())))


def _form_context(error: str | None = None) -> dict:
    return {
        "languages": languages,
        "budgets": list(BudgetLevel),
        "priorities": list(Priority),
        "use_cases": USE_CASES,
        "providers": providers,
        "error": error,
        "use_modes": list(UseMode),
        "workload_types": list(WorkloadType),
        "intensities": list(Intensity),
        "cloud_providers": list(CloudProvider),
        "subscription_plans": subscriptions,
    }


def _model_profile(model) -> dict:
    return {
        "model": model,
        "best_for": best_for(model, models),
        "less_suited_for": less_suited_for(model),
        "quality_profile": quality_profile(model),
    }


def _comparison_rows(recommended, alternative) -> list[dict]:
    """Zips the two models' quality_profile() outputs into side-by-side rows."""
    return [
        {
            "label": r["label"],
            "recommended_level": r["level"],
            "recommended_ordinal": r["ordinal"],
            "alternative_level": a["level"],
            "alternative_ordinal": a["ordinal"],
            "max_ordinal": r["max_ordinal"],
        }
        for r, a in zip(quality_profile(recommended), quality_profile(alternative))
    ]


def _other_alternatives(recommendation):
    """`alternatives`, minus whatever's already shown as an also-strong option.

    also_strong_options isn't capped at MAX_ALTERNATIVES (see
    decision/explainer/explainer.py), so it frequently contains the
    same models as the top-ranked `alternatives` list -- rendering both
    sections unfiltered would show the same model twice on the page,
    once framed as "practically tied" and once as a plain alternative.
    """
    if not recommendation:
        return ()
    also_strong_ids = {opt.model.id for opt in recommendation.also_strong_options}
    return tuple(alt for alt in recommendation.alternatives if alt.model.id not in also_strong_ids)


def _exact_ties(recommendation, candidates) -> set[str]:
    """Also-strong options whose score equals the winner's. Only for these is
    the order a tie-break (dataset order); the rest scored a little lower, and
    the page must not say otherwise."""
    if not recommendation:
        return set()
    scores = {c.model.id: c.score for c in candidates}
    top = scores[recommendation.recommended.id]
    return {
        o.model.id for o in recommendation.also_strong_options if math.isclose(scores[o.model.id], top, rel_tol=1e-9)
    }


def _savings_summary(recommendation, candidates, budget_usd, priority_1) -> dict | None:
    """Whether a cheaper, still-fair-swap qualifying model exists, and how it compares.

    Always returns a dict when there's a recommendation -- silently
    omitting this when there's nothing to show left the UI unable to
    say *why*, which read as a gap rather than a (genuinely good or
    genuinely non-existent) answer. Three distinct states, per
    HANDOFF.md's "Rediseño de Budget":

    - `is_cheapest`: no qualifying model is cheaper at all, full stop.
    - `filtered_by_quality`: a cheaper model exists, but none stays
      within one quality tier of the winner on `priority_1` (see
      cheapest_qualifying_alternative's docstring) -- there IS
      something cheaper, it's just not a fair comparison, and saying
      "already the cheapest" here would be false.
    - otherwise: a fair, cheaper alternative exists -- `comparison_rows`
      carries the full side-by-side table, not just a savings percentage.
    """
    if not recommendation:
        return None

    qualifying_models = [c.model for c in candidates if c.qualifies]
    winner = recommendation.recommended
    any_cheaper_exists = any(
        m.cost.blended < winner.cost.blended for m in qualifying_models if m.id != winner.id
    )
    cheaper = cheapest_qualifying_alternative(winner, qualifying_models, priority_1)

    if not cheaper:
        return {"is_cheapest": not any_cheaper_exists, "filtered_by_quality": any_cheaper_exists}

    input_pct, output_pct = cost_savings_pct(winner, cheaper)
    summary = {
        "is_cheapest": False,
        "filtered_by_quality": False,
        "model": cheaper,
        "input_pct": round(input_pct),
        "output_pct": round(output_pct),
        "comparison_rows": _comparison_rows(winner, cheaper),
    }

    if budget_usd:
        summary["input_capacity"] = estimated_input_capacity(budget_usd, cheaper)
        summary["output_capacity"] = estimated_output_capacity(budget_usd, cheaper)

    return summary


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", _form_context())


_CONTEXT_FIELDS = ("language", "budget", "priority_1", "priority_2", "priority_3")


@app.get("/compare", response_class=HTMLResponse)
def compare(request: Request, m: list[str] = Query(default=[])):
    """Side-by-side of 2-4 models, optionally with the engine's verdict for a context.

    The context fields are optional. With none filled in this is a plain
    stored-data comparison (FEATURES.md, "Static Model Comparator"); with
    them, decision/ is run over the dataset and its result per model is
    shown first, unchanged.
    """
    selected = parse_selection(m, models)
    form = dict(request.query_params)
    context_error = None
    fit = None
    if any(form.get(field) for field in _CONTEXT_FIELDS):
        try:
            context = context_from_form(form)
        except InvalidFormError as error:
            context_error = error.message
        else:
            if len(selected) >= MIN_COMPARED:
                fit = context_fit(selected, models, context)
    budget_usd = parse_budget_usd(form.get("monthly_budget_usd"))
    ready = len(selected) >= MIN_COMPARED
    sections = None
    if ready:
        sections = build_comparison(
            selected,
            access_routes,
            fit,
            all_models=models,
            plan_names=subscription_plan_names,
            today=date.today(),
            budget_usd=budget_usd,
            form=form,
        )
    return templates.TemplateResponse(
        request,
        "compare.html",
        {
            "model_groups": group_models(models),
            "selected": selected,
            "selected_ids": [model.id for model in selected],
            "max_compared": MAX_COMPARED,
            "min_compared": MIN_COMPARED,
            "links": selection_links(selected, form, fit),
            "sections": sections,
            "counts": row_counts(sections) if sections else None,
            "fit": fit,
            "orbit": orbit(fit, selected) if fit else None,
            "podium": podium(fit, selected) if fit else None,
            "constellations": constellations(selected) if ready else None,
            "frame": constellation_frame(),
            "budget_usd": budget_usd,
            "form": form,
            "context_open": bool(context_error or any(form.get(field) for field in _CONTEXT_FIELDS)),
            "context_error": context_error,
            "languages": languages,
            "budgets": list(BudgetLevel),
            "priorities": list(Priority),
        },
    )


@app.get("/plans", response_class=HTMLResponse)
def plans(request: Request):
    """Subscription or API for one model (FEATURES.md, "Subscription vs. API
    Comparator"). decision/access/plan_compare.py decides; the model is an
    input, so nothing here touches the recommendation."""
    context = plans_context(dict(request.query_params), models, access_routes, subscriptions)
    return templates.TemplateResponse(request, "plans.html", context)


@app.get("/use-case-suggestion", response_class=JSONResponse)
def use_case_suggestion(text: str = ""):
    """Deterministic keyword suggestion for the free-text use case field.

    A read-only lookup, not a decision -- the client shows it as a
    dismissible suggestion and only pre-fills priorities if the
    developer explicitly accepts it. Priorities never come from
    decision/ here; they're the same static USE_CASES pairing the
    preset dropdown already uses.
    """
    result = match_use_case(text)
    priorities = use_case_priorities.get(result.category, ()) if result.category else ()
    return {
        "category": result.category,
        "priorities": [p.value for p in priorities],
        "tied_categories": list(result.tied_categories),
    }


@app.post("/recommend", response_class=HTMLResponse)
async def recommend(request: Request):
    """Kept for forms cached from before results had their own URL."""
    return _result_response(request, await request.form())


@app.get("/recommend", response_class=HTMLResponse)
def recommend_link(request: Request):
    """A result's own URL. The form submits by GET, so the context is in the
    query string and the same link rebuilds the same result (the engine is
    deterministic) on the current catalog. Without a context there is
    nothing to show: back to the form."""
    if not request.query_params:
        return RedirectResponse("/", status_code=303)
    return _result_response(request, request.query_params)


def _result_response(request: Request, form):
    try:
        context = context_from_form(form)
    except InvalidFormError as error:
        return templates.TemplateResponse(
            request, "index.html", _form_context(error=error.message), status_code=422
        )

    try:
        candidates = evaluate(context, models)
        recommendation = explain(context, candidates)
    except NoQualifyingModelsError:
        recommendation = None

    profile = _model_profile(recommendation.recommended) if recommendation else None

    access_context = access_context_from_form(form)
    access = (
        recommend_access(recommendation.recommended, access_context, access_routes)
        if recommendation
        else None
    )

    budget_usd = parse_budget_usd(form.get("monthly_budget_usd"))
    input_capacity = output_capacity = input_capacity_pct = output_capacity_pct = None
    if recommendation and budget_usd:
        input_capacity = estimated_input_capacity(budget_usd, recommendation.recommended)
        output_capacity = estimated_output_capacity(budget_usd, recommendation.recommended)
        input_capacity_pct, output_capacity_pct = capacity_bar_widths(input_capacity, output_capacity)

    savings = _savings_summary(recommendation, candidates, budget_usd, context.priorities[0]) if recommendation else None

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "context": context,
            "recommendation": recommendation,
            "profile": profile,
            "budget_usd": budget_usd,
            "input_capacity": input_capacity,
            "output_capacity": output_capacity,
            "input_capacity_pct": input_capacity_pct,
            "output_capacity_pct": output_capacity_pct,
            "savings": savings,
            "other_alternatives": _other_alternatives(recommendation),
            "exact_ties": _exact_ties(recommendation, candidates),
            "access": access,
            "subscription_plan_names": subscription_plan_names,
            "share_url": "/recommend?" + urlencode([(key, value) for key, value in form.multi_items() if value]),
        },
    )
