"""anatomybidsexporter.py

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

from ...anatomy import Anatomy
from ..base import AnatomyImporter
from ..importspec import ImportSpec


# Definitions #
# Classes #
class AnatomyPiaImporter(AnatomyImporter):
    anat_pia_spec = [
        ImportSpec("T1w", ".nii.gz", Path("mri/brain.mgz"), copy_command="mri_convert"),
        ImportSpec("T1w", ".json", Path("acpc/T1_orig.json")),
    ]

    def __init__(
        self,
        modality: Anatomy | None = None,
        src_root: Path | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        self.modality: Optional[Anatomy] = None
        self.src_root: Optional[Path] = None
        super().__init__(init=False)

        if init:
            self.construct(
                modality=modality,
                src_root=src_root,
                specs=self.anat_pia_spec,
                **kwargs,
            )


Anatomy.default_importers["Pia"] = AnatomyPiaImporter
