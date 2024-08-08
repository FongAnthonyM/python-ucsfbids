""""sessionpiaimporter.py

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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...modalities import CT, IEEG, Anatomy
from ...sessions import Session
from ..sessionimporter import SessionImporter
from .anatomypiaimporter import AnatomyPiaImporter
from .ctpiaimporter import CTPiaImporter
from .ieegpiaimporter import IEEGPiaImporter


# Definitions #
# Classes #
class SessionPiaImporter(SessionImporter):

    # Attributes #
    importer_name: str = "Pia"

    inner_maps: list[tuple[str, type, dict[str, Any], str, type, dict[str, Any]]] = [
        ("anat", Anatomy, {}, "Pia", AnatomyPiaImporter, {}),
        ("ieeg", IEEG, {}, "Pia", IEEGPiaImporter, {}),
        ("ct", CT, {}, "Pia", CTPiaImporter, {}),
    ]


# Assign Importer
Session.importers["Pia"] = (SessionPiaImporter, {})
