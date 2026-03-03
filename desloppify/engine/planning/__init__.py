"""Planning public API with lazy imports to avoid import cycles."""

from __future__ import annotations

from typing import Any

from desloppify.engine.planning.common import CONFIDENCE_ORDER


def generate_plan_md(*args: Any, **kwargs: Any):
    from desloppify.engine.planning.core import generate_plan_md as _generate_plan_md

    return _generate_plan_md(*args, **kwargs)


def generate_issues(*args: Any, **kwargs: Any):
    from desloppify.engine.planning.core import generate_issues as _generate_issues

    return _generate_issues(*args, **kwargs)


def get_next_item(*args: Any, **kwargs: Any):
    from desloppify.engine.planning.core import get_next_item as _get_next_item

    return _get_next_item(*args, **kwargs)


def get_next_items(*args: Any, **kwargs: Any):
    from desloppify.engine.planning.core import get_next_items as _get_next_items

    return _get_next_items(*args, **kwargs)


__all__ = [
    "CONFIDENCE_ORDER",
    "generate_issues",
    "generate_plan_md",
    "get_next_item",
    "get_next_items",
]
