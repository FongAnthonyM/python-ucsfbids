"""anatomybidsexporter.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, List

# Imports #
# Standard Libraries #
from baseobjects import BaseObject

# Local Packages #
from ..modality import Modality
from .importspec import ImportSpec

# Third-Party Packages #


# Definitions #
# Classes #
class ModalityImporter(BaseObject):
    import_file_names: set[str] = set()
    import_exclude_names: set[str] = set()

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        modality: Modality | None = None,
        src_root: Path | None = None,
        specs: List[ImportSpec] = [],
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.modality: Modality | None = None
        self.src_root: Path | None = None
        self.specs: List[ImportSpec] = []

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                modality=modality,
                src_root=src_root,
                specs=specs,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        modality: Modality | None = None,
        src_root: Path | None = None,
        specs: List[ImportSpec] = [],
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

        if specs:
            self.specs = specs

        super().construct(**kwargs)

    def import_all_files(self, path: Path) -> None:
        if self.modality is None:
            raise RuntimeError("Undefined Modality")
        for importspec in self.specs:
            subject_name = self.modality.subject_name
            if subject_name is None:
                raise RuntimeError("subject name undefined")
            if self.src_root is None:
                raise RuntimeError("Import root undefined")
            old_path = self.src_root / subject_name / importspec.path_from_root
            if old_path.is_file():
                old_name = old_path.name
                exclude = any(n in old_name for n in self.import_exclude_names)
                if not exclude:
                    new_path = path / f"{self.modality.full_name}_{importspec.suffix}{importspec.extension}"
                    if not new_path.exists():
                        if importspec.copy_command is not None:
                            if isinstance(importspec.copy_command, str):
                                subprocess.run(f"{importspec.copy_command} {old_path} {new_path}")
                            elif callable(importspec.copy_command):
                                importspec.copy_command(old_path, new_path)
                        else:
                            shutil.copy(old_path, new_path)
                        if importspec.post_command is not None:
                            subprocess.run(f"{importspec.post_command} {new_path}")

    def import_select_files(self, path: Path) -> None:
        if self.modality is None:
            raise RuntimeError("Undefined Modality")
        for importspec in self.specs:
            subject_name = self.modality.subject_name
            if subject_name is None:
                raise RuntimeError("subject name undefined")
            if self.src_root is None:
                raise RuntimeError("Import root undefined")
            old_path = self.src_root / subject_name / importspec.path_from_root
            if old_path.is_file():
                old_name = old_path.name
                include = any(n in old_name for n in self.import_file_names)
                exclude = any(n in old_name for n in self.import_exclude_names)
                if include and not exclude:
                    new_path = path / f"{self.modality.full_name}_{importspec.suffix}{importspec.extension}"
                    if not new_path.exists():
                        if importspec.copy_command is not None:
                            if isinstance(importspec.copy_command, str):
                                subprocess.run(f"{importspec.copy_command} {old_path} {new_path}")
                            elif callable(importspec.copy_command):
                                importspec.copy_command(old_path, new_path)
                        else:
                            shutil.copy(old_path, new_path)
                        if importspec.post_command is not None:
                            subprocess.run(f"{importspec.post_command} {new_path}")

    def execute_import(self, path: Path) -> None:
        if self.modality is None:
            raise RuntimeError("Undefined Modality")
        new_path = path / f"{self.modality.name}"
        new_path.mkdir(exist_ok=True)
        self.import_all_files(path=new_path)


# Assign Exporter
Modality.default_importers["BIDS"] = ModalityImporter
