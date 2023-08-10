"""basesubject.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from baseobjects import BaseComposite
from pathlib import Path
from typing import Any


# Third-Party Packages #


# Local Packages #
from ..sessions import BaseSession


# Definitions #
# Classes #
class BaseSubject(BaseComposite):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self._path: Path | None = None

        self.name: str | None = None
        self.parent_name: str | None = None

        self.sessions: dict[str, BaseSession] = {}

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                path=path,
                name=name,
                parent_path=parent_path,
                **kwargs,
            )

    @property
    def path(self) -> Path:
        """The path to the subject."""
        return self._path

    @path.setter
    def path(self, value: str | Path) -> None:
        if isinstance(value, Path) or value is None:
            self._path = value
        else:
            self._path = Path(value)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            path: The path to the subject's directory.
            name: The name of the session.
            parent_path: The parent path of this session.
        """
        if name is not None:
            self.name = name

        if path is not None:
            self.path = path

        if self.path is not None:
            if name is None:
                self.name = self.path.stem.lstrip[4:]
        elif parent_path is not None and self.name is not None:
            self.path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"sub-{self.name}"

        if self.path is not None:
            self.parent_name = self.path.parts[-2][4:]

        super().construct(**kwargs)

    def create(self):
        self.path.mkdir(exist_ok=True)

    def load_sessions(self) -> None:
        """Loads all sessions in this subject."""
        dirs = [p for p in self.path.iterdir() if p.is_dir()]
        pass

    def export_to_bids(self, path: Path | str) -> None:
        pass

    def generate_latest_session_name(self) -> str:
        return f"S{len(self.sessions):04d}"

    def create_new_session(self, session: type[BaseSession], name: str | None = None, **kwargs) -> BaseSession:
        if name is None:
            name = self.generate_latest_session_name()

        self.sessions[name] = new_session = session(name=name, parent_path=self.path, **kwargs)
        return new_session

