"""anatomybidsexporter.py

"""
# Package Header #
from ucsfbids.header import *

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

from ...anatomy import Anatomy

# Local Packages #
from ..modalitybidsimporter import ModalityBIDSImporter

# Third-Party Packages #


# Definitions #
# Classes #
class AnatomyBIDSImporter(ModalityBIDSImporter):
    pass


Anatomy.default_importers["BIDS"] = AnatomyBIDSImporter
