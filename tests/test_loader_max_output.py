import pytest

from decision.loader import DatasetValidationError, load_model_file

_TEMPLATE = """
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
{max_output_line}cost:
  input_per_million: 1.0
  output_per_million: 1.0
ecosystem:
  integration_ease: high
  maturity: stable
access:
  has_free_access: false
"""


def _load(tmp_path, max_output_line):
    path = tmp_path / "broken.yaml"
    path.write_text(_TEMPLATE.format(max_output_line=max_output_line), encoding="utf-8")
    return load_model_file(path)


def test_null_max_output_means_not_published(tmp_path):
    model = _load(tmp_path, "  max_output: null\n")

    assert model.operational.max_output is None
    assert model.operational.context_window == 1000


def test_positive_max_output_still_loads(tmp_path):
    assert _load(tmp_path, "  max_output: 4096\n").operational.max_output == 4096


def test_omitted_max_output_is_rejected(tmp_path):
    with pytest.raises(DatasetValidationError) as exc_info:
        _load(tmp_path, "")

    assert "operational.max_output must be present" in str(exc_info.value)


@pytest.mark.parametrize("value", ["0", "-5", "1.5", '"big"', "true"])
def test_non_positive_or_non_integer_max_output_is_rejected(tmp_path, value):
    with pytest.raises(DatasetValidationError) as exc_info:
        _load(tmp_path, f"  max_output: {value}\n")

    assert "operational.max_output must be a positive integer or null" in str(exc_info.value)
