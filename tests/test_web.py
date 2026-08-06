from fastapi.testclient import TestClient

from interfaces.web.app import app

client = TestClient(app)


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


def test_recommend_rejects_a_missing_priority():
    response = client.post(
        "/recommend",
        data={"use_case": "", "language": "es", "budget": "low"},
    )

    assert response.status_code == 422
    assert "Choose at least one priority" in response.text
