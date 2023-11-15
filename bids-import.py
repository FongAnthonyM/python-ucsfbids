import os
from pathlib import Path
from typing import List

from ucsfbids.datasets import Dataset
from ucsfbids.datasets.importers.pia import DatasetPiaImporter

SUBJECTS: List[str] = ["EC212", "EC287"]

if __name__ == "__main__":
    Dataset.default_importers["Pia"] = DatasetPiaImporter
    dataset = Dataset(
        parent_path=Path(os.path.expanduser("~/Kleen-Lab/bids-data/")), name="test", mode="w", create=True, load=False
    )

    dataset.create_importer("Pia", Path(os.path.expanduser("~/pia/")), subjects=SUBJECTS).execute_import()
