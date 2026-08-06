"""How far a stated dollar budget goes with a given model.

Deterministic math over real dataset pricing and a number the user
typed in -- never an assumption about how many "conversations" or
"requests" that represents, since we have no honest source for what a
request costs in tokens. See IMPLEMENTATION_NOTES.md-style reasoning:
input is money (something every user actually knows), output is a
derived token capacity, not the other way around.
"""

from decision.domain import AIModel


def estimated_token_capacity(budget_usd: float, model: AIModel) -> int:
    """Tokens `budget_usd` buys per month, assuming a roughly even mix of input/output."""
    return round((budget_usd / model.cost.blended) * 1_000_000)


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
