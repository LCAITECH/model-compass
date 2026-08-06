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
