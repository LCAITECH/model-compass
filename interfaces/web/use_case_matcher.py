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
        "telegram bots",
        "whatsapp bot",
        "whatsapp bots",
        "discord bot",
        "discord bots",
        "messaging bot",
        "messaging bots",
        "chatbot",
        "chatbots",
        "chat bot",
    ),
    "Customer support": (
        "customer support",
        "customer service",
        "helpdesk",
        "help desk",
        "support ticket",
        "support tickets",
        "faq bot",
        "support agent",
    ),
    "Python development": (
        "python development",
        "python developer",
        "python script",
        "python scripts",
        "django",
        "flask",
        "pandas",
    ),
    "Web / app development": (
        "web app",
        "web apps",
        "web development",
        "web developer",
        "mobile app",
        "mobile apps",
        "frontend",
        "backend",
        "react",
    ),
    "Content creation": (
        "blog post",
        "blog posts",
        "marketing copy",
        "social media post",
        "social media posts",
        "copywriting",
        "copywriter",
        "article writing",
    ),
    "Data analysis": (
        "data analysis",
        "data analytics",
        "data extraction",
        "spreadsheet",
        "spreadsheets",
        "data pipeline",
        "data pipelines",
    ),
    "Agentic workflow": (
        "agentic",
        "autonomous agent",
        "autonomous agents",
        "multi-step workflow",
        "multi-step workflows",
        "tool calling",
        "orchestration",
        "agent orchestration",
    ),
    "Code review": (
        "code review",
        "code reviews",
        "pull request",
        "pull requests",
        "pr review",
        "refactor",
        "refactoring",
        "linting",
    ),
    "RAG / Document Q&A": (
        "rag",
        "rag pipeline",
        "rag system",
        "document q&a",
        "document qa",
        "retrieval augmented",
        "knowledge base",
        "vector search",
        "vector database",
    ),
    "Research & summarization": (
        "research assistant",
        "literature review",
        "literature reviews",
        "summarization",
        "summarize documents",
        "text summarization",
        "long document summary",
        "long document summaries",
    ),
    "SQL / database work": (
        "sql",
        "sql query",
        "sql queries",
        "database schema",
        "database schemas",
        "stored procedure",
        "stored procedures",
        "database migration",
    ),
    "Test generation": (
        "unit tests",
        "unit testing",
        "test generation",
        "integration tests",
        "integration testing",
        "edge cases",
        "test coverage",
        "test cases",
        "test suite",
    ),
    "Technical documentation": (
        "technical documentation",
        "technical docs",
        "api docs",
        "api documentation",
        "readme",
        "readmes",
        "docstring",
        "docstrings",
        "internal documentation",
        "developer documentation",
    ),
    "Translation / localization": (
        "translation",
        "translations",
        "localization",
        "localizations",
        "translate text",
        "translating text",
        "multilingual content",
        "language translation",
    ),
    "Crypto / trading bot": (
        "crypto",
        "trading bot",
        "trading bots",
        "crypto community",
        "crypto communities",
        "crypto trading",
        "defi",
        "trading algorithm",
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
