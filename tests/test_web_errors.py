"""Error pages: HTML for browsers, the default JSON for everything else."""

from fastapi.testclient import TestClient

import interfaces.web.app as web_app

HTML = {"accept": "text/html,application/xhtml+xml"}


def test_an_unknown_url_gets_the_sites_404_page_in_a_browser(client):
    response = client.get("/no-such-page", headers=HTML)

    assert response.status_code == 404
    assert "nothing at this address" in response.text
    assert 'class="site-header"' in response.text
    assert 'href="/"' in response.text


def test_an_unknown_url_keeps_the_json_body_for_api_clients(client):
    response = client.get("/no-such-page", headers={"accept": "application/json"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_opening_the_result_url_without_a_form_goes_back_to_the_form(client):
    # A result only exists as the answer to a POST; a GET used to be a
    # bare 405 JSON body.
    response = client.get("/recommend", headers=HTML, follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_an_unhandled_error_gets_the_sites_500_page(monkeypatch):
    def broken(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(web_app, "plans_context", broken)
    response = TestClient(web_app.app, raise_server_exceptions=False).get("/plans", headers=HTML)

    assert response.status_code == 500
    assert "This page could not be built" in response.text
    assert "boom" not in response.text
