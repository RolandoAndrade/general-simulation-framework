from __future__ import annotations

from abc import abstractmethod

from typing import TYPE_CHECKING, Dict

from gsf.control.core import SimulationStrategy
from gsf.core.debug.domain.debug import debug
from gsf.core.events import EventBus, static_event_bus
from gsf.core.types import Time

if TYPE_CHECKING:
    from gsf.models.models.discrete_event_model import ModelInput
    from gsf.simulation.core.base_simulator import BaseSimulator


class BaseControl:
    """Simulation control"""

    _simulator: BaseSimulator
    """Simulator to be executed"""

    _is_paused: bool
    """Boolean that indicates if the simulation is paused"""

    _simulation_strategy: SimulationStrategy
    """Strategy for infrastructure details."""

    _event_bus: EventBus
    """Event bus of the module."""

    @debug("Control initialized", True)
    def __init__(
        self,
        simulator: BaseSimulator,
        simulation_strategy: SimulationStrategy,
        event_bus: EventBus = None,
    ):
        """
        Args:
            simulator (BaseSimulator): Simulation engine to be executed.
        """
        self._simulator = simulator
        self._is_paused = True
        self._simulation_strategy = simulation_strategy
        self._event_bus = event_bus or static_event_bus

    @abstractmethod
    def _execute(self, frequency: Time, wait_time: Time, stop_time: Time):
        """Executes the simulation loop number of seconds.

        Args:
            frequency (Time): Frequency of the simulation computation.
            wait_time (Time): Delay execution for a given.
            stop_time (Time): Duration of the simulation.
        """
        raise NotImplementedError

    @abstractmethod
    def start(
        self,
        start_input: Dict[str, ModelInput] = None,
        frequency: Time = 0,
        stop_time: Time = 0,
        wait_time: Time = 0,
    ):
        """Starts the simulation

        Args:
            start_input: Input of the dynamic system.
            frequency (Time): Frequency of the simulation computation.
            stop_time (Time): Time of the simulation
            wait_time (Time): Delay execution for a given number of seconds.
        """
        raise NotImplementedError

    @abstractmethod
    def pause(self):
        """Pauses the simulation"""
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stops the simulation"""
        raise NotImplementedError

    @abstractmethod
    def wait(self, timeout: Time = None):
        """Waits the simulation end

        Args:
            timeout (Time): Time to wait.
        """
        raise NotImplementedError

    def init(self):
        self._is_paused = True
