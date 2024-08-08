"""sessionexporter.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from pathlib import Path
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..base import BaseExporter


# Definitions #
# Classes #
class SessionExporter(BaseExporter):

    # Instance Methods #
    def export_modalities(
        self,
        path: Path,
        name_map: dict[str, str] | None = None,
        type_map: dict[type, type] | None = None,
        **kwargs: Any,
    ) -> None:
        if name_map is None:
            name_map = self.name_map

        if type_map is None:
            type_map = self.type_map

        if name_map:
            for modality_name, new_name in name_map.items():
                # Get modality
                modality = self.bids_object.modalities[modality_name]

                # Export using correct exporter type
                exporter, d_kwargs = type_map.get(type(modality), (None, {}))
                if exporter is not None:
                    exporter(bids_object=modality, **d_kwargs).execute_export(path, name=new_name)
                else:
                    exporter, d_kwargs = self.default_type
                    m_exporter = modality.require_exporter(self.exporter_name, exporter, **d_kwargs)
                    m_exporter.execute_export(path, name=new_name)
        else:
            for modality in self.bids_object.modalities.values():
                # Export using correct exporter type
                exporter, d_kwargs = type_map.get(type(modality), (None, {}))
                if exporter is not None:
                    exporter(bids_object=modality, **d_kwargs).execute_export(path)
                else:
                    exporter, d_kwargs = self.default_type
                    m_exporter = modality.require_exporter(self.exporter_name, exporter, **d_kwargs)
                    m_exporter.execute_export(path)

    def execute_export(
        self,
        path: Path,
        name: str | None = None,
        files: bool | set[str, ...] | None = True,
        inner: bool = True,
        name_map: dict[str, str] | None = None,
        type_map: dict[type, type] | None = None,
        **kwargs: Any,
    ) -> None:
        if name is None:
            name = self.bids_object.full_name

        new_path = path / name.split('_')[1]
        new_path.mkdir(exist_ok=True)
        if files or files is None:
            self.export_files(path=new_path, name=name, files=files)
        if inner:
            self.export_modalities(path=new_path, name_map=name_map)
