"""modalityexporter.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from pathlib import Path
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..base import BaseExporter


# Definitions #
# Classes #
class ModalityExporter(BaseExporter):

    # Instance Methods #
    def execute_export(
        self,
        path: Path,
        name: str | None = None,
        files: bool | set[str, ...] | None = True,
        **kwargs: Any,
    ) -> None:
        if name is None:
            name = self.bids_object.full_name

        new_path = path / name
        new_path.mkdir(exist_ok=True)
        if files or files is None:
            self.export_files(path=new_path, name=name, files=files)
