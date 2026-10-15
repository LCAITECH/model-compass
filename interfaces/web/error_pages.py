"""The site's own pages for errors, instead of FastAPI's JSON bodies.

An unknown URL, a GET on the POST-only /recommend, or an unhandled
exception all answer with a JSON body by default, so a person following
an old link or reopening a result saw raw JSON. Requests that accept
HTML get a page in the site's language now; anything else (fetch()
calls such as the use-case suggestion) keeps the JSON it parses.
"""

from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

_COPY = {
    404: ("Page not found", "There's nothing at this address", "The link may be old or mistyped."),
    500: (
        "Something went wrong",
        "This page could not be built",
        "The error is on our side, not in what you sent. Try again, or start from the form.",
    ),
}
_FALLBACK = ("Request not completed", "This request could not be completed", "Start again from the form.")


def _wants_html(request: Request) -> bool:
    return "text/html" in request.headers.get("accept", "")


def install_error_pages(app: FastAPI, templates: Jinja2Templates) -> None:
    def page(request: Request, status_code: int):
        eyebrow, heading, detail = _COPY.get(status_code, _FALLBACK)
        context = {"eyebrow": eyebrow, "heading": heading, "detail": detail}
        return templates.TemplateResponse(request, "error.html", context, status_code=status_code)

    @app.get("/recommend", include_in_schema=False)
    def recommend_without_a_form():
        # A result is computed from a submitted form and has no URL of its
        # own: opening it in a new tab, sharing it or coming back to it
        # after the browser dropped the form lands here, on the form.
        return RedirectResponse("/", status_code=303)

    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):
        if not _wants_html(request):
            return await http_exception_handler(request, exc)
        return page(request, exc.status_code)

    @app.exception_handler(Exception)
    async def server_error(request: Request, exc: Exception):
        if not _wants_html(request):
            return PlainTextResponse("Internal Server Error", status_code=500)
        return page(request, 500)
