"""ctbidsexporter.py

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
from ...modalities import CT
from .modalitybidsexporter import ModalityBIDSExporter


# Definitions #
# Classes #
class CTBIDSExporter(ModalityBIDSExporter):
    pass


# Assign Exporter
CT.exporters["BIDS"] = (CTBIDSExporter, {})
