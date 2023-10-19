"""ieegbidsexporter.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

from pathlib import Path
from typing import Any
import subprocess
import shutil
import pandas as pd
import json
from scipy.io import loadmat

from ...ieeg import IEEG
from ..base import IEEGBIDSImporter
from ..importspec import ImportSpec


# Definitions #
# Functions #
def convert_electrodes(old_path, new_path):
    if not old_path.is_file():
        pass
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
    bids_montage.to_csv(new_path, sep="\t")


def create_coords(_, new_path):
    coordsystem_json = {"iEEGCoordinateSystem": "ACPC", "iEEGCoordinateUnits": "mm"}
    with open(new_path, "w") as f:
        json.dump(coordsystem_json, f)
    pass


# Classes #
class IEEGPiaImporter(IEEGBIDSImporter):
    ieeg_pia_specs = [
        ImportSpec("electrodes", ".tsv", Path("elecs/clinical_TDT_elecs_all.mat"), copy_command=convert_electrodes),
        ImportSpec("coordsystem", ".json", Path(""), copy_command=create_coords),
    ]

    def __init__(
        self, modality: IEEG | None = None, src_root: Path | None = None, *, init: bool = True, **kwargs: Any
    ) -> None:
        super().__init__(modality=modality, src_root=src_root, specs=self.ieeg_pia_specs, init=init, **kwargs)

    def import_all_files(self, path: Path) -> None:
        if self.modality is None:
            raise RuntimeError("Undefined Modality")

        for importspec in self.specs:
            if self.modality.subject_name is None:
                raise RuntimeError("subject name undefined")

            if self.src_root is None:
                raise RuntimeError("Import root undefined")

            subject_name = self.modality.subject_name
            imaging_root = self.src_root / "data_store2/imaging/subjects"
            imaging_path = imaging_root / subject_name / importspec.path_from_root
            new_path = path / f"{self.modality.full_name}_{importspec.suffix}{importspec.extension}"

            if imaging_path.is_file():
                old_name = imaging_path.name
                exclude = any(n in old_name for n in self.import_exclude_names)

                if not exclude:
                    if not new_path.exists():
                        if importspec.copy_command is not None:
                            if isinstance(importspec.copy_command, str):
                                subprocess.run(f"{importspec.copy_command} {imaging_path} {new_path}")
                            elif callable(importspec.copy_command):
                                importspec.copy_command(imaging_path, new_path)
                        else:
                            shutil.copy(imaging_path, new_path)

                        if importspec.post_command is not None:
                            subprocess.run(f"{importspec.post_command} {new_path}")
            elif not new_path.exists():
                if not callable(importspec.copy_command):
                    raise RuntimeError("No source file but no function provided to gather data")
                else:
                    importspec.copy_command(imaging_path, new_path)


IEEG.default_importers["Pia"] = IEEGPiaImporter
