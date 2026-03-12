"""Direct tests for triage plan-state access helpers."""

from __future__ import annotations

from desloppify.app.commands.plan.triage.plan_state_access import (
    ensure_cluster_map,
    ensure_execution_log,
    ensure_queue_order,
    ensure_skipped_map,
    ensure_triage_meta,
    normalized_issue_id_list,
)


def test_plan_state_access_initializes_missing_collections() -> None:
    plan: dict[str, object] = {}

    queue_order = ensure_queue_order(plan)
    skipped = ensure_skipped_map(plan)
    clusters = ensure_cluster_map(plan)
    meta = ensure_triage_meta(plan)
    log = ensure_execution_log(plan)

    assert queue_order == []
    assert skipped == {}
    assert clusters == {}
    assert meta == {}
    assert log == []
    assert plan["queue_order"] is queue_order
    assert plan["skipped"] is skipped
    assert plan["clusters"] is clusters
    assert plan["epic_triage_meta"] is meta
    assert plan["execution_log"] is log


def test_normalized_issue_id_list_filters_non_strings() -> None:
    assert normalized_issue_id_list(["a", 123, None, "b"]) == ["a", "b"]
    assert normalized_issue_id_list("a") == []
