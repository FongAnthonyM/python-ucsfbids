"""baseimporter.py

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
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

# Third-Party Packages #
from baseobjects import BaseObject

# Local Packages #


# Definitions #
# Classes #
class BaseImporter(BaseObject):

    # Attributes #
    importer_name: str

    file_maps: list[tuple[str, str, Iterable[Path], Callable, dict[str, Any]]] = []
    inner_maps: list[tuple[str, type, dict[str, Any], str, type, dict[str, Any]]] = []

    default_type: tuple[type["BaseImporter"], dict[str, Any]]
    name_map: dict[str, str] = {}
    type_map: dict[type, (type, dict[str, Any])] = {}

    bids_object: Any = None

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        bids_object: Any = None,
        files_names: set[str, ...] | None = None,
        exclude_names: set[str, ...] | None = None,
        name_map: dict[str, str] | None = None,
        type_map: dict[type, type] | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        if self.export_file_names is not None:
            self.export_file_names = self.export_file_names.copy()

        self.export_exclude_names = self.file_maps.copy()

        self.name_map = self.name_map.copy()
        self.type_map = self.type_map.copy()

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                bids_object=bids_object,
                files_names=files_names,
                exclude_names=exclude_names,
                name_map=name_map,
                type_map=type_map,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        bids_object: Any = None,
        files_names: set[str, ...] | None = None,
        exclude_names: set[str, ...] | None = None,
        name_map: dict[str, str] | None = None,
        type_map: dict[type, type] | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if bids_object is not None:
            self.bids_object = bids_object

        if files_names is not None:
            if self.export_file_names is None:
                self.export_file_names = files_names.copy()
            else:
                self.export_file_names.update(files_names)

        if exclude_names is not None:
            self.export_exclude_names.update(exclude_names)

        if name_map is not None:
            self.name_map.update(name_map)

        if type_map is not None:
            self.type_map.update(type_map)

        super().construct(**kwargs)

    def import_files(self, path: Path, file_maps: list[tuple] | None = None) -> None:
        if file_maps is None:
            file_maps = self.file_maps

        for suffix, extension, relative_paths, import_call, i_kwargs in file_maps:
            new_path = self.bids_object.path / f"{self.bids_object.full_name}_{suffix}{extension}"
            for relative_path in relative_paths:
                if relative_path.exists():
                    import_call(path / relative_path, new_path, **i_kwargs)
                    break


    @abstractmethod
    def execute_import(self, path: Path, **kwargs: Any) -> None:
        pass
