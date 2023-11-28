"""subject.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


import shutil
from pathlib import Path
from typing import Any

# Imports #
# Standard Libraries #
from baseobjects import BaseObject

# Local Packages #
from ..dataset import Dataset

# Third-Party Packages #


# Definitions #
# Classes #
class DatasetBIDSExporter(BaseObject):
    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        dataset: Dataset | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.dataset: Dataset | None = None

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                dataset=dataset,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        dataset: Dataset | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if dataset is not None:
            self.dataset = dataset

        super().construct(**kwargs)

    def export_subjects(self, path: Path):
        assert self.dataset is not None
        for subject in self.dataset.subjects.values():
            subject.create_exporter("BIDS").execute_export(path)

    def execute_export(self, path: Path, name: str) -> None:
        new_path = path / name
        new_path.mkdir(exist_ok=True)
        assert self.dataset is not None
        assert self.dataset.path is not None
        for file in [f for f in self.dataset.path.iterdir() if f.is_file()]:
            shutil.copy2(file, new_path / file.name)
        self.export_subjects(path=new_path)


# Assign Exporter
Dataset.default_exporters["BIDS"] = DatasetBIDSExporter
