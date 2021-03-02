from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from core.events.event_bus import subscriber, subscribe
from dynamic_system.events.external_state_transition_event import ExternalStateTransitionEvent

from dynamic_system.control.scheduler import static_scheduler
from dynamic_system.control.input_manager import InputManager


if TYPE_CHECKING:
    from dynamic_system.utils.bag_of_values import BagOfValues
    from dynamic_system.control.scheduler import Scheduler, static_scheduler

from dynamic_system.models.base_model import BaseModel


@subscriber
class Model(BaseModel):
    """A dynamic system that changes in response to its environment and affects
    its environment as it changes
    """

    _input_manager: InputManager
    _last_inputs: BagOfValues
    _scheduler: Scheduler

    def __init__(self, name: str = None, scheduler: Scheduler = static_scheduler):
        super().__init__(name)
        self._scheduler = scheduler
        self._scheduler.schedule(self, self.timeAdvanceFunction())
        self._input_manager = InputManager()
        self._last_inputs = None

    def receiveInput(self, model_id: str, inputs: BagOfValues):
        self._input_manager.saveInput(model_id, inputs)
        if self._input_manager.isReady():
            self._last_inputs = self._input_manager.getInputs()
            out = self.outputFunction(self._last_inputs)
            self.notifyOutput(out)
            self._input_manager.clear()

    def internalTransition(self):
        return self.internalStateTransitionFunction()

    def confluentTransition(self):
        return self.confluentStateTransitionFunction(self._last_inputs)

    @subscribe(ExternalStateTransitionEvent)
    def _externalTransition(self, event: ExternalStateTransitionEvent):
        return self.externalStateTransitionFunction(self._last_inputs, event.getTime())

    def add(self, model: BaseModel):
        self._input_manager.addInput(model.getID())
        model.addListener(self)

    def getOutput(self):
        return self.outputFunction(self._last_inputs)

    @abstractmethod
    def internalStateTransitionFunction(self):
        """Implements the internal state transition function. The internal state transition function computes the next state
        of the model from the state of an autonomous action

         .. math:: \delta_int \; : \; S \longrightarrow S
        """
        pass

    @abstractmethod
    def externalStateTransitionFunction(self, xb: BagOfValues, event_time: float):
        """Implements the external state transition function. The external state transition function computes the
        next state of the model from its current total state Q and a bag xb of inputs in X

         .. math:: \delta_ext \; : \; Q \; x \; X^b \longrightarrow S

        :param xb: Inputs for the transition
        :param event_time: time of event
        """
        pass

    def confluentStateTransitionFunction(self, xb: BagOfValues):
        """Implements the confluent state transition function. The confluent state transition function computes the
        next state of the model from its current state S and a bag xb of inputs in X

         .. math:: \delta_con \; : \; S \; x \; X^b \longrightarrow S

        """
        self.internalStateTransitionFunction()
        return self.externalStateTransitionFunction(xb, self.timeAdvanceFunction())

    @abstractmethod
    def outputFunction(self, output_bag: BagOfValues) -> BagOfValues:
        """Implements the output function. The output function maps the current state S
        to a bag yb of outputs in Y

        .. math:: \lambda \; : \; S \; \longrightarrow Y^b

        :param output_bag: set of bags with elements in Y (outputs set) where state will be mapped
        :returns bag yb of outputs in Y
        """
        pass

    @abstractmethod
    def timeAdvanceFunction(self) -> float:
        """Implement the model’s time advance function.

        :returns time of the autonomous event
        """
        pass
