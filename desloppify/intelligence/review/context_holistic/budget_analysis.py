"""Compatibility wrapper for holistic budget analysis helpers."""

from .budget.analysis import (
    _count_signature_params,
    _extract_type_names,
    _score_clamped,
    _strip_docstring,
)

__all__ = [
    "_count_signature_params",
    "_extract_type_names",
    "_score_clamped",
    "_strip_docstring",
]
