"""Builds the reasoning behind an Evaluator outcome.

Takes the Candidate objects produced by decision/evaluator/ and turns
them into a Recommendation: which model, why, what's traded off by
choosing it over the alternatives, and which alternatives exist. Per
ARCHITECTURE.md, has no knowledge of how a Recommendation will later
be displayed — that's interfaces/'s job.

Unlike the Evaluator, this module is allowed to reference model names —
"never branch on a model name" (AGENTS.md) is a constraint on decision
logic, not on generating human-readable text about the models that
logic already picked.
"""

from decision.domain.ai_model import AIModel
from decision.domain.candidate import Candidate
from decision.domain.context import Context, Priority
from decision.domain.recommendation import Alternative, Exclusion, Outranked, Recommendation
from decision.explainer.errors import NoQualifyingModelsError

MAX_ALTERNATIVES = 3

# 2%: "practically tied" score gap for Also-strong-options -- see
# HANDOFF.md's threshold sensitivity audit (2026-08-11) for why 2% and
# not 1%/5%/10%. On its own it isn't sufficient (also see
# _passes_quality_floor) -- it's a necessary, not a sufficient, condition.
ALSO_STRONG_SCORE_GAP = 0.02

_QUALITY_ATTR = {
    Priority.REASONING: "reasoning",
    Priority.CODING: "coding",
    Priority.CREATIVE_WRITING: "creative_writing",
    Priority.INSTRUCTION_FOLLOWING: "instruction_following",
}

_PRIORITY_LABEL = {
    Priority.COST: "cost",
    Priority.REASONING: "reasoning",
    Priority.CODING: "coding",
    Priority.CREATIVE_WRITING: "creative writing",
    Priority.INSTRUCTION_FOLLOWING: "instruction following",
    Priority.CONTEXT_WINDOW: "context window",
}


def explain(context: Context, candidates: list[Candidate]) -> Recommendation:
    """Turns an Evaluator's Candidate list into an explainable Recommendation."""
    qualifying = [c for c in candidates if c.qualifies]
    if not qualifying:
        raise NoQualifyingModelsError(context)

    winner, *runners_up = qualifying
    qualifying_models = [c.model for c in qualifying]

    return Recommendation(
        recommended=winner.model,
        cost_tier=winner.cost_tier,
        reasons=_build_reasons(context, winner.model, qualifying_models),
        trade_offs=_trade_offs(context, winner.model, qualifying_models),
        total_qualifying=len(qualifying),
        alternatives=tuple(
            Alternative(model=c.model, rank=rank, reasons=_standout_reasons(c.model, qualifying_models))
            for rank, c in enumerate(runners_up[:MAX_ALTERNATIVES], start=2)
        ),
        also_strong_options=_also_strong_options(winner, runners_up, qualifying_models),
        outranked=tuple(
            Outranked(model=c.model, rank=rank, reasons=_outranked_reasons(context, c.model, qualifying_models))
            for rank, c in enumerate(runners_up[MAX_ALTERNATIVES:], start=MAX_ALTERNATIVES + 2)
        ),
        excluded=tuple(
            Exclusion(model=c.model, reasons=c.disqualified_reasons)
            for c in candidates
            if not c.qualifies
        ),
    )


def _build_reasons(context: Context, winner: AIModel, qualifying: list[AIModel]) -> tuple[str, ...]:
    reasons = []
    opening = _opening_reason(context)
    if opening:
        reasons.append(opening)
    reasons.extend(_priority_reason(priority, winner, qualifying) for priority in context.priorities)
    reasons.append(_language_reason(context, winner))
    return tuple(reasons)


def _opening_reason(context: Context) -> str | None:
    """A framing sentence tying the priorities back to the use case, when given.

    Still fully deterministic string formatting over Context — no model
    is asked to write this, and the same Context always produces the
    same sentence.
    """
    if not context.use_case:
        return None

    labels = [_PRIORITY_LABEL[priority] for priority in context.priorities]
    return f"Because your use case is {context.use_case}, we weighted {_join_naturally(labels)} most heavily."


