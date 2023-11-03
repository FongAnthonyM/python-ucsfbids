""" __init__.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


from .base import AnatomyImporter, CTImporter, IEEGImporter

# Imports #
# Local Packages #
from .modalityimporter import ModalityImporter
