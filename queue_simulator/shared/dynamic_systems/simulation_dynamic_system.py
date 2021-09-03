from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from dynamic_system.future_event_list import Scheduler


class SimulationDynamicSystem(DiscreteEventDynamicSystem):
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
        for path in self._paths:
            if path.get_id() == name:
                return path
        return None
