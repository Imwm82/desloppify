"""Direct tests for lazy package-root command entrypoints."""

from __future__ import annotations

import argparse

import desloppify.app.commands.autofix as autofix_pkg
import desloppify.app.commands.autofix.cmd as autofix_cmd_mod
import desloppify.app.commands.backlog as backlog_pkg
import desloppify.app.commands.backlog.cmd as backlog_cmd_mod
import desloppify.app.commands.move as move_pkg
import desloppify.app.commands.move.cmd as move_cmd_mod
import desloppify.app.commands.next as next_pkg
import desloppify.app.commands.next.cmd as next_cmd_mod
import desloppify.app.commands.scan as scan_pkg
import desloppify.app.commands.scan.cmd as scan_cmd_mod
import desloppify.app.commands.show as show_pkg
import desloppify.app.commands.show.cmd as show_cmd_mod


def test_package_root_entrypoints_delegate_to_command_modules(monkeypatch) -> None:
    args = argparse.Namespace(path=".")
    calls: list[tuple[str, argparse.Namespace]] = []

    monkeypatch.setattr(autofix_cmd_mod, "cmd_autofix", lambda value: calls.append(("autofix", value)))
    monkeypatch.setattr(backlog_cmd_mod, "cmd_backlog", lambda value: calls.append(("backlog", value)))
    monkeypatch.setattr(move_cmd_mod, "cmd_move", lambda value: calls.append(("move", value)))
    monkeypatch.setattr(next_cmd_mod, "cmd_next", lambda value: calls.append(("next", value)))
    monkeypatch.setattr(scan_cmd_mod, "cmd_scan", lambda value: calls.append(("scan", value)))
    monkeypatch.setattr(show_cmd_mod, "cmd_show", lambda value: calls.append(("show", value)))

    autofix_pkg.cmd_autofix(args)
    backlog_pkg.cmd_backlog(args)
    move_pkg.cmd_move(args)
    next_pkg.cmd_next(args)
    scan_pkg.cmd_scan(args)
    show_pkg.cmd_show(args)

    assert calls == [
        ("autofix", args),
        ("backlog", args),
        ("move", args),
        ("next", args),
        ("scan", args),
        ("show", args),
    ]
