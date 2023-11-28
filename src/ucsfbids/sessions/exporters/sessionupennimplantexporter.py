from pathlib import Path

from xltektools.xltekucsfbids.modalities.ieegxltek import IEEGXLTEK

from ucsfbids.modalities import CT, IEEG
from ucsfbids.modalities.exporters.ctupennexporter import CTUPENNExporter
from ucsfbids.modalities.exporters.ieegupennexporter import IEEGUPENNExporter
from ucsfbids.sessions.exporters import SessionBIDSExporter


class SessionUPENNImplantExporter(SessionBIDSExporter):
    def export_modalities(self, path: Path, name: str):
        assert self.session is not None

        for mod in self.session.modalities.values():
            if isinstance(mod, IEEG):
                mod = IEEGXLTEK(mod.path, mod.name)
                mod.add_exporter("UPENN", IEEGUPENNExporter)
            elif isinstance(mod, IEEGXLTEK):
                print("works!")
                mod.add_exporter("UPENN", IEEGUPENNExporter)
            elif isinstance(mod, CT):
                mod.add_exporter("UPENN", CTUPENNExporter)
            else:
                continue

            mod.create_exporter("UPENN").execute_export(path, name=name)
