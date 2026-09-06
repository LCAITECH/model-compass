"""_savings_summary at the unit level, plus one HTTP sanity check that the
muted "no fair swap" state doesn't leak into a query where one exists."""

from types import SimpleNamespace

from decision.domain import Priority
from interfaces.web.app import _savings_summary, models


def test_savings_summary_shows_comparison_rows_for_a_fair_cheaper_alternative(candidate_factory):
    # Budget=high, priority=reasoning: claude-opus-4-7 (very_high reasoning)
    # wins, deepseek-v4-flash (high reasoning, one tier below -- a fair
    # swap after the 2026-08-11 calibration fix) is the fair cheaper
    # alternative. See test_recommend_shows_real_savings_when_a_cheaper_option_exists
    # (tests/test_web_budget.py) for the same scenario at the HTTP level;
    # this checks the actual comparison_rows payload directly.
    recommendation = SimpleNamespace(recommended=next(m for m in models if m.id == "claude-opus-4-7"))
    candidates = [candidate_factory("claude-opus-4-7"), candidate_factory("deepseek-v4-flash")]

    summary = _savings_summary(recommendation, candidates, budget_usd=None, priority_1=Priority.REASONING)

    assert summary["is_cheapest"] is False
    assert summary["filtered_by_quality"] is False
    assert summary["model"].id == "deepseek-v4-flash"
    assert len(summary["comparison_rows"]) == 4
    reasoning_row = next(r for r in summary["comparison_rows"] if r["label"] == "Reasoning")
    assert reasoning_row["recommended_level"] == "very high"
    assert reasoning_row["alternative_level"] == "high"


def test_savings_summary_reports_filtered_by_quality_when_only_unfair_alternatives_are_cheaper(candidate_factory):
    # claude-fable-5 is the only very_high creative_writing model;
    # gemini-3.5-flash-lite is cheaper but rated low on creative_writing
    # -- three tiers below, not a fair swap. Restricting the candidate
    # pool to just these two isolates the "cheaper exists but filtered"
    # state without needing a real end-to-end query that happens to
    # produce it (none does in the current 26-model catalog).
    recommendation = SimpleNamespace(recommended=next(m for m in models if m.id == "claude-fable-5"))
    candidates = [candidate_factory("claude-fable-5"), candidate_factory("gemini-3.5-flash-lite")]

    summary = _savings_summary(recommendation, candidates, budget_usd=None, priority_1=Priority.CREATIVE_WRITING)

    assert summary["is_cheapest"] is False
    assert summary["filtered_by_quality"] is True
    assert "model" not in summary


def test_recommend_does_not_show_no_fair_swap_message_when_a_fair_option_exists(client):
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
