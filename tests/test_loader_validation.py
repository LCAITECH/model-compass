import pytest

from decision.loader import DatasetValidationError, load_model_file


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
