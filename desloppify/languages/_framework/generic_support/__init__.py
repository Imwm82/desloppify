"""Canonical generic-plugin support subpackage for language framework helpers."""

from .capabilities import (
    SHARED_PHASE_LABELS,
    capability_report,
    empty_dep_graph,
    generic_zone_rules,
    make_file_finder,
    noop_extract_functions,
)
from .core import (
    GenericLangOptions,
    generic_lang,
    make_tool_phase,
    parse_cargo,
    parse_eslint,
    parse_gnu,
    parse_golangci,
    parse_json,
    parse_rubocop,
)
from .registration import (
    _build_generic_phases,
    _register_generic_tool_specs,
    _resolve_generic_extractors,
)
from .structural import _make_coupling_phase, _make_structural_phase

__all__ = [
    "GenericLangOptions",
    "SHARED_PHASE_LABELS",
    "_build_generic_phases",
    "_make_coupling_phase",
    "_make_structural_phase",
    "_register_generic_tool_specs",
    "_resolve_generic_extractors",
    "capability_report",
    "empty_dep_graph",
    "generic_lang",
    "generic_zone_rules",
    "make_file_finder",
    "make_tool_phase",
    "noop_extract_functions",
    "parse_cargo",
    "parse_eslint",
    "parse_gnu",
    "parse_golangci",
    "parse_json",
    "parse_rubocop",
]
