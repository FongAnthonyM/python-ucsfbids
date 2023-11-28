from pathlib import Path
from typing import Any

from xltektools.xltekucsfbids.modalities.exporters.ieegxltekbidsexporter import IEEGXLTEKBIDSExporter


class IEEGUPENNExporter(IEEGXLTEKBIDSExporter):
    default_export_file_names = {"coordsystem.json", "electrodes.tsv"}

    def construct(self, modality: None = None, **kwargs: Any) -> None:
        if modality is not None:
            self.modality = modality

        self.export_file_names = self.default_export_file_names
        super().construct(**kwargs)
