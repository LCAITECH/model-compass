"""HTTP-level behavior of budget_mode (tier/custom/stale/default), the free-access
chip, and the introductory-price reversion note -- all budget-tier-gated display."""

from dataclasses import replace

from conftest import visible_html
from decision.domain import Access, BudgetLevel, BudgetMode, Context, Priority
from decision.evaluator import evaluate
from decision.explainer import explain
from interfaces.web.app import templates


def _pricing_card(models, budget: BudgetLevel, *, free_access: bool) -> tuple[str, str]:
    """The real cost-first recommendation, rendered through _result_pricing.html,
    with only its model's has_free_access flag set as given.

    Since 2026-10-15 no active model with free access wins, or reaches the
    top alternatives, under budget=low: the only one in that price band,
    gemini-3.1-flash-lite, always ranks lower. The chip's rule still needs
    a test, so the flag is set on the real winner instead of pretending a
    context exists where such a model wins.
    """
    context = Context(use_case="", budget_mode=BudgetMode.TIER, budget=budget, priorities=(Priority.COST,), language="en")
    recommendation = explain(context, evaluate(context, models))
    winner = replace(recommendation.recommended, access=Access(has_free_access=free_access))
    html = templates.env.get_template("_result_pricing.html").render(
        recommendation=replace(recommendation, recommended=winner), context=context
    )
    return winner.id, html


def test_recommend_shows_no_match_when_nothing_qualifies(client):
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


def test_recommend_confirms_when_the_winner_is_already_cheapest(client):
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


def test_recommend_shows_real_savings_when_a_cheaper_option_exists(client):
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
    assert "DeepSeek V4.1 Flash" in response.text


def test_free_access_chip_shown_for_low_budget_winner_with_free_access(models):
    winner_id, html = _pricing_card(models, BudgetLevel.LOW, free_access=True)

    assert "Free access also documented" in html
    assert f"https://github.com/LCAITECH/model-compass/blob/main/Docs/models/{winner_id}.md#access" in html


def test_free_access_chip_not_shown_above_low_budget(models):
    # Same flagged winner, only the budget differs: the chip is
    # budget-gated, not just tied to the model.
    _, html = _pricing_card(models, BudgetLevel.HIGH, free_access=True)

    assert "Free access also documented" not in html
    assert "Read access docs" not in html


def test_free_access_chip_shown_for_the_real_low_budget_winner(client):
    # The real page today: claude-haiku-5-5 wins under budget=low with
    # instruction following first, and Claude.ai's Free plan reaches it
    # (has_free_access counts a free consumer plan since Iteration #32), so
    # the chip shows and links to the Access notes that say it is the app.
    # 2026-10-27: it used to win cost-first too; qwen3.7-flash ($0.16
    # blended, no free access) now does, so the cost-first page must not show
    # the chip.
    response = client.post(
        "/recommend",
        data={"use_case": "", "language": "en", "budget": "low", "priority_1": "instruction_following"},
    )

    assert response.status_code == 200
    assert "Claude Haiku 5.5" in response.text
    assert "Free access also documented" in response.text
    assert "Docs/models/claude-haiku-5-5.md#access" in response.text

    cost_first = client.post(
        "/recommend",
        data={"use_case": "", "language": "en", "budget": "low", "priority_1": "cost"},
    )

    assert "Qwen3.7-Flash" in cost_first.text
    assert "Free access also documented" not in cost_first.text


def test_pricing_shows_introductory_price_reversion_note(client):
    # budget=medium, priority_1=reasoning, priority_2=context_window ->
    # gemini-3.7-flash wins (verified against a real evaluate()/
    # explain() run, not guessed). It has cost.effective_until set
    # (see dataset/models/gemini-3.7-flash.yaml), so the Pricing card
    # should surface the reversion date and post-reversion price.
    response = client.post(
        "/recommend",
        data={
            "use_case": "",
            "language": "en",
            "budget": "medium",
            "priority_1": "reasoning",
            "priority_2": "context_window",
        },
    )

    assert response.status_code == 200
    assert "Gemini 3.7 Flash" in response.text
    assert "Introductory price, in effect until Dec 31, 2026" in response.text  # short_date since 2026-10-31
    assert "$1.50 input" in response.text
    assert "$7.50 output" in response.text


def test_pricing_omits_reversion_note_for_models_without_one(client):
    # budget=low, context_window -> gpt-5-6-luna (re-derived 2026-10-15 from
    # a real run), which has no cost.effective_until -- the note must not appear.
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
    assert "Introductory price" not in response.text


def test_recommend_accepts_custom_budget_mode_without_a_tier(client):
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


def test_recommend_ignores_a_stale_tier_value_under_custom_budget_mode(client):
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


def test_recommend_still_defaults_to_tier_mode_when_budget_mode_is_absent(client):
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
    # Not present as a model id/link outside the graph's data list (which
    # carries every excluded model's id since 2026-10-15), i.e. not the winner.
    assert "claude-fable-5" not in visible_html(response.text)
    assert "cost tier exceeds a &#39;high&#39; budget" in response.text or "cost tier exceeds a 'high' budget" in response.text


def test_the_budget_tier_tooltip_states_the_engines_own_bands(client):
    # 2026-11-01: the tooltip called the tier a "monthly API budget"; it is a
    # band of blended price per million tokens. Its numbers must follow the
    # evaluator's ceilings, so this fails if either side changes alone.
    from decision.evaluator.evaluator import _COST_TIER_CEILINGS

    html = client.get("/").text
    for ceiling, tier in _COST_TIER_CEILINGS:
        assert f"{tier.name.replace('_', ' ').capitalize()} up to ${ceiling:g}" in html
    assert "monthly API budget" not in html
