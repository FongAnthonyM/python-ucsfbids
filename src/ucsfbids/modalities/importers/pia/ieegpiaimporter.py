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

from ...ieeg import IEEG
from ..base import IEEGBIDSImporter
from ..importspec import ImportSpec


# Definitions #
# Functions #
def convert_electrodes(old_path, new_path):
    pass


def convert_coords(old_path, new_path):
    pass


def convert_ieeg_days(old_path, new_path):
    pass


# Classes #
class IEEGPiaImporter(IEEGBIDSImporter):
    ieeg_pia_specs = [
        ImportSpec("electrodes", ".tsv", Path("elecs/clinical_TDT_elecs_all.mat"), copy_command=convert_electrodes),
        ImportSpec("coordsystem", ".json", Path(""), copy_command=convert_coords),
        ImportSpec("ieeg", ".h5", Path("human/converted_clinical"), copy_command=convert_ieeg_days),
    ]

    def __init__(
        self, modality: IEEG | None = None, src_root: Path | None = None, *, init: bool = True, **kwargs: Any
    ) -> None:
        super().__init__(modality=modality, src_root=src_root, specs=self.ieeg_pia_specs, init=init, **kwargs)


IEEG.default_importers["Pia"] = IEEGPiaImporter
