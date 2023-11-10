from typing import NamedTuple

import ucsfbids.sessions.importers as importers


class SessionSpec(NamedTuple):
    name: str
    importer_name: str
    importer_type: type[importers.SessionImporter]
