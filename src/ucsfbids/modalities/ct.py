"""ct.py
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
from .modality import Modality
from .exporters import CTBIDSExporter
from .importers import CTBIDSImporter


# Definitions #
# Classes #
class CT(Modality):
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

    default_meta_info: dict[str, Any] = Modality.default_meta_info.copy()
    default_name: str = "ct"
    default_exporters: dict[str, type] = {"BIDS": CTBIDSExporter}
    default_importers: dict[str, type] = {"BIDS": CTBIDSImporter}

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str = "r",
        create: bool = False,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                path=path,
                name=name,
                parent_path=parent_path,
                mode=mode,
                create=create,
                **kwargs,
            )

    # Instance Methods #
    def create(self) -> None:
        """Creates and sets up the ct directory."""
        self.path.mkdir(exist_ok=True)
        self.create_meta_info()
