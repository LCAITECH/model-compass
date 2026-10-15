"""Dated catalog facts turned into notices: new releases, introductory
prices, and models leaving the catalog.

Every fact comes from a model's own fields (lifecycle.*, cost.effective_until,
cost.reverts_to), each sourced from the provider's page. The only thing
computed here is calendar arithmetic against today's date, which is why
this lives in interfaces/ and not in decision/: the engine never reads the
calendar, a page may. No percentages or progress bars either -- "days
left" is a real date difference, a bar would need a total nobody publishes.
"""

from dataclasses import dataclass
from datetime import date, timedelta

from decision.domain import AIModel

# "New" is a presentation rule over a sourced release date, not a quality
# signal: the engine never ranks on it.
NEW_WINDOW_DAYS = 30


@dataclass(frozen=True)
class NewRelease:
    model: AIModel
    release_date: str
    days_ago: int


@dataclass(frozen=True)
class Promo:
    model: AIModel
    ends: str  # last day the introductory price holds
    reverts_on: str
    days_left: int  # 0 on the last day
    now: tuple[float, float]
    then: tuple[float, float]


@dataclass(frozen=True)
class Retiring:
    model: AIModel
    deprecated: bool
    shutdown_date: str | None
    days_left: int | None
    replacement: AIModel | None


@dataclass(frozen=True)
class Badges:
    new: NewRelease | None
    promo: Promo | None
    retiring: Retiring | None

    def __bool__(self) -> bool:
        return bool(self.new or self.promo or self.retiring)


@dataclass(frozen=True)
class CatalogNotices:
    new: tuple[NewRelease, ...]
    promos: tuple[Promo, ...]
    retiring: tuple[Retiring, ...]

    def __bool__(self) -> bool:
        return bool(self.new or self.promos or self.retiring)


def _new_release(model: AIModel, today: date) -> NewRelease | None:
    if not model.lifecycle.release_date or model.lifecycle.deprecated:
        return None
    days_ago = (today - date.fromisoformat(model.lifecycle.release_date)).days
    if 0 <= days_ago <= NEW_WINDOW_DAYS:
        return NewRelease(model, model.lifecycle.release_date, days_ago)
    return None


def _promo(model: AIModel, today: date) -> Promo | None:
    cost = model.cost
    if not cost.effective_until or model.lifecycle.deprecated:
        # A deprecated model is never recommended; its promo is not an offer.
        return None
    ends = date.fromisoformat(cost.effective_until)
    days_left = (ends - today).days
    if days_left < 0:
        # Already over: the stored price is stale and tests/test_catalog_dates.py
        # fails until it is fixed. Showing an expired promo would mislead.
        return None
    return Promo(
        model=model,
        ends=cost.effective_until,
        reverts_on=(ends + timedelta(days=1)).isoformat(),
        days_left=days_left,
        now=(cost.input_per_million, cost.output_per_million),
        then=(cost.reverts_to.input_per_million, cost.reverts_to.output_per_million),
    )


def _retiring(model: AIModel, by_id: dict[str, AIModel], today: date) -> Retiring | None:
    lifecycle = model.lifecycle
    if not lifecycle.deprecated and not lifecycle.shutdown_date:
        return None
    days_left = None
    if lifecycle.shutdown_date:
        days_left = (date.fromisoformat(lifecycle.shutdown_date) - today).days
        if days_left <= 0:
            # Off from the shutdown date itself (the same day
            # tests/test_catalog_dates.py starts failing): the entry must go.
            return None
    return Retiring(
        model=model,
        deprecated=lifecycle.deprecated,
        shutdown_date=lifecycle.shutdown_date,
        days_left=days_left,
        replacement=by_id.get(lifecycle.replacement) if lifecycle.replacement else None,
    )


def badges_for(model: AIModel, models: list[AIModel], today: date) -> Badges:
    by_id = {m.id: m for m in models}
    return Badges(_new_release(model, today), _promo(model, today), _retiring(model, by_id, today))


def catalog_notices(models: list[AIModel], today: date) -> CatalogNotices:
    by_id = {m.id: m for m in models}
    new = [n for n in (_new_release(m, today) for m in models) if n]
    promos = [p for p in (_promo(m, today) for m in models) if p]
    retiring = [r for r in (_retiring(m, by_id, today) for m in models) if r]
    return CatalogNotices(
        new=tuple(sorted(new, key=lambda n: (n.days_ago, n.model.name))),
        promos=tuple(sorted(promos, key=lambda p: (p.days_left, p.model.name))),
        # Soonest shutdown first; deprecated models without a date (already
        # routed to a successor) after the dated ones.
        retiring=tuple(sorted(retiring, key=lambda r: (r.days_left is None, r.days_left or 0, r.model.name))),
    )


def short_date(iso: str) -> str:
    """'2026-11-30' -> 'Nov 30, 2026' (portable: no %-d on Windows)."""
    day = date.fromisoformat(iso)
    return f"{day:%b} {day.day}, {day.year}"
