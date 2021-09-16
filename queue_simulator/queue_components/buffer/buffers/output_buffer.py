from __future__ import annotations

from core.entity.core import EntityManager
from core.entity.properties import NumberProperty, StringProperty
from queue_simulator.queue_components.buffer.core import Buffer, BufferPolicy


class OutputBuffer(Buffer):
    """Output buffer"""

    def __init__(
        self,
        name: str,
        capacity: NumberProperty = NumberProperty(float("inf")),
        policy: StringProperty = StringProperty(str(BufferPolicy.FIFO)),
        entity_manager: EntityManager = None,
    ):
        """
        Args:
            name (str): Name of the buffer.
            capacity (NumberProperty): Capacity of the buffer.
            policy (StringProperty): Policy of the buffer.
        """
        super().__init__(name, capacity, policy, entity_manager)

    def set_id(self, name: str):
        super(OutputBuffer, self).set_id(name + ".OutputBuffer")
