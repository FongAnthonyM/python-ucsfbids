"""ieegbidsexporter.py

"""
# Package Header #
from ucsfbids.header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from baseobjects import BaseObject
from pathlib import Path
from typing import Any

# Third-Party Packages #

# Local Packages #
from .modalitybidsexporter import ModalityBIDSExporter


# Definitions #
# Classes #
class IEEGBIDSExporter(ModalityBIDSExporter):
    export_file_names: set[str, ...] = {"ieeg", "coordsystem", "electrodes", "channels", "photo"}
    export_exclude_names: set[str, ...] = {"ieeg-meta"}

    def execute_export(self, path: Path, name: str) -> None:
        new_path = path / f"{self.modality.name}"
        new_path.mkdir(exist_ok=True)
        self.export_select_files(path=new_path, name=name)
