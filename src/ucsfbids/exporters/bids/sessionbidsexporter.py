"""subject.py

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

# Third-Party Packages #

# Local Packages #
from ...sessions import Session
from ..sessionexporter import SessionExporter
from .modalitybidsexporter import ModalityBIDSExporter


# Definitions #
# Classes #
class SessionBIDSExporter(SessionExporter):

    # Attributes #
    exporter_name: str = "BIDS"
    default_type: type = (ModalityBIDSExporter, {})


# Assign Exporter
Session.exporters["BIDS"] = (SessionBIDSExporter, {})
