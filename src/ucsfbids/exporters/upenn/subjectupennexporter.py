"""subjectupennexporter.py

"""
# Package Header #
from ...header import *

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
from xltektools.xltekucsfbids.sessions.xltekucsfbidssession import XLTEKUCSFBIDSSession

# Local Packages #
from ..bids import SubjectBIDSExporter
from .sessionupennimplantexporter import SessionUPENNImplantExporter
from .sessionupennpreimplantexporter import SessionUPENNPreImplantExporter


# Definitions #
# Classes #
class SubjectUPENNExporter(SubjectBIDSExporter):
    # Attributes #
    exporter_name: str = "UPENN"

    # Instance Methods #
    def export_sessions(
        self,
        path: Path,
        name_map: dict[str, str] | None = None,
        type_map: dict[type, type] | None = None,
        **kwargs: Any,
    ) -> None:
        non_cdfs_session = self.bids_object.sessions["clinicalintracranial"]
        session = XLTEKUCSFBIDSSession(
            path=non_cdfs_session.path,
            name=non_cdfs_session.name,
            mode="r",
        )
        implant = session.require_exporter("UPENNImplant", SessionUPENNImplantExporter)
        implant.execute_export(path, name="implant01")
        preimplant = session.require_exporter("UPENNPreImplant", SessionUPENNPreImplantExporter)
        preimplant.execute_export(path, name="preimplant01")
