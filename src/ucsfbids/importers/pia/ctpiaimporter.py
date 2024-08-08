"""ctpiaimporter.py

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
from pathlib import Path
import shutil
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..modalityimporter import ModalityImporter
from ..file import strip_json


# Definitions #
# Classes #
class CTPiaImporter(ModalityImporter):

    # Attributes #
    importer_name: str = "Pia"

    strip_fields: set[str] = {
        "InstitutionName",
        "InstitutionalDepartmentName",
        "InstitutionAddress",
        "DeviceSerialNumber",
    }
    file_maps: list[tuple[str, str, Iterable[Path], Callable, dict[str, Any]]] = [
        ("CT", ".nii", (Path("CT/CT.nii"), Path("CT/CT.nii.gz")), shutil.copy, {"command": "mri_convert"}),
        ("CT", ".json", (Path("CT/CT_orig.json"), Path("CT/CT.json")), strip_json, {"strip": strip_fields}),
    ]

