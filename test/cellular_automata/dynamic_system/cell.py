from dynamic_system.models.input_model import InputModel
from dynamic_system.models.model import Model
from dynamic_system.utils.bag_of_values import BagOfValues


class Cell(Model, InputModel):
    ALIVE = True
    DEAD = False

    _state: bool

    def __init__(self, state: bool):
        super().__init__()
        self._state = state
        self._inputs = state

    def internalStateTransitionFunction(self):
        return 0

    def externalStateTransitionFunction(self, xb: BagOfValues, event_time: float):
        left_state = xb[len(xb.keys())]
        self._state = left_state
        self._inputs = xb

    def outputFunction(self, output_bag: BagOfValues) -> bool:
        return self._state

    def timeAdvanceFunction(self) -> float:
        return 0

    def getState(self) -> bool:
        return self._state
