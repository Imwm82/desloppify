"""Shared compatibility exports for staged triage command handlers."""

from __future__ import annotations

from desloppify.app.commands.plan.triage.progress_render import (
    _print_progress,
    _print_stage_progress,
)
from desloppify.app.commands.plan.triage.reflect_dashboard import (
    _print_reflect_dashboard,
)
from desloppify.app.commands.plan.triage.stage_helpers import (
    _manual_clusters_with_issues,
    _require_triage_pending,
    _triage_coverage,
    _unenriched_clusters,
    _validate_stage_report,
)
from desloppify.app.commands.plan.triage.stage_persistence import (
    record_triage_stage,
    refresh_stage_snapshot,
)

__all__ = [
    "_manual_clusters_with_issues",
    "_print_progress",
    "_print_reflect_dashboard",
    "_print_stage_progress",
    "_require_triage_pending",
    "_triage_coverage",
    "_unenriched_clusters",
    "_validate_stage_report",
    "record_triage_stage",
    "refresh_stage_snapshot",
]
