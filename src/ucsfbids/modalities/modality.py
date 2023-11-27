"""modality.py
A base class which defines a Modality and dispatches a specific Modality subclass based on meta information.
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

import pandas as pd

# Third-Party Packages #
from baseobjects import BaseComposite
from baseobjects.cachingtools.cachingobject import CachingObject
from baseobjects.objects.dispatchableclass import DispatchableClass

# Local Packages #


# Definitions #
# Classes #
class Modality(CachingObject, BaseComposite, DispatchableClass):
    """A base class which defines a Modality and dispatches a specific Modality subclass based on meta information.

    Class Attributes:
        namespace: The namespace of the subclass.
        name: The name of which the subclass will be registered as.
        register: A register of all subclasses of this class.
        registration: Determines if this class/subclass will be added to the register.
        default_meta_info: The default meta information about the session.

    Attributes:
        _path: The path to session.
        _is_open: Determines if this session and its contents are open.
        _mode: The file mode of this session.
        meta_info: The meta information that describes this session.
        name: The name of this session.
        parent_name: The name of the parent subject of this session.

    Args:
        path: The path to the session's directory.
        name: The name of the session.
        parent_path: The parent path of this session.
        mode: The file mode to set this session to.
        create: Determines if this session will be created if it does not exist.
        init: Determines if this object will construct.
        kwargs: The keyword arguments for inheritance if any.
    """

    register: dict[str, dict[str, type]] = {}
    registration: bool = True
    default_meta_info: dict[str, Any] = {
        "ModalityNamespace": "",
        "ModalityType": "",
    }
    default_name: str = ""
    default_importers: dict[str, type] = {}
    default_exporters: dict[str, type] = {}

    # Class Methods #
    # register
    @classmethod
    def register_class(cls, namespace: str | None = None, name: str | None = None) -> None:
        """Registers this class with the given namespace and name.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the subclass.
        """
        super().register_class(namespace=namespace, name=name)
        cls.default_meta_info.update(ModalityNamespace=cls.register_namespace, ModalityType=cls.register_name)

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
            if not isinstance(parent_path, Path):
                path = Path(path)

            if name is None:
                name = path.stem
        elif parent_path is not None and name is not None:
            path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"{name}"
        else:
            raise ValueError("Either path or (parent_path and name) must be given to disptach class.")

        subject_name = path.parts[-3][4:]
        session_name = path.parts[-2][4:]

        meta_info_path = path / f"sub-{subject_name}_ses-{session_name}_{name}-meta.json"
        with meta_info_path.open("r") as file:
            info = json.load(file)

        return info["ModalityNamespace"], info["ModalityType"]

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
        self._path: Path | None = None
        self._is_open: bool = False
        self._mode: str = "r"

        self.meta_info: dict = self.default_meta_info.copy()

        self.name: str = self.default_name
        self.subject_name: str | None = None
        self.session_name: str | None = None

        self.importers: dict[str, type] = self.default_importers.copy()
        self.exporters: dict[str, type] = self.default_exporters.copy()

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

    @property
    def path(self) -> Path:
        """The path to the session."""
        return self._path

    @path.setter
    def path(self, value: str | Path) -> None:
        if isinstance(value, Path) or value is None:
            self._path = value
        else:
            self._path = Path(value)

    @property
    def full_name(self) -> str:
        """The fill name of this session, including subject."""
        return f"sub-{self.subject_name}_ses-{self.session_name}"

    @property
    def meta_info_path(self) -> Path:
        """The path to the meta information json file."""
        return self._path / f"{self.full_name}_{self.name}-meta.json"

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str | None = None,
        create: bool = False,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            path: The path to the session's directory.
            name: The name of the session.
            parent_path: The parent path of this session.
            mode: The file mode to set this session to.
            create: Determines if this session will be created if it does not exist.
            kwargs: The keyword arguments for inheritance if any.
        """
        if name is not None:
            self.name = name

        if path is not None:
            self.path = path

        if self.path is not None:
            if name is None:
                self.name = self.path.stem
        elif parent_path is not None and self.name is not None:
            self.path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"{self.name}"

        if self.path is not None:
            self.subject_name = self.path.parts[-3][4:]
            self.session_name = self.path.parts[-2][4:]

        if mode is not None:
            self._mode = mode

        if create:
            self.create()

        super().construct(**kwargs)

    def create_meta_info(self) -> None:
        """Creates meta information file and saves the meta information."""
        with self.meta_info_path.open(self._mode) as file:
            json.dump(self.meta_info, file)

    def load_meta_info(self) -> dict:
        """Loads the meta information from the file.

        Returns:
            The modality meta information.
        """
        self.meta_info.clear()
        with self.meta_info_path.open("r") as file:
            self.meta_info.update(json.load(file))
        return self.meta_info

    def save_meta_info(self) -> None:
        """Saves the meta information to the file."""
        with self.meta_info_path.open(self._mode) as file:
            json.dump(self.meta_info, file)

    def create(self) -> None:
        """Creates all contents of the modality."""
        self.path.mkdir(exist_ok=True)
        self.create_meta_info()

    def create_importer(self, type_: str, src_root: Path | None, **kwargs) -> Any:
        return self.importers[type_](modality=self, src_root=src_root, **kwargs)


    def create_exporter(self, type_: str) -> Any:
        return self.exporters[type_](modality=self)

    def add_importer(self, type_: str, importer: type, overwrite: bool = False):
        if type_ not in self.importers or overwrite:
            self.importers[type_] = importer
