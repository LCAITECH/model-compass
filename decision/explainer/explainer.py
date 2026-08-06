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
from decision.domain.recommendation import Exclusion, Recommendation
from decision.explainer.errors import NoQualifyingModelsError

MAX_ALTERNATIVES = 3

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
        trade_offs=_build_trade_offs(context, winner.model, qualifying_models),
        alternatives=tuple(c.model for c in runners_up[:MAX_ALTERNATIVES]),
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


def _build_trade_offs(context: Context, winner: AIModel, qualifying: list[AIModel]) -> tuple[str, ...]:
    trade_offs = []

    for priority in Priority:
        if priority in context.priorities:
            continue  # already covered by a reason; a trade-off there would contradict it.

        if priority == Priority.COST and not _is_cheapest(winner, qualifying):
            trade_offs.append("Not the cheapest option among the qualifying alternatives")
        elif priority == Priority.CONTEXT_WINDOW and not _has_largest_context(winner, qualifying):
            trade_offs.append("Not the largest context window among the qualifying alternatives")
        elif priority in _QUALITY_ATTR and not _is_best_quality(priority, winner, qualifying):
            label = _PRIORITY_LABEL[priority]
            trade_offs.append(f"Not the strongest {label} among the qualifying alternatives")

    return tuple(trade_offs)


def _is_cheapest(model: AIModel, qualifying: list[AIModel]) -> bool:
    return all(other.cost.blended >= model.cost.blended for other in qualifying)


def _has_largest_context(model: AIModel, qualifying: list[AIModel]) -> bool:
    return all(other.operational.context_window <= model.operational.context_window for other in qualifying)


def _is_best_quality(priority: Priority, model: AIModel, qualifying: list[AIModel]) -> bool:
    attr = _QUALITY_ATTR[priority]
    level = getattr(model.quality, attr).ordinal
    return all(getattr(other.quality, attr).ordinal <= level for other in qualifying)
