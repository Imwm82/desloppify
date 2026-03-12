"""Compatibility wrapper for language registration helpers."""

from __future__ import annotations

from .registry import registration as _impl


def register_lang_class(name, config_cls) -> None:
    _impl.register_lang_class(name, config_cls)


def register_lang_class_with(name, config_cls, *, validate_lang_structure_fn=_impl.validate_lang_structure) -> None:
    _impl.register_lang_class_with(
        name,
        config_cls,
        validate_lang_structure_fn=validate_lang_structure_fn,
    )


def register_full_plugin(name, config_cls, *, test_coverage: object) -> None:
    _impl.register_full_plugin(name, config_cls, test_coverage=test_coverage)


__all__ = [
    "register_full_plugin",
    "register_lang_class",
    "register_lang_class_with",
]
