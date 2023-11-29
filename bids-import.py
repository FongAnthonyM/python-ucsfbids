import os
from pathlib import Path
from typing import List

from ucsfbids.datasets import Dataset
from ucsfbids.datasets.importers.pia import DatasetPiaImporter
from ucsfbids.modalities.importers.pia.ieegpiaimporter import convert_electrodes

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
    dataset.create_importer("Pia", Path("~/pia").expanduser(), subjects=SUBJECTS).execute_import(
        source_patients=SUBJECTS_ROOT
    )
    clinical_path = Path("~/Kleen-Lab/data/imaging/EC217/Imaging/elecs/clinical_elecs_all.mat").expanduser()
    dst = Path(
        "~/pia/userdata/rchristin/test-ucsfbids-5/sub-EC0217/ses-clinicalintracranial/ieeg/sub-EC0217_ses-clinicalintracranial_electrodes.tsv"
    )

    convert_electrodes(clinical_path, dst)
