"""anatomybidsexporter.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


from json import dump, load
from pathlib import Path
from typing import Any, Optional

from ucsfbids.importspec import FileSpec
from ucsfbids.modalities import Anatomy
from ucsfbids.modalities.importers.base import AnatomyImporter


def strip_json(old_path, new_path):
    with open(old_path, "r") as f:
        data_orig = load(f)

    data_clean = {key: value for key, value in data_orig.values() if key not in TO_STRIP}

    with open(new_path, "w") as f:
        dump(data_clean, f)


TO_STRIP = ["InstitutionName", "InstitutionalDepartmentName", "InstitutionAddress", "DeviceSerialNumber"]
DEFAULT_FILES = [
    FileSpec("T1w", ".nii.gz", Path("mri/brain.mgz"), copy_command="mri_convert"),
    FileSpec("T1w", ".json", Path("acpc/T1_orig.json"), copy_command=strip_json),
]


class AnatomyPiaImporter(AnatomyImporter):
    def construct(
        self,
        modality: Optional[Anatomy] = None,
        src_root: Optional[Path] = None,
        files: list[FileSpec] = [],
        **kwargs: Any,
    ) -> None:
        if modality is not None:
            self.modality = modality

        if src_root is not None:
            self.src_root = src_root

        files.extend(DEFAULT_FILES)
        self.files = files
        super().construct(**kwargs)


Anatomy.default_importers["Pia"] = AnatomyPiaImporter
