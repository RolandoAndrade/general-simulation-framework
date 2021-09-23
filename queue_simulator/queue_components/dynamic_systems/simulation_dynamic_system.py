from __future__ import annotations

from typing import List, Union, Set, Dict

from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from dynamic_system.future_event_list import Scheduler
from models.models import DiscreteEventModel
from queue_simulator.queue_components.route import Route
from queue_simulator.queue_components.server import Server
from queue_simulator.queue_components.shared.stats import ComponentStats
from queue_simulator.queue_components.sink.sink import Sink
from queue_simulator.queue_components.source import Source
import numpy as np


class SimulationDynamicSystem(DiscreteEventDynamicSystem):
    _models: Set[Union[Server, Source, Sink]]
    _paths: Dict[DiscreteEventModel, Set[Route]]

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

    def _get_effective_paths(self, emitter_model: DiscreteEventModel) -> Set[Route]:
        """Gets the correct paths for an output"""
        if emitter_model in self._paths:
            weights = []
            effective_path = []
            for path in self._paths[emitter_model]:
                weights.append(path.get_weight())
                effective_path.append(path)
            if len(weights) > 0:
                weights = np.array(weights) / sum(weights)
                choice = np.random.choice(len(weights), p=weights)
                return {effective_path[choice]}
        return set()

    def serialize(self):
        ds = {'models': set(), 'paths': set()}
        for model in self._models:
            ds['models'].add(model.serialize())
        for path_origin in self._paths:
            for path in self._paths[path_origin]:
                ds['paths'].add(path.serialize())
        return ds
