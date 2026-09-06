"""Shared fixtures and path constants for the test suite."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from decision.domain import (
    Access,
    AIModel,
    Candidate,
    Capabilities,
    Cost,
    CostTier,
    Ecosystem,
    IntegrationEase,
    License,
    Maturity,
    Operational,
    Quality,
    QualityLevel,
)
from decision.loader import load_dataset
from interfaces.web.app import app
from interfaces.web.app import models as _web_models

ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT / "dataset" / "models"
ACCESS_ROUTES_DIR = ROOT / "dataset" / "access_routes"
SUBSCRIPTIONS_DIR = ROOT / "dataset" / "subscriptions"


@pytest.fixture(scope="module")
def models():
    return load_dataset(DATASET_DIR)


@pytest.fixture
def make_model():
    """Factory for a minimal synthetic AIModel, for evaluator/explainer/affordability unit tests.

    `quality` sets all four quality dimensions at once; pass any of
    `reasoning`/`coding`/`creative_writing`/`instruction_following`
    individually to override just that one and leave the rest at `quality`.
    """

    def _make(
        id: str = "test-model",
        *,
        quality: QualityLevel = QualityLevel.LOW,
        reasoning: QualityLevel | None = None,
        coding: QualityLevel | None = None,
        creative_writing: QualityLevel | None = None,
        instruction_following: QualityLevel | None = None,
        input_per_million: float = 1.0,
        output_per_million: float = 1.0,
    ) -> AIModel:
        return AIModel(
            id=id,
            name=id,
            provider="Test",
            version="1",
            license=License.PROPRIETARY,
            capabilities=Capabilities(False, False, False, False, False, False),
            quality=Quality(
                reasoning if reasoning is not None else quality,
                coding if coding is not None else quality,
                creative_writing if creative_writing is not None else quality,
                instruction_following if instruction_following is not None else quality,
            ),
            languages=("en",),
            language_quality={"en": quality},
            operational=Operational(context_window=1000, max_output=1000),
            cost=Cost(input_per_million=input_per_million, output_per_million=output_per_million),
            ecosystem=Ecosystem(IntegrationEase.LOW, Maturity.STABLE),
            access=Access(has_free_access=False),
        )

    return _make


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture
def candidate_factory():
    """Factory for a Candidate wrapping a real model from the web app's loaded dataset."""

    def _make(model_id: str) -> Candidate:
        model = next(m for m in _web_models if m.id == model_id)
        return Candidate(model=model, score=1.0, cost_tier=CostTier.LOW)

    return _make
