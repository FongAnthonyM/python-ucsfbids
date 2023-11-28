import os
from pathlib import Path
from typing import List

from ucsfbids.datasets import Dataset
from ucsfbids.datasets.importers.pia import DatasetPiaImporter

SUBJECTS: List[str] = ["EC0217", "EC0216"]
SUBJECTS_ROOT: list[str] = ["EC217", "EC216"]

if __name__ == "__main__":
    Dataset.default_importers["Pia"] = DatasetPiaImporter
    dataset = Dataset(
        parent_path=Path(os.path.expanduser("~/pia/userdata/rchristin/")),
        name="test-ucsfbids-5",
        mode="w",
        create=True,
        load=False,
    )
