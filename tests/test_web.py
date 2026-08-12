from types import SimpleNamespace

from fastapi.testclient import TestClient

from decision.domain import Candidate, CostTier, Priority
from interfaces.web.app import _savings_summary, app, models

client = TestClient(app)


def _candidate(model_id: str) -> Candidate:
    model = next(m for m in models if m.id == model_id)
    return Candidate(model=model, score=1.0, cost_tier=CostTier.LOW)


def test_index_shows_the_form():
    response = client.get("/")

    assert response.status_code == 200
    assert "Get a recommendation" in response.text
    assert "es" in response.text  # a real language from the dataset made it into the <select>


def test_recommend_renders_a_recommendation_for_a_valid_context():
    response = client.post(
        "/recommend",
        data={
            "use_case": "Telegram community bot",
            "language": "es",
            "budget": "low",
            "priority_1": "cost",
        },
    )

    assert response.status_code == 200
    assert "Recommended model" in response.text
    assert "DeepSeek V4 Flash" in response.text


def test_recommend_shows_no_match_when_nothing_qualifies():
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "xx",
            "budget": "high",
            "priority_1": "cost",
        },
    )

    assert response.status_code == 200
    assert "No model in the dataset fits these constraints" in response.text


def test_recommend_confirms_when_the_winner_is_already_cheapest():
    # Budget=low leaves 6 models qualifying (see test_evaluator.py's
    # cost-tier math); deepseek wins on cost and is already the cheapest
    # of the six, so there's no honest savings to show -- the UI should
    # say so explicitly instead of just omitting the savings box.
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "es",
            "budget": "low",
            "priority_1": "cost",
        },
    )

    assert response.status_code == 200
    assert "Already the cheapest option" in response.text
    assert "You could spend less" not in response.text


def test_recommend_shows_real_savings_when_a_cheaper_option_exists():
    # Budget=high, priority=reasoning -> claude-fable-5 wins (see
    # test_evaluator.py for the reasoning-priority tie-break), but
    # deepseek-v4-flash is real and cheaper.
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "es",
            "budget": "high",
            "priority_1": "reasoning",
        },
    )

    assert response.status_code == 200
    assert "You could spend less" in response.text
    assert "Already the cheapest option" not in response.text
    assert "DeepSeek V4 Flash" in response.text


def test_free_access_chip_shown_for_low_budget_winner_with_free_access():
    # Budget=low is a fixed <=$2 cost tier now (see SCHEMA.md's Cost
    # section), not a relative tercile -- with priority=context_window,
    # gemini-2.5-flash-lite and gemini-3.1-flash-lite tie for the
    # largest context window among the five qualifying models, and
    # gemini-2.5-flash-lite wins the tie by dataset load order. It has
    # access.has_free_access=True (see docs/models/gemini-2.5-flash-lite.md).
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "en",
            "budget": "low",
            "priority_1": "context_window",
        },
    )

    assert response.status_code == 200
    assert "Gemini 2.5 Flash-Lite" in response.text
    assert "Free access also documented" in response.text
    assert (
        "https://github.com/LCAITECH/model-compass/blob/main/Docs/models/gemini-2.5-flash-lite.md#access"
        in response.text
    )


def test_free_access_chip_not_shown_above_low_budget():
    # Same winner (gemini-2.5-flash) and same has_free_access=True as
    # above, only budget differs -- isolates that the chip is
    # budget-gated, not just tied to the model.
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "en",
            "budget": "high",
            "priority_1": "context_window",
        },
    )

    assert response.status_code == 200
    assert "Gemini 2.5 Flash" in response.text
    assert "Free access also documented" not in response.text
    assert "Read access docs" not in response.text


def test_recommend_accepts_custom_budget_mode_without_a_tier():
    # budget_mode=custom never filters by cost (see BudgetMode's
    # docstring) -- claude-fable-5 ($60 blended) can win here purely on
    # reasoning, something no BudgetLevel tier below VERY_HIGH would
    # ever allow, and no "budget" field is submitted at all.
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "es",
            "budget_mode": "custom",
            "priority_1": "reasoning",
        },
    )

    assert response.status_code == 200
    assert "Claude Fable 5" in response.text


def test_recommend_ignores_a_stale_tier_value_under_custom_budget_mode():
    # If the (hidden) tier <select> still carries a leftover value from
    # before the visitor switched to Custom, it must be ignored -- Custom
    # mode is the source of truth, not whatever the tier field happens
    # to hold.
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "es",
            "budget_mode": "custom",
            "budget": "low",  # stale/leftover -- must not filter anything
            "priority_1": "reasoning",
        },
    )

    assert response.status_code == 200
    assert "Claude Fable 5" in response.text


def test_recommend_still_defaults_to_tier_mode_when_budget_mode_is_absent():
    # Backward compatible: a form submission with no budget_mode field at
    # all (e.g. a stale cached page) behaves exactly like explicit
    # budget_mode=tier -- claude-fable-5's VERY_HIGH cost tier exceeds a
    # "high" budget, so it's excluded (still listed as an excluded
    # model, just not the recommendation itself).
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "es",
            "budget": "high",
            "priority_1": "reasoning",
        },
    )

    assert response.status_code == 200
    assert "Recommended model" in response.text
    assert "claude-fable-5" not in response.text  # not present as a model id/link, i.e. not the winner
    assert "cost tier exceeds a &#39;high&#39; budget" in response.text or "cost tier exceeds a 'high' budget" in response.text


