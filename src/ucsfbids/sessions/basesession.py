"""basesession.py

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


# Local Packages #


# Definitions #
# Classes #
class BaseSession(CachingObject, BaseComposite):
    """

    Class Attributes:

    Attributes:

    Args:

    """
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
        self._path: Path | None = None
        self._is_open: bool = False
        self._mode: str = "r"

        self.name: str | None = None
        self.parent_name: str | None = None

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

    @property
    def path(self) -> Path:
        """The path to the subject."""
        return self._path

    @path.setter
    def path(self, value: str | Path) -> None:
        if isinstance(value, Path) or value is None:
            self._path = value
        else:
            self._path = Path(value)

    @property
    def full_name(self) -> str:
        return f"sub-{self.parent_name}_ses-{self.name}"

    @property
    def ieeg_path(self) -> Path:
        """The path to the ieeg data."""
        return self._path / "ieeg"

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
        if name is not None:
            self.name = name

        if path is not None:
            self.path = path

        if self.path is not None:
            if name is None:
                self.name = self.path.stem.lstrip[4:]
        elif parent_path is not None and self.name is not None:
            self.path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"ses-{self.name}"

        if self.path is not None:
            self.parent_name = self.path.parts[-2][4:]

        super().construct(**kwargs)

    def create_anat(self) -> None:
        pass

    def create_ieeg(self) -> None:
        pass
