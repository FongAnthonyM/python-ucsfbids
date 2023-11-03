"""ctbidsexporter.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


from pathlib import Path
from typing import Any

# Imports #
# Standard Libraries #
from baseobjects import BaseObject

from ...ct import CT

# Local Packages #
from ..modalityimporter import ModalityImporter

# Third-Party Packages #


# Definitions #
# Classes #
class CTImporter(ModalityImporter):
    pass


CT.default_importers["BIDS"] = CTImporter
