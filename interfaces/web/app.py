"""FastAPI app: the web interface, and the only consumer of decision/ in the MVP.

Loads the dataset once at startup, turns a form submission into a
Context, and renders whatever decision/ returns. Has no decision logic
of its own — per ARCHITECTURE.md, decision/ would work identically if
this whole package were deleted.
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from decision.domain import BudgetLevel, Priority
from decision.evaluator import evaluate
from decision.explainer import NoQualifyingModelsError, explain
from decision.loader import load_dataset
from interfaces.web.context_form import InvalidFormError, context_from_form
from interfaces.web.languages import language_name
from interfaces.web.model_profile import best_for, less_suited_for
from interfaces.web.use_cases import USE_CASES

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR.parent.parent / "dataset" / "models"

app = FastAPI(title="Model Compass")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.filters["language_name"] = language_name

models = load_dataset(DATASET_DIR)
languages = sorted({language for model in models for language in model.languages})


def _form_context(error: str | None = None) -> dict:
    return {
        "languages": languages,
        "budgets": list(BudgetLevel),
        "priorities": list(Priority),
        "use_cases": USE_CASES,
        "error": error,
    }


def _model_profile(model) -> dict:
    return {
        "model": model,
        "best_for": best_for(model, models),
        "less_suited_for": less_suited_for(model),
    }


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", _form_context())


@app.post("/recommend", response_class=HTMLResponse)
async def recommend(request: Request):
    form = await request.form()

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

    return templates.TemplateResponse(
        request,
        "result.html",
        {"context": context, "recommendation": recommendation, "profile": profile},
    )
