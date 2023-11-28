"""subject.py

"""

from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


from pathlib import Path
from typing import Any, Optional

from baseobjects import BaseObject

from ucsfbids.importspec.sessionspec import SessionSpec
from ucsfbids.sessions import Session
from ucsfbids.subjects.subject import Subject


class SubjectImporter(BaseObject):
    def __init__(
        self,
        subject: Optional[Subject] = None,
        src_root: Optional[Path] = None,
        sessions: list[SessionSpec] = [],
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        self.subject: Optional[Subject] = None
        self.src_root: Optional[Path] = None

        super().__init__(init=False)

        if init:
            self.construct(
                subject=subject,
                src_root=src_root,
                sessions=sessions,
                **kwargs,
            )

    def _process_sessions(self, sessions):
        assert self.subject is not None

        for session in sessions:
            if session.name not in self.subject.sessions:
                self.subject.create_new_session(Session, session.name, self.subject._mode)
            self.subject.sessions[session.name].add_importer(session.importer_name, session.importer_type)
            # self.subject.sessions[session.name].importers[session.importer_name] = session.importer_type

    def construct(
        self,
        subject: Subject | None = None,
        src_root: Path | None = None,
        sessions: list[SessionSpec] = [],
        process: bool = True,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if subject is not None:
            self.subject = subject

        if src_root is not None:
            self.src_root = src_root

        if process:
            self._process_sessions(sessions)

        super().construct(process=False, **kwargs)

    def import_sessions(self, path: Path, source_patient: str):
        assert self.subject is not None

        for session in self.subject.sessions.values():
            session.create_importer("BIDS", self.src_root).execute_import(path, source_patient)

    def execute_import(self, path: Path, source_patient: str, name: Optional[str] = None) -> None:
        assert self.subject is not None
        if name is None:
            name = self.subject.name
        assert name is not None

        new_path = path / f"sub-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_sessions(path=new_path, source_patient=source_patient)


Subject.default_importers["BIDS"] = SubjectImporter
