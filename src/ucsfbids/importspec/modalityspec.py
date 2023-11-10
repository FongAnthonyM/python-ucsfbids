from typing import NamedTuple

import ucsfbids.modalities.importers as importers
from ucsfbids.modalities import Modality


class ModalitySpec(NamedTuple):
    name: str
    modality_type: type[Modality]
    importer_key: str
    importer: type[importers.ModalityImporter]
