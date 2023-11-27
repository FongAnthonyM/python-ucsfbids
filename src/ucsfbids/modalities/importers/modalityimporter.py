"""anatomybidsexporter.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional

# Local Packages #
from baseobjects import BaseObject

from ucsfbids.importspec import FileSpec

# Third-Party Packages #
from ucsfbids.modalities import Modality


# Definitions #
# Classes #
class ModalityImporter(BaseObject):
    import_file_names: set[str] = set()
    import_exclude_names: set[str] = set()

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        modality: Optional[Modality] = None,
        src_root: Optional[Path] = None,
        files: list[FileSpec] = [],
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.modality: Optional[Modality] = None
        self.src_root: Optional[Path] = None
        self.files: list[FileSpec] = []

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                modality=modality,
                src_root=src_root,
                files=files,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        modality: Optional[Modality] = None,
        src_root: Optional[Path] = None,
        files: list[FileSpec] = [],
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if modality is not None:
            self.modality = modality

        if src_root is not None:
            self.src_root = src_root

        if files:
            self.files = files

        super().construct(**kwargs)

    def _import_file(self, file: FileSpec, old_path: Path, new_path: Path):
        if file.copy_command is None:
            shutil.copy(old_path, new_path)
        elif isinstance(file.copy_command, str):
            # subprocess.run(f"{file.copy_command} {old_path} {new_path}")
            subprocess.run([file.copy_command, old_path, new_path])
        elif callable(file.copy_command):
            file.copy_command(old_path, new_path)

        if file.post_command is not None:
            # subprocess.run(f"{file.post_command} {new_path}")
            subprocess.run([file.post_command, new_path])

    def import_all_files(self, path: Path) -> None:
        assert self.modality is not None
        assert self.src_root is not None
        subject_name = self.modality.subject_name
        assert subject_name is not None

        for file in self.files:
            old_path = self.src_root / subject_name / file.path_from_root
            old_name = old_path.name
            exclude = any(n in old_name for n in self.import_exclude_names)
            new_path = path / f"{self.modality.full_name}_{file.suffix}{file.extension}"

            if not old_path.is_file():
                continue

            if exclude:
                continue

            if new_path.exists():
                continue

            self._import_file(file, old_path, new_path)

    def import_select_files(self, path: Path) -> None:
        assert self.modality is not None
        assert self.src_root is not None
        subject_name = self.modality.subject_name
        assert subject_name is not None

        for file in self.files:
            old_path = self.src_root / subject_name / file.path_from_root
            old_name = old_path.name
            include = any(n in old_name for n in self.import_file_names)
            exclude = any(n in old_name for n in self.import_exclude_names)
            new_path = path / f"{self.modality.full_name}_{file.suffix}{file.extension}"

            if not old_path.is_file():
                continue

            if exclude:
                continue

            if not include:
                continue

            if new_path.exists():
                continue

            self._import_file(file, old_path, new_path)

    def execute_import(self, path: Path) -> None:
        assert self.modality is not None

        new_path = path / f"{self.modality.name}"
        new_path.mkdir(exist_ok=True)
        self.import_all_files(path=new_path)


# Assign Exporter
Modality.default_importers["BIDS"] = ModalityImporter
