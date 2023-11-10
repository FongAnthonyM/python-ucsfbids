"""sessionimporter.py

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

from baseobjects import BaseObject

from ucsfbids.importspec import ModalitySpec
from ucsfbids.sessions.session import Session


class SessionImporter(BaseObject):
    def __init__(
        self,
        session: Optional[Session] = None,
        src_root: Optional[Path] = None,
        modalities: list[ModalitySpec] = [],
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        self.session: Optional[Session] = None
        self.src_root: Optional[Path] = None

        super().__init__(init=False)

        if init:
            self.construct(
                session=session,
                src_root=src_root,
                modalities=modalities,
                **kwargs,
            )

    def _process_modalities(self, modalities: list[ModalitySpec]):
        assert self.session is not None

        for modality in modalities:  # FIX: add to importers not default_importers
            modality.modality_type.default_importers[modality.importer_key] = modality.importer
            mod = modality.modality_type(parent_path=self.session.path, mode=self.session._mode)
            self.session.modalities[modality.name] = mod  # FIX: modality is a RegisteredClass
        self.session.create()

    def construct(
        self,
        session: Optional[Session] = None,
        src_root: Optional[Path] = None,
        modalities: list[ModalitySpec] = [],
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if session is not None:
            self.session = session

        if src_root is not None:
            self.src_root = src_root

        self._process_modalities(modalities)
        super().construct(**kwargs)

    def import_modalities(self, path: Path):
        assert self.session is not None

        for modality in self.session.modalities.values():
            modality.create_importer("BIDS", self.src_root).execute_import(path)

    def execute_import(self, path: Path, name: str | None = None) -> None:
        assert self.session is not None
        if name is None:
            name = self.session.name
        assert name is not None

        new_path = path / f"ses-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_modalities(path=new_path)


Session.default_importers["BIDS"] = SessionImporter
