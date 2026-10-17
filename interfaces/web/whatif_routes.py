"""The what-if endpoints: JSON for the result page's panel (whatif.js).

Both reuse the form parser of the normal flow, so a scenario is validated by
exactly the rules of the form, and both are GET (same input, same output).
"""

from collections.abc import Callable
from urllib.parse import parse_qsl, urlencode

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from decision.domain import AIModel
from interfaces.web.catalog_notices import Badges
from interfaces.web.context_form import InvalidFormError, context_from_form
from interfaces.web.whatif import neighbors, scenario_payload


def make_router(models: list[AIModel], badges_of: Callable[[AIModel], Badges]) -> APIRouter:
    router = APIRouter()

    def _error(message: str, status: int = 422) -> JSONResponse:
        return JSONResponse({"error": message}, status_code=status)

    @router.get("/whatif")
    def whatif(request: Request):
        """The scenario in the query string, plus `from`: the visitor's own
        query string. Returns the scenario's graph items and what changed."""
        fields = [(key, value) for key, value in request.query_params.multi_items() if key != "from" and value]
        origin = request.query_params.get("from")
        if not fields or not origin:
            return _error("Send the scenario and the context it comes from (from=...).", 400)
        try:
            context = context_from_form(dict(fields))
            base_context = context_from_form(dict(parse_qsl(origin.removeprefix("/recommend?"))))
        except InvalidFormError as error:
            return _error(error.message)
        return scenario_payload(context, base_context, models, badges_of, "/recommend?" + urlencode(fields))

    @router.get("/whatif/neighbors")
    def whatif_neighbors(request: Request):
        """The single-step changes that would give a different winner."""
        fields = [(key, value) for key, value in request.query_params.multi_items() if value]
        if not fields:
            return _error("Send the visitor's context.", 400)
        try:
            context = context_from_form(dict(fields))
        except InvalidFormError as error:
            return _error(error.message)
        return neighbors(context, models)

    return router
