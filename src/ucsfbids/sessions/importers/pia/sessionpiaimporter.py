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
from ucsfbids.modalities import CT, IEEG, Anatomy
from ucsfbids.modalities.importers.pia import AnatomyPiaImporter, CTPiaImporter, IEEGPiaImporter
from ucsfbids.sessions import Session
from ucsfbids.sessions.importers import SessionImporter

DEFAULT_MODALITIES = [
    ModalitySpec("anat", Anatomy, "Pia", AnatomyPiaImporter),
    ModalitySpec("ieeg", IEEG, "Pia", IEEGPiaImporter),
    ModalitySpec("ct", CT, "Pia", CTPiaImporter),
]


class SessionPiaImporter(SessionImporter):
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

    def import_modalities(self, path: Path):
        assert self.session is not None
        for modality in self.session.modalities.values():
            modality.create_importer("Pia", self.src_root).execute_import(path)

    def execute_import(self, path: Path, name: str | None = None) -> None:
        assert self.session is not None
        if name is None:
            name = self.session.name
        assert name is not None

        new_path = path / f"ses-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_modalities(path=new_path)


Session.default_importers["Pia"] = SessionPiaImporter
