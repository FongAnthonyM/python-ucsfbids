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
from collections.abc import Iterable, MutableMapping
from collections import ChainMap
from pathlib import Path
import json
from typing import Any

# Third-Party Packages #
import pandas as pd

# Local Packages #
from ..base import BaseBIDSDirectory, BaseImporter, BaseExporter
from ..subjects import Subject


# Definitions #
# Classes #
class Dataset(BaseBIDSDirectory):

    # Attributes #
    subject_prefix: str = "S"
    subject_digits: int = 4

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]] = ChainMap()
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]] = ChainMap()

    meta_information: dict[str, Any] = {
        "DatasetNamespace": "",
        "DatasetType": "",
    }

    description: dict[str, Any] = {
        "Name": "Default name, should be updated",
        "BIDSVersion": "1.6.0",
        "DatasetType": "raw",
    }

    participant_fields: dict[str, Any] = {}
    participants: pd.DataFrame | None = None
    
    subjects: dict[str, Subject]

    # Properties #
    @property
    def directory_name(self) -> str:
        """The directory name of this Dataset."""
        return self.name

    @property
    def full_name(self) -> str:
        """The full name of this Dataset."""
        return self.name

    @property
    def description_path(self) -> Path:
        """The path to the description json file."""
        return self._path / f"dataset_description.json"

    @property
    def participant_fields_path(self) -> Path:
        """The path to the participant json file."""
        return self._path / f"participants.json"

    @property
    def participants_path(self) -> Path:
        """The path to the participant tsv file."""
        return self._path / f"participants.tsv"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str | None = None,
        create: bool = False,
        build: bool = True,
        load: bool = False,
        subjects_to_load: list[str] | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.description = self.description.copy()
        self.participant_fields = self.participant_fields.copy()
        self.subjects = {}

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
                build=build,
                load=load,
                subjects_to_load=subjects_to_load,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str | None = None,
        create: bool = False,
        build: bool = True,
        load: bool = False,
        subjects_to_load: list[str] | None = None,
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
        # Construct Parent #
        super().construct(
            path=path,
            name=name,
            parent_path=parent_path,
            mode=mode,
            **kwargs,
        )

        # Create or Load
        if self.path is not None:
            if not self.path.exists():
                if create:
                    self.create(build=build)
            elif load:
                self.load(subjects_to_load)

    def build(self) -> None:
        super().build()
        self.create_description()

    def load(
        self,
        names: Iterable[str] | None = None,
        mode: str | None = None,
        load: bool = True,
        **kwargs: Any,
    ) -> None:
        super().load()
        self.load_subjects(names, mode, load)

    # Description
    def create_description(self) -> None:
        """Creates description file and saves the description."""
        with self.description_path.open(self._mode) as file:
            json.dump(self.description, file)

    def load_description(self) -> dict:
        """Loads the description from the file.

        Returns:
            The dataset description.
        """
        self.description.clear()
        with self.description_path.open("r") as file:
            self.description.update(json.load(file))
        return self.description

    def save_description(self) -> None:
        """Saves the description to the file."""
        with self.description_path.open(self._mode) as file:
            json.dump(self.description, file)

    # Participant Fields
    def create_participant_fields(self) -> None:
        """Creates participant fields file and saves the participant fields."""
        with self.participant_fields_path.open(self._mode) as file:
            json.dump(self.participant_fields, file)

    def load_participant_fields(self) -> dict:
        """Loads the participant fields from the file.

        Returns:
            The dataset participant fields.
        """
        self.participant_fields.clear()
        with self.participant_fields_path.open("r") as file:
            self.participant_fields.update(json.load(file))
        return self.participant_fields

    def save_participant_fields(self) -> None:
        """Saves the participant fields to the file."""
        with self.participant_fields_path.open(self._mode) as file:
            json.dump(self.participant_fields, file)

    # Participants
    def create_participants(self) -> None:
        """Creates participants file and saves the participants."""
        if self.participants is None:
            self.participants = pd.DataFrame(columns=["participant_id"])

        self.participants.to_csv(self.participants_path, mode=self._mode, sep="\t")

    def load_participants(self) -> pd.DataFrame:
        """Loads the participant information from the file.

        Returns:
            The participant information.
        """
        self.participants = participants = pd.read_csv(self.participants_path, sep="\t")
        return participants

    def save_participants(self) -> None:
        """Saves the participants to the file."""
        self.participants.to_csv(self.participants_path, mode=self._mode, sep="\t")

    # Subject
    def load_subjects(self, names: Iterable[str] | None = None, mode: str | None = None, load: bool = True) -> None:
        """Loads all subjects in this dataset."""
        m = self._mode if mode is None else mode
        self.subjects.clear()

        # Use an iterator to load subjects
        self.subjects.update(
            (s.name, s)  # The key and subject to add
            for p in self.path.iterdir()  # Iterate over the path's contents
            # Check if the path is a directory and the name is in the names list
            if p.is_dir() and (names is None or any(n in p.stem for n in names)) and
            # Create a subject and check if it is valid
            (s := Subject(path=p, mode=m, load=load)) is not None
        )

    def generate_latest_subject_name(self, prefix: str | None = None, digits: int | None = None) -> str:
        """Generates a subject name for a new latest subject.

        Returns:
            The name of the latest session to create.
        """
        if prefix is None:
            prefix = self.subject_prefix
        if digits is None:
            digits = self.subject_digits
        return f"{prefix}{len(self.subjects):0{digits}d}"

    def create_subject(
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
