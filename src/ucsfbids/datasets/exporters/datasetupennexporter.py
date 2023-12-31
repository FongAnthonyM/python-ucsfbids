from pathlib import Path

from ucsfbids.datasets.exporters import DatasetBIDSExporter
from ucsfbids.subjects.exporters.subjectupennexporter import SubjectUPENNExporter


class DatasetUPENNExporter(DatasetBIDSExporter):
    def export_subjects(self, path: Path, sub_name_map: dict[str, str]):
        assert self.dataset is not None
        for subject in self.dataset.subjects.values():
            subject.add_exporter("UPENN", SubjectUPENNExporter)
            assert subject.name is not None
            new_name = sub_name_map[subject.name]
            subject.create_exporter("UPENN").execute_export(path, new_name)