def test_savings_summary_shows_comparison_rows_for_a_fair_cheaper_alternative():
    # Budget=high, priority=reasoning: claude-opus-4-7 (very_high reasoning)
    # wins, deepseek-v4-flash (high reasoning, one tier below -- a fair
    # swap after the 2026-08-11 calibration fix) is the fair cheaper
    # alternative. See test_recommend_shows_real_savings_when_a_cheaper_option_exists
    # for the same scenario at the HTTP level; this checks the actual
    # comparison_rows payload directly.
    recommendation = SimpleNamespace(recommended=next(m for m in models if m.id == "claude-opus-4-7"))
    candidates = [_candidate("claude-opus-4-7"), _candidate("deepseek-v4-flash")]

    summary = _savings_summary(recommendation, candidates, budget_usd=None, priority_1=Priority.REASONING)

    assert summary["is_cheapest"] is False
    assert summary["filtered_by_quality"] is False
    assert summary["model"].id == "deepseek-v4-flash"
    assert len(summary["comparison_rows"]) == 4
    reasoning_row = next(r for r in summary["comparison_rows"] if r["label"] == "Reasoning")
    assert reasoning_row["recommended_level"] == "very high"
    assert reasoning_row["alternative_level"] == "high"


def test_savings_summary_reports_filtered_by_quality_when_only_unfair_alternatives_are_cheaper():
    # claude-fable-5 is the only very_high creative_writing model;
    # gemini-3.5-flash-lite is cheaper but rated low on creative_writing
    # -- three tiers below, not a fair swap. Restricting the candidate
    # pool to just these two isolates the "cheaper exists but filtered"
    # state without needing a real end-to-end query that happens to
    # produce it (none does in the current 26-model catalog).
    recommendation = SimpleNamespace(recommended=next(m for m in models if m.id == "claude-fable-5"))
    candidates = [_candidate("claude-fable-5"), _candidate("gemini-3.5-flash-lite")]

    summary = _savings_summary(recommendation, candidates, budget_usd=None, priority_1=Priority.CREATIVE_WRITING)

    assert summary["is_cheapest"] is False
    assert summary["filtered_by_quality"] is True
    assert "model" not in summary


def test_recommend_does_not_show_no_fair_swap_message_when_a_fair_option_exists():
    # Sanity check at the HTTP level: the new muted "No fair lower-cost
    # swap" state must not leak into a real query where a fair cheaper
    # alternative genuinely exists.
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "es",
            "budget_mode": "custom",
            "priority_1": "creative_writing",
        },
    )

    assert response.status_code == 200
    assert "Claude Fable 5" in response.text
    assert "No fair lower-cost swap" not in response.text


def test_recommend_rejects_tier_mode_without_a_budget():
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "es",
            "budget_mode": "tier",
            "priority_1": "cost",
        },
    )

    assert response.status_code == 422
    assert "Choose a budget" in response.text


def test_recommend_shows_also_strong_options_when_practically_tied():
    # Customer support, creative_writing#1/instruction_following#2,
    # budget=low: deepseek-v4-pro and mistral-large-3 are an exact
    # score tie (see HANDOFF.md's "cost leakage" investigation) --
    # DeepSeek wins the deterministic alphabetical tie-break, Mistral
    # should show up as an also-strong option, not silently vanish.
    response = client.post(
        "/recommend",
        data={
            "use_case": "Customer support",
            "language": "en",
            "budget": "low",
            "priority_1": "creative_writing",
            "priority_2": "instruction_following",
        },
    )

    assert response.status_code == 200
    assert "DeepSeek V4 Pro" in response.text
    assert "Also strong options" in response.text
    assert "Mistral Large 3" in response.text
    assert "practically tied" in response.text.lower()


def test_also_strong_options_are_not_duplicated_in_the_alternatives_section():
    # Same scenario as above. Mistral Large 3 must appear once (in
    # "Also strong options"), not a second time in "Alternatives".
    response = client.post(
        "/recommend",
        data={
            "use_case": "Customer support",
            "language": "en",
            "budget": "low",
            "priority_1": "creative_writing",
            "priority_2": "instruction_following",
        },
    )

    assert response.text.count("Mistral Large 3") == 1


def test_alternatives_section_is_omitted_when_every_alternative_is_also_strong():
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


def test_recommend_omits_also_strong_options_when_the_winner_is_unmatched():
    # budget=very_high, same priorities: claude-fable-5 wins outright,
    # no exact or practical tie -- no also-strong-options card, and the
    # ordinary "Alternatives" section (unfiltered) should render.
    response = client.post(
        "/recommend",
        data={
            "use_case": "Customer support",
            "language": "en",
            "budget": "very_high",
            "priority_1": "creative_writing",
            "priority_2": "instruction_following",
        },
    )

    assert response.status_code == 200
    assert "Claude Fable 5" in response.text
    assert "Also strong options" not in response.text
    assert "Claude Opus 4.7" in response.text  # a real, unfiltered alternative


def test_access_route_rows_link_to_the_curated_guide_and_flag_non_production_routes():
    # budget=high, reasoning+context_window -> gemini-2.5-pro wins (see
    # test_evaluator.py's dual-priority matrix). It has two real access
    # routes: direct-api (production_allowed=true) and ai-studio
    # (production_allowed=false) -- the only route in the sample dataset
    # exercising that branch. Each row must link to access.guide_ref
    # (ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 3.5), never bare evidence,
    # and the ai-studio row must warn it isn't for production use.
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "en",
            "budget": "high",
            "priority_1": "reasoning",
            "priority_2": "context_window",
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


def test_recommend_rejects_a_missing_priority():
    response = client.post(
        "/recommend",
        data={"use_case": "", "language": "es", "budget": "low"},
    )

    assert response.status_code == 422
    assert "Choose at least one priority" in response.text
