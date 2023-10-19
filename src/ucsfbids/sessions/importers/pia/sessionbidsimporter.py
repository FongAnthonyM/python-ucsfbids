"""subject.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __maintainer__, __email__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from baseobjects import BaseObject
from pathlib import Path
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...session import Session
from ..sessionbidsimporter import SessionBIDSImporter
from ....modalities.importers import pia


# Definitions #
# Classes #
class SessionPiaImporter(SessionBIDSImporter):
    # Magic Methods #
    def import_modalities(self, path: Path):
        if self.session is None:
            raise RuntimeError("Undefined Session.")
        for modality in self.session.modalities.values():
            modality.create_importer("Pia", self.src_root).execute_import(path)

    def execute_import(self, path: Path, name: str | None = None) -> None:
        if self.session is None:
            raise RuntimeError("Undefined Session.")
        if name is None:
            name = self.session.name

        new_path = path / f"ses-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_modalities(path=new_path)


# Assign Exporter
Session.default_importers["Pia"] = SessionPiaImporter
