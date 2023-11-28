"""subjectpiaimporter.py

"""

from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

from pathlib import Path
from typing import Any, Optional

from ucsfbids.importspec import SessionSpec
from ucsfbids.sessions.importers.pia.sessionpiaimporter import SessionPiaImporter
from ucsfbids.subjects.importers.subjectimporter import SubjectImporter
from ucsfbids.subjects.subject import Subject

PIA_SESSIONS = [SessionSpec("clinicalintracranial", "Pia", SessionPiaImporter)]


class SubjectPiaImporter(SubjectImporter):
    def construct(
        self,
        subject: Subject | None = None,
        src_root: Path | None = None,
        sessions: list[SessionSpec] = [],
        process=True,
        **kwargs: Any,
    ) -> None:
        if subject is not None:
            self.subject = subject

        if src_root is not None:
            self.src_root = src_root

        sessions.extend(PIA_SESSIONS)

        if process:
            self._process_sessions(sessions)

        super().construct(process=False, **kwargs)

    def import_sessions(self, path: Path, source_patient: str) -> None:
        assert self.subject is not None

        for session in self.subject.sessions.values():
            session.create_importer("Pia", self.src_root).execute_import(
                path, source_patient=source_patient, name=session.name
            )

    def execute_import(self, path: Path, source_patient: str, name: Optional[str] = None) -> None:
        assert self.subject is not None
        if name is None:
            name = self.subject.name
        assert name is not None

        new_path = path / f"sub-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_sessions(path=new_path, source_patient=source_patient)


Subject.default_importers["Pia"] = SubjectPiaImporter
