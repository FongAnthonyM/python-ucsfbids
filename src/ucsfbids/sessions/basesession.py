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
from baseobjects.objects import DispatchableClass


# Local Packages #


# Definitions #
# Classes #
class BaseSession(CachingObject, BaseComposite, DispatchableClass):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    namespace: str | None = "base"
    registry: dict[str, dict[str, type]] = {}
    registration: bool = True
    default_meta_info: dict[str, Any] = {
        "SessionNamespace": "",
        "SessionType": "",
    }

    # Class Methods #
    # Registry
    @classmethod
    def register_class(cls, namespace: str | None = None, name: str | None = None) -> None:
        """Registers this class with the given namespace and name.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the subclass.
        """
        super().register_class(namespace=namespace, name=name)
        cls.default_meta_info.update(SessionNamespace=cls.namespace, SessionType=cls.name)

    @classmethod
    def get_class_information(
        cls,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> tuple[str, str]:
        """Gets a class namespace and name from a given set of arguments.

        Args:
            path: The path to the session.
            name: The name of the session.
            parent_path: The path to the parent of the session.
            *args: The arguments to get the namespace and name from.
            **kwargs: The keyword arguments to get the namespace and name from.

        Returns:
            The namespace and name of the class.
        """
        if path is not None:
            if name is None:
                name = path.stem[4:]
        elif parent_path is not None and name is not None:
            path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"ses-{name}"
        else:
            raise ValueError("Either path or (parent_path and name) must be given to disptach class.")

        parent_name = path.parts[-2][4:]

        meta_info_path = path / f"sub-{parent_name}_ses-{name}_meta.json"
        with meta_info_path.open("r") as file:
            info = json.load(file)

        return info["SessionNamespace"], info["SessionType"]

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str = 'r',
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
        mode: str | None = None,
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
                self.name = self.path.stem[4:]
        elif parent_path is not None and self.name is not None:
            self.path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"ses-{self.name}"

        if self.path is not None:
            self.parent_name = self.path.parts[-2][4:]
            
        if mode is not None:
            self._mode = mode

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
