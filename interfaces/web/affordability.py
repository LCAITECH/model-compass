"""How far a stated dollar budget goes with a given model.

Deterministic math over real dataset pricing and a number the user
typed in -- never an assumption about how many "conversations" or
"requests" that represents, since we have no honest source for what a
request costs in tokens. See IMPLEMENTATION_NOTES.md-style reasoning:
input is money (something every user actually knows), output is a
derived token capacity, not the other way around.
"""

from decision.domain import AIModel


def estimated_input_capacity(budget_usd: float, model: AIModel) -> int:
    """Input tokens `budget_usd` buys, if spent entirely on input.

    One of two independent bounds, not a joint estimate -- a single
    blended number (e.g. "assuming an even split of input/output")
    would bake in an unstated ratio assumption that doesn't hold for
    most real usage. Showing both extremes makes no assumption about
    the mix at all; real usage falls somewhere between the two.
    """
    return round((budget_usd / model.cost.input_per_million) * 1_000_000)


def estimated_output_capacity(budget_usd: float, model: AIModel) -> int:
    """Output tokens `budget_usd` buys, if spent entirely on output. See estimated_input_capacity."""
    return round((budget_usd / model.cost.output_per_million) * 1_000_000)


def capacity_bar_widths(input_capacity: int, output_capacity: int) -> tuple[int, int]:
    """Bar widths (0-100) for input/output capacity, scaled relative to each other.

    Not relative to any assumed ceiling -- there isn't one. The larger
    of the two figures gets 100, the other is scaled proportionally, so
    the bars visualize the real ratio between them (e.g. input often
    being much cheaper than output) without implying either one is
    "full" in any absolute sense.
    """
    larger = max(input_capacity, output_capacity)
    if larger == 0:
        return (0, 0)
    return (
        round(input_capacity / larger * 100),
        round(output_capacity / larger * 100),
    )


def cost_savings_pct(from_model: AIModel, to_model: AIModel) -> tuple[float, float]:
    """How much cheaper `to_model` is than `from_model`, input and output separately.

    An exact ratio of two real prices, not an estimate -- it holds
    regardless of actual usage volume, since cost is linear in tokens
    used. Kept as two figures instead of one blended percentage
    because the input/output price ratio can differ between models;
    see estimated_input_capacity's docstring for the same reasoning.
    Returns 0 for either side priced at $0 (nothing to save there).
    """
    input_pct = _pct_lower(from_model.cost.input_per_million, to_model.cost.input_per_million)
    output_pct = _pct_lower(from_model.cost.output_per_million, to_model.cost.output_per_million)
    return (input_pct, output_pct)


def _pct_lower(from_price: float, to_price: float) -> float:
    if from_price == 0:
        return 0
    return (from_price - to_price) / from_price * 100


def cheapest_qualifying_alternative(recommended: AIModel, qualifying_models: list[AIModel]) -> AIModel | None:
    """The cheapest qualifying model other than the winner, if any is actually cheaper.

    Searches every qualifying candidate, not just the capped
    Recommendation.alternatives list -- the true cheapest option might
    not be among the top-ranked runners-up shown there.
    """
    others = [m for m in qualifying_models if m.id != recommended.id]
    if not others:
        return None
    cheapest = min(others, key=lambda m: m.cost.blended)
    return cheapest if cheapest.cost.blended < recommended.cost.blended else None


def parse_budget_usd(raw: str | None) -> float | None:
    """Parses an optional form field into a positive float, or None if absent/invalid.

    Invalid input is treated the same as "not provided" -- this is a
    bonus calculator, not a required decision input, so it shouldn't
    block the rest of the recommendation over a bad number.
    """
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    return value if value > 0 else None
