"""ieeg.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any

# Third-Party Packages #
import pandas as pd

# Local Packages #
from ...base import BaseImporter, BaseExporter
from ..modality import Modality


# Definitions #
# Classes #
class IEEG(Modality):
    """.

    Class Attributes:
        namespace: The namespace of the subclass.
        name: The name of which the subclass will be registered as.
        registry: A registry of all subclasses of this class.
        registration: Determines if this class/subclass will be added to the registry.
        meta_information: The default meta information about the session.
        cdfs_type: The type of CDFS the session objects of this class will use.

    Attributes:
        _path: The path to session.
        _is_open: Determines if this session and its contents are open.
        _mode: The file mode of this session.
        meta_info: The meta information that describes this session.
        name: The name of this session.
        subject_name: The name of the parent subject of this session.
        cdfs: The CDFS object of this session.

    Args:
        path: The path to the session's directory.
        name: The name of the session.
        parent_path: The parent path of this session.
        mode: The file mode to set this session to.
        create: Determines if this session will be created if it does not exist.
        init: Determines if this object will construct.
        kwargs: The keyword arguments for inheritance.
    """

    # Attributes #
    name: str = "ieeg"

    meta_information: dict[str, Any] = Modality.meta_information.copy()

    electrode_columns: list[str] = [
        "name",
        "x",
        "y",
        "z",
        "size",
        "material",
        "manufacturer",
        "group",
        "hemisphere",
        "type",
        "impedance",
    ]
    electrodes: pd.DataFrame | None = None

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]] = Modality.importers.new_child()
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]] = Modality.exporters.new_child()

    # Properties #
    @property
    def electrodes_path(self) -> Path:
        """The path to the meta information json file."""
        return self.path / f"{self.full_name}_electrodes.tsv"

    # Instance Methods #
    # Electrodes
    def create_electrodes(self) -> None:
        """Creates electrodes file and saves the electrodes."""
        if self.electrodes is None:
            self.electrodes = pd.DataFrame(columns=self.electrode_columns)

        self.electrodes.to_csv(self.electrodes_path, mode=self._mode, sep="\t")

    def load_electrodes(self) -> pd.DataFrame:
        """Loads the electrode information from the file.

        Returns:
            The electrode information.
        """
        self.electrodes = electrodes = pd.read_csv(self.electrodes_path, sep="\t")
        return electrodes

    def save_electrodes(self) -> None:
        """Saves the electrodes to the file."""
        self.electrodes.to_csv(self.electrodes_path, mode=self._mode, sep="\t")