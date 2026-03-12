"""Compatibility wrapper for language discovery helpers."""

from __future__ import annotations

from desloppify.base.discovery.paths import get_project_root

from .registry import discovery as _impl

_PLUGIN_CONFIG_LOAD_ERRORS = _impl._PLUGIN_CONFIG_LOAD_ERRORS
_PLUGIN_IMPORT_ERRORS = _impl._PLUGIN_IMPORT_ERRORS
_IMPL_USER_PLUGINS_TRUSTED = _impl._user_plugins_trusted


def _sync_impl_globals() -> None:
    """Mirror monkeypatchable module globals onto the canonical implementation."""
    _impl.__file__ = __file__
    _impl.get_project_root = get_project_root
    _impl._user_plugins_trusted = _user_plugins_trusted


def _user_plugins_trusted(*, load_config_fn=None) -> bool:
    return _IMPL_USER_PLUGINS_TRUSTED(load_config_fn=load_config_fn)


def load_all(*, force_reload: bool = False) -> None:
    _sync_impl_globals()
    _impl.load_all(force_reload=force_reload)


def raise_load_errors() -> None:
    _impl.raise_load_errors()


def reload_all() -> None:
    _sync_impl_globals()
    _impl.reload_all()


def reset_runtime_state() -> None:
    _impl.reset_runtime_state()


__all__ = [
    "load_all",
    "raise_load_errors",
    "reload_all",
    "reset_runtime_state",
]
