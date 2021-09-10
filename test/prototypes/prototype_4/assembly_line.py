from typing import List

from core.types import Time
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from test.prototypes.prototype_4.drill import Drill
from test.prototypes.prototype_4.generator import Generator
from test.prototypes.prototype_4.press import Press


class AssemblyLine(DiscreteEventDynamicSystem):
    generator: Generator
    press: Press
    drill: Drill

    def __init__(self, pieces: List[int]):
        super().__init__()
        self.generator = Generator(self, pieces)
        self.press = Press(self, "Press")
        self.drill = Drill(self, "Drill")
        self.generator.add(self.press)
        self.press.add(self.drill)
        print(self._scheduler)
