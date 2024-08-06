"""subject.py

"""
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

from pathlib import Path
from typing import Any

from ucsfbids.importspec import ModalitySpec
from ucsfbids.modalities import CT, Anatomy, DWI
from ucsfbids.modalities.importers.enigma import (
    AnatomyEnigmaImporter,
    CTEnigmaImporter,
    DWIEnigmaImporter,
)
from ucsfbids.sessions import Session
from ucsfbids.sessions.importers import SessionImporter

DEFAULT_MODALITIES = [
    ModalitySpec("anat", Anatomy, "Enigma", AnatomyEnigmaImporter),
    ModalitySpec("ct", CT, "Enigma", CTEnigmaImporter),
    ModalitySpec("dwi", DWI, "Enigma", DWIEnigmaImporter),
]


class SessionEnigmaImporter(SessionImporter):
    def construct(
        self,
        session: Session | None = None,
        src_root: Path | None = None,
        modalities: list[ModalitySpec] = [],
        **kwargs: Any,
    ) -> None:
        if session is not None:
            self.session = session

        if src_root is not None:
            self.src_root = src_root

        modalities.extend(DEFAULT_MODALITIES)

        self._process_modalities(modalities)
        super().construct(**kwargs)

    def import_modalities(self, path: Path, source_patient: str):
        assert self.session is not None
        for modality in self.session.modalities.values():
            modality.create_importer("Enigma", self.src_root).execute_import(
                path, source_patient
            )

    def execute_import(
        self, path: Path, source_patient: str, name: str | None = None
    ) -> None:
        assert self.session is not None
        if name is None:
            name = self.session.name
        assert name is not None

        new_path = path / f"ses-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_modalities(path=new_path, source_patient=source_patient)


Session.default_importers["Enigma"] = SessionEnigmaImporter
