"""ieegcdfs.py

"""
# Package Header #
from ....header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from typing import Any

# Third-Party Packages #
from baseobjects.composition import BaseComponent
from cdfs import BaseCDFS

# Local Packages #


# Definitions #
# Classes #
class IEEGCDFSComponent(BaseComponent):
    # Attributes #
    cdfs_type: type[BaseCDFS] = BaseCDFS
    cdfs: BaseCDFS | None = None

    # Instance Methods #
    # Construction/Destruction
    def construct_cdfs(self, file_name: str | None = None, create: bool = False, **kwargs: Any) -> BaseCDFS:
        """Creates or loads the CDFS of this modality.

        Args:
            **kwargs: The keyword arguments for creating the CDFS.

        Returns:
            The CDFS of this session.
        """
        if file_name is None:
            file_name = self.generate_contents_file_name()

        composite = self._composite()
        self.cdfs = cdfs = self.cdfs_type(
            path=composite.path,
            name=composite.full_name,
            mode=composite._mode,
            create=create,
            contents_name=file_name,
            **kwargs,
        )
        return cdfs

    def build(self) -> None:
        self.construct_cdfs(create=True, build=True)

    def load(self) -> None:
        self.construct_cdfs(open_=True, create=False)

    def generate_contents_file_name(self) -> str:
        """Generates a name for the contents file from the subject and session name.

        Returns:
            The name of the contents file.
        """
        return f"{self._composite().full_name}_contents.sqlite3"



