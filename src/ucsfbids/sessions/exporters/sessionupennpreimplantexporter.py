from pathlib import Path

from ucsfbids.modalities.anatomy import Anatomy
from ucsfbids.modalities.exporters.anatomyupennexporter import AnatomyUPENNExporter
from ucsfbids.sessions.exporters import SessionBIDSExporter


class SessionUPENNPreImplantExporter(SessionBIDSExporter):
    def export_modalities(self, path: Path, name: str):
        assert self.session is not None
        for modality in self.session.modalities.values():
            if isinstance(modality, Anatomy):
                modality.add_exporter("UPENN", AnatomyUPENNExporter)
                modality.create_exporter("UPENN").execute_export(path, name=name)
