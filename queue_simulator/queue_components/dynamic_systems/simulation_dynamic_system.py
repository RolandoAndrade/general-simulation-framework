from __future__ import annotations

from typing import List, Union, Set

from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from dynamic_system.future_event_list import Scheduler
from queue_simulator.queue_components.server import Server
from queue_simulator.queue_components.shared.stats import ComponentStats
from queue_simulator.queue_components.sink.sink import Sink
from queue_simulator.queue_components.source import Source


class SimulationDynamicSystem(DiscreteEventDynamicSystem):
    _models: Set[Union[Server, Source, Sink]]

    def __init__(self, scheduler=None):
        """Constructs the dynamic system"""
        if scheduler is None:
            scheduler = Scheduler()
        DiscreteEventDynamicSystem.__init__(self, scheduler)

    def get_model(self, name: str):
        for model in self._models:
            if model.get_id() == name:
                return model
        return None

    def get_path(self, name: str):
        for model_paths in self._paths:
            for path in self._paths[model_paths]:
                if path.get_id() == name:
                    return path
        return None

    def init(self):
        for model in self._models:
            model.clear()

    def get_stats(self) -> List[ComponentStats]:
        s = []
        for model in self._models:
            s.append(model.get_stats())
        return s