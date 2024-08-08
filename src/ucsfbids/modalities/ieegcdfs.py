"""ieegcdfs.py

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
from typing import Any

# Third-Party Packages #
from cdfs import BaseCDFS

# Local Packages #
from ..base import BaseImporter, BaseExporter
from ...exporters import IEEGBIDSExporter
from .ieeg import IEEG


# Definitions #
# Classes #
class IEEGCDFS(IEEG):
    """A Session which contains a CDFS as part of its structure.

    Class Attributes:
        namespace: The namespace of the subclass.
        name: The name of which the subclass will be registered as.
        registry: A registry of all subclasses of this class.
        registration: Determines if this class/subclass will be added to the registry.
        meta_information: The default meta information about the session.
        cdfs_type: The type of CDFS the session objects of this class will use.

    Attributes:
        _path: The path to session.
        _is_open: Determines if this session and its contents are open.
        _mode: The file mode of this session.
        meta_info: The meta information that describes this session.
        name: The name of this session.
        subject_name: The name of the parent subject of this session.
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

    # Attributes #
    meta_information: dict[str, Any] = IEEG.meta_information.copy()

    cdfs_type: type[BaseCDFS] = BaseCDFS
    cdfs: BaseCDFS | None = None

    importers: dict[str, tuple[type[BaseImporter], dict[str, Any]]] = {}
    exporters: dict[str, tuple[type[BaseExporter], dict[str, Any]]] = {"BIDS": (IEEGBIDSExporter, {})}

    # Instance Methods #
    def build(self) -> None:
        super().build()
        self.require_cdfs(open_=True)
        self.cdfs.close()

    def generate_contents_file_name(self) -> str:
        """Generates a name for the contents file from the subject and session name.

        Returns:
            The name of the contents file.
        """
        return f"{self.full_name}_contents.sqlite3"

    def require_cdfs(self, **kwargs: Any) -> BaseCDFS:
        """Creates or loads the CDFS of this session.

        Args:
            **kwargs: The keyword arguments for creating the CDFS.

        Returns:
            The CDFS of this session.
        """
        self.cdfs = cdfs = self.cdfs_type(
            path=self.path,
            name=self.full_name,
            mode=self._mode,
            create=True,
            contents_name=self.generate_contents_file_name(),
            **kwargs,
        )
        return cdfs

