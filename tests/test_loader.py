from pathlib import Path

import pytest

from decision.domain import AIModel, License, QualityLevel
from decision.loader import DatasetValidationError, load_dataset, load_model_file

DATASET_DIR = Path(__file__).resolve().parents[1] / "dataset" / "models"

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
    "gemini-3.1-pro-preview",
    "deepseek-v4-pro",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gpt-5-6-sol",
    "claude-sonnet-4-5",
    "claude-opus-4-5",
}


def test_loads_all_real_models():
    models = load_dataset(DATASET_DIR)

    assert len(models) == 27
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


def test_rejects_id_filename_mismatch(tmp_path):
    content = """
id: different-id
name: Broken
provider: Test
version: "1"
license: proprietary
capabilities:
  vision: true
  audio: false
  image_generation: false
  tool_calling: true
  structured_output: true
  json_mode: true
quality:
  reasoning: high
  coding: high
  creative_writing: high
  instruction_following: high
languages: [en]
language_quality:
  en: high
operational:
  context_window: 1000
  max_output: 1000
cost:
  input_per_million: 1.0
  output_per_million: 1.0
ecosystem:
  integration_ease: high
  maturity: stable
access:
  has_free_access: false
"""
    path = tmp_path / "expected-id.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(path)

    assert "does not match filename" in str(exc_info.value)


def test_rejects_missing_required_fields(tmp_path):
    path = tmp_path / "incomplete.yaml"
    path.write_text("id: incomplete\nname: Incomplete\n", encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(path)

    assert "missing required field" in str(exc_info.value)


def test_rejects_language_quality_mismatch(tmp_path):
    content = """
id: broken
name: Broken
provider: Test
version: "1"
license: proprietary
capabilities:
  vision: true
  audio: false
  image_generation: false
  tool_calling: true
  structured_output: true
  json_mode: true
quality:
  reasoning: high
  coding: high
  creative_writing: high
  instruction_following: high
languages: [en, es]
language_quality:
  en: high
operational:
  context_window: 1000
  max_output: 1000
cost:
  input_per_million: 1.0
  output_per_million: 1.0
ecosystem:
  integration_ease: high
  maturity: stable
access:
  has_free_access: false
"""
    path = tmp_path / "broken.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(path)

    assert "language_quality missing entries" in str(exc_info.value)


def test_rejects_invalid_enum_value(tmp_path):
    content = """
id: broken
name: Broken
provider: Test
version: "1"
license: totally-free
capabilities:
  vision: true
  audio: false
  image_generation: false
  tool_calling: true
  structured_output: true
  json_mode: true
quality:
  reasoning: high
  coding: high
  creative_writing: high
  instruction_following: high
languages: [en]
language_quality:
  en: high
operational:
  context_window: 1000
  max_output: 1000
cost:
  input_per_million: 1.0
  output_per_million: 1.0
ecosystem:
  integration_ease: high
  maturity: stable
access:
  has_free_access: false
"""
    path = tmp_path / "broken.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(path)

    assert "invalid license" in str(exc_info.value)


def test_rejects_missing_access_field(tmp_path):
    content = """
id: broken
name: Broken
provider: Test
version: "1"
license: proprietary
capabilities:
  vision: true
  audio: false
  image_generation: false
  tool_calling: true
  structured_output: true
  json_mode: true
quality:
  reasoning: high
  coding: high
  creative_writing: high
  instruction_following: high
languages: [en]
language_quality:
  en: high
operational:
  context_window: 1000
  max_output: 1000
cost:
  input_per_million: 1.0
  output_per_million: 1.0
ecosystem:
  integration_ease: high
  maturity: stable
"""
    path = tmp_path / "broken.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(path)

    assert "missing required field 'access'" in str(exc_info.value)


def test_rejects_non_boolean_has_free_access(tmp_path):
    content = """
id: broken
name: Broken
provider: Test
version: "1"
license: proprietary
capabilities:
  vision: true
  audio: false
  image_generation: false
  tool_calling: true
  structured_output: true
  json_mode: true
quality:
  reasoning: high
  coding: high
  creative_writing: high
  instruction_following: high
languages: [en]
language_quality:
  en: high
operational:
  context_window: 1000
  max_output: 1000
cost:
  input_per_million: 1.0
  output_per_million: 1.0
ecosystem:
  integration_ease: high
  maturity: stable
access:
  has_free_access: "yes"
"""
    path = tmp_path / "broken.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(path)

    assert "access.has_free_access must be a boolean" in str(exc_info.value)


def _minimal_cost_yaml(cost_block: str) -> str:
    return f"""
id: broken
name: Broken
provider: Test
version: "1"
license: proprietary
capabilities:
  vision: true
  audio: false
  image_generation: false
  tool_calling: true
  structured_output: true
  json_mode: true
quality:
  reasoning: high
  coding: high
  creative_writing: high
  instruction_following: high
languages: [en]
language_quality:
  en: high
operational:
  context_window: 1000
  max_output: 1000
cost:
{cost_block}
ecosystem:
  integration_ease: high
  maturity: stable
access:
  has_free_access: false
"""


def test_rejects_effective_until_without_reverts_to(tmp_path):
    content = _minimal_cost_yaml(
        "  input_per_million: 1.0\n  output_per_million: 1.0\n  effective_until: \"2027-01-01\"\n"
    )
    path = tmp_path / "broken.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(path)

    assert "cost.effective_until and cost.reverts_to must both be present or both absent" in str(
        exc_info.value
    )


def test_rejects_reverts_to_without_effective_until(tmp_path):
    content = _minimal_cost_yaml(
        "  input_per_million: 1.0\n  output_per_million: 1.0\n"
        "  reverts_to:\n    input_per_million: 2.0\n    output_per_million: 2.0\n"
    )
    path = tmp_path / "broken.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(path)

    assert "cost.effective_until and cost.reverts_to must both be present or both absent" in str(
        exc_info.value
    )


def test_rejects_invalid_effective_until_date(tmp_path):
    content = _minimal_cost_yaml(
        "  input_per_million: 1.0\n  output_per_million: 1.0\n  effective_until: \"not-a-date\"\n"
        "  reverts_to:\n    input_per_million: 2.0\n    output_per_million: 2.0\n"
    )
    path = tmp_path / "broken.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(path)

    assert "cost.effective_until must be an ISO date string" in str(exc_info.value)
