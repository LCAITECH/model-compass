"""Maps raw HTML form data into a Context.

Parsing and validating what a browser sends is interfaces/'s job, not
decision/'s — Context itself stays a clean typed object with no idea
an HTML form exists.
"""

from decision.domain import BudgetLevel, BudgetMode, Context, Priority

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
        budget_mode = BudgetMode(form.get("budget_mode") or BudgetMode.TIER.value)
    except ValueError:
        raise InvalidFormError("Choose how you'd like to set your budget.")

    if budget_mode == BudgetMode.TIER:
        try:
            budget = BudgetLevel(form.get("budget", ""))
        except ValueError:
            raise InvalidFormError("Choose a budget.")
    else:
        # Custom Budget never filters or weighs the ranking (see
        # BudgetMode's docstring) -- there's no tier to validate here,
        # whatever the (possibly stale, hidden) tier <select> holds is
        # ignored.
        budget = None

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
        budget_mode=budget_mode,
        budget=budget,
        priorities=tuple(priorities),
        language=language,
    )