def _join_naturally(items: list[str]) -> str:
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def _priority_reason(priority: Priority, winner: AIModel, qualifying: list[AIModel]) -> str:
    label = _PRIORITY_LABEL[priority]

    if priority == Priority.COST:
        if _is_cheapest(winner, qualifying):
            return "Lowest cost among the models that fit your budget"
        return (
            f"Cost fits your budget "
            f"(${winner.cost.input_per_million:g}/${winner.cost.output_per_million:g} per million tokens)"
        )

    if priority == Priority.CONTEXT_WINDOW:
        if _has_largest_context(winner, qualifying):
            return f"Largest {label} among qualifying models"
        return f"{winner.operational.context_window:,} token context window"

    attr = _QUALITY_ATTR[priority]
    level_text = getattr(winner.quality, attr).value.replace("_", " ")
    if _is_best_quality(priority, winner, qualifying):
        return f"Strongest {label} quality among qualifying models ({level_text})"
    return f"{level_text.capitalize()} {label} quality"


def _language_reason(context: Context, winner: AIModel) -> str:
    level = winner.language_quality[context.language].value.replace("_", " ")
    return f"Supports {context.language} with {level} quality"


def _dimension_gaps(model: AIModel, qualifying: list[AIModel]) -> dict[Priority, str]:
    """Every dimension `model` isn't the best qualifying option on, keyed by Priority.

    Keyed rather than a flat tuple so the two callers below can each
    reshape it differently without re-deriving which gap came from
    which dimension. Iterates `Priority` in its declared order (cost,
    then each quality dimension, then context window), so insertion
    order is deterministic.
    """
    gaps: dict[Priority, str] = {}

    for priority in Priority:
        if priority == Priority.COST and not _is_cheapest(model, qualifying):
            gaps[priority] = "Not the cheapest option among the qualifying alternatives"
        elif priority == Priority.CONTEXT_WINDOW and not _has_largest_context(model, qualifying):
            gaps[priority] = "Not the largest context window among the qualifying alternatives"
        elif priority in _QUALITY_ATTR and not _is_best_quality(priority, model, qualifying):
            label = _PRIORITY_LABEL[priority]
            gaps[priority] = f"Not the strongest {label} among the qualifying alternatives"

    return gaps


def _trade_offs(context: Context, winner: AIModel, qualifying: list[AIModel]) -> tuple[str, ...]:
    """The winner's gaps, minus whatever the user already prioritized.

    A gap on a prioritized dimension would contradict the positive
    `reasons` line already covering it (see `_build_reasons`) — e.g. if
    cost was priority #1, `reasons` already says "lowest cost", so a
    trade-off wouldn't make sense there even if it were somehow true.
    """
    gaps = _dimension_gaps(winner, qualifying)
    return tuple(text for priority, text in gaps.items() if priority not in context.priorities)


def _outranked_reasons(context: Context, model: AIModel, qualifying: list[AIModel]) -> tuple[str, ...]:
    """An outranked model's gaps, most relevant first -- nothing omitted.

    Unlike `_trade_offs`, nothing is skipped: there's no positive
    `reasons` line here to contradict, and if the user's top priority
    is cost, "not the cheapest" is exactly why this model lost —
    hiding it would hide the actual reason. Instead, the dimensions the
    user actually prioritized (in the order they ranked them) are moved
    to the front, so the template can show the 1-2 most relevant
    reasons without truncating to an arbitrary/alphabetical subset.
    """
    gaps = _dimension_gaps(model, qualifying)
    relevance_order = list(context.priorities) + [p for p in Priority if p not in context.priorities]
    return tuple(gaps[priority] for priority in relevance_order if priority in gaps)


