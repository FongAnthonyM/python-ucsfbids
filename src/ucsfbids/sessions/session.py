"""session.py
A base class which defines a Session and dispatches a specific Session subclass based on meta information.
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
from ..modalities import Modality


# Definitions #
# Classes #
class Session(CachingObject, DispatchableClass):
    """A base class which defines a Session and dispatches a specific Session subclass based on meta information.

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
        "SessionNamespace": "",
        "SessionType": "",
    }
    default_modalities: dict[str, Any] = {}
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
        cls.default_meta_info.update(SessionNamespace=cls.register_namespace, SessionType=cls.register_name)

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
            if not isinstance(path, Path):  # NOTE: path was parent_path on this line
                path = Path(path)

            if name is None:
                name = path.stem[4:]
        elif parent_path is not None and name is not None:
            path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"ses-{name}"
        else:
            raise ValueError("Either path or (parent_path and name) must be given to disptach class.")

        parent_name = path.parts[-2][4:]

        meta_info_path = path / f"sub-{parent_name}_ses-{name}_meta.json"
        if not meta_info_path.exists():
            info = cls.default_meta_info
        else:
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
        mode: str = "r",
        create: bool = False,
        load: bool = True,
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

        self.meta_info: dict = self.default_meta_info.copy()
        self.modalities: dict[str, Any] = {}

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
                load=load,
                **kwargs,
            )

    @property
    def path(self) -> Path | None:
        """The path to the session."""
        return self._path  # WARN: path can be none

    @path.setter
    def path(self, value: str | Path) -> None:
        if isinstance(value, Path) or value is None:
            self._path = value
        else:
            self._path = Path(value)

    @property
    def full_name(self) -> str:
        """The fill name of this session, including subject."""
        return f"sub-{self.parent_name}_ses-{self.name}"

    @property
    def meta_info_path(self) -> Path:
        """The path to the meta information json file."""
        assert self._path is not None
        return self._path / f"{self.full_name}_meta.json"

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str | None = None,
        create: bool = False,
        load: bool = False,
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
                self.name = self.path.stem[4:]
        elif parent_path is not None and self.name is not None:
            self.path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"ses-{self.name}"

        assert self.path is not None
        # if self.path is not None:
        self.parent_name = self.path.parts[-2][4:]

        if mode is not None:
            self._mode = mode

        if not load:
            self.build_default_modalities()

        if self.path is not None:
            if load and self.path.exists():
                self.load_modalities()
            elif create:
                self.create()

        super().construct(**kwargs)

    def create_meta_info(self) -> None:
        """Creates meta information file and saves the meta information."""
        with self.meta_info_path.open(self._mode) as file:
            json.dump(self.meta_info, file)

    def load_meta_info(self) -> dict:
        """Loads the meta information from the file.

        Returns:
            The session meta information.
        """
        self.meta_info.clear()
        with self.meta_info_path.open("r") as file:
            self.meta_info.update(json.load(file))
        return self.meta_info

    def save_meta_info(self) -> None:
        """Saves the meta information to the file."""
        with self.meta_info_path.open(self._mode) as file:
            json.dump(self.meta_info, file)

    def build_default_modalities(self) -> None:
        for name, modality_type in self.default_modalities.items():
            self.modalities[name] = modality_type(parent_path=self.path, mode=self._mode)

    def create_modalities(self) -> None:
        for modality in self.modalities.values():
            modality.create()

    def create(self) -> None:
        """Creates all contents of the session."""
        if self.path is not None:
            self.path.mkdir(exist_ok=True)
        self.create_meta_info()
        self.create_modalities()

    def load_modalities(self, mode: str | None = None) -> None:
        """Loads all modalities in this session."""
        mode = self._mode if mode is None else mode
        self.modalities.clear()
        self.modalities.update(
            {m.name: m for p in self.path.iterdir() if p.is_dir() and (m := Modality(path=p, mode=mode)) is not None},
        )

    def create_importer(self, type_: str, src_root: Path | None, **kwargs) -> Any:
        return self.importers[type_](session=self, src_root=src_root, **kwargs)

    def create_exporter(self, type_):
        return self.exporters[type_](session=self)

    def add_importer(self, type_: str, importer: type, overwrite: bool = False):
        if type_ not in self.importers or overwrite:
            self.importers[type_] = importer

    def add_exporter(self, type_: str, exporter: type, overwrite: bool = False):
        if type_ not in self.exporters or overwrite:
            self.exporters[type_] = exporter
