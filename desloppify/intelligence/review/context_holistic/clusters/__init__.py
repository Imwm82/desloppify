"""Canonical mechanical evidence cluster builders for holistic review."""

from .accessors import _get_detail, _get_signals, _safe_num
from .complexity import _build_complexity_hotspots
from .consistency import _build_duplicate_clusters, _build_naming_drift
from .dependency import (
    _build_boundary_violations,
    _build_dead_code,
    _build_deferred_import_density,
    _build_private_crossings,
)
from .error_state import _build_error_hotspots, _build_mutable_globals
from .organization import _build_flat_dir_issues, _build_large_file_distribution
from .security import (
    _build_security_hotspots,
    _build_signal_density,
    _build_systemic_patterns,
)

__all__ = [
    "_build_boundary_violations",
    "_build_complexity_hotspots",
    "_build_dead_code",
    "_build_deferred_import_density",
    "_build_duplicate_clusters",
    "_build_error_hotspots",
    "_build_flat_dir_issues",
    "_build_large_file_distribution",
    "_build_mutable_globals",
    "_build_naming_drift",
    "_build_private_crossings",
    "_build_security_hotspots",
    "_build_signal_density",
    "_build_systemic_patterns",
    "_get_detail",
    "_get_signals",
    "_safe_num",
]
