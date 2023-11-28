from pathlib import Path

from ucsfbids.datasets.exporters import DatasetBIDSExporter
from ucsfbids.subjects.exporters.subjectupennexporter import SubjectUPENNExporter


class DatasetUPENNExporter(DatasetBIDSExporter):
    def export_subjects(self, path: Path):
        assert self.dataset is not None
        for subject in self.dataset.subjects.values():
            subject.add_exporter("UPENN", SubjectUPENNExporter)
            subject.create_exporter("UPENN").execute_export(path)
