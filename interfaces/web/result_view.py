"""What the result page shows around the engine's answer: the winner's
profile, the alternatives not already listed as also-strong, which ties are
exact, and the lower-cost comparison.

Presentation only, like plans_view.py: everything here reads decision/'s
Recommendation and Candidates and never ranks anything itself.
"""

import math

from interfaces.web.affordability import (
    cheapest_qualifying_alternative,
    cost_savings_pct,
    estimated_input_capacity,
    estimated_output_capacity,
)
from interfaces.web.model_profile import best_for, less_suited_for, quality_profile


def model_profile(model, models) -> dict:
    return {
        "model": model,
        "best_for": best_for(model, models),
        "less_suited_for": less_suited_for(model),
        "quality_profile": quality_profile(model),
    }


def comparison_rows(recommended, alternative) -> list[dict]:
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


def other_alternatives(recommendation):
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


def exact_ties(recommendation, candidates) -> set[str]:
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


def savings_summary(recommendation, candidates, budget_usd, priority_1) -> dict | None:
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
        "comparison_rows": comparison_rows(winner, cheaper),
    }

    if budget_usd:
        summary["input_capacity"] = estimated_input_capacity(budget_usd, cheaper)
        summary["output_capacity"] = estimated_output_capacity(budget_usd, cheaper)

    return summary


def _times(ratio: float) -> str:
    if ratio >= 10:
        return f"{ratio:.0f}×"
    return f"{ratio:.2f}×" if ratio < 0.1 else f"{ratio:.1f}×"


def price_ratio(model, winner) -> str | None:
    """`model`'s input and output prices as multiples of the winner's, e.g.
    "3.3× / 3.8×". Two figures, never one blended ratio: that would assume an
    input/output mix nobody stated (affordability.py). None when the prices
    are equal or the winner's is $0 (no ratio to state)."""
    a, b = model.cost, winner.cost
    if not b.input_per_million or not b.output_per_million:
        return None
    if (a.input_per_million, a.output_per_million) == (b.input_per_million, b.output_per_million):
        return None
    return f"{_times(a.input_per_million / b.input_per_million)} / {_times(a.output_per_million / b.output_per_million)}"
