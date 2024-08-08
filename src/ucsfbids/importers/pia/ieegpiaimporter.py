"""ieegpiaimporter.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import Callable, Iterable
import json
from pathlib import Path
from typing import Any

# Third-Party Packages #
import pandas as pd
from scipy.io import loadmat

# Local Packages #
from ..modalityimporter import ModalityImporter


# Definitions #
# Functions #
def convert_electrodes(old_path, new_path):
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
    eleclabels = eleclabels[: len(xyz), :]
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


# Classes #
class IEEGPiaImporter(ModalityImporter):

    # Attributes #
    importer_name: str = "Pia"

    strip_fields: set[str] = {
        "InstitutionName",
        "InstitutionalDepartmentName",
        "InstitutionAddress",
        "DeviceSerialNumber",
    }
    file_maps: list[tuple[str, str, Iterable[Path], Callable, dict[str, Any]]] = [
        (
            "electrodes",
            ".tsv",
            (Path("elecs/clinical_elecs_all.mat"), Path("elecs/clinical_TDT_elecs_all.mat"), Path("elecs/clinical_elecs_all1.mat")),
            convert_electrodes,
            {},
        ),
        ("coordsystem", ".json", (Path("")), create_coords, {}),
    ]

