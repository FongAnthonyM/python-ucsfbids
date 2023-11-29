from pathlib import Path

from ucsfbids.datasets import Dataset
from ucsfbids.datasets.exporters.datasetupennexporter import DatasetUPENNExporter

if __name__ == "__main__":
    dataset = Dataset(Path("~/pia/userdata/rchristin/test-ucsfbids-5").expanduser())
    dataset.add_exporter("UPENN", DatasetUPENNExporter)
    dataset.create_exporter("UPENN").execute_export(Path("~/Kleen-Lab/bids-mount").expanduser(), "test")
