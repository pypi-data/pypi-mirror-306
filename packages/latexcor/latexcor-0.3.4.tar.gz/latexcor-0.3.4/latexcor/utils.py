from dataclasses import dataclass
from pathlib import Path


@dataclass
class TexFile:
    name: Path
    time_modification: float
    path: Path
