"""Skip and unskip command handlers for plan overrides."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from desloppify import state as state_mod
from desloppify.base.output.terminal import colorize
from desloppify.base.output.user_message import print_user_message


def _validate_skip_requirements(
    *,
    kind: str,
    attestation: str | None,
    note: str | None,
) -> bool:
    from . import override_handlers as host  # noqa: PLC0415

    if not host.skip_kind_requires_attestation(kind):
        return True
    if not host.validate_attestation(attestation):
        host.show_attestation_requirement(
            "Permanent skip" if kind == "permanent" else "False positive",
            attestation,
            host.ATTEST_EXAMPLE,
        )
        return False
    if host.skip_kind_requires_note(kind) and not note:
        print(
            colorize("  --permanent requires --note to explain the decision.", "yellow"),
            file=sys.stderr,
        )
        return False
    return True


def _apply_state_skip_resolution(
    *,
    kind: str,
    state_file: Path | None,
    issue_ids: list[str],
    note: str | None,
    attestation: str | None,
) -> dict | None:
    status = _skip_kind_state_status(kind)
    if status is None:
        return None
    state_data = state_mod.load_state(state_file)
    for fid in issue_ids:
        state_mod.resolve_issues(
            state_data,
            fid,
            status,
            note or "",
            attestation=attestation,
        )
    return state_data


def _skip_kind_state_status(kind: str) -> str | None:
    from . import override_handlers as host  # noqa: PLC0415

    return host.skip_kind_state_status(kind)


def cmd_plan_skip(args: argparse.Namespace) -> None:
    """Skip issues — unified command for temporary/permanent/false-positive."""
    from . import override_handlers as host  # noqa: PLC0415

    runtime = host.command_runtime(args)
    state = runtime.state
    if not host.require_completed_scan(state):
        return

    patterns: list[str] = getattr(args, "patterns", [])
    reason: str | None = getattr(args, "reason", None)
    review_after: int | None = getattr(args, "review_after", None)
    permanent: bool = getattr(args, "permanent", False)
    false_positive: bool = getattr(args, "false_positive", False)
    note: str | None = getattr(args, "note", None)
    attestation: str | None = getattr(args, "attest", None)

    kind = host.skip_kind_from_flags(permanent=permanent, false_positive=false_positive)
    if not _validate_skip_requirements(kind=kind, attestation=attestation, note=note):
        return

    state_file = runtime.state_path
    plan_file = host._plan_file_for_state(state_file)
    plan = host.load_plan(plan_file)
    issue_ids = host.resolve_ids_from_patterns(state, patterns, plan=plan)
    if not issue_ids:
        print(colorize("  No matching issues found.", "yellow"))
        return

    if len(issue_ids) > host._BULK_SKIP_THRESHOLD:
        print(
            colorize(
                f"  Bulk skip: {len(issue_ids)} items will be removed from the active queue.",
                "yellow",
            ),
            file=sys.stderr,
        )
        if not getattr(args, "confirm", False):
            raise host.CommandError(
                f"Skipping {len(issue_ids)} items requires --confirm. "
                "Review the items first, or skip individually."
            )

    state_data = _apply_state_skip_resolution(
        kind=kind,
        state_file=state_file,
        issue_ids=issue_ids,
        note=note,
        attestation=attestation,
    )

    scan_count = state.get("scan_count", 0)
    count = host.skip_items(
        plan,
        issue_ids,
        kind=kind,
        reason=reason,
        note=note,
        attestation=attestation,
        review_after=review_after,
        scan_count=scan_count,
    )

    host.append_log_entry(
        plan,
        "skip",
        issue_ids=issue_ids,
        actor="user",
        note=note,
        detail={"kind": kind, "reason": reason},
    )
    if state_data is not None:
        host._save_plan_state_transactional(
            plan=plan,
            plan_path=plan_file,
            state_data=state_data,
            state_path_value=state_file,
        )
    else:
        host.save_plan(plan, plan_file)

    print(colorize(f"  {host.SKIP_KIND_LABELS[kind]} {count} item(s).", "green"))
    if review_after:
        print(colorize(f"  Will re-surface after {review_after} scan(s).", "dim"))
    print_user_message(
        "Hey — if skipping was the right call, just continue with"
        " what you were doing. If you think a broader re-triage is"
        " needed, use `desloppify plan triage`. Run `desloppify"
        " plan --help` to see all available plan tools. Otherwise"
        " no need to reply, just keep going."
    )


def cmd_plan_unskip(args: argparse.Namespace) -> None:
    """Unskip issues — bring back to queue."""
    from . import override_handlers as host  # noqa: PLC0415

    runtime = host.command_runtime(args)
    state = runtime.state
    if not host.require_completed_scan(state):
        return

    patterns: list[str] = getattr(args, "patterns", [])

    state_file = runtime.state_path
    plan_file = host._plan_file_for_state(state_file)
    plan = host.load_plan(plan_file)
    issue_ids = host.resolve_ids_from_patterns(state, patterns, plan=plan, status_filter="all")
    if not issue_ids:
        print(colorize("  No matching issues found.", "yellow"))
        return

    include_protected = bool(getattr(args, "force", False))
    count, need_reopen, protected_kept = host.unskip_items(
        plan,
        issue_ids,
        include_protected=include_protected,
    )
    unskipped_ids = [fid for fid in issue_ids if fid not in protected_kept]
    host.append_log_entry(
        plan,
        "unskip",
        issue_ids=unskipped_ids,
        actor="user",
        detail={"need_reopen": need_reopen},
    )

    reopened: list[str] = []
    if need_reopen:
        state_data = state_mod.load_state(state_file)
        for fid in need_reopen:
            reopened.extend(state_mod.resolve_issues(state_data, fid, "open"))
        host._save_plan_state_transactional(
            plan=plan,
            plan_path=plan_file,
            state_data=state_data,
            state_path_value=state_file,
        )
        print(colorize(f"  Reopened {len(reopened)} issue(s) in state.", "dim"))
    else:
        host.save_plan(plan, plan_file)

    print(colorize(f"  Unskipped {count} item(s) — back in queue.", "green"))
    if protected_kept:
        print(
            colorize(
                f"  Kept {len(protected_kept)} protected skip(s) "
                f"(permanent/false_positive with notes). Use --force to override.",
                "yellow",
            )
        )


__all__ = [
    "_apply_state_skip_resolution",
    "_validate_skip_requirements",
    "cmd_plan_skip",
    "cmd_plan_unskip",
]
