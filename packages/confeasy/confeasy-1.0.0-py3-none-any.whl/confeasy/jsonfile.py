"""Module containing JSON files configuration source."""

from __future__ import annotations

import json
from pathlib import Path

from confeasy import SNAKE_CASE_REPLACE_PATTERN


class JsonFile:
    """JSON files configuration source."""

    def __init__(self, base_dir: str | None = None):
        """
        :param base_dir: unless absolute path is defined for a JSON file,
        this is where the relative paths will be looked for.
        If no base_dir is passed, then current working directory is assumed.
        """
        self._base_dir: Path = Path.cwd() if base_dir is None else Path(base_dir)
        self._files: list[tuple[str, bool]] = []

    def optional(self, path: str) -> JsonFile:
        """Define optional JSON file. If the path does not exist it is silently ignored."""
        self._files.append((path, False))
        return self

    def required(self, path: str) -> JsonFile:
        """
        Define required JSON file.

        :raises ValueError: if the path does not exist.
        """
        self._files.append((path, True))
        return self

    def get_configuration_data(self) -> dict[str, str | int | float | bool]:
        """
        Get data which should be merged into configuration.
        The keys should follow the required pattern - see documentation in developer.md.
        """
        result = {}
        for path_str, is_required in self._files:
            path = Path(path_str)
            path = path if path.is_absolute() else self._base_dir / path

            if not path.exists():
                if is_required:
                    raise ValueError(f"configuration file {path} does not exist")
                continue

            with Path.open(path) as file:
                js = json.load(file)
                flat = _flatten_json(js)
                result.update(flat)

        return result


def _flatten_json(js: dict, parent: str = "") -> dict[str, str | int | float | bool]:
    result: dict[str, str | int | float | bool] = {}
    for k, v in js.items():
        key = f"{parent}.{k}" if parent else k
        if isinstance(v, dict):
            result.update(_flatten_json(v, key))
        else:
            key = SNAKE_CASE_REPLACE_PATTERN.sub("_", key).lower()
            result[key] = v
    return result
