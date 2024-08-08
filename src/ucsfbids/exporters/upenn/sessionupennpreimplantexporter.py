"""sessionupennpreimplantexporter.py

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
from ...modalities import Anatomy
from ..bids import SessionBIDSExporter
from .anatomyupennexporter import AnatomyUPENNExporter


# Definitions #
# Classes #
class SessionUPENNPreImplantExporter(SessionBIDSExporter):

    # Attributes #
    exporter_name: str = "UPENN"
    type_map: dict[type, (type, dict[str, Any])] = {
        Anatomy: (AnatomyUPENNExporter, {}),
    }
