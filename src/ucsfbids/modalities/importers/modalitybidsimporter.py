"""anatomybidsexporter.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __maintainer__, __email__

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
from typing import Any, Mapping

# Third-Party Packages #

# Local Packages #
from ..modality import Modality


# Definitions #
# Classes #
class ModalityBIDSImporter(BaseObject):
    import_file_names: set[str] = set()
    import_exclude_names: set[str] = set()

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        modality: Modality | None = None,
        src_root: Path | None = None,
        src: Mapping[str, Path] = {},
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.modality: Modality | None = None
        self.src_root: Path | None = None
        self.src: Mapping[str, Path] = {}

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                modality=modality,
                src_root = src_root,
                src = src,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        modality: Modality | None = None,
        src_root: Path | None = None,
        src: Mapping[str, Path] = {},
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if modality is not None:
            self.modality = modality

        if src_root:
            self.src_root = src_root

        if src:
            self.src = src

        super().construct(**kwargs)

    def import_all_files(self, path: Path) -> None:
        if self.modality is None:
            raise RuntimeError("Undefined Modality")
        for bids_suffix, old_path in self.src.items():
            if old_path.is_file():
                old_name = old_path.name
                exclude = any(n in old_name for n in self.import_exclude_names)
                if not exclude:
                    file_suffix = "".join(old_path.suffixes)
                    new_path = path / f"{self.modality.full_name}_{bids_suffix}{file_suffix}"
                    if not new_path.exists():
                        shutil.copy(old_path, new_path)

    def import_select_files(self, path: Path) -> None:
        if self.modality is None:
            raise RuntimeError("Undefined Modality")
        for bids_suffix, old_path in self.src.items():
            if old_path.is_file():
                old_name = old_path.name
                include = any(n in old_name for n in self.import_file_names)
                exclude = any(n in old_name for n in self.import_exclude_names)
                if include and not exclude:
                    file_suffix = "".join(old_path.suffixes)
                    new_path = path / f"{self.modality.full_name}_{bids_suffix}{file_suffix}"
                    if not new_path.exists():
                        shutil.copy(old_path, new_path)

    def execute_import(self, path: Path) -> None:
        if self.modality is None:
            raise RuntimeError("Undefined Modality")
        new_path = path / f"{self.modality.name}"
        new_path.mkdir(exist_ok=True)
        self.import_all_files(path=new_path)


# Assign Exporter
Modality.default_importers["BIDS"] = ModalityBIDSImporter
