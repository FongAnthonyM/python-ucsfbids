"""subject.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __maintainer__, __email__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from baseobjects import BaseObject
from pathlib import Path
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..dataset import Dataset


# Definitions #
# Classes #
class DatasetBIDSImporter(BaseObject):
    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        dataset: Dataset | None = None,
        src_root: Path | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.dataset: Dataset | None = None
        self.src_roott: Path | None = None

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                dataset=dataset,
                src_root=src_root,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        dataset: Dataset | None = None,
        src_root: Path | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if dataset is not None:
            self.dataset = dataset

        if src_root is not None:
            self.src_root = src_root

        super().construct(**kwargs)

    def import_subjects(self, path: Path):
        if self.dataset is None:
            raise RuntimeError("Undefined Dataset")
        for subject in self.dataset.subjects.values():
            subject.create_importer("BIDS", self.src_root).execute_import(path)

    def execute_import(self, path: Path, name: str) -> None:
        new_path = path / f"sub-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_subjects(path=new_path)


# Assign Exporter
Dataset.default_importers["BIDS"] = DatasetBIDSImporter
