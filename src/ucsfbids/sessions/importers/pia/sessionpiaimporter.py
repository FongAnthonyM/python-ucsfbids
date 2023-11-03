"""subject.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

# eader #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


import dataclasses
from pathlib import Path
from typing import Any

# Imports #
# Standard Libraries #
from baseobjects import BaseObject

from ....modalities import CT, IEEG, Anatomy, Modality
from ....modalities.importers import ModalityImporter, pia

# Local Packages #
from ...session import Session
from ..sessionimporter import SessionImporter

# Third-Party Packages #


@dataclasses.dataclass
class ModalitySpec:
    name: str
    modality_type: type[Modality]
    importer_key: str
    importer: type[ModalityImporter]


# Definitions #
# Classes #
class SessionPiaImporter(SessionImporter):
    pia_modality_spec = [
        ModalitySpec("anat", Anatomy, "Pia", pia.AnatomyPiaImporter),
        ModalitySpec("ieeg", IEEG, "Pia", pia.IEEGPiaImporter),
        ModalitySpec("ct", CT, "Pia", pia.CTPiaImporter),
    ]

    def construct(self, session: Session | None = None, src_root: Path | None = None, **kwargs: Any) -> None:
        if session is not None:
            self.session = session

        if src_root is not None:
            self.src_root = src_root

        super().construct(**kwargs)

        for spec in self.pia_modality_spec:
            if self.session is None:
                raise RuntimeError("Session is None")

            spec.modality_type.default_importers[spec.importer_key] = spec.importer
            modality = spec.modality_type(parent_path=self.session.path, mode=self.session._mode)
            self.session.modalities[
                spec.name
            ] = modality  # FIX: modality is a RegisteredClass instead of a Modality for some reason
            self.session.create()

    # Magic Methods #
    def import_modalities(self, path: Path):
        if self.session is None:
            raise RuntimeError("Undefined Session.")
        for modality in self.session.modalities.values():
            modality.create_importer("Pia", self.src_root).execute_import(path)

    def execute_import(self, path: Path, name: str | None = None) -> None:
        if self.session is None:
            raise RuntimeError("Undefined Session.")
        if name is None:
            name = self.session.name

        new_path = path / f"ses-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_modalities(path=new_path)


# Assign Exporter
Session.default_importers["Pia"] = SessionPiaImporter
