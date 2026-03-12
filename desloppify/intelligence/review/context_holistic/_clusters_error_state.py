"""Compatibility wrapper for error-state evidence cluster helpers."""

from .clusters.error_state import _build_error_hotspots, _build_mutable_globals

__all__ = ["_build_error_hotspots", "_build_mutable_globals"]
