""" __init__.py

"""
# Package Header #
from ucsfbids.header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Local Packages #
from .anatomyenigmaimporter import AnatomyEnigmaImporter  # noqa
from .ctenigmaimporter import CTEnigmaImporter  # noqa
from .dtienigmaimporter import DTIEnigmaImporter  # noqa
