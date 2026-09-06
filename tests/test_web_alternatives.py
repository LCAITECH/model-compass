"""What renders below the recommendation: also-strong-options/alternatives
dedup, and access route rows."""


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
    assert "DeepSeek V4 Flash" in response.text
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

    assert response.text.count("Mistral Large 3") == 1


def test_alternatives_section_is_omitted_when_every_alternative_is_also_strong(client):
    # Same context at budget=medium: all 6 tied models (winner +
    # 5 also-strong) exhaust the top-3 "alternatives" slots entirely,
    # so the plain "Alternatives" section should not render at all --
    # nothing left to show there once the also-strong ones are excluded.
    response = client.post(
        "/recommend",
        data={
            "use_case": "Customer support",
            "language": "en",
            "budget": "medium",
            "priority_1": "creative_writing",
            "priority_2": "instruction_following",
        },
    )

    assert response.status_code == 200
    assert "Claude Haiku 4.5" in response.text
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
    # pick for "outright winner" going forward.
    response = client.post(
        "/recommend",
        data={
            "use_case": "Customer support",
            "language": "en",
            "budget": "low",
            "priority_1": "reasoning",
            "priority_2": "instruction_following",
        },
    )

    assert response.status_code == 200
    assert "Mistral Large 3" in response.text
    assert "Also strong options" not in response.text
    assert "DeepSeek V4 Flash" in response.text  # a real, unfiltered alternative


def test_access_route_rows_link_to_the_curated_guide_and_flag_non_production_routes(client):
    # budget=high, creative_writing+cost -> gemini-2.5-pro wins. Previously
    # reasoning+context_window produced this winner, but the 2026-08-27
    # catalog refresh corrected gpt-5-6-sol's stale $35 blended price to
    # OpenAI's live promotional $24 (see Docs/CHANGELOG.md), which now
    # both qualifies under budget=high and has the largest context
    # window (1,050,000 vs. Gemini 2.5 Pro's 1,048,576) -- so that
    # priority pair now picks gpt-5-6-sol instead. Re-verified against a
    # real run of the engine that creative_writing+cost still picks
    # gemini-2.5-pro, which has two real access routes: direct-api
    # (production_allowed=true) and ai-studio (production_allowed=false)
    # -- the only route in the sample dataset exercising that branch.
    # Each row must link to access.guide_ref
    # (ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 3.5), never bare evidence,
    # and the ai-studio row must warn it isn't for production use.
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "en",
            "budget": "high",
            "priority_1": "creative_writing",
            "priority_2": "cost",
        },
    )

    assert response.status_code == 200
    assert "Gemini 2.5 Pro" in response.text
    assert "How to access" in response.text
    assert "Docs/access-guides/google.md#googledirect-api" in response.text
    assert "Docs/access-guides/google.md#googleai-studio" in response.text
    assert "Not allowed for production use per official docs." in response.text
    # Regression: the ai-studio route's caveat used to ship in Spanish
    # ("Restricciones de Google One indican...") while the rest of the
    # page is English -- Model Compass has no i18n system and every
    # other dataset field is English-only (see dataset/models/*.yaml),
    # so free-text dataset fields must never mix languages either.
    assert "Restricciones de Google One" not in response.text
    assert "Google One" in response.text and "AI Studio access is currently limited" in response.text
