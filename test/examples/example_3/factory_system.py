from core.expresions import Expression
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from examples.example_3.exit import Exit
from examples.example_3.generator import Generator, GeneratorState


class FactorySystem(DiscreteEventDynamicSystem):
    generator: Generator
    exit: Exit

    def __init__(self, pieces: GeneratorState, interarrival_time: Expression):
        super().__init__()
        self.generator = Generator(self, pieces, interarrival_time)
        self.exit = Exit(self)
