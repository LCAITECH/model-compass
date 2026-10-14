import pytest

from conftest import DATASET_DIR
from decision.domain import AIModel, License, QualityLevel
from decision.loader import DatasetValidationError, load_dataset, load_model_file

EXPECTED_IDS = {
    "gemini-2.5-flash",
    "gpt-5-mini",
    "claude-sonnet-5",
    "deepseek-v4-flash",
    "mistral-large-3",
    "gpt-5",
    "gemini-2.5-pro",
    "claude-opus-5",
    "gpt-4o",
    "gpt-5-nano",
    "claude-haiku-4-5",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash-lite",
    "claude-opus-4-8",
    "claude-opus-4-7",
    "claude-opus-4-6",
    "claude-sonnet-4-6",
    "claude-fable-5",
    "claude-fable-5-1",
    "gemini-3.8-flash",
    "gemini-3.1-pro-preview",
    "deepseek-v4-pro",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gpt-5-6-sol",
    "claude-sonnet-4-5",
    "claude-opus-4-5",
    "gpt-6-astra",
    "qwen3.8-max",
    "claude-sonnet-5-5",
    "claude-opus-5-5",
    "gpt-6-1-sol",
    "gpt-6-luna",
    "gpt-5-6-terra",
    "gpt-5-6-luna",
    "claude-haiku-5-5",
}


def test_loads_all_real_models():
    models = load_dataset(DATASET_DIR)

    assert len(models) == 38  # +claude-haiku-5-5 (2026-10-08)
    assert all(isinstance(model, AIModel) for model in models)
    assert {model.id for model in models} == EXPECTED_IDS


def test_claude_sonnet_5_fields_round_trip():
    model = load_model_file(DATASET_DIR / "claude-sonnet-5.yaml")

    assert model.provider == "Anthropic"
    assert model.license == License.PROPRIETARY
    assert model.quality.reasoning == QualityLevel.VERY_HIGH
    assert model.operational.context_window == 1_000_000
    assert model.cost.input_per_million == 2.00
    assert model.access.has_free_access is False


def test_gemini_2_5_flash_has_free_access():
    model = load_model_file(DATASET_DIR / "gemini-2.5-flash.yaml")

    assert model.access.has_free_access is True


def test_gemini_3_8_flash_has_free_access():
    model = load_model_file(DATASET_DIR / "gemini-3.8-flash.yaml")

    assert model.access.has_free_access is True


def test_gemini_3_6_flash_has_introductory_price_reversion():
    model = load_model_file(DATASET_DIR / "gemini-3.6-flash.yaml")

    assert model.cost.input_per_million == 0.75
    assert model.cost.effective_until == "2026-12-31"
    assert model.cost.reverts_to.input_per_million == 1.50
    assert model.cost.reverts_to.output_per_million == 7.50


def test_claude_sonnet_5_has_no_price_reversion():
    # Most models never had an introductory price -- both fields
    # should stay None rather than defaulting to something fabricated.
    model = load_model_file(DATASET_DIR / "claude-sonnet-5.yaml")

    assert model.cost.effective_until is None
    assert model.cost.reverts_to is None


@pytest.mark.parametrize("model_id", sorted(EXPECTED_IDS))
def test_language_quality_mirrors_languages(model_id):
    model = load_model_file(DATASET_DIR / f"{model_id}.yaml")

    assert set(model.languages) == set(model.language_quality.keys())

