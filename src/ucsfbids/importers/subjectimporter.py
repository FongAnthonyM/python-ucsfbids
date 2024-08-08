"""subjectimporter.py

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
class SubjectImporter(BaseImporter):
    # Instance Methods #
    def import_sessions(
        self,
        path: Path,
        inner_maps: list[tuple[str, type, dict[str, Any], str, type, dict[str, Any]]] | None = None,
        **kwargs: Any,
    ) -> None:
        if inner_maps is None:
            inner_maps = self.inner_maps

        for s_name, s_type, s_kwargs, i_name, importer, i_kwargs in inner_maps:
            # Correct names
            if s_name[:4] == "ses-":
                s_name = s_name[4:]
            
            session = self.bids_object.sessions.get(s_name, None)
            if session is None:
                self.bids_object.create_session(s_name, s_type, **({"create": True, "build": True} | s_kwargs))

            if importer is None:
                importer, i_kwargs = session.importers.get(i_name, (None, {}))

            if importer is None:
                importer, i_kwargs = self.default_type

            importer(bids_object=session, **i_kwargs).execute_import(path)

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
            self.import_sessions(path=path, inner_maps=inner_maps)
