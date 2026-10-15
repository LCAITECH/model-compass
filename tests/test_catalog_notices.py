"""Catalog notices: badges, the result dock and the landing radar.

Dates are fixed: the module computes "days left/ago" against today, so
every test pins today to 2026-10-14 (the day these facts were verified)
instead of depending on when the suite runs.
"""

import dataclasses
from datetime import date

import pytest

import interfaces.web.app as web_app
from decision.domain import Cost, CostReversion, Lifecycle, LifecycleStatus
from interfaces.web.catalog_notices import NEW_WINDOW_DAYS, badges_for, catalog_notices, short_date

TODAY = date(2026, 10, 14)


class _FixedDate(date):
    @classmethod
    def today(cls):
        return TODAY


@pytest.fixture
def pinned_today(monkeypatch):
    monkeypatch.setattr(web_app, "date", _FixedDate)


def _by_id(models, model_id):
    return next(m for m in models if m.id == model_id)


def test_argon_is_new_and_on_an_introductory_price(models):
    badges = badges_for(_by_id(models, "gemini-4-argon"), models, TODAY)

    assert badges.new.days_ago == 1
    assert (badges.promo.ends, badges.promo.reverts_on, badges.promo.days_left) == ("2026-11-30", "2026-12-01", 47)
    assert (badges.promo.now, badges.promo.then) == ((2.0, 10.0), (4.0, 20.0))
    assert badges.retiring is None


def test_new_lasts_exactly_the_window(make_model):
    model = make_model("fresh", lifecycle=Lifecycle(LifecycleStatus.ACTIVE, release_date="2026-09-14"))

    assert badges_for(model, [model], date(2026, 9, 14) + _days(NEW_WINDOW_DAYS)).new is not None
    assert badges_for(model, [model], date(2026, 9, 14) + _days(NEW_WINDOW_DAYS + 1)).new is None


def test_a_promo_disappears_once_it_has_ended(make_model):
    model = dataclasses.replace(make_model("promo"), cost=Cost(1.0, 1.0, "2026-11-30", CostReversion(2.0, 2.0)))

    assert badges_for(model, [model], date(2026, 11, 30)).promo.days_left == 0
    assert badges_for(model, [model], date(2026, 12, 1)).promo is None


def test_a_deprecated_model_shows_no_promo_or_new_badge(models):
    # gemini-3.7-flash still stores an introductory price, but it is
    # deprecated: neither its price nor its recency is an offer anymore.
    badges = badges_for(_by_id(models, "gemini-3.7-flash"), models, TODAY)

    assert badges.promo is None and badges.new is None
    assert badges.retiring.deprecated and badges.retiring.replacement.id == "gemini-3.8-flash"


def test_retiring_lists_dated_shutdowns_first_then_routed_ones(models):
    retiring = catalog_notices(models, TODAY).retiring

    assert [r.model.id for r in retiring] == [
        "claude-sonnet-4-5",  # 47 days
        "gpt-5", "gpt-5-mini", "gpt-5-nano",  # 58 days
        "gpt-4o",  # 92 days
        "gemini-3.1-flash-lite",  # 205 days, active
        "gemini-3.5-flash", "gemini-3.7-flash",  # no date: already routed
    ]
    assert retiring[0].days_left == 47 and retiring[0].replacement.name == "Claude Sonnet 5.5"
    assert not retiring[5].deprecated


def test_catalog_lists_new_releases_and_promos_soonest_first(models):
    notices = catalog_notices(models, TODAY)

    assert [n.model.id for n in notices.new][:2] == ["gemini-4-argon", "claude-haiku-5-5"]
    assert [p.model.id for p in notices.promos] == ["gpt-5-6-sol", "gemini-4-argon", "gemini-3.6-flash", "gemini-3.8-flash"]


def test_nothing_is_retiring_after_its_shutdown_date(make_model):
    model = make_model("old", lifecycle=Lifecycle(LifecycleStatus.DEPRECATED, shutdown_date="2026-12-11"))

    assert badges_for(model, [model], date(2026, 12, 10)).retiring.days_left == 1
    assert badges_for(model, [model], date(2026, 12, 11)).retiring is None


def test_short_date():
    assert short_date("2026-11-30") == "Nov 30, 2026"
    assert short_date("2027-01-04") == "Jan 4, 2027"


def test_landing_shows_the_ticker_and_the_radar(client, pinned_today):
    html = client.get("/").text

    assert "What's moving in the catalog" in html
    assert 'class="catalog-ticker"' in html
    assert "Gemini 4 Argon" in html and "47" in html


def test_result_page_dock_explains_the_winners_introductory_price(client, pinned_today):
    # Reasoning then cost under a high budget: gemini-3.8-flash wins, on
    # an introductory price through 2026-12-31.
    response = client.post(
        "/recommend",
        data={"use_case": "Agent", "language": "es", "budget": "high", "priority_1": "reasoning", "priority_2": "cost"},
    )
    html = response.text

    assert "data-notice-dock" in html
    assert "Gemini 3.8 Flash costs $0.75 / $3.75 per 1M tokens until Dec 31, 2026" in html
    assert "This ranking used today&#39;s price." in html or "This ranking used today's price." in html
    assert "7 models deprecated by their providers" in html
    assert 'data-promo="Dec 31, 2026"' in html


def test_compare_header_carries_the_badges(client, pinned_today):
    html = client.get("/compare?m=gemini-4-argon&m=gpt-5-nano").text

    assert "mc-badge-new" in html and "mc-badge-promo" in html
    assert "mc-badge-retiring is-deprecated" in html


def _days(n):
    from datetime import timedelta

    return timedelta(days=n)
