"""lifecycle: loading, validation, and the evaluator's deprecation filter."""

import pytest

from decision.domain import BudgetLevel, BudgetMode, Context, Lifecycle, LifecycleStatus, Priority
from decision.evaluator import evaluate
from decision.loader import DatasetValidationError, load_dataset, load_model_file

_TEMPLATE = """
id: {model_id}
name: Test
provider: Test
version: "1"
license: proprietary
capabilities:
  vision: false
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
{lifecycle}"""

_ACTIVE = "lifecycle:\n  status: active\n  release_date: null\n  shutdown_date: null\n  replacement: null\n"


def _write(directory, model_id, lifecycle):
    path = directory / f"{model_id}.yaml"
    path.write_text(_TEMPLATE.format(model_id=model_id, lifecycle=lifecycle), encoding="utf-8")
    return path


def _issues(tmp_path, lifecycle):
    with pytest.raises(DatasetValidationError) as exc_info:
        load_model_file(_write(tmp_path, "broken", lifecycle))
    return str(exc_info.value)


def test_deprecated_lifecycle_loads_with_date_and_replacement(tmp_path):
    lifecycle = 'lifecycle:\n  status: deprecated\n  release_date: null\n  shutdown_date: "2026-12-11"\n  replacement: successor\n'

    model = load_model_file(_write(tmp_path, "old", lifecycle))

    assert model.lifecycle == Lifecycle(LifecycleStatus.DEPRECATED, "2026-12-11", "successor")
    assert model.lifecycle.deprecated


def test_missing_lifecycle_is_rejected(tmp_path):
    assert "missing required field 'lifecycle'" in _issues(tmp_path, "")


def test_every_lifecycle_key_is_required_even_when_null(tmp_path):
    message = _issues(tmp_path, "lifecycle:\n  status: active\n")

    assert "lifecycle.shutdown_date must be present" in message
    assert "lifecycle.replacement must be present" in message


@pytest.mark.parametrize("status", ["legacy", "retired", "null"])
def test_unknown_status_is_rejected(tmp_path, status):
    lifecycle = f"lifecycle:\n  status: {status}\n  release_date: null\n  shutdown_date: null\n  replacement: null\n"

    assert "invalid lifecycle.status" in _issues(tmp_path, lifecycle)


@pytest.mark.parametrize("value", ["2026-12-11", '"next year"', '"2026-13-01"'])
def test_shutdown_date_must_be_a_quoted_iso_date(tmp_path, value):
    # An unquoted 2026-12-11 is parsed by YAML as a date object, not the
    # string every other date field in the dataset uses.
    lifecycle = f"lifecycle:\n  status: deprecated\n  release_date: null\n  shutdown_date: {value}\n  replacement: null\n"

    assert "lifecycle.shutdown_date must be an ISO date string" in _issues(tmp_path, lifecycle)


def test_release_date_must_be_a_quoted_iso_date(tmp_path):
    lifecycle = 'lifecycle:\n  status: active\n  release_date: "soon"\n  shutdown_date: null\n  replacement: null\n'

    assert "lifecycle.release_date must be an ISO date string" in _issues(tmp_path, lifecycle)


def test_release_date_must_come_before_the_shutdown_date(tmp_path):
    lifecycle = (
        'lifecycle:\n  status: deprecated\n  release_date: "2026-12-11"\n'
        '  shutdown_date: "2026-12-11"\n  replacement: null\n'
    )

    assert "release_date must be before lifecycle.shutdown_date" in _issues(tmp_path, lifecycle)


def test_a_model_cannot_replace_itself(tmp_path):
    lifecycle = "lifecycle:\n  status: deprecated\n  release_date: null\n  shutdown_date: null\n  replacement: broken\n"

    assert "cannot be the model itself" in _issues(tmp_path, lifecycle)


def test_replacement_must_be_a_model_in_the_dataset(tmp_path):
    _write(tmp_path, "active-one", _ACTIVE)
    _write(tmp_path, "old", "lifecycle:\n  status: deprecated\n  release_date: null\n  shutdown_date: null\n  replacement: missing\n")

    with pytest.raises(DatasetValidationError) as exc_info:
        load_dataset(tmp_path)

    assert "lifecycle.replacement 'missing' is not a model in the dataset" in str(exc_info.value)


