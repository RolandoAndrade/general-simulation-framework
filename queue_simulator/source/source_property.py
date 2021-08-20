from __future__ import annotations

import enum


class SourceProperty(str, enum.Enum):
    ENTITY_TYPE = 'Entity Type'
    INTER_ARRIVAL_TIME = 'Interarrival Time'
    TIME_OFFSET = 'Time Offset'
    ENTITIES_PER_ARRIVAL = 'Entities Per Arrival'
