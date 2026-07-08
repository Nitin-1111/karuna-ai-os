"""Smoke tests for package importability."""

import importlib
import pkgutil


def test_package_import_walk() -> None:
    """All project modules should import without circular import failures."""

    for package_name in ("backend", "agents", "workflows", "memory", "config", "llm"):
        package = importlib.import_module(package_name)
        for module in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            importlib.import_module(module.name)
