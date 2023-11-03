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
from typing import Any, Optional

# Imports #
# Standard Libraries #
from baseobjects import BaseObject

from ...ct import CT

# Local Packages #
from ..base import CTImporter
from ..importspec import ImportSpec

# Third-Party Packages #


# Definitions #
# Classes #
class CTPiaImporter(CTImporter):
    ct_pia_spec = [
        ImportSpec("CT", ".nii", Path("CT/CT.nii")),
        ImportSpec("CT", ".json", Path("CT/CT_orig.json")),
    ]

    def __init__(
        self, modality: CT | None = None, src_root: Path | None = None, *, init: bool = True, **kwargs: Any
    ) -> None:
        self.modality: Optional[CT] = None
        self.src_root: Optional[Path] = None

        super().__init__(init=False)

        if init:
            self.construct(modality=modality, src_root=src_root, specs=self.ct_pia_spec, **kwargs)


CT.default_importers["Pia"] = CTPiaImporter
