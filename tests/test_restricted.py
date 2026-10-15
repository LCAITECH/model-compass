"""lifecycle.status `restricted`: still served, closed to new developers
(IMPLEMENTATION_NOTES.md, Iteration #29). The engine keeps it out of the
recommendation by attribute; the site says so without calling it deprecated."""

from datetime import date

import pytest

from decision.domain import BudgetLevel, BudgetMode, Context, Lifecycle, LifecycleStatus, Priority
from decision.evaluator import evaluate
from decision.loader import load_access_routes
from interfaces.web.catalog_notices import badges_for, catalog_notices
from interfaces.web.comparison import build_comparison
from tests.conftest import ACCESS_ROUTES_DIR

TODAY = date(2026, 10, 15)
RESTRICTED = {"gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite"}


@pytest.fixture(scope="module")
def access_routes():
    return load_access_routes(ACCESS_ROUTES_DIR)


def _context():
    return Context(
        use_case="Bot", budget_mode=BudgetMode.TIER, budget=BudgetLevel.VERY_HIGH, priorities=(Priority.COST,), language="en"
    )


def test_the_real_dataset_marks_exactly_the_gemini_2_5_models(models):
    assert {m.id for m in models if m.lifecycle.restricted} == RESTRICTED
    assert not any(m.lifecycle.deprecated for m in models if m.id in RESTRICTED)


def test_successors_follow_the_owners_per_model_pick(models):
    by_id = {m.id: m for m in models}

    assert by_id["gemini-2.5-flash-lite"].lifecycle.replacement == "gemini-3.5-flash-lite"
    assert by_id["gemini-2.5-flash"].lifecycle.replacement == "gemini-3.8-flash"
    assert by_id["gemini-2.5-pro"].lifecycle.replacement is None


def test_a_restricted_model_never_qualifies_and_says_why(make_model):
    restricted = make_model("closed", lifecycle=Lifecycle(LifecycleStatus.RESTRICTED, replacement="open"))
    open_model = make_model("open")

    by_id = {c.model.id: c for c in evaluate(_context(), [restricted, open_model])}

    assert not by_id["closed"].qualifies
    assert by_id["closed"].disqualified_reasons == (
        "limited by its provider to developers who already used it (for new projects: open)",
    )
    assert by_id["open"].qualifies


def test_the_reason_omits_a_successor_nobody_named(make_model):
    restricted = make_model("closed", lifecycle=Lifecycle(LifecycleStatus.RESTRICTED))

    [candidate] = evaluate(_context(), [restricted])

    assert candidate.disqualified_reasons == ("limited by its provider to developers who already used it",)


def test_restricted_models_get_their_own_badge_and_never_new_or_promo(models):
    by_id = {m.id: m for m in models}

    badges = badges_for(by_id["gemini-2.5-flash-lite"], models, TODAY)

    assert badges.restricted.replacement.id == "gemini-3.5-flash-lite"
    assert badges.new is None and badges.promo is None
    assert badges.retiring is None  # not leaving the catalog: Google says it keeps serving it


def test_restricted_models_are_not_listed_as_leaving_the_catalog(models):
    leaving = {notice.model.id for notice in catalog_notices(models, TODAY).retiring}

    assert not leaving & RESTRICTED


def test_the_comparator_shows_the_status_and_offers_the_successor(models, access_routes):
    by_id = {m.id: m for m in models}
    sections = build_comparison(
        [by_id["gemini-2.5-flash-lite"], by_id["claude-haiku-5-5"]], access_routes, all_models=models, today=TODAY
    )
    rows = {row["label"]: row for section in sections for row in section["rows"]}

    assert rows["Status"]["cells"][0]["text"] == "Existing users only"
    assert rows["Replacement"]["cells"][0]["action"]["label"] == "Swap in"
