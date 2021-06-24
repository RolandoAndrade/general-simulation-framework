from __future__ import annotations

from abc import abstractmethod

from typing import TYPE_CHECKING, Dict

from core.debug.domain.debug import debug

if TYPE_CHECKING:
    from models.models.discrete_event_model import ModelInput
    from simulation.core.base_simulator import BaseSimulator


class BaseControl:
    """Simulation control"""

    _simulator: BaseSimulator
    """Simulator to be executed"""

    _isPaused: bool
    """Boolean that indicates if the simulation is paused"""

    @debug("Control initialized", True)
    def __init__(self, simulator: BaseSimulator):
        """
        Args:
            simulator (BaseSimulator): Simulation engine to be executed.
        """
        self._simulator = simulator
        self._isPaused = True

    @abstractmethod
    def _execute(self, frequency: float = 0, wait_time: float = 0):
        """Executes the simulation loop number of seconds.

        Args:
            frequency (float): Frequency of the simulation computation.
            wait_time (float): Delay execution for a given.
        """
        raise NotImplementedError

    @abstractmethod
    def start(
        self,
        start_input: Dict[str, ModelInput] = None,
        frequency: float = 0,
        wait_time: float = 0,
    ):
        """Starts the simulation

        Args:
            start_input: Input of the dynamic system.
            frequency (float): Frequency of the simulation computation.
            wait_time (float): Delay execution for a given number of seconds.
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
