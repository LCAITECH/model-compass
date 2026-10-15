"""Dated facts in the dataset that stop being true on a known day.

Two kinds, both published by a provider ahead of time:
`cost.effective_until` (an introductory price ends, so `cost.*` must be
updated to `cost.reverts_to`) and `lifecycle.shutdown_date` (the model
is turned off, so its YAML and access routes must leave the dataset).

Nothing in decision/ reads the calendar -- the engine stays
deterministic, same input, same output, on any day. This module is the
alarm instead: it fails from the first day a dated fact is no longer
true, and warns during the WARNING_WINDOW_DAYS before that.
"""

import dataclasses
import warnings
from datetime import date, timedelta

from decision.domain import Cost, CostReversion, Lifecycle, LifecycleStatus

WARNING_WINDOW_DAYS = 30


def _dated_facts(models):
    """(model id, what to do, first day the stored fact is wrong)."""
    for model in models:
        if model.cost.effective_until:
            # effective_until is the last day the price holds.
            first_wrong_day = date.fromisoformat(model.cost.effective_until) + timedelta(days=1)
            yield model.id, "introductory price ended: set cost.* to cost.reverts_to", first_wrong_day
        if model.lifecycle.shutdown_date:
            first_wrong_day = date.fromisoformat(model.lifecycle.shutdown_date)
            yield model.id, "shut down by its provider: remove it and its access routes", first_wrong_day


def overdue(models, today):
    return [fact for fact in _dated_facts(models) if fact[2] <= today]


def due_soon(models, today, days=WARNING_WINDOW_DAYS):
    return [fact for fact in _dated_facts(models) if today < fact[2] <= today + timedelta(days=days)]


def _describe(facts):
    return "\n".join(f"  {model_id}: {what} (since {day})" for model_id, what, day in facts)


def test_no_dated_fact_in_the_dataset_has_passed(models):
    late = overdue(models, date.today())

    assert not late, "Dataset facts no longer true; re-verify on the provider's page and update:\n" + _describe(late)


def test_dated_facts_coming_up_are_reported_as_warnings(models):
    # Never fails: a date inside the window is still true today. The
    # warning shows up in pytest's summary, where the daily review of the
    # catalog (and anyone running the suite) sees it ahead of time.
    for model_id, what, day in due_soon(models, date.today()):
        warnings.warn(f"{model_id}: {what} on {day}", UserWarning, stacklevel=1)


def _with_dates(model, effective_until=None, shutdown_date=None):
    cost = model.cost
    if effective_until:
        cost = Cost(cost.input_per_million, cost.output_per_million, effective_until, CostReversion(2.0, 2.0))
    lifecycle = Lifecycle(LifecycleStatus.DEPRECATED, shutdown_date=shutdown_date) if shutdown_date else model.lifecycle
    return dataclasses.replace(model, cost=cost, lifecycle=lifecycle)


def test_an_introductory_price_is_overdue_the_day_after_effective_until(make_model):
    model = _with_dates(make_model("promo"), effective_until="2026-11-30")

    assert overdue([model], date(2026, 11, 30)) == []
    assert [fact[0] for fact in overdue([model], date(2026, 12, 1))] == ["promo"]


def test_a_shutdown_is_overdue_on_the_shutdown_date_itself(make_model):
    model = _with_dates(make_model("old"), shutdown_date="2026-12-11")

    assert overdue([model], date(2026, 12, 10)) == []
    assert [fact[0] for fact in overdue([model], date(2026, 12, 11))] == ["old"]


def test_due_soon_covers_only_the_window_before_the_date(make_model):
    model = _with_dates(make_model("old"), shutdown_date="2026-12-11")

    assert due_soon([model], date(2026, 11, 10)) == []  # 31 days ahead
    assert len(due_soon([model], date(2026, 11, 11))) == 1  # 30 days ahead
    assert due_soon([model], date(2026, 12, 11)) == []  # already overdue, not "soon"


def test_a_model_without_dates_never_raises_the_alarm(make_model):
    model = make_model("plain")

    assert overdue([model], date(2100, 1, 1)) == []
    assert due_soon([model], date(2100, 1, 1)) == []
