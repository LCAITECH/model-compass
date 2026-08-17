"""Common use cases offered as form shortcuts.

Picking one pre-fills the priority dropdowns as a starting point — the
user can still change any of them before submitting. Context.priorities
is always exactly what ends up selected in the form; this mapping never
reaches into decision/ or changes what a submitted Context means, it
only saves a developer some clicking.
"""

from decision.domain import Priority

USE_CASES = [
    ("Telegram / WhatsApp bot", (Priority.COST, Priority.INSTRUCTION_FOLLOWING)),
    ("Customer support", (Priority.INSTRUCTION_FOLLOWING, Priority.COST)),
    ("Python development", (Priority.CODING, Priority.REASONING)),
    ("Web / app development", (Priority.CODING, Priority.INSTRUCTION_FOLLOWING)),
    ("Content creation", (Priority.CREATIVE_WRITING, Priority.COST)),
    ("Data analysis", (Priority.REASONING, Priority.CODING)),
    ("Agentic workflow", (Priority.REASONING, Priority.CODING)),
    ("Code review", (Priority.CODING, Priority.REASONING)),
    ("RAG / Document Q&A", (Priority.CONTEXT_WINDOW, Priority.REASONING)),
    ("Research & summarization", (Priority.REASONING, Priority.CONTEXT_WINDOW)),
    ("SQL / database work", (Priority.CODING, Priority.REASONING)),
    ("Test generation", (Priority.CODING, Priority.INSTRUCTION_FOLLOWING)),
    ("Technical documentation", (Priority.INSTRUCTION_FOLLOWING, Priority.CREATIVE_WRITING)),
    ("Translation / localization", (Priority.INSTRUCTION_FOLLOWING, Priority.COST)),
]
