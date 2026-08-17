"""Deterministic keyword detection over the free-text use case field.

Purely a UI convenience, same tier as use_cases.py's preset pills: it
never reaches decision/, never rewrites Context.use_case, and only ever
*suggests* a priority pre-fill the developer can accept or ignore. No
LLM, no fuzzy scoring -- same free text always produces the same
suggestion (or the same lack of one), which is what keeps this honest
rather than a guess dressed up as detection.

Keyword phrases are deliberately specific (multi-word where possible)
and never repeated across categories -- a phrase shared by two
categories would force a tie every time it appears, silently defeating
the whole mechanism. Ambiguity is surfaced, never resolved by an
arbitrary pick: if two or more categories tie for the top score, no
category wins and the caller is told which ones tied.
"""

import re
from dataclasses import dataclass

# Keys must match USE_CASES labels exactly (interfaces/web/use_cases.py)
# -- that's where the corresponding Priority pair lives, kept in one
# place rather than duplicated here.
USE_CASE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Telegram / WhatsApp bot": (
        "telegram",
        "whatsapp",
        "telegram bot",
        "whatsapp bot",
        "discord bot",
        "messaging bot",
        "chatbot",
    ),
    "Customer support": (
        "customer support",
        "customer service",
        "helpdesk",
        "support ticket",
        "faq bot",
    ),
    "Python development": (
        "python development",
        "python script",
        "django",
        "flask",
        "pandas",
    ),
    "Web / app development": (
        "web app",
        "web development",
        "mobile app",
        "frontend",
        "backend",
        "react",
    ),
    "Content creation": (
        "blog post",
        "marketing copy",
        "social media post",
        "copywriting",
        "article writing",
    ),
    "Data analysis": (
        "data analysis",
        "data extraction",
        "spreadsheet",
        "data pipeline",
    ),
    "Agentic workflow": (
        "agentic",
        "autonomous agent",
        "multi-step workflow",
        "tool calling",
        "orchestration",
    ),
    "Code review": (
        "code review",
        "pull request",
        "pr review",
        "refactor",
        "linting",
    ),
    "RAG / Document Q&A": (
        "rag",
        "document q&a",
        "document qa",
        "retrieval augmented",
        "knowledge base",
        "vector search",
    ),
    "Research & summarization": (
        "research assistant",
        "literature review",
        "summarization",
        "summarize documents",
        "long document summary",
    ),
    "SQL / database work": (
        "sql",
        "sql query",
        "database schema",
        "stored procedure",
    ),
    "Test generation": (
        "unit tests",
        "test generation",
        "integration tests",
        "edge cases",
        "test coverage",
    ),
    "Technical documentation": (
        "technical documentation",
        "api docs",
        "readme",
        "docstring",
        "internal documentation",
    ),
    "Translation / localization": (
        "translation",
        "localization",
        "translate text",
        "multilingual content",
    ),
    "Crypto / trading bot": (
        "crypto",
        "trading bot",
        "crypto community",
        "crypto trading",
        "defi",
    ),
}


@dataclass(frozen=True)
class MatchResult:
    """category is the single winning label, or None if there's no
    unambiguous winner. tied_categories is only non-empty when two or
    more categories shared the top score -- lets the caller explain
    *why* nothing was suggested instead of just going quiet.
    """

    category: str | None
    tied_categories: tuple[str, ...]
    score: int


_NO_MATCH = MatchResult(category=None, tied_categories=(), score=0)


def match_use_case(text: str) -> MatchResult:
    if not text or not text.strip():
        return _NO_MATCH

    text_lower = text.lower()
    scores: dict[str, int] = {}
    for category, phrases in USE_CASE_KEYWORDS.items():
        count = sum(
            1 for phrase in phrases if re.search(rf"\b{re.escape(phrase)}\b", text_lower)
        )
        if count:
            scores[category] = count

    if not scores:
        return _NO_MATCH

    max_score = max(scores.values())
    winners = tuple(category for category, score in scores.items() if score == max_score)

    if len(winners) == 1:
        return MatchResult(category=winners[0], tied_categories=(), score=max_score)
    return MatchResult(category=None, tied_categories=winners, score=max_score)
