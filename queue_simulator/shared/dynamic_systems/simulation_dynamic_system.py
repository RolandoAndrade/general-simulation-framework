from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from dynamic_system.future_event_list import Scheduler


class SimulationDynamicSystem(DiscreteEventDynamicSystem):
    def __init__(self, scheduler=Scheduler()):
        """Constructs the dynamic system"""
        DiscreteEventDynamicSystem.__init__(self, scheduler)
