"""ctbidsexporter.py

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

# Imports #
# Standard Libraries #
from baseobjects import BaseObject

from ...ct import CT

# Local Packages #
from ..base import CTBIDSImporter
from ..importspec import ImportSpec

# Third-Party Packages #


# Definitions #
# Classes #
class CTPiaImporter(CTBIDSImporter):
    ct_pia_spec = [
        ImportSpec("CT", ".nii", Path("CT/CT.nii")),
        ImportSpec("CT", ".json", Path("CT/CT_orig.json")),
    ]

    def __init__(
        self, modality: CT | None = None, src_root: Path | None = None, *, init: bool = True, **kwargs: Any
    ) -> None:
        specs = self.ct_pia_spec
        super().__init__(modality=modality, src_root=src_root, specs=specs, init=init, **kwargs)


CT.default_importers["Pia"] = CTPiaImporter
