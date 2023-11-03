# header
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__
from ucsfbids.subjects.subject import Subject

__author__ = __author__
__maintainer__ = __maintainer__
__credits__ = __credits__
__email__ = __email__

from pathlib import Path
from typing import Any, List, Optional

from ....subjects.importers.pia import SubjectPiaImporter
from ...dataset import Dataset
from ..datasetimporter import DatasetImporter


class DatasetPiaImporter(DatasetImporter):
    def construct(
        self, dataset: Dataset | None = None, src_root: Path | None = None, subjects: List[str] = [], **kwargs: Any
    ) -> None:
        if dataset is None:
            raise RuntimeError("Dataset in None")

        self.dataset = dataset

        if src_root is not None:
            self.src_root = src_root

        Subject.default_importers["Pia"] = SubjectPiaImporter

        for subject in subjects:
            if subject in self.dataset.subjects:
                self.dataset.subjects[subject].default_importers["Pia"] = SubjectPiaImporter
                continue
            self.dataset.create_new_subject(Subject, subject)

        super().construct(**kwargs)

    def import_subjects(self, path: Path):
        if self.dataset is None:
            raise RuntimeError("Dataset is None")
        for subject in self.dataset.subjects.values():
            subject.create_importer("Pia", self.src_root).execute_import(path)

    def execute_import(self, path: Path, name: Optional[str]) -> None:
        if self.dataset is None:
            raise RuntimeError("Dataset is None")
        if name is None:
            name = self.dataset.name

        new_path = path / name
        new_path.mkdir(exist_ok=True)
        self.import_subjects(path=new_path)
