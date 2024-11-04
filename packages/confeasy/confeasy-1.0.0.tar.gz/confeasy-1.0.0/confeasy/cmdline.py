"""Module containing command line arguments configuration source."""

import re
import sys

from confeasy import SNAKE_CASE_REPLACE_PATTERN


TWO_OR_MORE_UNDERSCORES_PATTERN = re.compile(r"_{2,}")


class CommandLine:
    """Command line arguments configuration source"""

    def __init__(self, args: list[str] | None = None):
        self._args = sys.argv[1:] if args is None else args

    def get_configuration_data(self) -> dict[str, str | int | float | bool]:
        """
        Get data which should be merged into configuration.
        The keys should follow the required pattern - see documentation in developer.md.
        """
        result = {}
        i = 0
        while i < len(self._args):
            arg = self._args[i]

            # "--key=value" format
            if "=" in arg and arg.startswith("--"):
                key, value = arg.split("=", 1)
                key = _fmt_key(key.lstrip("-"))
                result[key] = _fmt_val(value)

            # "--key value" format
            elif arg.startswith("--"):
                key = _fmt_key(arg.lstrip("-"))
                if i + 1 < len(self._args) and not self._args[i + 1].startswith("--"):
                    result[key] = _fmt_val(self._args[i + 1])
                    i += 1
                else:
                    result[key] = True

            i += 1

        return result


def _fmt_key(s: str) -> str:
    sc = SNAKE_CASE_REPLACE_PATTERN.sub("_", s)
    return TWO_OR_MORE_UNDERSCORES_PATTERN.sub(".", sc).lower()


def _fmt_val(s: str) -> str | int | float | bool:
    if len(s) > 12:
        return s

    if s in ("true", "True", "TRUE"):
        return True

    if s.lstrip("-").isdigit():
        try:
            return int(s)
        except ValueError:
            pass

    if re.fullmatch(r"^-?\d*\.\d+$", s):
        try:
            return float(s)
        except ValueError:
            pass

    return s
