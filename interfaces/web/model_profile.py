"""A quick "what is this model good at" summary, independent of context.

Unlike decision/explainer/'s reasons (which explain a recommendation
for a specific Context), this is a static profile of the model itself
-- so it lives here in interfaces/web/, not in decision/explainer/.
Derived only from AIModel's own fields; nothing here is stored or
invented.
"""

from decision.domain import AIModel, QualityLevel

_QUALITY_LABELS = {
    "reasoning": "Reasoning",
    "coding": "Coding",
    "creative_writing": "Creative writing",
    "instruction_following": "Instruction following",
}

_CAPABILITY_LABELS = {
    "vision": "Vision",
    "audio": "Audio",
    "image_generation": "Image generation",
    "tool_calling": "Tool calling",
    "structured_output": "Structured output",
    "json_mode": "JSON mode",
}


def best_for(model: AIModel, all_models: list[AIModel]) -> list[str]:
    strengths = [
        label
        for attr, label in _QUALITY_LABELS.items()
        if getattr(model.quality, attr).ordinal >= QualityLevel.HIGH.ordinal
    ]
    strengths += [
        label for attr, label in _CAPABILITY_LABELS.items() if getattr(model.capabilities, attr)
    ]
    if _has_above_average_context(model, all_models):
        strengths.append("Long context")
    return strengths


def less_suited_for(model: AIModel) -> list[str]:
    return [
        label
        for attr, label in _QUALITY_LABELS.items()
        if getattr(model.quality, attr) == QualityLevel.LOW
    ]


def _has_above_average_context(model: AIModel, all_models: list[AIModel]) -> bool:
    average = sum(m.operational.context_window for m in all_models) / len(all_models)
    return model.operational.context_window > average
