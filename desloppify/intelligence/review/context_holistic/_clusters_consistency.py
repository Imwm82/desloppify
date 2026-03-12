"""Compatibility wrapper for consistency evidence cluster helpers."""

from .clusters.consistency import _build_duplicate_clusters, _build_naming_drift

__all__ = ["_build_duplicate_clusters", "_build_naming_drift"]
