"""What renders below the recommendation: also-strong-options/alternatives
dedup, and access route rows."""

from conftest import visible_html


def test_recommend_shows_also_strong_options_when_practically_tied(client):
    # Customer support, reasoning#1/coding#2, budget=low: deepseek-v4-flash
    # and mistral-large-3 are an exact score tie (0.6667 == 0.6667).
    # Previously this scenario used deepseek-v4-pro/creative_writing --
    # the 2026-08-27 catalog refresh corrected deepseek-v4-pro's stale
    # price, pushing its $5.28 blended cost out of the "low" budget
    # tier entirely (see Docs/CHANGELOG.md), so it no longer qualifies
    # here. deepseek-v4-flash wins this pair's deterministic
    # alphabetical tie-break; mistral-large-3 should show up as an
    # also-strong option, not silently vanish.
    response = client.post(
        "/recommend",
        data={
            "use_case": "Customer support",
            "language": "en",
            "budget": "low",
            "priority_1": "reasoning",
            "priority_2": "coding",
        },
    )

    assert response.status_code == 200
    assert "DeepSeek V4.1 Flash" in response.text
    assert "Also strong options" in response.text
    assert "Mistral Large 3" in response.text
    assert "practically tied" in response.text.lower()


def test_also_strong_options_are_not_duplicated_in_the_alternatives_section(client):
    # Same scenario as above. Mistral Large 3 must appear once (in
    # "Also strong options"), not a second time in "Alternatives" --
    # even though it also holds alternative rank 2 internally.
    response = client.post(
        "/recommend",
        data={
            "use_case": "Customer support",
            "language": "en",
            "budget": "low",
            "priority_1": "reasoning",
            "priority_2": "coding",
        },
    )

    assert visible_html(response.text).count("Mistral Large 3") == 1


def test_alternatives_section_is_omitted_when_every_alternative_is_also_strong(client):
    # 2026-10-27: the old context (budget=medium, creative_writing then
    # instruction_following) stopped working when gpt-6-1-terra, rated high
    # on all four dimensions, became the outright winner there with no
    # also-strong options. The mechanism is shown now by budget=low with
    # coding as the priority: claude-haiku-5-5 wins and its top-3
    # alternatives (deepseek-v4-flash, mistral-large-3, qwen3.7-flash) are all
    # also-strong (5 also-strong in total), so they exhaust the "alternatives"
    # slots entirely and the plain "Alternatives" section should not render at
    # all -- nothing left to show there once the also-strong ones are excluded.
    response = client.post(
        "/recommend",
        data={
            "use_case": "Customer support",
            "language": "en",
            "budget": "low",
            "priority_1": "coding",
        },
    )

    assert response.status_code == 200
    assert "Claude Haiku 5.5" in response.text
    assert "Also strong options" in response.text
    assert "<h2 class=\"eyebrow section-eyebrow\">" not in response.text  # the "Alternatives" heading markup


def test_recommend_omits_also_strong_options_when_the_winner_is_unmatched(client):
    # budget=low, reasoning#1/instruction_following#2: mistral-large-3
    # wins outright, no exact or practical tie -- no also-strong-options
    # card, and the ordinary "Alternatives" section (unfiltered) should
    # render. This scenario has already been replaced twice by new
    # admissions turning the previous winner into a tie: first
    # claude-fable-5-1 (2026-09-01) tied claude-fable-5 on
    # creative_writing/instruction_following, then gemini-3.8-flash
    # (2026-09-02) tied gemini-3.7-flash on reasoning/cost. mistral-large-3
    # has no same-family sibling in this dataset, so it's a more durable
    # pick for "outright winner" going forward. 2026-10-08: claude-haiku-5-5
    # ($0.60 blended, same reasoning/instruction_following as mistral-large-3)
    # turned that into a practical tie too, so priority_2 is now cost:
    # claude-haiku-5-5 wins outright, no also-strong card. 2026-10-15:
    # qwen3.8-flash ($0.62 blended, same ratings) tied it as well, so the
    # scenario is now cost then context window, found by searching every
    # low/medium priority pair for one without a tie: gpt-6-luna wins
    # outright on its 1.05M context window, and claude-haiku-5-5,
    # qwen3.8-flash and gpt-5-6-luna are the ordinary alternatives.
    response = client.post(
        "/recommend",
        data={
            "use_case": "Customer support",
            "language": "en",
            "budget": "low",
            "priority_1": "cost",
            "priority_2": "context_window",
        },
    )

    assert response.status_code == 200
    assert "GPT-6 Luna" in response.text
    assert "Also strong options" not in response.text
    assert "Qwen3.8-Flash" in response.text  # a real, unfiltered alternative


