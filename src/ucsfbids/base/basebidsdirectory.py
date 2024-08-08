"""basebidsdirectory.py

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
from abc import abstractmethod
from collections.abc import MutableMapping
import json
from pathlib import Path
from typing import ClassVar, Any

# Third-Party Packages #
from baseobjects import BaseComposite

# Local Packages #
from .baseimporter import BaseImporter
from .baseexporter import BaseExporter


# Definitions #
# Classes #
class BaseBIDSDirectory(BaseComposite):
    """A subject in the UCSF BIDS format.

    Attributes:
        _path: The path to subject.
        _is_open: Determines if this subject and its contents are open.
        _mode: The file mode of this subject.
        name: The name of this subject.
        sessions: The session of the subject.

    Args:
        path: The path to the subject's directory.
        name: The ID name of the subject.
        parent_path: The parent path of this subject.
        mode: The file mode to set this subject to.
        create: Determines if this subject will be created if it does not exist.
        load: Determines if the sessions will be loaded from the subject's directory.
        init: Determines if this object will construct.
        kwargs: The keyword arguments for inheritance if any.
    """

    # Attributes #
    _path: Path | None = None
    _mode: str = "r"

    name: str | None = None

    meta_information: dict[str, Any] = {}

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]]
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]]

    # Properties #
    @property
    def path(self) -> Path | None:
        """The path to the BIDS directory."""
        return self._path

    @path.setter
    def path(self, value: str | Path) -> None:
        if isinstance(value, Path) or value is None:
            self._path = value
        else:
            self._path = Path(value)

    @property
    @abstractmethod
    def directory_name(self) -> str:
        """The directory name of this BIDS Directory object."""

    @property
    @abstractmethod
    def full_name(self) -> str:
        """The full name of this BIDS Directory object."""

    @property
    def meta_information_path(self) -> Path:
        """The path to the meta information json file."""
        return self._path / f"{self.full_name}_meta.json"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str = "r",
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.meta_information = self.meta_information.copy()

        self.importers = dict(self.importers)
        self.exporters = dict(self.exporters)

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                path=path,
                name=name,
                parent_path=parent_path,
                mode=mode,
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
        if name is not None:
            self.name = name

        if path is not None:
            self.path = Path(path)

        if mode is not None:
            self._mode = mode

        super().construct(**kwargs)

    def create(self, build: bool = True) -> None:
        self.path.mkdir(exist_ok=True)
        if build:
            self.build()

    def build(self) -> None:
        self.create_meta_information()

    def load(self, **kwargs: Any) -> None:
        self.load_meta_information()

    # Meta Information
    def create_meta_information(self) -> None:
        """Creates meta information file and saves the meta information."""
        with self.meta_information_path.open(self._mode) as file:
            json.dump(self.meta_information, file)

    def load_meta_information(self) -> dict:
        """Loads the meta information from the file.

        Returns:
            The modality meta information.
        """
        self.meta_information.clear()
        with self.meta_information_path.open("r") as file:
            self.meta_information.update(json.load(file))
        return self.meta_information

    def save_meta_information(self) -> None:
        """Saves the meta information to the file."""
        with self.meta_information_path.open(self._mode) as file:
            json.dump(self.meta_information, file)

    # Import/Export
    def create_importer(self, type_: str, src_root: Path | None, **kwargs: Any) -> BaseImporter:
        importer, d_kwargs = self.importers[type_]
        return importer(dataset=self, src_root=src_root, **(d_kwargs | kwargs))

    def add_importer(
        self,
        type_: str,
        importer: type[BaseImporter],
        kwargs: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> None:
        if type_ not in self.importers or overwrite:
            self.importers[type_] = (importer, kwargs)
            
    def require_importer(
        self,
        type_: str,
        importer: type[BaseImporter],
        kwargs: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> BaseImporter:
        importer_, d_kwargs = self.importers.get(type_, (None, {}))
        if importer_ is None or overwrite:
            self.importers[type_] = (importer, kwargs)
            importer_ = importer

        return importer_(self, **(d_kwargs | kwargs))

    def create_exporter(self, type_: str, **kwargs: Any) -> BaseExporter:
        exporter, d_kwargs = self.exporters[type_]
        return exporter(self, **(d_kwargs | kwargs))

    def add_exporter(
        self,
        type_: str,
        exporter: type[BaseExporter],
        kwargs: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> None:
        if type_ not in self.exporters or overwrite:
            self.exporters[type_] = (exporter, kwargs)
            
    def require_exporter(
        self,
        type_: str,
        exporter: type[BaseExporter],
        kwargs: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> BaseExporter:
        exporter_, d_kwargs = self.exporters.get(type_, (None, {}))
        if exporter_ is None or overwrite:
            self.exporters[type_] = (exporter, kwargs)
            exporter_ = exporter

        return exporter_(self, **(d_kwargs | kwargs))
    