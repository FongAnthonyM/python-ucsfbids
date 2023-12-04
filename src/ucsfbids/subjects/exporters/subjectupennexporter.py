from pathlib import Path

from xltektools.xltekucsfbids import IEEGXLTEK
from xltektools.xltekucsfbids.sessions.xltekucsfbidssession import XLTEKUCSFBIDSSession

from ucsfbids.sessions.exporters.sessionupennimplantexporter import SessionUPENNImplantExporter
from ucsfbids.sessions.exporters.sessionupennpreimplantexporter import SessionUPENNPreImplantExporter
from ucsfbids.subjects.exporters import SubjectBIDSExporter


class SubjectUPENNExporter(SubjectBIDSExporter):
    def export_sessions(self, path: Path):
        assert self.subject is not None
        non_cdfs_session = self.subject.sessions["clinicalintracranial"]
        session = XLTEKUCSFBIDSSession(
            path=non_cdfs_session.path,
            name=non_cdfs_session.name,
            mode="r",
        )
        session.add_exporter("UPENNImplant", SessionUPENNImplantExporter)
        session.create_exporter("UPENNImplant").execute_export(path, name="implant01")
        session.add_exporter("UPENNPreImplant", SessionUPENNPreImplantExporter)
        session.create_exporter("UPENNPreImplant").execute_export(path, name="preimplant01")
