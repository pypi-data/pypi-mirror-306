"""Module containing environment variables configuration source."""

import os


class EnvironmentVariables:
    """Environment variables configuration source"""

    def __init__(self, prefix: str | None = None):
        self._prefix: str | None = prefix

    def get_configuration_data(self) -> dict[str, str | int | float | bool]:
        """
        Get data which should be merged into configuration.
        The keys should follow the required pattern - see documentation in developer.md.
        """

        def fmt(k: str) -> str:
            k = k if skip == 0 else k[skip:]
            return k.lower().lstrip("_").replace("__", ".")

        result: dict[str, str | int | float | bool] = {}
        skip = 0 if self._prefix is None else len(self._prefix)
        for key, value in os.environ.items():
            if not self._prefix:
                result[fmt(key)] = value
                continue
            if key.startswith(self._prefix):
                result[fmt(key)] = value

        return result
