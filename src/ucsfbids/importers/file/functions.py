"""functions.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import Iterable
from json import dump, load
from pathlib import Path
import subprocess

# Third-Party Packages #

# Local Packages #


# Definitions #
# Functions #
def strip_json(old_path: Path, new_path: Path, strip: Iterable[str] = ()) -> None:
    if not old_path.exists():
        print(f"could not find {old_path}")
        return
    with open(old_path, "r") as f:
        data_orig = load(f)

    data_clean = {key: value for key, value in data_orig.items() if key not in strip}

    with open(new_path, "w") as f:
        dump(data_clean, f)


def command_copy(old_path: Path, new_path: Path, command: str) -> None:
    subprocess.run([command, str(old_path), str(new_path)])


__all__ = ["strip_json", "command_copy"]
