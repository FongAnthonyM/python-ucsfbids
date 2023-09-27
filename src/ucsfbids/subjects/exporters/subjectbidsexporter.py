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
from ..subject import Subject


# Definitions #
# Classes #
class SubjectBIDSExporter(BaseObject):
    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        subject: Subject | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.subject: Subject | None = None

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                subject=subject,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        subject: Subject | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if subject is not None:
            self.subject = subject

        super().construct(**kwargs)

    def export_sessions(self, path: Path, name: str):
        for session in self.subject.sessions.values():
            session.create_exporter("BIDS").export(path, name=name)

    def export(self, path: Path, name: str) -> None:
        new_path = path / f"sub-{name}"
        new_path.mkdir(exist_ok=True)
        self.export_sessions(path=new_path)


# Assign Exporter
Subject.default_exporters["BIDS"] = SubjectBIDSExporter
