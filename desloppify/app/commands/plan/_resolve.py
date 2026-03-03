"""Pattern → issue-ID resolution for plan commands."""

from __future__ import annotations

from desloppify.engine.plan import PlanModel
from desloppify.state import StateModel, match_issues


def resolve_ids_from_patterns(
    state: StateModel,
    patterns: list[str],
    *,
    plan: PlanModel | None = None,
    status_filter: str = "open",
) -> list[str]:
    """Resolve one or more patterns to a deduplicated list of issue IDs.

    When *plan* is provided, literal IDs that exist only in the plan
    (e.g. ``subjective::*`` synthetic items) are included even if they
    have no corresponding entry in ``state["issues"]``.
    """
    seen: set[str] = set()
    result: list[str] = []

    # Collect all plan IDs for literal-match fallback
    plan_ids: set[str] = set()
    if plan is not None:
        plan_ids.update(plan.get("queue_order", []))
        plan_ids.update(plan.get("skipped", {}).keys())
        for cluster in plan.get("clusters", {}).values():
            plan_ids.update(cluster.get("issue_ids", []))

    for pattern in patterns:
        matches = match_issues(state, pattern, status_filter=status_filter)
        if matches:
            for issue in matches:
                fid = issue["id"]
                if fid not in seen:
                    seen.add(fid)
                    result.append(fid)
        elif pattern in plan_ids and pattern not in seen:
            # Literal plan ID (e.g. subjective::foo) not in state issues
            seen.add(pattern)
            result.append(pattern)
        elif plan is not None and pattern in plan.get("clusters", {}):
            # Cluster name → expand to member IDs
            for fid in plan["clusters"][pattern].get("issue_ids", []):
                if fid not in seen:
                    seen.add(fid)
                    result.append(fid)
    return result


__all__ = ["resolve_ids_from_patterns"]
