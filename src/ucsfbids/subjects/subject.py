"""subject.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


import json
from pathlib import Path
from typing import Any, Optional

# Imports #
# Standard Libraries #
from baseobjects import BaseComposite

# Local Packages #
from ..sessions import Session

# Third-Party Packages #


# Definitions #
# Classes #
class Subject(BaseComposite):
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

    default_meta_info: dict[str, Any] = {
        "SubjectNamespace": "",
    }
    default_importers: dict[str, type] = {}
    default_exporters: dict[str, type] = {}

    # @classmethod
    # def get_class_information(
    #     cls,
    #     path: Path | str | None = None,
    #     name: str | None = None,
    #     parent_path: Path | str | None = None,
    #     *args: Any,
    #     **kwargs: Any,
    # ) -> tuple[str, str]:
    #     """Gets a class namespace and name from a given set of arguments.
    #
    #     Args:
    #         path: The path to the session.
    #         name: The name of the session.
    #         parent_path: The path to the parent of the session.
    #         *args: The arguments to get the namespace and name from.
    #         **kwargs: The keyword arguments to get the namespace and name from.
    #
    #     Returns:
    #         The namespace and name of the class.
    #     """
    #     if path is not None:
    #         if not isinstance(path, Path):
    #             path = Path(path)
    #
    #         if name is None:
    #             name = path.stem[4:]
    #     elif parent_path is not None and name is not None:
    #         path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"sub-{name}"
    #     else:
    #         raise ValueError("Either path or (parent_path and name) must be given to disptach class.")
    #
    #     meta_info_path = path / f"sub-{name}_meta.json"
    #     with meta_info_path.open("r") as file:
    #         info = json.load(file)
    #
    #     return info["SubjectNamespace"]

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
        self.parent_name: Optional[str] = None

        self.meta_info: dict = self.default_meta_info.copy()
        self.sessions: dict[str, Session] = {}

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
    def path(self) -> Path:
        """The path to the subject."""
        assert self._path is not None
        return self._path

    @path.setter
    def path(self, value: str | Path) -> None:
        if isinstance(value, Path) or value is None:
            self._path = value
        else:
            self._path = Path(value)

    @property
    def full_name(self) -> str:
        return f"sub-{self.name}"

    @property
    def meta_info_path(self) -> Path:
        assert self._path is not None
        return self._path / f"{self.full_name}_meta.json"

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
            self.path = Path(path)

        if mode is not None:
            self._mode = mode

        if self.path is not None:
            if name is None:
                self.name = self.path.stem[4:]

        elif parent_path is not None and self.name is not None:
            self.path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"sub-{self.name}"

        assert self.path is not None
        self.parent_name = self.path.parts[-2]

        if mode is not None:
            self._mode = mode

        if self.path is not None:
            if load and self.path.exists():
                self.load_sessions()
            elif create:
                print(self.path, parent_path)
                self.create()

        super().construct(**kwargs)

    def create_meta_info(self) -> None:
        with self.meta_info_path.open(self._mode) as file:
            json.dump(self.meta_info, file)

    def load_meta_info(self) -> dict:
        self.meta_info.clear()
        with self.meta_info_path.open("r") as file:
            self.meta_info.update(json.load(file))
        return self.meta_info

    def save_meta_info(self) -> None:
        with self.meta_info_path.open(self._mode) as file:
            json.dump(self.meta_info, file)

    def create_sessions(self) -> None:
        for session in self.sessions.values():
            session.create()

    def create(self) -> None:
        """Creates and sets up the subject's directory."""
        self.path.mkdir(exist_ok=True)
        self.create_meta_info()

    def load_sessions(self, mode: str | None = None, load: bool = True) -> None:
        """Loads all sessions in this subject."""
        m = self._mode if mode is None else mode
        self.sessions.clear()
        self.sessions.update(
            {
                s.name: s
                for p in self.path.iterdir()
                if p.is_dir() and (s := Session(path=p, mode=m, load=load)) is not None
            },
        )

    def generate_latest_session_name(self) -> str:
        """Generates a session name for a new latest session.

        Returns:
            The name of the latest session to create.
        """
        return f"S{len(self.sessions):04d}"

    def create_new_session(
        self,
        session: type,
        name: str | None = None,
        mode: str | None = None,
        load: bool = False,
        create: bool = True,
        **kwargs: Any,
    ) -> Session:
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
            name = self.generate_latest_session_name()

        if mode is None:
            mode = self._mode

        print(self.path)

        self.sessions[name] = new_session = session(
            name=name,
            parent_path=self.path,
            mode=mode,
            load=load,
            create=create,
            **kwargs,
        )
        return new_session

    def create_importer(self, type_: str, src_root: Path | None, **kwargs) -> Any:
        return self.importers[type_](subject=self, src_root=src_root, **kwargs)

    def create_exporter(self, type_: str) -> Any:
        return self.exporters[type_](subject=self)

    def add_importer(self, type_: str, importer: type):
        assert type_ not in self.importers
        self.importers[type_] = importer
