from pathlib import Path

from ucsfbids.datasets import Dataset
from ucsfbids.datasets.exporters.datasetupennexporter import DatasetUPENNExporter

name_map = {
    "EC0219": "UPenn0001",
    "EC0214": "UPenn0002",
    "EC0213": "UPenn0003",
    "EC0210": "UPenn0004",
    "EC0208": "UPenn0005",
}

if __name__ == "__main__":
    dataset = Dataset(Path("~/pia/userdata/rchristin/test-ucsfbids-5").expanduser())
    dataset.add_exporter("UPENN", DatasetUPENNExporter)
    dataset.create_exporter("UPENN").execute_export(Path("~/Kleen-Lab/bids-mount").expanduser(), "test", name_map)
