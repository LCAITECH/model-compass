"""A result's own URL: GET /recommend with the context rebuilds the result."""

import re

CONTEXT = {"use_case": "Customer support bot", "language": "en", "budget": "low", "priority_1": "cost"}


def _winner(html):
    return re.search(r"<h1[^>]*>([^<]+)</h1>", html).group(1)


def test_the_form_submits_by_get_so_results_have_a_url(client):
    assert '<form method="get" action="/recommend"' in client.get("/").text


def test_a_result_url_rebuilds_the_same_result_as_the_form(client):
    posted = client.post("/recommend", data=CONTEXT)
    linked = client.get("/recommend", params=CONTEXT)

    assert linked.status_code == 200
    assert _winner(linked.text) == _winner(posted.text) == "Claude Haiku 5.5"


def test_the_share_link_leaves_empty_fields_out_and_round_trips(client):
    response = client.post("/recommend", data={**CONTEXT, "priority_2": "", "monthly_budget_usd": ""})

    share_url = re.search(r'data-share-url="([^"]+)"', response.text).group(1).replace("&amp;", "&")
    assert share_url.startswith("/recommend?")
    assert "priority_2" not in share_url and "monthly_budget_usd" not in share_url
    assert _winner(client.get(share_url).text) == "Claude Haiku 5.5"


def test_access_context_survives_the_link(client):
    # Checkbox groups repeat their key in the query string; both values arrive.
    params = [*CONTEXT.items(), ("has_api_billing", "yes"), ("subscriptions", "claude-pro"), ("subscriptions", "claude-max-5x")]
    response = client.get("/recommend", params=params)

    share_url = re.search(r'data-share-url="([^"]+)"', response.text).group(1).replace("&amp;", "&")
    assert "subscriptions=claude-pro" in share_url and "subscriptions=claude-max-5x" in share_url
    assert "has_api_billing=yes" in share_url


def test_an_incomplete_result_url_returns_the_form_with_its_error(client):
    response = client.get("/recommend", params={"budget": "low", "priority_1": "cost"})

    assert response.status_code == 422
    assert '<form method="get" action="/recommend"' in response.text
