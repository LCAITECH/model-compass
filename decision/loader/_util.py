"""Small helpers shared across decision/loader/ and its interfaces/ callers."""


def enum_values(enum_cls) -> set:
    return {member.value for member in enum_cls}
