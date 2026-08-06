"""Maps raw HTML form data into a Context.

Parsing and validating what a browser sends is interfaces/'s job, not
decision/'s — Context itself stays a clean typed object with no idea
an HTML form exists.
"""

from decision.domain import BudgetLevel, Context, Priority

_PRIORITY_RANKS = ("priority_1", "priority_2", "priority_3")


class InvalidFormError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def context_from_form(form) -> Context:
    language = (form.get("language") or "").strip()
    if not language:
        raise InvalidFormError("Choose a language.")

    try:
        budget = BudgetLevel(form.get("budget", ""))
    except ValueError:
        raise InvalidFormError("Choose a budget.")

    priorities = []
    for field in _PRIORITY_RANKS:
        raw = (form.get(field) or "").strip()
        if not raw:
            continue
        try:
            priority = Priority(raw)
        except ValueError:
            raise InvalidFormError("Choose valid priorities.")
        if priority not in priorities:
            priorities.append(priority)

    if not priorities:
        raise InvalidFormError("Choose at least one priority.")

    return Context(
        use_case=(form.get("use_case") or "").strip(),
        budget=budget,
        priorities=tuple(priorities),
        language=language,
    )
