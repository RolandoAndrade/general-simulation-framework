from typing import Any, Dict

from dynamic_system.models.discrete_event_model import DiscreteEventModel


class Phases:
    OUTPUT = 0
    EXEC = 1
    WAIT = 2


class InterruptHandler(DiscreteEventModel):
    _timeToNextEvent: float
    _interruptPeriod: float
    _executePeriod: float
    _phase: int

    def __init__(self, interrupt_period: float, execute_period: float):
        super().__init__()
        self._interruptPeriod = interrupt_period
        self._executePeriod = execute_period
        self.setUpState({
            'status': Phases.WAIT,
            'V': 0,
            'counter': 0
        })

    def internalStateTransitionFunction(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if state['status'] is Phases.WAIT:
            self._timeToNextEvent = self._executePeriod
            state['status'] = Phases.EXEC
        elif state['status'] is Phases.EXEC:
            state['V'] = 5
            state['counter'] += 1
            state['status'] = Phases.OUTPUT
            self._timeToNextEvent = 0
        elif state['status'] is Phases.OUTPUT:
            self._timeToNextEvent = self._interruptPeriod
            state['status'] = Phases.WAIT
        return state

    def externalStateTransitionFunction(self, state: Dict[str, Any], inputs: float, event_time: float) -> Dict[str, Any]:
        self._timeToNextEvent = self._timeToNextEvent - event_time
        state['V'] += inputs
        return state

    def timeAdvanceFunction(self, state: Dict[str, Any]) -> float:
        return self._timeToNextEvent

    def outputFunction(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return state
