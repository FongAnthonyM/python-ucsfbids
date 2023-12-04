"""ieegbidsexporter.py

"""

from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

import json
from pathlib import Path
from typing import Any, Optional

import pandas as pd
from scipy.io import loadmat

from ucsfbids.importspec import FileSpec
from ucsfbids.modalities import IEEG
from ucsfbids.modalities.importers.base import IEEGImporter


def convert_electrodes(old_path, new_path):
    if not old_path.is_file():
        return
    original_montage = loadmat(old_path, squeeze_me=True)
    bids_montage = pd.DataFrame(
        columns=[
            "name",
            "x",
            "y",
            "z",
            "size",
            "material",
            "manufacturer",
            "group",
            "hemisphere",
            "type",
            "impedance",
        ]
    )
    xyz = original_montage["elecmatrix"]
    eleclabels = original_montage["eleclabels"]
    bids_montage.loc[:, "x"] = xyz[:, 0]
    bids_montage.loc[:, "y"] = xyz[:, 1]
    bids_montage.loc[:, "z"] = xyz[:, 2]
    bids_montage.loc[:, "name"] = eleclabels[:, 0]
    bids_montage.loc[:, "group"] = eleclabels[:, 2]
    bids_montage.loc[:, "size"] = "n/a"
    bids_montage.loc[:, "material"] = "n/a"
    bids_montage.loc[:, "manufacturer"] = "n/a"
    bids_montage.loc[bids_montage["x"] > 0, "hemisphere"] = "r"
    bids_montage.loc[bids_montage["x"] <= 0, "hemisphere"] = "l"
    bids_montage.loc[:, "type"] = "n/a"
    bids_montage.loc[:, "impedance"] = "n/a"
    bids_montage.name = bids_montage.name.fillna("NaN")
    bids_montage.to_csv(new_path, sep="\t")


def create_coords(_, new_path):
    coordsystem_json = {"iEEGCoordinateSystem": "ACPC", "iEEGCoordinateUnits": "mm"}
    with open(new_path, "w") as f:
        json.dump(coordsystem_json, f)
    pass


DEFAULT_FILES = [
    FileSpec(
        "electrodes",
        ".tsv",
        [Path("elecs/clinical_elecs_all.mat"), Path("elecs/clinical_TDT_elecs_all.mat")],
        copy_command=convert_electrodes,
    ),
    FileSpec("coordsystem", ".json", [Path("")], copy_command=create_coords),
]


class IEEGPiaImporter(IEEGImporter):
    def construct(
        self,
        modality: Optional[IEEG] = None,
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
            imaging_root = self.src_root / "data_store2/imaging/subjects"
            new_path = path / f"{self.modality.full_name}_{file.suffix}{file.extension}"
            for filepath in file.path_from_root:
                imaging_path = imaging_root / source_name / filepath
                old_name = imaging_path.name
                exclude = any(n in old_name for n in self.import_exclude_names)

                if new_path.exists():
                    continue

                if exclude:
                    continue

                if imaging_path.is_file():
                    self._import_file(file, imaging_path, new_path)
                    break

                if not callable(file.copy_command):
                    continue

                file.copy_command(imaging_path, new_path)

            if not callable(file.copy_command) and not new_path.exists():
                print(new_path)
                raise RuntimeError("No source file but no function provided to gather data")


IEEG.default_importers["Pia"] = IEEGPiaImporter