def test_replacement_present_in_the_dataset_loads(tmp_path):
    _write(tmp_path, "active-one", _ACTIVE)
    _write(tmp_path, "old", "lifecycle:\n  status: deprecated\n  release_date: null\n  shutdown_date: null\n  replacement: active-one\n")

    assert {m.id for m in load_dataset(tmp_path)} == {"active-one", "old"}


def _context(budget=BudgetLevel.VERY_HIGH):
    return Context(
        use_case="Bot", budget_mode=BudgetMode.TIER, budget=budget, priorities=(Priority.COST,), language="en"
    )


def test_a_deprecated_model_never_qualifies_even_when_it_fits_otherwise(make_model):
    old = make_model(
        "old", input_per_million=0.1, output_per_million=0.1,
        lifecycle=Lifecycle(LifecycleStatus.DEPRECATED, "2026-12-11", "new"),
    )
    new = make_model("new")

    candidates = evaluate(_context(), [old, new])

    assert candidates[0].model.id == "new"
    assert candidates[1].disqualified_reasons == (
        "deprecated by its provider (shuts down 2026-12-11; replacement: new)",
    )


def test_deprecation_reason_omits_what_the_provider_did_not_publish(make_model):
    old = make_model("old", lifecycle=Lifecycle(LifecycleStatus.DEPRECATED))

    candidates = evaluate(_context(), [old, make_model("new")])

    assert candidates[1].disqualified_reasons == ("deprecated by its provider",)


def test_deprecation_is_listed_with_any_other_reason(make_model):
    old = make_model(
        "old", input_per_million=40.0, output_per_million=40.0,
        lifecycle=Lifecycle(LifecycleStatus.DEPRECATED),
    )

    candidates = evaluate(_context(BudgetLevel.LOW), [old, make_model("new")])

    assert candidates[1].disqualified_reasons == (
        "deprecated by its provider",
        "cost tier exceeds a 'low' budget",
    )


def test_the_real_dataset_marks_exactly_the_provider_deprecated_models(models):
    # Verified 2026-10-14 against each provider's own deprecations page
    # (sources in each YAML's lifecycle comment).
    deprecated = {m.id for m in models if m.lifecycle.deprecated}

    assert deprecated == {
        "claude-sonnet-4-5",
        "gemini-3.5-flash",
        "gemini-3.7-flash",
        "gpt-4o",
        "gpt-5",
        "gpt-5-mini",
        "gpt-5-nano",
    }


def test_every_replacement_in_the_real_dataset_is_an_active_model(models):
    # A successor that is itself deprecated would send the user in a
    # circle: when a replacement gets deprecated, point to its own one.
    by_id = {m.id: m for m in models}
    replacements = {m.lifecycle.replacement for m in models if m.lifecycle.replacement}

    assert replacements
    assert all(not by_id[replacement].lifecycle.deprecated for replacement in replacements)


def test_an_active_model_with_a_published_shutdown_date_still_qualifies(models):
    # gemini-3.1-flash-lite: Google publishes 2027-05-07 and names a
    # successor, but has announced no deprecation. Shown, not filtered.
    flash_lite = next(c for c in evaluate(_context(), models) if c.model.id == "gemini-3.1-flash-lite")

    assert flash_lite.model.lifecycle.shutdown_date == "2027-05-07"
    assert flash_lite.qualifies


def test_result_page_lists_deprecated_models_with_their_successor(client):
    response = client.post(
        "/recommend",
        data={"use_case": "Support bot", "language": "en", "budget": "very_high", "priority_1": "cost"},
    )

    assert response.status_code == 200
    assert "deprecated by its provider (shuts down 2026-11-30; replacement: claude-sonnet-5-5)" in response.text


def test_every_model_in_the_real_dataset_has_a_sourced_release_date(models):
    # Each one read on the provider's own page on 2026-10-14; the source
    # is cited in the YAML comment above the lifecycle block.
    assert all(m.lifecycle.release_date for m in models)
    by_id = {m.id: m.lifecycle.release_date for m in models}
    assert by_id["gemini-4-argon"] == "2026-10-13"
    assert by_id["gpt-4o"] == "2024-05-13"
