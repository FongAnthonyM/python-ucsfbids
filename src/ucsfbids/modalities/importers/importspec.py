from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class ImportSpec:
    suffix: str
    extension: str
    path_from_root: Path
    copy_command: str | Callable[[Path, Path], None] | None = None
    post_command: str | None = None
