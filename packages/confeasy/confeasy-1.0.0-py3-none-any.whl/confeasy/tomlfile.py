"""Module containing TOML files configuration source."""

from __future__ import annotations

from pathlib import Path
import tomllib

from confeasy import SNAKE_CASE_REPLACE_PATTERN


class TomlFile:
    """TOML files configuration source."""

    def __init__(self, base_dir: str | None = None):
        """
        :param base_dir: unless absolute path is defined for a TOML file,
        this is where the relative paths will be looked for.
        If no base_dir is passed, then current working directory is assumed.
        """
        self._base_dir: Path = Path.cwd() if base_dir is None else Path(base_dir)
        self._files: list[tuple[str, bool]] = []

    def optional(self, path: str) -> TomlFile:
        """Define optional TOML file. If the path does not exist it is silently ignored."""
        self._files.append((path, False))
        return self

    def required(self, path: str) -> TomlFile:
        """
        Define required TOML file.

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

            with open(path, "rb") as file:
                toml = tomllib.load(file)
                flat = _flatten_dict(toml)
                result.update(flat)

        return result


def _flatten_dict(d: dict, parent: str = "") -> dict[str, str | int | float | bool]:
    result: dict[str, str | int | float | bool] = {}
    for k, v in d.items():
        key = f"{parent}.{k}" if parent else k
        if isinstance(v, dict):
            result.update(_flatten_dict(v, key))
        else:
            key = SNAKE_CASE_REPLACE_PATTERN.sub("_", key).lower()
            result[key] = v
    return result
