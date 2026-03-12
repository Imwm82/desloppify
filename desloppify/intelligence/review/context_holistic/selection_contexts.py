"""Compatibility wrapper for holistic selection context builders."""

from .selection.contexts import (
    api_surface_context,
    architecture_context,
    coupling_context,
    dependencies_context,
    error_strategy_context,
    in_allowed_files,
    naming_conventions_context,
    sibling_behavior_context,
    testing_context,
)

__all__ = [
    "api_surface_context",
    "architecture_context",
    "coupling_context",
    "dependencies_context",
    "error_strategy_context",
    "in_allowed_files",
    "naming_conventions_context",
    "sibling_behavior_context",
    "testing_context",
]
