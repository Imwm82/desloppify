"""Top-level issue generation for the test-coverage detector."""

from __future__ import annotations

from desloppify.engine.detectors.coverage.mapping import (
    build_test_import_index,
    get_test_files_for_prod,
)

from ._issue_gaps import transitive_coverage_gap_issue, untested_module_issue
from ._issue_quality import select_direct_test_quality_issue
from .metrics import _file_loc, _loc_weight


def _build_test_importer_index(
    parsed_imports_by_test: dict[str, set[str]],
) -> dict[str, set[str]]:
    """Build a reverse index: production_file -> set of test files that import it."""
    index: dict[str, set[str]] = {}
    for test_path, prod_files in parsed_imports_by_test.items():
        for prod_file in prod_files:
            index.setdefault(prod_file, set()).add(test_path)
    return index


def _combined_importer_count(
    filepath: str, graph: dict, test_importer_index: dict[str, set[str]]
) -> int:
    """Combined count of production-file and test-file importers."""
    prod_importers = graph.get(filepath, {}).get("importer_count", 0)
    test_importers = len(test_importer_index.get(filepath, set()))
    return prod_importers + test_importers


def generate_issues(
    scorable: set[str],
    directly_tested: set[str],
    transitively_tested: set[str],
    test_quality: dict[str, dict],
    graph: dict,
    lang_name: str,
    complexity_map: dict[str, float] | None = None,
) -> list[dict]:
    """Generate test-coverage issues for all scorable production files."""
    entries: list[dict] = []
    cmap = complexity_map or {}
    test_files = set(test_quality.keys())
    production_scope = set(scorable) | set(directly_tested) | set(transitively_tested)
    parsed_imports_by_test = build_test_import_index(
        test_files,
        production_scope,
        lang_name,
    )
    test_importer_index = _build_test_importer_index(parsed_imports_by_test)

    for filepath in scorable:
        loc = _file_loc(filepath)
        importer_count = _combined_importer_count(filepath, graph, test_importer_index)
        loc_weight = _loc_weight(loc)

        if filepath in directly_tested:
            related_tests = get_test_files_for_prod(
                filepath,
                test_files,
                graph,
                lang_name,
                parsed_imports_by_test=parsed_imports_by_test,
            )
            issue = select_direct_test_quality_issue(
                prod_file=filepath,
                related_tests=related_tests,
                test_quality=test_quality,
                loc_weight=loc_weight,
            )
            if issue:
                entries.append(issue)
            continue

        complexity = cmap.get(filepath, 0)
        if filepath in transitively_tested:
            entries.append(
                transitive_coverage_gap_issue(
                    file_path=filepath,
                    loc=loc,
                    importer_count=importer_count,
                    loc_weight=loc_weight,
                    complexity=complexity,
                )
            )
            continue

        entries.append(
            untested_module_issue(
                file_path=filepath,
                loc=loc,
                importer_count=importer_count,
                loc_weight=loc_weight,
                complexity=complexity,
            )
        )

    return entries


__all__ = ["generate_issues"]
