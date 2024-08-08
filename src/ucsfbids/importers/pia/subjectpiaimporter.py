""""subjectpiaimporter.py

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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...sessions import Session
from ...subjects import Subject
from ..subjectimporter import SubjectImporter
from .sessionpiaimporter import SessionPiaImporter


# Definitions #
# Classes #
class SubjectPiaImporter(SubjectImporter):

    # Attributes #
    importer_name: str = "Pia"

    inner_maps: list[tuple[str, type, dict[str, Any], str, type, dict[str, Any]]] = [
        ("clinicalintracranial", Session, {}, "Pia", SessionPiaImporter, {}),
    ]


# Assign Importer
Subject.importers["Pia"] = (SubjectPiaImporter, {})
