from interfaces.web.use_case_matcher import USE_CASE_KEYWORDS, match_use_case
from interfaces.web.use_cases import USE_CASES

_USE_CASE_LABELS = {label for label, _ in USE_CASES}


def test_every_keyword_category_has_a_matching_use_case_preset():
    # USE_CASE_KEYWORDS piggybacks on USE_CASES for the Priority pair --
    # a typo'd or renamed label here would silently lose that mapping.
    assert set(USE_CASE_KEYWORDS) == _USE_CASE_LABELS


def test_no_keyword_phrase_is_shared_across_categories():
    # A shared phrase would force a permanent tie whenever it appears,
    # silently defeating the whole mechanism -- enforced here, not just
    # by discipline when the dict is edited.
    seen: dict[str, str] = {}
    for category, phrases in USE_CASE_KEYWORDS.items():
        for phrase in phrases:
            assert phrase not in seen, (
                f"{phrase!r} appears in both {seen.get(phrase)!r} and {category!r}"
            )
            seen[phrase] = category


def test_empty_text_has_no_suggestion():
    result = match_use_case("")
    assert result.category is None
    assert result.tied_categories == ()
    assert result.score == 0


def test_whitespace_only_text_has_no_suggestion():
    result = match_use_case("   ")
    assert result.category is None


def test_text_without_any_keyword_has_no_suggestion():
    result = match_use_case("something completely unrelated to any category")
    assert result.category is None
    assert result.tied_categories == ()


def test_clear_single_match():
    result = match_use_case("Building a telegram bot for my community")
    assert result.category == "Telegram / WhatsApp bot"
    assert result.tied_categories == ()
    assert result.score >= 1


def test_multi_keyword_match_beats_single_keyword_match():
    # "code review" scores Code review twice (a single phrase counted
    # once) -- but a text with two distinct phrases from one category
    # and one from another should still resolve to the higher scorer.
    result = match_use_case("pull request code review with linting")
    assert result.category == "Code review"


def test_real_tie_between_two_categories_yields_no_suggestion():
    # "python script" (Python development) and "data analysis" (Data
    # analysis) each score exactly 1 -- a genuine tie now that bare
    # "python" was deliberately dropped as a keyword (too generic).
    result = match_use_case("python script for data analysis")
    assert result.category is None
    assert set(result.tied_categories) == {"Python development", "Data analysis"}
    assert result.score == 1


def test_sql_database_work_match():
    result = match_use_case("optimizing a slow sql query against our database schema")
    assert result.category == "SQL / database work"


def test_rag_match():
    result = match_use_case("a rag pipeline over our internal knowledge base")
    assert result.category == "RAG / Document Q&A"


def test_translation_match():
    result = match_use_case("translation of product listings into multilingual content")
    assert result.category == "Translation / localization"


def test_word_boundary_prevents_substring_false_positive():
    # "chatbot" must not match inside an unrelated longer word.
    result = match_use_case("chatbotany research project")
    assert result.category is None
