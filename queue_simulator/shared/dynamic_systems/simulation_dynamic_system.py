from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from dynamic_system.future_event_list import Scheduler


class SimulationDynamicSystem(DiscreteEventDynamicSystem):
    def __init__(self, scheduler=None):
        """Constructs the dynamic system"""
        if scheduler is None:
            scheduler = Scheduler()
        DiscreteEventDynamicSystem.__init__(self, scheduler)
