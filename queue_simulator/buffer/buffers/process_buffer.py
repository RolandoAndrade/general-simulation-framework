from __future__ import annotations

from core.components.entity.properties.number_property import NumberProperty
from core.components.entity.properties.string_property import StringProperty
from queue_simulator.buffer.core.buffer import Buffer
from queue_simulator.buffer.core.buffer_policy import BufferPolicy


class ProcessBuffer(Buffer):
    """Input buffer"""
    def __init__(self, name: str,
                 capacity: NumberProperty = NumberProperty(float("inf")),
                 policy: StringProperty = StringProperty(BufferPolicy.FIFO)
                 ):
        """
        Args:
            name (str): Name of the buffer.
            capacity (NumberProperty): Capacity of the buffer.
            policy (StringProperty): Policy of the buffer.
        """
        super().__init__(name + ".ProcessBuffer", capacity, policy)