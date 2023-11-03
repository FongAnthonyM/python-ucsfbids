"""subject.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__
from ucsfbids.sessions.importers.pia.sessionpiaimporter import SessionPiaImporter
from ucsfbids.sessions.session import Session

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


from dataclasses import dataclass

# Imports #
# Standard Libraries #
from pathlib import Path
from typing import Any, Optional

from ....sessions.importers import SessionImporter

# Local Packages #
from ...subject import Subject
from ..subjectimporter import SubjectImporter


@dataclass
class SessionSpec:
    name: str
    importer_name: str
    importer_type: type[SessionImporter]


# Definitions #
# Classes #
class SubjectPiaImporter(SubjectImporter):
    pia_session_spec = [SessionSpec("0000", "Pia", SessionPiaImporter)]

    def __init__(
        self, subject: Subject | None = None, src_root: Path | None = None, *, init: bool = True, **kwargs: Any
    ) -> None:
        super().__init__(subject, src_root, init=init, **kwargs)
        if init:
            self.construct(subject, src_root, **kwargs)

        for spec in self.pia_session_spec:
            if self.subject is None:
                raise RuntimeError("Subject is None")
            if spec.name in self.subject.sessions:
                self.subject.sessions[spec.name].default_importers[spec.importer_name] = spec.importer_type
                break
            Session.default_importers[spec.importer_name] = spec.importer_type
            self.subject.create_new_session(Session, spec.name, self.subject._mode)

    def import_sessions(self, path: Path):
        if self.subject is None:
            raise RuntimeError("Subject is None")
        for session in self.subject.sessions.values():
            session.create_importer("Pia", self.src_root).execute_import(path, session.name)

    def execute_import(self, path: Path, name: Optional[str]) -> None:
        if self.subject is None:
            raise RuntimeError("Subject is None")
        if name is None:
            name = self.subject.name
        new_path = path / f"sub-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_sessions(path=new_path)


# Assign Exporter
Subject.default_importers["Pia"] = SubjectPiaImporter
