"""
anatomybidsexporter
"""

from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

from pathlib import Path
from typing import Any, Optional

from ucsfbids.importspec import FileSpec
from ucsfbids.modalities import DWI

from ...importers import ModalityImporter


class DWIImporter(ModalityImporter):
    def __init__(
        self,
        modality: Optional[DWI] = None,
        src_root: Optional[Path] = None,
        files: list[FileSpec] = [],
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        self.modality: Optional[DWI] = None
        self.src_root: Optional[Path] = None
        self.files: list[FileSpec] = []

        super().__init__(init=False)
        if init:
            self.construct(
                modality=modality,
                src_root=src_root,
                files=files,
                **kwargs,
            )
