"""anatomybidsexporter.py

"""
# Package Header #
from ucsfbids.header import *

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
from .modalitybidsexporter import ModalityBIDSExporter


# Definitions #
# Classes #
class AnatomyBIDSExporter(ModalityBIDSExporter):
    pass
