"""anatomybidsexporter.py

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
import shutil
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..modality import Modality


# Definitions #
# Classes #
class ModalityBIDSExporter(BaseObject):
    export_file_names: set[str, ...] = set()
    export_exclude_names: set[str, ...] = set()

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        modality: Modality | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.modality: Modality | None = None

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                modality=modality,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        modality: Modality | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if modality is not None:
            self.modality = modality

        super().construct(**kwargs)

    def export_all_files(self, path: Path, name: str) -> None:
        for old_path in self.path.iterdir():
            new_path = path / old_path.name.replace(self.modality.full_name, name)
            if not new_path.exists():
                shutil.copy(old_path, new_path)

    def export_select_files(self, path: Path, name: str) -> None:
        for old_path in self.path.iterdir():
            if old_path.is_file():
                old_name = old_path.name
                include = any(n in old_name for n in self.export_file_names)
                exclude = any(n in old_name for n in self.export_exclude_names)
                if include and not exclude:
                    new_path = path / old_path.name.replace(self.modality.full_name, name)
                    if not new_path.exists():
                        shutil.copy(old_path, path / old_name.replace(self.modality.full_name, name))

    def export(self, path: Path, name: str) -> None:
        new_path = path / f"{self.modality.name}"
        new_path.mkdir(exist_ok=True)
        self.export_all_files(path=new_path, name=name)


# Assign Exporter
Modality.default_exporters["BIDS"] = ModalityBIDSExporter
