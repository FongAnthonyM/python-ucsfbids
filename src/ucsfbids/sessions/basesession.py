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
import json
from pathlib import Path
from typing import Any


# Third-Party Packages #
from baseobjects import BaseComposite
from baseobjects.cachingtools import CachingObject, timed_keyless_cache


# Local Packages #


# Definitions #
# Classes #
class BaseSession(CachingObject, BaseComposite):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_meta_info: dict = {
        "SessionType": "Base"
    }

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

        self.meta_info: dict = self.default_meta_info.copy()

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
    def meta_info_path(self) -> Path:
        return self._path / f"{self.full_name}_meta.json"

    @property
    def anat_path(self) -> Path:
        """The path to the ieeg data."""
        return self._path / "anat"

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

    def create_meta_info(self) -> None:
        with self.meta_info_path.open("w") as file:
            json.dump(self.meta_info, file)

    def load_meta_info(self) -> dict:
        self.meta_info.clear()
        with self.meta_info_path.open("r") as file:
            self.meta_info.update(json.load(file))
        return self.meta_info

    def save_meta_info(self) -> None:
        with self.meta_info_path.open("w") as file:
            json.dump(self.meta_info, file)

    def create_anat(self) -> None:
        self.anat_path.mkdir(exist_ok=True)

    def create_ieeg(self) -> None:
        self.ieeg_path.mkdir(exist_ok=True)

    def create(self) -> None:
        self.path.mkdir(exist_ok=True)
        self.create_meta_info()
        self.create_anat()
        self.create_ieeg()

    def export_to_bids(self, path: Path | str) -> None:
        pass
