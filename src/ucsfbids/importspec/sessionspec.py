from typing import NamedTuple


class SessionSpec(NamedTuple):
    name: str
    importer_name: str
    importer_type: type
