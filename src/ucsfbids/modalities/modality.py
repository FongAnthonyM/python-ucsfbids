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
from collections.abc import MutableMapping
from collections import ChainMap
import json
from pathlib import Path
from typing import Any

# Third-Party Packages #
from baseobjects.objects.dispatchableclass import DispatchableClass

# Local Packages #
from ..base import BaseBIDSDirectory, BaseImporter, BaseExporter


# Definitions #
# Classes #
class Modality(BaseBIDSDirectory, DispatchableClass):
    """A base class which defines a Modality and dispatches a specific Modality subclass based on meta information.

    Class Attributes:
        namespace: The namespace of the subclass.
        name: The name of which the subclass will be registered as.
        register: A register of all subclasses of this class.
        registration: Determines if this class/subclass will be added to the register.
        meta_information: The default meta information about the session.

    Attributes:
        _path: The path to session.
        _is_open: Determines if this session and its contents are open.
        _mode: The file mode of this session.
        meta_info: The meta information that describes this session.
        name: The name of this session.
        subject_name: The name of the parent subject of this session.

    Args:
        path: The path to the session's directory.
        name: The name of the session.
        parent_path: The parent path of this session.
        mode: The file mode to set this session to.
        create: Determines if this session will be created if it does not exist.
        init: Determines if this object will construct.
        kwargs: The keyword arguments for inheritance if any.
    """

    # Class Attributes #
    register: dict[str, dict[str, type]] = {}
    registration: bool = True

    # Class Methods #
    @classmethod
    def register_class(cls, namespace: str | None = None, name: str | None = None) -> None:
        """Registers this class with the given namespace and name.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the subclass.
        """
        super().register_class(namespace=namespace, name=name)
        cls.meta_information.update(ModalityNamespace=cls.register_namespace, ModalityType=cls.register_name)

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
            if not isinstance(path, Path):
                path = Path(path)

            if name is None:
                name = path.stem
        elif parent_path is not None and name is not None:
            path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"{name}"
        else:
            raise ValueError("Either path or (parent_path and name) must be given to dispatch class.")

        subject_name = path.parts[-3][4:]
        session_name = path.parts[-2][4:]

        meta_info_path = path / f"sub-{subject_name}_ses-{session_name}_{name}-meta.json"
        with meta_info_path.open("r") as file:
            info = json.load(file)

        return info["ModalityNamespace"], info["ModalityType"]

    # Attributes #
    subject_name: str | None = None
    session_name: str | None = None

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]] = ChainMap()
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]] = ChainMap()

    meta_information: dict[str, Any] = {
        "ModalityNamespace": "",
        "ModalityType": "",
    }

    # Properties #
    @property
    def directory_name(self) -> str:
        """The directory name of this Modality."""
        return self.name

    @property
    def full_name(self) -> str:
        """The full name of this Modality."""
        return f"sub-{self.subject_name}_ses-{self.session_name}"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str | None = None,
        create: bool = False,
        build: bool = True,
        load: bool = True,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #

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
                build=build,
                load=load,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str | None = None,
        create: bool = False,
        build: bool = True,
        load: bool = True,
        modalities_to_load: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            path: The path to the subject's directory.
            name: The ID name of the subject.
            parent_path: The parent path of this subject.
            mode: The file mode to set this subject to.
            create: Determines if this subject will be created if it does not exist.
            load: Determines if the sessions will be loaded from the subject's directory.
            kwargs: The keyword arguments for inheritance if any.
        """
        # Construct Parent #
        super().construct(
            path=path,
            name=name,
            parent_path=parent_path,
            mode=mode,
            **kwargs,
        )

        # Name and Path resolution
        if self.path is not None:
            if name is None:
                self.name = self.path.stem
        elif parent_path is not None and self.name is not None:
            self.path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / self.directory_name

        if self.path is not None:
            self.subject_name = self.path.parts[-3][4:]
            self.session_name = self.path.parts[-2][4:]

        # Create or Load
        if self.path is not None:
            if not self.path.exists():
                if create:
                    self.create(build=build)
            elif load:
                self.load()
