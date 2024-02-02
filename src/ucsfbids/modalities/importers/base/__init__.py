""" __init__.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Local Packages #
from .anatomyimporter import AnatomyImporter  # noqa
from .ctimporter import CTImporter  # noqa
from .ieegimporter import IEEGImporter  # noqa
from .dtiimporter import DTIImporter  # noqa
