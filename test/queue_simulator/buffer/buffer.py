from __future__ import annotations

from abc import ABC
from typing import List

from core.components.entity.entity import Entity
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from models.models.discrete_event_model import DiscreteEventModel


class Buffer(DiscreteEventModel, ABC):
    _time: float

    def __init__(self, dynamic_system: DiscreteEventDynamicSystem,
                 name: str, time: float = 1):
        super().__init__(dynamic_system, name, {
            'numberEntered': 0,
            'capacity': float('inf'),
            'contents': []
        })
        self.__time = time