def _also_strong_sentence(client, params) -> str:
    html = " ".join(client.get("/recommend", params=params).text.split())
    start = html.index("Also strong options")
    return html[start:html.index("</p>", start)]


def test_the_tie_break_is_named_only_for_an_exact_tie(client):
    # 2026-10-31 audit: the card always said the winner was first "because of a
    # deterministic tie-break, not because it scored higher", even when it had
    # scored higher. Reasoning only, budget=low: claude-haiku-5-5 and all its
    # also-strong options score exactly the same.
    sentence = _also_strong_sentence(client, {"language": "en", "budget": "low", "priority_1": "reasoning"})

    assert "because of a deterministic tie-break, not because it scored higher" in sentence


def test_a_winner_that_scored_higher_is_not_called_a_tie_break(client):
    # Reasoning then cost, budget=low: claude-haiku-5-5 ($0.60 blended) is
    # cheaper than its only also-strong option, qwen3.8-flash ($0.62), so it
    # scored higher, by less than 2%.
    sentence = _also_strong_sentence(
        client, {"language": "en", "budget": "low", "priority_1": "reasoning", "priority_2": "cost"}
    )

    assert "Claude Haiku 5.5 is listed first because it scored slightly higher, by less than 2%." in sentence
    assert "tie-break" not in sentence


def test_a_mixed_group_says_which_option_is_an_exact_tie(client):
    # Context window only, budget=low: gpt-5-6-luna wins; gpt-6-luna has the
    # same 1.05M window (an exact tie), gemini-3.1-flash-lite a slightly smaller
    # one (1,048,576), so a lower score.
    sentence = _also_strong_sentence(client, {"language": "en", "budget": "low", "priority_1": "context_window"})

    assert "scored slightly higher than Gemini 3.1 Flash-Lite; with GPT-6 Luna the score is exactly equal" in sentence


def test_access_route_rows_link_to_the_curated_guide_and_flag_non_production_routes(client):
    # budget=low, instruction_following -> claude-haiku-5-5 wins (re-derived
    # 2026-10-27 from a real run: with cost first, qwen3.7-flash now wins,
    # and it has a direct-API route only; before that this test used
    # cost-first, and 2026-10-15 replaced gemini-2.5-pro, which is
    # restricted and lost its AI Studio route). Haiku 5.5 has both kinds of
    # route: direct-api (production_allowed=true) and the Claude
    # subscription (production_allowed=false). Each row must link to
    # access.guide_ref (the curated Docs/access-guides/ section), never
    # bare evidence, and the subscription row must warn it isn't for
    # production use.
    response = client.post(
        "/recommend",
        data={"use_case": "", "language": "en", "budget": "low", "priority_1": "instruction_following"},
    )

    assert response.status_code == 200
    assert "Claude Haiku 5.5" in response.text
    assert "How to access" in response.text
    assert "Docs/access-guides/anthropic.md#anthropicdirect-api" in response.text
    assert "Docs/access-guides/anthropic.md#anthropicclaude-subscription" in response.text
    assert "Not allowed for production use per official docs." in response.text
    # Free-text dataset fields render in English (no i18n system; an
    # earlier route caveat once shipped in Spanish).
    assert "can select Haiku 5.5 on Claude.ai" in response.text
