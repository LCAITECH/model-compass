"""Cells for the model comparator, and the few derivations a cell may show.

Every value here is a stored field or an exact reading of one: a price, a
price ratio, a token count a typed-in dollar amount buys at a stored
price. Bars are relative to the largest value in the same row, never to
an assumed ceiling (same rule as affordability.capacity_bar_widths).
"""


def cell(text: str, **extra) -> dict:
    return {
        "text": text,
        "best": False,
        "note": None,
        "reasons": (),
        "tone": None,
        "ordinal": None,
        "max_ordinal": None,
        "flag": None,
        "bar": None,  # 0-100, relative to the largest value in the row
        "ratio": None,  # e.g. "3.2×", against the lowest value in the row
        "chips": (),  # access routes: {"label", "detail", "title", "href"}
        "action": None,  # {"label", "href"}: a link that changes the selection
        **extra,
    }


def best_flags(values: list[float | int | None], higher_is_better: bool) -> list[bool]:
    present = [v for v in values if v is not None]
    if len(set(present)) < 2:
        return [False] * len(values)
    target = max(present) if higher_is_better else min(present)
    return [v is not None and v == target for v in values]


def with_best(cells: list[dict], values, higher_is_better: bool) -> list[dict]:
    for item, best in zip(cells, best_flags(values, higher_is_better)):
        item["best"] = best
    return cells


def with_bars(cells: list[dict], values: list[float | int | None]) -> list[dict]:
    """Bar widths relative to the row's largest value; no bar where the value is missing."""
    present = [v for v in values if v is not None]
    top = max(present, default=0)
    for item, value in zip(cells, values):
        if value is not None and top > 0:
            item["bar"] = round(value / top * 100, 1)
    return cells


def with_ratios(cells: list[dict], values: list[float | None]) -> list[dict]:
    """A "3.2×" label against the lowest value in the row, on every other cell.

    An exact ratio of two stored prices: cost is linear in tokens, so it
    holds at any usage volume (see affordability.cost_savings_pct).
    """
    present = [v for v in values if v is not None and v > 0]
    if len(set(present)) < 2:
        return cells
    lowest = min(present)
    for item, value in zip(cells, values):
        if value is not None and value > lowest:
            ratio = value / lowest
            item["ratio"] = f"{ratio:.1f}×" if ratio < 10 else f"{ratio:.0f}×"
    return cells


def price(value: float) -> str:
    return f"${value:,.2f}"


def dollars(value: float) -> str:
    """A typed-in amount: "$20", or "$12.50" when it has cents."""
    return f"${value:,.0f}" if value == int(value) else f"${value:,.2f}"


def tokens(count: int) -> str:
    """12_500_000 -> "12.5M tokens". Three significant figures at most."""
    for size, suffix in ((1_000_000_000, "B"), (1_000_000, "M"), (1_000, "K")):
        if count >= size:
            value = count / size
            digits = 0 if value >= 100 else 1 if value >= 10 else 2
            return f"{value:.{digits}f}{suffix} tokens"
    return f"{count:,} tokens"
