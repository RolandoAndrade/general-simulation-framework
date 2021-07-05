from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)


class FactorySystem(DiscreteEventDynamicSystem):
    def __init__(self):
        super().__init__()
