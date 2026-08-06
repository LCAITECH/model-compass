"""Human-readable names for the ISO 639-1 codes used in the dataset.

A hand-written lookup rather than a dependency like pycountry — the
dataset only uses a handful of language codes, and AGENTS.md asks for
new dependencies to be flagged, not reached for by default. The ISO
code is still what's sent to the server; this only changes the label
shown to a person.
"""

LANGUAGE_NAMES = {
    "ar": "Arabic",
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "hi": "Hindi",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "nl": "Dutch",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
}


def language_name(code: str) -> str:
    return LANGUAGE_NAMES.get(code, code)
