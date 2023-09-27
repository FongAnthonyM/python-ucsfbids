"""subject.py

"""
# Package Header #
from ucsfbids.header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from baseobjects import BaseObject
from pathlib import Path
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..session import Session


# Definitions #
# Classes #
class SessionBIDSExporter(BaseObject):
    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        session: Session | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.session: Session | None = None

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                session=session,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        session: Session | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if session is not None:
            self.session = session

        super().construct(**kwargs)

    def export_modalities(self, path: Path, name: str):
        for session in self.subject.modalities.values():
            session.create_exporter("BIDS").export(path, name=name)

    def export(self, path: Path, name: str) -> None:
        new_path = path / f"ses-{name}"
        new_path.mkdir(exist_ok=True)
        self.export_modalties(path=new_path, name=name)


# Assign Exporter
Session.default_exporters["BIDS"] = SessionBIDSExporter
