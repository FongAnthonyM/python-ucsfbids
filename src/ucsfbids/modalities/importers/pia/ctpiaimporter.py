"""ctbidsexporter.py

"""

from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


from json import dump, load
from pathlib import Path
from typing import Any, Optional

from ucsfbids.importspec import FileSpec
from ucsfbids.modalities import CT
from ucsfbids.modalities.importers.base import CTImporter


def strip_json(old_path, new_path):
    if not old_path.exists():
        print(f"could not find {old_path}")
        return
    with open(old_path, "r") as f:
        data_orig = load(f)

    data_clean = {key: value for key, value in data_orig.items() if key not in TO_STRIP}

    with open(new_path, "w") as f:
        dump(data_clean, f)


TO_STRIP = ["InstitutionName", "InstitutionalDepartmentName", "InstitutionAddress", "DeviceSerialNumber"]
DEFAULT_FILES = [
    FileSpec("CT", ".nii", [Path("CT/CT.nii"), Path("CT/CT.nii.gz")]),
    FileSpec("CT", ".json", [Path("CT/CT_orig.json"), Path("CT/CT.json")], copy_command=strip_json),
]


class CTPiaImporter(CTImporter):
    def construct(
        self,
        modality: Optional[CT] = None,
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

    def import_all_files(self, path: Path, source_name: str) -> None:
        assert self.modality is not None
        assert self.src_root is not None

        for file in self.files:
            for path in file.path_from_root:
                imaging_root = self.src_root / "data_store2/imaging/subjects"
                imaging_path = imaging_root / source_name / path
                new_path = path / f"{self.modality.full_name}_{file.suffix}{file.extension}"
                old_name = imaging_path.name
                exclude = any(n in old_name for n in self.import_exclude_names)

                if new_path.exists():
                    continue

                if exclude:
                    continue

                if imaging_path.is_file():
                    self._import_file(file, imaging_path, new_path)
                    continue

                if not callable(file.copy_command):
                    print(f"No source file for {imaging_path}, skipping...")
                    continue

                file.copy_command(imaging_path, new_path)
                break


CT.default_importers["Pia"] = CTPiaImporter
