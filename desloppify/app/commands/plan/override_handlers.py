"""Plan override subcommand handlers: describe, note, skip, unskip, done, reopen, focus."""

from __future__ import annotations

import argparse
import logging

from pathlib import Path

from desloppify import state as state_mod
from desloppify.app.commands.helpers.runtime import command_runtime
from desloppify.app.commands.helpers.state import require_completed_scan, state_path
from desloppify.app.commands.plan._resolve import resolve_ids_from_patterns
from desloppify.app.commands.plan.triage.helpers import has_triage_in_queue, inject_triage_stages
from desloppify.app.commands.plan.triage_playbook import TRIAGE_STAGE_DEPENDENCIES
from desloppify.app.commands.resolve.cmd import cmd_resolve
from desloppify.app.commands.helpers.attestation import (
    show_attestation_requirement,
    show_note_length_requirement,
    validate_attestation,
    validate_note_length,
)
from desloppify.base.exception_sets import PLAN_LOAD_EXCEPTIONS, CommandError
from desloppify.engine._work_queue.core import ATTEST_EXAMPLE
from desloppify.engine.plan import (
    TRIAGE_IDS,
    TRIAGE_STAGE_IDS,
    SKIP_KIND_LABELS,
    WORKFLOW_CREATE_PLAN_ID,
    WORKFLOW_SCORE_CHECKPOINT_ID,
    annotate_issue,
    auto_complete_steps,
    append_log_entry,
    clear_focus,
    describe_issue,
    load_plan,
    purge_ids,
    purge_uncommitted_ids,
    save_plan,
    set_focus,
    skip_kind_from_flags,
    skip_kind_requires_attestation,
    skip_kind_requires_note,
    skip_kind_state_status,
    skip_items,
    unskip_items,
)

from .override_io import _plan_file_for_state
from .override_io import save_plan_state_transactional as _save_plan_state_transactional_impl
from .override_misc import cmd_plan_describe as _cmd_plan_describe_impl
from .override_misc import cmd_plan_focus as _cmd_plan_focus_impl
from .override_misc import cmd_plan_note as _cmd_plan_note_impl
from .override_misc import cmd_plan_reopen as _cmd_plan_reopen_impl
from .override_misc import cmd_plan_scan_gate as _cmd_plan_scan_gate_impl
from .override_resolve_cmd import cmd_plan_resolve as _cmd_plan_resolve_impl
from .override_resolve_helpers import blocked_triage_stages as _blocked_triage_stages_impl
from .override_resolve_helpers import check_cluster_guard as _check_cluster_guard_impl
from .override_skip import cmd_plan_skip as _cmd_plan_skip_impl
from .override_skip import cmd_plan_unskip as _cmd_plan_unskip_impl

logger = logging.getLogger(__name__)

_BULK_SKIP_THRESHOLD = 5
_CLUSTER_INDIVIDUAL_THRESHOLD = 10


def _save_plan_state_transactional(
    *,
    plan: dict,
    plan_path: Path | None,
    state_data: dict,
    state_path_value: Path | None,
) -> None:
    """Persist plan+state together; rollback both files on partial write failure."""
    _save_plan_state_transactional_impl(
        plan=plan,
        plan_path=plan_path,
        state_data=state_data,
        state_path_value=state_path_value,
    )


def _check_cluster_guard(patterns: list[str], plan: dict, state: dict) -> bool:
    """Return True if blocked by cluster guard, False if OK to proceed."""
    return _check_cluster_guard_impl(patterns, plan, state)


def _blocked_triage_stages(plan: dict) -> dict[str, list[str]]:
    """Return ``{stage_id: [blocked_by_ids]}`` for triage stages that can't run yet."""
    return _blocked_triage_stages_impl(plan)


def cmd_plan_describe(args: argparse.Namespace) -> None:
    _cmd_plan_describe_impl(args)


def cmd_plan_note(args: argparse.Namespace) -> None:
    _cmd_plan_note_impl(args)


def cmd_plan_skip(args: argparse.Namespace) -> None:
    """Skip issues — unified command for temporary/permanent/false-positive."""
    _cmd_plan_skip_impl(args)


def cmd_plan_unskip(args: argparse.Namespace) -> None:
    """Unskip issues — bring back to queue."""
    _cmd_plan_unskip_impl(args)


def cmd_plan_resolve(args: argparse.Namespace) -> None:
    """Mark issues as fixed — delegates to cmd_resolve for rich UX."""
    _cmd_plan_resolve_impl(args)


def cmd_plan_reopen(args: argparse.Namespace) -> None:
    """Reopen resolved issues from plan context."""
    _cmd_plan_reopen_impl(args)


def cmd_plan_focus(args: argparse.Namespace) -> None:
    """Set or clear the active cluster focus."""
    _cmd_plan_focus_impl(args)


def cmd_plan_scan_gate(args: argparse.Namespace) -> None:
    """Check or skip the scan requirement for workflow items."""
    _cmd_plan_scan_gate_impl(args)


__all__ = [
    "cmd_plan_describe",
    "cmd_plan_resolve",
    "cmd_plan_focus",
    "cmd_plan_note",
    "cmd_plan_reopen",
    "cmd_plan_scan_gate",
    "cmd_plan_skip",
    "cmd_plan_unskip",
]
