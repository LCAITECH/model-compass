"""Errors raised while building a Recommendation."""


class NoQualifyingModelsError(Exception):
    """No model in the dataset qualifies for the given Context.

    Not a bug — a legitimate outcome when a context's constraints (a
    budget, a language) are too narrow for the current dataset. Left
    for the caller (an interface) to turn into a "no match, try
    relaxing X" message; the Explainer only knows this happened, not
    how it should be communicated.
    """

    def __init__(self, context):
        self.context = context
        super().__init__(f"no model qualifies for context: {context}")
