import os
from pathlib import Path
from typing import List

from ucsfbids.datasets import Dataset
from ucsfbids.datasets.importers.enigma import DatasetEnigmaImporter

SUBJECTS: List[str] = [
    "Enigma1",
    "Enigma2",
    "Enigma3",
    "Enigma4",
    "Enigma5",
    "Enigma6",
    "Enigma7",
    "Enigma8",
    "Enigma9",
    "Enigma10",
    "Enigma11",
    "Enigma12",
    "Enigma13",
    "Enigma14",
    "Enigma15",
    "Enigma16",
    "Enigma17",
    "Enigma18",
    "Enigma19",
    "Enigma20",
    "Enigma21",
    "Enigma22",
    "Enigma23",
    "Enigma24",
    "Enigma25",
    "Enigma26",
    "Enigma27",
    "Enigma28",
    "Enigma29",
    "Enigma30",
]
SUBJECTS_ROOT: list[str] = [
    "EC101",
    "EC102",
    "EC186",
    "EC188",
    "EC189",
    "EC190",
    "EC191",
    "EC192",
    "EC196",
    "EC197",
    "EC201",
    "EC202",
    "EC203",
    "EC204",
    "EC206",
    "EC210",
    "EC212",
    "EC213",
    "EC214",
    "EC219",
    "EC241",
    "EC243",
    "EC244",
    "EC253",
    "EC265",
    "EC271",
    "EC273",
    "EC274",
    "EC275",
    "EC276",
]

if __name__ == "__main__":
    Dataset.default_importers["Pia"] = DatasetEnigmaImporter
    dataset = Dataset(
        subjects_to_load=None,
        parent_path=Path(os.path.expanduser("~/")),
        name="enigma",
        mode="w",
        create=True,
        load=False,
    )
    dataset.create_importer(
        "Pia", Path("~/pia").expanduser(), subjects=SUBJECTS
    ).execute_import(source_patients=SUBJECTS_ROOT)
