"""/plans ("Subscription or API?"): the page, its form handling, and the
rule that a plan's limit is never shown in tokens."""

import re

from interfaces.web.plans_view import parse_usage

OPUS = "claude-opus-5-5"
NO_PLAN = "deepseek-v4-pro"


def _fog(html: str) -> str:
    """The plan's limit block: everything it says about the limit."""
    match = re.search(r'<div class="fog[^"]*">(.*?)</div>', html, re.S)
    assert match, "no fog block on the page"
    return match.group(1)


def test_plans_page_without_a_model_shows_only_the_form(client):
    response = client.get("/plans")

    assert response.status_code == 200
    assert "How should you pay for it?" in response.text
    assert 'class="paths' not in response.text


def test_a_model_with_plans_shows_both_paths_and_no_cost_verdict(client):
    response = client.get("/plans", params={"model": OPUS})

    assert response.status_code == 200
    assert "Claude Pro" in response.text and "Claude Max 20x" in response.text
    assert "Add your monthly usage to compare costs" in response.text
    assert 'value="20.00"' in response.text  # the cheapest plan's list price, prefilled
    assert "5.00M tokens" in response.text  # $20 / $4 per 1M input, the API side


def test_the_plan_limit_is_never_given_in_tokens(client):
    fog = _fog(client.get("/plans", params={"model": OPUS, "plan": "claude-max-20x"}).text)

    assert "not published in tokens" in fog
    assert not re.search(r"\d[\d.,]*\s*[KMB]?\s*tokens", fog)
    assert "20× Claude Pro (usage per 5-hour session) for 10.0× its price" in fog


def test_included_api_credits_are_shown_with_what_they_buy(client):
    response = client.get("/plans", params={"model": OPUS, "plan": "claude-max-5x"})

    assert "Includes $100/month of API credits" in response.text
    assert "25.0M tokens of input" in response.text  # $100 / $4 per 1M


def test_usage_gives_an_exact_cost_verdict(client):
    response = client.get("/plans", params={"model": OPUS, "input_m": "1", "output_m": "0.5"})

    assert "The API costs less for your usage" in response.text
    assert "Your usage costs $14 a month on the API, $6 less than Claude Pro at $20." in response.text


def test_building_on_the_model_points_to_the_api(client):
    response = client.get("/plans", params={"model": OPUS, "use": "api_integration"})

    assert "Use the API" in response.text
    assert "monthly API credits for it" in response.text  # Max plans include them


def test_a_model_no_plan_names_says_so(client):
    response = client.get("/plans", params={"model": NO_PLAN})

    assert "The API is the way in" in response.text
    assert "No plan names DeepSeek" in response.text
    assert "Not documented is not the same as unavailable" in response.text


def test_an_amount_filled_in_for_another_plan_is_ignored(client):
    response = client.get(
        "/plans", params={"model": OPUS, "plan": "claude-max-5x", "monthly_usd": "20", "amount_for": "claude-pro"}
    )

    assert 'value="100.00"' in response.text


def test_the_developer_can_type_what_they_actually_pay(client):
    response = client.get(
        "/plans", params={"model": OPUS, "plan": "claude-pro", "monthly_usd": "25", "amount_for": "claude-pro"}
    )

    assert 'value="25.00"' in response.text
    assert "$25 a month on the API" in response.text


def test_parse_usage_reads_millions_and_ignores_blanks():
    assert parse_usage({}) is None
    usage = parse_usage({"input_m": "2.5", "output_m": ""})
    assert (usage.input_tokens, usage.output_tokens) == (2_500_000, 0)
    assert parse_usage({"input_m": "-1"}) is None


def test_the_site_links_to_the_plans_page(client):
    assert 'href="/plans"' in client.get("/").text
    response = client.post(
        "/recommend",
        data={"use_case": "Coding agent", "language": "en", "budget": "very_high", "priority_1": "coding"},
    )
    assert "/plans?model=" in response.text
