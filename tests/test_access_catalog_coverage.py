"""Coverage-shape tests for the access catalog expansion
(ACCESS_CATALOG_COVERAGE_RESEARCH_2026-08-12.md's implementation contract).

Asserts the *shape* of coverage -- every dataset model reachable through
at least one confirmed route -- not the exact route count, so this stays
meaningful as secondary-pattern routes are added on top of the base 23.
"""

from pathlib import Path

from decision.domain import EvidenceStatus
from decision.loader import load_access_routes, load_dataset

ROOT = Path(__file__).resolve().parents[1]
ACCESS_ROUTES_DIR = ROOT / "dataset" / "access_routes"
MODELS_DIR = ROOT / "dataset" / "models"


def test_every_model_has_at_least_one_confirmed_route():
    models = load_dataset(MODELS_DIR)
    routes = load_access_routes(ACCESS_ROUTES_DIR)

    confirmed_model_ids = {
        route.model_id for route in routes if route.evidence.status == EvidenceStatus.CONFIRMED
    }
    missing = {model.id for model in models} - confirmed_model_ids

    assert not missing, f"models with no confirmed access route: {sorted(missing)}"


def test_every_route_model_id_is_exact_not_a_family_placeholder():
    # Guards Definition of Done #3: model_id must be the exact dataset id,
    # never a family name standing in for several models.
    models = load_dataset(MODELS_DIR)
    known_ids = {model.id for model in models}
    routes = load_access_routes(ACCESS_ROUTES_DIR)

    for route in routes:
        assert route.model_id in known_ids, route.route_id
