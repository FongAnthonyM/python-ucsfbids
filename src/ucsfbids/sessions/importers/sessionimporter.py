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
from ..session import Session

# Third-Party Packages #


# Definitions #
# Classes #
class SessionImporter(BaseObject):
    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        session: Session | None = None,
        src_root: Path | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.session: Session | None = None
        self.src_root: Path | None = None

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                session=session,
                src_root=src_root,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        session: Session | None = None,
        src_root: Path | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            kwargs: The keyword arguments for inheritance if any.
        """
        if session is not None:
            self.session = session

        if src_root is not None:
            self.src_root = src_root

        super().construct(**kwargs)

    def import_modalities(self, path: Path):
        if self.session is None:
            raise RuntimeError("Undefined Session.")
        for modality in self.session.modalities.values():
            modality.create_importer("BIDS", self.src_root).execute_import(path)

    def execute_import(self, path: Path, name: str | None = None) -> None:
        if self.session is None:
            raise RuntimeError("Undefined Session.")
        if name is None:
            name = self.session.name

        new_path = path / f"ses-{name}"
        new_path.mkdir(exist_ok=True)
        self.import_modalities(path=new_path)


# Assign Exporter
Session.default_importers["BIDS"] = SessionImporter
