"""Base confeasy module."""

from __future__ import annotations

import re
from typing import Any, Protocol, TypeVar


__version__ = "1.0.0"

T = TypeVar("T")
VALID_KEY_PATTERN = re.compile(r"^[a-z]+(\.[a-z_]+)*$")
MAX_BIND_DEPTH = 5
SNAKE_CASE_REPLACE_PATTERN = re.compile(r"(?<!^)(?=[A-Z][a-z]|[A-Z](?=[A-Z][a-z]|$))")


class Source(Protocol):
    """Defines protocol for configuration sources."""

    def get_configuration_data(self) -> dict[str, str | int | float | bool]:
        """
        Get data which should be merged into configuration.
        The keys should follow the required pattern - see documentation in developer.md.
        """
        raise NotImplementedError("method must be implemented by classes that conform to the protocol.")


class Configuration:
    """
    Configuration merged from all the sources.
    It provides methods to retrieve individual values or to populate property values of a class instance.
    """

    def __init__(self, data: dict[str, str | int | float | bool]):
        self._data = data

    @property
    def data(self) -> dict[str, str | int | float | bool]:
        """Get all available configuration data."""
        return self._data

    def get_value(self, key: str) -> str | int | float | bool | None:
        """Get individual value from configuration by key."""
        return self._data.get(key, None)

    def bind(self, instance: T, prefix: str | None = None) -> T:
        """
        Populate property values of a class instance in-place (it does not create a copy).

        :param instance: a class instance, it should have either plain fields and/or properties including setters
        :param prefix: only configuration values with keys starting with this prefix will be used
        :return: the same instance of T that has been passed in
        """
        data = self._data if prefix is None else _filter_data(prefix, self._data)
        for key, value in data.items():
            _bind(instance, key, value, 0)

        return instance


def _filter_data(prefix: str, data: dict[str, str | int | float | bool]) -> dict[str, str | int | float | bool]:
    def new_key(k: str) -> str:
        idx = prefix_len + 1 if k[prefix_len] == "." else prefix_len
        return k[idx:]

    prefix_len = len(prefix)
    return {new_key(k): v for k, v in data.items() if k.startswith(prefix)}


def _bind(instance: T, path: str, value: str | int | float | bool, depth: int) -> bool:
    member_name, path_remainder = _expand_path(path)

    if not hasattr(instance, member_name):
        return False  # no field or property of such name has been found

    attr = getattr(type(instance), member_name, None)
    if isinstance(attr, property) and attr.fset is None:
        return False  # the property is read-only

    current_value = getattr(instance, member_name, None)
    if current_value is None:
        setattr(instance, member_name, value)
        return True

    if isinstance(current_value, str):
        setattr(instance, member_name, _force_str(value))
        return True

    if isinstance(current_value, int):
        setattr(instance, member_name, _force_int(value))
        return True

    if isinstance(current_value, float):
        setattr(instance, member_name, _force_float(value))
        return True

    if isinstance(current_value, bool):
        setattr(instance, member_name, _force_bool(value))
        return True

    if isinstance(current_value, list):
        setattr(instance, member_name, value)
        return True

    if depth >= MAX_BIND_DEPTH:
        return False

    return _bind(current_value, path_remainder, value, depth + 1)


def _force_str(v: Any) -> str:
    return v if isinstance(v, str) else str(v)


def _force_int(v: Any) -> int:
    return v if isinstance(v, int) else int(v)


def _force_float(v: Any) -> float:
    return v if isinstance(v, float) else float(v)


def _force_bool(v: Any) -> bool:
    return v if isinstance(v, bool) else bool(v)


def _expand_path(path: str) -> tuple[str, str]:
    if "." in path:
        before_dot, after_dot = path.split(".", 1)
        return before_dot, after_dot
    else:
        return path, ""


class Builder:
    """Defines which configuration sources will be included in building the final configuration data."""

    def __init__(self, drop_invalid_keys: bool = True):
        self._sources: list[Source] = []
        self._data: dict[str, str | int | float | bool] = {}
        self._drop_invalid_keys = drop_invalid_keys

    def add_source(self, source: Source) -> Builder:
        """Add new configuration source."""
        self._sources.append(source)
        return self

    def add_data(self, data: dict[str, Any]) -> Builder:
        """Add configuration data explicitly without a configuration source. This is useful for testing."""
        sanitized = _sanitize(data, self._drop_invalid_keys)
        self._data.update(sanitized)
        return self

    def build(self) -> Configuration:
        """Create final configuration from all the sources previously defined."""
        merged = self._data.copy()
        for source in self._sources:
            src = source.get_configuration_data()
            sanitized = _sanitize(src, self._drop_invalid_keys)
            merged.update(sanitized)
        return Configuration(merged)


def _sanitize(data: dict[str, Any], drop_invalid_keys: bool = True) -> dict[str, str | int | float | bool]:
    sanitized = {}
    for key, value in data.items():
        key = key.lower()
        if not VALID_KEY_PATTERN.match(key):
            if drop_invalid_keys:
                continue
            else:
                raise ValueError(f"invalid key '{key}'")

        if isinstance(value, str | int | float | bool):
            sanitized[key] = value
        else:
            sanitized[key] = str(value)

    return sanitized
