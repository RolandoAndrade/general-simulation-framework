from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Event:
    _subject: str
    _message: Any
