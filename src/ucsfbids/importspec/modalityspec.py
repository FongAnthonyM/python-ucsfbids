from typing import NamedTuple


class ModalitySpec(NamedTuple):
    name: str
    modality_type: type
    importer_key: str
    importer: type
