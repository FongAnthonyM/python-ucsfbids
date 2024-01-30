"""subject.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


from pathlib import Path
from typing import Any

# Imports #
# Standard Libraries #
from baseobjects import BaseComposite

# Local Packages #
from ..subjects import Subject

# Third-Party Packages #


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
        subjects_to_load: list[str] | None = None,
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

        print(subjects_to_load)
        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                path=path,
                name=name,
                parent_path=parent_path,
                subjects_to_load=subjects_to_load,
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
        subjects_to_load: list[str] | None = None,
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
            self.path = Path(path)

        if mode is not None:
            self._mode = mode

        if self.path is not None:
            if name is None:
                self.name = self.path.stem
        elif parent_path is not None and self.name is not None:
            self.path = (
                parent_path if isinstance(parent_path, Path) else Path(parent_path)
            ) / f"{self.name}"

        if self.path is not None:
            if load and self.path.exists():
                self.load_subjects(subjects_to_load)
            elif create:
                self.create()

        super().construct(**kwargs)

    def create(self) -> None:
        """Creates and sets up the subject's directory."""
        assert self.path is not None
        self.path.mkdir(exist_ok=True)

    def load_subjects(
        self,
        subjects_to_load: list[str] | None = None,
        mode: str | None = None,
        load: bool = True,
    ) -> None:
        """Loads all sessions in this subject."""
        assert self.path is not None
        m = self._mode if mode is None else mode
        self.subjects.clear()
        subjects_to_update = {}
        print(subjects_to_load)
        for p in self.path.iterdir():
            if subjects_to_load is not None and not any(
                [sub in p.as_posix() for sub in subjects_to_load]
            ):
                continue
            if not p.is_dir():
                continue
            if (s := Subject(path=p, mode=m, load=load)) is not None:
                continue
            subjects_to_update.update({s.name: s})

        self.subjects.update(subjects_to_update)

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
        load: bool = False,
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
            load=load,
            create=create,
            **kwargs,
        )
        return new_subject

    def create_importer(self, type_: str, src_root: Path | None, **kwargs) -> Any:
        return self.importers[type_](dataset=self, src_root=src_root, **kwargs)

    def create_exporter(self, type_: str) -> Any:
        return self.exporters[type_](dataset=self)

    def add_importer(self, type_: str, importer: type, overwrite: bool = False):
        if type_ not in self.importers or overwrite:
            self.importers[type_] = importer

    def add_exporter(self, type_: str, exporter: type, overwrite: bool = False):
        if type_ not in self.exporters or overwrite:
            self.exporters[type_] = exporter
