"""Compatibility wrapper for holistic budget wrapper-pattern helpers."""

from .budget.patterns_wrappers import (
    _find_delegation_heavy_classes,
    _find_facade_modules,
    _find_python_passthrough_wrappers,
    _is_delegation_stmt,
    _python_passthrough_target,
)

__all__ = [
    "_find_delegation_heavy_classes",
    "_find_facade_modules",
    "_find_python_passthrough_wrappers",
    "_is_delegation_stmt",
    "_python_passthrough_target",
]
