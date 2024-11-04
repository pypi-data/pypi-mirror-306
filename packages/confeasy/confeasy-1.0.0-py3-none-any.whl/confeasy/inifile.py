"""Module containing INI files configuration source."""

from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

from confeasy import SNAKE_CASE_REPLACE_PATTERN


class IniFile:
    """
    INI files configuration source.

    If you use $root as the name of a section in an INI file, the keys under the $root section will be treated
    as though they have no section at all (meaning the prefix "$root." will be stripped from their names).
    This approach emulates configurations in other sources where keys can exist at the root level.
    """

    def __init__(self, base_dir: str | None = None):
        """
        :param base_dir: unless absolute path is defined for a INI file,
        this is where the relative paths will be looked for.
        If no base_dir is passed, then current working directory is assumed.
        """
        self._base_dir: Path = Path.cwd() if base_dir is None else Path(base_dir)
        self._files: list[tuple[str, bool]] = []

    def optional(self, path: str) -> IniFile:
        """Define optional INI file. If the path does not exist it is silently ignored."""
        self._files.append((path, False))
        return self

    def required(self, path: str) -> IniFile:
        """
        Define required INI file.

        :raises ValueError: if the path does not exist.
        """
        self._files.append((path, True))
        return self

    def get_configuration_data(self) -> dict[str, str | int | float | bool]:
        """
        Get data which should be merged into configuration.
        The keys should follow the required pattern - see documentation in developer.md.
        """
        result: dict[str, str | int | float | bool] = {}
        for path_str, is_required in self._files:
            path = Path(path_str)
            path = path if path.is_absolute() else self._base_dir / path

            if not path.exists():
                if is_required:
                    raise ValueError(f"configuration file {path} does not exist")
                continue

            config = ConfigParser()
            # The following line allows the casing of the keys remain as in the original source (file).
            config.optionxform = str  # type: ignore[method-assign, assignment]
            config.read(path)

            for section in config.sections():
                for k, v in config.items(section):
                    key = f"{section}.{k}" if section != "$root" else k
                    key = SNAKE_CASE_REPLACE_PATTERN.sub("_", key).lower()
                    result[key] = v

        return result
