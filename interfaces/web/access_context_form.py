"""Maps raw HTML form data into an AccessContext.

Same split as context_form.py: parsing/defaulting belongs here, not in
decision/. Unlike the main Context form, every field here is optional --
Access Advisor is a bonus layer on top of the model recommendation, not
a second gate the developer must clear (see
Docs/ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 3.3). An empty submission
still produces a usable, if uncertain, AccessContext.
"""

from decision.domain import AccessContext, CloudProvider, Intensity, UseMode, WorkloadType

_TRI_STATE = {"yes": True, "no": False, "unknown": None, "": None}


def access_context_from_form(form) -> AccessContext:
    return AccessContext(
        use_mode=_enum_or_default(UseMode, form.get("use_mode"), UseMode.MANUAL),
        workload_type=_enum_or_default(WorkloadType, form.get("workload_type"), WorkloadType.EXPLORATORY),
        intensity=_enum_or_default(Intensity, form.get("intensity"), Intensity.OCCASIONAL),
        country=(form.get("country") or "").strip().upper() or None,
        subscriptions=tuple(form.getlist("subscriptions")),
        has_api_billing=_tri_state(form.get("has_api_billing")),
        cloud_accounts=tuple(
            CloudProvider(value) for value in form.getlist("cloud_accounts") if value in _values(CloudProvider)
        ),
        program_memberships=tuple(form.getlist("program_memberships")),
        has_gpu_infrastructure=_tri_state(form.get("has_gpu_infrastructure")),
    )


def _enum_or_default(enum_cls, raw, default):
    try:
        return enum_cls(raw)
    except ValueError:
        return default


def _tri_state(raw) -> bool | None:
    return _TRI_STATE.get((raw or "").strip().lower(), None)


def _values(enum_cls):
    return {member.value for member in enum_cls}
