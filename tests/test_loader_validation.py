import pytest

from conftest import model_yaml
from decision.loader import DatasetValidationError, load_model_file


def _issues(path, content) -> str:
    path.write_text(content, encoding="utf-8")
    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(path)
    return str(exc_info.value)


def test_rejects_id_filename_mismatch(tmp_path):
    assert "does not match filename" in _issues(tmp_path / "expected-id.yaml", model_yaml("different-id"))


def test_rejects_missing_required_fields(tmp_path):
    assert "missing required field" in _issues(tmp_path / "incomplete.yaml", "id: incomplete\nname: Incomplete\n")


def test_rejects_language_quality_mismatch(tmp_path):
    content = model_yaml().replace("languages: [en]", "languages: [en, es]")

    assert "language_quality missing entries" in _issues(tmp_path / "broken.yaml", content)


def test_rejects_invalid_enum_value(tmp_path):
    content = model_yaml().replace("license: proprietary", "license: totally-free")

    assert "invalid license" in _issues(tmp_path / "broken.yaml", content)


def test_rejects_missing_access_field(tmp_path):
    content = model_yaml(lifecycle="").replace("access:\n  has_free_access: false\n", "")

    assert "missing required field 'access'" in _issues(tmp_path / "broken.yaml", content)


def test_rejects_non_boolean_has_free_access(tmp_path):
    content = model_yaml().replace("has_free_access: false", 'has_free_access: "yes"')

    assert "access.has_free_access must be a boolean" in _issues(tmp_path / "broken.yaml", content)


def test_rejects_effective_until_without_reverts_to(tmp_path):
    content = model_yaml(cost='  input_per_million: 1.0\n  output_per_million: 1.0\n  effective_until: "2027-01-01"\n')

    assert "cost.effective_until and cost.reverts_to must both be present or both absent" in _issues(
        tmp_path / "broken.yaml", content
    )


def test_rejects_reverts_to_without_effective_until(tmp_path):
    content = model_yaml(
        cost="  input_per_million: 1.0\n  output_per_million: 1.0\n"
        "  reverts_to:\n    input_per_million: 2.0\n    output_per_million: 2.0\n"
    )

    assert "cost.effective_until and cost.reverts_to must both be present or both absent" in _issues(
        tmp_path / "broken.yaml", content
    )


def test_rejects_invalid_effective_until_date(tmp_path):
    content = model_yaml(
        cost='  input_per_million: 1.0\n  output_per_million: 1.0\n  effective_until: "not-a-date"\n'
        "  reverts_to:\n    input_per_million: 2.0\n    output_per_million: 2.0\n"
    )

    assert "cost.effective_until must be an ISO date string" in _issues(tmp_path / "broken.yaml", content)
