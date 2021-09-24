from core.expresions import Expression
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from examples.example_3.exit import Exit
from examples.example_3.generator import Generator, GeneratorState


class FactorySystem(DiscreteEventDynamicSystem):
    """Factory system

    Is the dynamic system where all the stations process parts.

    Attributes:
        generator (Generator): Generator of entities of the factory.
        exit (Exit): Sink of the factory,
    """
    generator: Generator
    exit: Exit

    def __init__(self, pieces: GeneratorState, interarrival_time: Expression):
        """Args:
            pieces(GeneratorState): number of pieces to create when there is an arrival.
            interarrival_time(Expression): interarrival time of pieces.
        """
        super().__init__()
        self.generator = Generator(self, pieces, interarrival_time)
        self.exit = Exit(self)
