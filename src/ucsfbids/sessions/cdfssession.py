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
import pathlib
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
        path: pathlib.Path | str | None = None,
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
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        path: pathlib.Path | str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            path: The path to the subject's directory.
        """

        super().construct(**kwargs)

    def create_anat(self) -> None:
        pass

    def create_ieeg(self) -> None:
        pass

    def require_cdfs(self) -> None:
        self.cdfs = self.cdfs_type(path=self.ieeg_path, s_id=self.full_name, mode=self._mode)
