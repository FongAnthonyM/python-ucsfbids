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
from .anatomybidsimporter import AnatomyBIDSImporter
from .ctbidsimporter import CTBIDSImporter 
from .ieegbidsimporter import IEEGBIDSImporter 
