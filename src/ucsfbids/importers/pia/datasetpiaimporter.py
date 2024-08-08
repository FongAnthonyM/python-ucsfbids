""""datasetpiaimporter.py

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
from ...datasets import Dataset
from ..datasetimporter import DatasetImporter


# Definitions #
# Classes #
class DatasetPiaImporter(DatasetImporter):

    # Attributes #
    importer_name: str = "Pia"


# Assign Importer
Dataset.importers["Pia"] = (DatasetPiaImporter, {})