def _standout_reasons(model: AIModel, qualifying: list[AIModel]) -> tuple[str, ...]:
    """Why you'd pick `model` over the winner — dimensions it's the best qualifying option for.

    The mirror image of _dimension_gaps: instead of "what this model
    isn't best at", this is "what this alternative is actually best at".
    Never invents a reason — a model that isn't the strongest at
    anything among the qualifying set simply gets no reasons here.
    """
    reasons = []

    if _is_cheapest(model, qualifying):
        reasons.append("Choose this if cost matters most to you — it's the cheapest qualifying option")
    if _has_largest_context(model, qualifying):
        reasons.append("Choose this if you need the largest context window")
    for priority, attr in _QUALITY_ATTR.items():
        if _is_best_quality(priority, model, qualifying):
            reasons.append(f"Choose this if {_PRIORITY_LABEL[priority]} matters most to you")

    return tuple(reasons)


def _passes_quality_floor(winner: AIModel, other: AIModel) -> bool:
    """Never more than one quality tier below the winner, on ANY of the four dimensions.

    Deliberately checks all four, not just the user's #1 priority --
    a close weighted score alone doesn't mean a fair swap. Concrete
    case from HANDOFF.md's sensitivity audit: with priority_1 =
    context_window, gpt-5-6-sol and gemini-2.5-flash-lite land within
    0.15% of each other (context_window dominates the weighting), but
    are `very_high/very_high/high/very_high` vs.
    `medium/medium/low/medium` -- an 8-tier cumulative gap. Score
    closeness alone would have called that "practically tied"; it
    isn't. Same principle already used for Lower-cost Alternative (see
    interfaces/web/affordability.py), applied here to all four
    dimensions instead of just priority_1, since Also-strong-options
    isn't scoped to one dimension the way that feature is.
    """
    return all(
        getattr(winner.quality, attr).ordinal - getattr(other.quality, attr).ordinal <= 1
        for attr in _QUALITY_ATTR.values()
    )


def _also_strong_options(
    winner: Candidate, runners_up: list[Candidate], qualifying_models: list[AIModel]
) -> tuple[Alternative, ...]:
    """Runners-up that are a practically-tied, fair swap for the winner.

    Two independent conditions, both required (HANDOFF.md, "Also
    strong options" sensitivity audit, 2026-08-11): within
    ALSO_STRONG_SCORE_GAP of the winner's score, AND passing
    _passes_quality_floor. Score closeness alone let through pairs
    that weren't really equivalent (see that function's docstring) --
    it's necessary, not sufficient.

    Not capped at MAX_ALTERNATIVES -- a genuinely tied group can be
    larger than the top-3 alternatives shown elsewhere, and capping it
    here would silently drop real ties. `runners_up` is already
    score-sorted descending, so the score gap only grows with rank --
    safe to stop at the first candidate that fails the score
    condition, since every later one would fail it too.
    """
    if winner.score <= 0:
        return ()

    also_strong = []
    for rank, candidate in enumerate(runners_up, start=2):
        gap = (winner.score - candidate.score) / winner.score
        if gap > ALSO_STRONG_SCORE_GAP + 1e-9:  # float-rounding tolerance, not a looser threshold
            break
        if not _passes_quality_floor(winner.model, candidate.model):
            continue
        also_strong.append(
            Alternative(
                model=candidate.model,
                rank=rank,
                reasons=_standout_reasons(candidate.model, qualifying_models),
            )
        )
    return tuple(also_strong)


def _is_cheapest(model: AIModel, qualifying: list[AIModel]) -> bool:
    return all(other.cost.blended >= model.cost.blended for other in qualifying)


def _has_largest_context(model: AIModel, qualifying: list[AIModel]) -> bool:
    return all(other.operational.context_window <= model.operational.context_window for other in qualifying)


def _is_best_quality(priority: Priority, model: AIModel, qualifying: list[AIModel]) -> bool:
    attr = _QUALITY_ATTR[priority]
    level = getattr(model.quality, attr).ordinal
    return all(getattr(other.quality, attr).ordinal <= level for other in qualifying)
