"""subject.py

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
from ..subjects import Subject


# Definitions #
# Classes #
class Dataset(BaseComposite):
    """A subject in the UCSF BIDS format.

    Attributes:
        _path: The path to subject.
        _is_open: Determines if this subject and its contents are open.
        _mode: The file mode of this subject.
        name: The name of this subject.
        sessions: The session of the subject.

    Args:
        path: The path to the subject's directory.
        name: The ID name of the subject.
        parent_path: The parent path of this subject.
        mode: The file mode to set this subject to.
        create: Determines if this subject will be created if it does not exist.
        load: Determines if the sessions will be loaded from the subject's directory.
        init: Determines if this object will construct.
        kwargs: The keyword arguments for inheritance if any.
    """

    default_importers: dict[str, type] = {}
    default_exporters: dict[str, type] = {}

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str = "r",
        create: bool = False,
        load: bool = True,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self._path: Path | None = None
        self._mode: str = "r"

        self.name: str | None = None

        self.subjects: dict[str, Subject] = {}

        self.importers: dict[str, type] = self.default_importers.copy()
        self.exporters: dict[str, type] = self.default_exporters.copy()

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                path=path,
                name=name,
                parent_path=parent_path,
                mode=mode,
                create=create,
                load=load,
                **kwargs,
            )

    @property
    def path(self) -> Path | None:
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
        mode: str | None = None,
        create: bool = False,
        load: bool = False,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            path: The path to the subject's directory.
            name: The ID name of the subject.
            parent_path: The parent path of this subject.
            mode: The file mode to set this subject to.
            create: Determines if this subject will be created if it does not exist.
            load: Determines if the sessions will be loaded from the subject's directory.
            kwargs: The keyword arguments for inheritance if any.
        """
        if name is not None:
            self.name = name

        if path is not None:
            self.path = path

        if mode is not None:
            self._mode = mode

        if self.path is not None:
            if name is None:
                self.name = self.path.stem.lstrip[4:]
        elif parent_path is not None and self.name is not None:
            self.path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"sub-{self.name}"

        if self.path is not None:
            if load and self.path.exists():
                self.load_subjects()
            elif create:
                self.create()

        super().construct(**kwargs)

    def create(self) -> None:
        """Creates and sets up the subject's directory."""
        self.path.mkdir(exist_ok=True)

    def load_subjects(self, mode: str | None = None, load: bool = True) -> None:
        """Loads all sessions in this subject."""
        m = self._mode if mode is None else mode
        self.subjects.clear()
        self.subjects.update(
            {
                s.name: s
                for p in self.path.iterdir()
                if p.is_dir() and (s := Subject(path=p, mode=m, load=load)) is not None
            },
        )

    def generate_latest_subject_name(self) -> str:
        """Generates a session name for a new latest session.

        Returns:
            The name of the latest session to create.
        """
        return f"S{len(self.subjects):04d}"

    def create_new_subject(
        self,
        subject: type[Subject],
        name: str | None = None,
        mode: str | None = None,
        create: bool = True,
        **kwargs: Any,
    ) -> Subject:
        """Create a new session for this subject with a given session type and arguments.

        Args:
            session: The type of session to create.
            name: The name of the new session, defaults to the latest generated name.
            mode: The file mode to set the session to, defaults to the subject's mode.
            create: Determines if the session will create its contents.
            **kwargs: The keyword arguments for the session.

        Returns:
            The newly created session.
        """
        if name is None:
            name = self.generate_latest_subject_name()

        if mode is None:
            mode = self._mode

        self.subjects[name] = new_subject = subject(
            name=name,
            parent_path=self.path,
            mode=mode,
            create=create,
            **kwargs,
        )
        return new_subject

    def create_importer(self, type_: str, src_root: Path | None) -> Any:
        return self.importers[type_](dataset=self, src_root=src_root)

    def create_exporter(self, type_: str) -> Any:
        return self.exporters[type_](dataset=self)
