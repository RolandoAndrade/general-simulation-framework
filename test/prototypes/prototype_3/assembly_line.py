from typing import List, Dict, Optional

from core.types import Time
from dynamic_system.dynamic_systems import DiscreteEventDynamicSystem
from test.prototypes.prototype_3.drill import Drill
from test.prototypes.prototype_3.press import Press


class AssemblyLine(DiscreteEventDynamicSystem):
    press: Press
    drill: Drill

    def __init__(self):
        super().__init__()
        self.press = Press(self, "Press")
        self.drill = Drill(self, "Drill")
        self.press.add(self.drill)

    def process(self, inputs: List[int]):
        i = 0
        while True:
            print("------------------")
            print("time -> " + str(i))
            if inputs[int(i)] is not None:
                print("Inserting " + str(inputs[int(i)]) + " part(s)")
            print("output -> " + str(self.get_output()))
            print("--")
            r_input = None
            if inputs[int(i)]:
                r_input = {self.press: inputs[int(i)]}
            if i < 1:
                self.state_transition(r_input, Time(0))
            else:
                self.state_transition(r_input, self.get_time_of_next_events())
            print("--")
            print(self._scheduler)
            if self.get_time_of_next_events() == -1:
                break
            i = i + self.get_time_of_next_events()
        return i


