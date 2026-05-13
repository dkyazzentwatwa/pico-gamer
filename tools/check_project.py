#!/usr/bin/env python3
"""Off-device checks for Pico Gamer.

This intentionally avoids importing MicroPython-only modules such as machine.
It validates syntax, the game registry, and import targets by reading source.
"""

from __future__ import annotations

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def read_module_defs(path: pathlib.Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            names.add(node.name)
    return names


def check_syntax() -> list[str]:
    errors = []
    for path in sorted(ROOT.rglob("*.py")):
        if ".git" in path.parts:
            continue
        try:
            ast.parse(path.read_text(), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    return errors


def load_registry() -> tuple[list[dict], list[dict]]:
    namespace: dict[str, object] = {}
    games_path = ROOT / "games.py"
    exec(compile(games_path.read_text(), str(games_path), "exec"), namespace)
    return namespace["PLAYABLE_GAMES"], namespace["PLANNED_GAMES"]


def check_registry() -> list[str]:
    errors = []
    playable, planned = load_registry()
    seen_titles = set()
    for item in playable:
        title = item.get("title")
        module = item.get("module")
        entrypoint = item.get("entrypoint")
        if not title or not module or not entrypoint:
            errors.append(f"Bad playable registry item: {item}")
            continue
        if title in seen_titles:
            errors.append(f"Duplicate game title: {title}")
        seen_titles.add(title)
        module_path = ROOT / f"{module}.py"
        if not module_path.exists():
            errors.append(f"{title}: missing module {module}.py")
            continue
        defs = read_module_defs(module_path)
        if entrypoint not in defs:
            errors.append(f"{title}: missing entrypoint {entrypoint} in {module}.py")

    planned_titles = set()
    for item in planned:
        title = item.get("title")
        if not title:
            errors.append(f"Bad planned registry item: {item}")
        elif title in seen_titles or title in planned_titles:
            errors.append(f"Duplicate planned game title: {title}")
        planned_titles.add(title)
    return errors


def main() -> int:
    errors = []
    errors.extend(check_syntax())
    errors.extend(check_registry())
    if errors:
        for error in errors:
            print(error)
        return 1
    playable, planned = load_registry()
    print(f"OK: {len(playable)} playable games, {len(planned)} planned games")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
