from __future__ import annotations

from abc import ABC
from typing import List

from core.components.entity.entity import Entity
from core.components.entity.entity_property import EntityProperty
from core.components.entity.number_property import NumberProperty


class Buffer(Entity, ABC):
    def __init__(self,
                 name: str, capacity: float = float('inf')):
        super().__init__(name, {
            'numberEntered': NumberProperty(),
            'capacity': capacity,
            'contents': [],
            'policy': 'FIFO'
        })

    def add(self, entity: Entity, quantity: int = 1):
        if len(self['contents']) + quantity <= self['capacity']:
            for i in range(quantity):
                sel