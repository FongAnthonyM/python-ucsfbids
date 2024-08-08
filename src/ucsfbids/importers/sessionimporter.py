"""sessionimporter.py

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
from ..base import BaseImporter


# Definitions #
# Classes #
class SessionImporter(BaseImporter):
    # Instance Methods #
    def import_modalities(
        self,
        path: Path,
        inner_maps: list[tuple[str, type, dict[str, Any], str, type, dict[str, Any]]] | None = None,
        **kwargs: Any,
    ) -> None:
        if inner_maps is None:
            inner_maps = self.inner_maps

        for m_name, m_type, m_kwargs, i_name, importer, i_kwargs in inner_maps:
            modality = self.bids_object.modalities.get(m_name, None)
            if modality is None:
                self.bids_object.create_modality(m_name, m_type, **({"create": True, "build": True} | m_kwargs))

            if importer is None:
                importer, i_kwargs = modality.importers.get(i_name, (None, {}))

            if importer is None:
                importer, i_kwargs = self.default_type

            importer(bids_object=modality, **i_kwargs).execute_import(path)

    def execute_import(
        self,
        path: Path,
        file_maps: bool | list[tuple] | None = True,
        inner_maps: bool | list[tuple[str, type, dict[str, Any], str, type, dict[str, Any]]] | None = True,
        **kwargs: Any,
    ) -> None:
        self.bids_object.create(build=False)
        if file_maps or file_maps is None:
            self.import_files(path=path, file_maps=file_maps)
        if inner_maps or inner_maps is None:
            self.import_modalities(path=path, inner_maps=inner_maps)
