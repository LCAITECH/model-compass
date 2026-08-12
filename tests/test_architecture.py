"""Import-boundary checks -- mechanical enforcement of the hard constraints
in AGENTS.md/ARCHITECTURE.md and ACCESS_ADVISOR_AUDIT_2026-08-11.md Part 5.0.

Previously these boundaries were held by discipline/code review only.
Added here per the spec's own note that decision/access/ -> decision/
evaluator/ should get its own test, with the decision/ -> interfaces/
boundary added alongside it since the mechanism is identical.
"""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def _assert_no_forbidden_imports(package_dir: Path, forbidden_prefixes: tuple[str, ...]):
    violations = []
    for path in package_dir.rglob("*.py"):
        for module in _imported_modules(path):
            if module.startswith(forbidden_prefixes):
                violations.append(f"{path.relative_to(ROOT)} imports '{module}'")
    assert not violations, "\n".join(violations)


def test_decision_access_never_imports_evaluator_or_explainer():
    _assert_no_forbidden_imports(
        ROOT / "decision" / "access", ("decision.evaluator", "decision.explainer")
    )


def test_access_domain_types_never_import_evaluator_or_explainer():
    for filename in ("access_context.py", "access_route.py", "access_recommendation.py", "subscription.py"):
        path = ROOT / "decision" / "domain" / filename
        for module in _imported_modules(path):
            assert not module.startswith(("decision.evaluator", "decision.explainer")), (
                f"{filename} imports '{module}'"
            )


def test_decision_never_imports_interfaces():
    _assert_no_forbidden_imports(ROOT / "decision", ("interfaces",))
