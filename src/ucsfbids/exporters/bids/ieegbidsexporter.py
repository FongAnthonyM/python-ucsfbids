"""ieegbidsexporter.py

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
from ...modalities import IEEG
from .modalitybidsexporter import ModalityBIDSExporter


# Definitions #
# Classes #
class IEEGBIDSExporter(ModalityBIDSExporter):

    # Attributes #
    export_file_names: set[str, ...] = {"ieeg", "coordsystem", "electrodes", "channels", "photo"}
    export_exclude_names: set[str, ...] = {"ieeg_meta"}


# Assign Exporter
IEEG.exporters["BIDS"] = (IEEGBIDSExporter, {})
