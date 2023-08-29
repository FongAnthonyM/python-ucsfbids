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

    cdfs_type: type[CDFS] = CDFS

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str = 'r',
        create: bool = False,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.cdfs: CDFS | None = None

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
    # Constructors/Destructors
    def generate_contents_file_name(self) -> str:
        """Generates a name for the contents file from the subject and session name.

        Returns:
            The name of the contents file.
        """
        return f"{self.full_name}_contents.sqlite3"

    def require_cdfs(self, **kwargs: Any) -> CDFS:
        """Creates or loads the CDFS of this session.

        Args:
            **kwargs: The keyword arguments for creating the CDFS.

        Returns:
            The CDFS of this session.
        """
        self.cdfs = cdfs = self.cdfs_type(
            path=self.ieeg_path,
            name=self.full_name,
            mode=self._mode,
            contents_name=self.generate_contents_file_name(),
            **kwargs,
        )
        return cdfs

    def create_ieeg(self) -> None:
        """Creates and sets up the ieeg directory."""
        self.ieeg_path.mkdir(exist_ok=True)
        self.require_cdfs(open_=True, create=True)
        self.cdfs.close()
