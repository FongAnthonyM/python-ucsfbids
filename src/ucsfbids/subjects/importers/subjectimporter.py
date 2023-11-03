"""subject.py

"""
# Package Header #
from ucsfbids.header import __author__, __credits__, __email__, __maintainer__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


from pathlib import Path
from typing import Any

# Imports #
# Standard Libraries #
from baseobjects import BaseObject

# Local Packages #
from ..subject import Subject

# Third-Party Packages #


# Definitions #
# Classes #
class SubjectImporter(BaseObject):
    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        subject: Subject | None = None,
        src_root: Path | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.subject: Subject | None = None
        self.src_root: Path | None = None

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                subject=subject,
                src_root=src_root,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        subject: Subject | None = None,
        src_root: Path | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if subject is not None:
            self.subject = subject

        if src_root is not None:
            self.src_root = src_root

        super().construct(**kwargs)

    def import_sessions(self, path: Path):
        if self.subject is None:
            raise RuntimeError("Undefined Subject")
        for session in self.subject.sessions.values():
            session.create_importer("BIDS", self.src_root).execute_import(path)

    def execute_import(self, path: Path, name: str) -> None:
        new_path = path / f"sub-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_sessions(path=new_path)


# Assign Exporter
Subject.default_importers["BIDS"] = SubjectImporter
