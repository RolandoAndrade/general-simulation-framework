from __future__ import annotations

import enum


class ServerProperty(str, enum.Enum):
    INITIAL_CAPACITY = "Initial Capacity"
    PROCESSING_TIME = "Processing Time"
