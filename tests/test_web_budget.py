"""HTTP-level behavior of budget_mode (tier/custom/stale/default), the free-access
chip, and the introductory-price reversion note -- all budget-tier-gated display."""


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
    assert "DeepSeek V4 Flash" in response.text


def test_free_access_chip_shown_for_low_budget_winner_with_free_access(client):
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


def test_free_access_chip_not_shown_above_low_budget(client):
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
    assert "Introductory price, in effect until 2026-12-31" in response.text
    assert "$1.50 input" in response.text
    assert "$7.50 output" in response.text


def test_pricing_omits_reversion_note_for_models_without_one(client):
    # Same free-access-chip winner as the tests above (gemini-2.5-flash-lite),
    # which has no cost.effective_until -- the note must not appear.
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
    assert "claude-fable-5" not in response.text  # not present as a model id/link, i.e. not the winner
    assert "cost tier exceeds a &#39;high&#39; budget" in response.text or "cost tier exceeds a 'high' budget" in response.text
