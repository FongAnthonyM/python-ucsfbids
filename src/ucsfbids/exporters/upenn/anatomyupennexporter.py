"""anatomyupennexporter.py

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
from ..bids import AnatomyBIDSExporter


# Definitions #
# Classes #
class AnatomyUPENNExporter(AnatomyBIDSExporter):

    # Attributes #
    exporter_name: str = "UPENN"