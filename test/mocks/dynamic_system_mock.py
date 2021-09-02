from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem


class DynamicSystemMock(DiscreteEventDynamicSystem):
    """Discrete event dynamic system for testing"""

    def __init__(self, scheduler=None):
        """Constructs the dynamic system"""
        DiscreteEventDynamicSystem.__init__(self, scheduler)
