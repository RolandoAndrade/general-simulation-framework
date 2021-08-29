from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem


class SimulationDynamicSystem(DiscreteEventDynamicSystem):
    def __init__(self, scheduler=None):
        """Constructs the dynamic system"""
        DiscreteEventDynamicSystem.__init__(self, scheduler)
