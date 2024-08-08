"""sessionupennimplantexporter.py

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
from xltektools.xltekucsfbids.modalities.ieegxltek import IEEGXLTEK

# Local Packages #
from ...modalities import CT
from ..bids import SessionBIDSExporter
from .ctupennexporter import CTUPENNExporter
from .ieegupennexporter import IEEGUPENNExporter


# Definitions #
# Classes #
class SessionUPENNImplantExporter(SessionBIDSExporter):

    # Attributes #
    exporter_name: str = "UPENN"
    type_map: dict[type, (type, dict[str, Any])] = {
        IEEGXLTEK: (IEEGUPENNExporter, {}),
        CT: (CTUPENNExporter, {}),
    }

