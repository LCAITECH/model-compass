"""Basic rendering, the use-case-suggestion endpoint, and top-level form validation."""


def test_index_shows_the_form(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Get a recommendation" in response.text
    assert "es" in response.text  # a real language from the dataset made it into the <select>


def test_recommend_renders_a_recommendation_for_a_valid_context(client):
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


def test_use_case_suggestion_returns_a_unique_match(client):
    response = client.get("/use-case-suggestion", params={"text": "a customer support helpdesk"})

    assert response.status_code == 200
    assert response.json() == {
        "category": "Customer support",
        "priorities": ["instruction_following", "cost"],
        "tied_categories": [],
    }


def test_use_case_suggestion_returns_tied_categories_and_no_category(client):
    response = client.get(
        "/use-case-suggestion", params={"text": "python script for data analysis"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["category"] is None
    assert body["priorities"] == []
    assert set(body["tied_categories"]) == {"Python development", "Data analysis"}


def test_use_case_suggestion_returns_nothing_for_unrelated_text(client):
    response = client.get("/use-case-suggestion", params={"text": "lorem ipsum dolor"})

    assert response.status_code == 200
    assert response.json() == {"category": None, "priorities": [], "tied_categories": []}


def test_recommend_rejects_tier_mode_without_a_budget(client):
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


def test_recommend_rejects_a_missing_priority(client):
    response = client.post(
        "/recommend",
        data={"use_case": "", "language": "es", "budget": "low"},
    )

    assert response.status_code == 422
    assert "Choose at least one priority" in response.text
