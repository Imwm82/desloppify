"""Compatibility wrapper for dependency evidence cluster helpers."""

from .clusters.dependency import (
    _build_boundary_violations,
    _build_dead_code,
    _build_deferred_import_density,
    _build_private_crossings,
)

__all__ = [
    "_build_boundary_violations",
    "_build_dead_code",
    "_build_deferred_import_density",
    "_build_private_crossings",
]
