"""basesubject.py

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
from .basesession import BaseSession


# Definitions #
# Classes #
class CDFSSession(BaseSession):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    cdfs_type: type[CDFS] = CDFS

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
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
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            path: The path to the subject's directory.
            name: The name of the session.
            parent_path: The parent path of this session.
        """

        super().construct(path=path, name=name, parent_path=parent_path, **kwargs)

    def generate_content_file_name(self):
        return f"{self.full_name}_contents.sqlite3"

    def require_cdfs(self, **kwargs: Any) -> CDFS:
        self.cdfs = cdfs = self.cdfs_type(
            path=self.ieeg_path,
            name=self.full_name,
            mode=self._mode,
            contents_name=self.generate_content_file_name(),
            **kwargs,
        )
        return cdfs

    def create_ieeg(self) -> None:
        self.ieeg_path.mkdir(exist_ok=True)
        self.require_cdfs(open_=True, create=True)
        self.cdfs.close()
