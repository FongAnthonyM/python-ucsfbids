"""anatomypiaimporter.py

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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..modalityimporter import ModalityImporter
from ..file import command_copy, strip_json


# Definitions #
# Classes #
class AnatomyPiaImporter(ModalityImporter):

    # Attributes #
    importer_name: str = "Pia"

    strip_fields: set[str] = {
        "InstitutionName",
        "InstitutionalDepartmentName",
        "InstitutionAddress",
        "DeviceSerialNumber",
    }
    file_maps: list[tuple[str, str, Iterable[Path], Callable, dict[str, Any]]] = [
        ("T1w", ".nii.gz", (Path("mri/brain.mgz")), command_copy, {"command": "mri_convert"}),
        ("T1w", ".json", (Path("acpc/T1_orig.json"), Path("acpc/T1.json")), strip_json, {"strip": strip_fields}),
    ]

