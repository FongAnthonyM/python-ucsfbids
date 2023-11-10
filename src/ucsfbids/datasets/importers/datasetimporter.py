"""datasetimporter.py

"""
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__
from ucsfbids.subjects.subject import Subject

__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


from pathlib import Path
from typing import Any, List, Optional

from baseobjects import BaseObject

from ..dataset import Dataset


class DatasetImporter(BaseObject):
    def __init__(
        self,
        dataset: Optional[Dataset] = None,
        src_root: Optional[Path] = None,
        subjects: List[str] = [],
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        self.dataset: Optional[Dataset] = None
        self.src_root: Optional[Path] = None

        super().__init__(init=False)

        if init:
            self.construct(
                dataset=dataset,
                src_root=src_root,
                subjects=subjects,
                **kwargs,
            )

    def _process_subjects(self, subjects: list[str]):
        assert self.dataset is not None

        for subject in subjects:
            if subject not in self.dataset.subjects:  # TEST: maybe this is not the right datastructure
                self.dataset.create_new_subject(Subject, subject)

    def construct(
        self,
        dataset: Optional[Dataset] = None,
        src_root: Optional[Path] = None,
        subjects: List[str] = [],
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
        assert self.dataset is not None

        for subject in self.dataset.subjects.values():
            subject.create_importer("BIDS", self.src_root).execute_import(path)

    def execute_import(self, path: Path, name: Optional[str]) -> None:
        assert self.dataset is not None
        if name is None:
            name = self.dataset.name
        assert name is not None

        new_path = path / f"sub-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_subjects(path=new_path)


Dataset.default_importers["BIDS"] = DatasetImporter
