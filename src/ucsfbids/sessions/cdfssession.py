"""cdfssession.py
A Session which contains a CDFS as part of its structure.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from baseobjects import BaseComposite
from baseobjects.cachingtools import CachingObject, timed_keyless_cache
from pathlib import Path
from typing import Any

# Third-Party Packages #
from cdfs import CDFS

# Local Packages #
from .session import Session
from .exporters import SessionBIDSExporter
from ..modalities import Modality, Anatomy, CT, IEEGCDFS


# Definitions #
# Classes #
class CDFSSession(Session):
    """A Session which contains a CDFS as part of its structure.

    Class Attributes:
        namespace: The namespace of the subclass.
        name: The name of which the subclass will be registered as.
        registry: A registry of all subclasses of this class.
        registration: Determines if this class/subclass will be added to the registry.
        default_meta_info: The default meta information about the session.
        cdfs_type: The type of CDFS the session objects of this class will use.

    Attributes:
        _path: The path to session.
        _is_open: Determines if this session and its contents are open.
        _mode: The file mode of this session.
        meta_info: The meta information that describes this session.
        name: The name of this session.
        parent_name: The name of the parent subject of this session.
        cdfs: The CDFS object of this session.

    Args:
        path: The path to the session's directory.
        name: The name of the session.
        parent_path: The parent path of this session.
        mode: The file mode to set this session to.
        create: Determines if this session will be created if it does not exist.
        init: Determines if this object will construct.
        kwargs: The keyword arguments for inheritance.
    """

    default_meta_info: dict[str, Any] = Session.default_meta_info.copy()
    default_modalities: dict[str, type[Modality]] = {"anat": Anatomy, "ct": CT, "ieeg": IEEGCDFS}
    default_exporters: dict[str, type] = {"BIDS": SessionBIDSExporter}
