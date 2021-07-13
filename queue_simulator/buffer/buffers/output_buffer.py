from __future__ import annotations

from core.components.entity.properties.number_property import NumberProperty
from core.components.entity.properties.string_property import StringProperty
from queue_simulator.buffer.core.buffer import Buffer
from queue_simulator.buffer.core.buffer_policy import BufferPolicy


class OutputBuffer(Buffer):
    """Output buffer"""
    def __init__(self, name: str,
                 capacity: NumberProperty = NumberProperty(float("inf")),
                 policy: StringProperty = StringProperty(BufferPolicy.FIFO)
                 ):
        super().__init__(name + ".OutputBuffer", capacity, policy)
